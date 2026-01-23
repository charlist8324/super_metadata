# -*- coding: utf-8 -*-
import sqlite3
import sys

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()

# 查询所有表
cursor.execute('SELECT table_name, row_count, size_bytes, datasource_id FROM table_metadata LIMIT 10')
print("All tables:")
print("-" * 100)
for row in cursor.fetchall():
    print(f"Table: {row[0]}, Rows: {row[1]}, Size(bytes): {row[2]}, DatasourceID: {row[3]}")

# 查询最近的抽取历史
cursor.execute('SELECT id, datasource_id, status, extraction_time, message FROM extraction_history ORDER BY extraction_time DESC LIMIT 5')
print("\n\nExtraction history:")
print("-" * 120)
for row in cursor.fetchall():
    print(f"ID: {row[0]}, DatasourceID: {row[1]}, Status: {row[2]}, Time: {row[3]}, Message: {row[4]}")

# 查询数据源
cursor.execute('SELECT id, name, type FROM data_sources')
print("\n\nDatasources:")
print("-" * 80)
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")

conn.close()
