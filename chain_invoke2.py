import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # streaming=True,
)

prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一名专业翻译，请将后面的文字翻译成{language}"),
        ("user", "{text}"),
    ]
)

parser = StrOutputParser()
chain = prompt_template | model | parser

resp = chain.invoke({"text": "你好", "language": "韩文"})
print(resp)
