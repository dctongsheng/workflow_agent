from utils import process_data_meatinfo
import asyncio
import json

data_meatinfo = {
    "records": [
        {"name": "1111.fq.gz", "omics": "genomics", "is_raw_data": False},
        {"name": "input.json", "omics": "genomics", "wfTag": "workflow", "is_raw_data": True}
    ]
}
# 将字典转换为JSON字符串
data_meatinfo_json = json.dumps(data_meatinfo)
res = asyncio.run(process_data_meatinfo(data_meatinfo_json))
print(res)