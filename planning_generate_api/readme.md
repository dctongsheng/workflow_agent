# Workflow Planning API

这是一个基于FastAPI构建的工作流规划生成API，使用LLM（大语言模型）来生成工作流计划。

## 安装

1. 克隆仓库
```bash
git clone [repository_url]
cd planning_generate_api
```

2. 安装依赖
```bash
pip install fastapi uvicorn pydantic python-dotenv
```

3. 配置环境变量
创建 `.env` 文件并设置必要的环境变量：
```env
API_KEY=your_api_key
```

## 启动服务

```bash
python app.py
```

服务将在 `http://localhost:8000` 启动。

## API 文档

### 生成工作流计划

**端点**: `/planning_generate`

**方法**: POST

**请求体**:
```json
{
    "query": "string",
    "data_meatinfo": "string"
}
```

**参数说明**:
- `query`: 用户查询字符串，描述所需的工作流计划
- `data_meatinfo`: 数据文件信息

**响应格式**:
```json
{
    "code": 200,
    "message": "Success",
    "structured_output": {
        // 生成的工作流计划
    }
}
```

**状态码**:
- 200: 成功
- 401: API密钥无效
- 429: 超出速率限制
- 500: 服务器内部错误

## 使用示例

### 使用 curl
```bash
curl -X POST "http://localhost:8000/planning_generate" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "帮我使用时空组学的数据，进行标准分析和下游高级分析",
           "data_meatinfo": "mouse.fq.gz"
         }'
```

