# -*- coding: utf-8 -*-
import requests
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

BASE_URL = "http://127.0.0.1:5000"

print("=" * 80)
print("API测试")
print("=" * 80)

# 1. 获取数据源列表
print("\n1. 获取数据源列表:")
try:
    r = requests.get(f"{BASE_URL}/api/data-sources", timeout=5)
    print(f"   状态码: {r.status_code}")
    if r.status_code == 200:
        sources = r.json()
        print(f"   数据源数量: {len(sources)}")
        for s in sources:
            print(f"     - ID={s['id']}, 名称={s['name']}, 类型={s['type']}")
    else:
        print(f"   响应: {r.text[:200]}")
except Exception as e:
    print(f"   错误: {e}")

# 2. 获取抽取历史
print("\n2. 获取抽取历史:")
try:
    r = requests.get(f"{BASE_URL}/api/extraction-history?page=1&per_page=3", timeout=5)
    print(f"   状态码: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   总记录数: {data['pagination']['total']}")
        print(f"   返回记录数: {len(data['history'])}")
        if data['history']:
            for h in data['history']:
                print(f"     - 数据源={h['datasource_name']}, 状态={h['status']}, 表数={h['extracted_tables']}, 时间={h['extraction_time_readable']}")
    else:
        print(f"   响应: {r.text[:200]}")
except Exception as e:
    print(f"   错误: {e}")

# 3. 获取第一个数据源的表
print("\n3. 获取第一个数据源的表列表:")
if 'sources' in locals() and sources:
    source_id = sources[0]['id']
    print(f"   数据源ID: {source_id}")
    try:
        r = requests.get(f"{BASE_URL}/api/data-sources/{source_id}/tables?page=1&per_page=10", timeout=5)
        print(f"   状态码: {r.status_code}")
        if r.status_code == 200:
            result = r.json()
            print(f"   总表数: {result['pagination']['total']}")
            print(f"   当前页: {result['pagination']['page']}/{result['pagination']['pages']}")
            print(f"   返回表数: {len(result['tables'])}")
            if result['tables']:
                for t in result['tables'][:5]:
                    print(f"     - ID={t['id']}, 表名={t['table_name']}, 行数={t['row_count']}, 大小={t['size_bytes']}")
            else:
                print("     没有表数据")
        else:
            print(f"   响应: {r.text[:200]}")
    except Exception as e:
        print(f"   错误: {e}")
else:
    print("   跳过：没有数据源")

print("\n" + "=" * 80)