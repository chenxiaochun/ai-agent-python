# 长期记忆，语义搜索
from langgraph.store.base import embed
from langgraph.store.memory import InMemoryStore
from get_embedding_model import get_embedding_model
from get_model import get_model

get_model()

index_config = {"embed": get_embedding_model(), "dims": 1024, "fields": ["$", "course"]}

store = InMemoryStore(index=index_config)

namespace1 = ("users", "Alice", "memories")
key1 = "preferences"
value1 = {"language": "英语", "interests": ["AI", "编程"]}

namespace2 = ("users", "Bob", "memories")
key2 = "preferences"
value2 = {"language": "中文", "interests": ["AI", "机器学习"]}

namespace3 = ("users", "Charlie", "memories")
key3 = "preferences"
value3 = {"language": "西班牙语", "interests": ["AI", "绘画和雕塑"]}

store.put(namespace1, key1, value1)
store.put(namespace2, key2, value2)
store.put(namespace3, key3, value3)

for item in store.search(("users",), query="画画"):
    print(item)
