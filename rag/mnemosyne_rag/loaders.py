from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

SUPPORTED_SUFFIXES = {".txt", ".md", ".markdown", ".pdf"}


@dataclass(frozen=True)
class LoadedDocument:
    source: str
    title: str
    text: str
    pages: int


class UnsupportedDocument(ValueError):
    pass


def load_path(path: Path) -> LoadedDocument:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise UnsupportedDocument(f"Unsupported file type: {suffix}")
    if suffix == ".pdf":
        return _load_pdf(path)
    text = path.read_text(encoding="utf-8")
    return LoadedDocument(source=str(path), title=path.stem, text=text, pages=1)


def _load_pdf(path: Path) -> LoadedDocument:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        extracted = page.extract_text() or ""
        if extracted.strip():
            pages.append(f"[page {index}]\n{extracted.strip()}")
    text = "\n\n".join(pages)
    if not text.strip():
        raise UnsupportedDocument(f"No extractable text in PDF: {path}")
    return LoadedDocument(source=str(path), title=path.stem, text=text, pages=len(reader.pages))
