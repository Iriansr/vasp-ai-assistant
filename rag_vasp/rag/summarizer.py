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
[1] The factor 2 accounts for the two equivalent surfaces in symmetric slabs.
[2] N is the number of bulk units in the slab, and E_bulk is the energy per bulk unit.

Answer:
In Density Functional Theory (DFT) calculations using the slab model, the surface energy (γ) is typically computed by taking the difference between the total energy of the slab and the energy of a corresponding amount of bulk material. The general formula is:

γ = (E_slab - N * E_bulk) / (2A)

where:
- E_slab is the total energy of the slab calculation [0].
- N is the number of bulk formula units contained within the slab [2].
- E_bulk is the energy per formula unit of the bulk material [2].
- A is the surface area of one side of the slab [0].

The factor of 2 in the denominator accounts for the fact that a standard slab model has two equivalent surfaces (top and bottom) [1]. It is crucial that the slab is thick enough to reach bulk-like behavior in the center and that sufficient vacuum is included to avoid interactions between periodic images [0][1][2].

---

Example 2:
Question: What is the physical meaning of surface energy and what affects its value?

Sources:
[0] Surface energy represents the energy required to create a surface by breaking bonds.
[1] It arises from reduced coordination at the surface.
[2] Surface energy depends on the Miller indices (hkl) of the surface.

Answer:
Surface energy represents the excess energy associated with the creation of a physical surface, essentially the energetic cost of "breaking" bonds in the bulk to form a new interface [0]. 

From an atomic perspective, atoms at the surface have a lower coordination number (fewer neighbors) than atoms in the bulk [1]. This reduced coordination leads to unsaturated bonds, which are energetically unfavorable, hence the positive value of surface energy.

The value of surface energy is highly dependent on the crystallographic orientation of the surface, defined by its Miller indices (hkl). Different planes have different atomic densities and numbers of broken bonds; typically, close-packed surfaces (like (111) in FCC) have lower surface energies because fewer bonds are broken [0][2].

---

Example 3:
Question: How is band structure computed in VASP?

Sources:
[0] Band structures are computed by performing a self-consistent calculation followed by a non-self-consistent calculation along high-symmetry k-points.
[1] The charge density is kept fixed during the second step (ICHARG=11).
[2] The k-points for the second step are specified in the KPOINTS file, usually along a high-symmetry path.

Answer:
Computing a band structure in VASP is typically a two-step process:

1. **Self-Consistent Field (SCF) Calculation**: First, a standard ground-state calculation is performed to obtain the converged electronic charge density. This step uses a regular k-point grid to sample the Brillouin zone accurately [0].

2. **Non-Self-Consistent (Non-SCF) Calculation**: Once the charge density is obtained, a second calculation is run. In this step, the charge density from the first step is kept fixed (typically by setting `ICHARG=11` in the INCAR file) [1]. Instead of a regular grid, the k-points are chosen along high-symmetry lines in the Brillouin zone, as specified in the KPOINTS file [2]. This allows for the calculation of eigenvalues along specific paths to visualize the energy bands [0][1][2].

"""

        prompt = f"""
You are an expert senior condensed matter physicist specializing in VASP and DFT simulations.

Your task:
- Provide a comprehensive, detailed, and scientifically rigorous answer to the user's question.
- Synthesize information from all provided sources to give a complete picture.
- Explain the physical principles behind the formulas or procedures.
- When describing a procedure, include important details, flags (if mentioned), and common pitfalls or requirements (like convergence).
- Structure your answer clearly using headings or bullet points where appropriate for readability.

STRICT RULES:
- Use ONLY the provided sources. Do not introduce outside knowledge unless it is common physical knowledge that bridges the provided information.
- If the sources do not contain enough information to give a full answer, state clearly what is missing.
- Do NOT hallucinate.
- ALWAYS cite sources using [i] notation and provide a reference list at the end.

{few_shot}

QUESTION:
{query}

SOURCES:
{context}

OUTPUT FORMAT:

Answer:
<detailed scientific answer with citations>

Sources:
[0] Title - short description
[1] Title - short description
"""

        return prompt