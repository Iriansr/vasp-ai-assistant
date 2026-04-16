from rag_vasp.rag.build_rag import build_rag
from web_search.pipeline import WebAgentPipeline

# Singletons for performance
_rag = None
_web_agent = None

def get_rag():
    global _rag
    if _rag is None:
        _rag = build_rag()
    return _rag

def get_web_agent():
    global _web_agent
    if _web_agent is None:
        _web_agent = WebAgentPipeline()
    return _web_agent

def vasp_retrieval_tool(query: str) -> dict:
    """
    Search specifically in VASP documentation for technical answers about simulation parameters,
    tags (INCAR, KPOINTS, etc.), and VASP workflows.
    
    Args:
        query: The technical question about VASP.
    
    Returns:
        A dictionary containing the answer, context, and sources.
    """
    rag = get_rag()
    result = rag.run(query)
    return {
        "answer": result.get("answer"),
        "context": result.get("context"),
        "sources": result.get("sources"),
        "source_type": "rag"
    }

def web_search_tool(query: str) -> dict:
    """
    Perform a general scientific web search to answer conceptual questions or broad topics
    not specifically covered in VASP documentation.
    
    Args:
        query: The scientific question to search on the web.
        
    Returns:
        A dictionary containing the answer and web sources.
    """
    web_agent = get_web_agent()
    result = web_agent.run(query)
    return {
        "answer": result.get("answer"),
        "sources": result.get("sources"),
        "source_type": "web"
    }
