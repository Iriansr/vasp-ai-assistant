from .router import Router

_router = None


def router_node(state):

    global _router

    if _router is None:
        _router = Router()

    query = state["query"]

    route = _router.route(query)

    return {
        **state,   
        "route": route
    }