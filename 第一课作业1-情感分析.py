import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role

# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

# 封装模型响应函数


def get_response(messages):
    response = dashscope.Generation.call(
        model='deepseek-v3',
        messages=messages,
        result_format='message'  # 将输出设置为message形式
    )
    return response


situations = [
    # '我今天下班回家很晚，老婆没有等我吃饭',
    '小孩说爸爸放学后你可以接我吗？'
]
messages = [
    {"role": "system", "content": "你是一名情感分析师，帮我判断小孩喜欢爸爸，请用一个词语回复：喜欢或者不喜欢，并给出分析原因"},
    {"role": "user", "content": situations}
]
response = get_response(messages)
print(response.output.choices[0].message.content)
