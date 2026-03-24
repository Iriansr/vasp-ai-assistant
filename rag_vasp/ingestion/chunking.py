import uuid
import tiktoken


class SectionChunker:

    def __init__(
        self,
        chunk_size=350,
        overlap=80,
        model="text-embedding-3-large",
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.encoding_for_model(model)

    def token_len(self, text):

        return len(self.tokenizer.encode(text))

    def split_paragraphs(self, text):

        paragraphs = [
            p.strip()
            for p in text.split("\n")
            if p.strip()
        ]

        return paragraphs

    def chunk_paragraphs(self, paragraphs):

        chunks = []
        current = []

        for p in paragraphs:

            current.append(p)

            joined = "\n".join(current)

            if self.token_len(joined) > self.chunk_size:

                chunk = "\n".join(current[:-1])

                if chunk:
                    chunks.append(chunk)

                current = current[-1:]

        if current:
            chunks.append("\n".join(current))

        return chunks

    def chunk_document(self, doc):

        chunks = []

        title = doc["title"]
        url = doc["url"]

        doc_id = str(uuid.uuid4())

        for section in doc["sections"]:

            section_name = section["section"]
            content = section["content"]

            full_title = f"{title} - {section_name}"

            paragraphs = self.split_paragraphs(content)

            section_chunks = self.chunk_paragraphs(paragraphs)

            for chunk in section_chunks:

                chunks.append(
                    {
                        "chunk_id": str(uuid.uuid4()),
                        "doc_id": doc_id,
                        "title": title,
                        "section": section_name,
                        "full_title": full_title,
                        "text": f"{section_name}\n\n{chunk}",
                        "text_for_embedding": f"{title}. {section_name}. {chunk}",
                        "url": url,
                    }
                )

        return chunks

    def chunk_documents(self, docs):

        all_chunks = []

        for doc in docs:

            doc_chunks = self.chunk_document(doc)

            all_chunks.extend(doc_chunks)

        return all_chunks