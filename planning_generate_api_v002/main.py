import json
from example import *
import asyncio
# from utils import query_nodes_and_relationships_by_label
from utils import query_app_nodes_for_nodes_list
from neo4j_search_node import search_node_by_contain_relationship
from py2neo import Graph
from typing import Optional, List, Dict, Any, Union
import json

# 连接到Neo4j数据库
graph = Graph("bolt://10.176.160.201:7687", auth=("stomics", "W867M3Goqzpfry6Z"))
from py2neo import Graph
from typing import Optional, List, Dict, Any, Union

def get_node_dependon(graph: Graph, model_id: int) -> Optional[Any]:
    """
    根据model_id获取节点的depend_on属性值
    
    Args:
        graph: Neo4j图数据库连接
        model_id: 节点的model_id属性值（唯一标识）
        
    Returns:
        depend_on属性值，如果节点不存在或没有depend_on属性则返回None
    """
    try:
        cypher_query = """
        MATCH (n {model_id: $model_id})
        RETURN n.depend_on as depend_on
        """
        
        result = graph.run(cypher_query, model_id=model_id)
        
        # 将结果转换为列表
        records = list(result)
        
        if records:
            # 获取第一条记录
            record = records[0]
            depend_on_value = record['depend_on']
            print(f"节点 {model_id} 的 depend_on 属性值: {depend_on_value}")
            return depend_on_value
        else:
            print(f"未找到 model_id 为 '{model_id}' 的节点")
            return None
            
    except Exception as e:
        print(f"查询节点depend_on属性时出错: {e}")
        return None
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
class DifyAPIError(Exception):
    """Dify API调用异常"""
    pass

from llm_dify import call_dify_workflow,get_docs

async def run_example(meta_info,query):
    final_result={}
    """测试函数"""
    try:
        # 测试调用
        # meta_info=data_meatinfo1
        data_meatinfo_json = json.dumps(meta_info,ensure_ascii=False)
        res = await process_data_meatinfo(data_meatinfo_json)
        print(res)
        # 解析JSON字符串为字典
        res_dict = json.loads(res)
        print(res_dict["data"])
        docs=get_docs(res_dict["data"])
        # print(docs)
        # start_node=find_first_node(meta_info)
        start_node=res_dict["data"]["start_node"]
        print("start_node",start_node)
        start_node=start_node
        data_name=res_dict["data"]["name"]
        print("data_name",data_name)
        result = await call_dify_workflow(
            query=query,
            data_meatinfo=data_name,
            docs=str(docs),
            start_node=start_node
        )
        print("API调用成功:")
        # print(json.dumps(result, ensure_ascii=False, indent=2))

        dify_result=result["data"]["outputs"]["structured_output"]["required_steps"]

        n=0
        print("dify_result",dify_result)
        print("dify_result",len(dify_result))
        final_result_list=[]        
        for i in dify_result:
            app_nodes=search_node_by_contain_relationship(i)
            i_dict={}
            i_dict["title"]=app_nodes["node_name"]
            i_dict["step"]=n
            i_dict["previous_step"]=get_node_dependon(graph,app_nodes["model_id"])
            if app_nodes["nodes_app"] != {}:
                i_dict["name"]=app_nodes["nodes_app"]["target_properties"]["workflow_name"]
                i_dict["oid"]=app_nodes["nodes_app"]["target_properties"]["workflow_id"]
                i_dict["description"]=i["nodes_app"]["target_properties"]["summary_short"]
                i_dict["input"]=i["nodes_app"]["target_properties"]["input_files"]
                i_dict["output"]=i["nodes_app"]["target_properties"]["output_files"]
                final_result_list.append(i_dict)
                
            else:
                i_dict["name"]=""
                i_dict["oid"]=""
                i_dict["description"]=""
                i_dict["input"]=""
                i_dict["output"]=""
                final_result_list.append(i_dict)
            n+=1
                # print("app_nodes:",app_nodes)
        # app_nodes=query_app_nodes_for_nodes_list(dify_result)

        # n=0
        # final_result_list=[]
        # print("app_nodes:",app_nodes)
        # for i in app_nodes:
        #     try:
        #         i_dict={}
                
        #         i_dict["title"]=i["name"]
        #         i_dict["step"]=n
        #         i_dict["previous_step"]=i["dependon"]
        #         i_dict["name"]=i["app_properties"]["workflow_name"]
        #         i_dict["oid"]=i["app_properties"]["workflow_id"]
        #         i_dict["description"]=i["app_properties"]["summary_short"]
        #         i_dict["input"]=i["app_properties"]["input_files"]
        #         i_dict["output"]=i["app_properties"]["output_files"]
        #         final_result_list.append(i_dict)
        #         n+=1
        #     except Exception as e:
        #         print(f"未知错误: {e}")
        
            
            
            
                
            
        final_result["planning_steps"]=final_result_list
        print(final_result)
        return final_result

        
    except DifyAPIError as e:
        print(f"API调用失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")






if __name__ == "__main__":
    query = "只进行拟时序和互作分析"
    data_meatinfo = auto_fill_parameters_data

    asyncio.run(run_example(meta_info=data_meatinfo,query=query))



