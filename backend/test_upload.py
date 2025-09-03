import requests
import os
import glob

url = "http://127.0.0.1:8000/documents/upload"

# Find PDF files dynamically
pdf_files = glob.glob("*.pdf") + glob.glob("../*.pdf") + glob.glob("../../*.pdf")

if not pdf_files:
    print("No PDF files found in current or parent directories")
    exit(1)

# Use the first PDF file found
file_path = pdf_files[0]
print(f"Using PDF file: {file_path}")

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/pdf")}
        response = requests.post(url, files=files)

    print("Status Code:", response.status_code)
    print("Response:", response.json())
