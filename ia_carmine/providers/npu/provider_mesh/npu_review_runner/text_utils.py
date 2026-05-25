"""Text loading and prompt fitting helpers for NPU review."""

from __future__ import annotations

from pathlib import Path

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_text_limited(path: Path, max_chars: int) -> str:
    text = read_text(path)

    if max_chars <= 0 or len(text) <= max_chars:
        return text

    return text[:max_chars] + "\n\n[TRUNCATED BY brokered NPU review helper]\n"


def split_text(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + max_chars, text_len)
        chunks.append(text[start:end])
        if end == text_len:
            break
        start = max(end - max(0, overlap_chars), start + 1)

    return chunks


def load_context_chunks(
    context_path: Path,
    chunk_dir: Path,
    chunk_chars: int,
    overlap_chars: int,
    max_chunks: int,
) -> list[tuple[str, str]]:
    chunk_files = []
    if chunk_dir.exists():
        chunk_files = sorted(chunk_dir.glob("chunk_*.md"))

    if chunk_files:
        chunks = [(path.name, read_text(path)) for path in chunk_files]
    else:
        text = read_text(context_path)
        chunks = [
            (f"context_slice_{index:03d}.md", chunk)
            for index, chunk in enumerate(split_text(text, chunk_chars, overlap_chars), 1)
        ]

    if max_chunks > 0:
        chunks = chunks[:max_chunks]

    return chunks


def fit_prompt(prefix: str, context: str, suffix: str, max_prompt_chars: int) -> str:
    if max_prompt_chars <= 0:
        return prefix + context + suffix

    budget = max_prompt_chars - len(prefix) - len(suffix)
    if budget < 1000:
        budget = 1000

    if len(context) > budget:
        context = context[:budget] + "\n\n[CHUNK TRIMMED TO FIT NPU PROMPT WINDOW]\n"

    return prefix + context + suffix
