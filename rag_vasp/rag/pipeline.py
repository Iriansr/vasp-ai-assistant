from .retriever import HybridRetriever
from .reranker import Reranker
from .context_builder import ContextBuilder
from llm.vertex_llm import VertexLLM
from rag_vasp.rag.summarizer import Summarizer


class RAGPipeline:

    def __init__(
        self,
        retriever,
        context_builder,
        llm,
        summarizer,
        reranker = None
    ):

        self.retriever = retriever
        self.reranker = reranker
        self.context_builder = context_builder
        self.llm = llm 
        self.summarizer = summarizer
        self.reranker = reranker

    def deduplicate(self,docs):

        seen = set()
        unique_docs = []

        for d in docs:

            key = (d["title"], d["section"], d["text"][:100])

            if key not in seen:
                seen.add(key)
                unique_docs.append(d)

        return unique_docs
    
    def run(self, query):

        # 1. retrieve
        docs = self.retriever.retrieve(query)

        # 1.5 rerank 
        if self.reranker:
            docs = self.reranker.rerank(query,docs)

        # 2. build context
        context = self.context_builder.build(docs)

        # 3. build prompt
        prompt = self.summarizer.summarize(query, docs)

        # 4. generate
        answer = self.llm.generate(prompt)

        return {
            "query": query,
            "context": context,
            "sources": docs,
            "answer": answer,
        }
    
"""
    def run(self, query):

        docs = self.retriever.retrieve(query)

        #docs = self.reranker.rerank(query, docs)

        #docs = self.deduplicate(docs)

        context = self.context_builder.build(docs)

        return {
            "query": query,
            "context": context,
            "sources": docs,
        }
"""

