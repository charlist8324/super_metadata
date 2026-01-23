from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = quote_plus('root')
password = quote_plus('Admin@900')
database = quote_plus('snipeit')
conn_str = f'mysql+pymysql://{username}:{password}@10.178.80.101:3306/{database}'

print(f'连接字符串: {conn_str}')

try:
    engine = create_engine(conn_str)
    conn = engine.connect()
    print('连接成功！')
    
    from sqlalchemy import text
    result = conn.execute(text("SHOW TABLES"))
    tables = result.fetchall()
    print(f'找到 {len(tables)} 个表:')
    for table in tables:
        print(f'  - {table[0]}')
    
    conn.close()
except Exception as e:
    print(f'连接失败: {e}')
    import traceback
    traceback.print_exc()
