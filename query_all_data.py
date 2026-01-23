# -*- coding: utf-8 -*-
import sqlite3
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()

# 查询所有数据源
cursor.execute('SELECT * FROM data_sources')
print("All Data Sources:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

# 查询所有ETL任务
cursor.execute('SELECT * FROM etl_tasks')
print("\n\nAll ETL Tasks:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

# 查询所有抽取历史
cursor.execute('SELECT * FROM extraction_history')
print("\n\nAll Extraction History:")
print("-" * 150)
for row in cursor.fetchall():
    print(row)

# 查询所有表
cursor.execute('SELECT table_name, datasource_id, row_count, size_bytes FROM table_metadata')
print("\n\nAll Tables:")
print("-" * 100)
for row in cursor.fetchall():
    print(row)

conn.close()
