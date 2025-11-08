"""
使用 Ollama Python SDK 调用本地 DeepSeek 模型（推荐方式）

安装: pip install ollama
"""

import ollama


def call_deepseek(prompt: str, model: str = "deepseek-chat"):
    """
    简单调用 DeepSeek
    
    Args:
        prompt: 用户输入
        model: 模型名称（deepseek-chat, deepseek-r1 等）
    
    Returns:
        模型响应
    """
    response = ollama.generate(
        model=model,
        prompt=prompt
    )
    return response['response']


def chat_deepseek(messages: list, model: str = "deepseek-chat"):
    """
    多轮对话
    
    Args:
        messages: 消息列表，格式: [{"role": "user", "content": "..."}, ...]
        model: 模型名称
    
    Returns:
        模型响应
    """
    response = ollama.chat(
        model=model,
        messages=messages
    )
    return response['message']['content']


def chat_deepseek_stream(messages: list, model: str = "deepseek-chat"):
    """
    流式多轮对话
    
    Args:
        messages: 消息列表
        model: 模型名称
    
    Yields:
        每次生成的文本片段
    """
    stream = ollama.chat(
        model=model,
        messages=messages,
        stream=True
    )
    
    for chunk in stream:
        if chunk['message']['content']:
            yield chunk['message']['content']


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

