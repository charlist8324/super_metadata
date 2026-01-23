import sqlite3
conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()

# 查询所有表
cursor.execute('SELECT table_name, row_count, size_bytes, datasource_id FROM table_metadata LIMIT 10')
print("所有表的记录:")
print("-" * 100)
for row in cursor.fetchall():
    print(f"表名: {row[0]}, 行数: {row[1]}, 大小(bytes): {row[2]}, 数据源ID: {row[3]}")

# 查询最近的抽取历史
cursor.execute('SELECT id, datasource_id, status, extraction_time, message FROM extraction_history ORDER BY extraction_time DESC LIMIT 5')
print("\n\n最近的抽取历史:")
print("-" * 120)
for row in cursor.fetchall():
    print(f"ID: {row[0]}, 数据源ID: {row[1]}, 状态: {row[2]}, 时间: {row[3]}, 消息: {row[4]}")

conn.close()
