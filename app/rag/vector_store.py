
from dataclasses import dataclass
from typing import List

import faiss
import numpy as np

from .embedder import Embedder


@dataclass
class Document:
    id: int
    text: str


class VectorStore:
    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.index = None
        self.documents: List[Document] = []

    def build_index(self, texts: List[str]):
        self.documents = [Document(id=i, text=t) for i, t in enumerate(texts)]
        embeddings = self.embedder.encode(texts)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.ascontiguousarray(embeddings, dtype="float32"))

    def search(self, query: str, top_k: int = 5) -> List[Document]:
        if self.index is None or not self.documents:
            return []
        query_emb = self.embedder.encode([query]).astype("float32")
        distances, indices = self.index.search(query_emb, top_k)
        results: List[Document] = []
        for idx in indices[0]:
            if idx < 0 or idx >= len(self.documents):
                continue
            results.append(self.documents[idx])
        return results
