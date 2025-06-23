#!/usr/bin/env python3
"""
自动填写参数模块
基于Dify聊天消息API实现参数自动填充功能
"""

import aiohttp
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import json
import re

def parse_ai_json_output(ai_output):
    """
    专门处理AI输出的JSON解析函数
    """
    if not ai_output:
        return None
    
    try:
        # 如果已经是字典
        if isinstance(ai_output, dict):
            return ai_output
        
        # 转换为字符串处理
        content = str(ai_output).strip()
        
        # 查找JSON内容（可能被包装在其他文本中）
        json_pattern = r'\{.*\}'
        match = re.search(json_pattern, content, re.DOTALL)
        
        if match:
            json_str = match.group()
            
            # 移除可能的转义
            if json_str.startswith('"{') and json_str.endswith('}"'):
                json_str = json_str[1:-1]  # 移除外层引号
                json_str = json_str.replace('\\"', '"')  # 处理转义引号
                json_str = json_str.replace('\\n', '')   # 移除转义换行符
            
            return json.loads(json_str)
        
        # 如果没找到JSON模式，尝试直接解析
        return json.loads(content)
        
    except Exception as e:
        print(f"解析AI输出失败: {e}")
        print(f"原始输出: {ai_output}")
        return None

class AutoParamFillerError(Exception):
    """自动填写参数异常"""
    pass

class AutoParamFiller:
    """自动填写参数客户端"""
    
    def __init__(
        self, 
        base_url: str = "http://172.28.140.214", 
        api_key: str = "app-I9zUYHi9izQnqdDBZ5Z0cGx6"
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    async def auto_fill_parameters(
        self,
        data_choose: Dict[str, str],
        query_template: Dict[str, str],
        user: str = "abc-123",
        response_mode: str = "blocking",
        conversation_id: str = "",
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        异步调用自动填写参数API
        
        Args:
            data_choose: 数据选择列表或字符串
            query_template: 查询模板字典，包含需要填写的参数
            user: 用户标识
            response_mode: 响应模式 ("blocking" 或 "streaming")
            conversation_id: 会话ID
            timeout: 超时时间（秒）
            
        Returns:
            API响应结果
            
        Raises:
            AutoParamFillerError: API调用失败时抛出
        """
        url = f"{self.base_url}/v1/chat-messages"
        
        # 处理data_choose参数
        if isinstance(data_choose, list):
            data_choose_str = json.dumps(data_choose)
        else:
            data_choose_str = data_choose
        
        payload = {
            "inputs": {
                "data_choose": data_choose_str
            },
            "query": json.dumps(query_template),
            "response_mode": response_mode,
            "conversation_id": conversation_id,
            "user": user
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"自动填写参数API调用成功")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"自动填写参数API调用失败: HTTP {response.status}, {error_text}")
                        raise AutoParamFillerError(f"HTTP {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            logger.error("自动填写参数API调用超时")
            raise AutoParamFillerError("请求超时")
        except aiohttp.ClientError as e:
            logger.error(f"自动填写参数API网络错误: {e}")
            raise AutoParamFillerError(f"网络错误: {e}")
        except Exception as e:
            logger.error(f"自动填写参数API未知错误: {e}")
            raise AutoParamFillerError(f"未知错误: {e}")
    
    async def parse_filled_parameters(self, response: Dict[str, Any]) -> Dict[str, str]:
        """
        解析API响应中的已填写参数
        
        Args:
            response: API响应结果
            
        Returns:
            解析后的参数字典
        """
        try:
            # 从响应中提取answer字段
            answer = response.get("answer", "")
            
            # 尝试解析JSON格式的answer
            if isinstance(answer, str):
                try:
                    parsed_params = json.loads(answer)
                    return parsed_params
                except json.JSONDecodeError:
                    logger.warning("无法解析answer为JSON格式")
                    return {"raw_answer": answer}
            else:
                return answer
                
        except Exception as e:
            logger.error(f"解析参数失败: {e}")
            return {"error": str(e)}

# 创建全局客户端实例
auto_param_filler = AutoParamFiller()

async def auto_fill_parameters(
    data_choose: Dict[str, Any],
    query_template: Dict[str, str],
    user: str = "abc-123",
    conversation_id: str = "",
    response_mode: str = "blocking"
) -> Dict[str, Any]:
    """
    便捷函数：自动填写参数
    
    Args:
        data_choose: 数据选择列表或字符串
        query_template: 查询模板字典
        user: 用户标识
        conversation_id: 会话ID
        response_mode: 响应模式 ("blocking" 或 "streaming")
        
    Returns:
        API响应结果
    """
    return await auto_param_filler.auto_fill_parameters(
        data_choose, query_template, user, response_mode, conversation_id
    )

async def get_filled_parameters(
    data_choose: Dict[str, Any],
    query_template: Dict[str, str],
    user: str = "abc-123",
    conversation_id: str = "",
    response_mode: str = "blocking"
) -> Dict[str, str]:
    """
    获取已填写的参数
    
    Args:
        data_choose: 数据选择列表或字符串
        query_template: 查询模板字典
        user: 用户标识
        conversation_id: 会话ID
        response_mode: 响应模式 ("blocking" 或 "streaming")
        
    Returns:
        已填写的参数字典
    """
    response = await auto_fill_parameters(data_choose, query_template, user, conversation_id, response_mode)
    return await auto_param_filler.parse_filled_parameters(response)
from example import get_auto_fill_parameters,auto_fill_parameters_data
# 示例使用
async def main():
    """测试函数"""
    try:
        # 测试数据
        data_choose = get_auto_fill_parameters(auto_fill_parameters_data)
        print(data_choose)
        
        query_template = {
            'SN': '',
            'RegistJson': '',
            'DataDir': '',
            'ImageTar': '',
            'ImagePreDir': '',
            'Tissue': '',
            'Reference': ''
        }
        
        print("=== 测试自动填写参数功能 ===")
        
        # 调用API
        result = await auto_fill_parameters(data_choose, query_template)
        print("API调用成功:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 解析参数
        filled_params = await get_filled_parameters(data_choose, query_template)
        print("\n已填写的参数:")
        print(json.dumps(filled_params, ensure_ascii=False, indent=2))
        
    except AutoParamFillerError as e:
        print(f"API调用失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 