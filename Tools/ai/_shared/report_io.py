"""Shared report I/O helpers for AI runtime packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def resolve_output_path(repo_root: Path, output_arg: str) -> Path:
    """Resolve an output path relative to the repository root when needed."""
    output = Path(output_arg)
    if not output.is_absolute():
        output = repo_root / output
    return output.resolve()


def write_json_report(report: dict[str, Any], output: Path | None = None) -> str:
    """Serialize a report, optionally write it, and return the JSON text."""
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    return text


def write_text_report(text: str, output: Path) -> str:
    """Write UTF-8 text report content and return the written text."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return text
