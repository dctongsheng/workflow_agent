from py2neo import Graph
import json
from typing import Dict, Optional, List
import asyncio
def merge_list_to_dict(input_list):
    result = {}
    
    for item in input_list:
        for key, value in item.items():
            if key in result:
                # 处理 'omics' 字段
                if key in ['omics']:
                    # 记录出现次数
                    if isinstance(result[key], dict):
                        result[key][value] += 1
                    else:
                        result[key] = result[key]
                else:
                    # 处理其他字段
                    if isinstance(result[key], list):
                        result[key].append(value)
                    else:
                        result[key] = [result[key], value]
            else:
                # 如果键不存在，直接赋值
                result[key] = value

    # 处理 'omics' 字段，找到出现次数最多的值
    if 'omics' in result:
        if isinstance(result['omics'], dict):
            most_common_omics = max(result['omics'], key=result['omics'].get)
            result['omics'] = most_common_omics
        # 如果omics已经是字符串，保持不变（只有一个值的情况）
        # 不需要额外的处理

    return result


def process_data_0630(input_list):
    # 初始化结果字典
    result = {
        "name": [],
        "start_node": [],
        "omics": ""
    }
    
    # 遍历输入列表
    for item in input_list:
        # 添加 name 和 start_node
        result["name"].append(item.get("name", ""))
        result["start_node"].append(item.get("start_node", ""))
        
        # 更新 omics，取最后一个不为空的值
        if item.get("omics"):
            result["omics"] = item["omics"]
    
    return result
from find_first_node.utils import workflow_dict,app_dict

import re

def extract_standard_name(input_str):
    """
    从输入字符串中提取标准化名称：
    - 去掉 "Copy-" 前缀（如果存在）
    - 去掉 "(数字)" 后缀（如果存在）
    - 返回剩余部分
    """
    # 1. 去掉 "Copy-" 前缀
    if input_str.startswith("Copy-"):
        input_str = input_str[5:]
    
    # 2. 去掉 "(数字)" 后缀
    input_str = re.sub(r'\(\d+\)$', '', input_str)
    
    return input_str

def extract_standard_name_str(input_str):
    new_omics_ = extract_standard_name(input_str)
    if new_omics_ in app_dict:
        new_omics_ = app_dict[new_omics_]
    else:   
        print("new_omics_",new_omics_)
        new_omics_ = "查不到该组学："+new_omics_

    return new_omics_

async def process_data_meatinfo(data_meatinfo: str):
    """
    处理data_meatinfo的JSON数据
    
    Args:
        data_meatinfo (str): JSON格式的数据元信息字符串
        
    Returns:
        str: JSON格式的处理结果字符串
    """
    try:
        # 解析JSON字符串
        data = json.loads(data_meatinfo)
        # print("data",data)
        
        # 检查数据格式
        if not isinstance(data, dict) or "records" not in data:
            return json.dumps({
                "success": False,
                "message": "Invalid data format: missing 'records' field",
                "data": None
            })
            
        records = data["records"]
        # print(records)
        if not isinstance(records, list) or not records:
            return json.dumps({
                "success": False,
                "message": "Invalid data format: 'records' should be a non-empty list",
                "data": None
            })
            
        # 处理每条记录
        processed_records = []
        for record in records:
            
            if not isinstance(record, dict):
                continue
                
            
            if record["dataType"]=="0":
                processed_record = {}
                if "name" in record:
                    processed_record["name"] = record["name"]
                    file_suffix=record["name"].split(".")[-1]
                    
                if "omics" in record:
                    if "wfTag" in record:
                        # print("record",record)
                        print("record：",record["wfTag"])
                        omics_name_0630= extract_standard_name_str(record["wfTag"])
                        print("omics_name_0630：",omics_name_0630)
                        processed_record["omics"] = omics_name_0630

                        if record["wfTag"] in workflow_dict:
                            processed_record["start_node"] = workflow_dict[record["wfTag"]]
                        elif file_suffix=="gef":
                            processed_record["start_node"] = "SAW标准分析"
                        elif file_suffix=="h5ad":
                            processed_record["start_node"] = "数据质控分析"
                        else:
                            processed_record["start_node"] = ""
                    else:  # "wfTag" not in record
                        if file_suffix=="gef":
                            processed_record["start_node"] = "SAW标准分析"
                        elif file_suffix=="h5ad":
                            processed_record["start_node"] = "数据质控分析"
                        else:
                            processed_record["start_node"] = ""
                        processed_record["omics"] = ""
                else:  # "omics" not in record
                    if "wfTag" in record:
                        if record["wfTag"] in workflow_dict:
                            processed_record["start_node"] = workflow_dict[record["wfTag"]]
                        elif file_suffix=="gef":
                            processed_record["start_node"] = "SAW标准分析"
                        elif file_suffix=="h5ad":
                            processed_record["start_node"] = "数据质控分析"
                        else:
                            processed_record["start_node"] = ""
                        processed_record["omics"] = ""
                    else:  # "wfTag" not in record
                        if file_suffix=="gef":
                            processed_record["start_node"] = "SAW标准分析"
                        elif file_suffix=="h5ad":
                            processed_record["start_node"] = "数据质控分析"
                        else:
                            processed_record["start_node"] = ""
                        processed_record["omics"] = ""
                
                # print("processed_record",processed_record)
                processed_records.append(processed_record)



        print("processed_records",processed_records)
        if not processed_records:
            return json.dumps({
                "success": False,
                "message": "No valid records found",
                "data": None
            })
            
        return json.dumps({
            "success": True,
            "message": "Success",
            "data": process_data_0630(processed_records)
        })
        
    except json.JSONDecodeError:
        return json.dumps({
            "success": False,
            "message": "Invalid JSON format",
            "data": None
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        })

