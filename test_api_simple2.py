# -*- coding: utf-8 -*-
import sys
import json

# 测试API接口
def test_api():
    import urllib.request
    import urllib.error

    base_url = "http://localhost:5000"

    try:
        # 测试获取数据源
        print("=== 测试获取数据源 ===")
        try:
            with urllib.request.urlopen(f"{base_url}/api/data-sources", timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f"数据源数量: {len(data)}")
                    for source in data:
                        print(f"  - ID: {source['id']}, 名称: {source['name']}, 类型: {source['type']}")
                else:
                    print(f"HTTP状态码: {response.status}")
        except urllib.error.URLError as e:
            print(f"请求失败: {e}")

        # 测试获取抽取历史
        print("\n=== 测试获取抽取历史 ===")
        try:
            with urllib.request.urlopen(f"{base_url}/api/extraction-history?page=1&per_page=5", timeout=5) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode('utf-8'))
                    print(f"历史记录数量: {len(result['history'])}")
                    for record in result['history']:
                        print(f"  - ID: {record['id']}, 数据源: {record.get('datasource_name', 'N/A')}, 状态: {record['status']}, 时间: {record.get('extraction_time_readable', 'N/A')}")
                else:
                    print(f"HTTP状态码: {response.status}")
        except urllib.error.URLError as e:
            print(f"请求失败: {e}")

    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_api()
