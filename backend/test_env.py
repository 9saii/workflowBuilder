import os
from dotenv import load_dotenv

load_dotenv()

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("SERPAPI_KEY:", os.getenv("SERPAPI_KEY"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
