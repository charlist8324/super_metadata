# -*- coding: utf-8 -*-
"""
测试API接口是否正常工作
"""
import sys
sys.path.insert(0, 'D:\\python\\py_opencode\\metadata_manager\\Lib\\site-packages')

from db_manager import init_db_manager, get_db_session
from config import Config
from models import DataSource, ExtractionHistory, TableMetadata
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_api_logic():
    """测试API逻辑"""
    print("=" * 80)
    print("测试API逻辑")
    print("=" * 80)

    # 初始化数据库
    init_db_manager(Config.DATABASE_URL)

    try:
        with get_db_session() as session:
            # 测试1：获取所有数据源
            print("\n1. 测试获取所有数据源")
            sources = session.query(DataSource).all()
            print(f"   数据源数量: {len(sources)}")
            for source in sources:
                print(f"   - ID: {source.id}, 名称: {source.name}, 类型: {source.type}")

            # 测试2：获取指定数据源的表
            print("\n2. 测试获取指定数据源的表（数据源ID=4）")
            tables = session.query(TableMetadata).filter(
                TableMetadata.datasource_id == 4
            ).order_by(TableMetadata.table_name).limit(5).all()
            print(f"   表数量: {len(tables)}")
            for table in tables:
                print(f"   - ID: {table.id}, 表名: {table.table_name}, 模式: {table.schema_name}")

            # 测试3：获取抽取历史
            print("\n3. 测试获取抽取历史")
            histories = session.query(ExtractionHistory).order_by(
                ExtractionHistory.extraction_time.desc()
            ).limit(5).all()
            print(f"   历史记录数量: {len(histories)}")
            for hist in histories:
                ds_name = hist.datasource.name if hist.datasource else 'Unknown'
                print(f"   - ID: {hist.id}, 数据源: {ds_name}, 状态: {hist.status}, 时间: {hist.extraction_time}")

            # 测试4：格式化时间
            print("\n4. 测试时间格式化")
            from api import format_datetime, format_datetime_readable
            for hist in histories[:2]:
                iso_time = format_datetime(hist.extraction_time)
                readable_time = format_datetime_readable(hist.extraction_time)
                print(f"   - 原始时间: {hist.extraction_time}")
                print(f"     ISO格式: {iso_time}")
                print(f"     可读格式: {readable_time}")

        print("\n" + "=" * 80)
        print("所有测试完成！")
        print("=" * 80)

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_api_logic()
