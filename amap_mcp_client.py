import os
import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


load_dotenv()

llm = ChatOpenAI(
    model_name="qwen3-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True,
)


# mcp url 前面为什么一定要加个“f”？如果去掉就会报错，不明白是为啥
async def create_amap_mcp_client():
    amap_key = os.getenv("AMAP_MCP_KEY")
    mcp_config = {
        "amap": {"url": f"https://mcp.amap.com/sse?key={amap_key}", "transport": "sse"}
    }

    client = MultiServerMCPClient(mcp_config)
    tools = await client.get_tools()
    print(tools)
    return client, tools


async def create_agent():
    client, tools = create_amap_mcp_client()

    agent = llm.bind_tools([tools])


asyncio.run(create_amap_mcp_client())
