# -*- coding: utf-8 -*-
import pymysql
import sys
from datetime import datetime

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

# 获取系统当前时间
print("=" * 100)
print("时间检查报告")
print("=" * 100)

print("\n1. Python系统时间:")
utc_now = datetime.utcnow()
print(f"   UTC时间: {utc_now}")
print(f"   本地时间: {datetime.now()}")

print("\n2. 数据库服务器时间:")
cursor.execute("SELECT NOW(), UTC_TIMESTAMP()")
db_time_result = cursor.fetchone()
if db_time_result:
    print(f"   服务器本地时间: {db_time_result[0]}")
    print(f"   服务器UTC时间: {db_time_result[1]}")

print("\n3. 数据库时区设置:")
cursor.execute("SELECT @@global.time_zone, @@session.time_zone")
tz_result = cursor.fetchone()
if tz_result:
    print(f"   全局时区: {tz_result[0]}")
    print(f"   会话时区: {tz_result[1]}")

print("\n4. 表创建时间检查:")
cursor.execute("""
    SELECT table_name, created_at, updated_at 
    FROM table_metadata 
    ORDER BY created_at DESC 
    LIMIT 5
""")
tables = cursor.fetchall()
if tables:
    print("\n   表名 | 创建时间(原始) | 创建时间(格式化) | 更新时间")
    print("   " + "-" * 100)
    for table in tables:
        created_at = table[1]
        updated_at = table[2]
        created_formatted = created_at.strftime('%Y/%m/%d %H:%M:%S') if created_at else '-'
        updated_formatted = updated_at.strftime('%Y/%m/%d %H:%M:%S') if updated_at else '-'
        print(f"   {table[0]:25} | {table[1]} | {created_formatted} | {updated_formatted}")

print("\n5. 前端显示模拟:")
print("   JavaScript会使用 new Date(iso_string).toLocaleString()")
print("   例如: new Date('2026-01-19T03:36:24').toLocaleString()")
test_date = datetime(2026, 1, 19, 3, 36, 24)
print(f"   当前系统时区显示: {test_date.strftime('%Y/%m/%d %H:%M:%S')}")

conn.close()
