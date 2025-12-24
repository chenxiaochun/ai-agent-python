import os

from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate

load_dotenv()


class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool(description="add tow numbers", args_schema=AddInputArgs)
def add(a, b):
    return a + b


def create_calc_tools():
    return [add]


calc_tools = create_calc_tools()


model = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # streaming=True,
)


# system_template_message = ChatMessagePromptTemplate.from_template(
#     template="你是一位{role}专家，擅长回答{topic}领域的问题", role="system"
# )

# user_template_message = ChatMessagePromptTemplate.from_template(
#     template="用户的问题：{question}", role="user"
# )

# chat_prompt_message = ChatPromptTemplate.from_messages(
#     [system_template_message, user_template_message]
# )

# messages = chat_prompt_message.format_messages(
#     role="计算", topic="使用工具进行数学计算", question="100+100=？"
# )

agent = create_agent(model, system_prompt="你是张三，你是我的助手")

resp = agent.invoke({"messages": [{"role": "user", "content": "你是谁？"}]})["messages"]

print(resp)
