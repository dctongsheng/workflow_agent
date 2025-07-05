"""
意图识别模块
用于判断用户查询是否与生物信息学分析相关
"""

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv(".env")

# 意图识别的系统提示词
INTENT_SYSTEM_PROMPT = """你是一个专业的生物信息学意图识别助手。你的任务是判断用户的查询是否与生物信息学分析相关。

生物信息学分析相关的查询通常包括但不限于：
- 基因表达分析
- 蛋白质组学分析
- 代谢组学分析
- 基因组学分析
- 转录组学分析
- 时空组学分析
- 单细胞测序分析
- 生物信息学数据处理
- 生物标志物发现
- 通路分析
- 差异表达分析
- 聚类分析
- 生物信息学可视化
- 序列分析
- 结构生物学分析
- 生物信息学工作流
- 数据分析流程
- 生物信息学工具使用

请仔细分析用户的查询，如果查询与生物信息学分析相关，返回1；如果不相关，返回0。
只返回数字，不要其他解释。"""

# 意图识别的用户提示词模板
INTENT_USER_PROMPT = """用户查询：{query}

请判断这个查询是否与生物信息学分析相关。"""

async def detect_bioinformatics_intent(query: str) -> int:
    """
    检测用户查询是否与生物信息学分析相关
    
    Args:
        query (str): 用户的查询字符串
        
    Returns:
        int: 1表示与生信分析相关，0表示不相关
    """
    model = init_chat_model("qwen-max", model_provider="openai")
    
    # 创建意图识别的提示模板
    intent_prompt = ChatPromptTemplate.from_messages([
        ("system", INTENT_SYSTEM_PROMPT),
        ("user", INTENT_USER_PROMPT)
    ])
    
    # 构建输入
    input_messages = intent_prompt.invoke({"query": query})
    
    # 调用模型
    response = await model.ainvoke(input_messages)
    print(response)
    
    # 解析响应
    try:
        result = int(response.content.strip())
        return result if result in [0, 1] else 0
    except (ValueError, AttributeError):
        # 如果解析失败，默认返回0
        return 0

def is_bioinformatics_related(intent_result: int) -> bool:
    """
    根据意图识别结果判断是否与生信分析相关
    
    Args:
        intent_result (int): 意图识别结果
        
    Returns:
        bool: True表示相关，False表示不相关
    """
    return intent_result == 1 

