# Full-Stack Workflow Builder

This is a full-stack application for building and executing custom workflows using AI components.

## Architecture

- **Backend**: FastAPI with PostgreSQL and ChromaDB
- **Frontend**: React with React Flow
- **Components**: KnowledgeBase, LLM Engine, Web Search

## Setup

1. Clone the repository
2. Run `docker-compose up --build`
3. Access frontend at http://localhost:3000
4. Backend API at http://localhost:8000

## Usage

1. Drag components from the library to the canvas
2. Connect them to create a workflow
3. Configure each component
4. Save the workflow
5. Chat with the workflow

## API Endpoints

- POST /documents/upload: Upload documents
- POST /workflows/save: Save workflow
- POST /workflows/run: Execute workflow
