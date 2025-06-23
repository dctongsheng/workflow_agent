#!/usr/bin/env python3
"""
测试修复后的自动填写参数API
"""

import asyncio
import aiohttp
import json

async def test_fixed_api():
    """测试修复后的API"""
    
    # 使用你提供的入参格式（去掉records包装）
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
            "RegistJson": "",
            "DataDir": "",
            "ImageTar": "",
            "ImagePreDir": "",
            "Tissue": "",
            "Reference": ""
        },
        "user": "test_user_001",
        "conversation_id": "",
        "response_mode": "blocking"
    }
    
    url = "http://localhost:8008/auto_filled_params"
    
    print("🚀 测试修复后的API...")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=test_data) as response:
                print(f"\n📊 响应状态码: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ API调用成功!")
                    print("📋 响应结果:")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                    
                    # 验证响应结构
                    if result.get("code") == 200:
                        print("✅ 响应状态正确")
                    else:
                        print(f"❌ 响应状态异常: {result.get('code')}")
                        
                    if "filled_parameters" in result:
                        print("✅ 包含filled_parameters字段")
                        if result["filled_parameters"]:
                            print("✅ 参数填充成功")
                            print("📝 填充的参数:")
                            for key, value in result["filled_parameters"].items():
                                print(f"  {key}: {value}")
                        else:
                            print("⚠️ 参数填充为空")
                    else:
                        print("❌ 缺少filled_parameters字段")
                        
                else:
                    error_text = await response.text()
                    print(f"❌ API调用失败: {error_text}")
                    
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    asyncio.run(test_fixed_api()) 