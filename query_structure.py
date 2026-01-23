# -*- coding: utf-8 -*-
import sqlite3
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()

# 查看所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables in database:")
for row in cursor.fetchall():
    print(f"  - {row[0]}")

# 查看ETL任务表结构
cursor.execute("PRAGMA table_info(etl_tasks)")
print("\n\nETL tasks table structure:")
print("-" * 100)
for row in cursor.fetchall():
    print(f"Column: {row[1]}, Type: {row[2]}, NotNull: {row[3]}, Default: {row[4]}, PK: {row[5]}")

# 查看ETL任务数据
cursor.execute('SELECT * FROM etl_tasks')
print("\n\nETL tasks data:")
print("-" * 120)
for row in cursor.fetchall():
    print(row)

# 查看数据源数据
cursor.execute('SELECT * FROM data_sources')
print("\n\nData sources:")
print("-" * 120)
for row in cursor.fetchall():
    print(row)

conn.close()
