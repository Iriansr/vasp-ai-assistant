"""
Routing logic for LangGraph

Split decision logic from the rest of the system
"""

# =========================
# ROUTER (query → tool)
# =========================

def router_decision(state):
    """
    Which node we take after the router.
    Expects:
        state["route"] = "rag" | "web"
    """
    route = state.get("route", "web")

    # secure fallback 
    if route not in ["rag", "web"]:
        return "web"

    return route


# =========================
# VALIDATOR (answer quality)
# =========================

"""
def validation_route(state):

    validation = state.get("validation", {})

    # 🔍 debug opcional
    # print("VALIDATION:", validation)

    is_valid = validation.get("valid", False)
    score = validation.get("score", 0)
    issues = validation.get("issues", [])
    answer = state.get("answer", "")

    if answer and "i don't know" not in answer.lower():
        return "__end__"

    # ✅ caso ideal
    if is_valid and score >= 0.6:
        return "__end__"

    # 🔥 problemas críticos → fallback web
    if "hallucination" in issues:
        return "web"

    if "incorrect" in issues:
        return "web"

    if "missing_sources" in issues:
        return "web"

    # 🔥 baja confianza
    if score < 0.6:
        return "web"
    
    if validation.get("valid", False):
        return "__end__"


    # fallback final
    return "__end__"
"""

def validation_route(state):

    answer = state.get("answer", "")
    validation = state.get("validation", {})
    attempts = state.get("attepmts",0)

    print("VALIDATION ROUTE DEBUG")
    print("answer:", answer[:100])
    print("validation:", validation)

    # CASE 1: correct answer → FINISH
    if validation.get("valid", False):
        return "__end__"

    # CASE 2: it does not explicitly know → fallback web
    if "i don't know" in answer.lower():
        return "web"

    # CASE 3: bad quality → fallback
    if validation.get("score", 0) < 0.6:
        return "web"
    
    if attempts >= 2:
        return "__end__"

    return "__end__"


# =========================
# RETRY LOGIC
# =========================

def should_retry(state):
    """
    Optional hook for the future:
    decide if trying w/ another prompt
    """
    validation = state.get("validation", {})
    return validation.get("score", 0) < 0.4


# =========================
# DEBUG / TRACE
# =========================

def debug_state(state, label="STATE"):
    """
    Helper for debugging
    """
    print(f"\n--- {label} ---")
    for k, v in state.items():
        print(f"{k}: {str(v)[:200]}")