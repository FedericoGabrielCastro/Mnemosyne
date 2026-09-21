from __future__ import annotations

import argparse
import json
from pathlib import Path

from mnemosyne_rag.config import PalaceConfig
from mnemosyne_rag.embeddings import create_embedder
from mnemosyne_rag.pipeline import MemoryPalace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mnemosyne-rag", description="Local RAG for Mnemosyne.")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Index a document into a vault")
    _add_common(ingest)
    ingest.add_argument("path", type=Path)

    search = sub.add_parser("search", help="Semantic search over a vault")
    _add_common(search)
    search.add_argument("query")
    search.add_argument("--top-k", type=int, default=5)

    ask = sub.add_parser("ask", help="Retrieve and answer from a vault")
    _add_common(ask)
    ask.add_argument("question")
    ask.add_argument("--top-k", type=int, default=5)

    stats = sub.add_parser("stats", help="Show vault totals")
    _add_common(stats)

    args = parser.parse_args(argv)
    palace = MemoryPalace(
        PalaceConfig(persist_dir=args.persist_dir, vault=args.vault),
        embedder=create_embedder(lexical=args.lexical),
    )

    if args.command == "ingest":
        result = palace.ingest_path(args.path)
        print(json.dumps(result.__dict__, indent=2))
        return 0
    if args.command == "search":
        hits = palace.search(args.query, top_k=args.top_k)
        payload = [
            {"score": hit.score, "title": hit.title, "document_id": hit.document_id, "text": hit.text}
            for hit in hits
        ]
        print(json.dumps(payload, indent=2))
        return 0
    if args.command == "ask":
        answer = palace.ask(args.question, top_k=args.top_k)
        print(json.dumps({"mode": answer.mode, "answer": answer.answer, "citations": len(answer.citations)}, indent=2))
        return 0
    stats_result = palace.stats()
    print(json.dumps(stats_result.__dict__, indent=2))
    return 0


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("persist_dir", type=Path)
    parser.add_argument("vault")
    parser.add_argument("--lexical", action="store_true", help="Use the hashed lexical embedder")


if __name__ == "__main__":
    raise SystemExit(main())
