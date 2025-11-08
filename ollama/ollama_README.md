# 调用本地 Ollama DeepSeek 模型

## 📋 前置要求

### 1. 安装 Ollama

**macOS:**
```bash
brew install ollama
# 或下载安装包: https://ollama.ai/download
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
下载安装包: https://ollama.ai/download

### 2. 启动 Ollama 服务

```bash
ollama serve
```

### 3. 拉取 DeepSeek 模型

```bash
# 拉取 deepseek-chat 模型（推荐）
ollama pull deepseek-chat

# 或拉取 deepseek-r1 模型
ollama pull deepseek-r1
```

### 4. 安装 Python 依赖

```bash
pip install requests ollama
```

## 🚀 使用方法

### 方法 1: 使用 requests 直接调用 API（推荐用于学习）

```python
from ollama_deepseek import call_ollama_deepseek_simple

result = call_ollama_deepseek_simple("你好，介绍一下你自己")
print(result)
```

**优点:**
- 不依赖额外 SDK
- 代码清晰，易于理解
- 可以自定义请求

### 方法 2: 使用 Ollama Python SDK（推荐用于生产）

```python
from ollama_deepseek_sdk import call_deepseek, chat_deepseek

# 简单调用
result = call_deepseek("你好")

# 多轮对话
messages = [
    {"role": "user", "content": "我的名字是张三"}
]
response = chat_deepseek(messages)
```

**优点:**
- 官方 SDK，更稳定
- API 更简洁
- 支持流式输出

## 📝 代码示例

### 简单调用

```python
import ollama

response = ollama.generate(
    model="deepseek-chat",
    prompt="你好，介绍一下你自己"
)
print(response['response'])
```

### 多轮对话

```python
import ollama

messages = [
    {"role": "user", "content": "我的名字是张三"}
]

response = ollama.chat(
    model="deepseek-chat",
    messages=messages
)
print(response['message']['content'])

# 继续对话
messages.append({"role": "assistant", "content": response['message']['content']})
messages.append({"role": "user", "content": "我刚才说我叫什么？"})

response = ollama.chat(
    model="deepseek-chat",
    messages=messages
)
print(response['message']['content'])
```

### 流式输出

```python
import ollama

messages = [{"role": "user", "content": "写一首关于春天的诗"}]

stream = ollama.chat(
    model="deepseek-chat",
    messages=messages,
    stream=True
)

for chunk in stream:
    if chunk['message']['content']:
        print(chunk['message']['content'], end='', flush=True)
```

## 🔧 API 端点说明

Ollama 默认运行在 `http://localhost:11434`

### 主要 API 端点：

1. **生成文本**: `POST /api/generate`
   ```json
   {
     "model": "deepseek-chat",
     "prompt": "你好",
     "stream": false
   }
   ```

2. **对话**: `POST /api/chat`
   ```json
   {
     "model": "deepseek-chat",
     "messages": [
       {"role": "user", "content": "你好"}
     ],
     "stream": false
   }
   ```

3. **列出模型**: `GET /api/tags`

## 🆚 与 DashScope 的区别

| 特性 | Ollama (本地) | DashScope (云端) |
|------|--------------|------------------|
| 位置 | 本地运行 | 云端服务 |
| 费用 | 免费 | 按量付费 |
| 速度 | 取决于本地硬件 | 稳定快速 |
| 隐私 | 完全本地，数据不出本地 | 数据发送到云端 |
| 模型选择 | 需要手动拉取 | 直接可用 |
| API Key | 不需要 | 需要 |

## 🐛 常见问题

### 1. 连接错误

**错误**: `ConnectionError: 无法连接到 Ollama`

**解决**:
```bash
# 确保 Ollama 服务正在运行
ollama serve

# 或检查服务状态
curl http://localhost:11434/api/tags
```

### 2. 模型不存在

**错误**: `model 'deepseek-chat' not found`

**解决**:
```bash
# 拉取模型
ollama pull deepseek-chat

# 查看已安装的模型
ollama list
```

### 3. 内存不足

如果模型太大，可以：
- 使用较小的模型
- 增加系统内存
- 使用量化版本（如 deepseek-chat:7b）

## 📚 更多资源

- [Ollama 官方文档](https://github.com/ollama/ollama)
- [Ollama Python SDK](https://github.com/ollama/ollama-python)
- [可用模型列表](https://ollama.com/library)

