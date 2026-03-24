# rag_vasp/web/pipeline.py

from .search import WebSearch
from .summarizer import Summarizer


class WebAgentPipeline:

    def __init__(self):
        self.search = WebSearch()
        self.summarizer = Summarizer()

    def clean_text(self,text, max_chars=600):

        if not text:
            return ""

        # delete typical noise
        text = text.replace("[edit]", "")
        text = text.replace("\n\n", "\n")

        # optional: erase things like "Fig."
        text = text.replace("Fig.", "")

        # cut
        return text[:max_chars]

    def run(self, query):

        # 1. search (Tavily)
        results = self.search.search(query)

        # 2. filter noise 
        docs = []

        for r in results:
            raw = r.get("content", "")
            cleaned = self.clean_text(raw)

            if cleaned and len(cleaned) > 50:
                docs.append({
                    "title": r["title"],
                    "url": r["url"],
                    "content": cleaned
                })

        docs = docs[:5]

        # fallback if there is no useful info
        if not docs:
            return {
                "answer": "No relevant information found from web search.",
                "sources": []
            }

        # 3. summarize
        answer = self.summarizer.summarize(query, docs)

        return {
            "answer": answer,
            "sources": docs
        }