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

# 查询所有数据源
cursor.execute('SELECT * FROM data_sources')
print("All Data Sources:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

# 查询StarRocks相关的数据源
cursor.execute("SELECT * FROM data_sources WHERE type='starrocks'")
print("\n\nStarRocks Data Sources:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

# 查询所有ETL任务
cursor.execute('SELECT * FROM etl_tasks')
print("\n\nAll ETL Tasks:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

# 查询最近的抽取历史
cursor.execute('SELECT * FROM extraction_history ORDER BY extraction_time DESC LIMIT 10')
print("\n\nRecent Extraction History:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

# 查询表数据（特别是ADS_REPORT相关的）
cursor.execute("SELECT table_name, datasource_id, row_count, size_bytes, updated_at FROM table_metadata ORDER BY updated_at DESC LIMIT 20")
print("\n\nRecent Table Metadata:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

conn.close()
