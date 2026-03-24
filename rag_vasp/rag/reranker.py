from FlagEmbedding import FlagReranker
from rag_vasp.config.settings import settings

class Reranker:

    def __init__(self, top_k=5):
        from FlagEmbedding import FlagReranker
        self.model = FlagReranker(
            "cross-encoder/ms-marco-MiniLM-L2-v2",
            use_fp16=False
        )

    def rerank(self, query, docs, top_k = None):
        top_k = settings.reranker.top_k
        pairs = [[query, d["text"]] for d in docs]

        scores = self.model.compute_score(pairs)

        ranked = sorted(
            zip(scores, docs),
            key=lambda x: x[0],
            reverse=True
        )

        reranked_docs = []

        for score, doc in ranked[:top_k]:
            doc["rerank_score"] = float(score)  # 🔥 clave
            reranked_docs.append(doc)

        return reranked_docs