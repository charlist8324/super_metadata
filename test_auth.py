from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

username = quote_plus('root')
password = quote_plus('Admin@900')
database = quote_plus('meta_db')
conn_str = f'mysql+pymysql://{username}:{password}@10.178.80.101:3306/{database}?charset=utf8mb4'

engine = create_engine(conn_str)

with engine.connect() as conn:
    # 检查用户表
    print('=== 用户列表 ===')
    result = conn.execute(text("SELECT id, username, full_name, role, created_at FROM users"))
    users = result.fetchall()
    if users:
        for row in users:
            print(f'ID: {row[0]}, 用户名: {row[1]}, 姓名: {row[2]}, 角色: {row[3]}, 创建时间: {row[4]}')
    else:
        print('没有用户')
    
    # 检查会话表（如果存在）
    print('\n=== 检查会话存储 ===')
    try:
        result = conn.execute(text("SHOW TABLES LIKE 'sessions'"))
        sessions_table = result.fetchone()
        if sessions_table:
            result = conn.execute(text("SELECT COUNT(*) FROM sessions"))
            count = result.fetchone()[0]
            print(f'活跃会话数: {count}')
        else:
            print('没有sessions表')
    except Exception as e:
        print(f'检查会话失败: {e}')
