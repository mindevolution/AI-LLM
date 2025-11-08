"""
使用 Ollama Python SDK 调用本地 DeepSeek 模型（推荐方式）

安装: pip install ollama
"""

import ollama
import requests


def get_available_deepseek_model():
    """
    获取可用的 DeepSeek 模型名称
    
    Returns:
        第一个可用的 DeepSeek 模型名称，如果没有则返回 None
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        models = response.json().get("models", [])
        deepseek_models = [m["name"] for m in models if "deepseek" in m["name"].lower()]
        if deepseek_models:
            return deepseek_models[0]
    except:
        pass
    return None


def call_deepseek(prompt: str, model: str = None):
    """
    简单调用 DeepSeek
    
    Args:
        prompt: 用户输入
        model: 模型名称（deepseek-chat, deepseek-r1 等），如果为 None 则自动检测
    
    Returns:
        模型响应
    """
    if model is None:
        model = get_available_deepseek_model() or "deepseek-r1:8b"
    response = ollama.generate(
        model=model,
        prompt=prompt
    )
    return response['response']


def chat_deepseek(messages: list, model: str = None):
    """
    多轮对话
    
    Args:
        messages: 消息列表，格式: [{"role": "user", "content": "..."}, ...]
        model: 模型名称，如果为 None 则自动检测
    
    Returns:
        模型响应
    """
    if model is None:
        model = get_available_deepseek_model() or "deepseek-r1:8b"
    response = ollama.chat(
        model=model,
        messages=messages
    )
    return response['message']['content']


def chat_deepseek_stream(messages: list, model: str = None):
    """
    流式多轮对话
    
    Args:
        messages: 消息列表
        model: 模型名称，如果为 None 则自动检测
    
    Yields:
        每次生成的文本片段
    """
    if model is None:
        model = get_available_deepseek_model() or "deepseek-r1:8b"
    stream = ollama.chat(
        model=model,
        messages=messages,
        stream=True
    )
    
    for chunk in stream:
        if chunk['message']['content']:
            yield chunk['message']['content']


def chat_deepseek_with_tools(messages: list, tools: list = None, model: str = None):
    """
    带工具调用的多轮对话
    
    Args:
        messages: 消息列表，格式: [{"role": "user", "content": "..."}, ...]
        tools: 工具/函数定义列表，格式参考 Ollama tools 规范
        model: 模型名称，如果为 None 则自动检测
    
    Returns:
        完整的响应对象，包含 message 和可能的 tool_calls
    """
    if model is None:
        model = get_available_deepseek_model() or "deepseek-r1:8b"
    
    params = {
        "model": model,
        "messages": messages
    }
    
    if tools:
        params["tools"] = tools
    
    response = ollama.chat(**params)
    return response


def run_conversation_with_tools(user_query: str, tools: list, tool_functions: dict, model: str = None, max_iterations: int = 5):
    """
    运行带工具调用的完整对话流程
    
    Args:
        user_query: 用户查询
        tools: 工具定义列表（Ollama 格式）
        tool_functions: 工具函数字典，格式: {"function_name": callable_function}
        model: 模型名称，如果为 None 则自动检测
        max_iterations: 最大迭代次数，防止无限循环
    
    Returns:
        最终响应内容
    """
    if model is None:
        model = get_available_deepseek_model() or "deepseek-r1:8b"
    
    messages = [{"role": "user", "content": user_query}]
    
    for iteration in range(max_iterations):
        # 调用模型
        response = chat_deepseek_with_tools(messages, tools=tools, model=model)
        assistant_message = response.get('message', {})
        messages.append(assistant_message)
        
        # 检查是否有工具调用
        tool_calls = assistant_message.get('tool_calls', [])
        
        if not tool_calls:
            # 没有工具调用，返回最终响应
            return assistant_message.get('content', '')
        
        # 处理每个工具调用
        for tool_call in tool_calls:
            function_name = tool_call.get('function', {}).get('name')
            function_args = tool_call.get('function', {}).get('arguments', '{}')
            
            if function_name in tool_functions:
                # 执行工具函数
                import json
                try:
                    args = json.loads(function_args) if isinstance(function_args, str) else function_args
                    tool_result = tool_functions[function_name](**args)
                except Exception as e:
                    tool_result = f"Error executing {function_name}: {str(e)}"
                
                # 添加工具结果到消息历史
                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": str(tool_result)
                })
            else:
                # 工具函数不存在
                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": f"Function {function_name} not found"
                })
    
    # 如果达到最大迭代次数，返回最后一条消息
    return messages[-1].get('content', 'Max iterations reached')


# ========== 示例使用 ==========
if __name__ == "__main__":
    # 示例 1: 简单调用
    print("=" * 50)
    print("示例 1: 简单调用")
    print("=" * 50)
    result = call_deepseek("你好，介绍一下你自己")
    print(f"回答: {result}\n")
    
    # 示例 2: 多轮对话
    print("=" * 50)
    print("示例 2: 多轮对话")
    print("=" * 50)
    messages = [
        {"role": "user", "content": "我的名字是李四"}
    ]
    
    response1 = chat_deepseek(messages)
    print(f"用户: {messages[0]['content']}")
    print(f"助手: {response1}\n")
    
    messages.append({"role": "assistant", "content": response1})
    messages.append({"role": "user", "content": "我刚才说我叫什么？"})
    
    response2 = chat_deepseek(messages)
    print(f"用户: {messages[-1]['content']}")
    print(f"助手: {response2}\n")
    
    # 示例 3: 流式输出
    print("=" * 50)
    print("示例 3: 流式输出")
    print("=" * 50)
    messages = [{"role": "user", "content": "用一句话介绍人工智能"}]
    print("回答: ", end="", flush=True)
    for chunk in chat_deepseek_stream(messages):
        print(chunk, end="", flush=True)
    print("\n")
    
    # 示例 4: Function Calling（需要支持工具调用的模型）
    print("=" * 50)
    print("示例 4: Function Calling")
    print("=" * 50)
    print("注意: Function Calling 示例请参考 ollama_deep_seek_function_call.py")
    print("需要支持工具调用的模型，如: deepseek-r1 或 MFDoom/deepseek-r1-tool-calling\n")

