from llm.vertex_llm import VertexLLM


class Router:

    def __init__(self):
        self.llm = VertexLLM()

    def route(self, query):

        prompt = f"""
        You are a strict routing system for a scientific assistant.

        Your task is to classify the user query into ONE of the following categories:

        - "rag": questions specifically about VASP, its documentation, or how to perform calculations using VASP
        - "web": general scientific questions or anything not directly tied to VASP usage

        ---------------------
        DEFINITION OF "rag":

        Select "rag" ONLY if the query is clearly about:
        - VASP-specific inputs, tags, or workflows (e.g., INCAR, KPOINTS, POSCAR)
        - How to run or interpret VASP calculations
        - Surface calculations, slabs, band structures, etc. IN THE CONTEXT OF VASP
        - Questions that can likely be answered using VASP documentation

        ---------------------
        DEFINITION OF "web":

        Select "web" if the query is:
        - General physics, chemistry, or materials science (even if it mentions DFT)
        - Conceptual questions (e.g., "what is surface energy")
        - Not explicitly tied to VASP usage or implementation
        - Broad scientific explanations

        ---------------------
        IMPORTANT RULES:

        - If the query is conceptual → "web"
        - If the query is about HOW TO DO something in VASP → "rag"
        - If unsure → default to "web"
        - Be conservative: only choose "rag" when clearly justified

        ---------------------
        EXAMPLES:

        Query: "How do I set ISMEAR in VASP?"
        Answer: rag

        Query: "What is surface energy?"
        Answer: web

        Query: "How to compute surface energy in VASP slab calculations?"
        Answer: rag

        Query: "What does the Fermi level represent?"
        Answer: web

        Query: "How to converge k-points in VASP?"
        Answer: rag

        Query: "What is DFT?"
        Answer: web

        ---------------------
        OUTPUT FORMAT:

        Return ONLY one word:
        rag
        or
        web

        ---------------------
        Query:
        {query}
        """
        response = self.llm.generate(prompt).strip().lower()

        if "rag" in response:
            return "rag"
        else:
            return "web"