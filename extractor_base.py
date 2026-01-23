import abc
from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from models import DataSource, TableMetadata, ColumnMetadata, ExtractionHistory
from db_config import get_connection_string
from exceptions import DatabaseConnectionException, ExtractionException
import logging
from etl_logger import ETLLogger
import time


class MetadataExtractorBase(abc.ABC):
    """
    元数据抽取器基类
    定义通用的元数据抽取接口
    """
    
    def __init__(self, datasource: DataSource):
        self.datasource = datasource
        self.connection = None
        self.engine = None
        
    def connect(self):
        """连接到数据源"""
        try:
            connection_string = get_connection_string(
                db_type=self.datasource.type,
                host=self.datasource.host,
                port=self.datasource.port,
                username=self.datasource.username,
                password=self.datasource.password,
                database=self.datasource.database
            )
            
            self.engine = create_engine(connection_string)
            self.connection = self.engine.connect()
            
            ETLLogger.log_connection_success(
                self.datasource.name,
                self.datasource.type
            )
            return True
        except Exception as e:
            ETLLogger.log_connection_failed(
                self.datasource.name,
                self.datasource.type,
                str(e)
            )
            logging.error(f"连接数据库失败: {str(e)}")
            raise DatabaseConnectionException(f"连接数据库失败: {str(e)}")
    
    def disconnect(self):
        """断开连接"""
        try:
            if self.connection:
                self.connection.close()
            if self.engine:
                self.engine.dispose()
        except Exception as e:
            logging.error(f"断开数据库连接失败: {str(e)}")
    
    @abc.abstractmethod
    def get_table_list(self) -> List[str]:
        """
        获取数据库中所有表的列表
        :return: 表名列表
        """
        pass
    
    @abc.abstractmethod
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """
        获取指定表的元数据信息
        :param table_name: 表名
        :return: 包含表元数据的字典
        """
        pass
    
    @abc.abstractmethod
    def get_column_metadata(self, table_name: str) -> List[Dict[str, Any]]:
        """
        获取指定表的列元数据信息
        :param table_name: 表名
        :return: 包含列元数据的字典列表
        """
        pass
    
    @abc.abstractmethod
    def get_row_count(self, table_name: str) -> int:
        """
        获取表的行数
        :param table_name: 表名
        :return: 行数
        """
        pass
    
    @abc.abstractmethod
    def get_table_size(self, table_name: str) -> int:
        """
        获取表的数据大小（字节）
        :param table_name: 表名
        :return: 数据大小（字节）
        """
        pass
    
    @abc.abstractmethod
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        """
        获取表之间的关联关系
        :return: 包含表关联关系的字典列表
        """
        pass

    def get_table_update_time(self, table_name: str) -> str:
        """
        获取表的更新时间（用于增量抽取）
        :param table_name: 表名
        :return: 更新时间字符串
        """
        return None

    def extract_all_metadata(self) -> Dict[str, Any]:
        """
        抽取所有表的元数据（全量抽取）
        :return: 包含所有元数据的字典
        """
        return self.extract_metadata(full=True, include_stats=True)

    def extract_incremental_metadata(self, last_sync_time: str = None) -> Dict[str, Any]:
        """
        增量抽取元数据（只抽取新增或变更的表）
        :param last_sync_time: 上次同步时间
        :return: 包含元数据的字典
        """
        return self.extract_metadata(full=False, include_stats=True, last_sync_time=last_sync_time)

    def extract_schema_only_metadata(self) -> Dict[str, Any]:
        """
        仅抽取表结构元数据（不统计行数和数据大小）
        :return: 包含表结构元数据的字典
        """
        return self.extract_metadata(full=True, include_stats=False)

    def extract_metadata(self, full: bool = True, include_stats: bool = True, last_sync_time: str = None) -> Dict[str, Any]:
        """
        通用的元数据抽取方法
        :param full: 是否全量抽取
        :param include_stats: 是否包含统计信息（行数、大小）
        :param last_sync_time: 上次同步时间（用于增量抽取）
        :return: 包含元数据的字典
        """
        start_time = time.time()
        success_tables = 0
        failed_tables = 0
        
        ETLLogger.log_extraction_start(
            self.datasource.id,
            self.datasource.name,
            self.datasource.type
        )
        
        try:
            if not self.connect():
                ETLLogger.log_extraction_failed(
                    self.datasource.id,
                    "无法连接到数据库"
                )
                return {"status": "failed", "message": "无法连接到数据库"}

            tables_data = []
            table_names = self.get_table_list()
            
            ETLLogger.get_logger().info(f"发现 {len(table_names)} 个表")

            for table_name in table_names:
                table_start_time = time.time()
                
                try:
                    # 增量抽取：检查表是否变更
                    if not full and last_sync_time:
                        update_time = self.get_table_update_time(table_name)
                        if not update_time or str(update_time) <= str(last_sync_time):
                            continue  # 跳过未变更的表

                    table_meta = self.get_table_metadata(table_name)
                    column_meta = self.get_column_metadata(table_name)

                    # 根据参数决定是否添加统计信息
                    if include_stats:
                        table_meta['row_count'] = self.get_row_count(table_name)
                        table_meta['size_bytes'] = self.get_table_size(table_name)
                    else:
                        table_meta['row_count'] = 0
                        table_meta['size_bytes'] = 0

                    table_data = {
                        "table_info": table_meta,
                        "columns": column_meta
                    }
                    tables_data.append(table_data)
                    
                    table_duration = time.time() - table_start_time
                    ETLLogger.log_table_extracted(
                        table_name,
                        table_meta['row_count'],
                        table_meta['size_bytes'],
                        table_duration
                    )
                    ETLLogger.log_column_extracted(table_name, len(column_meta))
                    
                    success_tables += 1
                    
                except Exception as e:
                    failed_tables += 1
                    ETLLogger.log_table_failed(table_name, str(e))
                    logging.warning(f"抽取表 {table_name} 失败: {str(e)}")
                    continue

            # 获取表关联关系（只有全量抽取才获取）
            if full:
                relationships = self.get_table_relationships()
                for rel in relationships:
                    ETLLogger.log_relationship_extracted(
                        rel.get('constraint_name', ''),
                        rel.get('table_name', ''),
                        rel.get('referenced_table_name', '')
                    )
            else:
                relationships = []

            total_duration = time.time() - start_time
            
            result = {
                "status": "success",
                "datasource_id": self.datasource.id,
                "tables_count": len(tables_data),
                "tables": tables_data,
                "relationships": relationships,
                "extraction_type": "full" if full else "incremental"
            }
            
            ETLLogger.log_extraction_success(
                self.datasource.id,
                len(tables_data),
                len(relationships),
                total_duration
            )
            
            if failed_tables > 0:
                ETLLogger.log_summary(
                    len(tables_data) + failed_tables,
                    success_tables,
                    failed_tables
                )

            return result

        except Exception as e:
            total_duration = time.time() - start_time
            ETLLogger.log_extraction_failed(
                self.datasource.id,
                str(e)
            )
            logging.error(f"抽取元数据失败: {str(e)}")
            return {"status": "failed", "message": str(e)}
        finally:
            self.disconnect()


