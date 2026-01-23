import sqlite3
conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()
cursor.execute('SELECT id, table_name, row_count, size_bytes FROM table_metadata WHERE table_name="ads_report" LIMIT 3')
result = cursor.fetchall()
print("ads_report表的数据:")
for row in result:
    print(f"ID: {row[0]}, 表名: {row[1]}, 行数: {row[2]}, 大小(bytes): {row[3]}")
conn.close()
