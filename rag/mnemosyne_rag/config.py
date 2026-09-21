from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
DEFAULT_OLLAMA_HOST = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2"


@dataclass(frozen=True)
class PalaceConfig:
    persist_dir: Path
    vault: str = "default"
    chunk_size: int = 900
    chunk_overlap: int = 140
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    ollama_host: str = DEFAULT_OLLAMA_HOST
    ollama_model: str = DEFAULT_OLLAMA_MODEL
    extra_metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "persist_dir", Path(self.persist_dir).expanduser().resolve())
        if not self.vault.strip():
            raise ValueError("vault name cannot be empty")
        if self.chunk_size < 200:
            raise ValueError("chunk_size must be at least 200 characters")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
