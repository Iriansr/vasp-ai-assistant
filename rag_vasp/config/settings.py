from pydantic import BaseModel
import os


class VertexConfig(BaseModel):
    project: str = os.getenv("VERTEX_PROJECT", "your-project")
    location: str = os.getenv("VERTEX_LOCATION", "us-central1")
    batch_size: int = 32
    model: str = "text-embedding-004"


class RetrieverConfig(BaseModel):
    k: int = 20


class RerankerConfig(BaseModel):
    top_k: int = 5


class ElasticConfig(BaseModel):
    host: str = os.getenv("ES_HOST", "http://127.0.0.1:9200")
    index_name: str = "vasp_docs"


class Settings(BaseModel):
    vertex: VertexConfig = VertexConfig()
    retriever: RetrieverConfig = RetrieverConfig()
    reranker: RerankerConfig = RerankerConfig()
    elastic: ElasticConfig = ElasticConfig()


settings = Settings()