def connect_to_neo4j():
    """连接到Neo4j数据库"""
    return Graph("bolt://172.28.140.214:7687", auth=("neo4j", "f012464998"))

def query_omics_scenario_nodes_and_relationships():
    """
    查询生信领域场景的节点和关系
    
    生信领域场景包括：
    - scVDJ-seq
    - scATAC-Seq
    - Genomics
    - scRNA-seq
    - STOmics
    
    返回:
        dict: 包含节点和关系信息的字典
    """
    try:
        graph = connect_to_neo4j()
        
        # 定义生信领域场景标签
        omics_labels = [
            "scVDJ-seq",
            "scATAC-Seq", 
            "Genomics",
            "scRNA-seq",
            "STOmics"
        ]
        
        # 查询指定标签的节点
        nodes_query = """
        MATCH (n)
        WHERE labels(n)[0] IN $omics_labels
        RETURN n.name as name, 
               labels(n)[0] as label, 
               n.model_id as model_id,

               id(n) as node_id,
               properties(n) as all_properties
        """
        
        nodes_result = graph.run(nodes_query, omics_labels=omics_labels).data()
        
        # 查询这些节点之间的关系
        relationships_query = """
        MATCH (source)-[r]->(target)
        WHERE labels(source)[0] IN $omics_labels OR labels(target)[0] IN $omics_labels
        RETURN source.name as source_name,
               target.name as target_name,
               labels(source)[0] as source_label,
               labels(target)[0] as target_label,
               type(r) as relationship_type,
               properties(r) as relationship_properties,
               id(r) as relationship_id
        """
        
        relationships_result = graph.run(relationships_query, omics_labels=omics_labels).data()
        
        # 查询节点之间的双向关系（包括指向这些节点的关系）
        incoming_relationships_query = """
        MATCH (source)-[r]->(target)
        WHERE labels(target)[0] IN $omics_labels
        RETURN source.name as source_name,
               target.name as target_name,
               labels(source)[0] as source_label,
               labels(target)[0] as target_label,
               type(r) as relationship_type,
               properties(r) as relationship_properties,
               id(r) as relationship_id
        """
        
        incoming_result = graph.run(incoming_relationships_query, omics_labels=omics_labels).data()
        
        # 合并所有关系结果
        all_relationships = relationships_result + incoming_result
        
        # 去重关系（基于关系ID）
        unique_relationships = {}
        for rel in all_relationships:
            rel_id = rel['relationship_id']
            if rel_id not in unique_relationships:
                unique_relationships[rel_id] = rel
        
        relationships_list = list(unique_relationships.values())
        
        # 构建返回结果
        result = {
            "success": True,
            "message": f"成功查询到 {len(nodes_result)} 个节点和 {len(relationships_list)} 个关系",
            "data": {
                "nodes": nodes_result,
                "relationships": relationships_list,
                "statistics": {
                    "total_nodes": len(nodes_result),
                    "total_relationships": len(relationships_list),
                    "omics_labels": omics_labels
                }
            }
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": f"查询生信领域场景时出错: {str(e)}",
            "data": None
        }

