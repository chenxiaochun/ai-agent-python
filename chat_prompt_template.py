import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
 
llm = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一位{role}专家，擅长回答{topic}相关问题"),
    ("user", "用户问题：{question}"),
])
prompt = prompt_template.format_messages(role="编程", topic="web开发", question="如何构建一个基于Vue的前端应用")

resp = llm.stream(prompt)

for chunk in resp:
    print(chunk.content, end="", flush=True)
