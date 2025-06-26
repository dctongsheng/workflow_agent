from utils import process_data_meatinfo
import asyncio
import json

data_meatinfo = {
    "records": [
        {"name": "1111.gef", "omics": "genomics", "wfTag": "", "is_raw_data": False},
        {"name": "input.gef", "omics": "genomics", "wfTag": "","is_raw_data": True}
    ]
}
# 将字典转换为JSON字符串
data_meatinfo_json = json.dumps(data_meatinfo,ensure_ascii=False)
res = asyncio.run(process_data_meatinfo(data_meatinfo_json))
print(res)