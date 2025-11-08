"""
Function Calling (函数调用) 工作原理详解

Function Calling 允许大模型调用外部函数来获取信息或执行操作
"""

import json
import os
import dashscope

# ========== 第一步：定义函数 ==========
def get_current_weather(location, unit="摄氏度"):
    """
    实际的函数实现
    这个函数会被大模型调用
    """
    # 模拟天气数据
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


# ========== 第二步：定义函数描述（Schema） ==========
"""
函数描述告诉大模型：
1. 函数叫什么名字
2. 函数是做什么的
3. 函数需要什么参数
4. 参数的类型和说明
"""
functions = [
    {
        'name': 'get_current_weather',  # 函数名
        'description': 'Get the current weather in a given location.',  # 函数描述
        'parameters': {  # 参数定义
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': 'The city and state, e.g. San Francisco, CA'
                },
                'unit': {
                    'type': 'string',
                    'enum': ['celsius', 'fahrenheit']  # 可选值
                }
            },
            'required': ['location']  # 必需参数
        }
    }
]


# ========== 第三步：封装模型调用函数 ==========
def get_response(messages):
    """
    调用大模型，并传入函数描述
    """
    response = dashscope.Generation.call(
        model='qwen-max',
        messages=messages,           # 对话历史
        functions=functions,          # 函数描述（关键！）
        result_format='message'       # 返回消息格式
    )
    return response


# ========== 第四步：Function Calling 完整流程 ==========
def run_conversation():
    """
    Function Calling 的完整工作流程：
    
    1. 用户提问
    2. 模型分析是否需要调用函数
    3. 如果需要，模型返回 function_call
    4. 执行函数
    5. 将函数结果返回给模型
    6. 模型生成最终回答
    """
    
    # ===== Step 1: 用户提问 =====
    query = "大连的天气怎样"
    messages = [{"role": "user", "content": query}]
    
    # ===== Step 2: 第一次调用模型 =====
    # 模型会分析：用户问天气，需要调用 get_current_weather 函数
    response = get_response(messages)
    
    if not response or not response.output:
        print("获取响应失败")
        return None
    
    message = response.output.choices[0].message
    messages.append(message)  # 保存模型的消息
    
    # ===== Step 3: 检查模型是否要调用函数 =====
    if hasattr(message, 'function_call') and message.function_call:
        function_call = message.function_call
        tool_name = function_call['name']  # 函数名：'get_current_weather'
        arguments = json.loads(function_call['arguments'])  # 参数：{"location": "大连", "unit": "celsius"}
        
        print(f"模型决定调用函数: {tool_name}")
        print(f"函数参数: {arguments}")
        
        # ===== Step 4: 执行函数 =====
        tool_response = get_current_weather(
            location=arguments.get('location'),
            unit=arguments.get('unit', 'celsius'),
        )
        
        # ===== Step 5: 将函数结果添加到对话历史 =====
        tool_info = {
            "role": "function",           # 角色：function
            "name": tool_name,            # 函数名
            "content": tool_response      # 函数返回结果
        }
        messages.append(tool_info)
        
        # ===== Step 6: 第二次调用模型 =====
        # 模型现在有了函数返回的天气数据，可以生成最终回答
        response = get_response(messages)
        
        if not response or not response.output:
            print("获取第二次响应失败")
            return None
        
        message = response.output.choices[0].message
        return message
    
    # 如果模型不需要调用函数，直接返回
    return message


# ========== 工作流程图示 ==========
"""
用户: "大连的天气怎样"
  ↓
[模型分析] → 需要调用 get_current_weather 函数
  ↓
[模型返回] function_call: {
    "name": "get_current_weather",
    "arguments": '{"location": "大连", "unit": "celsius"}'
}
  ↓
[执行函数] get_current_weather("大连", "celsius")
  ↓
[函数返回] '{"location": "大连", "temperature": 11, ...}'
  ↓
[将结果返回给模型]
  ↓
[模型生成最终回答] "大连今天的天气是晴天，温度11摄氏度，有微风。"
"""


# ========== 关键点说明 ==========
"""
1. functions 参数：
   - 告诉模型有哪些函数可用
   - 模型根据函数描述决定是否调用

2. function_call 响应：
   - 模型返回 function_call 而不是普通文本
   - 包含函数名和参数（JSON字符串）

3. 对话历史管理：
   - 必须包含完整的对话历史
   - 包括：user消息、assistant消息、function消息

4. 消息角色：
   - "user": 用户消息
   - "assistant": 模型消息
   - "function": 函数返回结果

5. 多轮对话：
   - 可以多次调用函数
   - 每次函数调用后，模型会基于结果继续生成
"""


if __name__ == "__main__":
    # 设置 API Key
    api_key = os.environ.get('DASHSCOPE_API_KEY')
    dashscope.api_key = api_key
    
    result = run_conversation()
    if result:
        print("\n最终结果:", result.content)
    else:
        print("对话执行失败")

