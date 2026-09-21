from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import uuid4

from mnemosyne_rag.chunking import split_text
from mnemosyne_rag.config import PalaceConfig
from mnemosyne_rag.embeddings import Embedder, create_embedder
from mnemosyne_rag.generate import GenerativeError, generate_with_ollama, ollama_available
from mnemosyne_rag.loaders import load_path
from mnemosyne_rag.store import ChromaMemoryStore
from mnemosyne_rag.synthesize import build_generative_prompt, synthesize_extractive
from mnemosyne_rag.types import Answer, IngestResult, SearchHit, VaultStats


class MemoryPalace:
    def __init__(self, config: PalaceConfig, embedder: Embedder | None = None) -> None:
        self.config = config
        self.embedder = embedder or create_embedder(config.embedding_model)
        self.store = ChromaMemoryStore(config.persist_dir, config.vault)

    def ingest_path(self, path: Path, document_id: str | None = None, title: str | None = None) -> IngestResult:
        loaded = load_path(path)
        return self.ingest_text(
            loaded.text,
            document_id=document_id or _document_id(loaded.source),
            source=loaded.source,
            title=title or loaded.title,
        )

    def ingest_text(
        self,
        text: str,
        *,
        document_id: str,
        source: str = "inline",
        title: str | None = None,
        extra_metadata: dict[str, str] | None = None,
    ) -> IngestResult:
        chunks = split_text(text, self.config.chunk_size, self.config.chunk_overlap)
        if not chunks:
            raise ValueError("Document is empty after normalization")

        ids = [f"{document_id}:{chunk.index}" for chunk in chunks]
        embeddings = self.embedder.embed([chunk.text for chunk in chunks])
        metadatas = []
        for chunk in chunks:
            meta = {
                "document_id": document_id,
                "source": source,
                "title": title or Path(source).stem or document_id,
                "chunk_index": chunk.index,
                "vault": self.config.vault,
            }
            meta.update(self.config.extra_metadata)
            if extra_metadata:
                meta.update(extra_metadata)
            metadatas.append(meta)

        self.store.delete_document(document_id)
        self.store.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=[chunk.text for chunk in chunks],
            metadatas=metadatas,
        )
        return IngestResult(
            document_id=document_id,
            source=source,
            chunks=len(chunks),
            characters=len(text),
        )

    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> list[SearchHit]:
        if not query.strip():
            raise ValueError("query cannot be empty")
        embedding = self.embedder.embed([query.strip()])[0]
        where = {"document_id": document_id} if document_id else None
        return self.store.query(embedding, top_k=max(1, top_k), where=where)

    def ask(self, question: str, *, top_k: int = 5, prefer_generative: bool = True) -> Answer:
        hits = self.search(question, top_k=top_k)
        if prefer_generative and hits and ollama_available(self.config.ollama_host):
            prompt = build_generative_prompt(question, hits)
            try:
                text = generate_with_ollama(
                    prompt,
                    host=self.config.ollama_host,
                    model=self.config.ollama_model,
                )
                return Answer(question=question, answer=text, citations=hits, mode="generative")
            except GenerativeError:
                pass
        return Answer(
            question=question,
            answer=synthesize_extractive(question, hits),
            citations=hits,
            mode="extractive",
        )

    def forget(self, document_id: str) -> None:
        self.store.delete_document(document_id)

    def stats(self) -> VaultStats:
        return self.store.stats()


def _document_id(source: str) -> str:
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:12]
    return f"doc-{digest}-{uuid4().hex[:6]}"
