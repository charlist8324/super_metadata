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
    print("✓ MySQL连接成功！")
    
    cursor = conn.cursor()
    
    # 查询所有数据源
    cursor.execute("SELECT id, name, type FROM data_sources ORDER BY id")
    sources = cursor.fetchall()
    print(f"\n数据源数量: {len(sources)}")
    
    for source in sources:
        source_id, source_name, source_type = source
        print(f"\n{'=' * 60}")
        print(f"数据源: {source_name} (ID: {source_id}, 类型: {source_type})")
        print(f"{'=' * 60}")
        
        # 查询该数据源的表数量
        cursor.execute(f"SELECT COUNT(*) FROM table_metadata WHERE datasource_id = {source_id}")
        table_count = cursor.fetchone()[0]
        print(f"\n表数量: {table_count}")
        
        if table_count > 0:
            # 查询前10个表
            cursor.execute(f"""
                SELECT id, table_name, schema_name, row_count, size_bytes, comment
                FROM table_metadata 
                WHERE datasource_id = {source_id}
                ORDER BY id DESC
                LIMIT 10
            """)
            tables = cursor.fetchall()
            
            print(f"\n前10个表:")
            for t in tables:
                table_id, table_name, schema_name, row_count, size_bytes, comment = t
                size = f"{size_bytes/1024/1024:.2f}MB" if size_bytes else '-'
                comment_text = comment[:30] + '...' if comment and len(comment) > 30 else (comment or '-')
                print(f"  - [{table_id}] {table_name} ({schema_name}) - 行数: {row_count}, 大小: {size}, 注释: {comment_text}")
            
            # 查询一个表的字段
            if tables:
                first_table_id = tables[0][0]
                first_table_name = tables[0][1]
                cursor.execute(f"SELECT COUNT(*) FROM column_metadata WHERE table_id = {first_table_id}")
                column_count = cursor.fetchone()[0]
                print(f"\n表 {first_table_name} 的字段数量: {column_count}")
                
                if column_count > 0:
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable, default_value, column_comment
                        FROM column_metadata 
                        WHERE table_id = {first_table_id}
                        ORDER BY ordinal_position
                        LIMIT 5
                    """)
                    columns = cursor.fetchall()
                    print(f"\n前5个字段:")
                    for col in columns:
                        col_name, data_type, is_nullable, default_val, col_comment = col
                        nullable = "可空" if is_nullable == "YES" else "不可空"
                        comment_text = col_comment[:30] + '...' if col_comment and len(col_comment) > 30 else (col_comment or '-')
                        print(f"  - {col_name} ({data_type}) {nullable} - 默认: {default_val or '-'}, 注释: {comment_text}")
        else:
            print("  该数据源暂无表元数据")
        
        # 查询该数据源的抽取历史
        cursor.execute(f"""
            SELECT id, extraction_time, status, message, extracted_tables, duration
            FROM extraction_history 
            WHERE datasource_id = {source_id}
            ORDER BY extraction_time DESC
            LIMIT 3
        """)
        histories = cursor.fetchall()
        print(f"\n最近3次抽取记录:")
        for h in histories:
            hist_id, ext_time, status, message, ext_tables, duration = h
            print(f"  - [{hist_id}] 时间: {ext_time}, 状态: {status}, 表数: {ext_tables}, 耗时: {duration}秒")
            if message:
                print(f"      消息: {message[:100]}")
    
    conn.close()
    print("\n✓ 数据库查询完成！")
    
except Exception as e:
    print(f"\n✗ 错误: {str(e)}")
    import traceback
    traceback.print_exc()