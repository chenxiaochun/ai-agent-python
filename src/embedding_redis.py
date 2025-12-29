import redis
from get_model import get_model
from get_embedding_model import get_embedding_model
from langchain_redis import RedisConfig, RedisVectorStore

redis_url = "redis://localhost:6379"
texts = ["香蕉很长", "苹果很甜", "西瓜又大又圆"]

model = get_model()
embedding_model = get_embedding_model()

redis_client = redis.from_url(redis_url)

print(redis_client.ping())

config = RedisConfig(index_name="fruit", redis_url=redis_url)

vector_store = RedisVectorStore(embedding_model, config=config)
vector_store.add_texts(texts)
res = vector_store.similarity_search_with_score("又圆又大的水果是什么？", k=3)

for doc, score in res:
    print(f"{doc.page_content} - {score}")
