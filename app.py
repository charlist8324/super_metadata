import os
import sys
from api import create_app
from db_manager import init_db_manager
from auth import init_auth_tables
from config import Config
import logging


def create_application(config_name=None):
    """
    创建应用程序实例
    :param config_name: 配置名称 ('development', 'production', 'testing')
    :return: Flask应用实例
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = create_app()
    
    # 应用配置
    app.config.from_object(Config)
    
    return app


def initialize_system():
    """
    初始化系统组件
    """
    print("正在初始化Super MetaData 元数据管理系统...")
    
    try:
        # 初始化数据库管理器
        print("正在初始化数据库管理器...")
        init_db_manager(Config.DATABASE_URL)
        print("数据库管理器初始化完成")
        
        # 初始化认证表
        print("正在初始化认证表...")
        init_auth_tables()
        print("认证表初始化完成")
        
        print("系统初始化完成")
    except Exception as e:
        logging.error(f"系统初始化失败: {str(e)}")
        print(f"系统初始化失败: {str(e)}")
        raise


if __name__ == '__main__':
    # 初始化系统
    initialize_system()
    
    # 创建应用
    app = create_application()
    
    # 启动应用
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"启动Super MetaData 元数据管理系统服务器在 {host}:{port}")
    print(f"调试模式: {debug}")
    
    app.run(host=host, port=port, debug=debug)