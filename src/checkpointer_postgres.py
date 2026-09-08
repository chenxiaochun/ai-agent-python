from langgraph.checkpoint.postgres import PostgresSaver
from get_model import get_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

model = get_model()

checkpointer = InMemorySaver()
DB_URI = "postgresql://user:123456@localhost:5432/langgraph_db"

# PostgresSaver 不接受 url/table_name；用 from_conn_string 创建，并先 setup 建表
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

    agent = create_agent(
        model,
        checkpointer=checkpointer,
    )

    config = {"configurable": {"thread_id": 1}}

    res1 = agent.invoke({"messages": [{"role": "user", "content": "你好，我是小明"}]}, config)
    for msg in res1["messages"]:
        msg.pretty_print()

    res2 = agent.invoke({"messages": [{"role": "user", "content": "你知道我是谁吗？"}]}, config)
    for msg in res2["messages"]:
        msg.pretty_print()
