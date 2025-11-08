"""
调用本地 Ollama DeepSeek 模型示例

需要先安装 ollama 并拉取 deepseek 模型：
1. 安装 ollama: https://ollama.ai
2. 拉取模型: ollama pull deepseek-chat
3. 或者: ollama pull deepseek-r1
"""

import json
import requests


# ========== 方法 1: 使用 requests 直接调用 Ollama API ==========
def call_ollama_deepseek_simple(prompt: str, model: str = "deepseek-chat"):
    """
    简单调用方式 - 单次对话
    
    Args:
        prompt: 用户输入
        model: 模型名称，默认 deepseek-chat
    
    Returns:
        模型响应文本
    """
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False  # 非流式输出
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except requests.exceptions.ConnectionError:
        return "错误: 无法连接到 Ollama，请确保 Ollama 服务正在运行"
    except Exception as e:
        return f"错误: {str(e)}"


# ========== 方法 2: 流式输出 ==========
def call_ollama_deepseek_stream(prompt: str, model: str = "deepseek-chat"):
    """
    流式调用方式 - 实时输出
    
    Args:
        prompt: 用户输入
        model: 模型名称
    
    Yields:
        每次生成的文本片段
    """
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": True  # 流式输出
    }
    
    try:
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "response" in chunk:
                    yield chunk["response"]
                if chunk.get("done", False):
                    break
    except requests.exceptions.ConnectionError:
        yield "错误: 无法连接到 Ollama，请确保 Ollama 服务正在运行"
    except Exception as e:
        yield f"错误: {str(e)}"


# ========== 方法 3: 多轮对话（Chat API） ==========
def call_ollama_deepseek_chat(messages: list, model: str = "deepseek-chat"):
    """
    多轮对话方式 - 支持对话历史
    
    Args:
        messages: 消息列表，格式: [{"role": "user", "content": "..."}, ...]
        model: 模型名称
    
    Returns:
        模型响应
    """
    url = "http://localhost:11434/api/chat"
    
    data = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("message", {}).get("content", "")
    except requests.exceptions.ConnectionError:
        return "错误: 无法连接到 Ollama，请确保 Ollama 服务正在运行"
    except Exception as e:
        return f"错误: {str(e)}"


# ========== 方法 4: 流式多轮对话 ==========
def call_ollama_deepseek_chat_stream(messages: list, model: str = "deepseek-chat"):
    """
    流式多轮对话
    
    Args:
        messages: 消息列表
        model: 模型名称
    
    Yields:
        每次生成的文本片段
    """
    url = "http://localhost:11434/api/chat"
    
    data = {
        "model": model,
        "messages": messages,
        "stream": True
    }
    
    try:
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]
                if chunk.get("done", False):
                    break
    except requests.exceptions.ConnectionError:
        yield "错误: 无法连接到 Ollama，请确保 Ollama 服务正在运行"
    except Exception as e:
        yield f"错误: {str(e)}"


# ========== 方法 5: 使用 ollama Python SDK（推荐） ==========
def call_ollama_deepseek_sdk(prompt: str, model: str = "deepseek-chat"):
    """
    使用 ollama Python SDK（需要先安装: pip install ollama）
    
    Args:
        prompt: 用户输入
        model: 模型名称
    
    Returns:
        模型响应
    """
    try:
        import ollama
        
        response = ollama.generate(
            model=model,
            prompt=prompt
        )
        return response['response']
    except ImportError:
        return "错误: 请先安装 ollama SDK: pip install ollama"
    except Exception as e:
        return f"错误: {str(e)}"


# ========== 测试函数 ==========
def test_simple():
    """测试简单调用"""
    print("=" * 50)
    print("测试 1: 简单调用")
    print("=" * 50)
    result = call_ollama_deepseek_simple("你好，请介绍一下你自己")
    print(f"回答: {result}\n")


def test_stream():
    """测试流式输出"""
    print("=" * 50)
    print("测试 2: 流式输出")
    print("=" * 50)
    print("回答: ", end="", flush=True)
    for chunk in call_ollama_deepseek_stream("用一句话介绍 Python"):
        print(chunk, end="", flush=True)
    print("\n")


def test_chat():
    """测试多轮对话"""
    print("=" * 50)
    print("测试 3: 多轮对话")
    print("=" * 50)
    
    messages = [
        {"role": "user", "content": "我的名字是张三"}
    ]
    
    # 第一轮
    response1 = call_ollama_deepseek_chat(messages)
    print(f"用户: {messages[0]['content']}")
    print(f"助手: {response1}\n")
    
    # 第二轮
    messages.append({"role": "assistant", "content": response1})
    messages.append({"role": "user", "content": "我刚才说我叫什么名字？"})
    response2 = call_ollama_deepseek_chat(messages)
    print(f"用户: {messages[-1]['content']}")
    print(f"助手: {response2}\n")


def test_chat_stream():
    """测试流式多轮对话"""
    print("=" * 50)
    print("测试 4: 流式多轮对话")
    print("=" * 50)
    
    messages = [
        {"role": "user", "content": "写一首关于春天的短诗"}
    ]
    
    print("回答: ", end="", flush=True)
    for chunk in call_ollama_deepseek_chat_stream(messages):
        print(chunk, end="", flush=True)
    print("\n")


# ========== 主函数 ==========
if __name__ == "__main__":
    # 检查 Ollama 是否运行
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        print("✓ Ollama 服务运行正常\n")
    except:
        print("✗ 错误: Ollama 服务未运行")
        print("请先启动 Ollama 服务，或运行: ollama serve\n")
        exit(1)
    
    # 运行测试
    test_simple()
    # test_stream()
    # test_chat()
    # test_chat_stream()

