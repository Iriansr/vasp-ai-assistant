from web_search.pipeline import WebAgentPipeline

# singleton (as in rag_node)
_web_agent = None


def web_node(state):

    global _web_agent

    if _web_agent is None:
        _web_agent = WebAgentPipeline()

    query = state["query"]

    result = _web_agent.run(query)
    print("ENTERING WEB MODE")

    return {
        **state,
        "answer": result["answer"],
        "sources": result["sources"],
        "source_type": "web"
        }