# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'D:\\python\\py_opencode\\metadata_manager\\Lib\\site-packages')

from db_manager import get_db_session
from models import DataSource, ExtractionHistory, TableMetadata

try:
    with get_db_session() as session:
        # 测试查询数据源
        sources = session.query(DataSource).all()
        print(f"\n=== 数据源查询结果 ===")
        print(f"数据源数量: {len(sources)}")
        for source in sources:
            print(f"ID: {source.id}, 名称: {source.name}, 类型: {source.type}")
        
        # 测试查询抽取历史
        histories = session.query(ExtractionHistory).order_by(ExtractionHistory.extraction_time.desc()).limit(3).all()
        print(f"\n=== 抽取历史查询结果 ===")
        print(f"历史记录数量: {len(histories)}")
        for hist in histories:
            ds_name = hist.datasource.name if hist.datasource else 'Unknown'
            print(f"ID: {hist.id}, 数据源: {ds_name}, 时间: {hist.extraction_time}, 状态: {hist.status}, 表数: {hist.extracted_tables}")
        
        # 测试查询表元数据
        tables = session.query(TableMetadata).filter(TableMetadata.datasource_id == 1).limit(3).all()
        print(f"\n=== 表元数据查询结果 ===")
        print(f"数据源1的表数量: {len(tables)}")
        for table in tables:
            print(f"ID: {table.id}, 表名: {table.table_name}, 模式: {table.schema_name}")
    
    print("\n✓ 测试完成！")
    
except Exception as e:
    print(f"\n✗ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
