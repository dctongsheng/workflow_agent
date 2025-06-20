#!/usr/bin/env python3
"""
测试自动填写参数API路由
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List

# API配置
API_BASE_URL = "http://localhost:8008"
AUTO_FILLED_PARAMS_ENDPOINT = f"{API_BASE_URL}/auto_filled_params"

async def test_auto_filled_params_api():
    """测试自动填写参数API"""
    
    # 测试数据1：使用字符串列表作为data_choose
    test_data_1 = {
        "data_choose": [
            "sample_data_001.fastq.gz",
            "sample_data_002.fastq.gz", 
            "reference_genome.fa",
            "annotation.gtf"
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
    
    # 测试数据2：使用单个字符串作为data_choose
    test_data_2 = {
        "data_choose": "single_sample_data.fastq.gz",
        "query_template": {
            "input_file": "",
            "output_dir": "",
            "threads": "",
            "quality": ""
        },
        "user": "test_user_002",
        "conversation_id": "",
        "response_mode": "blocking"
    }
    
    # 测试数据3：简化的查询模板
    test_data_3 = {
        "data_choose": [
            "RNA_seq_data_1.fastq",
            "RNA_seq_data_2.fastq"
        ],
        "query_template": {
            "input_files": "",
            "output_directory": "",
            "reference_genome": ""
        }
    }
    
    # 测试数据4：使用字典列表作为data_choose
    test_data_4 = {
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
        "user": "test_user_004",
        "conversation_id": "",
        "response_mode": "blocking"
    }
    
    test_cases = [
        ("测试用例1 - 多文件数据选择", test_data_1),
        ("测试用例2 - 单文件数据选择", test_data_2),
        ("测试用例3 - 简化模板", test_data_3),
        ("测试用例4 - 字典列表数据选择", test_data_4)
    ]
    
    async with aiohttp.ClientSession() as session:
        for test_name, test_data in test_cases:
            print(f"\n{'='*50}")
            print(f"{test_name}")
            print(f"{'='*50}")
            
            try:
                print(f"请求数据:")
                print(json.dumps(test_data, ensure_ascii=False, indent=2))
                
                # 发送POST请求
                async with session.post(
                    AUTO_FILLED_PARAMS_ENDPOINT,
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    print(f"\n响应状态码: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        print("✅ API调用成功!")
                        print("响应结果:")
                        print(json.dumps(result, ensure_ascii=False, indent=2))
                        
                        # 验证响应结构
                        if "code" in result and result["code"] == 200:
                            print("✅ 响应结构正确")
                        else:
                            print("❌ 响应结构异常")
                            
                        if "filled_parameters" in result:
                            print("✅ 包含filled_parameters字段")
                            if result["filled_parameters"]:
                                print("✅ 参数填充成功")
                            else:
                                print("⚠️ 参数填充为空")
                        else:
                            print("❌ 缺少filled_parameters字段")
                            
                    else:
                        error_text = await response.text()
                        print(f"❌ API调用失败: HTTP {response.status}")
                        print(f"错误信息: {error_text}")
                        
            except aiohttp.ClientError as e:
                print(f"❌ 网络错误: {e}")
            except Exception as e:
                print(f"❌ 未知错误: {e}")

async def test_error_cases():
    """测试错误情况"""
    
    print(f"\n{'='*50}")
    print("错误情况测试")
    print(f"{'='*50}")
    
    error_test_cases = [
        ("空data_choose", {
            "data_choose": [],
            "query_template": {"test": ""}
        }),
        ("空query_template", {
            "data_choose": ["test.txt"],
            "query_template": {}
        }),
        ("无效的data_choose类型", {
            "data_choose": 123,  # 应该是字符串或列表
            "query_template": {"test": ""}
        }),
        ("缺少必需字段", {
            "data_choose": ["test.txt"]
            # 缺少query_template
        })
    ]
    
    async with aiohttp.ClientSession() as session:
        for test_name, test_data in error_test_cases:
            print(f"\n--- {test_name} ---")
            
            try:
                async with session.post(
                    AUTO_FILLED_PARAMS_ENDPOINT,
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    print(f"状态码: {response.status}")
                    result = await response.json()
                    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    
            except Exception as e:
                print(f"错误: {e}")

async def test_api_health():
    """测试API健康状态"""
    
    print(f"\n{'='*50}")
    print("API健康状态测试")
    print(f"{'='*50}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # 测试根路径
            async with session.get(f"{API_BASE_URL}/") as response:
                print(f"根路径状态码: {response.status}")
                
            # 测试OpenAPI文档
            async with session.get(f"{API_BASE_URL}/docs") as response:
                print(f"API文档状态码: {response.status}")
                
    except Exception as e:
        print(f"健康检查失败: {e}")

async def main():
    """主测试函数"""
    print("开始测试自动填写参数API...")
    
    # 测试API健康状态
    await test_api_health()
    
    # 测试正常情况
    await test_auto_filled_params_api()
    
    # 测试错误情况
    await test_error_cases()
    
    print(f"\n{'='*50}")
    print("测试完成!")
    print(f"{'='*50}")

if __name__ == "__main__":
    asyncio.run(main()) 