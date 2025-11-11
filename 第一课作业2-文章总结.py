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


# 待总结的文章内容
article = """
人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，它试图理解智能的实质，
并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、
图像识别、自然语言处理和专家系统等。

人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。可以设想，未来人工智能带来的科技产品，
将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，
但能像人那样思考、也可能超过人的智能。

近年来，随着深度学习技术的发展，人工智能在图像识别、语音识别、自然语言处理等领域取得了突破性进展。
各大科技公司纷纷投入巨资研发AI技术，推动了整个行业的快速发展。
"""

messages = [
    {"role": "system", "content": "你是一名专业的文章总结助手。请对用户提供的文章进行总结，要求：1. 提取文章的核心观点和主要内容；2. 总结要简洁明了，控制在200字以内；3. 保持原文的关键信息;4. 输出为markdown格式"},
    {"role": "user", "content": article}
]

response = get_response(messages)
print("=" * 60)
print("文章总结结果：")
print("=" * 60)
print(response.output.choices[0].message.content)
