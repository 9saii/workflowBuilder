from openai import OpenAI
from typing import Optional
import os
from utils import retry_openai_call

def call_llm(query: str, context: Optional[str] = None, prompt: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        # Return dummy response for testing
        return f"Dummy LLM response to: {query}"

    try:
        client = OpenAI(api_key=api_key)
        messages = []
        if prompt:
            messages.append({"role": "system", "content": prompt})
        if context:
            messages.append({"role": "user", "content": f"Context: {context}\nQuery: {query}"})
        else:
            messages.append({"role": "user", "content": query})

        def _call_chat_completion():
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content

        return retry_openai_call(_call_chat_completion)
    except Exception as e:
        # Return dummy response if API call fails (quota, network, etc.)
        print(f"OpenAI API error: {e}")
        return f"Dummy LLM response to: {query} (API unavailable)"
