"""
API接口测试脚本
"""

import asyncio
import aiohttp
import json

async def test_intent_detection_api():
    """测试意图识别API接口"""
    
    # API基础URL
    base_url = "http://localhost:8000"
    
    # 测试用例
    test_cases = [
        "帮我使用时空组学的数据，进行标准分析和下游高级分析",
        "今天天气怎么样？",
        "请帮我分析基因表达数据",
        "我想看电影",
        "进行蛋白质组学分析",
        "帮我写一篇文章"
    ]
    
    print("=== 意图识别API测试 ===\n")
    
    async with aiohttp.ClientSession() as session:
        for query in test_cases:
            try:
                # 构建请求数据
                request_data = {"query": query}
                
                # 发送POST请求
                async with session.post(
                    f"{base_url}/intent_detection",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        print(f"查询: {query}")
                        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                        print("-" * 60)
                    else:
                        error_text = await response.text()
                        print(f"查询: {query}")
                        print(f"错误: HTTP {response.status} - {error_text}")
                        print("-" * 60)
                        
            except Exception as e:
                print(f"查询: {query}")
                print(f"异常: {str(e)}")
                print("-" * 60)

async def test_planning_generate_api():
    """测试工作流生成API接口"""
    
    base_url = "http://localhost:8000"
    
    # 测试数据
    test_data = {
        "query": "帮我使用时空组学的数据，进行标准分析和下游高级分析",
        "data_meatinfo": {
            "file_name": "mouse.fq.gz",
            "file_type": "fastq",
            "data_type": "spatial_transcriptomics"
        }
    }
    
    print("\n=== 工作流生成API测试 ===\n")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{base_url}/planning_generate",
                json=test_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                else:
                    error_text = await response.text()
                    print(f"错误: HTTP {response.status} - {error_text}")
                    
        except Exception as e:
            print(f"异常: {str(e)}")

if __name__ == "__main__":
    async def main():
        await test_intent_detection_api()
        await test_planning_generate_api()
    
    asyncio.run(main()) 