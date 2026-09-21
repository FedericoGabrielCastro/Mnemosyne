from __future__ import annotations

from mnemosyne_rag.types import SearchHit

_EXTRACT_LIMIT = 3
_SNIPPET = 420


def synthesize_extractive(question: str, hits: list[SearchHit]) -> str:
    if not hits:
        return (
            "The vault is silent. No memory shard is close enough to this question. "
            "Inscribe more documents, then ask again."
        )
    lines = [
        f"Remembered against the question: {question.strip()}",
        "",
    ]
    for index, hit in enumerate(hits[:_EXTRACT_LIMIT], start=1):
        snippet = _clip(hit.text)
        lines.append(f"{index}. From {hit.title} (score {hit.score:.2f}): {snippet}")
    return "\n".join(lines)


def build_generative_prompt(question: str, hits: list[SearchHit]) -> str:
    evidence = "\n\n".join(
        f"[{index}] source={hit.title}\n{hit.text}" for index, hit in enumerate(hits, start=1)
    )
    return (
        "You are Mnemosyne, a local memory oracle. Answer only from the cited shards. "
        "If the shards do not contain the answer, say so. Quote sources by number.\n\n"
        f"Question: {question}\n\n"
        f"Memory shards:\n{evidence}\n\n"
        "Answer:"
    )


def _clip(text: str, limit: int = _SNIPPET) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"
