from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class DataSource(Base):
    """
    数据源定义表
    """
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)  # 数据源名称
    type = Column(String(50), nullable=False)  # 数据库类型：mysql, postgresql, sqlserver, oracle
    host = Column(String(255), nullable=False)  # 主机地址
    port = Column(Integer, nullable=False)  # 端口号
    username = Column(String(255), nullable=False)  # 用户名
    password = Column(String(255), nullable=False)  # 密码
    database = Column(String(255), nullable=False)  # 数据库名
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 关系：一个数据源对应多个表
    tables = relationship("TableMetadata", back_populates="datasource")


class TableMetadata(Base):
    """
    表元数据表
    """
    __tablename__ = 'table_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(255), nullable=False)  # 表名
    schema_name = Column(String(255))  # 模式名
    row_count = Column(BigInteger)  # 行数
    size_bytes = Column(BigInteger)  # 数据大小（字节）
    comment = Column(Text)  # 表注释
    datasource_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 关系：一个表对应多个字段
    columns = relationship("ColumnMetadata", back_populates="table")
    datasource = relationship("DataSource", back_populates="tables")


class ColumnMetadata(Base):
    """
    字段元数据表
    """
    __tablename__ = 'column_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    column_name = Column(String(255), nullable=False)  # 字段名
    data_type = Column(String(100), nullable=False)  # 数据类型
    is_nullable = Column(String(10), nullable=False)  # 是否可空
    default_value = Column(String(255))  # 默认值
    column_comment = Column(Text)  # 字段注释
    ordinal_position = Column(Integer)  # 字段位置
    table_id = Column(Integer, ForeignKey('table_metadata.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 关系：一个字段属于一个表
    table = relationship("TableMetadata", back_populates="columns")


class TableRelationship(Base):
    """
    表关联关系表
    """
    __tablename__ = 'table_relationships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    constraint_name = Column(String(255))  # 约束名称
    table_id = Column(Integer, ForeignKey('table_metadata.id'), nullable=False)  # 主表ID
    referenced_table_id = Column(Integer, ForeignKey('table_metadata.id'), nullable=False)  # 引用表ID
    column_name = Column(String(255), nullable=False)  # 主表字段名
    referenced_column_name = Column(String(255), nullable=False)  # 引用表字段名
    constraint_type = Column(String(50), nullable=False)  # 约束类型：FOREIGN KEY, PRIMARY KEY等
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系：定义双向关系
    table = relationship("TableMetadata", foreign_keys=[table_id], backref="relationships")
    referenced_table = relationship("TableMetadata", foreign_keys=[referenced_table_id], backref="referenced_by")


class ExtractionHistory(Base):
    """
    抽取历史记录表
    """
    __tablename__ = 'extraction_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datasource_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)
    extraction_time = Column(DateTime, default=datetime.utcnow)  # 抽取时间
    status = Column(String(20), nullable=False)  # 状态：running, success, failed
    message = Column(Text)  # 详细信息或错误信息
    extracted_tables = Column(Integer)  # 抽取的表数量
    duration = Column(Integer)  # 耗时（秒）
    etl_task_id = Column(Integer, ForeignKey('etl_tasks.id'), nullable=True)  # 关联的ETL任务ID

    datasource = relationship("DataSource")
    etl_task = relationship("ETLTask", back_populates="extraction_history")


class ETLTask(Base):
    """
    ETL任务表
    """
    __tablename__ = 'etl_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # 任务名称
    task_type = Column(String(50), nullable=False)  # 任务类型：full, incremental, schema_only
    datasource_id = Column(Integer, ForeignKey('data_sources.id'), nullable=False)  # 关联的数据源ID
    schedule_type = Column(String(50), nullable=False)  # 调度类型：interval, cron, manual
    interval_value = Column(Integer)  # 时间间隔值
    interval_unit = Column(String(20))  # 时间间隔单位：minutes, hours, days, weeks
    cron_expression = Column(String(100))  # CRON表达式
    status = Column(String(20), default='active')  # 状态：active, inactive
    description = Column(Text)  # 任务描述
    last_run = Column(DateTime)  # 上次运行时间
    next_run = Column(DateTime)  # 下次运行时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    datasource = relationship("DataSource")
    extraction_history = relationship("ExtractionHistory", back_populates="etl_task")


def init_database():
    """初始化数据库表"""
    from db_manager import db_manager
    if db_manager is None:
        raise Exception("数据库管理器未初始化")
    Base.metadata.create_all(bind=db_manager.engine)
    return db_manager.engine