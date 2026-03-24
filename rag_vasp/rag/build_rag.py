from .retriever import HybridRetriever
from .reranker import Reranker
from .context_builder import ContextBuilder
from .pipeline import RAGPipeline
from rag_vasp.ingestion.embedding import VertexEmbedder
from llm.vertex_llm import VertexLLM
from rag_vasp.rag.summarizer import Summarizer

from rag_vasp.config.settings import settings


def build_rag(
    retriever_k=None,
    rerank_k=None,
):

    embedder = VertexEmbedder()

    retriever = HybridRetriever(
        embedder=embedder,   # 🔥 clave
        k=retriever_k or settings.retriever.k
    )

    reranker = Reranker(
        top_k=rerank_k or settings.reranker.top_k
    )

    context_builder = ContextBuilder()

    llm = VertexLLM()
    summarizer = Summarizer()

    return RAGPipeline(
        retriever=retriever,
        context_builder=context_builder,
        llm=llm,
        summarizer=summarizer,
        reranker = reranker
    )
