from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
# from llm import generate_workflow_plan
import uvicorn
from utils import process_data_meatinfo
import json
# from intent_detection import detect_bioinformatics_intent
from main import run_example
from auto_param_filler import get_filled_parameters
from example import get_auto_fill_parameters
from call_dify import chat_with_api
from neo4j_search_node import search_node_by_contain_relationship
from main import get_node_dependon
from py2neo import Graph
from typing import Optional, List, Dict, Any, Union
from base_call_dify_workflow import intent_detection

# 连接到Neo4j数据库
graph = Graph("bolt://10.176.160.201:7687", auth=("stomics", "W867M3Goqzpfry6Z"))

app = FastAPI(
    title="Workflow Planning API",
    description="API for generating workflow plans using LLM",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

class PlanningRequest(BaseModel):
    query: str
    data_meatinfo: Dict[str, Any]

class PlanningResponse(BaseModel):
    code: int
    message: str
    structured_output: Optional[dict] = None

class IntentDetectionRequest(BaseModel):
    query: str

class IntentDetectionResponse(BaseModel):
    code: int
    message: str
    intent: int  # 1表示生信分析相关，0表示不相关
    is_bioinformatics_related: bool

class AutoFilledParamsRequest(BaseModel):
    data_meatinfo: Dict[str, Any]
    query_template: Dict[str, str]
    user: str = "abc-123"
    conversation_id: str = ""
    response_mode: str = "blocking"

class AutoFilledParamsResponse(BaseModel):
    code: int
    message: str
    filled_parameters: Optional[Dict[str, str]] = None

@app.post("/intent_detection", response_model=IntentDetectionResponse)
async def detect_intent(request: IntentDetectionRequest):
    """
    意图识别接口
    判断用户查询是否与生物信息学分析相关
    """
    try:
        # 调用意图识别函数
        intent_result = await intent_detection(request.query)
        
        return IntentDetectionResponse(
            code=200,
            message="Success",
            intent=intent_result,
            is_bioinformatics_related=intent_result == 1
        )
    except Exception as e:
        if "API key" in str(e):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        elif "rate limit" in str(e).lower():
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

@app.post("/planning_generate_old", response_model=PlanningResponse)
async def generate_planning_old(request: PlanningRequest):
    try:
        # 调用LLM生成工作流计划
        result = await run_example(
            meta_info=request.data_meatinfo,
            query=request.query
        )

        return PlanningResponse(
            code=200,
            message="Success",
            structured_output=result
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        if "API key" in str(e):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        elif "rate limit" in str(e).lower():
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
    
@app.post("/planning_generate", response_model=PlanningResponse)
async def generate_planning(request: PlanningRequest):
    final_result={}
    try:
        # 调用LLM生成工作流计划

        result_dify = await chat_with_api(
            inputs={"data_choose":json.dumps(request.data_meatinfo)},
            query=request.query
        )
        result_dify=json.loads(result_dify["answer"])
        dify_result=result_dify["structured_output"]["required_steps"]
        n=0
        print("dify_result",dify_result)
        print("dify_result",len(dify_result))
        final_result_list=[] 

        for i in dify_result:
            i["model_id"]=int(i["model_id"])
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

        final_result["planning_steps"]=final_result_list
        return PlanningResponse(
            code=200,
            message="Success",
            structured_output=final_result           
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        if "API key" in str(e):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        elif "rate limit" in str(e).lower():
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

@app.post("/auto_filled_params", response_model=AutoFilledParamsResponse)
async def auto_fill_parameters_endpoint(request: AutoFilledParamsRequest):
    """
    自动填写参数接口
    基于data_choose和query_template自动填充参数
    """
    # print(f"接收到的data_choose: {request.data_meatinfo}")
    rrr = request.data_meatinfo
    from data_process.data_p import get_data_from_auto_fill_params
    # print(rrr["records"][0])
    # res = []
    # for i in rrr["records"]:
    #     sun_param={}
    #     for key,value in i.items():
    #         if key in ["name","omics","menuPath","chipId"] and value != "":
                
    #             sun_param[key]=value
    #     res.append(sun_param)
    res=get_data_from_auto_fill_params(rrr)
    print(res)
    try:
        # 调用自动填写参数函数
        filled_params = await get_filled_parameters(
            data_choose=str(res),  # 直接传递，不转换为JSON字符串
            query_template=request.query_template,
            user=request.user,
            conversation_id=request.conversation_id,
            response_mode=request.response_mode
        )
        
        return AutoFilledParamsResponse(
            code=200,
            message="Success",
            filled_parameters=filled_params
        )
    except Exception as e:
        if "API key" in str(e):
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        elif "rate limit" in str(e).lower():
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8008, reload=True)








