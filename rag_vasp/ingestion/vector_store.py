from elasticsearch import Elasticsearch
from typing import List
from tqdm import tqdm
from rag_vasp.config.settings import settings


class ElasticVectorStore:

    def __init__(
        self,
        hosts=None,
        index_name=None,
        embedding_dim=768,
    ):
        
        self.hosts = hosts or settings.elastic.host
        self.index_name = index_name or settings.elastic.index_name
        self.embedding_dim = embedding_dim
        
        self.client = Elasticsearch(self.hosts)
        self.connect()

    def connect(self):

        if not self.client.ping():
            raise RuntimeError(
                "Elasticsearch is not running on localhost:9200"
            )

        print("Connected to Elasticsearch")

    def create_index(self):

        if self.client.indices.exists(index=self.index_name):
            print("Index already exists")
            return

        mapping = {
            "mappings": {
                "properties": {

                    "chunk_id": {"type": "keyword"},
                    "doc_id": {"type": "keyword"},

                    "title": {
                        "type": "text"
                    },

                    "section": {
                        "type": "text"
                    },

                    "full_title": {
                        "type": "text"
                    },

                    "text": {
                        "type": "text"
                    },

                    "url": {
                        "type": "keyword"
                    },

                    "embedding": {
                        "type": "dense_vector",
                        "dims": self.embedding_dim,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }

        self.client.indices.create(
            index=self.index_name,
            body=mapping
        )

        print("Index created")

    def index_chunks(self, chunks):

        for chunk in tqdm(chunks):

            doc = {
                "chunk_id": chunk["chunk_id"],
                "doc_id": chunk["doc_id"],
                "title": chunk["title"],
                "section": chunk["section"],
                "full_title": chunk["full_title"],
                "text": chunk["text"],
                "url": chunk["url"],
                "embedding": chunk["embedding"],
            }

            self.client.index(
                index=self.index_name,
                id=chunk["chunk_id"],
                document=doc
            )

    def hybrid_search(self, query, query_vector, k=10):

        response = self.client.search(
            index=self.index_name,
            size=k,
            query={
                "script_score": {
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "title^3",
                                "section^2",
                                "full_title^2",
                                "text"
                            ]
                        }
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {
                            "query_vector": query_vector
                        }
                    }
                }
            }
        )

        return response["hits"]["hits"]