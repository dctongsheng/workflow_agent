#!/usr/bin/env python3
"""
测试Dify异步API调用功能
"""

import asyncio
import json
from llm_dify import call_dify_workflow, DifyClient, DifyAPIError

async def test_single_call():
    """测试单个API调用"""
    print("=== 测试单个Dify API调用 ===")
    try:
        result = await call_dify_workflow(
            query="细胞注释",
            data_meatinfo="1111.h5ad"
        )
        print("✅ API调用成功!")
        print(f"响应结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return True
    except DifyAPIError as e:
        print(f"❌ API调用失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

async def test_multiple_calls():
    """测试多个并发API调用"""
    print("\n=== 测试多个并发Dify API调用 ===")
    
    # 准备多个测试请求
    test_requests = [
        ("细胞注释", "1111.h5ad"),
        ("基因表达分析", "2222.h5ad"),
        ("蛋白质组学分析", "3333.h5ad"),
    ]
    
    # 并发执行
    tasks = []
    for query, data_meatinfo in test_requests:
        task = call_dify_workflow(query, data_meatinfo)
        tasks.append(task)
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, (query, data_meatinfo) in enumerate(test_requests):
            if isinstance(results[i], Exception):
                print(f"❌ 请求 {i+1} 失败: {results[i]}")
            else:
                print(f"✅ 请求 {i+1} 成功: {query}")
                print(f"   响应: {json.dumps(results[i], ensure_ascii=False, indent=2)}")
        
        return results
    except Exception as e:
        print(f"❌ 并发调用失败: {e}")
        return None

async def test_custom_client():
    """测试自定义客户端配置"""
    print("\n=== 测试自定义客户端配置 ===")
    
    # 创建自定义客户端
    custom_client = DifyClient(
        base_url="http://172.28.140.214",
        api_key="app-UsYqYl0FxzbiexcetyViJS3L"
    )
    
    try:
        result = await custom_client.run_workflow(
            query="测试自定义客户端",
            data_meatinfo="test.h5ad",
            user="test-user",
            response_mode="blocking",
            timeout=60
        )
        print("✅ 自定义客户端调用成功!")
        print(f"响应结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return True
    except DifyAPIError as e:
        print(f"❌ 自定义客户端调用失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("开始测试Dify异步API调用功能...\n")
    
    # 测试1: 单个调用
    await test_single_call()
    
    # 测试2: 多个并发调用
    await test_multiple_calls()
    
    # 测试3: 自定义客户端
    await test_custom_client()
    
    print("\n测试完成!")

if __name__ == "__main__":
    asyncio.run(main()) 