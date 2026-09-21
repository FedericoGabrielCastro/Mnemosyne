# Mnemosyne

Local memory palace: **retrieval-augmented generation** and **semantic search**, fully on your machine.

| Layer | Stack | Role |
| --- | --- | --- |
| [`rag/`](rag/README.md) | Poetry, ChromaDB, FastEmbed | Local embeddings, ingest, semantic retrieval |
| [`backend/`](backend/README.md) | Django, Django REST Framework | HTTP API over the memory vaults |
| `frontend/` | React, Vite, pnpm, Tailwind | Oracle UI — next pull request |

## Requirements

- Python 3.11–3.13
- [Poetry](https://python-poetry.org/)

Optional: [Ollama](https://ollama.com/) on `127.0.0.1:11434` for generative answers. Without it, the oracle answers extractively from cited shards.

## RAG

```bash
cd rag
poetry install
poetry run pytest
```

## Django API

```bash
cd backend
cp .env.example .env
poetry install
poetry run python manage.py migrate
poetry run python manage.py seed_memory
poetry run python manage.py runserver 8000
```

API root: `http://127.0.0.1:8000/api/`

Set `MNEMOSYNE_LEXICAL=true` in `backend/.env` to skip downloading the ONNX embedding model. Leave it false so `BAAI/bge-small-en-v1.5` runs locally.

## Tests

```bash
cd rag && poetry install && poetry run pytest
cd backend && poetry install && MNEMOSYNE_LEXICAL=true poetry run python manage.py test
```