def query_omics_nodes_by_label(specific_label=None):
    """
    查询指定生信领域标签的节点
    
    参数:
        specific_label: 指定的标签，如果为None则查询所有生信领域标签
    返回:
        dict: 包含节点信息的字典
    """
    try:
        graph = connect_to_neo4j()
        
        # 定义生信领域场景标签
        omics_labels = [
            "scVDJ-seq",
            "scATAC-Seq", 
            "Genomics",
            "scRNA-seq",
            "STOmics"
        ]
        
        if specific_label:
            if specific_label not in omics_labels:
                return {
                    "success": False,
                    "message": f"指定的标签 '{specific_label}' 不在生信领域场景列表中",
                    "data": None
                }
            query_labels = [specific_label]
        else:
            query_labels = omics_labels
        
        # 查询指定标签的节点
        nodes_query = """
        MATCH (n)
        WHERE labels(n)[0] IN $omics_labels
        RETURN n.name as name, 
               labels(n)[0] as label, 
               n.model_id as model_id,

               id(n) as node_id,
               properties(n) as all_properties
        ORDER BY labels(n)[0], n.name
        """
        
        nodes_result = graph.run(nodes_query, omics_labels=query_labels).data()
        
        # 按标签分组统计
        label_stats = {}
        for node in nodes_result:
            label = node['label']
            if label not in label_stats:
                label_stats[label] = 0
            label_stats[label] += 1
        
        result = {
            "success": True,
            "message": f"成功查询到 {len(nodes_result)} 个节点",
            "data": {
                "nodes": nodes_result,
                "statistics": {
                    "total_nodes": len(nodes_result),
                    "label_statistics": label_stats,
                    "queried_labels": query_labels
                }
            }
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": f"查询生信领域节点时出错: {str(e)}",
            "data": None
        }

def query_omics_relationships_by_type(relationship_type=None):
    """
    查询生信领域节点之间的关系
    
    参数:
        relationship_type: 指定的关系类型，如果为None则查询所有关系
    返回:
        dict: 包含关系信息的字典
    """
    try:
        graph = connect_to_neo4j()
        
        # 定义生信领域场景标签
        omics_labels = [
            "scVDJ-seq",
            "scATAC-Seq", 
            "Genomics",
            "scRNA-seq",
            "STOmics"
        ]
        
        if relationship_type:
            # 查询指定类型的关系
            relationships_query = """
            MATCH (source)-[r]->(target)
            WHERE (labels(source)[0] IN $omics_labels OR labels(target)[0] IN $omics_labels)
            AND type(r) = $relationship_type
            RETURN source.name as source_name,
                   target.name as target_name,
                   labels(source)[0] as source_label,
                   labels(target)[0] as target_label,
                   type(r) as relationship_type,
                   properties(r) as relationship_properties,
                   id(r) as relationship_id
            """
            relationships_result = graph.run(relationships_query, 
                                           omics_labels=omics_labels,
                                           relationship_type=relationship_type).data()
        else:
            # 查询所有关系
            relationships_query = """
            MATCH (source)-[r]->(target)
            WHERE labels(source)[0] IN $omics_labels OR labels(target)[0] IN $omics_labels
            RETURN source.name as source_name,
                   target.name as target_name,
                   labels(source)[0] as source_label,
                   labels(target)[0] as target_label,
                   type(r) as relationship_type,
                   properties(r) as relationship_properties,
                   id(r) as relationship_id
            """
            relationships_result = graph.run(relationships_query, omics_labels=omics_labels).data()
        
        # 按关系类型分组统计
        relationship_stats = {}
        for rel in relationships_result:
            rel_type = rel['relationship_type']
            if rel_type not in relationship_stats:
                relationship_stats[rel_type] = 0
            relationship_stats[rel_type] += 1
        
        result = {
            "success": True,
            "message": f"成功查询到 {len(relationships_result)} 个关系",
            "data": {
                "relationships": relationships_result,
                "statistics": {
                    "total_relationships": len(relationships_result),
                    "relationship_type_statistics": relationship_stats,
                    "queried_type": relationship_type
                }
            }
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": f"查询生信领域关系时出错: {str(e)}",
            "data": None
        }

