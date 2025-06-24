# Neo4j 节点查询 API

基于 FastAPI 实现的 Neo4j 节点查询 API，可以根据标签查询数据库中的节点。

## 功能特性

- 根据标签查询 Neo4j 数据库中的节点
- 支持 POST 和 GET 两种请求方式
- 完整的错误处理和响应格式
- 健康检查接口
- 自动生成的 API 文档

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python app.py
```

服务将在 `http://localhost:8000` 启动。

## API 接口

### 1. 根路径
- **URL**: `GET /`
- **描述**: 返回 API 基本信息
- **响应示例**:
```json
{
  "message": "Neo4j 节点查询 API",
  "version": "1.0.0",
  "endpoints": {
    "query_by_label": "/api/query/nodes",
    "health": "/health"
  }
}
```

### 2. 健康检查
- **URL**: `GET /health`
- **描述**: 检查服务状态和数据库连接
- **响应示例**:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 3. 根据标签查询节点 (POST)
- **URL**: `POST /api/query/nodes`
- **描述**: 通过 POST 请求体传递标签信息查询节点
- **请求体**:
```json
{
  "label": "app"
}
```
- **响应示例**:
```json
{
  "success": true,
  "message": "找到 60 个标签为 'app' 的节点",
  "count": 60,
  "nodes": [
    {
      "id": 25,
      "labels": ["app"],
      "properties": {
        "workflow_id": "68243cd1e27ff3f8ca8e5285",
        "name": "SAW-ST-V8-realign",
        "type": "app",
        "omics": "STOmics"
      }
    }
  ]
}
```

### 4. 根据标签查询节点 (GET)
- **URL**: `GET /api/query/nodes/{label}`
- **描述**: 通过 URL 路径参数传递标签信息查询节点
- **示例**: `GET /api/query/nodes/app`
- **响应格式**: 与 POST 方法相同

## API 文档

启动服务后，可以访问以下地址查看自动生成的 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 错误处理

API 包含完整的错误处理机制：

- **400 Bad Request**: 标签为空或格式错误
- **500 Internal Server Error**: 服务器内部错误或数据库查询失败
- **503 Service Unavailable**: 数据库连接失败

## 使用示例

### 使用 curl 测试

```bash
# 健康检查
curl http://localhost:8000/health

# POST 方式查询
curl -X POST "http://localhost:8000/api/query/nodes" \
     -H "Content-Type: application/json" \
     -d '{"label": "app"}'

# GET 方式查询
curl http://localhost:8000/api/query/nodes/app
```

### 使用 Python 测试

```python
import requests

# 查询节点
response = requests.post(
    "http://localhost:8000/api/query/nodes",
    json={"label": "app"}
)

if response.status_code == 200:
    data = response.json()
    print(f"找到 {data['count']} 个节点")
    for node in data['nodes']:
        print(f"节点 ID: {node['id']}, 名称: {node['properties'].get('name', 'N/A')}")
else:
    print(f"请求失败: {response.status_code}")
``` 