import requests
import json

def test_save_workflow():
    url = "http://localhost:8000/workflows/save"
    workflow_data = {
        "graph": {
            "nodes": [
                {"id": "1", "type": "KnowledgeBase"},
                {"id": "2", "type": "LLM"},
                {"id": "3", "type": "WebSearch"}
            ],
            "edges": [
                {"from": "1", "to": "2"},
                {"from": "2", "to": "3"}
            ]
        }
    }
    response = requests.post(url, json=workflow_data)
    print("Save Workflow Status Code:", response.status_code)
    print("Save Workflow Response:", response.json())
    return response.json().get("workflow_id")

def test_run_workflow(workflow_id):
    url = "http://localhost:8000/workflows/run"
    params = {
        "workflow_id": workflow_id,
        "query": "What is the capital of France?"
    }
    response = requests.post(url, params=params)
    print("Run Workflow Status Code:", response.status_code)
    print("Run Workflow Response:", response.json())

if __name__ == "__main__":
    workflow_id = test_save_workflow()
    if workflow_id:
        test_run_workflow(workflow_id)
