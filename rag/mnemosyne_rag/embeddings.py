from __future__ import annotations

import hashlib
import re
from typing import Protocol

import numpy as np

_TOKEN = re.compile(r"[a-z0-9']+")
_MODEL_DIMENSIONS = {
    "BAAI/bge-small-en-v1.5": 384,
    "BAAI/bge-base-en-v1.5": 768,
}


class Embedder(Protocol):
    dimension: int

    def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class LexicalEmbedder:
    """Deterministic bag-of-words hashing. Used in tests and as a fallback."""

    def __init__(self, dimension: int = 256) -> None:
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            vector = np.zeros(self.dimension, dtype=np.float32)
            for token in _TOKEN.findall(text.lower()):
                digest = hashlib.sha256(token.encode("utf-8")).digest()
                index = int.from_bytes(digest[:4], "little") % self.dimension
                sign = 1.0 if digest[4] % 2 == 0 else -1.0
                vector[index] += sign
            norm = float(np.linalg.norm(vector)) or 1.0
            vectors.append((vector / norm).tolist())
        return vectors


class FastEmbedder:
    """Local ONNX embeddings. Model weights stay on disk after the first download."""

    def __init__(self, model_name: str) -> None:
        from fastembed import TextEmbedding

        self.model_name = model_name
        self._model = TextEmbedding(model_name=model_name)
        self.dimension = _MODEL_DIMENSIONS.get(model_name, 384)

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return [vector.tolist() for vector in self._model.embed(texts, batch_size=32)]


def create_embedder(model_name: str | None = None, *, lexical: bool = False) -> Embedder:
    if lexical or model_name == "lexical":
        return LexicalEmbedder()
    return FastEmbedder(model_name or "BAAI/bge-small-en-v1.5")
