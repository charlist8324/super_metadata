# -*- coding: utf-8 -*-
import sqlite3
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()

# 查询ETL任务
cursor.execute('SELECT id, task_name, datasource_id, task_type, last_run, status FROM etl_tasks')
print("ETL Tasks:")
print("-" * 120)
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, DatasourceID: {row[2]}, Type: {row[3]}, LastRun: {row[4]}, Status: {row[5]}")

# 查询所有数据源
cursor.execute('SELECT id, name, type FROM data_sources')
print("\n\nAll Datasources:")
print("-" * 80)
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")

# 查询所有表
cursor.execute('SELECT table_name, datasource_id FROM table_metadata')
print("\n\nAll Tables in DB:")
print("-" * 80)
count = 0
for row in cursor.fetchall():
    print(f"Table: {row[0]}, DatasourceID: {row[1]}")
    count += 1
if count == 0:
    print("(No tables found)")

conn.close()
