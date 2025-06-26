#传入一个list；输出一个模块。
import json

workflow_dict = {
    "SAW-ST-V8-makeRef": "构建参考基因组索引",
    "SAW-ST-V8": "SAW标准分析",
    "SAW-ST-V7": "SAW标准分析",
    "Stereo_Miner_data_qc": "数据质控分析",
    "Stereo_Miner_Preprocessing": "数据预处理",
    "Stereo_Miner_Clustering": "细胞聚类分析",
    "Stereo_Miner_Autoannotation": "细胞注释",
    "Stereo_Miner_Pseudotime": "拟时序分析",
    "Stereo_Miner_Interaction": "细胞互作分析",
    "Stereo_Miner_Enrichment": "富集分析",
    "scRNA-seq-build-index": "构建参考基因组索引",
    "scRNA-seq_v3": "scRNA-seq标准分析流程",
    "scRNA-seq_v3.1.5": "scRNA-seq标准分析流程",
    "Single-cell-multi-sample-anlysis": "多样本整合分析",
    "SC_Miner_data_qc": "数据质控分析",
    "SC_Miner_Preprocessing": "数据预处理",
    "SC_Miner_Clustering": "细胞聚类分析",
    "SC_Miner_Autoannotation": "细胞注释",
    "SC_Miner_Pseudotime": "拟时序分析",
    "SC_Miner_Interaction": "细胞互作分析",
    "SC_Miner_Enrichment": "富集分析",
    "scATAC-seq-build-index": "构建参考基因组索引",
    "scATAC-seq_v3": "scATAC标准分析流程",
    "scVDJ-build-IMGT-ref": "构建参考基因组索引",
    "scVDJ-seq": "scVDJ标准分析流程",
    "BulkRNA-seq-build-index": "构建参考基因组索引",
    "BulkRNA-seq": "BulkRNA-seq标准分析流程"
}


def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_first_app(list_data):
    res_list=[]
    res_dict={}
    for i in list_data:
        if "wfTag" in i:
            # wfTag存在
            if i["wfTag"] is not None and i["wfTag"] != "":
                # wfTag不为空，返回包含三个空字符串的列表
                
                if i["wfTag"] not in res_list:
                    res_list.append(i["wfTag"])
    res_dict["wftag"]=res_list
    return res_dict
def get_first_node(res_dict):
    if len(res_dict["wftag"])>=1:
        for i in res_dict["wftag"]:
            if i in workflow_dict:
                return workflow_dict[i]
    else:
        return None

if __name__ == "__main__":
    file_path = "/Users/bws/cursor_project_202506/git25/workflow_planning_06/data_scripts/data/文件meta.json"
    data = read_json(file_path)
    first_appp = get_first_app(data["data"]["records"])
    print(first_appp)
    first_node = get_first_node(first_appp)
    print(first_node)







