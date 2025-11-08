# 阿里千问大模型调用示例

这是一个使用 DashScope SDK 调用阿里千问大模型的基础示例程序。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 获取 DashScope API Key
   - 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
   - 创建 API Key

2. 设置 API Key
   - 方式一：设置环境变量
     ```bash
     export DASHSCOPE_API_KEY=your_api_key_here
     ```
   - 方式二：在代码中直接设置（不推荐，仅用于测试）
     ```python
     dashscope.api_key = "your_api_key_here"
     ```

3. 运行程序
   ```bash
   python main.py
   ```

## 代码说明

- `main.py`: 主程序文件，包含调用千问模型的函数
- `requirements.txt`: Python依赖包列表

## 模型说明

当前使用 `qwen_turbo` 模型，你也可以替换为其他千问模型：
- `qwen_turbo`: 快速版本
- `qwen_plus`: 增强版本
- `qwen_max`: 最强版本