def query_nodes_by_direct_cypher(label_name, limit=25):
    """
    直接使用Cypher查询语句查询指定标签的节点和关系
    
    参数:
        label_name: 标签名称，如 'scRNA-seq'
        limit: 限制返回的节点数量，默认25
    返回:
        dict: 包含节点和关系信息的字典
    """
    try:
        graph = connect_to_neo4j()
        
        # 查询节点
        nodes_query = f"""
        MATCH (n:`{label_name}`) 
        RETURN n 
        LIMIT {limit}
        """
        nodes_result = graph.run(nodes_query).data()
        
        # 提取节点ID列表
        node_ids = [record['n'].identity for record in nodes_result]
        
        # 查询这些节点之间的关系
        relationships_query = f"""
        MATCH (source)-[r]->(target)
        WHERE id(source) IN $node_ids OR id(target) IN $node_ids
        RETURN source.name as source_name,
               target.name as target_name,
               labels(source)[0] as source_label,
               labels(target)[0] as target_label,
               type(r) as relationship_type,
               properties(r) as relationship_properties,
               id(r) as relationship_id,
               id(source) as source_id,
               id(target) as target_id
        """
        relationships_result = graph.run(relationships_query, node_ids=node_ids).data()
        
        # 处理节点数据，提取标签名
        processed_nodes = []
        for record in nodes_result:
            node = record['n']
            node_data = {
                'node_id': node.identity,
                'label': list(node.labels)[0] if node.labels else None,  # 输出标签名
                'properties': dict(node)
            }
            processed_nodes.append(node_data)
        
        # 统计信息
        label_stats = {}
        for node in processed_nodes:
            label = node['label']
            if label not in label_stats:
                label_stats[label] = 0
            label_stats[label] += 1
        
        relationship_stats = {}
        for rel in relationships_result:
            rel_type = rel['relationship_type']
            if rel_type not in relationship_stats:
                relationship_stats[rel_type] = 0
            relationship_stats[rel_type] += 1
        
        result = {
            "success": True,
            "message": f"成功查询到 {len(processed_nodes)} 个节点和 {len(relationships_result)} 个关系",
            "data": {
                "nodes": processed_nodes,
                "relationships": relationships_result,
                "statistics": {
                    "total_nodes": len(processed_nodes),
                    "total_relationships": len(relationships_result),
                    "label_statistics": label_stats,
                    "relationship_type_statistics": relationship_stats,
                    "queried_label": label_name,
                    "limit": limit
                }
            }
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": f"查询节点时出错: {str(e)}",
            "data": None
        }

def query_nodes_and_relationships_by_label(label_name, limit=25):
    """
    查询指定标签的节点及其相关关系
    
    参数:
        label_name: 标签名称，如 'scRNA-seq'
        limit: 限制返回的节点数量，默认25
    返回:
        dict: 包含节点信息的字典，节点中包含 dependon 字段体现关系
    """
    try:
        graph = connect_to_neo4j()
        
        # 查询节点
        nodes_query = f"""
        MATCH (n:`{label_name}`) 
        RETURN n.name as name,
               labels(n)[0] as label,
               n.model_id as model_id,
               id(n) as node_id,
               properties(n) as all_properties
        LIMIT {limit}
        """
        nodes_result = graph.run(nodes_query).data()
        
        # 提取节点ID列表
        node_ids = [record['node_id'] for record in nodes_result]
        
        # 查询这些节点之间的 dependon 关系
        dependon_relationships_query = """
        MATCH (source)-[r:dependon]->(target)
        WHERE id(source) IN $node_ids AND id(target) IN $node_ids
        RETURN source.name as source_name,
               target.name as target_name,
               id(source) as source_id,
               id(target) as target_id
        """
        dependon_relationships = graph.run(dependon_relationships_query, node_ids=node_ids).data()
        
        # 构建节点名称到节点ID的映射
        node_name_to_id = {node['name']: node['node_id'] for node in nodes_result}
        
        # 为每个节点构建 dependon 字段
        for node in nodes_result:
            node_name = node['name']
            node_id = node['node_id']
            
            # 找出该节点依赖的其他节点
            dependon_nodes = []
            for rel in dependon_relationships:
                if rel['source_id'] == node_id:  # 当前节点是源节点，依赖目标节点
                    dependon_nodes.append(rel['target_name'])
            
            # 添加 dependon 字段到节点
            node['dependon'] = dependon_nodes
        
        # 统计信息
        label_stats = {}
        for node in nodes_result:
            label = node['label']
            if label not in label_stats:
                label_stats[label] = 0
            label_stats[label] += 1
        
        # 统计 dependon 关系数量
        total_dependon_relationships = len(dependon_relationships)
        
        result = {
            "success": True,
            "message": f"成功查询到 {len(nodes_result)} 个节点和 {total_dependon_relationships} 个依赖关系",
            "data": {
                "nodes": nodes_result,
                "statistics": {
                    "total_nodes": len(nodes_result),
                    "total_dependon_relationships": total_dependon_relationships,
                    "label_statistics": label_stats,
                    "queried_label": label_name,
                    "limit": limit
                }
            }
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": f"查询节点和关系时出错: {str(e)}",
            "data": None
        }

