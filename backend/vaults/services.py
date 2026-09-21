from __future__ import annotations

from functools import lru_cache

from django.conf import settings

from mnemosyne_rag import MemoryPalace, PalaceConfig
from mnemosyne_rag.embeddings import Embedder, create_embedder


def get_embedder() -> Embedder:
    return _embedder()


@lru_cache(maxsize=1)
def _embedder() -> Embedder:
    if settings.MNEMOSYNE_LEXICAL:
        return create_embedder(lexical=True)
    return create_embedder(settings.MNEMOSYNE_EMBEDDING_MODEL)


def palace_for(vault_id: str) -> MemoryPalace:
    config = PalaceConfig(
        persist_dir=settings.MNEMOSYNE_INDEX_DIR,
        vault=str(vault_id),
        embedding_model=settings.MNEMOSYNE_EMBEDDING_MODEL,
        ollama_host=settings.OLLAMA_HOST,
        ollama_model=settings.OLLAMA_MODEL,
    )
    return MemoryPalace(config, embedder=get_embedder())


def reset_palace_cache() -> None:
    _embedder.cache_clear()
