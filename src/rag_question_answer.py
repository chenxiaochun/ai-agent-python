from get_model import get_model
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from get_embedding_model import get_embedding_model
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_core.prompts import ChatPromptTemplate


model = get_model()
embedding_model = get_embedding_model()

# 加载文档
loader = TextLoader(
    "/Users/chenxiaochun/Documents/MyProject/ai-agent-python/docs/tiao_sheng.txt"
)
documents = loader.load()


# 拆分文档
text_splitter = CharacterTextSplitter(
    chunk_size=200, chunk_overlap=0, separator=f"\n", keep_separator=True
)
segments = text_splitter.split_documents(documents)
# segment_documents = text_splitter.create_documents(segments[0].page_content)

redis_url = "redis://localhost:6379"
config = RedisConfig(index_name="tiao_sheng", redis_url=redis_url)

# 文档向量化
vector_store = RedisVectorStore(embedding_model, config=config)
vector_store.add_documents(segments)

query = "跳长绳"

retriever = vector_store.as_retriever()
retrieve_segments = retriever.invoke(query, k=10)

text = []
for doc in retrieve_segments:
    text.append(doc.page_content)

# print(text)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            """你是一个答疑机器人，请按照已知信息回答问题。已知信息：{context}。用户问题：{question}。如果已知信息中不包含用户问题的答案，请直接回答我不知道""",
        )
    ]
)

prompt = prompt_template.invoke({"context": text, "question": "我要出去玩儿什么？"})
# print(prompt.to_string())

resp = model.invoke(prompt)
print(resp.content)

# for segment in retrieve_segments:
#     print(segment.page_content)
#     print("-------")
