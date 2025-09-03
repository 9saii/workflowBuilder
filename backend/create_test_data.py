import sys
import os
sys.path.append('.')

from models import SessionLocal, Workflow, Document
import json
import chromadb
from services.embedding_service import generate_embeddings
import uuid

# Create a test workflow
def create_test_workflow():
    db = SessionLocal()
    try:
        # Create a simple workflow graph
        graph = {
            "nodes": [
                {"id": "1", "type": "knowledgeBase", "position": {"x": 100, "y": 100}},
                {"id": "2", "type": "llm", "position": {"x": 300, "y": 100}},
                {"id": "3", "type": "webSearch", "position": {"x": 500, "y": 100}}
            ],
            "edges": [
                {"id": "e1-2", "source": "1", "target": "2"},
                {"id": "e2-3", "source": "2", "target": "3"}
            ]
        }

        workflow = Workflow(name="Test Workflow", graph=json.dumps(graph))
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        print(f"Created test workflow with ID: {workflow.id}")
        return workflow.id
    except Exception as e:
        print(f"Error creating workflow: {e}")
        db.rollback()
        return None
    finally:
        db.close()

# Create a test document
def create_test_document():
    db = SessionLocal()
    try:
        test_content = """
        This is a test document for the workflow system.
        It contains information about artificial intelligence and machine learning.
        The system can use this document to provide context for user queries.
        """

        doc = Document(filename="test_document.txt", content=test_content)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        print(f"Created test document with ID: {doc.id}")

        # Add to ChromaDB
        try:
            client = chromadb.PersistentClient(path="./chroma_db")
            collection = client.get_or_create_collection(name="documents")
            embeddings = generate_embeddings(test_content)
            doc_id = str(uuid.uuid4())
            collection.add(
                documents=[test_content],
                embeddings=[embeddings],
                ids=[doc_id]
            )
            print(f"Added document to ChromaDB with ID: {doc_id}")
        except Exception as e:
            print(f"Error adding to ChromaDB: {e}")

        return doc.id
    except Exception as e:
        print(f"Error creating document: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating test data...")
    workflow_id = create_test_workflow()
    doc_id = create_test_document()

    if workflow_id and doc_id:
        print("Test data created successfully!")
        print(f"Workflow ID: {workflow_id}")
        print(f"Document ID: {doc_id}")
    else:
        print("Failed to create test data")
