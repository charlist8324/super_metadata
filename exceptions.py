"""
自定义异常类
"""
class MetadataException(Exception):
    """Super MetaData 元数据管理系统基础异常"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

class DatabaseConnectionException(MetadataException):
    """数据库连接异常"""
    def __init__(self, message="数据库连接失败"):
        super().__init__(message, "DB_CONN_ERROR")

class AuthenticationException(MetadataException):
    """认证异常"""
    def __init__(self, message="认证失败"):
        super().__init__(message, "AUTH_ERROR")

class AuthorizationException(MetadataException):
    """授权异常"""
    def __init__(self, message="权限不足"):
        super().__init__(message, "AUTHZ_ERROR")

class DataSourceNotFoundException(MetadataException):
    """数据源不存在异常"""
    def __init__(self, message="数据源不存在"):
        super().__init__(message, "DS_NOT_FOUND")

class ExtractionException(MetadataException):
    """元数据抽取异常"""
    def __init__(self, message="元数据抽取失败"):
        super().__init__(message, "EXTRACTION_ERROR")

class ValidationException(MetadataException):
    """验证异常"""
    def __init__(self, message="参数验证失败"):
        super().__init__(message, "VALIDATION_ERROR")