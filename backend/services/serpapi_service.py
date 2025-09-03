import requests
import os

def perform_web_search(query: str) -> str:
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key or api_key == "your_serpapi_key_here":
        # Return dummy response for testing
        return f"Dummy web search result for: {query}"
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        # Extract top results
        organic_results = results.get('organic_results', [])
        if organic_results:
            return organic_results[0]['snippet']
    return "No results found."
