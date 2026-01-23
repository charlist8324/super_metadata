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

# 测试解析大小
test_sizes = ['3.768 GB', '1.5 MB', '500 KB', '2.0 TB']

def parse_size(size_str):
    size_str = size_str.strip().upper()
    size_bytes = 0
    if 'KB' in size_str:
        size_bytes = int(float(size_str.replace('KB', '').strip()) * 1024)
    elif 'MB' in size_str:
        size_bytes = int(float(size_str.replace('MB', '').strip()) * 1024 * 1024)
    elif 'GB' in size_str:
        size_bytes = int(float(size_str.replace('GB', '').strip()) * 1024 * 1024 * 1024)
    elif 'TB' in size_str:
        size_bytes = int(float(size_str.replace('TB', '').strip()) * 1024 * 1024 * 1024 * 1024)
    else:
        try:
            size_bytes = int(size_str)
        except:
            size_bytes = 0
    return size_bytes

print("Testing size parsing:")
print("-" * 100)
for size_str in test_sizes:
    bytes_value = parse_size(size_str)
    print(f"{size_str:15} -> {bytes_value:20,} bytes")

# 从StarRocks获取真实数据并测试
print("\n\nReal data from StarRocks:")
print("-" * 100)
cursor.execute("SHOW DATA FROM `ADS_REPORT`.`TB_QMS_RODSTOCKDETAIL`")
results = cursor.fetchall()

for row in results:
    # 跳过总计行
    if len(row) >= 2 and str(row[1]).upper() == 'TOTAL':
        continue
    
    # Size在索引2的位置
    if len(row) >= 3:
        size_str = str(row[2]).strip().upper()
        bytes_value = parse_size(size_str)
        print(f"Table: {row[0]:40} Size: {size_str:15} -> {bytes_value:20,} bytes")

conn.close()
