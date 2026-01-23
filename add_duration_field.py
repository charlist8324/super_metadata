# -*- coding: utf-8 -*-
import pymysql

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

# 添加duration字段
try:
    cursor.execute("ALTER TABLE extraction_history ADD COLUMN duration INT NULL COMMENT '耗时（秒）'")
    print("成功添加duration字段到extraction_history表")
    conn.commit()
except Exception as e:
    if "Duplicate column" in str(e):
        print("duration字段已存在，跳过添加")
    else:
        print(f"添加字段失败: {e}")

# 查看表结构
cursor.execute("DESCRIBE extraction_history")
print("\nExtraction History 表结构:")
print("-" * 100)
for row in cursor.fetchall():
    print(f"字段: {row[0]:20} | 类型: {row[1]:20} | 允许空: {row[2]:5} | 键: {row[3]:10} | 默认值: {row[4]}")

conn.close()
