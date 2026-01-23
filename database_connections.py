"""
统一数据库连接配置文件

所有数据库的连接配置都在这里集中管理
包括：
1. 系统数据库（元数据存储库）配置
2. 支持的数据库类型配置
3. 数据库连接字符串生成函数
"""

import os
from urllib.parse import quote_plus
from typing import Dict, Any


# ============================================================================
# 系统数据库（元数据存储库）配置
# ============================================================================

# 系统数据库连接配置
# 这是用来存储元数据的数据源（通常是MySQL）
SYSTEM_DATABASE = {
    # 默认连接URL
    'url': os.environ.get('DATABASE_URL', 
                        'mysql+pymysql://root:Admin%40900@10.178.80.101:3306/meta_db?charset=utf8mb4'),
    
    # 连接池配置
    'pool': {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', '10')),
        'max_overflow': int(os.environ.get('DB_POOL_MAX_OVERFLOW', '20')),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', '3600')),  # 1小时
        'pool_pre_ping': True,
    },
    
    # 连接参数
    'connect_args': {
        'connect_timeout': int(os.environ.get('CONNECTION_TIMEOUT', '30')),
        'charset': 'utf8mb4'
    },
    
    # 是否输出SQL语句（用于调试）
    'echo': os.environ.get('DB_ECHO', 'False').lower() == 'true',
}


# ============================================================================
# 支持的数据库类型配置
# ============================================================================

SUPPORTED_DATABASES = {
    'mysql': {
        'driver': 'pymysql',
        'port': 3306,
        'dialect': 'mysql',
        'test_query': 'SELECT 1',
        'name': 'MySQL',
        'description': 'MySQL数据库',
    },
    'postgresql': {
        'driver': 'psycopg2',
        'port': 5432,
        'dialect': 'postgresql',
        'test_query': 'SELECT 1',
        'name': 'PostgreSQL',
        'description': 'PostgreSQL数据库',
    },
    'sqlserver': {
        'driver': 'pyodbc',
        'port': 1433,
        'dialect': 'mssql',
        'test_query': 'SELECT 1',
        'name': 'SQL Server',
        'description': 'Microsoft SQL Server',
    },
    'oracle': {
        'driver': 'oracledb',
        'port': 1521,
        'dialect': 'oracle',
        'test_query': 'SELECT 1 FROM DUAL',
        'name': 'Oracle',
        'description': 'Oracle数据库',
        'note': '使用 oracledb 瘦模式，无需 Oracle Instant Client',
    },
    'starrocks': {
        'driver': 'pymysql',
        'port': 9030,
        'dialect': 'mysql',
        'test_query': 'SELECT 1',
        'name': 'StarRocks',
        'description': 'StarRocks数据库（基于MySQL协议）',
    },
}


# ============================================================================
# 数据库连接字符串生成函数
# ============================================================================

def get_connection_string(db_type: str, host: str, port: int, 
                        username: str, password: str, database: str) -> str:
    """
    根据数据库类型生成SQLAlchemy连接字符串
    
    参数:
        db_type: 数据库类型（mysql, postgresql, sqlserver, oracle, starrocks）
        host: 数据库主机地址
        port: 数据库端口
        username: 数据库用户名
        password: 数据库密码
        database: 数据库名称/服务名/SID
    
    返回:
        SQLAlchemy连接字符串
    
    示例:
        mysql -> mysql+pymysql://user:pass@host:3306/db
        postgresql -> postgresql+psycopg2://user:pass@host:5432/db
        sqlserver -> mssql+pyodbc://user:pass@host:1433/db?driver=ODBC+Driver+17+for+SQL+Server
        oracle -> oracle+oracledb://user:pass@host:1521/orcl
        starrocks -> mysql+pymysql://user:pass@host:9030/db
    """
    # 检查数据库类型是否支持
    if db_type not in SUPPORTED_DATABASES:
        supported_types = ', '.join(SUPPORTED_DATABASES.keys())
        raise ValueError(f"不支持的数据库类型: {db_type}。支持的类型: {supported_types}")
    
    config = SUPPORTED_DATABASES[db_type]
    
    # URL编码用户名和密码，防止特殊字符造成问题
    encoded_username = quote_plus(str(username))
    encoded_password = quote_plus(str(password))
    encoded_database = quote_plus(str(database))
    
    # 根据数据库类型生成连接字符串
    if db_type == 'mysql':
        connection_string = f"mysql+pymysql://{encoded_username}:{encoded_password}@{host}:{port}/{encoded_database}"
        
    elif db_type == 'starrocks':
        # StarRocks使用MySQL协议，连接字符串与MySQL相同
        connection_string = f"mysql+pymysql://{encoded_username}:{encoded_password}@{host}:{port}/{encoded_database}"
        
    elif db_type == 'postgresql':
        connection_string = f"postgresql+psycopg2://{encoded_username}:{encoded_password}@{host}:{port}/{encoded_database}"
        
    elif db_type == 'sqlserver':
        # SQL Server需要额外的参数
        connection_string = f"mssql+pyodbc://{encoded_username}:{encoded_password}@{host}:{port}/{encoded_database}?driver=ODBC+Driver+17+for+SQL+Server"
        
    elif db_type == 'oracle':
        # 使用 oracledb 驱动（纯 Python 实现，无需 Oracle Instant Client）
        # DSN 格式：host:port/service_name 或 host:port/SID
        connection_string = f"oracle+oracledb://{encoded_username}:{encoded_password}@{host}:{port}/{encoded_database}"
        
    else:
        raise ValueError(f"未知的数据库类型: {db_type}")
    
    return connection_string


