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

# 查询所有抽取历史
cursor.execute("SELECT COUNT(*) FROM extraction_history")
total_count = cursor.fetchone()[0]
print(f"总记录数: {total_count}")

# 查询最近的抽取历史（包括所有字段）
cursor.execute("""
    SELECT id, datasource_id, extraction_time, status, message, extracted_tables, duration, etl_task_id 
    FROM extraction_history 
    ORDER BY extraction_time DESC 
    LIMIT 10
""")
print("\n最近的抽取历史:")
print("-" * 120)
print(f"{'ID':<6} {'数据源ID':<10} {'抽取时间':<25} {'状态':<10} {'抽取表数':<10} {'耗时(秒)':<10} {'任务ID':<10} {'消息':<30}")
print("-" * 120)
for row in cursor.fetchall():
    print(f"{row[0]:<6} {row[1]:<10} {str(row[2]):<25} {row[3]:<10} {row[5] if row[5] else 0:<10} {row[6] if row[6] else 0:<10} {row[7] if row[7] else 0:<10} {(str(row[4])[:30] if row[4] else ''):<30}")

conn.close()
