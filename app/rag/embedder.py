
from typing import List

import torch
from sentence_transformers import SentenceTransformer

from ..config import settings


class Embedder:
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL_NAME):
        device = "cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=device)

    def encode(self, texts: List[str]):
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embeddings
