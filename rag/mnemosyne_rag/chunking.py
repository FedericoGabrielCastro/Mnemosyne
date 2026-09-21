from __future__ import annotations

import re
from dataclasses import dataclass

_WHITESPACE = re.compile(r"[ \t]+\n")


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    start: int
    end: int


def normalize_text(text: str) -> str:
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = _WHITESPACE.sub("\n", cleaned)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[TextChunk]:
    body = normalize_text(text)
    if not body:
        return []
    if len(body) <= chunk_size:
        return [TextChunk(index=0, text=body, start=0, end=len(body))]

    chunks: list[TextChunk] = []
    start = 0
    index = 0
    while start < len(body):
        end = min(len(body), start + chunk_size)
        if end < len(body):
            snap = _last_break(body, start, end)
            if snap > start:
                end = snap
        piece = body[start:end].strip()
        if piece:
            chunks.append(TextChunk(index=index, text=piece, start=start, end=end))
            index += 1
        if end >= len(body):
            break
        next_start = max(end - chunk_overlap, start + 1)
        start = _next_break(body, next_start)
        if start <= chunks[-1].start:
            start = end
    return chunks


def _last_break(text: str, start: int, end: int) -> int:
    window = text[start:end]
    min_keep = max(1, len(window) // 3)
    for separator in ("\n\n", "\n", ". ", " "):
        pos = window.rfind(separator)
        if pos >= min_keep:
            return start + pos + len(separator)
    return end


def _next_break(text: str, index: int) -> int:
    while index < len(text) and index > 0 and not text[index].isspace() and not text[index - 1].isspace():
        index -= 1
    while index < len(text) and text[index].isspace():
        index += 1
    return index