### 使用 Python
```python
import requests
import json

url = "http://localhost:8000/planning_generate"
payload = {
    "query": "帮我使用时空组学的数据，进行标准分析和下游高级分析",
    "data_meatinfo": "mouse.fq.gz"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## API 文档访问

启动服务后，可以通过以下URL访问交互式API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 注意事项

1. 确保API密钥配置正确
2. 注意请求速率限制
3. 建议在生产环境中使用HTTPS
4. 建议配置适当的日志记录和监控

## 入参
1、数据的meta信息
        {
          "checkCode": "915381468",
          "commonTag": "un_is_send_cnsa",
          "barcodeLen": "",
          "subnet": "hpc",
          "refrenece": "",
          "memo": "",
          "tissue": "",
          "pid": "",
          "path": "/zfsms3/ST_STOMICS/STOmics_cloud/odms/test/dcs_cloud/P1871461072416366593/Files/ResultData/Workflow/W202505120000001/test/output/raw_matrix/features.tsv.gz",
          "sampleRandomNo": "",
          "zone": "st",
          "id": "bd04bf1ce6d5414abf306f593fd37481",
          "tag": "",
          "umiLocation": "",
          "batchNo": "WF2025051210000",
          "mapping": "test/output/raw_matrix/features.tsv.gz",
          "sampleId": "test",
          "wfName": "",
          "wfTag": "scRNA-seq_v3",
          "bussinessName": "时空workflow",
          "sampleNum": "test",
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
          "srcFilePath": "/zdsms1/ST_NOTEBOOK/P20Z10200N0039/workflow/test/cromwell-executions-volcano/scRNA/7a6c17fa-0700-446b-8bdf-19e4b76e18cf/call-dnbc4toolsPipeline/execution/test/output/raw_matrix/features.tsv.gz",
          "umiStartPos": "",
          "omicsType": "",
          "omics": "genomics",
          "fileSize": "141108",
          "name": "features.tsv.gz",
          "fastqType": "",
          "projectId": "P1871461072416366593",
          "status": "0",
          "metadataType": 0,
          "barcodeStart": "",
          "delFlag": "0",
          "sid": "1921812867273261057",
          "umiLen": "",
          "fileStatus": "0",
          "processId": "scRNA-seq_v3",
          "fileExtension": "tsv.gz",
          "bussinessCode": "202406170032",
          "chipId": "",
          "lane": "",
          "chipCategory": "",
          "creator": "c-liguansheng",
          "dyeType": "",
          "env": "alitest",
          "parentId": "b747657fbd45463eaec1c5a5f22a6db4",
          "createTime": "2025-05-12 15:58:09",
          "species": "",
          "readLen": "",
          "taskId": "W202505120000001",
          "downloadType": "0",
          "metadataId": "e75f84c967ea463caa9676b72cb350f3",
          "metadataMenuId": "b747657fbd45463eaec1c5a5f22a6db4",
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
          "processVersion": "3.2.2",
          "splitCount": "",
          "cbLength": "",
          "cbStart": "",
          "libraryType": "",
          "subProject": "",
          "snId": "",
          "menuId": "b747657fbd45463eaec1c5a5f22a6db4",
          "menuStatus": "0",
          "menuSort": "1",
          "dataType": "0",
          "searchName": "features.tsv.gz",
          "menuPath": "/Files/ResultData/Workflow/W202505120000001/test/output/raw_matrix",
          "trackCrossQcPassFlag": "",
          "stitchedImage": "",
          "menuName": "raw_matrix",
          "linkType": "2"
        }
2、用户的query
e:帮我进行聚类分析

## 返回参数
{
  "structured_output": {
    "planning_steps": [
      {
        "step": 1,
        "title": "标准流程分析",
        "name": "SAW-ST-V8",
        "oid": "WF09202503053KQYyK",
        "description": "处理Stereo-seq测序数据，将测序读数映射到组织切片的空间位置，量化空间特征表达并可视化呈现空间表达分布。",
        "input": {
          "type": "fq.gz",
          "description": "原始测序数据文件"
        },
        "output": {
          "type": ".gef",
          "description": "空间特征表达文件"
        }
      },
      {
        "step": 2,
        "title": "",
        "name": "Stereo_Miner_Preprocessing",
        "oid": "WF09202501232b7Orb",
        "description": "对空间转录组原始数据进行预处理，包括数据过滤、标准化处理、矩阵标准化以及识别高变基因。",
        "input": {
          "type": ".gef",
          "description": "空间特征表达文件"
        },
        "output": {
          "type": "h5ad",
          "description": "预处理后的数据文件"
        }
      },
      {
        "step": 3,
        "title": "",
        "name": "Stereo_Miner_Clustering",
        "oid": "WF0920250123qb6R7b",
        "description": "通过UMAP降维和Leiden/Louvain聚类算法对标准化表达矩阵进行分析，识别空间转录组数据中的细胞亚群并生成各簇的标记基因表。",
        "input": {
          "type": ".h5ad",
          "description": "预处理后的数据文件"
        },
        "output": {
          "type": ".h5ad",
          "description": "聚类分析结果文件"
        }
      },
      {
        "step": 4,
        "title": "",
        "name": "Stereo_Miner_Enrichment",
        "oid": "WF09202501233nPWAk",
        "description": "基于stereopy生成的marker_gene.csv表格，使用clusterProfiler对差异基因进行GO和KEGG功能富集分析，并生成可视化图表和结果列表。",
        "input": {
          "type": ".csv",
          "description": "标记基因表"
        },
        "output": {
          "type": ".pdf,.png,.xls",
          "description": "富集分析结果和火山图"
        }
      }
    ]
  }
}



## dify返回的参数

请求方法：
curl -X POST 'http://172.28.140.214/v1/workflows/run' \
--header 'Authorization: Bearer app-rRmTHZB3dR36dO226ocq2iwq' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {"query": "hi"},
    "response_mode": "blocking",
    "user": "abc-123"
}'

返回：
{"task_id": "24497ce4-6973-4082-9b7f-b95323fe8f41", "workflow_run_id": "14cc923a-0ef4-4040-a953-d7f475f1e199", 
"data": {"id": "14cc923a-0ef4-4040-a953-d7f475f1e199", 
          "workflow_id": "196c3f0b-03cb-4b52-bbb3-5cd33523426c", "status": "succeeded", 
          "outputs": {"structured_output": {"planning_steps": [{"step": 1, "name": "Stereo_Miner_Clustering", "oid": "WF0920250123qb6R7b", "description": "\u5bf9\u6807\u51c6\u5316\u8868\u8fbe\u77e9\u9635\u8fdb\u884cUMAP\u964d\u7ef4\u548cLeiden/Louvain\u805a\u7c7b\u5206\u6790\uff0c\u8bc6\u522b\u7ec6\u80de\u4e9a\u7fa4\u5e76\u751f\u6210\u6807\u8bb0\u57fa\u56e0\u8868\u3002", "input": {"type": "h5ad", "description": "\u8f93\u5165\u6587\u4ef6\u4e3a111.h5ad\uff0c\u5305\u542b\u6807\u51c6\u5316\u540e\u7684\u7a7a\u95f4\u8f6c\u5f55\u7ec4\u6570\u636e\u3002"}, "output": {"type": "h5ad", "description": "\u8f93\u51fa\u6587\u4ef6\u4e3a\u5305\u542b\u805a\u7c7b\u7ed3\u679c\u7684h5ad\u6587\u4ef6\u3002"}}]}}, 
"error": null, "elapsed_time": 9.410107392817736, "total_tokens": 1613, "total_steps": 3, "created_at": 1749793375, "finished_at": 1749793384}}