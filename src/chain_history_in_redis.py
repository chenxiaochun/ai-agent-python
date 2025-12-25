from get_model import get_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_redis import RedisChatMessageHistory

model = get_model()

history = RedisChatMessageHistory(
    session_id="test", redis_url="redis://localhost:6379/0"
)

prompt_message = ChatPromptTemplate.from_messages([("user", "{text}")])

parser = StrOutputParser()

chain = prompt_message | model | parser

runnable = RunnableWithMessageHistory(chain, get_session_history=lambda: history)

history.clear()

runnable.invoke({"text": "你是谁？"})
print(runnable.invoke({"text": "请重复一次"}))
