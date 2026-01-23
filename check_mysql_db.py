from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

username = quote_plus('root')
password = quote_plus('Admin@900')
database = quote_plus('meta_db')
conn_str = f'mysql+pymysql://{username}:{password}@10.178.80.101:3306/{database}?charset=utf8mb4'

print(f'连接数据库: {conn_str}')

engine = create_engine(conn_str)

with engine.connect() as conn:
    # 检查数据源
    print('\n=== 数据源列表 ===')
    result = conn.execute(text("SELECT id, name, type, host, port, `database` FROM data_sources"))
    sources = result.fetchall()
    if sources:
        for row in sources:
            print(f'ID: {row[0]}, 名称: {row[1]}, 类型: {row[2]}, 主机: {row[3]}:{row[4]}, 数据库: {row[5]}')
    else:
        print('没有数据源')
    
    # 检查表元数据
    print('\n=== 表元数据 ===')
    result = conn.execute(text("SELECT COUNT(*) FROM table_metadata"))
    table_count = result.fetchone()[0]
    print(f'表总数: {table_count}')
    
    if table_count > 0:
        result = conn.execute(text("SELECT id, table_name, schema_name, row_count, size_bytes, datasource_id FROM table_metadata LIMIT 10"))
        tables = result.fetchall()
        for row in tables:
            print(f'ID: {row[0]}, 表名: {row[1]}, 模式: {row[2]}, 行数: {row[3]}, 大小: {row[4]}, 数据源ID: {row[5]}')
    
    # 检查列元数据
    print('\n=== 列元数据 ===')
    result = conn.execute(text("SELECT COUNT(*) FROM column_metadata"))
    column_count = result.fetchone()[0]
    print(f'列总数: {column_count}')
    
    # 检查抽取历史
    print('\n=== 抽取历史 ===')
    result = conn.execute(text("SELECT id, datasource_id, status, message, extracted_tables, extraction_time FROM extraction_history ORDER BY extraction_time DESC LIMIT 5"))
    histories = result.fetchall()
    if histories:
        for row in histories:
            print(f'ID: {row[0]}, 数据源ID: {row[1]}, 状态: {row[2]}, 表数: {row[4]}, 时间: {row[5]}')
            if row[3]:
                print(f'  消息: {row[3][:100]}...')
    else:
        print('没有抽取历史')
