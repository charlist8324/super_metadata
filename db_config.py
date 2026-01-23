import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from exceptions import DatabaseConnectionException
import logging

# 从统一配置文件导入数据库连接配置
from database_connections import (
    SYSTEM_DATABASE,
    DatabaseConfig as DBConfig,
    get_connection_string,
    SUPPORTED_DATABASES
)


class DatabaseConfig:
    """
    数据库配置类（系统数据库连接）
    
    注意：现在所有数据库连接配置都在 database_connections.py 中统一管理
    """
    def __init__(self):
        # 从统一配置文件获取数据库URL
        self.database_url = DBConfig.get_system_database_url()
        self.engine = None
        self.SessionLocal = None
        
    def init_db(self):
        """初始化数据库引擎"""
        try:
            # 从统一配置获取连接池参数
            pool_config = DBConfig.get_system_database_pool_config()
            connect_args = DBConfig.get_system_database_connect_args()
            
            self.engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=pool_config.get('pool_size', 10),
                max_overflow=pool_config.get('max_overflow', 20),
                pool_recycle=pool_config.get('pool_recycle', 3600),
                pool_pre_ping=pool_config.get('pool_pre_ping', True),
                echo=DBConfig.is_echo_enabled(),
                connect_args=connect_args
            )
              
            # 创建会话工厂
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
              
            return self.engine
        except Exception as e:
            logging.error(f"数据库引擎初始化失败: {str(e)}")
            raise DatabaseConnectionException(f"数据库引擎初始化失败: {str(e)}")
    
    @contextmanager
    def get_session(self):
        """获取数据库会话的上下文管理器"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"数据库会话错误: {str(e)}")
            raise DatabaseConnectionException(f"数据库操作失败: {str(e)}")
        finally:
            session.close()


# 支持的数据库类型映射（从统一配置导入）
# 保留此常量以保持向后兼容
SUPPORTED_DATABASES = SUPPORTED_DATABASES


# get_connection_string 函数从统一配置导入
# 保留此函数引用以保持向后兼容
__all__ = [
    'DatabaseConfig',
    'SUPPORTED_DATABASES',
    'get_connection_string',
]
