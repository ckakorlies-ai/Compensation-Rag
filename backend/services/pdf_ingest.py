import os
import fitz
import json
import numpy as np
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.services.vector_store import VectorStore

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100


def split_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_text(text)


def extract_pdf_text(pdf_path: str):
    with fitz.open(pdf_path) as doc:
        for page_index in range(len(doc)):
            page = doc[page_index]
            text = page.get_text()
            if text.strip():
                yield page_index + 1, text


def ingest_pdfs(docs_dir: str):
    if not os.path.isdir(docs_dir):
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    store = VectorStore()
    metadata = []

    for filename in os.listdir(docs_dir):
        if not filename.lower().endswith(".pdf"):
            continue
        pdf_path = os.path.join(docs_dir, filename)
        for page_number, text in extract_pdf_text(pdf_path):
            for chunk in split_text(text):
                store.add_document(
                    chunk,
                    {
                        "source": filename,
                        "page": page_number,
                        "text": chunk,
                    },
                )

    index_path = os.path.join(os.path.dirname(__file__), "..", "data", "vector_index.npz")
    store.save(index_path)
    return {"status": "indexed", "index_path": index_path}
