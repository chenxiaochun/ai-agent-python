import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate

load_dotenv()
 
llm = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True
)

example_template="输入：{input}\n输出：{output}"
examples=[
    {
        "input": "将你好翻译成英文",
        "output": "这是英文翻译结果：Hello"
    }
]

few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate.from_template(example_template),
    prefix="请将以下中文翻译成英文：",
    suffix="输入：{text}\n输出：",
    input_variables=["text"],
)

chain = few_shot_prompt_template | llm

resp = chain.stream(input={"text": "谢谢你"})

for chunk in resp:
    print(chunk.content, end="", flush=True)