class MySQLMetadataExtractor(MetadataExtractorBase):
    """
    MySQL元数据抽取器
    """
    
    def get_table_list(self) -> List[str]:
        query = text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_TYPE = 'BASE TABLE'
        """)
        
        result = self.connection.execute(query, {"database_name": self.datasource.database})
        return [row[0] for row in result.fetchall()]
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        query = text("""
            SELECT 
                TABLE_COMMENT AS comment
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database,
            "table_name": table_name
        }).fetchone()
        
        comment = result.comment if result else ""
        
        return {
            "table_name": table_name,
            "schema_name": self.datasource.database,
            "comment": comment
        }
    
    def get_column_metadata(self, table_name: str) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                ORDINAL_POSITION,
                COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
            ORDER BY ORDINAL_POSITION
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database,
            "table_name": table_name
        })
        
        columns = []
        for row in result:
            columns.append({
                "column_name": row.COLUMN_NAME,
                "data_type": row.DATA_TYPE,
                "is_nullable": row.IS_NULLABLE,
                "default_value": row.COLUMN_DEFAULT,
                "ordinal_position": row.ORDINAL_POSITION,
                "column_comment": row.COLUMN_COMMENT
            })
        
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        query = text(f"SELECT COUNT(*) FROM `{self.datasource.database}`.`{table_name}`")
        try:
            result = self.connection.execute(query).fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 行数失败: {str(e)}, 返回0")
            return 0
    
    def get_table_size(self, table_name: str) -> int:
        query = text("""
            SELECT 
                (DATA_LENGTH + INDEX_LENGTH) AS size_bytes
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        
        try:
            result = self.connection.execute(query, {
                "database_name": self.datasource.database,
                "table_name": table_name
            }).fetchone()
            return result.size_bytes if result and result.size_bytes else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 大小失败: {str(e)}, 返回0")
            return 0
    
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT
                CONSTRAINT_NAME,
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE REFERENCED_TABLE_SCHEMA = :database_name
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)

        result = self.connection.execute(query, {
            "database_name": self.datasource.database
        })

        relationships = []
        for row in result:
            relationships.append({
                "constraint_name": row.CONSTRAINT_NAME,
                "table_name": row.TABLE_NAME,
                "column_name": row.COLUMN_NAME,
                "referenced_table_name": row.REFERENCED_TABLE_NAME,
                "referenced_column_name": row.REFERENCED_COLUMN_NAME,
                "constraint_type": "FOREIGN KEY"
            })

        return relationships

    def get_table_update_time(self, table_name: str) -> str:
        """获取表的更新时间"""
        query = text("""
            SELECT UPDATE_TIME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        try:
            result = self.connection.execute(query, {
                "database_name": self.datasource.database,
                "table_name": table_name
            }).fetchone()
            return str(result.UPDATE_TIME) if result and result.UPDATE_TIME else None
        except Exception:
            return None


class PostgreSQLMetadataExtractor(MetadataExtractorBase):
    """
    PostgreSQL元数据抽取器
    """
    
    def get_table_list(self) -> List[str]:
        query = text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        
        result = self.connection.execute(query)
        return [row[0] for row in result.fetchall()]
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        query = text("""
            SELECT obj_description(c.oid) AS comment
            FROM pg_class c
            JOIN pg_namespace n ON c.relnamespace = n.oid
            WHERE c.relname = :table_name
            AND n.nspname = 'public'
        """)
        
        result = self.connection.execute(query, {"table_name": table_name}).fetchone()
        comment = result.comment if result else ""
        
        return {
            "table_name": table_name,
            "schema_name": "public",
            "comment": comment
        }
    
    def get_column_metadata(self, table_name: str) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                ordinal_position,
                col_description((SELECT c.oid FROM pg_class c JOIN pg_namespace n ON c.relnamespace = n.oid WHERE c.relname = :table_name AND n.nspname = 'public'), ordinal_position) AS column_comment
            FROM information_schema.columns
            WHERE table_name = :table_name
            AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        
        result = self.connection.execute(query, {"table_name": table_name})
        
        columns = []
        for row in result:
            columns.append({
                "column_name": row.column_name,
                "data_type": row.data_type,
                "is_nullable": row.is_nullable,
                "default_value": row.column_default,
                "ordinal_position": row.ordinal_position,
                "column_comment": row.column_comment
            })
        
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        query = text(f"SELECT COUNT(*) FROM public.{table_name}")
        try:
            result = self.connection.execute(query).fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 行数失败: {str(e)}, 返回0")
            return 0
    
    def get_table_size(self, table_name: str) -> int:
        query = text(f"SELECT pg_total_relation_size('{table_name}') AS size_bytes")
        
        try:
            result = self.connection.execute(query).fetchone()
            return result.size_bytes if result and result.size_bytes else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 大小失败: {str(e)}, 返回0")
            return 0
    
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        # PostgreSQL中获取外键关系的查询
        query = text("""
            SELECT
                tc.constraint_name,
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS referenced_table_name,
                ccu.column_name AS referenced_column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public'
        """)

        result = self.connection.execute(query)

        relationships = []
        for row in result:
            relationships.append({
                "constraint_name": row.constraint_name,
                "table_name": row.table_name,
                "column_name": row.column_name,
                "referenced_table_name": row.referenced_table_name,
                "referenced_column_name": row.referenced_column_name,
                "constraint_type": "FOREIGN KEY"
            })

        return relationships

    def get_table_update_time(self, table_name: str) -> str:
        """获取表的更新时间"""
        query = text("""
            SELECT stats.update_time
            FROM pg_stat_all_tables stats
            JOIN pg_class c ON stats.relid = c.oid
            JOIN pg_namespace n ON c.relnamespace = n.oid
            WHERE c.relname = :table_name
            AND n.nspname = 'public'
        """)
        try:
            result = self.connection.execute(query, {"table_name": table_name}).fetchone()
            return str(result.update_time) if result and result.update_time else None
        except Exception:
            return None


class SQLServerMetadataExtractor(MetadataExtractorBase):
    """
    SQL Server元数据抽取器
    """
    
    def get_table_list(self) -> List[str]:
        query = text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            AND TABLE_SCHEMA = 'dbo'
        """)
        
        result = self.connection.execute(query)
        return [row[0] for row in result.fetchall()]
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        query = text("""
            SELECT value AS comment
            FROM sys.extended_properties ep
            INNER JOIN sys.tables t ON ep.major_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE s.name = 'dbo'
            AND t.name = :table_name
            AND ep.name = 'MS_Description'
        """)
        
        result = self.connection.execute(query, {"table_name": table_name}).fetchone()
        comment = result.comment if result else ""
        
        return {
            "table_name": table_name,
            "schema_name": "dbo",
            "comment": comment
        }
    
    def get_column_metadata(self, table_name: str) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.IS_NULLABLE,
                c.COLUMN_DEFAULT,
                c.ORDINAL_POSITION,
                CAST(ep.value AS NVARCHAR(MAX)) AS column_comment,
                c.CHARACTER_MAXIMUM_LENGTH,
                c.NUMERIC_PRECISION,
                c.NUMERIC_SCALE,
                c.DATETIME_PRECISION
            FROM INFORMATION_SCHEMA.COLUMNS c
            LEFT JOIN sys.extended_properties ep ON OBJECT_ID(c.TABLE_SCHEMA + '.' + c.TABLE_NAME) = ep.major_id
                AND c.ORDINAL_POSITION = ep.minor_id
                AND ep.name = 'MS_Description'
            WHERE c.TABLE_NAME = :table_name
            AND c.TABLE_SCHEMA = 'dbo'
            ORDER BY c.ORDINAL_POSITION
        """)
        
        result = self.connection.execute(query, {"table_name": table_name})
        
        columns = []
        for row in result:
            # 构建完整的数据类型字符串（包含长度、精度等）
            data_type = row.DATA_TYPE
            
            # 根据不同的数据类型添加长度/精度信息
            if data_type in ('varchar', 'char', 'nvarchar', 'nchar', 'binary', 'varbinary'):
                # 字符串和二进制类型：使用 CHARACTER_MAXIMUM_LENGTH
                if row.CHARACTER_MAXIMUM_LENGTH and row.CHARACTER_MAXIMUM_LENGTH != -1:
                    data_type = f"{data_type}({row.CHARACTER_MAXIMUM_LENGTH})"
                elif row.CHARACTER_MAXIMUM_LENGTH == -1:
                    # -1 表示 MAX 类型（如 varchar(max)）
                    data_type = f"{data_type}(max)"
            elif data_type in ('decimal', 'numeric'):
                # 十进制类型：使用精度和小数位数
                if row.NUMERIC_PRECISION:
                    scale = row.NUMERIC_SCALE if row.NUMERIC_SCALE else 0
                    data_type = f"{data_type}({row.NUMERIC_PRECISION},{scale})"
            elif data_type == 'float':
                # FLOAT 类型：使用精度
                if row.NUMERIC_PRECISION:
                    data_type = f"{data_type}({row.NUMERIC_PRECISION})"
            elif data_type in ('datetime2', 'datetimeoffset', 'time'):
                # 高精度日期时间类型：使用 DATETIME_PRECISION
                if row.DATETIME_PRECISION:
                    data_type = f"{data_type}({row.DATETIME_PRECISION})"
            
            columns.append({
                "column_name": row.COLUMN_NAME,
                "data_type": data_type,
                "is_nullable": row.IS_NULLABLE,
                "default_value": row.COLUMN_DEFAULT,
                "ordinal_position": row.ORDINAL_POSITION,
                "column_comment": row.column_comment if row.column_comment else ""
            })
        
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        query = text(f"SELECT COUNT(*) FROM dbo.{table_name}")
        try:
            result = self.connection.execute(query).fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 行数失败: {str(e)}, 返回0")
            return 0
    
    def get_table_size(self, table_name: str) -> int:
        query = text(f"""
            SELECT SUM(a.total_pages) * 8 * 1024 AS size_bytes
            FROM sys.tables t
            INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
            INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
            INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
            WHERE t.NAME = :table_name
            AND t.is_ms_shipped = 0
        """)
        
        try:
            result = self.connection.execute(query, {"table_name": table_name}).fetchone()
            return result.size_bytes if result and result.size_bytes else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 大小失败: {str(e)}, 返回0")
            return 0
    
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT
                fk.name AS constraint_name,
                t1.name AS table_name,
                c1.name AS column_name,
                t2.name AS referenced_table_name,
                c2.name AS referenced_column_name
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables t1 ON fk.parent_object_id = t1.object_id
            INNER JOIN sys.columns c1 ON fkc.parent_object_id = c1.object_id AND fkc.parent_column_id = c1.column_id
            INNER JOIN sys.tables t2 ON fk.referenced_object_id = t2.object_id
            INNER JOIN sys.columns c2 ON fkc.referenced_object_id = c2.object_id AND fkc.referenced_column_id = c2.column_id
            WHERE t1.schema_id = SCHEMA_ID('dbo')
            AND t2.schema_id = SCHEMA_ID('dbo')
        """)

        result = self.connection.execute(query)

        relationships = []
        for row in result:
            relationships.append({
                "constraint_name": row.constraint_name,
                "table_name": row.table_name,
                "column_name": row.column_name,
                "referenced_table_name": row.referenced_table_name,
                "referenced_column_name": row.referenced_column_name,
                "constraint_type": "FOREIGN KEY"
            })

        return relationships

    def get_table_update_time(self, table_name: str) -> str:
        """获取表的更新时间"""
        # 注意：SQL Server 的 STATS_DATE 返回的是统计信息更新时间，而不是数据修改时间
        # 这可能无法准确反映表数据的最后修改时间
        # 建议在 SQL Server 中使用全量抽取或通过触发器/时间戳字段来跟踪数据变更
        query = text("""
            SELECT STATS_DATE(OBJECT_ID(:table_name), 1) AS update_time
        """)
        try:
            result = self.connection.execute(query, {"table_name": table_name}).fetchone()
            return str(result.update_time) if result and result.update_time else None
        except Exception:
            return None


class OracleMetadataExtractor(MetadataExtractorBase):
    """
    Oracle元数据抽取器
    """
    
    def get_table_list(self) -> List[str]:
        query = text("""
            SELECT table_name 
            FROM user_tables
        """)
        
        result = self.connection.execute(query)
        return [row[0].lower() for row in result.fetchall()]
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        query = text("""
            SELECT comments
            FROM user_tab_comments
            WHERE table_name = UPPER(:table_name)
        """)
        
        result = self.connection.execute(query, {"table_name": table_name}).fetchone()
        comment = result.comments if result else ""
        
        return {
            "table_name": table_name.lower(),
            "schema_name": self.datasource.username.upper(),
            "comment": comment
        }
    
    def get_column_metadata(self, table_name: str) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                c.column_name,
                c.data_type,
                CASE c.nullable WHEN 'Y' THEN 'YES' ELSE 'NO' END AS is_nullable,
                c.data_default AS column_default,
                c.column_id AS ordinal_position,
                com.comments AS column_comment,
                c.char_length,
                c.data_length,
                c.data_precision,
                c.data_scale
            FROM user_tab_columns c
            LEFT JOIN user_col_comments com 
                ON c.table_name = com.table_name 
                AND c.column_name = com.column_name
            WHERE c.table_name = UPPER(:table_name)
            ORDER BY c.column_id
        """)
        
        result = self.connection.execute(query, {"table_name": table_name})
        
        columns = []
        for row in result:
            # 构建完整的数据类型字符串（包含长度、精度等）
            data_type = row.data_type.lower()
            
            # 根据不同的数据类型添加长度/精度信息
            if data_type in ('varchar2', 'char', 'nvarchar2', 'nchar'):
                # 字符类型：使用 char_length 或 data_length
                length = row.char_length if row.char_length else row.data_length
                if length:
                    data_type = f"{data_type}({length})"
            elif data_type == 'number':
                # 数字类型：精度和小数位数
                precision = row.data_precision
                scale = row.data_scale
                if precision:
                    if scale and scale > 0:
                        data_type = f"{data_type}({precision},{scale})"
                    else:
                        data_type = f"{data_type}({precision})"
            elif data_type in ('raw', 'float'):
                # RAW 和 FLOAT 类型使用 length
                if row.data_length:
                    data_type = f"{data_type}({row.data_length})"
            
            columns.append({
                "column_name": row.column_name.lower(),
                "data_type": data_type,
                "is_nullable": row.is_nullable,
                "default_value": row.column_default,
                "ordinal_position": row.ordinal_position,
                "column_comment": row.column_comment if row.column_comment else ""
            })
        
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        query = text(f"SELECT COUNT(*) FROM {self.datasource.username.upper()}.{table_name.upper()}")
        try:
            result = self.connection.execute(query).fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 行数失败: {str(e)}, 返回0")
            return 0
    
    def get_table_size(self, table_name: str) -> int:
        query = text("""
            SELECT bytes
            FROM user_segments
            WHERE segment_name = UPPER(:table_name)
            AND segment_type = 'TABLE'
        """)
        
        try:
            result = self.connection.execute(query, {"table_name": table_name}).fetchone()
            return result.bytes if result and result.bytes else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 大小失败: {str(e)}, 返回0")
            return 0
    
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT
                fk.constraint_name,
                fk.table_name,
                fk_col.column_name,
                pk.table_name AS referenced_table_name,
                pk_col.column_name AS referenced_column_name
            FROM user_constraints fk
            JOIN user_cons_columns fk_col 
                ON fk.constraint_name = fk_col.constraint_name 
                AND fk.table_name = fk_col.table_name
            JOIN user_constraints pk 
                ON fk.r_constraint_name = pk.constraint_name
            JOIN user_cons_columns pk_col 
                ON pk.constraint_name = pk_col.constraint_name 
                AND pk.table_name = pk_col.table_name
                AND fk_col.position = pk_col.position
            WHERE fk.constraint_type = 'R'
        """)

        result = self.connection.execute(query)

        relationships = []
        for row in result:
            relationships.append({
                "constraint_name": row.constraint_name,
                "table_name": row.table_name.lower(),
                "column_name": row.column_name.lower(),
                "referenced_table_name": row.referenced_table_name.lower(),
                "referenced_column_name": row.referenced_column_name.lower(),
                "constraint_type": "FOREIGN KEY"
            })

        return relationships

    def get_table_update_time(self, table_name: str) -> str:
        """获取表的更新时间"""
        query = text("""
            SELECT last_ddl_time
            FROM user_objects
            WHERE object_name = UPPER(:table_name)
            AND object_type = 'TABLE'
        """)
        try:
            result = self.connection.execute(query, {"table_name": table_name}).fetchone()
            return str(result.last_ddl_time) if result and result.last_ddl_time else None
        except Exception:
            return None

class StarRocksMetadataExtractor(MySQLMetadataExtractor):
    """
    StarRocks元数据抽取器
    StarRocks是基于MySQL协议的MPP数据库，可以复用MySQL的大部分逻辑
    """
    
    def get_table_list(self) -> List[str]:
        """获取StarRocks中所有表的列表"""
        query = text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_TYPE = 'BASE TABLE'
        """)
        
        result = self.connection.execute(query, {"database_name": self.datasource.database})
        return [row[0] for row in result.fetchall()]
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """获取指定表的元数据"""
        query = text("""
            SELECT 
                TABLE_COMMENT AS comment
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database,
            "table_name": table_name
        }).fetchone()
        
        comment = result.TABLE_COMMENT if result else ""
        
        return {
            "table_name": table_name,
            "schema_name": self.datasource.database,
            "comment": comment
        }
    
    def get_column_metadata(self, table_name: str) -> List[Dict[str, Any]]:
        """获取指定表的列元数据信息"""
        query = text("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                ORDINAL_POSITION,
                COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
            ORDER BY ORDINAL_POSITION
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database,
            "table_name": table_name
        })
        
        columns = []
        for row in result:
            columns.append({
                "column_name": row.COLUMN_NAME,
                "data_type": row.DATA_TYPE,
                "is_nullable": row.IS_NULLABLE,
                "default_value": row.COLUMN_DEFAULT,
                "ordinal_position": row.ORDINAL_POSITION,
                "column_comment": row.COLUMN_COMMENT
            })
        
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        """获取表的行数"""
        # StarRocks使用MySQL语法，可以用SELECT COUNT(*)
        query = text(f"SELECT COUNT(*) FROM `{self.datasource.database}`.`{table_name}`")
        try:
            result = self.connection.execute(query).fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 行数失败: {str(e)}, 返回0")
            return 0
    
    def get_table_size(self, table_name: str) -> int:
        """获取表的数据大小（字节）"""
        # StarRocks使用MySQL的INFORMATION_SCHEMA
        query = text("""
            SELECT 
                (DATA_LENGTH + INDEX_LENGTH) AS size_bytes
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        
        try:
            result = self.connection.execute(query, {
                "database_name": self.datasource.database,
                "table_name": table_name
            }).fetchone()
            return result.size_bytes if result and result.size_bytes else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 大小失败: {str(e)}, 返回0")
            return 0
    
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        """获取表之间的关联关系（StarRocks兼容MySQL的查询）"""
        query = text("""
            SELECT 
                CONSTRAINT_NAME,
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = :database_name
            AND REFERENCED_TABLE_SCHEMA = :database_name
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database
        })
        
        relationships = []
        for row in result:
            relationships.append({
                "constraint_name": row.CONSTRAINT_NAME,
                "table_name": row.TABLE_NAME,
                "column_name": row.COLUMN_NAME,
                "referenced_table_name": row.REFERENCED_TABLE_NAME,
                "referenced_column_name": row.REFERENCED_COLUMN_NAME,
                "constraint_type": "FOREIGN KEY"
            })
        
        return relationships
    
    def get_table_update_time(self, table_name: str) -> str:
        """获取表的更新时间"""
        query = text("""
            SELECT UPDATE_TIME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        try:
            result = self.connection.execute(query, {
                "database_name": self.datasource.database,
                "table_name": table_name
            }).fetchone()
            return str(result.UPDATE_TIME) if result and result.UPDATE_TIME else None
        except Exception:
            return None


class StarRocksMetadataExtractor(MetadataExtractorBase):
    """
    StarRocks元数据抽取器
    StarRocks是基于MySQL协议的MPP数据库
    """
    
    def get_table_list(self) -> List[str]:
        """获取StarRocks中所有表的列表"""
        query = text("""
            SELECT TABLE_NAME 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_TYPE = 'BASE TABLE'
        """)
        
        result = self.connection.execute(query, {"database_name": self.datasource.database})
        return [row.TABLE_NAME for row in result.fetchall()]
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """获取指定表的元数据"""
        query = text("""
            SELECT 
                TABLE_NAME,
                TABLE_SCHEMA,
                TABLE_COMMENT
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database,
            "table_name": table_name
        }).fetchone()
        
        if result:
            return {
                "table_name": result.TABLE_NAME,
                "schema_name": result.TABLE_SCHEMA,
                "comment": result.TABLE_COMMENT if result.TABLE_COMMENT else ""
            }
        else:
            return {
                "table_name": table_name,
                "schema_name": self.datasource.database,
                "comment": ""
            }
    
    def get_column_metadata(self, table_name: str) -> List[Dict[str, Any]]:
        """获取指定表的列元数据信息"""
        query = text("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                ORDINAL_POSITION,
                COLUMN_COMMENT
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
            ORDER BY ORDINAL_POSITION
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database,
            "table_name": table_name
        })
        
        columns = []
        for row in result:
            columns.append({
                "column_name": row.COLUMN_NAME,
                "data_type": row.DATA_TYPE,
                "is_nullable": row.IS_NULLABLE,
                "default_value": row.COLUMN_DEFAULT,
                "ordinal_position": row.ORDINAL_POSITION,
                "column_comment": row.COLUMN_COMMENT if row.COLUMN_COMMENT else ""
            })
        
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        """获取表的行数"""
        full_table_name = f"`{self.datasource.database}`.`{table_name}`"
        query = text(f"SELECT COUNT(*) FROM {full_table_name}")
        try:
            result = self.connection.execute(query).fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 行数失败: {str(e)}, 返回0")
            return 0
    
    def get_table_size(self, table_name: str) -> int:
        """获取表的数据大小（字节）"""
        try:
            query = text(f"SHOW DATA FROM `{self.datasource.database}`.`{table_name}`")
            results = self.connection.execute(query).fetchall()
            
            if not results:
                logging.warning(f"表 {table_name} 的 SHOW DATA 命令未返回结果")
                return 0
            
            for row in results:
                try:
                    # 跳过总计行
                    if len(row) >= 2 and str(row[1]).upper() == 'TOTAL':
                        continue
                    
                    # SHOW DATA返回格式: (TableName1, TableName2, Size, ReplicaCount, RowCount)
                    # Size在索引2的位置
                    if len(row) >= 3:
                        size_str = str(row[2]).strip().upper()
                        logging.info(f"表 {table_name} 的原始大小: {size_str}")
                        
                        size_bytes = 0
                        if 'KB' in size_str:
                            size_bytes = int(float(size_str.replace('KB', '').strip()) * 1024)
                        elif 'MB' in size_str:
                            size_bytes = int(float(size_str.replace('MB', '').strip()) * 1024 * 1024)
                        elif 'GB' in size_str:
                            size_bytes = int(float(size_str.replace('GB', '').strip()) * 1024 * 1024 * 1024)
                        elif 'TB' in size_str:
                            size_bytes = int(float(size_str.replace('TB', '').strip()) * 1024 * 1024 * 1024 * 1024)
                        else:
                            try:
                                size_bytes = int(size_str)
                            except:
                                size_bytes = 0
                        
                        logging.info(f"表 {table_name} 的解析后大小: {size_bytes} 字节")
                        return size_bytes
                except Exception as e:
                    logging.warning(f"解析表 {table_name} 大小失败: {str(e)}")
                    continue
            
            logging.warning(f"表 {table_name} 未找到有效的大小信息")
            return 0
        except Exception as e:
            logging.warning(f"获取表 {table_name} 大小失败: {str(e)}, 返回0")
            return 0
    
    def get_table_relationships(self) -> List[Dict[str, Any]]:
        """获取表之间的关联关系"""
        query = text("""
            SELECT 
                CONSTRAINT_NAME,
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = :database_name
            AND REFERENCED_TABLE_SCHEMA = :database_name
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        
        result = self.connection.execute(query, {
            "database_name": self.datasource.database
        })
        
        relationships = []
        for row in result:
            relationships.append({
                "constraint_name": row.CONSTRAINT_NAME,
                "table_name": row.TABLE_NAME,
                "column_name": row.COLUMN_NAME,
                "referenced_table_name": row.REFERENCED_TABLE_NAME,
                "referenced_column_name": row.REFERENCED_COLUMN_NAME,
                "constraint_type": "FOREIGN KEY"
            })
        
        return relationships
    
    def get_table_update_time(self, table_name: str) -> str:
        """获取表的更新时间"""
        query = text("""
            SELECT UPDATE_TIME
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = :database_name
            AND TABLE_NAME = :table_name
        """)
        try:
            result = self.connection.execute(query, {
                "database_name": self.datasource.database,
                "table_name": table_name
            }).fetchone()
            return str(result.UPDATE_TIME) if result and result.UPDATE_TIME else None
        except Exception:
            return None


def init_database():
    """初始化数据库表"""
    from db_manager import db_manager
    if db_manager is None:
        raise Exception("数据库管理器未初始化")
    Base.metadata.create_all(bind=db_manager.engine)
    return db_manager.engine
