"""
ETL日志记录模块

用于记录所有ETL（抽取、转换、加载）过程的详细日志
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class ETLLogger:
    """ETL日志记录器"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls):
        """获取ETL日志记录器单例"""
        if cls._logger is None:
            cls._logger = cls._setup_logger()
        return cls._logger
    
    @classmethod
    def _setup_logger(cls):
        """设置ETL日志记录器"""
        
        logger = logging.getLogger('etl')
        logger.setLevel(logging.INFO)
        
        if logger.handlers:
            return logger
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        log_dir = Path(__file__).parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / 'etl.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @classmethod
    def log_extraction_start(cls, source_id, source_name, source_type):
        """记录抽数开始"""
        logger = cls.get_logger()
        logger.info("=" * 80)
        logger.info(f"开始抽数 - 数据源ID: {source_id}, 名称: {source_name}, 类型: {source_type}")
        logger.info("=" * 80)
    
    @classmethod
    def log_extraction_success(cls, source_id, tables_count, relationships_count, duration=None):
        """记录抽数成功"""
        logger = cls.get_logger()
        msg = f"抽数成功 - 数据源ID: {source_id}, 抽取表数量: {tables_count}, 关联关系数量: {relationships_count}"
        if duration:
            msg += f", 耗时: {duration:.2f}秒"
        logger.info(msg)
        logger.info("=" * 80)
        logger.info("")
    
    @classmethod
    def log_extraction_failed(cls, source_id, error_msg):
        """记录抽数失败"""
        logger = cls.get_logger()
        logger.error(f"抽数失败 - 数据源ID: {source_id}, 错误: {error_msg}")
        logger.error("=" * 80)
        logger.error("")
    
    @classmethod
    def log_table_extracted(cls, table_name, row_count, size_bytes, duration=None):
        """记录表抽取成功"""
        logger = cls.get_logger()
        size_mb = size_bytes / (1024 * 1024) if size_bytes else 0
        msg = f"  ✓ 抽取表: {table_name}, 行数: {row_count}, 大小: {size_mb:.2f}MB"
        if duration:
            msg += f", 耗时: {duration:.2f}秒"
        logger.info(msg)
    
    @classmethod
    def log_table_failed(cls, table_name, error_msg):
        """记录表抽取失败"""
        logger = cls.get_logger()
        logger.warning(f"  ✗ 抽取表失败: {table_name}, 错误: {error_msg}")
    
    @classmethod
    def log_column_extracted(cls, table_name, column_count):
        """记录列抽取"""
        logger = cls.get_logger()
        logger.info(f"    - 表 {table_name} 抽取到 {column_count} 个列")
    
    @classmethod
    def log_relationship_extracted(cls, constraint_name, table_name, ref_table_name):
        """记录关联关系抽取"""
        logger = cls.get_logger()
        logger.info(f"    - 关联关系: {table_name} -> {ref_table_name} ({constraint_name})")
    
    @classmethod
    def log_clear_old_metadata(cls, source_id, tables_count):
        """记录清除旧元数据"""
        logger = cls.get_logger()
        logger.info(f"清除旧元数据 - 数据源ID: {source_id}, 删除表数量: {tables_count}")
    
    @classmethod
    def log_save_metadata(cls, source_id, tables_count, columns_count, relationships_count):
        """记录保存元数据"""
        logger = cls.get_logger()
        logger.info(f"保存元数据到数据库 - 数据源ID: {source_id}")
        logger.info(f"  表数量: {tables_count}, 列数量: {columns_count}, 关联关系数量: {relationships_count}")
    
    @classmethod
    def log_connection_success(cls, source_name, source_type):
        """记录连接成功"""
        logger = cls.get_logger()
        logger.info(f"数据库连接成功 - {source_type}: {source_name}")
    
    @classmethod
    def log_connection_failed(cls, source_name, source_type, error_msg):
        """记录连接失败"""
        logger = cls.get_logger()
        logger.error(f"数据库连接失败 - {source_type}: {source_name}, 错误: {error_msg}")
    
    @classmethod
    def log_summary(cls, total_tables, success_tables, failed_tables):
        """记录汇总信息"""
        logger = cls.get_logger()
        logger.info("-" * 80)
        logger.info(f"抽数汇总 - 总表数: {total_tables}, 成功: {success_tables}, 失败: {failed_tables}")
        logger.info("-" * 80)


def get_etl_logger():
    """获取ETL日志记录器"""
    return ETLLogger.get_logger()
