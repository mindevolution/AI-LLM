"""
基础调用阿里千问大模型的示例程序
使用dashscope SDK
"""

import os
import dashscope
from dashscope import Generation


def call_qwen(prompt: str, api_key: str = None):
    """
    调用千问模型
    
    Args:
        prompt: 输入的提示词
        api_key: DashScope API Key，如果不提供则使用默认值或从环境变量DASHSCOPE_API_KEY读取
    
    Returns:
        模型返回的响应
    """
    # 设置API Key（如果未提供则使用默认值）
    if api_key is None:
        api_key = os.getenv("DASHSCOPE_API_KEY")
    
    dashscope.api_key = api_key
    
    # 调用千问模型
    response = Generation.call(
        model=Generation.Models.qwen_turbo,  # 使用千问turbo模型
        prompt=prompt
    )
    
    # 返回结果
    if response.status_code == 200:
        return response.output.text
    else:
        return f"错误: {response.message}"


def main():
    """主函数"""
    # 提示：请设置环境变量 DASHSCOPE_API_KEY 或在代码中直接设置
    # dashscope.api_key = "your_api_key_here"
    
    # 测试调用
    prompt = "你好，请介绍一下你自己"
    
    print("正在调用千问模型...")
    print(f"输入: {prompt}\n")
    
    result = call_qwen(prompt)
    
    print("输出:")
    print(result)


if __name__ == "__main__":
    main()