def get_database_config(db_type: str) -> Dict[str, Any]:
    """
    获取指定数据库类型的配置
    
    参数:
        db_type: 数据库类型
    
    返回:
        数据库配置字典
    """
    if db_type not in SUPPORTED_DATABASES:
        raise ValueError(f"不支持的数据库类型: {db_type}")
    
    return SUPPORTED_DATABASES[db_type].copy()


def get_default_port(db_type: str) -> int:
    """
    获取指定数据库类型的默认端口
    
    参数:
        db_type: 数据库类型
    
    返回:
        默认端口号
    """
    config = get_database_config(db_type)
    return config['port']


def is_database_supported(db_type: str) -> bool:
    """
    检查数据库类型是否支持
    
    参数:
        db_type: 数据库类型
    
    返回:
        是否支持
    """
    return db_type in SUPPORTED_DATABASES


def get_supported_database_types() -> list:
    """
    获取所有支持的数据库类型列表
    
    返回:
        数据库类型列表
    """
    return list(SUPPORTED_DATABASES.keys())


def get_database_name(db_type: str) -> str:
    """
    获取数据库类型的显示名称
    
    参数:
        db_type: 数据库类型
    
    返回:
        数据库显示名称
    """
    config = get_database_config(db_type)
    return config.get('name', db_type.upper())


# ============================================================================
# 环境特定配置
# ============================================================================

class DatabaseConfig:
    """
    数据库配置类（用于向后兼容）
    现在从统一配置文件读取配置
    """
    
    @staticmethod
    def get_system_database_url() -> str:
        """获取系统数据库URL"""
        return SYSTEM_DATABASE['url']
    
    @staticmethod
    def get_system_database_pool_config() -> Dict[str, Any]:
        """获取系统数据库连接池配置"""
        return SYSTEM_DATABASE['pool'].copy()
    
    @staticmethod
    def get_system_database_connect_args() -> Dict[str, Any]:
        """获取系统数据库连接参数"""
        return SYSTEM_DATABASE['connect_args'].copy()
    
    @staticmethod
    def is_echo_enabled() -> bool:
        """是否启用SQL输出"""
        return SYSTEM_DATABASE['echo']


# ============================================================================
# 配置验证
# ============================================================================

def validate_database_connection(db_type: str, host: str, port: int, 
                              username: str, password: str, database: str) -> tuple:
    """
    验证数据库连接配置
    
    参数:
        db_type: 数据库类型
        host: 数据库主机地址
        port: 数据库端口
        username: 数据库用户名
        password: 数据库密码
        database: 数据库名称
    
    返回:
        (is_valid, error_message)
        is_valid: 配置是否有效
        error_message: 错误消息（如果无效）
    """
    errors = []
    
    # 检查数据库类型
    if not is_database_supported(db_type):
        errors.append(f"不支持的数据库类型: {db_type}")
    
    # 检查必需参数
    if not host:
        errors.append("主机地址不能为空")
    if not port or port <= 0 or port > 65535:
        errors.append("端口号必须在 1-65535 之间")
    if not username:
        errors.append("用户名不能为空")
    if not password:
        errors.append("密码不能为空")
    if not database:
        errors.append("数据库名称不能为空")
    
    # 检查数据库特定要求
    if db_type == 'oracle' and len(database) > 30:
        errors.append("Oracle 服务名/SID 长度不能超过30个字符")
    
    if errors:
        return False, '; '.join(errors)
    
    return True, None


# ============================================================================
# 导出的配置和函数
# ============================================================================

__all__ = [
    # 系统数据库配置
    'SYSTEM_DATABASE',
    
    # 支持的数据库类型
    'SUPPORTED_DATABASES',
    
    # 连接字符串生成函数
    'get_connection_string',
    'get_database_config',
    'get_default_port',
    'is_database_supported',
    'get_supported_database_types',
    'get_database_name',
    
    # 数据库配置类
    'DatabaseConfig',
    
    # 配置验证函数
    'validate_database_connection',
]
