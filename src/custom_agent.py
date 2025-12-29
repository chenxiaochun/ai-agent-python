import os
from dotenv import load_dotenv
from openai import OpenAI
from get_model import get_model
from langchain_core.tools import tool
from langchain.agents import create_agent

model = get_model()


@tool(description="获取某个城市的天气")
def get_weather(city: str):

    return "{city}的天气很好"


@tool(description="计算两个数字之和")
def add_number(a: int, b: int):
    return a + b + 2


agent = create_agent(
    model,
    system_prompt="你是我的私人助手，后面所有的问题都请使用工具进行获取",
    tools=[get_weather, add_number],
)

resp = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "北京的天气怎么样？"},
            {"role": "user", "content": "1+2=？"},
        ]
    }
)["messages"]

print(resp)
