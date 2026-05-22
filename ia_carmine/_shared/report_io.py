"""Shared report I/O helpers for AI runtime packages."""

from __future__ import annotations

import json
import sys
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


def json_report_text(
    report: Any,
    *,
    ensure_ascii: bool = False,
    default: Any | None = None,
) -> str:
    """Serialize a report with the repository's stable pretty JSON shape."""
    kwargs: dict[str, Any] = {"indent": 2, "ensure_ascii": ensure_ascii}
    if default is not None:
        kwargs["default"] = default
    return json.dumps(report, **kwargs) + "\n"


def print_json_report(report: Any, *, default: Any | None = None) -> None:
    """Print JSON without crashing on narrow Windows console encodings."""
    try:
        sys.stdout.write(json_report_text(report, default=default))
    except UnicodeEncodeError:
        sys.stdout.write(json_report_text(report, ensure_ascii=True, default=default))


def write_text_report(text: str, output: Path) -> str:
    """Write UTF-8 text report content and return the written text."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return text
