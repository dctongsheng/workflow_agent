# 自动填写参数异步函数模块

这个模块提供了基于Dify聊天消息API的自动填写参数功能，支持异步调用和参数解析。

## 功能特性

- ✅ 异步HTTP请求，提高性能
- ✅ 自动解析API响应中的参数
- ✅ 完整的错误处理和异常管理
- ✅ 支持并发调用
- ✅ 可配置的超时时间
- ✅ 详细的日志记录
- ✅ 类型提示支持
- ✅ 灵活的输入格式支持

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
from auto_param_filler import auto_fill_parameters, get_filled_parameters

async def main():
    # 准备数据
    data_choose = [
        '/Files/RawData/V350099495_L04_read_1.fq.gz',
        '/Files/RawData/V350099495_L04_read_2.fq.gz',
        '/Files/RawData/Y00862D8.barcodeToPos.h5'
    ]
    
    query_template = {
        'SN': '',
        'RegistJson': '',
        'DataDir': '',
        'ImageTar': '',
        'ImagePreDir': '',
        'Tissue': '',
        'Reference': ''
    }
    
    try:
        # 调用API
        result = await auto_fill_parameters(data_choose, query_template)
        print("API调用成功:", result)
        
        # 获取已填写的参数
        filled_params = await get_filled_parameters(data_choose, query_template)
        print("已填写的参数:", filled_params)
        
    except Exception as e:
        print("API调用失败:", e)

asyncio.run(main())
```

### 2. 使用自定义客户端

```python
import asyncio
from auto_param_filler import AutoParamFiller

async def main():
    # 创建自定义客户端
    client = AutoParamFiller(
        base_url="http://172.28.140.214",
        api_key="your-api-key"
    )
    
    data_choose = [
        '/Files/RawData/V350099495_L04_read_1.fq.gz',
        '/Files/RawData/V350099495_L04_read_2.fq.gz',
        '/Files/RawData/Y00862D8.barcodeToPos.h5'
    ]
    
    query_template = {
        'SN': '',
        'RegistJson': '',
        'DataDir': '',
        'ImageTar': '',
        'ImagePreDir': '',
        'Tissue': '',
        'Reference': ''
    }
    
    try:
        result = await client.auto_fill_parameters(
            data_choose=data_choose,
            query_template=query_template,
            user="custom-user",
            response_mode="blocking",
            timeout=300
        )
        print("API调用成功:", result)
        
        # 解析参数
        filled_params = await client.parse_filled_parameters(result)
        print("已填写的参数:", filled_params)
        
    except Exception as e:
        print("API调用失败:", e)

asyncio.run(main())
```

### 3. 并发调用

```python
import asyncio
from auto_param_filler import auto_fill_parameters

async def main():
    # 准备多个请求
    requests = [
        (
            ['/Files/RawData/sample1_read_1.fq.gz', '/Files/RawData/sample1_read_2.fq.gz'],
            {'SN': '', 'DataDir': '', 'Reference': ''}
        ),
        (
            ['/Files/RawData/sample2_read_1.fq.gz', '/Files/RawData/sample2_read_2.fq.gz'],
            {'SN': '', 'DataDir': '', 'Reference': ''}
        ),
        (
            ['/Files/RawData/sample3_read_1.fq.gz', '/Files/RawData/sample3_read_2.fq.gz'],
            {'SN': '', 'DataDir': '', 'Reference': ''}
        ),
    ]
    
    # 并发执行
    tasks = [
        auto_fill_parameters(data_choose, query_template)
        for data_choose, query_template in requests
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

### auto_fill_parameters 函数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data_choose | Union[List[str], str] | - | 数据选择列表或字符串 |
| query_template | Dict[str, str] | - | 查询模板字典，包含需要填写的参数 |
| user | str | "abc-123" | 用户标识 |
| conversation_id | str | "" | 会话ID |

### get_filled_parameters 函数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data_choose | Union[List[str], str] | - | 数据选择列表或字符串 |
| query_template | Dict[str, str] | - | 查询模板字典 |
| user | str | "abc-123" | 用户标识 |
| conversation_id | str | "" | 会话ID |

### AutoParamFiller.auto_fill_parameters 方法

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data_choose | Union[List[str], str] | - | 数据选择列表或字符串 |
| query_template | Dict[str, str] | - | 查询模板字典 |
| user | str | "abc-123" | 用户标识 |
| response_mode | str | "blocking" | 响应模式 ("blocking" 或 "streaming") |
| conversation_id | str | "" | 会话ID |
| timeout | int | 300 | 超时时间（秒） |

## 错误处理

模块提供了自定义异常 `AutoParamFillerError` 来处理API调用错误：

```python
from auto_param_filler import AutoParamFillerError

try:
    result = await auto_fill_parameters(data_choose, query_template)
except AutoParamFillerError as e:
    print(f"API错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 配置

默认配置：
- 服务器地址: `http://172.28.140.214`
- API密钥: `app-I9zUYHi9izQnqdDBZ5Z0cGx6`
- 超时时间: 300秒

可以通过创建自定义客户端来修改这些配置。

## 响应格式

API响应格式示例：

```json
{
  "event": "message",
  "task_id": "892a2597-7b88-45b4-99e7-463db6e177da",
  "id": "06881e2c-5fbf-4a4a-953c-6793b23f1a6f",
  "message_id": "06881e2c-5fbf-4a4a-953c-6793b23f1a6f",
  "conversation_id": "88549684-6002-4c11-b39d-7b4454f272c7",
  "mode": "advanced-chat",
  "answer": "{\n  \"SN\": \"V350099495_L04\",\n  \"RegistJson\": \"\",\n  \"DataDir\": \"/Files/RawData\",\n  \"ImageTar\": \"\",\n  \"ImagePreDir\": \"\",\n  \"Tissue\": \"\",\n  \"Reference\": \"/Files/RawData/Y00862D8.barcodeToPos.h5\"\n}",
  "metadata": {
    "usage": {
      "prompt_tokens": 177,
      "prompt_unit_price": "2",
      "prompt_price_unit": "0.000001",
      "prompt_price": "0.000354",
      "completion_tokens": 72,
      "completion_unit_price": "8",
      "completion_price_unit": "0.000001",
      "completion_price": "0.000576",
      "total_tokens": 249,
      "total_price": "0.00093",
      "currency": "RMB",
      "latency": 5.784288950264454
    }
  },
  "created_at": 1750409398
}
```

解析后的参数格式：

```json
{
  "SN": "V350099495_L04",
  "RegistJson": "",
  "DataDir": "/Files/RawData",
  "ImageTar": "",
  "ImagePreDir": "",
  "Tissue": "",
  "Reference": "/Files/RawData/Y00862D8.barcodeToPos.h5"
}
```

## 测试

运行测试脚本：

```bash
cd planning_generate_api_v002
python test_auto_param_filler.py
```

## 日志

模块使用Python标准logging模块记录日志，包括：
- API调用成功/失败信息
- 网络错误
- 超时错误
- 参数解析错误
- 其他异常

日志级别默认为INFO，可以通过修改logging配置来调整。

## 注意事项

1. **API密钥安全**: 请确保API密钥的安全性，不要在代码中硬编码
2. **网络连接**: 确保能够访问Dify服务器
3. **数据格式**: 确保data_choose和query_template的格式正确
4. **超时设置**: 根据网络情况调整超时时间
5. **错误处理**: 建议在生产环境中添加适当的错误处理逻辑 