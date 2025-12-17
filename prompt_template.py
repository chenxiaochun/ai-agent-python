import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()
 
llm = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True
)

prompt_template = PromptTemplate.from_template('今天{something}真不错')
prompt = prompt_template.format(something="天气")

resp = llm.stream(prompt)

for chunk in resp:
    print(chunk.content, end="", flush=True)