def query_app_nodes_for_nodes_list(nodes_list):
    """
    查询节点列表中每个节点对应的 app 标签节点，并将 app 属性加入到输入节点中
    
    参数:
        nodes_list: 节点列表，每个节点包含 node_id 或 name 字段
    返回:
        list: 包含 app 属性信息的节点列表
    """
    try:
        graph = connect_to_neo4j()
        
        # 提取节点ID或名称
        node_identifiers = []
        for node in nodes_list:
            if 'model_id' in node:
                node_identifiers.append(node['model_id'])
            elif 'name' in node:
                node_identifiers.append(node['name'])
            else:
                node_identifiers.append(None)
        
        # 过滤掉 None 值
        valid_identifiers = [id for id in node_identifiers if id is not None]
        
        if not valid_identifiers:
            return nodes_list
        
        # 查询每个节点对应的 app 节点（通过 contain 关系）
        app_nodes_query = """
        MATCH (source)-[r:contain]->(target:app)
        WHERE (id(source) IN $node_ids OR source.name IN $node_names)
        RETURN source.name as source_name,
               source.model_id as source_model_id,
               target.name as app_name,
               target.model_id as app_model_id,
               id(source) as source_id,
               id(target) as app_id,
               properties(target) as app_properties
        ORDER BY source.name, target.name
        """
        
        # 分离 node_id 和 name
        node_ids = [id for id in valid_identifiers if isinstance(id, int)]
        node_names = [id for id in valid_identifiers if isinstance(id, str)]
        
        app_nodes_result = graph.run(app_nodes_query, 
                                   node_ids=node_ids, 
                                   node_names=node_names).data()
        
        # 为每个输入节点添加对应的 app 属性
        result_nodes = []
        
        for i, node in enumerate(nodes_list):
            node_identifier = node_identifiers[i]
            if node_identifier is None:
                result_nodes.append(node)
                continue
            
            # 找到该节点对应的 app 节点
            matching_app_nodes = []
            for app_node in app_nodes_result:
                if (isinstance(node_identifier, int) and app_node['source_id'] == node_identifier) or \
                   (isinstance(node_identifier, str) and app_node['source_name'] == node_identifier):
                    matching_app_nodes.append(app_node)
            
            # 创建新的节点对象，包含原始属性和 app 属性
            new_node = node.copy()
            
            # 如果找到对应的 app 节点，添加 app 属性
            if matching_app_nodes:
                first_app = matching_app_nodes[0]
                
                # 复制 app_properties，但去掉 description 字段
                app_properties = first_app['app_properties'].copy()
                if 'description' in app_properties:
                    del app_properties['description']
                
                # 添加 app 相关字段到节点中
                new_node.update({
                    'app_name': first_app['app_name'],
                    'app_model_id': first_app['app_model_id'],
                    'app_id': first_app['app_id'],
                    'app_properties': app_properties,
                    'source_node_name': first_app['source_name'],
                    'source_node_model_id': first_app['source_model_id']
                })
            
            result_nodes.append(new_node)
        
        return result_nodes
        
    except Exception as e:
        print(f"查询 app 节点时出错: {str(e)}")
        return nodes_list

