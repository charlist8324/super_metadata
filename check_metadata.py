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
    cursor.execute("SELECT id, name, type, host, port, database FROM data_sources")
    print("\n=== 数据源列表 ===")
    print(f"{'ID':<5} {'名称':<30} {'类型':<12} {'主机':<20} {'端口':<8} {'数据库':<20}")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"{row[0]:<5} {row[1]:<30} {row[2]:<12} {row[3]:<20} {row[4]:<8} {row[5]:<20}")
    
    # 查询抽取历史记录
    cursor.execute("SELECT id, datasource_id, extraction_time, status, message, extracted_tables, duration FROM extraction_history ORDER BY extraction_time DESC LIMIT 5")
    print("\n=== 最近5条抽取历史 ===")
    print(f"{'ID':<5} {'数据源ID':<10} {'抽取时间':<20} {'状态':<10} {'消息':<30} {'表数':<8} {'耗时(秒)':<8}")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"{row[0]:<5} {row[1]:<10} {str(row[2]):<20} {row[3]:<10} {row[4][:30]:<30} {row[5]:<8} {row[6]:<8}")
    
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
        print(f"{'ID':<5} {'表名':<25} {'模式':<15} {'数据源':<20} {'行数':<12} {'数据量(字节)':<15} {'注释':<20}")
        print("-" * 120)
        for row in cursor.fetchall():
            size = f"{row[6]/1024/1024:.2f}MB" if row[6] else '-'
            comment = row[7][:20] if row[7] else '-'
            print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[4]:<20} {row[5]:<12} {size:<15} {comment:<20}")
    else:
        print("  暂无表元数据")
    
    # 查询字段元数据
    cursor.execute("SELECT COUNT(*) FROM column_metadata")
    column_count = cursor.fetchone()[0]
    print(f"\n=== 字段元数据统计 ===")
    print(f"总字段数: {column_count}")
    
    conn.close()
    print("\n数据库查询完成！")
    
except Exception as e:
    print(f"\n错误: {str(e)}")
    import traceback
    traceback.print_exc()