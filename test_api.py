# -*- coding: utf-8 -*-
import requests

# 测试抽取历史API
try:
    # 不带任何参数，应该返回所有记录
    response = requests.get('http://127.0.0.1:5000/api/extraction-history')
    data = response.json()
    
    print("API响应状态码:", response.status_code)
    print("\n响应数据:")
    print("总记录数:", data.get('pagination', {}).get('total'))
    print("当前页:", data.get('pagination', {}).get('page'))
    print("总页数:", data.get('pagination', {}).get('pages'))
    print("每页记录数:", data.get('pagination', {}).get('per_page'))
    
    print("\n返回的历史记录数:", len(data.get('history', [])))
    
    if data.get('history'):
        print("\n第一条记录:")
        first_record = data['history'][0]
        for key, value in first_record.items():
            print(f"  {key}: {value}")
    
except Exception as e:
    print("请求失败:", str(e))
