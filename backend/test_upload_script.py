import requests
import os

def test_upload_document():
    url = "http://127.0.0.1:8000/documents/upload"
    file_path = os.path.join(os.path.dirname(__file__), "..", "sample.pdf")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/pdf")}
        response = requests.post(url, files=files)

    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_upload_document()
