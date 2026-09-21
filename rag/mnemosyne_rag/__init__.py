"""Local RAG and semantic search for Mnemosyne."""

from mnemosyne_rag.config import PalaceConfig
from mnemosyne_rag.pipeline import MemoryPalace
from mnemosyne_rag.types import Answer, IngestResult, SearchHit, VaultStats

__all__ = [
    "Answer",
    "IngestResult",
    "MemoryPalace",
    "PalaceConfig",
    "SearchHit",
    "VaultStats",
]

__version__ = "0.1.0"
