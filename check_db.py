import sqlite3

conn = sqlite3.connect('D:/python/py_opencode/metadata_manager/metadata.db')
cursor = conn.cursor()

# 查询最新的抽取记录
cursor.execute('''
    SELECT eh.id, eh.datasource_id, ds.name, ds.type, eh.status, eh.extraction_time, eh.extracted_tables
    FROM extraction_history eh
    LEFT JOIN data_sources ds ON eh.datasource_id = ds.id
    ORDER BY eh.extraction_time DESC
    LIMIT 10
''')

print("最近的抽取记录:")
print("-" * 120)
for row in cursor.fetchall():
    print(f"ID: {row[0]}, 数据源: {row[2]} ({row[3]}), 状态: {row[4]}, 时间: {row[5]}, 表数: {row[6]}")

# 查询ads_report表的数据
print("\n\nads_report表的数据:")
print("-" * 120)
cursor.execute('''
    SELECT id, table_name, row_count, size_bytes, updated_at
    FROM table_metadata
    WHERE table_name = 'ads_report'
    ORDER BY updated_at DESC
    LIMIT 5
''')

for row in cursor.fetchall():
    print(f"ID: {row[0]}, 表名: {row[1]}, 行数: {row[2]}, 大小(bytes): {row[3]}, 更新时间: {row[4]}")

conn.close()
