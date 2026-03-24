class Summarizer:

    def summarize(self, query, docs):

        context = "\n\n".join([
            f"[{i}] {d['text']}"
            for i, d in enumerate(docs)
            if d.get("text")
        ])

        few_shot = """
EXAMPLES:

Example 1:
Question: How is surface energy computed in slab DFT calculations?

Sources:
[0] Surface energy is computed as (E_slab - N E_bulk) / (2A).
[1] The factor 2 accounts for the two equivalent surfaces.

Answer:
Surface energy is computed from the excess energy of a slab relative to the bulk, normalized by the surface area. It is typically expressed as (E_slab - N E_bulk) / (2A), where the factor of 2 accounts for the two equivalent surfaces in the slab model [0][1].

---

Example 2:
Question: What is the physical meaning of surface energy?

Sources:
[0] Surface energy represents the energy required to create a surface.
[1] It arises from broken bonds and reduced coordination at the surface.

Answer:
Surface energy represents the energetic cost of creating a surface, which originates from broken bonds and reduced atomic coordination compared to the bulk [0][1].

---

Example 3:
Question: How is band structure computed in VASP?

Sources:
[0] Band structures are computed by performing a self-consistent calculation followed by a non-self-consistent calculation along high-symmetry k-points.
[1] The charge density is kept fixed during the second step.

Answer:
Band structures in VASP are obtained through a two-step procedure: first, a self-consistent calculation is performed to obtain the ground-state charge density. Then, a non-self-consistent calculation is carried out along high-symmetry k-points while keeping the charge density fixed [0][1].

---

Bad Example:
Question: What is surface energy?

Sources:
[0] Surface energy is the energy required to create a surface.

Answer:
Surface energy depends on many quantum effects and electronic structure.

This answer is incorrect because it introduces information not present in the sources.
"""

        prompt = f"""
You are a senior condensed matter physicist.

You are given multiple sources extracted from scientific documentation.

Your task:
- Answer the question with scientific rigor
- Extract and synthesize the relevant information
- Prefer physical interpretation over raw formulas when possible
- When asked for a procedure, extract the general way of proceeding, do not give case-sensitive details. 

STRICT RULES:
- Use ONLY the provided sources
- Do NOT hallucinate
- If partial info → explain limitations
- ALWAYS Cite sources and add links to the page if possible 

{few_shot}

QUESTION:
{query}

SOURCES:
{context}

OUTPUT FORMAT:

Answer:
<scientific answer with citations>

Sources:
[0] Title - short description
[1] Title - short description
"""

        return prompt