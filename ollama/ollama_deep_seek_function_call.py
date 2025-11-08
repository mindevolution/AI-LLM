"""
使用 Ollama DeepSeek SDK 进行 Function Calling 示例

这个示例展示了如何使用 ollama_deepseek_sdk 进行函数调用
"""

import requests
import json
from ollama_deepseek_sdk import (
    chat_deepseek_with_tools, 
    run_conversation_with_tools,
    get_available_deepseek_model
)

# 检查 Ollama 服务
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    print("✓ Ollama 服务运行正常")
    
    # 列出可用模型
    models = response.json().get("models", [])
    deepseek_models = [m["name"] for m in models if "deepseek" in m["name"].lower()]
    print(f"✓ 找到 DeepSeek 模型: {deepseek_models}\n")
    
    if not deepseek_models:
        print("⚠️  警告: 未找到 DeepSeek 模型，请运行: ollama pull deepseek-r1:8b")
        print("   或者使用支持工具调用的模型: ollama pull MFDoom/deepseek-r1-tool-calling:8b\n")
except:
    print("✗ Ollama 服务未运行，请先运行: ollama serve")
    exit(1)


# ========== 1. 定义工具函数 ==========
def get_current_weather(location: str, unit: str = "摄氏度"):
    """
    获取指定地点的天气
    
    Args:
        location: 城市名称
        unit: 温度单位（摄氏度/华氏度）
    
    Returns:
        天气信息的 JSON 字符串
    """
    # 为了演示，这里使用固定数据
    # 实际应用中，可以调用真实的天气 API
    temperature = -1
    if '大连' in location or 'Dalian' in location:
        temperature = 11
    elif '上海' in location or 'Shanghai' in location:
        temperature = 36
    elif '深圳' in location or 'Shenzhen' in location:
        temperature = 37
    elif '北京' in location or 'Beijing' in location:
        temperature = 15
    
    weather_info = {
        "location": location,
        "temperature": temperature,
        "unit": unit,
        "forecast": ["晴天", "微风"],
    }
    return json.dumps(weather_info, ensure_ascii=False)


# ========== 2. 定义工具描述（Ollama 格式） ==========
# Ollama 使用 OpenAI 兼容的 tools 格式
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：大连、上海、深圳、北京"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["摄氏度", "华氏度"],
                        "description": "温度单位，默认为摄氏度"
                    }
                },
                "required": ["location"]
            }
        }
    }
]


# ========== 3. 方法一：使用 run_conversation_with_tools（推荐，最简单） ==========
def example_1_simple_way():
    """最简单的方式：使用 run_conversation_with_tools"""
    print("=" * 60)
    print("方法一：使用 run_conversation_with_tools（推荐）")
    print("=" * 60)
    
    # 定义工具函数映射
    tool_functions = {
        "get_current_weather": get_current_weather
    }
    
    query = "大连的天气怎样？"
    print(f"👤 用户: {query}\n")
    
    try:
        result = run_conversation_with_tools(
            user_query=query,
            tools=tools,
            tool_functions=tool_functions
        )
        print(f"🤖 助手: {result}\n")
    except Exception as e:
        print(f"❌ 错误: {e}\n")


# ========== 4. 方法二：手动处理工具调用（更灵活） ==========
def example_2_manual_way():
    """手动处理工具调用，更灵活的控制流程"""
    print("=" * 60)
    print("方法二：手动处理工具调用")
    print("=" * 60)
    
    query = "上海和深圳的天气分别是多少？"
    print(f"👤 用户: {query}\n")
    
    messages = [{"role": "user", "content": query}]
    model = get_available_deepseek_model() or "deepseek-r1:8b"
    
    max_iterations = 5
    for iteration in range(max_iterations):
        print(f"--- 第 {iteration + 1} 轮对话 ---")
        
        # 调用模型
        response = chat_deepseek_with_tools(
            messages=messages,
            tools=tools,
            model=model
        )
        
        assistant_message = response.get('message', {})
        messages.append(assistant_message)
        
        # 检查是否有工具调用
        tool_calls = assistant_message.get('tool_calls', [])
        
        if not tool_calls:
            # 没有工具调用，返回最终响应
            print(f"🤖 助手: {assistant_message.get('content', '')}\n")
            break
        
        # 处理每个工具调用
        print(f"🔧 模型决定调用 {len(tool_calls)} 个工具:")
        for tool_call in tool_calls:
            function_name = tool_call.get('function', {}).get('name')
            function_args = tool_call.get('function', {}).get('arguments', '{}')
            
            print(f"  - 函数: {function_name}")
            print(f"  - 参数: {function_args}")
            
            # 执行工具函数
            try:
                args = json.loads(function_args) if isinstance(function_args, str) else function_args
                tool_result = get_current_weather(**args)
                print(f"  - 结果: {tool_result}")
            except Exception as e:
                tool_result = f"Error: {str(e)}"
                print(f"  - 错误: {tool_result}")
            
            # 添加工具结果到消息历史
            messages.append({
                "role": "tool",
                "name": function_name,
                "content": str(tool_result)
            })
        
        print()
    else:
        print("⚠️  达到最大迭代次数\n")


# ========== 5. 主函数 ==========
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Ollama DeepSeek Function Calling 示例")
    print("=" * 60 + "\n")
    
    # 运行示例
    try:
        example_1_simple_way()
        print("\n")
        example_2_manual_way()
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("提示:")
    print("1. 确保使用支持工具调用的模型（如 deepseek-r1 或 MFDoom/deepseek-r1-tool-calling）")
    print("2. 如果模型不支持工具调用，可能需要使用其他模型")
    print("3. 工具定义格式遵循 OpenAI 兼容格式")
    print("=" * 60)
