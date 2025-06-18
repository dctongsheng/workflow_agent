# 意图识别功能说明

## 概述

意图识别功能用于判断用户的查询是否与生物信息学分析相关。该功能基于大语言模型，能够准确识别各种生物信息学相关的查询。

## 功能特点

- **智能识别**: 基于大语言模型的语义理解能力
- **高准确率**: 针对生物信息学领域优化的提示词
- **快速响应**: 异步处理，支持并发请求
- **易于集成**: 提供简单的API接口

## API接口

### 意图识别接口

**端点**: `POST /intent_detection`

**请求体**:
```json
{
    "query": "用户的查询字符串"
}
```

**响应体**:
```json
{
    "code": 200,
    "message": "Success",
    "intent": 1,
    "is_bioinformatics_related": true
}
```

**参数说明**:
- `intent`: 意图识别结果，1表示生信分析相关，0表示不相关
- `is_bioinformatics_related`: 布尔值，表示是否与生信分析相关

## 使用示例

### Python代码示例

```python
import asyncio
from intent_detection import detect_bioinformatics_intent

async def main():
    # 测试生信分析相关的查询
    query1 = "帮我使用时空组学的数据，进行标准分析和下游高级分析"
    result1 = await detect_bioinformatics_intent(query1)
    print(f"查询: {query1}")
    print(f"结果: {result1} (1=相关, 0=不相关)")
    
    # 测试非生信分析相关的查询
    query2 = "今天天气怎么样？"
    result2 = await detect_bioinformatics_intent(query2)
    print(f"查询: {query2}")
    print(f"结果: {result2} (1=相关, 0=不相关)")

asyncio.run(main())
```

### API调用示例

```bash
curl -X POST "http://localhost:8000/intent_detection" \
     -H "Content-Type: application/json" \
     -d '{"query": "帮我使用时空组学的数据，进行标准分析和下游高级分析"}'
```

## 支持的查询类型

### 生信分析相关查询

以下类型的查询会被识别为生信分析相关（返回1）：

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

### 非生信分析相关查询

以下类型的查询会被识别为非生信分析相关（返回0）：

- 日常对话
- 娱乐相关
- 其他技术领域
- 生活服务
- 教育学习（非生信领域）

## 测试

运行测试脚本：

```bash
# 测试意图识别功能
python test_intent.py

# 测试API接口
python test_api.py
```

## 集成到现有系统

在现有的工作流生成系统中，可以在生成工作流之前先进行意图识别：

```python
from intent_detection import detect_bioinformatics_intent
from llm import generate_workflow_plan

async def process_user_query(query: str, data_meatinfo: str):
    # 首先进行意图识别
    intent = await detect_bioinformatics_intent(query)
    
    if intent == 1:
        # 生信分析相关，生成工作流
        workflow = await generate_workflow_plan(query, data_meatinfo)
        return {"type": "workflow", "data": workflow}
    else:
        # 非生信分析相关，返回提示信息
        return {"type": "message", "data": "抱歉，我只能处理生物信息学分析相关的查询。"}
```

## 注意事项

1. 确保环境变量中配置了正确的API密钥
2. 意图识别功能需要网络连接以调用大语言模型
3. 建议在生产环境中添加适当的缓存机制以提高性能
4. 可以根据具体需求调整提示词以优化识别准确率 