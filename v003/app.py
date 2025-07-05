from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from py2neo import Graph
from typing import List, Dict, Any
import uvicorn

# 创建 FastAPI 应用
app = FastAPI(
    title="Neo4j 节点查询 API",
    description="根据标签查询 Neo4j 数据库中的节点",
    version="1.0.0"
)

# 连接到 Neo4j 数据库
graph = Graph("bolt://10.176.160.201:7687", auth=("stomics", "W867M3Goqzpfry6Z"))

# 请求模型
class LabelRequest(BaseModel):
    label: str

# 响应模型
class NodeResponse(BaseModel):
    id: int
    labels: List[str]
    properties: Dict[str, Any]

class QueryResponse(BaseModel):
    success: bool
    message: str
    count: int
    nodes: List[NodeResponse]

def query_nodes_by_label(label: str) -> List[Dict[str, Any]]:
    """
    根据标签查询该标签下的所有节点
    
    Args:
        label: 节点标签名称
        
    Returns:
        list: 节点列表
    """
    try:
        # 基本查询：获取指定标签的所有节点
        cypher_query = f"MATCH (n:{label}) RETURN n"
        
        result = graph.run(cypher_query)
        nodes = []
        
        for record in result:
            node = record['n']
            # 将节点转换为字典格式，便于处理
            node_dict = {
                'id': node.identity,  # 节点的内部ID
                'labels': list(node.labels),  # 节点标签
                'properties': dict(node)  # 节点属性
            }
            nodes.append(node_dict)
        
        return nodes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询节点时出错: {str(e)}")

@app.get("/")
async def root():
    """根路径，返回 API 信息"""
    return {
        "message": "Neo4j 节点查询 API",
        "version": "1.0.0",
        "endpoints": {
            "query_by_label": "/api/query/nodes",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 测试数据库连接
        graph.run("RETURN 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"数据库连接失败: {str(e)}")

@app.post("/api/query/nodes", response_model=QueryResponse)
async def query_nodes_by_label_api(request: LabelRequest):
    """
    根据标签查询节点
    
    Args:
        request: 包含标签信息的请求体
        
    Returns:
        QueryResponse: 查询结果
    """
    try:
        # 验证标签不为空
        if not request.label or not request.label.strip():
            raise HTTPException(status_code=400, detail="标签不能为空")
        
        # 查询节点
        nodes = query_nodes_by_label(request.label.strip())
        
        # 转换为响应格式
        node_responses = [
            NodeResponse(
                id=node['id'],
                labels=node['labels'],
                properties=node['properties']
            )
            for node in nodes
        ]
        
        return QueryResponse(
            success=True,
            message=f"找到 {len(nodes)} 个标签为 '{request.label}' 的节点",
            count=len(nodes),
            nodes=node_responses
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@app.get("/api/query/nodes/{label}", response_model=QueryResponse)
async def query_nodes_by_label_get(label: str):
    """
    根据标签查询节点 (GET 方法)
    
    Args:
        label: 节点标签
        
    Returns:
        QueryResponse: 查询结果
    """
    try:
        # 验证标签不为空
        if not label or not label.strip():
            raise HTTPException(status_code=400, detail="标签不能为空")
        
        # 查询节点
        nodes = query_nodes_by_label(label.strip())
        
        # 转换为响应格式
        node_responses = [
            NodeResponse(
                id=node['id'],
                labels=node['labels'],
                properties=node['properties']
            )
            for node in nodes
        ]
        
        return QueryResponse(
            success=True,
            message=f"找到 {len(nodes)} 个标签为 '{label}' 的节点",
            count=len(nodes),
            nodes=node_responses
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10104)
