import sys
import os
sys.path.append('.')

from backend.models import SessionLocal, Workflow
import chromadb

# Test database connection
def test_db():
    db = SessionLocal()
    try:
        workflows = db.query(Workflow).all()
        print(f"Found {len(workflows)} workflows in database")
        for w in workflows:
            print(f"Workflow ID: {w.id}, Name: {w.name}")
        return len(workflows) > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        db.close()

# Test ChromaDB
def test_chromadb():
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="documents")
        count = collection.count()
        print(f"ChromaDB collection has {count} documents")
        return True
    except Exception as e:
        print(f"ChromaDB error: {e}")
        return False

if __name__ == "__main__":
    print("Testing database...")
    db_ok = test_db()
    print("Testing ChromaDB...")
    chroma_ok = test_chromadb()

    if not db_ok:
        print("Database issue detected")
    if not chroma_ok:
        print("ChromaDB issue detected")
    if db_ok and chroma_ok:
        print("All systems appear to be working")
