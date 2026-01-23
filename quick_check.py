# -*- coding: utf-8 -*-
import pymysql
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

try:
    # 连接到MySQL数据库
    conn = pymysql.connect(
        host='10.178.80.101',
        port=3306,
        user='root',
        password='Admin@900',
        database='meta_db',
        charset='utf8mb4'
    )
    print("MySQL连接成功！")
    
    cursor = conn.cursor()
    
    # 查询所有数据源
    cursor.execute("SELECT id, name, type, host, port, `database` FROM data_sources")
    print("\n=== 数据源列表 ===")
    sources = cursor.fetchall()
    print(f"数据源数量: {len(sources)}")
    for row in sources:
        print(f"ID: {row[0]}, 名称: {row[1]}, 类型: {row[2]}, 主机: {row[3]}, 端口: {row[4]}, 数据库: {row[5]}")
    
    # 查询表元数据
    cursor.execute("SELECT COUNT(*) FROM table_metadata")
    table_count = cursor.fetchone()[0]
    print(f"\n=== 表元数据统计 ===")
    print(f"总表数: {table_count}")
    
    # 如果有表数据，显示前5条
    if table_count > 0:
        cursor.execute("""
            SELECT tm.id, tm.table_name, tm.schema_name, tm.datasource_id, 
                   ds.name as datasource_name, tm.row_count, tm.size_bytes, tm.comment
            FROM table_metadata tm
            LEFT JOIN data_sources ds ON tm.datasource_id = ds.id
            ORDER BY tm.id DESC
            LIMIT 5
        """)
        print("\n=== 最近5条表元数据 ===")
        for row in cursor.fetchall():
            size = f"{row[6]/1024/1024:.2f}MB" if row[6] else '-'
            comment = row[7][:20] if row[7] else '-'
            print(f"ID: {row[0]}, 表名: {row[1]}, 数据源: {row[4]}, 行数: {row[5]}, 大小: {size}")
    
    conn.close()
    print("\n数据库查询完成！")
    
except Exception as e:
    print(f"\n错误: {str(e)}")
    import traceback
    traceback.print_exc()
