import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional
import logging
from example import *
from utils import query_nodes_and_relationships_by_label,process_data_meatinfo
from py2neo import Graph
import json
# from find_first_node.utils import find_first_node

# 连接到Neo4j数据库
graph = Graph("bolt://10.176.160.201:7687", auth=("stomics", "W867M3Goqzpfry6Z"))

def query_nodes_by_label(label):
    """
    根据标签查询该标签下的所有节点
    
    Args:
        label: 节点标签名称
        
    Returns:
        list: 节点列表
    """
    try:
        # 基本查询：获取指定标签的所有节点
        cypher_query = f"MATCH (n:{label}) RETURN n"
        
        result = graph.run(cypher_query)
        nodes = []
        
        for record in result:
            node = record['n']
            # 将节点转换为字典格式，便于处理
            node_dict = {
                'id': node.identity,  # 节点的内部ID
                'labels': list(node.labels),  # 节点标签
                'properties': dict(node)  # 节点属性
            }
            nodes.append(node_dict)
        
        print(f"找到 {len(nodes)} 个标签为 '{label}' 的节点")
        return nodes
    except Exception as e:
        print(f"查询节点时出错: {e}")
        return []

# 测试查询

def get_docs(data_meatinfo):
    # print("data_meatinfo:",data_meatinfo)   
    docs = query_nodes_by_label(data_meatinfo["omics"])
    # print("docs:",docs)
    res={}
    new_list=[]
    # 修复数据结构访问 - docs是列表，不是字典
    for i in docs:
        new_dic={}
        # 从properties中获取数据
        properties = i["properties"]
        new_dic["name"]=properties.get("name", "")
        new_dic["model_id"]=properties.get("model_id", "")
        new_dic["depend_on"]=properties.get("depend_on", "")
        new_dic["input_suffix"]=properties.get("input_suffix", "")
        new_list.append(new_dic)
    res["nodes"]=new_list
    print(res)
    return res
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DifyAPIError(Exception):
    """Dify API调用异常"""
    pass

class DifyClient:
    """Dify API客户端"""
    
    def __init__(self, base_url: str = "http://172.28.140.214", api_key: str = "app-zGRmCDL52IBOJPFSJ8S31wjs"):
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
        start_node: str,
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
                "query": str(query),
                "data_meatinfo": str(data_meatinfo),
                "docs": docs,
                "start_node": str(start_node)
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
    start_node: str,
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
    return await dify_client.run_workflow(query, data_meatinfo, docs, start_node, user)

# 示例使用
async def main():
    """测试函数"""
    try:
        # 测试调用
        data_meatinfo_json = json.dumps(auto_fill_parameters_data,ensure_ascii=False)
        res = await process_data_meatinfo(data_meatinfo_json)
        print(res)
        # 解析JSON字符串为字典
        res_dict = json.loads(res)
        print(res_dict["data"])
        docs=get_docs(res_dict["data"])
        # print(docs)
        # start_node=find_first_node(meta_info)
        start_node=res_dict["data"]["start_node"]
        start_node=start_node
        data_name=res_dict["data"]["name"]
        print(start_node)
        result = await call_dify_workflow(
            query="细胞互作分析",
            data_meatinfo=data_name,
            docs=str(docs),
            start_node=start_node
        )
        print("API调用成功:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except DifyAPIError as e:
        print(f"API调用失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
