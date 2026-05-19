"""Chunk summary generation."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from .common import compact_text

def deterministic_summary(text: str, titles: list[str]) -> str:
    title_part = "; ".join(titles[:5]) if titles else "no explicit section title"
    preview = compact_text(text, 260)
    return f"Chunk deterministico. Sezioni: {title_part}. Preview: {preview}"

def call_ollama_summary(
    *,
    host: str,
    model: str,
    text: str,
    titles: list[str],
    timeout: int,
    max_input_chars: int,
    keep_alive: str,
) -> tuple[str | None, str | None, float]:
    prompt = (
        "Sei un summarizer locale per evidence bundle tecnici. "
        "Riassumi questo chunk in italiano tecnico in massimo 5 righe. "
        "Indica: scopo, segnali principali, eventuali guardrail o errori, perché serve a una AI cloud. "
        "Non inventare.\n\n"
        f"Titoli sezioni: {titles[:8]}\n\n"
        f"Chunk:\n{text[:max_input_chars]}"
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive,
        "options": {"temperature": 0.1, "num_predict": 220},
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, str(exc), round(time.perf_counter() - started, 3)
    elapsed = round(time.perf_counter() - started, 3)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"invalid ollama JSON: {exc}", elapsed
    text_out = str(data.get("response") or "").strip()
    if not text_out:
        return None, "empty ollama response", elapsed
    return text_out, None, elapsed
