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

# 测试简单调用
print("=" * 50)
print("测试调用 DeepSeek 模型，并调用天气函数")
print("=" * 50)

def get_current_weather(location, unit="摄氏度"):
    # 获取指定地点的天气
    temperature = -1
    if '大连' in location or 'Dalian' in location:
        temperature = 11
    if '上海' in location or 'Shanghai' in location:
        temperature = 36
    if '深圳' in location or 'Shenzhen' in location:
        temperature = 37
    weather_info = {
        "location": location,
        "temperature": temperature,
        "unit": unit,
        "forecast": ["晴天", "微风"],
    }
    return json.dumps(weather_info)

url = "http://localhost:11434/api/generate"
messages = [
    {"role": "user", "content": "我的名字是张三"}
]
# data = {
#     "model": "deepseek-r1:8b",  # 使用你已安装的模型
#     # "prompt": "大连的天气怎样",
#     "messages": [
#         {"role": "user", "content": "大连的天气怎样"}
#     ],
#     "functions": [
#         {
#             "name": "get_current_weather",
#             "description": "获取当前天气",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "城市名称"
#                     }
#                 }
#             }
#         }
#     ],
#     "stream": False,
#     "result_format": "message"
# }

try:
    # response = requests.post(url, json=data)
    response = chat_deepseek(messages)
    print(f"问题: {messages[0]['content']}")
    print(f"回答: {response}\n")
except Exception as e:
    print(f"错误: {e}")
