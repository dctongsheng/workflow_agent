#!/usr/bin/env python3
"""
快速测试自动填写参数API
"""

import asyncio
import aiohttp
import json

async def quick_test():
    """快速测试函数"""
    
    # 测试数据 - 使用字典列表
    test_data = {
        "data_choose": [
            {
                "omics": "genomics",
                "name": "C01935E1_SC_20250226_154926_4.1.1.tar.gz",
                "menuPath": "/Files/RawData"
            },
            {
                "name": "Y00799B3.barcodeToPos.h5",
                "menuPath": "/Files/RawData"
            },
            {
                "name": "Y00799B2.barcodeToPos.h5",
                "menuPath": "/Files/RawData"
            }
        ],
        "query_template": {
            "SN": "",
            "DataDir": "",
            "Reference": ""
        }
    }
    
    url = "http://localhost:8008/auto_filled_params"
    
    print("🚀 开始快速测试...")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=test_data) as response:
                print(f"\n📊 响应状态码: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ 测试成功!")
                    print("📋 响应结果:")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    error_text = await response.text()
                    print(f"❌ 测试失败: {error_text}")
                    
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test()) 