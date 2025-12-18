import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)

system_template_message = ChatMessagePromptTemplate.from_template(
    template="你是一位{role}专家，擅长回答{topic}相关问题", role="system"
)

user_template_message = ChatMessagePromptTemplate.from_template(
    template="用户问题：{question}", role="user"
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        system_template_message,
        user_template_message,
    ]
)
prompt = prompt_template.format_messages(
    role="编程", topic="web开发", question="你擅长什么？"
)
resp = llm.stream(prompt)

for chunk in resp:
    print(chunk.content, end="", flush=True)
