from get_model import get_model
from langchain_core.chat_history import InMemoryChatMessageHistory

model = get_model()

history = InMemoryChatMessageHistory()

history.add_user_message("你是谁？")
ai_message = model.invoke(history.messages)
print(ai_message.content)
history.add_user_message(ai_message.content)

history.add_user_message("请重复一次")
ai_message2 = model.invoke(history.messages)
print(ai_message2.content)
history.add_user_message(ai_message2.content)
