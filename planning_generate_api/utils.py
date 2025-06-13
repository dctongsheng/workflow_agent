import json
from typing import Dict, Optional, List
import asyncio

async def process_data_meatinfo(data_meatinfo: str) -> str:
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
            # print(record)
            if not isinstance(record, dict):
                continue
                
            processed_record = {}
            
            # 提取必要字段
            if "name" in record:
                processed_record["name"] = record["name"]
                
            if "omics" in record:
                processed_record["omics"] = record["omics"]
                
            if "wfTag" in record:
                processed_record["wfTag"] = record["wfTag"]
                # 判断是否为原始数据
                processed_record["is_raw_data"] = True
            else:
                processed_record["is_raw_data"] = False
            # 只添加包含必要字段的记录
            # if all(key in processed_record for key in ["name", "omics", "wfTag"]):
            processed_records.append(processed_record)
                
        if not processed_records:
            return json.dumps({
                "success": False,
                "message": "No valid records found",
                "data": None
            })
            
        return json.dumps({
            "success": True,
            "message": "Success",
            "data": processed_records
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

async def main():
    """
    示例函数，展示process_data_meatinfo的使用方法
    """
    # 示例1：有效的数据
    valid_data ={"records": [{"checkCode": "429167780", "commonTag": "un_is_send_cnsa", "barcodeLen": "", "subnet": "hpc", "refrenece": "", "memo": "", "tissue": "", "pid": "", "path": "/zfsms3/ST_STOMICS/STOmics_cloud/odms/test/dcs_cloud/P1871461072416366593/Files/ResultData/Workflow/W202506120003255/stdout", "sampleRandomNo": "", "zone": "st", "id": "899cd30a29024e75a8e79b9f05ac6ad5", "tag": "", "umiLocation": "", "batchNo": "WF2025061210187", "mapping": "stdout", "sampleId": "123", "wfName": "", "bussinessName": "\u65f6\u7a7aworkflow", "sampleNum": "", "sampleName": "", "sampleType": "", "sampleIntegrity": "", "resultNote": "", "sequenceType": "", "libraryNum": "", "slide": "", "barcode": "", "sequencePlatform": "", "basicQualityValue": "", "q30": "", "q20": "", "readNum": "", "baseNum": "", "estErr": "", "srcFilePath": "/zdsms1/ST_NOTEBOOK/P20Z10200N0039/workflow/test/cromwell-executions-volcano/Hello/12a1d31f-34b8-47e8-b115-699bd246e0d3/call-sayHello/execution/1111.fq.gz", "umiStartPos": "", "omicsType": "", "omics": "genomics", "fileSize": "247", "name": "1111.fq.gz", "fastqType": "", "projectId": "P1871461072416366593", "status": "0", "metadataType": 0, "barcodeStart": "", "delFlag": "0", "sid": "1933091680321863682", "umiLen": "", "fileStatus": "0", "processId": "Hello_multiple", "fileExtension": "stdout", "bussinessCode": "202406170032", "chipId": "", "lane": "", "chipCategory": "", "creator": "hujiaming", "dyeType": "", "env": "", "parentId": "ce0c33632fa84a6fb1c265e8fe31a189", "createTime": "2025-06-12 17:23:58", "species": "", "readLen": "", "taskId": "W202506120003255", "downloadType": "0", "metadataId": "47f02fbafece421a92d8bc2bce27c85c", "metadataMenuId": "ce0c33632fa84a6fb1c265e8fe31a189", "projectName": "", "businessType": "", "projectType": "", "productType": "", "chipSpecs": "", "experimentProcess": "", "isMicroscopeFile": "", "qcResultFile": "", "imageToolType": "", "manufacture": "", "imageQcVersion": "", "stereoResepSwitch": "", "iprVersion": "", "processVersion": "1.0.0", "splitCount": "", "cbLength": "", "cbStart": "", "libraryType": "", "subProject": "", "snId": "", "menuId": "ce0c33632fa84a6fb1c265e8fe31a189", "menuStatus": "0", "menuSort": "1", "dataType": "0", "searchName": "stdout", "menuPath": "/Files/ResultData/Workflow/W202506120003255", "trackCrossQcPassFlag": "", "stitchedImage": "", "menuName": "W202506120003255", "linkType": "2"}, 
                             {"checkCode": "3685340396", "commonTag": "un_is_send_cnsa", "barcodeLen": "", "subnet": "hpc", "refrenece": "", "memo": "", "tissue": "", "pid": "", "path": "/zfsms3/ST_STOMICS/STOmics_cloud/odms/test/dcs_cloud/P1871461072416366593/Files/ResultData/Workflow/W202506120003255/input.json", "sampleRandomNo": "", "zone": "st", "id": "11550f6b07ef4fcf83ee5cea4f091c02", "tag": "", "umiLocation": "", "batchNo": "WF2025061210187", "mapping": "input.json", "sampleId": "123", "wfName": "", "wfTag": "workflow", "bussinessName": "\u65f6\u7a7aworkflow", "sampleNum": "", "sampleName": "", "sampleType": "", "sampleIntegrity": "", "resultNote": "", "sequenceType": "", "libraryNum": "", "slide": "", "barcode": "", "sequencePlatform": "", "basicQualityValue": "", "q30": "", "q20": "", "readNum": "", "baseNum": "", "estErr": "", "srcFilePath": "/zdsms1/ST_NOTEBOOK/P20Z10200N0039/workflow/test/param/users/st_stomics/P20Z10200N0039/WF2025061210187/1933091680321863682/input.json", "umiStartPos": "", "omicsType": "", "omics": "genomics", "fileSize": "136", "name": "input.json", "fastqType": "", "projectId": "P1871461072416366593", "status": "0", "metadataType": 0, "barcodeStart": "", "delFlag": "0", "sid": "1933091680321863682", "umiLen": "", "fileStatus": "0", "processId": "Hello_multiple", "fileExtension": "json", "bussinessCode": "202406170032", "chipId": "", "lane": "", "chipCategory": "", "creator": "hujiaming", "dyeType": "", "env": "", "parentId": "ce0c33632fa84a6fb1c265e8fe31a189", "createTime": "2025-06-12 17:23:58", "species": "", "readLen": "", "taskId": "W202506120003255", "downloadType": "0", "metadataId": "f9c270ac5a204094934cf7edaaeb9e2a", "metadataMenuId": "ce0c33632fa84a6fb1c265e8fe31a189", "projectName": "", "businessType": "", "projectType": "", "productType": "", "chipSpecs": "", "experimentProcess": "", "isMicroscopeFile": "", "qcResultFile": "", "imageToolType": "", "manufacture": "", "imageQcVersion": "", "stereoResepSwitch": "", "iprVersion": "", "processVersion": "1.0.0", "splitCount": "", "cbLength": "", "cbStart": "", "libraryType": "", "subProject": "", "snId": "", "menuId": "ce0c33632fa84a6fb1c265e8fe31a189", "menuStatus": "0", "menuSort": "1", "dataType": "0", "searchName": "input.json", "menuPath": "/Files/ResultData/Workflow/W202506120003255", "trackCrossQcPassFlag": "", "stitchedImage": "", "menuName": "W202506120003255", "linkType": "2"}]}
    result = await process_data_meatinfo(json.dumps(valid_data))
    print("示例1 - 有效数据:")
    print(f"返回数据: {result}")
    print("-" * 50)
if __name__ == "__main__":
    asyncio.run(main())
