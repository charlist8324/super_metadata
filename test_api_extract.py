import requests
import json

base_url = "http://127.0.0.1:5000"

# 首先登录（如果需要）
try:
    # 尝试获取数据源列表（不需要登录）
    response = requests.get(f"{base_url}/api/data-sources")
    print(f"获取数据源列表: {response.status_code}")
    data_sources = response.json()
    print(f"找到 {len(data_sources)} 个数据源:")
    for ds in data_sources:
        print(f"  - ID: {ds['id']}, 名称: {ds['name']}, 类型: {ds['type']}")
    
    if data_sources:
        source_id = data_sources[0]['id']
        print(f"\n正在对数据源 {source_id} 进行元数据抽取...")
        
        extract_response = requests.post(f"{base_url}/api/data-sources/{source_id}/extract")
        print(f"抽取请求状态码: {extract_response.status_code}")
        
        if extract_response.status_code == 200:
            result = extract_response.json()
            print(f"抽取结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"抽取失败: {extract_response.text}")
            
except Exception as e:
    print(f"请求失败: {e}")
    import traceback
    traceback.print_exc()
