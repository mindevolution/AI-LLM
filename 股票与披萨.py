#!/usr/bin/env python
# coding: utf-8

import json
import dashscope
import random
from datetime import datetime

# 设置API密钥 - 使用你自己的密钥
dashscope.api_key = 'sk-07a445f7e4c84c6ca83f73450928191a'

print("🚀 智能助手启动...")

# 1. 股价查询函数（模拟）
def get_stock_price(stock_symbol):
    """获取股票价格 - 模拟真实数据"""
    stock_prices = {
        "TSLA": f"${random.uniform(180, 250):.2f}",
        "AAPL": f"${random.uniform(150, 200):.2f}", 
        "NVDA": f"${random.uniform(400, 500):.2f}",
        "MSFT": f"${random.uniform(300, 400):.2f}"
    }
    
    price = stock_prices.get(stock_symbol.upper(), "未知股票")
    result = {
        "股票代码": stock_symbol.upper(),
        "当前价格": price,
        "查询时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "涨跌幅": f"{random.uniform(-5, 5):.1f}%"
    }
    return json.dumps(result, ensure_ascii=False)

# 2. 披萨订购函数（模拟）
def order_pizza(pizza_type="玛格丽特", size="中份", address=None):
    """订购披萨 - 模拟真实下单"""
    if not address:
        address = "北京市朝阳区xxx街道"
    
    order_id = f"PZ{random.randint(1000, 9999)}"
    delivery_time = random.randint(25, 45)
    
    result = {
        "订单号": order_id,
        "披萨类型": pizza_type,
        "尺寸": size,
        "送达地址": address,
        "预计送达时间": f"{delivery_time}分钟",
        "订单状态": "已确认",
        "总金额": f"¥{random.randint(60, 120)}"
    }
    return json.dumps(result, ensure_ascii=False)

# 3. AI响应函数
def get_ai_response(messages):
    """调用AI获取响应"""
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=messages,
            tools=tools,
            result_format='message'
        )
        return response
    except Exception as e:
        print(f"❌ API调用出错: {e}")
        return None

# 4. 定义可用的功能列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "获取指定股票的实时价格信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_symbol": {
                        "type": "string",
                        "description": "股票代码，如TSLA、AAPL、NVDA等"
                    }
                },
                "required": ["stock_symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "order_pizza",
            "description": "订购披萨外卖",
            "parameters": {
                "type": "object",
                "properties": {
                    "pizza_type": {
                        "type": "string", 
                        "description": "披萨类型，如玛格丽特、海鲜、培根等",
                        "default": "玛格丽特"
                    },
                    "size": {
                        "type": "string",
                        "description": "披萨尺寸：小份、中份、大份",
                        "default": "中份"
                    },
                    "address": {
                        "type": "string",
                        "description": "配送地址"
                    }
                },
                "required": []
            }
        }
    }
]

# 5. 主对话函数
def run_conversation(user_query):
    """运行智能对话"""
    print(f"👤 用户提问: {user_query}")
    print("=" * 50)
    
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以帮用户查询股票价格和订购披萨。"},
        {"role": "user", "content": user_query}
    ]
    
    max_steps = 5  # 防止无限循环
    step = 0
    
    while step < max_steps:
        step += 1
        print(f"🔄 第{step}步推理...")
        
        # 获取AI响应
        response = get_ai_response(messages)
        if not response:
            print("❌ 获取AI响应失败")
            break
            
        message = response.output.choices[0].message
        messages.append(message)
        
        print(f"🤖 AI思考: {message.content if hasattr(message, 'content') else '正在调用功能...'}")
        
        # 检查是否需要停止
        if response.output.choices[0].finish_reason == 'stop':
            print("✅ 对话完成！")
            final_message = message.content if hasattr(message, 'content') else "对话结束"
            return final_message
        
        # 检查是否需要调用功能
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 调用功能: {function_name}")
                print(f"📋 功能参数: {function_args}")
                
                # 执行对应的功能
                if function_name == "get_stock_price":
                    function_result = get_stock_price(**function_args)
                elif function_name == "order_pizza":
                    function_result = order_pizza(**function_args)
                else:
                    function_result = json.dumps({"error": "未知功能"})
                
                print(f"📊 功能结果: {function_result}")
                
                # 将功能结果加入对话
                tool_message = {
                    "role": "tool",
                    "content": function_result,
                    "name": function_name
                }
                messages.append(tool_message)
        else:
            print("✅ 无需调用功能，直接回复")
            return message.content if hasattr(message, 'content') else "完成"
    
    return "对话超时"

# 6. 测试运行
if __name__ == "__main__":
    print("🎯 测试场景：查股价 + 订披萨")
    print("=" * 50)
    
    # 测试查询
    user_question = "帮我查下特斯拉股价，然后订个海鲜披萨大份送到北京市海淀区中关村"
    
    result = run_conversation(user_question)
    
    print("=" * 50)
    print("🎉 最终结果:")
    print(result)