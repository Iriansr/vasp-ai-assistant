from elasticsearch import Elasticsearch
from rag_vasp.config.settings import settings

class HybridRetriever:

    def __init__(
        self,
        index_name="vasp_docs",
        host= settings.elastic.host,
        embedder=None,
        k=20
    ):

        self.client = Elasticsearch(host)
        self.index_name = index_name
        self.embedder = embedder
        self.k = settings.retriever.k

    def retrieve(self, query, k=20):

        k = k or self.k
        query_vector = self.embedder.embed_batch([query])[0]

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

        hits = response["hits"]["hits"]

        docs = []

        for h in hits:
            source = h["_source"]

            docs.append(
                {
                    "score": h["_score"],
                    "text": source["text"],
                    "title": source["title"],
                    "section": source["section"],
                    "url": source["url"],
                    "doc_id": source["doc_id"],
                }
            )

        return docs