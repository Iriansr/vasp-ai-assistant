# rag_vasp/web/search.py

from tavily import TavilyClient

TAVILY_API_KEY = "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"

class WebSearch:

    def __init__(self):
        self.client = TavilyClient(TAVILY_API_KEY)

    def search(self, query, k=5):

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=k
        )

        results = []

        for r in response["results"]:
            results.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content"),  
            })

        return results