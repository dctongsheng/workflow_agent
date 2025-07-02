import aiohttp
import asyncio
import json
from typing import Dict, Any
# from example import auto_fill_parameters_data_rna_3

async def chat_with_api(inputs: Dict[str, Any], query: str) -> Dict[str, Any]:
    """
    异步调用聊天API的函数
    
    Args:
        inputs (Dict[str, Any]): 输入参数字典
        query (str): 查询内容
    
    Returns:
        Dict[str, Any]: API响应结果
    
    Raises:
        aiohttp.ClientError: 当请求失败时抛出异常
    """
    
    # API配置
    url = 'http://120.76.217.102/v1/chat-messages'
    headers = {
        'Authorization': 'Bearer app-5AwtFzA6MAynGUDmBpTsIUJ1',
        'Content-Type': 'application/json'
    }
    
    # 构建请求数据
    data = {
        "inputs": inputs,
        "query": query,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "abc-123"
    }
    
    try:
        # 创建异步HTTP会话
        async with aiohttp.ClientSession() as session:
            # 发送异步POST请求
            async with session.post(url, headers=headers, json=data) as response:
                # 检查响应状态
                response.raise_for_status()
                
                # 返回JSON响应
                return await response.json()
                
    except aiohttp.ClientError as e:
        print(f"请求失败: {e}")
        raise

# 使用示例
async def main():
    auto_fill_parameters_data_rna_3={
  "records": [
  {
    "viewType": "",
    "subnet": "",
    "id": "26412c7d89bf48bcb0916f885ae0ed8c",
    "projectId": "P1600787473158537217",
    "status": "0",
    "delFlag": "0",
    "processId": "Stereo_Miner_Clustering",
    "fileExtension": "",
    "env": "",
    "parentId": "1780858330605449217",
    "createTime": "2025-05-29 16:39:49",
    "menuLabel": "",
    "downloadType": "",
    "menuId": "26412c7d89bf48bcb0916f885ae0ed8c",
    "menuStatus": "0",
    "menuSort": "1",
    "dataType": "1",
    "searchName": "2",
    "systemType": "0",
    "menuPath": "/Files/RawData",
    "menuName": "2"
},
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
    "srcFilePath": "/zdsms1/ST_NOTEBOOK/P20Z10200N0039/workflow/test/cromwell-executions-volcano/Hello/12a1d31f-34b8-47e8-b115-699bd246e0d3/call-sayHello/execution/1111.h5ad",
    "umiStartPos": "",
    "omicsType": "STOmics",
    "omics": "STOmics",
    "fileSize": "247",
    "name": "1111.h5ad",
    "fastqType": "",
    "projectId": "P1871461072416366593",
    "status": "0",
    "metadataType": 0,
    "barcodeStart": "",
    "delFlag": "0",
    "sid": "1933091680321863682",
    "umiLen": "",
    "fileStatus": "0",
    "processId": "Stereo_Miner_Clustering",
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
    "wfTag": "Stereo_Miner_Clustering",
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
    "wfTag": "Stereo_Miner_Clustering",
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
  }

    """主函数，用于测试异步API调用"""
    try:
        # 调用异步API
        result = await chat_with_api(
            inputs={"data_choose": json.dumps(auto_fill_parameters_data_rna_3)}, 
            query="帮我进行富集分析"
        )
        print("响应结果:", json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"调用失败: {e}")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
