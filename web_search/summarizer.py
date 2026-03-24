from llm.vertex_llm import VertexLLM

class Summarizer:

    def __init__(self):
        self.llm = VertexLLM()

    def summarize(self, query, docs):

        context = "\n\n".join([
        f"[{i}] {d['title']}\n{d['content']}"
        for i, d in enumerate(docs)
        ])

        sources_text = "\n".join([
            f"[{i}] {d['title']} - {d['url']}"
            for i, d in enumerate(docs)
        ])

        prompt = f"""
        You are a senior condensed matter physicist.

        Your task is to answer the question using ONLY the provided sources.

        ---------------------
        RULES:
        - Use ONLY the information from the sources.
        - DO NOT use prior knowledge.
        - If relevant information is present, you MUST answer using it
        - Even if the answer is partial, provide the best possible explanation
        - Only say "I don't know" if absolutely no relevant information exists
        - Be precise, concise, and scientifically rigorous.
        - Explain concepts clearly when needed.
        - Prefer shorter answers unless detail is necessary
        - Think step by step internally, but ONLY output the final answer. Do NOT include intermediate reasoning or chain-of-thought in the output
        - If unsure, DO NOT guess. 
        - Prefer using fewer high-quality sources rather than many weak ones
        - Do NOT copy text verbatim from sources
        - Synthesize information into a coherent explanation
        - When relevant, include the defining equation or formula
        - Structure the answer as:
            1. Physical meaning
            2. Mathematical definition
            3. Interpretation of terms
        - Avoid repeating equivalent formulas unless they add new insight
        - Explain the physical meaning of the quantity, not only the formula

        CITATIONS:
        - You MUST cite sources using [number].
        - Each claim must be supported by a citation.
        - You can cite multiple sources like [0][2].

        ---------------------
        EXAMPLES:

        Example 1:
        Question: What determines surface energy in a slab?

        Sources:
        [0] Surface energy depends on broken bonds and slab thickness.
        [1] It can be computed from slab and bulk energies.

        Answer:
        Surface energy is determined by the energy cost of creating a surface, which is related to broken bonds and depends on slab thickness [0]. It is typically computed from the difference between slab and bulk energies [1].

        ---

        Example 2:
        Question: What is the work function?

        Sources:
        [0] The work function is defined as the difference between vacuum potential and Fermi level.

        Answer:
        The work function is defined as the difference between the vacuum potential and the Fermi level [0].

        ---
        Bad Example:
        Question: What determines surface energy?

        Sources:
        [0] Surface energy depends on broken bonds.

        Answer:
        Surface energy depends on atomic structure and quantum effects.

        This answer is incorrect because it introduces information not present in the sources.
        
        QUESTION:
        {query}

        ---------------------
        SOURCES:
        {context}

        ---------------------
        AVAILABLE REFERENCES:
        {sources_text}

        ---------------------

        OUTPUT FORMAT:

        Answer:
        <scientific answer with citations>

        Sources:
        [0] Title - short description
        [1] Title - short description
        """
        
        print("El contexto que he pasado es")
        print(context)
        answer = self.llm.generate(prompt)

        return answer  