from pathlib import Path

import pytest

from mnemosyne_rag.config import PalaceConfig
from mnemosyne_rag.embeddings import LexicalEmbedder
from mnemosyne_rag.pipeline import MemoryPalace

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def palace(tmp_path: Path) -> MemoryPalace:
    return MemoryPalace(
        PalaceConfig(persist_dir=tmp_path / "palace", vault="mythos"),
        embedder=LexicalEmbedder(),
    )