def query_app_nodes_by_node_ids(node_ids):
    """
    根据节点ID列表查询对应的 app 节点
    
    参数:
        node_ids: 节点ID列表
    返回:
        list: 包含每个节点对应 app 节点的列表
    """
    try:
        graph = connect_to_neo4j()
        
        if not node_ids:
            return []
        
        # 查询每个节点对应的 app 节点（通过 contain 关系）
        app_nodes_query = """
        MATCH (source)-[r:contain]->(target:app)
        WHERE id(source) IN $node_ids
        RETURN source.name as source_name,
               source.model_id as source_model_id,
               target.name as app_name,
               target.model_id as app_model_id,
               id(source) as source_id,
               id(target) as app_id,
               properties(target) as app_properties
        ORDER BY source.name, target.name
        """
        
        app_nodes_result = graph.run(app_nodes_query, node_ids=node_ids).data()
        
        # 为每个输入节点ID找到对应的 app 节点
        result_app_nodes = []
        
        for node_id in node_ids:
            # 找到该节点对应的 app 节点
            matching_app_nodes = [app for app in app_nodes_result if app['source_id'] == node_id]
            
            # 如果找到多个，只返回第一个
            if matching_app_nodes:
                first_app = matching_app_nodes[0]
                app_node_data = {
                    'app_name': first_app['app_name'],
                    'app_model_id': first_app['app_model_id'],
                    'app_id': first_app['app_id'],
                    'app_properties': first_app['app_properties'],
                    'source_node_name': first_app['source_name'],
                    'source_node_model_id': first_app['source_model_id']
                }
                result_app_nodes.append(app_node_data)
            else:
                result_app_nodes.append(None)
        
        return result_app_nodes
        
    except Exception as e:
        print(f"查询 app 节点时出错: {str(e)}")
        return []

# 使用示例
if __name__ == "__main__":
    # 查询所有生信领域场景的节点和关系
    # print("=== 查询所有生信领域场景的节点和关系 ===")
    # result1 = query_omics_scenario_nodes_and_relationships()
    # print(json.dumps(result1, indent=2, ensure_ascii=False))
    
    # 查询特定标签的节点
    # print("\n=== 查询 scRNA-seq 标签的节点 ===")
    # result2 = query_omics_nodes_by_label("scRNA-seq")
    # print(json.dumps(result2, indent=2, ensure_ascii=False))
    
    # # 查询特定类型的关系
    # print("\n=== 查询 BELONGS_TO 类型的关系 ===")
    # result3 = query_omics_relationships_by_type("BELONGS_TO")
    # print(json.dumps(result3, indent=2, ensure_ascii=False))
    
    # 使用直接Cypher查询语句查询节点和关系
    # print("\n=== 使用直接Cypher查询 scRNA-seq 节点和关系 ===")
    # result4 = query_nodes_by_direct_cypher("scRNA-seq", limit=25)
    # print(json.dumps(result4, indent=2, ensure_ascii=False))
    
    # 查询指定标签的节点及其关系
    print("\n=== 查询 scRNA-seq 节点及其关系 ===")
    result5 = query_nodes_and_relationships_by_label("scRNA-seq", limit=25)
    # print(json.dumps(result5, indent=2, ensure_ascii=False))
    
    # 查询节点对应的 app 节点并添加到输入节点中
    if result5["success"]:
        nodes_list = [
          {
            "model_id": 10,
            "name": "构建参考基因组索引",
            "text_input": "物种所对应的gtf和fasta文件",
            "dependon": []
          },
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
        print("\n=== 查询节点对应的 app 节点并添加到输入节点中 ===")
        # enhanced_nodes = query_app_nodes_for_nodes_list(nodes_list)
        # print(json.dumps(enhanced_nodes, indent=2, ensure_ascii=False))
        
        # # 使用节点ID查询 app 节点
        # print("\n=== 使用节点ID查询 app 节点 ===")
        node_ids = [node['model_id'] for node in nodes_list]
        app_nodes_by_ids = query_app_nodes_by_node_ids(node_ids)
        print(json.dumps(app_nodes_by_ids, indent=2, ensure_ascii=False))
