from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class IngestResult:
    document_id: str
    source: str
    chunks: int
    characters: int


@dataclass(frozen=True)
class SearchHit:
    document_id: str
    chunk_id: str
    text: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def title(self) -> str:
        return str(self.metadata.get("title") or self.metadata.get("source") or self.document_id)


@dataclass(frozen=True)
class Answer:
    question: str
    answer: str
    citations: list[SearchHit]
    mode: Literal["extractive", "generative"]


@dataclass(frozen=True)
class VaultStats:
    vault: str
    documents: int
    chunks: int
