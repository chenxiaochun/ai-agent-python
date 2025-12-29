import os
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()


def get_embedding_model():
    embedding_model = DashScopeEmbeddings(
        dashscope_api_key=os.getenv("sk-65fdf4deca47406ba50849e2c2efe909"),
        model="text-embedding-v4",
    )
    return embedding_model
