import requests
import json
from ollama_deepseek_sdk import call_deepseek, chat_deepseek
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


messages = [
    {"role": "user", "content": "我的名字是张三"}
]
try:
    response = chat_deepseek(messages)
    print(f"问题: {messages[0]['content']}")
    print(f"回答: {response}\n")
except Exception as e:
    print(f"错误: {e}")