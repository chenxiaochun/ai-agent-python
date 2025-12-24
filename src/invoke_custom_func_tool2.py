import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool, tool
from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    ChatMessagePromptTemplate,
)
from pydantic import BaseModel, Field

load_dotenv()


class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool(description="add tow numbers", args_schema=AddInputArgs)
def add(a, b):
    return a + b


llm = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)

system_template_message = ChatMessagePromptTemplate.from_template(
    template="你是一位{role}专家，擅长回答{topic}领域的问题", role="system"
)

user_template_message = ChatMessagePromptTemplate.from_template(
    template="用户的问题：{question}", role="user"
)

chat_prompt_message = ChatPromptTemplate.from_messages(
    [system_template_message, user_template_message]
)

# 将函数转变为 langchain 可以理解的函数
# name 必须是全局唯一，不能重复
# add_tools = Tool.from_function(func=add, name="add", description="add two numbers")

# 将大模型和 tool 对象绑定
llm_with_tools = llm.bind_tools([add])
print(llm_with_tools)

chain = chat_prompt_message | llm_with_tools
resp = chain.invoke(input={"role": "计算", "topic": "数学", "question": "100+100=?"})

tool_dict = {"add": add}

# 大模型不会自动调用自定义函数工具，需要我们自己实现调用
for tool_calls in resp.tool_calls:
    func_args = tool_calls["args"]
    func_name = tool_calls["name"]

    tool_func = tool_dict[func_name]
    tool_content = tool_func.invoke(func_args)

    print(tool_content)
