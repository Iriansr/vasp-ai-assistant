from rag_vasp.rag.build_rag import build_rag

# singleton - do not rebuild each time 
_rag = None

def get_rag():
    global _rag
    if _rag is None:
        _rag = build_rag()
    return _rag


def rag_node(state: dict) -> dict:
    """
    state esperado:
    {
        "query": str
    }
    """

    rag = get_rag()

    query = state["query"]

    result = rag.run(query)

    print("RETRIEVED DOCS:")
    for d in result["sources"]:
        print(d["title"], "-", d["section"])

    return {
        **state,
        "context": result["context"],
        "sources": result["sources"],
        "answer": result.get("answer"),   
        "source_type": "rag"
    }