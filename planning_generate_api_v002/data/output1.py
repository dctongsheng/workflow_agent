{'analysis_plans': [{'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '构建样本所对应的用于比对，注释的参考基因组索引文件夹', 'model_id': 10, 'name': '构建参考基因组索引', 'type': 'scRNA-seq', 'text_input': '物种所对应的gtf和fasta文件', 'dependon': []}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '以下机cDNA和oligo数据经过过滤，比对、注释，矩阵生成，细胞分群生成标准质控分析报告', 'model_id': 11, 'name': 'scRNA-seq标准分析流程', 'type': 'scRNA-seq', 'text_input': '下机数据cDNA和Oligo的fq.gz文件需对应，参考基因组索引文件夹', 'dependon': ['构建参考基因组索引']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '以多个样本下机的矩阵文件运行多样本整合后生成从数据质控、细胞聚类、注释、拟时序、互作、富集分析到最终产生交付报告全套分析流程', 'model_id': 12, 'name': '多样本整合分析', 'type': 'scRNA-seq', 'text_input': '以多个样本标准分析流程的输出文件中的FilterMatrix文件夹作为单样本输入，每个文件夹包含（barcodes.tsv.,gz，matrix.mtx.gz,fetures.tsv.gz）', 'dependon': ['scRNA-seq标准分析流程']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '统计并过滤组织区域内的低质量细胞数、MID数及线粒体数', 'model_id': 13, 'name': '数据质控分析', 'type': 'scRNA-seq', 'text_input': '以标准分析流程的输出文件中的FilterMatrix文件夹作为单样本输入，每个文件夹包含（barcodes.tsv.,gz，matrix.mtx.gz,fetures.tsv.gz）', 'dependon': ['多样本整合分析']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '个性化选择筛选条件过滤细胞、基因数，数据标准化并筛选高变基因用于后续分析', 'model_id': 14, 'name': '数据预处理', 'type': 'scRNA-seq', 'text_input': '输入质控后获得的h5ad文件', 'dependon': ['数据质控分析']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '依据数据预处理后的结果进行PCA主成分分析，Umap降维聚类分析，同时进行marker基因筛选', 'model_id': 15, 'name': '细胞聚类分析', 'type': 'scRNA-seq', 'text_input': '输入预处理后获得的h5ad矩阵文件', 'dependon': ['数据预处理']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '聚类后的结果通过SingleR等自动细胞注释软件与自带的reference数据库比对，给cluster定义细胞类型名', 'model_id': 16, 'name': '细胞注释', 'type': 'scRNA-seq', 'text_input': '输入细胞聚类后的h5ad矩阵文件', 'dependon': ['细胞聚类分析']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '使用聚类或者细胞注释后的h5ad矩阵文件推荐细胞类群或者类型之间随时间的发育轨迹及基因的表达的拟时序变化', 'model_id': 17, 'name': '拟时序分析', 'type': 'scRNA-seq', 'text_input': '输入细胞聚类后或者细胞注释后的h5ad矩阵文件', 'dependon': ['细胞聚类分析', '细胞注释']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '使用聚类或者细胞注释后的h5ad矩阵文件推荐细胞类群或者类型之间细胞互作通路', 'model_id': 18, 'name': '细胞互作分析', 'type': 'scRNA-seq', 'text_input': '输入细胞聚类后或者细胞注释后的h5ad矩阵文件', 'dependon': ['细胞聚类分析', '细胞注释']}, {'type_chinese': '单细胞转录组学全套分析（scRNA-seq）', 'description': '使用聚类或者细胞注释后的h5ad矩阵文件运行GO和KEGG富集分析，推断每种细胞类群或者类型的富集通路', 'model_id': 19, 'name': '富集分析', 'type': 'scRNA-seq', 'text_input': '输入细胞聚类后或者细胞注释后的h5ad矩阵文件', 'dependon': ['细胞聚类分析', '细胞注释']}]}


dify_output={
        "analysis_plans": [
          {
            "model_id": 1,
            "name": "构建参考基因组索引",
            "text_input": "物种所对应的gtf和fasta文件",
            "dependon": []
          },
          {
            "model_id": 2,
            "name": "SAW标准分析",
            "text_input": "下机测序数据fq.gz，芯片mask文件h5,实验拍照图像文件tar.gz或Tiff，参考基因组索引文件夹",
            "dependon": [
              "构建参考基因组索引"
            ]
          },
          {
            "model_id": 3,
            "name": "数据质控分析",
            "text_input": "输入SAW标准分析流程产出的tissue.gef和cellbin.gef组织区域表达矩阵文件",
            "dependon": [
              "SAW标准分析"
            ]
          },
          {
            "model_id": 4,
            "name": "数据预处理",
            "text_input": "输入质控后获得的h5ad文件",
            "dependon": [
              "数据质控分析"
            ]
          },
          {
            "model_id": 5,
            "name": "细胞聚类分析",
            "text_input": "输入预处理后获得的h5ad矩阵文件",
            "dependon": [
              "数据预处理"
            ]
          },
          {
            "model_id": 6,
            "name": "细胞注释",
            "text_input": "输入细胞聚类后的h5ad矩阵文件",
            "dependon": [
              "细胞聚类分析"
            ]
          },
          {
            "model_id": 7,
            "name": "拟时序分析",
            "text_input": "输入细胞聚类后或者细胞注释后的h5ad矩阵文件",
            "dependon": [
              "细胞聚类分析",
              "细胞注释"
            ]
          },
          {
            "model_id": 8,
            "name": "细胞互作分析",
            "text_input": "输入细胞聚类后或者细胞注释后的h5ad矩阵文件",
            "dependon": [
              "细胞聚类分析",
              "细胞注释"
            ]
          },
          {
            "model_id": 9,
            "name": "富集分析",
            "text_input": "输入细胞聚类后或者细胞注释后的h5ad矩阵文件",
            "dependon": [
              "细胞聚类分析",
              "细胞注释"
            ]
          }
        ]
}

final_output={
        "planning_steps": [
            {
                "title": "构建参考基因组索引",
                "step": 0,
                "previous_step": [],
                "name": "SAW-ST-V8-makeRef",
                "oid": "682ee06dc37f9411d54035c0",
                "description": "该WDL的核心功能是为SAW count准备参考基因组，需要输入GTF/GFF和FASTA文件或特定的rRNA FASTA文件。",
                "input": "{\"input_file_suffix\": \".gz\"}",
                "output": "{\"fllename_suffix\": \"count\"}"
            },
            {
                "title": "SAW标准分析",
                "step": 1,
                "previous_step": [
                    "构建参考基因组索引"
                ],
                "name": "SAW-ST-V8",
                "oid": "68243cd0e27ff3f8ca8e526d",
                "description": "该WDL的核心功能是处理Stereo-seq测序数据，通过空间定位、基因表达量化和可视化分析，生成空间特征表达矩阵，支持多种样本类型和下游分析流程。",
                "input": "{\n  \"input_file_suffix\": \".gz\"\n}",
                "output": "{\"fllename_suffix\": \".gef\"}"
            },
            {
                "title": "数据质控分析",
                "step": 2,
                "previous_step": [
                    "SAW标准分析"
                ],
                "name": "Stereo_Miner_data_qc",
                "oid": "6840fa0845902327e1a41215",
                "description": "该WDL的核心功能是对单细胞转录组数据进行质量控制分析，包括统计每个细胞的总分子标识符(MID)计数、基因类型数量以及线粒体基因百分比，并生成可视化图表和质量控制信息文件。",
                "input": "{\"input_file_suffix\": \".gef\"}",
                "output": "{\n  \"fllename_suffix\": \".txt\"\n}"
            },
            {
                "title": "数据预处理",
                "step": 3,
                "previous_step": [
                    "数据质控分析"
                ],
                "name": "Stereo_Miner_Preprocessing",
                "oid": "6840fa0745902327e1a41202",
                "description": "该WDL的核心功能是对空间转录组原始数据进行预处理，包括数据过滤、标准化和识别高变基因，以生成可靠的下游分析数据集。",
                "input": "{\"input_file_suffix\": \".gef\"}",
                "output": "{\n  \"fllename_suffix\": \"h5ad\"\n}"
            },
            {
                "title": "细胞聚类分析",
                "step": 4,
                "previous_step": [
                    "数据预处理"
                ],
                "name": "Stereo_Miner_Clustering",
                "oid": "6840fa0845902327e1a4121c",
                "description": "该WDL的核心功能是通过UMAP降维和leiden/louvain聚类算法对标准化表达矩阵进行分析，识别细胞亚群并生成标记基因表。",
                "input": "{\"input_file_suffix\": \".h5ad\"}",
                "output": "{\n  \"fllename_suffix\": \".h5ad\"\n}"
            },
            {
                "title": "细胞注释",
                "step": 5,
                "previous_step": [
                    "细胞聚类分析"
                ],
                "name": "Stereo_Miner_Autoannotation",
                "oid": "6840fa0845902327e1a41229",
                "description": "该WDL工作流的核心功能是使用SingleR工具基于参考数据集对单细胞进行自动细胞类型注释，包括内存估算、参考数据获取和细胞类型标注等步骤。",
                "input": "{\"input_file_suffix\": \".h5ad\"}",
                "output": "{\n  \"fllename_suffix\": \"h5ad\"\n}"
            },
            {
                "title": "拟时序分析",
                "step": 6,
                "previous_step": [
                    "细胞聚类分析",
                    "细胞注释"
                ],
                "name": "Stereo_Miner_Pseudotime",
                "oid": "6840fa0745902327e1a411fd",
                "description": "该WDL的核心功能是通过Monocle3工具对单细胞空间转录组数据进行伪时间分析，推断细胞发育轨迹并计算各细胞在轨迹上的相对位置（伪时间值），同时识别沿轨迹动态表达的标记基因。",
                "input": "{\n  \"input_file_suffix\": \".h5ad\"\n}",
                "output": "{\n  \"fllename_suffix\": \"rds\"\n}"
            },
            {
                "title": "细胞互作分析",
                "step": 7,
                "previous_step": [
                    "细胞聚类分析",
                    "细胞注释"
                ],
                "name": "Stereo_Miner_Interaction",
                "oid": "6840fa0745902327e1a41209",
                "description": "该WDL工作流的核心功能是使用CellChat和Cellphonedb两种工具分析单细胞空间转录组数据中不同细胞簇之间的相互作用关系，并生成可视化结果和统计表格。",
                "input": "{\"input_file_suffix\": \".h5ad\"}",
                "output": "{\"fllename_suffix\": \"csv\"}"
            },
            {
                "title": "富集分析",
                "step": 8,
                "previous_step": [
                    "细胞聚类分析",
                    "细胞注释"
                ],
                "name": "Stereo_Miner_Enrichment",
                "oid": "6840fa0745902327e1a4120f",
                "description": "该WDL的核心功能是：基于stereopy生成的marker_gene.csv表格，使用clusterProfiler对每个细胞类型的差异表达基因进行GO和KEGG功能富集分析，并生成可视化图表和结果列表。",
                "input": "{\"input_file_suffix\": \".csv\"}",
                "output": "{\"fllename_suffix\": \"pdf,png,xls\"}"
            }
        ]
    }


#自动填写参数输入：
{
  "data_meatinfo":{
  "records": [
  {
    "checkCode": "429167780",
    "commonTag": "un_is_send_cnsa",
    "barcodeLen": "",
    "subnet": "hpc",
    "refrenece": "",
    "memo": "",
    "tissue": "",
    "pid": "",
    "path": "/zfsms3/ST_STOMICS/STOmics_cloud/odms/test/dcs_cloud/P1871461072416366593/Files/ResultData/Workflow/W202506120003255/stdout",
    "sampleRandomNo": "",
    "zone": "st",
    "id": "899cd30a29024e75a8e79b9f05ac6ad5",
    "tag": "",
    "umiLocation": "",
    "batchNo": "WF2025061210187",
    "mapping": "stdout",
    "sampleId": "123",
    "wfName": "",
    "bussinessName": "时空workflow",
    "sampleNum": "",
    "sampleName": "",
    "sampleType": "",
    "sampleIntegrity": "",
    "resultNote": "",
    "sequenceType": "",
    "libraryNum": "",
    "slide": "",
    "barcode": "",
    "sequencePlatform": "",
    "basicQualityValue": "",
    "q30": "",
    "q20": "",
    "readNum": "",
    "baseNum": "",
    "estErr": "",
    "srcFilePath": "/zdsms1/ST_NOTEBOOK/P20Z10200N0039/workflow/test/cromwell-executions-volcano/Hello/12a1d31f-34b8-47e8-b115-699bd246e0d3/call-sayHello/execution/1111.fq.gz",
    "umiStartPos": "",
    "omicsType": "",
    "omics": "genomics",
    "fileSize": "247",
    "name": "1111.fq.gz",
    "fastqType": "",
    "projectId": "P1871461072416366593",
    "status": "0",
    "metadataType": 0,
    "barcodeStart": "",
    "delFlag": "0",
    "sid": "1933091680321863682",
    "umiLen": "",
    "fileStatus": "0",
    "processId": "Hello_multiple",
    "fileExtension": "stdout",
    "bussinessCode": "202406170032",
    "chipId": "",
    "lane": "",
    "chipCategory": "",
    "creator": "hujiaming",
    "dyeType": "",
    "env": "",
    "parentId": "ce0c33632fa84a6fb1c265e8fe31a189",
    "createTime": "2025-06-12 17:23:58",
    "species": "",
    "readLen": "",
    "taskId": "W202506120003255",
    "downloadType": "0",
    "metadataId": "47f02fbafece421a92d8bc2bce27c85c",
    "metadataMenuId": "ce0c33632fa84a6fb1c265e8fe31a189",
    "projectName": "",
    "businessType": "",
    "projectType": "",
    "productType": "",
    "chipSpecs": "",
    "experimentProcess": "",
    "isMicroscopeFile": "",
    "qcResultFile": "",
    "imageToolType": "",
    "manufacture": "",
    "imageQcVersion": "",
    "stereoResepSwitch": "",
    "iprVersion": "",
    "processVersion": "1.0.0",
    "splitCount": "",
    "cbLength": "",
    "cbStart": "",
    "libraryType": "",
    "subProject": "",
    "snId": "",
    "menuId": "ce0c33632fa84a6fb1c265e8fe31a189",
    "menuStatus": "0",
    "menuSort": "1",
    "dataType": "0",
    "searchName": "stdout",
    "menuPath": "/Files/ResultData/Workflow/W202506120003255",
    "trackCrossQcPassFlag": "",
    "stitchedImage": "",
    "menuName": "W202506120003255",
    "linkType": "2"
  },
  {
    "checkCode": "3685340396",
    "commonTag": "un_is_send_cnsa",
    "barcodeLen": "",
    "subnet": "hpc",
    "refrenece": "",
    "memo": "",
    "tissue": "",
    "pid": "",
    "path": "/zfsms3/ST_STOMICS/STOmics_cloud/odms/test/dcs_cloud/P1871461072416366593/Files/ResultData/Workflow/W202506120003255/input.json",
    "sampleRandomNo": "",
    "zone": "st",
    "id": "11550f6b07ef4fcf83ee5cea4f091c02",
    "tag": "",
    "umiLocation": "",
    "batchNo": "WF2025061210187",
    "mapping": "input.json",
    "sampleId": "123",
    "wfName": "",
    "wfTag": "workflow",
    "bussinessName": "时空workflow",
    "sampleNum": "",
    "sampleName": "",
    "sampleType": "",
    "sampleIntegrity": "",
    "resultNote": "",
    "sequenceType": "",
    "libraryNum": "",
    "slide": "",
    "barcode": "",
    "sequencePlatform": "",
    "basicQualityValue": "",
    "q30": "",
    "q20": "",
    "readNum": "",
    "baseNum": "",
    "estErr": "",
    "srcFilePath": "/zdsms1/ST_NOTEBOOK/P20Z10200N0039/workflow/test/param/users/st_stomics/P20Z10200N0039/WF2025061210187/1933091680321863682/input.json",
    "umiStartPos": "",
    "omicsType": "",
    "omics": "genomics",
    "fileSize": "136",
    "name": "input.json",
    "fastqType": "",
    "projectId": "P1871461072416366593",
    "status": "0",
    "metadataType": 0,
    "barcodeStart": "",
    "delFlag": "0",
    "sid": "1933091680321863682",
    "umiLen": "",
    "fileStatus": "0",
    "processId": "Hello_multiple",
    "fileExtension": "json",
    "bussinessCode": "202406170032",
    "chipId": "",
    "lane": "",
    "chipCategory": "",
    "creator": "hujiaming",
    "dyeType": "",
    "env": "",
    "parentId": "ce0c33632fa84a6fb1c265e8fe31a189",
    "createTime": "2025-06-12 17:23:58",
    "species": "",
    "readLen": "",
    "taskId": "W202506120003255",
    "downloadType": "0",
    "metadataId": "f9c270ac5a204094934cf7edaaeb9e2a",
    "metadataMenuId": "ce0c33632fa84a6fb1c265e8fe31a189",
    "projectName": "",
    "businessType": "",
    "projectType": "",
    "productType": "",
    "chipSpecs": "",
    "experimentProcess": "",
    "isMicroscopeFile": "",
    "qcResultFile": "",
    "imageToolType": "",
    "manufacture": "",
    "imageQcVersion": "",
    "stereoResepSwitch": "",
    "iprVersion": "",
    "processVersion": "1.0.0",
    "splitCount": "",
    "cbLength": "",
    "cbStart": "",
    "libraryType": "",
    "subProject": "",
    "snId": "",
    "menuId": "ce0c33632fa84a6fb1c265e8fe31a189",
    "menuStatus": "0",
    "menuSort": "1",
    "dataType": "0",
    "searchName": "input.json",
    "menuPath": "/Files/ResultData/Workflow/W202506120003255",
    "trackCrossQcPassFlag": "",
    "stitchedImage": "",
    "menuName": "W202506120003255",
    "linkType": "2"
  }
]
},
  "query_template": {
    "SN": "",
    "RegistJson": "",
    "DataDir": "",
    "ImageTar": "",
    "ImagePreDir": "",
    "Tissue": "",
    "Reference": ""
  },
  "user": "test_user_001",
  "conversation_id": "",
  "response_mode": "blocking"
}
# 自动填写参数输出：
{
  "code": 200,
  "message": "Success",
  "filled_parameters": {
    "SN": "",
    "RegistJson": "",
    "DataDir": "/Files/ResultData/Workflow/W202506120003255",
    "ImageTar": "",
    "ImagePreDir": "",
    "Tissue": "",
    "Reference": ""
  }
}