class ContextBuilder:

    def __init__(self, max_chunks=15):

        self.max_chunks = max_chunks

    def build(self, docs):

        context_blocks = []

        for d in docs[: self.max_chunks]:

            block = f"""
            SOURCE: {d["title"]} - {d["section"]}
            URL: {d["url"]}

            {d["text"]}
            """

            context_blocks.append(block)

        context = "\n\n---\n\n".join(context_blocks)

        return context