# -*- coding: utf-8 -*-
import pymysql
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 连接到StarRocks数据库
conn = pymysql.connect(
    host='10.200.222.10',
    port=9030,
    user='meta_user',
    password='meta@2025',
    database='ADS_REPORT',
    charset='utf8mb4'
)

cursor = conn.cursor()

# 测试SHOW DATA命令
table_name = 'TB_QMS_RODSTOCKDETAIL'
print(f"Testing SHOW DATA FROM ADS_REPORT.{table_name}")
print("-" * 150)

try:
    cursor.execute(f"SHOW DATA FROM `ADS_REPORT`.`{table_name}`")
    result = cursor.fetchall()
    
    print(f"Total rows returned: {len(result)}")
    print("\nAll results:")
    for idx, row in enumerate(result):
        print(f"Row {idx}: {row}")
        print(f"Row {idx} length: {len(row)}")
        for col_idx, col in enumerate(row):
            print(f"  Column {col_idx}: {repr(col)}")
    
    # 获取列名
    cursor.execute(f"SHOW DATA FROM `ADS_REPORT`.`{table_name}` LIMIT 1")
    desc = cursor.description
    print("\n\nColumn descriptions:")
    for idx, col_desc in enumerate(desc):
        print(f"Column {idx}: name={col_desc[0]}, type={col_desc[1]}")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()

conn.close()
