"""Shared JSONL helpers for heap/exchange runtime evidence."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def append_jsonl(path: Path | None, event: dict[str, Any]) -> None:
    """Append a timestamped JSON object to an exchange JSONL stream."""
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(event)
    payload.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
    path.open("a", encoding="utf-8", newline="\n").write(
        json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
    )


def load_jsonl(path: Path | None) -> tuple[list[dict[str, Any]], str | None]:
    """Load JSON object rows from an optional exchange JSONL stream."""
    if path is None:
        return [], "not provided"
    if not path.exists():
        return [], "missing"
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, line in enumerate(
        path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), start=1
    ):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = json.loads(stripped)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"line {index}: {type(exc).__name__}: {exc}")
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows, "; ".join(errors) if errors else None

