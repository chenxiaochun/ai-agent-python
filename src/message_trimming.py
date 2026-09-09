from typing import Any

from get_model import get_model
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware.types import before_model
from langchain_core.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime

model = get_model()

# 只保留最近 N 条消息（含 user / ai）
MAX_MESSAGES = 2


@before_model
def message_trimming(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    messages = state["messages"]
    if len(messages) <= MAX_MESSAGES:
        return None
    # messages 使用 add_messages：直接返回子集不会删旧消息，需用 RemoveMessage
    return {
        "messages": [RemoveMessage(id=m.id) for m in messages[:-MAX_MESSAGES] if m.id is not None]
    }


agent = create_agent(model, middleware=[message_trimming], checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": 1}}

res1 = agent.invoke({"messages": [{"role": "user", "content": "你好，我是小明"}]}, config)
for msg in res1["messages"]:
    msg.pretty_print()

res2 = agent.invoke({"messages": [{"role": "user", "content": "你知道我是谁吗？"}]}, config)
for msg in res2["messages"]:
    msg.pretty_print()

res3 = agent.invoke({"messages": [{"role": "user", "content": "你叫我小红吧"}]}, config)
for msg in res3["messages"]:
    msg.pretty_print()

res4 = agent.invoke({"messages": [{"role": "user", "content": "你叫我什么？"}]}, config)
for msg in res4["messages"]:
    msg.pretty_print()
