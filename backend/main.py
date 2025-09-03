from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
import fitz  # PyMuPDF
import os
import uuid
import json
from sqlalchemy.orm import Session
from models import SessionLocal, Document, Workflow
import chromadb
from services.embedding_service import generate_embeddings
from services.llm_service import call_llm
from services.serpapi_service import perform_web_search
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust as needed for frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ChromaDB setup
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents", embedding_function=None)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class WorkflowSchema(BaseModel):
    name: str
    description: str = ""
    graph: Dict[str, Any]

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    contents = await file.read()
    text = ""
    if file.filename.endswith('.pdf'):
        # Extract text from PDF using PyMuPDF
        doc = fitz.open(stream=contents, filetype="pdf")
        for page in doc:
            text += page.get_text()
    else:
        text = contents.decode('utf-8')

    # Generate embeddings
    embeddings = generate_embeddings(text)

    # Store text and embeddings in ChromaDB
    doc_id = str(uuid.uuid4())
    collection.add(
        documents=[text],
        embeddings=[embeddings],
        ids=[doc_id]
    )

    # Store document metadata in PostgreSQL
    doc_entry = Document(filename=file.filename, content=text)
    db.add(doc_entry)
    db.commit()
    db.refresh(doc_entry)

    return JSONResponse(content={"message": "Document uploaded and processed successfully.", "document_id": doc_entry.id})

@app.post("/workflows/save")
async def save_workflow(workflow: WorkflowSchema, db: Session = Depends(get_db)):
    graph = workflow.graph
    name = workflow.name
    description = workflow.description
    # TODO: Validate graph (single start and end node)

    workflow_entry = Workflow(name=name, description=description, graph=json.dumps(graph))
    db.add(workflow_entry)
    db.commit()
    db.refresh(workflow_entry)

    return JSONResponse(content={"message": "Workflow saved successfully.", "workflow_id": workflow_entry.id})

@app.get("/workflows")
async def get_workflows(db: Session = Depends(get_db)):
    workflows = db.query(Workflow).all()
    return JSONResponse(content={"workflows": [{"id": w.id, "name": w.name, "description": w.description, "created_at": w.created_at.isoformat()} for w in workflows]})

@app.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return JSONResponse(content={"id": workflow.id, "name": workflow.name, "description": workflow.description, "graph": workflow.graph, "created_at": workflow.created_at.isoformat()})

@app.put("/workflows/{workflow_id}")
async def update_workflow(workflow_id: int, workflow: WorkflowSchema, db: Session = Depends(get_db)):
    existing_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not existing_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    existing_workflow.name = workflow.name
    existing_workflow.description = workflow.description
    existing_workflow.graph = json.dumps(workflow.graph)
    db.commit()
    db.refresh(existing_workflow)

    return JSONResponse(content={"message": "Workflow updated successfully.", "workflow_id": existing_workflow.id})

@app.post("/workflows/run")
async def run_workflow(workflow_id: int, query: str, db: Session = Depends(get_db)):
    # Retrieve workflow graph from DB
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    graph = json.loads(workflow.graph)
    # TODO: Parse connections and execute components in order

    # For now, assume a simple chain: KnowledgeBase -> LLM -> Web Search if needed
    # This is a placeholder implementation

    # KnowledgeBase: Query ChromaDB
    # Generate embedding for query to match collection embedding dimension
    query_embedding = generate_embeddings(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    context = " ".join(results['documents'][0]) if results['documents'] and results['documents'][0] else ""

    # LLM: Call with context
    response = call_llm(query, context)

    # If web search is enabled, perform search
    # TODO: Check graph for web search component

    return JSONResponse(content={"response": response})
