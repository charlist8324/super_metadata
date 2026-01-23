"""
数据库连接管理器
"""
from contextlib import contextmanager
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DatabaseConnectionException


class DatabaseManager:
    """
    数据库连接管理器，提供连接池和会话管理
    """
    def __init__(self, database_url, pool_size=10, max_overflow=20):
        self.database_url = database_url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.engine = None
        self.SessionLocal = None
        self._init_engine()

    def _init_engine(self):
        """初始化数据库引擎"""
        try:
            self.engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_pre_ping=True,
                echo=False,
                connect_args={
                    'connect_timeout': 30,
                    'charset': 'utf8mb4'
                }
            )
            self.SessionLocal = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self.engine
            )
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

    def test_connection(self):
        """测试数据库连接"""
        try:
            with self.get_session() as session:
                # 测试连接
                result = session.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            logging.error(f"数据库连接测试失败: {str(e)}")
            return False

    def execute_query(self, query, params=None):
        """执行查询"""
        try:
            with self.get_session() as session:
                if params:
                    result = session.execute(text(query), params)
                else:
                    result = session.execute(text(query))
                session.commit()
                return result
        except SQLAlchemyError as e:
            logging.error(f"SQL执行错误: {str(e)}")
            raise DatabaseConnectionException(f"SQL执行失败: {str(e)}")
        except Exception as e:
            logging.error(f"执行查询失败: {str(e)}")
            raise DatabaseConnectionException(f"执行查询失败: {str(e)}")


# 全球数据库管理器实例
db_manager = None


def init_db_manager(database_url):
    """初始化数据库管理器"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    return db_manager


def get_db():
    """获取数据库会话生成器（用于依赖注入）"""
    if db_manager is None:
        raise DatabaseConnectionException("数据库管理器未初始化")
    return db_manager.get_session()


def get_db_session():
    """直接获取数据库会话"""
    if db_manager is None:
        raise DatabaseConnectionException("数据库管理器未初始化")
    return db_manager.get_session()