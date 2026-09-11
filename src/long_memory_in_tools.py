from langchain_core.messages import HumanMessage
from langchain.tools import ToolRuntime
from langchain_core.tools import tool
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent, AgentState
from typing_extensions import NotRequired

from get_model import get_model

store = InMemoryStore()


class CustomState(AgentState):
    user_id: NotRequired[str]


@tool
def save_user_info(name: str, runtime: ToolRuntime) -> str:
    """将用户信息保存到长期记忆"""
    namespace = ("users",)
    key = runtime.state["user_id"]
    value = {"name": name}
    store.put(namespace, key, value)
    return "saved"


# parse_docstring 为True时，会解析工具的docstring，并使用docstring中的参数和返回值来生成工具的输入和输出。
@tool(parse_docstring=True)
def get_user_info(runtime: ToolRuntime) -> str:
    """从长期记忆中获取用户信息"""
    namespace = ("users",)
    key = runtime.state["user_id"]
    item = store.get(namespace, key)
    return str(item.value) if item else "用户信息不存在"


agent = create_agent(
    model=get_model(),
    tools=[save_user_info, get_user_info],
    store=store,
    state_schema=CustomState,
    system_prompt="用户提及个人信息时，可以使用工具保存用户信息。如果用户询问用户信息时，可以尝试使用工具获取用户信息。",
)

print("=" * 80)

response1 = agent.invoke({"messages": HumanMessage(content="我的名字是张三"), "user_id": "123"})
for msg in response1["messages"]:
    msg.pretty_print()

print("=" * 80)
response2 = agent.invoke({"messages": HumanMessage(content="我的名字是什么？"), "user_id": "123"})
for msg in response2["messages"]:
    msg.pretty_print()
