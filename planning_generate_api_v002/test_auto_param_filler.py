#!/usr/bin/env python3
"""
测试自动填写参数功能
"""

import asyncio
import json
from auto_param_filler import (
    auto_fill_parameters, 
    get_filled_parameters, 
    AutoParamFiller, 
    AutoParamFillerError
)

async def test_single_call():
    """测试单个API调用"""
    print("=== 测试单个自动填写参数API调用 ===")
    try:
        # 测试数据
        data_choose = [
            '/Files/RawData/V350099495_L04_read_1.fq.gz',
            '/Files/RawData/V350099495_L04_read_2.fq.gz',
            '/Files/RawData/Y00862D8.barcodeToPos.h5'
        ]
        
        query_template = {
            'SN': '',
            'RegistJson': '',
            'DataDir': '',
            'ImageTar': '',
            'ImagePreDir': '',
            'Tissue': '',
            'Reference': ''
        }
        
        result = await auto_fill_parameters(data_choose, query_template)
        print("✅ API调用成功!")
        print(f"响应结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return True
    except AutoParamFillerError as e:
        print(f"❌ API调用失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

async def test_parameter_parsing():
    """测试参数解析功能"""
    print("\n=== 测试参数解析功能 ===")
    try:
        data_choose = [
            '/Files/RawData/V350099495_L04_read_1.fq.gz',
            '/Files/RawData/V350099495_L04_read_2.fq.gz',
            '/Files/RawData/Y00862D8.barcodeToPos.h5'
        ]
        
        query_template = {
            'SN': '',
            'RegistJson': '',
            'DataDir': '',
            'ImageTar': '',
            'ImagePreDir': '',
            'Tissue': '',
            'Reference': ''
        }
        
        filled_params = await get_filled_parameters(data_choose, query_template)
        print("✅ 参数解析成功!")
        print(f"已填写的参数: {json.dumps(filled_params, ensure_ascii=False, indent=2)}")
        return True
    except AutoParamFillerError as e:
        print(f"❌ 参数解析失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

async def test_multiple_calls():
    """测试多个并发API调用"""
    print("\n=== 测试多个并发自动填写参数API调用 ===")
    
    # 准备多个测试请求
    test_requests = [
        (
            ['/Files/RawData/sample1_read_1.fq.gz', '/Files/RawData/sample1_read_2.fq.gz'],
            {'SN': '', 'DataDir': '', 'Reference': ''}
        ),
        (
            ['/Files/RawData/sample2_read_1.fq.gz', '/Files/RawData/sample2_read_2.fq.gz'],
            {'SN': '', 'DataDir': '', 'Reference': ''}
        ),
        (
            ['/Files/RawData/sample3_read_1.fq.gz', '/Files/RawData/sample3_read_2.fq.gz'],
            {'SN': '', 'DataDir': '', 'Reference': ''}
        ),
    ]
    
    # 并发执行
    tasks = []
    for data_choose, query_template in test_requests:
        task = auto_fill_parameters(data_choose, query_template)
        tasks.append(task)
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, (data_choose, query_template) in enumerate(test_requests):
            if isinstance(results[i], Exception):
                print(f"❌ 请求 {i+1} 失败: {results[i]}")
            else:
                print(f"✅ 请求 {i+1} 成功")
                print(f"   数据: {data_choose}")
                print(f"   响应: {json.dumps(results[i], ensure_ascii=False, indent=2)}")
        
        return results
    except Exception as e:
        print(f"❌ 并发调用失败: {e}")
        return None

async def test_custom_client():
    """测试自定义客户端配置"""
    print("\n=== 测试自定义客户端配置 ===")
    
    # 创建自定义客户端
    custom_client = AutoParamFiller(
        base_url="http://172.28.140.214",
        api_key="app-I9zUYHi9izQnqdDBZ5Z0cGx6"
    )
    
    try:
        data_choose = [
            '/Files/RawData/V350099495_L04_read_1.fq.gz',
            '/Files/RawData/V350099495_L04_read_2.fq.gz',
            '/Files/RawData/Y00862D8.barcodeToPos.h5'
        ]
        
        query_template = {
            'SN': '',
            'RegistJson': '',
            'DataDir': '',
            'ImageTar': '',
            'ImagePreDir': '',
            'Tissue': '',
            'Reference': ''
        }
        
        result = await custom_client.auto_fill_parameters(
            data_choose=data_choose,
            query_template=query_template,
            user="test-user",
            response_mode="blocking",
            timeout=60
        )
        print("✅ 自定义客户端调用成功!")
        print(f"响应结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return True
    except AutoParamFillerError as e:
        print(f"❌ 自定义客户端调用失败: {e}")
        return False

async def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    # 测试无效的API密钥
    try:
        invalid_client = AutoParamFiller(
            base_url="http://172.28.140.214",
            api_key="invalid-api-key"
        )
        
        result = await invalid_client.auto_fill_parameters(
            data_choose=["test.fq.gz"],
            query_template={"SN": ""}
        )
        print("❌ 应该失败但没有失败")
        return False
    except AutoParamFillerError as e:
        print(f"✅ 正确处理了无效API密钥错误: {e}")
        return True
    except Exception as e:
        print(f"❌ 意外的错误类型: {e}")
        return False

async def main():
    """主测试函数"""
    print("开始测试自动填写参数异步API调用功能...\n")
    
    # 测试1: 单个调用
    await test_single_call()
    
    # 测试2: 参数解析
    await test_parameter_parsing()
    
    # 测试3: 多个并发调用
    await test_multiple_calls()
    
    # 测试4: 自定义客户端
    await test_custom_client()
    
    # 测试5: 错误处理
    await test_error_handling()
    
    print("\n测试完成!")

if __name__ == "__main__":
    asyncio.run(main()) 