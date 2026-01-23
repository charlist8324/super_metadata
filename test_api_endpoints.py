# -*- coding: utf-8 -*-
"""
诊断API访问问题
"""
import sys
import json
import urllib.request
import urllib.error

def test_api_endpoints():
    """测试所有API端点"""
    base_url = "http://127.0.0.1:5000"

    print("=" * 80)
    print("API端点测试")
    print("=" * 80)

    # 测试端点列表
    endpoints = [
        ('/', '首页'),
        ('/login', '登录页'),
        ('/api/current-user', '当前用户信息'),
        ('/api/data-sources', '数据源列表'),
        ('/api/overview', '资源概览'),
        ('/api/extraction-history?page=1&per_page=5', '抽取历史'),
        ('/api/etl-tasks', 'ETL任务'),
    ]

    for endpoint, description in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n测试: {description}")
            print(f"URL: {url}")

            with urllib.request.urlopen(url, timeout=5) as response:
                status = response.status
                content_type = response.headers.get('Content-Type', '')

                print(f"状态码: {status}")
                print(f"内容类型: {content_type}")

                if status == 200:
                    if 'application/json' in content_type:
                        data = json.loads(response.read().decode('utf-8'))
                        if isinstance(data, list):
                            print(f"返回数据: 列表，共 {len(data)} 项")
                        elif isinstance(data, dict):
                            print(f"返回数据: 字典，键: {list(data.keys())[:10]}")
                            if 'history' in data:
                                print(f"  历史记录数: {len(data.get('history', []))}")
                            if 'tables' in data:
                                print(f"  表数量: {len(data.get('tables', []))}")
                        else:
                            print(f"返回数据: {type(data)}")
                    else:
                        content = response.read().decode('utf-8')[:200]
                        print(f"HTML内容: {content[:100]}...")
                elif status == 302 or status == 301:
                    location = response.headers.get('Location', '')
                    print(f"重定向到: {location}")
                else:
                    print(f"错误状态: {status}")

        except urllib.error.HTTPError as e:
            print(f"HTTP错误: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"连接错误: {e.reason}")
        except Exception as e:
            print(f"其他错误: {type(e).__name__}: {str(e)}")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == '__main__':
    test_api_endpoints()
