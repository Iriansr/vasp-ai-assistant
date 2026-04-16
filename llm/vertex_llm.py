import vertexai
from vertexai.generative_models import GenerativeModel

from rag_vasp.config.settings import settings

# The model used as llm for generating the answers, we use a flash version since 
# this is a research project and want small latency, you can try heavier models

class VertexLLM:

    def __init__(self):

        vertexai.init(
            project=settings.vertex.project,
            location=settings.vertex.location,
        )

        self.model = GenerativeModel(settings.vertex.generative_model)

    def generate(self, prompt):

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0,   
                "max_output_tokens": 4*2048,
            }
        )

        return response.text