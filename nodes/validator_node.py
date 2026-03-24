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
        return json.loads(text)
    except:
        # 🔥 fallback: regex para encontrar JSON
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
    state["attepts"] = state.get("attepts",0)

    sources_text = "\n".join([
        f"- {s.get('title', '')}"
        for s in sources
    ])

    prompt = f"""
You are a strict scientific answer evaluator.

Evaluate the answer based ONLY on the provided information.

---------------------
QUESTION:
{query}

---------------------
ANSWER:
{answer}

---------------------
SOURCES:
{sources_text}

---------------------
EVALUATION CRITERIA:

1. Grounding
2. Relevance
3. Scientific correctness

---------------------
OUTPUT FORMAT (STRICT):

Return ONLY a valid JSON object:

{{
  "valid": true or false,
  "score": float between 0 and 1,
  "issues": list of strings,
  "reason": short explanation
}}

---------------------
ISSUE TYPES:

- hallucination
- missing_sources
- irrelevant
- incorrect

---------------------
RULES:

- No text outside JSON
- Be strict
"""

    raw = llm.generate(prompt)
    state["attepts"] = state.get("attepts",0) +1
    parsed = extract_json(raw)

    # robust fallback 
    if parsed is None:
        parsed = {
            "valid": False,
            "score": 0.0,
            "issues": ["parse_error"],
            "reason": raw[:200]
        }

    return {
        **state,
        "validation": parsed,
        "is_valid": parsed.get("valid", False)
    }