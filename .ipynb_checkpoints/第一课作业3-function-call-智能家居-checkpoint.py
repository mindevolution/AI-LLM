import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role
# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

# 定义函数规范
functions = [
    {
        "name": "control_device",
        "description": "控制家庭中的智能设备，如灯、空调、窗帘等",
        "parameters": {
            "type": "object",
            "properties": {
                "device": {"type": "string", "description": "设备名称，如灯、空调、窗帘"},
                "location": {"type": "string", "description": "设备所在位置，如客厅、卧室"},
                "action": {"type": "string", "description": "执行的操作，如打开、关闭、调节温度"},
                "value": {"type": "number", "description": "可选的数值参数，如温度、亮度", "nullable": True}
            },
            "required": ["device", "location", "action"]
        }
    },
    {
        "name": "get_device_status",
        "description": "获取指定设备的当前状态",
        "parameters": {
            "type": "object",
            "properties": {
                "device": {"type": "string"},
                "location": {"type": "string"}
            },
            "required": ["device", "location"]
        }
    }
]

# 模拟设备状态数据库
device_states = {
    ("灯", "客厅"): {"status": "关闭"},
    ("空调", "客厅"): {"status": "关闭", "温度": 26}
}

# 定义执行函数
def control_device(device, location, action, value=None):
    key = (device, location)
    if key not in device_states:
        return f"{location}的{device}不存在。"
    if action in ["打开", "开启"]:
        device_states[key]["status"] = "开启"
    elif action == "关闭":
        device_states[key]["status"] = "关闭"
    elif "调到" in action or "设置" in action:
        device_states[key]["温度"] = value
    return f"已{action}{location}的{device}。当前状态：{device_states[key]}"

def get_device_status(device, location):
    key = (device, location)
    if key not in device_states:
        return f"{location}的{device}不存在。"
    return device_states[key]

# 模拟用户输入
user_message = "打开客厅的灯并把空调调到24度"

# 调用模型
response = dashscope.Generation.call(
    model="deepseek-v3",
    messages=[{"role": "user", "content": user_message}],
    functions=functions,
    function_call="auto"
)
print('response=', response)

# 解析模型响应
# response_message = response.choices[0].message

# if response_message.function_call:
#     func_name = response_message.function_call.name
#     arguments = json.loads(response_message.function_call.arguments)

#     if func_name == "control_device":
#         result = control_device(**arguments)
#     elif func_name == "get_device_status":
#         result = get_device_status(**arguments)
#     else:
#         result = "未知函数"

#     print(f"🧩 模型调用函数: {func_name}")
#     print(f"📦 参数: {arguments}")
#     print(f"✅ 执行结果: {result}")
# else:
#     print("模型未调用函数:", response_message.content)