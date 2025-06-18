from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv(".env")
from prompt import system_prompt,user_prompt
from langchain_core.prompts import ChatPromptTemplate
from workflow_schema import WorkflowPlan
from langchain_core.messages import HumanMessage, SystemMessage
from intent_detection import detect_bioinformatics_intent
import json
import asyncio

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

请仔细分析用户的查询，如果查询与生物信息学分析相关，返回1；如果不相关，返回0。
只返回数字，不要其他解释。"""

# 意图识别的用户提示词模板
INTENT_USER_PROMPT = """用户查询：{query}

请判断这个查询是否与生物信息学分析相关。"""

async def generate_workflow_plan(query: str, data_meatinfo: str) -> dict:
    model = init_chat_model("qwen-max", model_provider="openai"
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", user_prompt)]
    )

    with open("./planning_generate_api/data/retrive_data.json", "r") as f:
        docs = json.load(f)
    docs = docs["docs"]

    model_with_tools = model.bind_tools([WorkflowPlan])
    input_f = prompt_template.invoke({
        "docs": docs,
        "query": query,
        "data_meatinfo": data_meatinfo
    })
    
    ai_msg = await model_with_tools.ainvoke(input_f)
    return ai_msg.tool_calls[0]["args"]

# 示例使用
if __name__ == "__main__":
    async def main():
        # 测试意图识别功能
        test_queries = [
            "帮我使用时空组学的数据，进行标准分析和下游高级分析",
            "今天天气怎么样？",
            "请帮我分析基因表达数据",
            "我想看电影",
            "进行蛋白质组学分析",
            "帮我写一篇文章"
        ]
        
        print("=== 意图识别测试 ===")
        for query in test_queries:
            intent = await detect_bioinformatics_intent(query)
            print(f"查询: {query}")
            print(f"意图: {'生信分析相关' if intent == 1 else '非生信分析相关'} ({intent})")
            print("-" * 50)
        
        print("\n=== 工作流生成测试 ===")
        result = await generate_workflow_plan(
            query="帮我使用时空组学的数据，进行标准分析和下游高级分析",
            data_meatinfo="mouse.fq.gz"
        )
        print(result)

    asyncio.run(main())