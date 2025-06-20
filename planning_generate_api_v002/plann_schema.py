from typing import Optional, List
from pydantic import BaseModel, Field

class AnalysisPlan(BaseModel):
    """单个分析计划的数据结构"""
    # description: str = Field(description="分析流程的详细描述")
    model_id: int = Field(description="模型ID")
    name: str = Field(description="分析流程名称")
    text_input: str = Field(description="输入数据要求说明")
    dependon: List[str] = Field(description="依赖的前置分析步骤列表")

class AnalysisPlanList(BaseModel):
    """分析计划列表的完整结构"""
    analysis_plans: List[AnalysisPlan] = Field(description="分析计划列表")

# 使用示例:
# structured_llm = llm.with_structured_output(AnalysisPlanList)
# result = structured_llm.invoke("生成生物信息学分析流程计划...")
