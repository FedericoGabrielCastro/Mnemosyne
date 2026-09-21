# Mnemosyne Django API

HTTP vaults around the local RAG engine. Documents are uploaded, chunked, embedded, and stored on disk. Search and ask never leave the machine unless Ollama is running locally.

## Install

```bash
cd rag && poetry install
cd ../backend && poetry install
```

## Run

```bash
cd backend
cp .env.example .env
poetry run python manage.py migrate
poetry run python manage.py seed_memory
poetry run python manage.py runserver 8000
```

API root: `http://127.0.0.1:8000/api/`

Set `MNEMOSYNE_LEXICAL=true` to skip downloading the ONNX embedding model (tests and first-run demos). Leave it false so `BAAI/bge-small-en-v1.5` runs locally.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health/` | Process pulse |
| GET/POST | `/api/vaults/` | List / inscribe vaults |
| GET/PATCH/DELETE | `/api/vaults/:id/` | Vault detail |
| GET/POST | `/api/vaults/:id/documents/` | List / offer documents |
| DELETE | `/api/vaults/:id/documents/:doc_id/` | Forget a document |
| POST | `/api/vaults/:id/search/` | Semantic search |
| POST | `/api/vaults/:id/ask/` | RAG answer with citations |
