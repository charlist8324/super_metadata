import sqlite3
from datetime import datetime

conn = sqlite3.connect('metadata.db')
cursor = conn.cursor()

# 插入一些测试表数据
test_tables = [
    ('glpi_users', 'snipeit', 1500, 102400, 'GLPI用户表'),
    ('glpi_computers', 'snipeit', 500, 5120000, 'GLPI计算机表'),
    ('glpi_tickets', 'snipeit', 2000, 2048000, 'GLPI工单表'),
    ('users', 'snipeit', 100, 102400, '用户表'),
    ('requests', 'snipeit', 300, 512000, '请求表'),
]

now = datetime.utcnow()

for table_name, schema_name, row_count, size_bytes, comment in test_tables:
    cursor.execute('''
        INSERT INTO table_metadata 
        (table_name, schema_name, row_count, size_bytes, comment, datasource_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 1, ?, ?)
    ''', (table_name, schema_name, row_count, size_bytes, comment, now, now))

# 插入一些测试列数据
test_columns = [
    (1, 'id', 'int', 'NO', None, 1, '主键ID'),
    (1, 'name', 'varchar', 'NO', None, 2, '用户名'),
    (1, 'email', 'varchar', 'YES', None, 3, '邮箱地址'),
    (2, 'id', 'int', 'NO', None, 1, '主键ID'),
    (2, 'computer_name', 'varchar', 'NO', None, 2, '计算机名称'),
    (2, 'serial_number', 'varchar', 'YES', None, 3, '序列号'),
]

for table_id, column_name, data_type, is_nullable, default_value, ordinal_position, column_comment in test_columns:
    cursor.execute('''
        INSERT INTO column_metadata 
        (column_name, data_type, is_nullable, default_value, ordinal_position, column_comment, table_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (column_name, data_type, is_nullable, default_value, ordinal_position, column_comment, table_id, now, now))

conn.commit()

# 验证插入结果
cursor.execute('SELECT COUNT(*) FROM table_metadata WHERE datasource_id = 1')
table_count = cursor.fetchone()[0]
print(f'插入了 {table_count} 个测试表')

cursor.execute('SELECT COUNT(*) FROM column_metadata')
column_count = cursor.fetchone()[0]
print(f'插入了 {column_count} 个测试列')

# 显示插入的表数据
print('\n测试表列表:')
cursor.execute('SELECT id, table_name, row_count, size_bytes, comment FROM table_metadata WHERE datasource_id = 1')
for row in cursor.fetchall():
    print(f'  - {row[1]} (ID: {row[0]}): {row[2]} 行, {row[3]} 字节')

conn.close()
print('\n测试数据插入完成！')
