"""
LiteLLM SDK 测试：通过 DashScope 调用 qwen3.7-plus
"""

import os
from dotenv import load_dotenv
import litellm

# 加载 .env 文件
load_dotenv()

# 从环境变量读取配置
api_key = os.getenv("DASHSCOPE_API_KEY")
base_url = os.getenv("DASHSCOPE_BASE_URL")

if not api_key or not base_url:
    raise RuntimeError("DASHSCOPE_API_KEY 或 DASHSCOPE_BASE_URL 未在 .env 中设置")

print(f"API Base: {base_url}")
print(f"API Key: {api_key[:20]}...")
print("-" * 50)

# 方式一：直接调用
print("\n[测试1] litellm.completion — 简单对话")
response = litellm.completion(
    model="openai/qwen3.7-plus",
    messages=[
        {"role": "user", "content": "你好，请用一句话介绍你自己"}
    ],
    api_key=api_key,
    api_base=base_url,
)

print(f"模型: {response.model}")
print(f"回复: {response.choices[0].message.content}")
print(f"Token 用量: {response.usage}")

# 方式二：带系统提示
print("\n" + "-" * 50)
print("\n[测试2] 带 system prompt 的多轮对话")
response = litellm.completion(
    model="openai/qwen3.7-plus",
    messages=[
        {"role": "system", "content": "你是一个 Python 编程专家，回答要简洁。"},
        {"role": "user", "content": "Python 中如何读取 .env 文件？一句话回答。"}
    ],
    api_key=api_key,
    api_base=base_url,
)

print(f"回复: {response.choices[0].message.content}")
print(f"Token 用量: {response.usage}")

# 方式三：流式调用
print("\n" + "-" * 50)
print("\n[测试3] 流式输出")
response = litellm.completion(
    model="openai/qwen3.7-plus",
    messages=[
        {"role": "user", "content": "写一首关于编程的五言绝句"}
    ],
    api_key=api_key,
    api_base=base_url,
    stream=True,
)

print("回复: ", end="", flush=True)
for chunk in response:
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content, end="", flush=True)
print()

print("\n" + "=" * 50)
print("[OK] 所有测试通过！LiteLLM + DashScope + qwen3.7-plus 工作正常")
