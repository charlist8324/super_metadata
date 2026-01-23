import os
from typing import Dict, Any
from database_connections import (
    SYSTEM_DATABASE,
    SUPPORTED_DATABASES,
    DatabaseConfig,
    get_database_config
)


class Config:
    """
    应用程序配置类
    """
    # 从环境变量获取配置，如果没有则使用默认值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-metadata-manager'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # 从统一配置文件获取数据库连接配置
    DATABASE_URL = DatabaseConfig.get_system_database_url()
    
    # 数据库连接池配置
    DB_POOL_CONFIG = DatabaseConfig.get_system_database_pool_config()
    DB_POOL_SIZE = DB_POOL_CONFIG.get('pool_size', 10)
    DB_POOL_MAX_OVERFLOW = DB_POOL_CONFIG.get('max_overflow', 20)
    DB_POOL_RECYCLE = DB_POOL_CONFIG.get('pool_recycle', 3600)
    DB_ECHO = DatabaseConfig.is_echo_enabled()
    
    # 连接参数
    DB_CONNECT_ARGS = DatabaseConfig.get_system_database_connect_args()
    CONNECTION_TIMEOUT = DB_CONNECT_ARGS.get('connect_timeout', 30)
    
    # API配置
    API_VERSION = 'v1'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 支持的数据库类型配置（从统一配置导入）
    SUPPORTED_DATABASES = SUPPORTED_DATABASES
    
    # 查询超时配置（秒）
    QUERY_TIMEOUT = int(os.environ.get('QUERY_TIMEOUT', '60'))
    
    # 元数据抽取配置
    EXTRACTION_BATCH_SIZE = int(os.environ.get('EXTRACTION_BATCH_SIZE', '100'))  # 批量处理表的数量
    EXTRACTION_TIMEOUT = int(os.environ.get('EXTRACTION_TIMEOUT', '3600'))  # 抽取超时时间（秒）
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'metadata_manager.log')


class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    DEBUG = True
    # 开发环境可以覆盖系统数据库URL
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL') or DatabaseConfig.get_system_database_url()


class ProductionConfig(Config):
    """
    生产环境配置
    """
    DEBUG = False
    # 生产环境必须通过环境变量设置数据库URL
    DATABASE_URL = os.environ.get('PROD_DATABASE_URL') or DatabaseConfig.get_system_database_url()
    
    # 生产环境安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'you-must-set-a-secret-key-in-production'
    
    # 生产环境数据库配置（可以覆盖默认值）
    DB_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE', '20'))
    DB_POOL_MAX_OVERFLOW = int(os.environ.get('DB_POOL_MAX_OVERFLOW', '40'))


class TestingConfig(Config):
    """
    测试环境配置
    """
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'sqlite:///:memory:'  # 使用内存数据库进行测试


# 配置字典
config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}