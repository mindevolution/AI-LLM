"""
快速测试 Ollama DeepSeek 调用
"""

import requests

# 检查 Ollama 服务
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    print("✓ Ollama 服务运行正常")
    
    # 列出可用模型
    models = response.json().get("models", [])
    deepseek_models = [m["name"] for m in models if "deepseek" in m["name"].lower()]
    print(f"✓ 找到 DeepSeek 模型: {deepseek_models}\n")
except:
    print("✗ Ollama 服务未运行，请先运行: ollama serve")
    exit(1)

# 测试简单调用
print("=" * 50)
print("测试调用 DeepSeek 模型")
print("=" * 50)

url = "http://localhost:11434/api/generate"
data = {
    "model": "deepseek-r1:8b",  # 使用你已安装的模型
    "prompt": "你好，请用一句话介绍你自己",
    "stream": False
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    print(f"问题: {data['prompt']}")
    print(f"回答: {result.get('response', '无响应')}\n")
except Exception as e:
    print(f"错误: {e}")

