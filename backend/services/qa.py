import os
import json
from typing import Dict, List
from backend.services.vector_store import VectorStore
from backend.services.openai_client import get_chat_response

store: VectorStore = None


def load_index(path: str):
    global store
    if os.path.exists(path):
        store = VectorStore.load(path)
    else:
        store = VectorStore()
    return store


def build_prompt(question: str, results: List[Dict]) -> str:
    source_lines = []
    for idx, item in enumerate(results, start=1):
        metadata = item["metadata"]
        source = metadata.get("source", "unknown")
        page = metadata.get("page", "?")
        text = metadata.get("text", "")
        source_lines.append(f"[{idx}] Source: {source}, page {page}\n{text}\n")

    context = "\n".join(source_lines)
    prompt = (
        "You are an AI assistant answering questions from KenteCode documentation. "
        "Answer using only the provided sources and cite them by source and page. "
        "If the answer is not contained in the sources, say you could not find it in the documentation.\n\n"
        "Sources:\n"
        f"{context}\n"
        "Question: "
        f"{question}\n\n"
        "Answer concisely and include citations like [source, page X]."
    )
    return prompt


def format_answer(answer: str, results: List[Dict]) -> Dict:
    citations = []
    seen = set()
    for item in results:
        metadata = item["metadata"]
        key = (metadata.get("source"), metadata.get("page"))
        if key not in seen:
            seen.add(key)
            citations.append({
                "source": key[0],
                "page": key[1],
            })
    return {
        "answer": answer,
        "citations": citations,
    }


def answer_question(question: str):
    global store
    if store is None:
        raise RuntimeError("Vector store not loaded")
    results = store.search(question, top_k=5)
    if not results:
        return {"answer": "I could not find an answer in the available KenteCode documentation.", "citations": []}
    prompt = build_prompt(question, results)
    answer = get_chat_response(prompt)
    return format_answer(answer, results)
