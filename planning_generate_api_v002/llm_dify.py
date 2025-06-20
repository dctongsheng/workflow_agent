import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional
import logging
from example import *
from utils import query_nodes_and_relationships_by_label


def get_docs(data_meatinfo):
    # print("data_meatinfo:",data_meatinfo)   
    docs = query_nodes_and_relationships_by_label(data_meatinfo["omics"])
    # print("docs:",docs)
    res={}
    new_list=[]
    # print(docs["data"]["nodes"])
    for i in docs["data"]["nodes"]:
        new_dic={}
        new_dic["name"]=i["name"]
        new_dic["model_id"]=i["model_id"]
        new_dic["description"]=i["all_properties"]["description"]
        new_dic["dependon"]=i["dependon"]
        new_dic["text_input"]=i["all_properties"]["text_input"]
        new_list.append(new_dic)
    res["nodes"]=new_list
    # print(res)
    return res
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DifyAPIError(Exception):
    """Dify API调用异常"""
    pass

class DifyClient:
    """Dify API客户端"""
    
    def __init__(self, base_url: str = "http://172.28.140.214", api_key: str = "app-UsYqYl0FxzbiexcetyViJS3L"):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    async def run_workflow(
        self, 
        query: str, 
        data_meatinfo: str, 
        docs: str,
        user: str = "abc-123",
        response_mode: str = "blocking",
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        异步调用Dify工作流
        
        Args:
            query: 用户查询
            data_meatinfo: 数据文件信息
            user: 用户标识
            response_mode: 响应模式 ("blocking" 或 "streaming")
            timeout: 超时时间（秒）
            
        Returns:
            API响应结果
            
        Raises:
            DifyAPIError: API调用失败时抛出
        """
        url = f"{self.base_url}/v1/workflows/run"
        
        payload = {
            "inputs": {
                "query": query,
                "data_meatinfo": data_meatinfo,
                "docs": docs
            },
            "response_mode": response_mode,
            "user": user
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Dify API调用成功: {query}")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Dify API调用失败: HTTP {response.status}, {error_text}")
                        raise DifyAPIError(f"HTTP {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            logger.error(f"Dify API调用超时: {query}")
            raise DifyAPIError("请求超时")
        except aiohttp.ClientError as e:
            logger.error(f"Dify API网络错误: {e}")
            raise DifyAPIError(f"网络错误: {e}")
        except Exception as e:
            logger.error(f"Dify API未知错误: {e}")
            raise DifyAPIError(f"未知错误: {e}")

# 创建全局客户端实例
dify_client = DifyClient()

async def call_dify_workflow(
    query: str, 
    data_meatinfo: str, 
    docs: str,
    user: str = "abc-123"
) -> Dict[str, Any]:
    """
    便捷函数：调用Dify工作流
    
    Args:
        query: 用户查询
        data_meatinfo: 数据文件信息
        user: 用户标识
        
    Returns:
        API响应结果
    """
    return await dify_client.run_workflow(query, data_meatinfo, docs, user)

# 示例使用
async def main():
    """测试函数"""
    try:
        # 测试调用
        meta_info=data_meatinfo1
        docs=get_docs(meta_info)
        result = await call_dify_workflow(
            query="细胞注释",
            data_meatinfo=meta_info["name"],
            docs=str(docs)
        )
        print("API调用成功:")
        # print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except DifyAPIError as e:
        print(f"API调用失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
