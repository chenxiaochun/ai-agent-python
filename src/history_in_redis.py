from get_model import get_model
from langchain_redis import RedisChatMessageHistory

model = get_model()

history = RedisChatMessageHistory(
    session_id="test", redis_url="redis://localhost:6379/0"
)

history.add_user_message("你是谁？")
ai_message = model.invoke(history.messages)
print(ai_message.content)
history.add_user_message(ai_message.content)

history.add_user_message("请重复一次")
ai_message2 = model.invoke(history.messages)
print(ai_message2.content)
history.add_user_message(ai_message2.content)
