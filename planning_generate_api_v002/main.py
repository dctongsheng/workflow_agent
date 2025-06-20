import json
from example import *
import asyncio
# from utils import query_nodes_and_relationships_by_label
from utils import query_app_nodes_for_nodes_list
from neo4j_search_node import search_node_by_contain_relationship

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
        docs=get_docs(meta_info)
        print("meta_info",meta_info)
        result = await call_dify_workflow(
            query=query,
            data_meatinfo=str(meta_info["name"]),
            docs=str(docs)
        )
        print("API调用成功:")
        # print(json.dumps(result, ensure_ascii=False, indent=2))

        dify_result=result["data"]["outputs"]["structured_output"]["analysis_plans"]

        n=0
        final_result_list=[]        
        for i in dify_result:
            app_nodes=search_node_by_contain_relationship(i)
            i_dict={}
            i_dict["title"]=app_nodes["name"]
            i_dict["step"]=n
            i_dict["previous_step"]=app_nodes["dependon"]
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
        # print(final_result)
        return final_result

        
    except DifyAPIError as e:
        print(f"API调用失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")






if __name__ == "__main__":
    query = "帮我进行聚类分析"
    data_meatinfo = data_meatinfo1

    asyncio.run(run_example(meta_info=data_meatinfo,query=query))



