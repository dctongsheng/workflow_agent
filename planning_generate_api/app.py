from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from llm import generate_workflow_plan
import uvicorn
from utils import process_data_meatinfo
import json
from intent_detection import detect_bioinformatics_intent

app = FastAPI(
    title="Workflow Planning API",
    description="API for generating workflow plans using LLM",
    version="1.0.0"
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

@app.post("/intent_detection", response_model=IntentDetectionResponse)
async def detect_intent(request: IntentDetectionRequest):
    """
    意图识别接口
    判断用户查询是否与生物信息学分析相关
    """
    try:
        # 调用意图识别函数
        intent_result = await detect_bioinformatics_intent(request.query)
        
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

@app.post("/planning_generate", response_model=PlanningResponse)
async def generate_planning(request: PlanningRequest):
    try:
        # 处理data_meatinfo
        # print(json.dumps(request.data_meatinfo))
        processed_meta = await process_data_meatinfo(json.dumps(request.data_meatinfo))
        processed_meta_json = json.loads(processed_meta)
        print(processed_meta_json)
        
        if not processed_meta_json["success"]:
            raise HTTPException(
                status_code=400,
                detail=processed_meta_json["message"]
            )

        # 调用LLM生成工作流计划
        result = await generate_workflow_plan(
            query=request.query,
            data_meatinfo=processed_meta_json["data"]
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

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)








