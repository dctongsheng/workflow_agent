from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class InputOutput(BaseModel):
    type: str = Field(description="输入或输出文件的类型")
    description: str = Field(description="输入或输出文件的描述")

class WorkflowStep(BaseModel):
    step: int = Field(description="步骤编号")
    previous_step: int = Field(description="前一步骤的编号")
    name: str = Field(description="工作流步骤名称")
    oid: str = Field(description="工作流步骤的唯一标识符")
    description: str = Field(description="工作流步骤的详细描述")
    input: InputOutput = Field(description="输入文件信息")
    output: InputOutput = Field(description="输出文件信息")
    title: str = Field(description="工作流步骤的标题")

class WorkflowResponse(BaseModel):
    """工作流响应的结构化输出格式"""
    steps: List[WorkflowStep] = Field(description="工作流步骤列表")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="额外的元数据信息")

def format_workflow_response(steps: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None) -> WorkflowResponse:
    """
    格式化工作流响应
    
    Args:
        steps: 工作流步骤列表
        metadata: 可选的元数据信息
        
    Returns:
        WorkflowResponse: 格式化后的响应对象
    """
    workflow_steps = [WorkflowStep(**step) for step in steps]
    return WorkflowResponse(steps=workflow_steps, metadata=metadata) 