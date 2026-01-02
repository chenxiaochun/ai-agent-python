import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载.env文件中的环境变量
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
    stream=True,
)
for chunk in completion:
    print(chunk.choices[0].delta.content, end="", flush=True)
