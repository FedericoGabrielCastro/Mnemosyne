from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection

from mnemosyne_rag.types import SearchHit, VaultStats


class ChromaMemoryStore:
    def __init__(self, persist_dir: Path, vault: str) -> None:
        persist_dir.mkdir(parents=True, exist_ok=True)
        self.vault = vault
        self._client = chromadb.PersistentClient(path=str(persist_dir))
        self._collection: Collection = self._client.get_or_create_collection(
            name=_safe_name(vault),
            metadata={"hnsw:space": "cosine", "vault": vault},
        )

    def upsert(
        self,
        *,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        if not ids:
            return
        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(
        self,
        embedding: list[float],
        top_k: int,
        where: dict[str, Any] | None = None,
    ) -> list[SearchHit]:
        count = self._collection.count()
        if count == 0:
            return []
        kwargs: dict[str, Any] = {
            "query_embeddings": [embedding],
            "n_results": min(top_k, count),
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where
        result = self._collection.query(**kwargs)
        hits: list[SearchHit] = []
        ids = (result.get("ids") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]
        for chunk_id, text, metadata, distance in zip(ids, docs, metas, distances):
            score = max(0.0, 1.0 - float(distance))
            payload = dict(metadata or {})
            hits.append(
                SearchHit(
                    document_id=str(payload.get("document_id", "")),
                    chunk_id=str(chunk_id),
                    text=text or "",
                    score=round(score, 4),
                    metadata=payload,
                )
            )
        return hits

    def delete_document(self, document_id: str) -> None:
        self._collection.delete(where={"document_id": document_id})

    def stats(self) -> VaultStats:
        records = self._collection.get(include=["metadatas"])
        metadatas = records.get("metadatas") or []
        document_ids = {str(meta.get("document_id")) for meta in metadatas if meta}
        return VaultStats(vault=self.vault, documents=len(document_ids), chunks=len(metadatas))


def _safe_name(vault: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in vault.lower())
    return cleaned.strip("-")[:60] or "default"
