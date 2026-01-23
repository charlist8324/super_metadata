# -*- coding: utf-8 -*-
import pymysql
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 连接到MySQL数据库
conn = pymysql.connect(
    host='10.178.80.101',
    port=3306,
    user='root',
    password='Admin@900',
    database='meta_db',
    charset='utf8mb4'
)

cursor = conn.cursor()

# 查看extraction_history表结构
cursor.execute("DESCRIBE extraction_history")
print("Extraction History 表结构:")
print("-" * 100)
for row in cursor.fetchall():
    print(f"字段: {row[0]:20} | 类型: {row[1]:20} | 允许空: {row[2]:5} | 键: {row[3]:10} | 默认值: {row[4]}")

# 查看最新几条记录
cursor.execute("SELECT * FROM extraction_history ORDER BY extraction_time DESC LIMIT 3")
print("\n\n最新记录:")
print("-" * 100)
cursor.execute("SHOW COLUMNS FROM extraction_history")
columns = [col[0] for col in cursor.fetchall()]

cursor.execute("SELECT * FROM extraction_history ORDER BY extraction_time DESC LIMIT 3")
rows = cursor.fetchall()
for row in rows:
    for idx, (col_name, value) in enumerate(zip(columns, row)):
        print(f"{col_name:20}: {value}")
    print("-" * 100)

conn.close()
