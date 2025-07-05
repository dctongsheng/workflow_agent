from py2neo import Graph
from typing import Dict, Optional, List, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_neo4j():
    """连接到Neo4j数据库"""
    try:
        return Graph("bolt://10.176.160.201:7687", auth=("stomics", "W867M3Goqzpfry6Z"))
    except Exception as e:
        logger.error(f"连接Neo4j失败: {e}")
        raise

def search_node_by_contain_relationship(node_params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    基于节点参数信息查询关系为"contain"的另外的边
    
    Args:
        node_params (Dict[str, Any]): 节点参数信息字典，包含节点的各种属性
                                    例如: {"model_id": 10, "name": "构建参考基因组索引", "type": "Workflow"}
        
    Returns:
        Optional[Dict[str, Any]]: 包含关系信息的字典，如果没有找到则返回None
    """
    try:
        graph = connect_to_neo4j()
        
        # 从节点参数中提取查询条件
        node_type = node_params.get('type')
        model_id = node_params.get('model_id')
        node_name = node_params.get('name')
        
        if not model_id:
            logger.error("节点参数中缺少model_id")
            return None
            
        # 构建查询条件
        where_conditions = []
        query_params = {}
        
        if node_type:
            where_conditions.append("(source.type = $node_type OR source.label = $node_type)")
            query_params['node_type'] = node_type
            
        if model_id:
            where_conditions.append("source.model_id = $model_id")
            query_params['model_id'] = model_id
            
        if node_name:
            where_conditions.append("source.name = $node_name")
            query_params['node_name'] = node_name
            
        if not where_conditions:
            logger.error("节点参数中缺少必要的查询条件")
            return None
            
        where_clause = " AND ".join(where_conditions)
        
        # Cypher查询：查找指定条件的节点，并查询其"contain"关系
        query = f"""
        MATCH (source)-[r:contain]->(target)
        WHERE {where_clause}
        RETURN target.name as target_name,
               labels(target) as target_labels,
               target.type as target_type,
               target.model_id as target_model_id,
               properties(target) as target_properties,
               properties(r) as relationship_properties,
               id(target) as target_node_id,
               id(r) as relationship_id,
               source.name as source_name,
               labels(source) as source_labels
        LIMIT 1
        """
        
        result = graph.run(query, **query_params).data()
        
        if result:
            # 返回第一个结果
            node_params["nodes_app"]=result[0]
            return node_params
        else:
            logger.info(f"未找到节点参数 {node_params} 的contain关系")
            node_params["nodes_app"]={}
            return node_params
            
    except Exception as e:
        logger.error(f"查询Neo4j时发生错误: {e}")
        raise

def search_all_contain_relationships(node_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    基于节点参数信息查询所有关系为"contain"的边
    
    Args:
        node_params (Dict[str, Any]): 节点参数信息字典
        
    Returns:
        List[Dict[str, Any]]: 包含所有关系信息的列表
    """
    try:
        graph = connect_to_neo4j()
        
        # 从节点参数中提取查询条件
        node_type = node_params.get('type')
        model_id = node_params.get('model_id')
        node_name = node_params.get('name')
        
        if not model_id:
            logger.error("节点参数中缺少model_id")
            return []
            
        # 构建查询条件
        where_conditions = []
        query_params = {}
        
        if node_type:
            where_conditions.append("(source.type = $node_type OR source.label = $node_type)")
            query_params['node_type'] = node_type
            
        if model_id:
            where_conditions.append("source.model_id = $model_id")
            query_params['model_id'] = model_id
            
        if node_name:
            where_conditions.append("source.name = $node_name")
            query_params['node_name'] = node_name
            
        if not where_conditions:
            logger.error("节点参数中缺少必要的查询条件")
            return []
            
        where_clause = " AND ".join(where_conditions)
        
        query = f"""
        MATCH (source)-[r:contain]->(target)
        WHERE {where_clause}
        RETURN target.name as target_name,
               labels(target) as target_labels,
               target.type as target_type,
               target.model_id as target_model_id,
               properties(target) as target_properties,
               properties(r) as relationship_properties,
               id(target) as target_node_id,
               id(r) as relationship_id,
               source.name as source_name,
               labels(source) as source_labels
        """
        
        result = graph.run(query, **query_params).data()
        
        if result:
            logger.info(f"找到 {len(result)} 个contain关系")
            return result
        else:
            logger.info(f"未找到节点参数 {node_params} 的contain关系")
            return []
            
    except Exception as e:
        logger.error(f"查询Neo4j时发生错误: {e}")
        raise

def search_node_by_contain_relationship_simple(node_params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    简化版本的查询函数，只基于model_id查询
    
    Args:
        node_params (Dict[str, Any]): 节点参数信息字典
        
    Returns:
        Optional[Dict[str, Any]]: 包含关系信息的字典，如果没有找到则返回None
    """
    try:
        graph = connect_to_neo4j()
        
        model_id = node_params.get('model_id')
        if not model_id:
            logger.error("节点参数中缺少model_id")
            return None
        
        # 简单的查询，只基于model_id
        query = """
        MATCH (source)-[r:contain]->(target)
        WHERE source.model_id = $model_id
        RETURN target.name as target_name,
               labels(target) as target_labels,
               target.type as target_type,
               target.model_id as target_model_id,
               properties(target) as target_properties,
               properties(r) as relationship_properties,
               id(target) as target_node_id,
               id(r) as relationship_id,
               source.name as source_name,
               labels(source) as source_labels
        LIMIT 1
        """
        
        result = graph.run(query, model_id=model_id).data()
        
        if result:
            return result[0]
        else:
            logger.info(f"未找到model_id={model_id}的节点的contain关系")
            return None
            
    except Exception as e:
        logger.error(f"查询Neo4j时发生错误: {e}")
        raise

# 使用示例
if __name__ == "__main__":
    # 示例用法 - 使用节点参数字典
    nodes_list = [
          {
            "model_id": 10,
            "name": "构建参考基因组索引",
            "text_input": "物种所对应的gtf和fasta文件",
            "dependon": []
          },
          {'name': '多样本整合分析', 'label': 'scRNA-seq', 'model_id': 12, 'node_id': 11, 'all_properties': {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '以多个样本下机的矩阵文件运行多样本整合后生成从数据质控、细胞聚类、注释、拟时序、互作、富集分析到最终产生交付报告全套分析流程', 'model_id': 12, 'name': '多样本整合分析', 'type': 'scRNA-seq', 'text_input': '以多个样本标准分析流程的输出文件中的FilterMatrix文件夹作为单样本输入，每个文件夹包含（barcodes.tsv.,gz，matrix.mtx.gz,fetures.tsv.gz）'}, 'dependon': ['scRNA-seq标准分析流程']},
          {
            "model_id": 11,
            "name": "scRNA-seq标准分析流程",
            "text_input": "下机数据cDNA和Oligo的fq.gz文件需对应，参考基因组索引文件夹",
            "dependon": [
              "构建参考基因组索引"
            ]
          },
          {
            "model_id": 13,
            "name": "数据质控分析",
            "text_input": "以标准分析流程的输出文件中的FilterMatrix文件夹作为单样本输入，每个文件夹包含（barcodes.tsv.,gz，matrix.mtx.gz,fetures.tsv.gz）",
            "dependon": [
              "scRNA-seq标准分析流程"
            ]
          },
          {
            "model_id": 14,
            "name": "数据预处理",
            "text_input": "输入质控后获得的h5ad文件",
            "dependon": [
              "数据质控分析"
            ]
          },
          {
            "model_id": 15,
            "name": "细胞聚类分析",
            "text_input": "输入预处理后获得的h5ad矩阵文件",
            "dependon": [
              "数据预处理"
            ]
          }
        ]
    for node_params in nodes_list:
        print(node_params)
        try:
            # 查询单个contain关系
            result = search_node_by_contain_relationship(node_params)
            print(result)
            if result:
                print("找到contain关系:")
                print(f"目标节点名称: {result['target_name']}")
                print(f"目标节点类型: {result['target_type']}")
                print(f"目标节点模型ID: {result['target_model_id']}")
            else:
                print("未找到contain关系")
                
            # 查询所有contain关系
            all_results = search_all_contain_relationships(node_params)
            print(f"总共找到 {len(all_results)} 个contain关系")
            
            # 使用简化版本
            simple_result = search_node_by_contain_relationship_simple(node_params)
            if simple_result:
                print("简化查询找到contain关系:")
                print(f"目标节点名称: {simple_result['target_name']}")
            
        except Exception as e:
            print(f"执行查询时发生错误: {e}")
