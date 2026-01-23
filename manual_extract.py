import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from api import create_app
from db_manager import init_db_manager
from config import Config
from models import DataSource
from extractor_base import MySQLMetadataExtractor

app = create_app()

with app.app_context():
    from db_manager import get_db_session
    
    with get_db_session() as session:
        source = session.query(DataSource).filter(DataSource.id == 1).first()
        
        if not source:
            print("数据源不存在")
            sys.exit(1)
        
        print(f"正在抽取数据源: {source.name} ({source.type})")
        print(f"主机: {source.host}:{source.port}")
        print(f"数据库: {source.database}")
        
        extractor = MySQLMetadataExtractor(source)
        
        try:
            print("正在连接数据库...")
            if extractor.connect():
                print("连接成功！")
                extractor.disconnect()
            else:
                print("连接失败")
        except Exception as e:
            print(f"连接异常: {e}")
            import traceback
            traceback.print_exc()
