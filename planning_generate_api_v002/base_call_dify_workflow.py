import aiohttp
import asyncio
import json
from typing import Dict, Any, Optional

async def run_workflow(
  api_key: str,
  inputs: Dict[str, Any] = None,
  response_mode: str = "blocking",
  user: str = "abc-123",
  base_url: str = "http://120.76.217.102"
) -> Dict[str, Any]:
  """
  异步调用工作流API
  
  Args:
      api_key (str): API密钥
      inputs (Dict[str, Any], optional): 输入参数，默认为空字典
      response_mode (str, optional): 响应模式，默认为"blocking"
      user (str, optional): 用户标识，默认为"abc-123"
      base_url (str, optional): API基础URL
  
  Returns:
      Dict[str, Any]: API响应结果
  
  Raises:
      aiohttp.ClientError: 网络请求错误
      json.JSONDecodeError: JSON解析错误
  """
  if inputs is None:
      inputs = {}
  
  url = f"{base_url}/v1/workflows/run"
  
  headers = {
      'Authorization': f'Bearer {api_key}',
      'Content-Type': 'application/json'
  }
  
  payload = {
      "inputs": inputs,
      "response_mode": response_mode,
      "user": user
  }
  
  async with aiohttp.ClientSession() as session:
      try:
          async with session.post(
              url, 
              headers=headers, 
              json=payload,
              timeout=aiohttp.ClientTimeout(total=30)
          ) as response:
              # 检查HTTP状态码
              response.raise_for_status()
              
              # 解析JSON响应
              result = await response.json()
              return result
              
      except aiohttp.ClientError as e:
          print(f"网络请求错误: {e}")
          raise
      except json.JSONDecodeError as e:
          print(f"JSON解析错误: {e}")
          raise
      except Exception as e:
          print(f"未知错误: {e}")
          raise

# 使用示例
async def intent_detection(query:str):
  """使用示例"""
  api_key = "app-UBY1y9xj4q3dT6XV2P4uBLKi"  # 替换为实际的API密钥
  
  try:
      # 调用工作流
      result = await run_workflow(
          api_key=api_key,
          inputs={"query": query},  # 根据需要修改输入参数
          response_mode="blocking",
          user="abc-123"
      )
      
      print("工作流执行成功:")
      print(json.dumps(result, indent=2, ensure_ascii=False))
      try:
        if result["data"]["outputs"]["structured_output"]["classification"] == "STANDARD_BIOINFORMATICS":
            return 1
        elif result["data"]["outputs"]["structured_output"]["classification"] == "NON_BIOINFORMATICS":
            return 0
        elif result["data"]["outputs"]["structured_output"]["classification"] == "ADVANCED_BIOINFORMATICS":
            return 2
        else:
            return 0
      except Exception as e:
        print(f"工作流执行失败: {e}")
        return -1

      
  except Exception as e:
      print(f"工作流执行失败: {e}")
      return -1

# 运行示例（如果直接执行此脚本）
if __name__ == "__main__":
  asyncio.run(intent_detection("富集分析"))