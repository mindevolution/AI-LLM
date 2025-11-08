"""
Function Calling 简化示例
演示核心工作流程
"""

import json
import os
import dashscope

# 设置 API Key
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

# ========== 1. 定义要调用的函数 ==========
def get_current_weather(location, unit="celsius"):
    """获取天气信息（模拟）"""
    weather_data = {
        "大连": 11,
        "上海": 36,
        "深圳": 37
    }
    temp = weather_data.get(location, 20)
    return json.dumps({
        "location": location,
        "temperature": temp,
        "unit": unit
    })


# ========== 2. 定义函数描述（告诉模型有这个函数） ==========
functions = [
    {
        'name': 'get_current_weather',
        'description': '获取指定城市的当前天气',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': '城市名称，例如：大连、上海'
                },
                'unit': {
                    'type': 'string',
                    'enum': ['celsius', 'fahrenheit'],
                    'description': '温度单位'
                }
            },
            'required': ['location']
        }
    }
]


# ========== 3. Function Calling 核心流程 ==========
def chat_with_function(user_query):
    """
    Function Calling 的核心流程：
    1. 用户提问
    2. 模型决定调用函数
    3. 执行函数
    4. 模型基于函数结果回答
    """
    
    # 初始化对话
    messages = [{"role": "user", "content": user_query}]
    
    # ===== 第一轮：模型决定调用函数 =====
    print(f"👤 用户: {user_query}\n")
    
    response = dashscope.Generation.call(
        model='qwen-max',
        messages=messages,
        functions=functions,  # 传入函数描述
        result_format='message'
    )
    
    message = response.output.choices[0].message
    messages.append(message)
    
    # ===== 检查是否需要调用函数 =====
    if hasattr(message, 'function_call') and message.function_call:
        func_call = message.function_call
        func_name = func_call['name']
        func_args = json.loads(func_call['arguments'])
        
        print(f"🤖 模型决定调用函数: {func_name}")
        print(f"📝 函数参数: {func_args}\n")
        
        # ===== 执行函数 =====
        if func_name == 'get_current_weather':
            result = get_current_weather(
                location=func_args.get('location'),
                unit=func_args.get('unit', 'celsius')
            )
            print(f"⚙️  函数执行结果: {result}\n")
            
            # ===== 将函数结果返回给模型 =====
            messages.append({
                "role": "function",
                "name": func_name,
                "content": result
            })
            
            # ===== 第二轮：模型基于函数结果回答 =====
            response = dashscope.Generation.call(
                model='qwen-max',
                messages=messages,
                functions=functions,
                result_format='message'
            )
            
            final_message = response.output.choices[0].message
            print(f"🤖 最终回答: {final_message.content}\n")
            
            return final_message.content
    
    # 如果不需要调用函数，直接返回
    print(f"🤖 回答: {message.content}\n")
    return message.content


# ========== 测试 ==========
if __name__ == "__main__":
    # 测试 1: 需要调用函数
    print("=" * 50)
    print("测试 1: 查询天气（需要调用函数）")
    print("=" * 50)
    chat_with_function("大连的天气怎么样？")
    
    print("\n" + "=" * 50)
    print("测试 2: 普通对话（不需要调用函数）")
    print("=" * 50)
    chat_with_function("你好，介绍一下你自己")

