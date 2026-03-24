import os
import json

from rag_vasp.ingestion.loader import VaspWikiLoader
from rag_vasp.ingestion.chunking import SectionChunker
from rag_vasp.ingestion.embedding import VertexEmbedder
from rag_vasp.ingestion.vector_store import ElasticVectorStore
from rag_vasp.config.settings import settings
from bs4 import XMLParsedAsHTMLWarning 
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)




DATA_DIR = "data"
DOC_PATH = f"{DATA_DIR}/docs.jsonl"
CHUNK_PATH = f"{DATA_DIR}/chunks.jsonl"
EMB_PATH = f"{DATA_DIR}/embedded_chunks.jsonl"


def save_jsonl(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


def load_jsonl(path):
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data


def run_loader():

    if os.path.exists(DOC_PATH):
        print("Loading cached docs...")
        return load_jsonl(DOC_PATH)

    print("Running loader...")
    loader = VaspWikiLoader()
    docs = loader.load()

    save_jsonl(docs, DOC_PATH)

    return docs


def run_chunking(docs):

    if os.path.exists(CHUNK_PATH):
        print("Loading cached chunks...")
        return load_jsonl(CHUNK_PATH)

    print("Running chunking...")

    chunker = SectionChunker()
    chunks = chunker.chunk_documents(docs)

    save_jsonl(chunks, CHUNK_PATH)

    return chunks


def run_embeddings(chunks):

    if os.path.exists(EMB_PATH):
        print("Loading cached embeddings...")
        return load_jsonl(EMB_PATH)

    print("Running embeddings...")

    embedder = VertexEmbedder(
        project_id=settings.vertex.project
    )

    embedded_chunks = embedder.embed_chunks(chunks)

    save_jsonl(embedded_chunks, EMB_PATH)

    return embedded_chunks


def run_indexing(embedded_chunks):

    print("Indexing into Elasticsearch...")

    store = ElasticVectorStore()

    store.create_index()

    store.index_chunks(embedded_chunks)

    print("Indexing complete")


def main():

    docs = run_loader()

    chunks = run_chunking(docs)

    embedded_chunks = run_embeddings(chunks)

    run_indexing(embedded_chunks)

    print("Ingestion pipeline finished")


if __name__ == "__main__":
    main()