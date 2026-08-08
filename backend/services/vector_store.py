import os
import json
import numpy as np
from typing import List, Dict, Optional
from backend.services.openai_client import get_embedding

INDEX_FILE = "vector_index.npz"

class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.metadata = []

    def add_document(self, text: str, metadata: Dict):
        embedding = get_embedding(text)
        self.embeddings.append(embedding)
        self.metadata.append(metadata)

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez_compressed(path, embeddings=np.array(self.embeddings), metadata=np.array(self.metadata, dtype=object))

    @staticmethod
    def load(path: str) -> "VectorStore":
        store = VectorStore()
        with np.load(path, allow_pickle=True) as data:
            store.embeddings = data["embeddings"].tolist()
            store.metadata = data["metadata"].tolist()
        return store

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = get_embedding(query)
        matrix = np.array(self.embeddings)
        if matrix.size == 0:
            return []
        norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(query_embedding)
        similarities = np.dot(matrix, query_embedding) / norms
        best_idxs = np.argsort(similarities)[-top_k:][::-1]
        results = []
        for idx in best_idxs:
            results.append({
                "score": float(similarities[idx]),
                "text": self.metadata[idx].get("text", ""),
                "metadata": self.metadata[idx],
            })
        return results
