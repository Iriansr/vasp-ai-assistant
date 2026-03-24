from langgraph.graph import StateGraph

from nodes.router_node import router_node
from nodes.rag_node import rag_node
from nodes.web_node import web_node
from nodes.validator_node import validator_node

from nodes.routing import router_decision, validation_route


# Define state as a dict (simple)
GraphState = dict


def build_graph():

    graph = StateGraph(GraphState)

    # =========================
    # NODES
    # =========================
    graph.add_node("router", router_node)
    graph.add_node("rag", rag_node)
    graph.add_node("web", web_node)
    graph.add_node("validator", validator_node)

    # =========================
    # ENTRY
    # =========================
    graph.set_entry_point("router")

    # =========================
    # ROUTER → TOOL
    # =========================
    graph.add_conditional_edges(
        "router",
        router_decision,
        {
            "rag": "rag",
            "web": "web",
        }
    )

    # =========================
    # TOOL → VALIDATOR
    # =========================
    graph.add_edge("rag", "validator")
    graph.add_edge("web", "validator")

    # =========================
    # VALIDATOR → NEXT STEP
    # =========================
    graph.add_conditional_edges(
        "validator",
        validation_route,
        {
            "__end__": "__end__",
            "web": "web",   # 🔥 fallback
        }
    )

    return graph.compile()