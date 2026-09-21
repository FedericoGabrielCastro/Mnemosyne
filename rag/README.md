# Mnemosyne RAG

Local retrieval-augmented generation and semantic search. Documents are chunked, embedded on-device, and stored in ChromaDB. Nothing leaves the machine unless you opt into an optional Ollama generator.

## Install

```bash
cd rag
poetry install
```

The first production ingest downloads `BAAI/bge-small-en-v1.5` as a local ONNX model via FastEmbed. Tests use a lexical embedder and never pull a model.

## CLI

```bash
poetry run mnemosyne-rag ingest ./data/palace mythos ./fixtures/mnemosyne.md
poetry run mnemosyne-rag search ./data/palace mythos "Who are the Muses?"
poetry run mnemosyne-rag ask ./data/palace mythos "What does Mnemosyne remember?"
```

## Library

```python
from pathlib import Path
from mnemosyne_rag import MemoryPalace, PalaceConfig

palace = MemoryPalace(PalaceConfig(persist_dir=Path("./data/palace"), vault="mythos"))
palace.ingest_path(Path("./notes/memory.md"))
hits = palace.search("rivers of memory", top_k=5)
answer = palace.ask("What is a memory palace?")
```

## Generation

`ask()` always retrieves. If Ollama is reachable at `OLLAMA_HOST` (default `http://127.0.0.1:11434`), Mnemosyne asks the configured model to compose a grounded answer. Otherwise it synthesizes an extractive reply from the cited shards.
