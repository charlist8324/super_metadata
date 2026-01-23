# -*- coding: utf-8 -*-
import requests
import json

# 基础URL
BASE_URL = "http://127.0.0.1:5000"

print("=" * 80)
print("测试Super MetaData 元数据管理系统API")
print("=" * 80)

# 1. 测试获取数据源列表
print("\n1. 获取数据源列表...")
try:
    response = requests.get(f"{BASE_URL}/api/data-sources")
    if response.status_code == 200:
        data_sources = response.json()
        print(f"✓ 成功获取 {len(data_sources)} 个数据源")
        for ds in data_sources:
            print(f"  - ID: {ds['id']}, 名称: {ds['name']}, 类型: {ds['type']}")
    else:
        print(f"✗ 获取数据源失败，状态码: {response.status_code}")
        print(f"  响应: {response.text}")
except Exception as e:
    print(f"✗ 请求失败: {str(e)}")

# 2. 测试获取抽取历史
print("\n2. 获取抽取历史...")
try:
    response = requests.get(f"{BASE_URL}/api/extraction-history?page=1&per_page=5")
    if response.status_code == 200:
        history_data = response.json()
        print(f"✓ 成功获取抽取历史")
        print(f"  总记录数: {history_data['pagination']['total']}")
        if history_data['history']:
            print(f"  最近抽取记录:")
            for h in history_data['history'][:3]:
                print(f"    - ID: {h['id']}, 数据源: {h['datasource_name']}, 时间: {h['extraction_time_readable']}, 状态: {h['status']}, 表数: {h['extracted_tables']}")
        else:
            print("  暂无抽取历史记录")
    else:
        print(f"✗ 获取抽取历史失败，状态码: {response.status_code}")
        print(f"  响应: {response.text}")
except Exception as e:
    print(f"✗ 请求失败: {str(e)}")

# 3. 测试获取数据源的表列表
print("\n3. 获取数据源的表列表...")
if data_sources:
    # 测试第一个数据源
    source_id = data_sources[0]['id']
    print(f"  正在获取数据源ID {source_id} ({data_sources[0]['name']}) 的表列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/data-sources/{source_id}/tables?page=1&per_page=20")
        if response.status_code == 200:
            result = response.json()
            tables = result['tables']
            print(f"✓ 成功获取表列表")
            print(f"  总表数: {result['pagination']['total']}")
            print(f"  当前页: {result['pagination']['page']}/{result['pagination']['pages']}")
            if tables:
                print(f"  前5个表:")
                for table in tables[:5]:
                    print(f"    - ID: {table['id']}, 表名: {table['table_name']}, 模式: {table['schema_name']}, 行数: {table['row_count']}, 数据量: {table['size_bytes']}")
            else:
                print("  该数据源暂无表数据")
        else:
            print(f"✗ 获取表列表失败，状态码: {response.status_code}")
            print(f"  响应: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
else:
    print("  没有数据源，跳过")

# 4. 测试获取表详情
print("\n4. 获取表详情...")
if data_sources and tables:
    # 获取第一个表的详情
    table_id = tables[0]['id']
    print(f"  正在获取表ID {table_id} ({tables[0]['table_name']}) 的详情...")
    try:
        response = requests.get(f"{BASE_URL}/api/tables/{table_id}")
        if response.status_code == 200:
            table_data = response.json()
            print(f"✓ 成功获取表详情")
            print(f"  表名: {table_data['table_name']}")
            print(f"  模式: {table_data['schema_name']}")
            print(f"  行数: {table_data['row_count']}")
            print(f"  数据量: {table_data['size_bytes']}")
            print(f"  字段数: {len(table_data['columns'])}")
            print(f"  关联关系数: {len(table_data['relationships'])}")
            if table_data['columns']:
                print(f"  前3个字段:")
                for col in table_data['columns'][:3]:
                    print(f"    - {col['column_name']} ({col['data_type']})")
        else:
            print(f"✗ 获取表详情失败，状态码: {response.status_code}")
            print(f"  响应: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
else:
    print("  没有表数据，跳过")

# 5. 测试概览数据
print("\n5. 获取概览数据...")
try:
    response = requests.get(f"{BASE_URL}/api/overview")
    if response.status_code == 200:
        overview = response.json()
        print(f"✓ 成功获取概览数据")
        print(f"  数据源数: {overview['data_sources_count']}")
        print(f"  表数: {overview['tables_count']}")
        print(f"  字段数: {overview['columns_count']}")
    else:
        print(f"✗ 获取概览失败，状态码: {response.status_code}")
        print(f"  响应: {response.text}")
except Exception as e:
    print(f"✗ 请求失败: {str(e)}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)