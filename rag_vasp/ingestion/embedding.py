from typing import List
from tqdm import tqdm
import vertexai
from vertexai.language_models import TextEmbeddingModel
from rag_vasp.config.settings import settings


class VertexEmbedder:

    def __init__(
        self,
        project_id: str = settings.vertex.project,
        location: str = settings.vertex.location,
        model_name: str = settings.vertex.embedding_model,
        batch_size: int = settings.vertex.batch_size,
    ):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=project_id, location=location)
        self.model = TextEmbeddingModel.from_pretrained(model_name)
        self.batch_size = batch_size

    def prepare_text(self, chunk):

        title = chunk["title"]
        section = chunk["section"]
        text = chunk["text"]

        return f"{title}. {section}. {text}"

    def embed_batch(self, texts):

        embeddings = self.model.get_embeddings(texts)

        return [e.values for e in embeddings]

    def embed_chunks(self, chunks):

        embedded_chunks = []

        for i in tqdm(range(0, len(chunks), self.batch_size)):

            batch = chunks[i:i + self.batch_size]

            texts = [self.prepare_text(c) for c in batch]

            vectors = self.embed_batch(texts)

            for chunk, emb in zip(batch, vectors):

                chunk["embedding"] = emb

                embedded_chunks.append(chunk)

        return embedded_chunks