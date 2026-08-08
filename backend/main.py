import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.services.pdf_ingest import ingest_pdfs
from backend.services.qa import answer_question, load_index

app = FastAPI(title="KenteCode AI Assistant")

class QueryRequest(BaseModel):
    question: str

@app.on_event("startup")
def startup_event():
    index_path = os.path.join(os.path.dirname(__file__), "data", "vector_index.npz")
    load_index(index_path)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest():
    try:
        docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
        docs_dir = os.path.abspath(docs_dir)
        ingest_pdfs(docs_dir)
        return {"status": "ingested", "docs_dir": docs_dir}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/query")
def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty")
    answer = answer_question(request.question)
    return answer
    