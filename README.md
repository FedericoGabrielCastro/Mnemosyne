# Mnemosyne

Local memory palace: **retrieval-augmented generation** and **semantic search**, fully on your machine.

| Layer | Stack | Role |
| --- | --- | --- |
| [`rag/`](rag/README.md) | Poetry, ChromaDB, FastEmbed | Local embeddings, ingest, semantic retrieval |
| `backend/` | Django, Django REST Framework | HTTP API — next pull request |
| `frontend/` | React, Vite, pnpm, Tailwind | Oracle UI — later pull request |

## RAG

```bash
cd rag
poetry install
poetry run pytest
poetry run mnemosyne-rag ingest ./data/palace mythos ./tests/fixtures/mnemosyne.md --lexical
poetry run mnemosyne-rag search ./data/palace mythos "Who are the Muses?" --lexical
poetry run mnemosyne-rag ask ./data/palace mythos "What does Mnemosyne remember?" --lexical
```

The first non-lexical ingest downloads `BAAI/bge-small-en-v1.5` (ONNX) and keeps it on disk. Pass `--lexical` to skip that download.

Optional: [Ollama](https://ollama.com/) on `127.0.0.1:11434` for generative answers. Without it, the oracle answers extractively from cited shards.
