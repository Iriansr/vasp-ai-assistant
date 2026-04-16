import json
import re
from llm.vertex_llm import VertexLLM

_validator = None


def get_validator():
    global _validator
    if _validator is None:
        _validator = VertexLLM()
    return _validator


def extract_json(text):
    """
    Extract JSON even if LLM infers noise 
    """
    try:
        # cleanup markdown blocks
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return None


def validator_node(state):

    llm = get_validator()

    query = state["query"]
    answer = state.get("answer", "")
    sources = state.get("sources", [])
    state["attempts"] = state.get("attempts", 0)

    sources_titles = [s.get('title', '') for s in sources]

    prompt = f"""Evaluate this scientific answer.
- Grounding: Is it supported by the sources?
- Relevance: Does it answer the question?
- Correctness: Is it scientifically sound?
- Appropriateness: Does it use RAG when asked about VASP?

QUESTION: {query}
ANSWER: {answer}
SOURCES: {", ".join(sources_titles)}

Return ONLY JSON:
{{"valid": bool, "score": float, "issues": [str], "reason": str}}
"""

    raw = llm.generate(prompt)
    state["attempts"] = state.get("attempts", 0) + 1
    parsed = extract_json(raw)

    if parsed is None:
        parsed = {
            "valid": True, # Assume valid if it's just a parse error to avoid loops
            "score": 0.5,
            "issues": ["parse_error"],
            "reason": "Could not parse validator output"
        }

    return {
        **state,
        "validation": parsed,
        "is_valid": parsed.get("valid", False)
    }