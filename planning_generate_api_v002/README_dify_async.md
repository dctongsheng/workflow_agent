# Dify异步API调用模块

这个模块提供了异步调用Dify API的功能，支持单个和并发API调用。

## 功能特性

- ✅ 异步HTTP请求，提高性能
- ✅ 完整的错误处理和异常管理
- ✅ 支持并发调用
- ✅ 可配置的超时时间
- ✅ 详细的日志记录
- ✅ 类型提示支持

## 安装依赖

```bash
pip install aiohttp>=3.8.0
```

或者使用requirements.txt：

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基本使用

```python
import asyncio
from llm_dify import call_dify_workflow

async def main():
    try:
        result = await call_dify_workflow(
            query="细胞注释",
            data_meatinfo="1111.h5ad"
        )
        print("API调用成功:", result)
    except Exception as e:
        print("API调用失败:", e)

asyncio.run(main())
```

### 2. 使用自定义客户端

```python
import asyncio
from llm_dify import DifyClient

async def main():
    # 创建自定义客户端
    client = DifyClient(
        base_url="http://172.28.140.214",
        api_key="your-api-key"
    )
    
    try:
        result = await client.run_workflow(
            query="细胞注释",
            data_meatinfo="1111.h5ad",
            user="custom-user",
            response_mode="blocking",
            timeout=300
        )
        print("API调用成功:", result)
    except Exception as e:
        print("API调用失败:", e)

asyncio.run(main())
```

### 3. 并发调用

```python
import asyncio
from llm_dify import call_dify_workflow

async def main():
    # 准备多个请求
    requests = [
        ("细胞注释", "1111.h5ad"),
        ("基因表达分析", "2222.h5ad"),
        ("蛋白质组学分析", "3333.h5ad"),
    ]
    
    # 并发执行
    tasks = [
        call_dify_workflow(query, data_meatinfo)
        for query, data_meatinfo in requests
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"请求 {i+1} 失败: {result}")
        else:
            print(f"请求 {i+1} 成功: {result}")

asyncio.run(main())
```

## API参数说明

### call_dify_workflow 函数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | str | - | 用户查询内容 |
| data_meatinfo | str | - | 数据文件信息 |
| user | str | "abc-123" | 用户标识 |

### DifyClient.run_workflow 方法

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | str | - | 用户查询内容 |
| data_meatinfo | str | - | 数据文件信息 |
| user | str | "abc-123" | 用户标识 |
| response_mode | str | "blocking" | 响应模式 ("blocking" 或 "streaming") |
| timeout | int | 300 | 超时时间（秒） |

## 错误处理

模块提供了自定义异常 `DifyAPIError` 来处理API调用错误：

```python
from llm_dify import DifyAPIError

try:
    result = await call_dify_workflow("查询", "数据文件")
except DifyAPIError as e:
    print(f"API错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 配置

默认配置：
- 服务器地址: `http://172.28.140.214`
- API密钥: `app-UsYqYl0FxzbiexcetyViJS3L`
- 超时时间: 300秒

可以通过创建自定义客户端来修改这些配置。

## 测试

运行测试脚本：

```bash
cd planning_generate_api_v002
python test_dify_async.py
```

## 日志

模块使用Python标准logging模块记录日志，包括：
- API调用成功/失败信息
- 网络错误
- 超时错误
- 其他异常

日志级别默认为INFO，可以通过修改logging配置来调整。 