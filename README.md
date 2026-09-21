# Mnemosyne

Local memory palace: **retrieval-augmented generation** and **semantic search**, fully on your machine.

Named for the Titaness of memory. Documents are inscribed into vaults, split into overlapping shards, embedded with a local ONNX model, and recalled by intent.

| Layer | Stack | Role |
| --- | --- | --- |
| [`rag/`](rag/README.md) | Poetry, ChromaDB, FastEmbed | Local embeddings, ingest, semantic retrieval |
| [`backend/`](backend/README.md) | Django, Django REST Framework | HTTP API over the memory vaults |
| [`frontend/`](frontend/README.md) | React, Vite, pnpm, Tailwind | Oracle UI |

## Requirements

- Python 3.11–3.13
- [Poetry](https://python-poetry.org/)
- Node 20+
- [pnpm](https://pnpm.io/)

Optional: [Ollama](https://ollama.com/) on `127.0.0.1:11434` for generative answers. Without it, the oracle answers extractively from cited shards.

## Run

```bash
cd rag && poetry install
cd ../backend && poetry install
cp .env.example .env
poetry run python manage.py migrate
poetry run python manage.py seed_memory
poetry run python manage.py runserver 8000
```

```bash
cd frontend
pnpm install
pnpm dev
```

Open `http://127.0.0.1:5173`. Vite proxies `/api` to Django.

The first non-lexical ingest downloads `BAAI/bge-small-en-v1.5` (ONNX) and keeps it on disk. Set `MNEMOSYNE_LEXICAL=true` in `backend/.env` to skip that download.

## Tests

```bash
cd rag && poetry install && poetry run pytest
cd backend && poetry install && MNEMOSYNE_LEXICAL=true poetry run python manage.py test
cd frontend && pnpm build
```
