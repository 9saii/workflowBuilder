import os
from openai import OpenAI
from utils import retry_openai_call

def generate_embeddings(text: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        # Return dummy embeddings for testing
        return [0.1] * 3072  # Adjusted to 3072 dimensions to match ChromaDB collection

    try:
        client = OpenAI(api_key=api_key)

        def _create_embedding():
            response = client.embeddings.create(
                input=text,
                model="text-embedding-3-large"
            )
            return response.data[0].embedding

        return retry_openai_call(_create_embedding)
    except Exception as e:
        # Return dummy embeddings if API call fails (quota, network, etc.)
        print(f"OpenAI Embeddings API error: {e}")
        return [0.1] * 3072  # Return dummy embeddings
