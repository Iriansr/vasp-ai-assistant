from pydantic import BaseModel
import os


class VertexConfig(BaseModel):
    project: str = os.getenv("VERTEX_PROJECT", "irian-sanchez-sandbox")
    location: str = os.getenv("VERTEX_LOCATION", "us-central1")
    batch_size: int = 32
    embedding_model: str = "text-embedding-004"
    generative_model: str = os.getenv("VERTEX_MODEL", "gemini-2.5-flash")


class RetrieverConfig(BaseModel):
    k: int = 20


class RerankerConfig(BaseModel):
    top_k: int = 10


class ElasticConfig(BaseModel):
    host: str = os.getenv("ES_HOST", "http://localhost:9200")
    index_name: str = "vasp_docs"


class Settings(BaseModel):
    vertex: VertexConfig = VertexConfig()
    retriever: RetrieverConfig = RetrieverConfig()
    reranker: RerankerConfig = RerankerConfig()
    elastic: ElasticConfig = ElasticConfig()


settings = Settings()