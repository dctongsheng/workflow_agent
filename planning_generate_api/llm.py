from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv(".env")
from prompt import system_prompt,user_prompt
from langchain_core.prompts import ChatPromptTemplate
from workflow_schema import WorkflowPlan
from langchain_core.messages import HumanMessage, SystemMessage
import json
import asyncio

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
        result = await generate_workflow_plan(
            query="帮我使用时空组学的数据，进行标准分析和下游高级分析",
            data_meatinfo="mouse.fq.gz"
        )
        print(result)

    asyncio.run(main())