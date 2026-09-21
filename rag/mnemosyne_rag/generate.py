from __future__ import annotations

from typing import Any

import httpx


class GenerativeError(RuntimeError):
    pass


def generate_with_ollama(prompt: str, *, host: str, model: str, timeout: float = 60.0) -> str:
    url = host.rstrip("/") + "/api/generate"
    payload: dict[str, Any] = {"model": model, "prompt": prompt, "stream": False}
    try:
        response = httpx.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise GenerativeError(f"Ollama is unreachable at {host}") from exc
    data = response.json()
    text = str(data.get("response") or "").strip()
    if not text:
        raise GenerativeError("Ollama returned an empty answer")
    return text


def ollama_available(host: str, timeout: float = 1.5) -> bool:
    try:
        response = httpx.get(host.rstrip("/") + "/api/tags", timeout=timeout)
        return response.status_code < 500
    except httpx.HTTPError:
        return False
