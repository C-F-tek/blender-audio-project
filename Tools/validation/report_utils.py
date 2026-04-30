"""Shared helpers for lightweight validation reports."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def resolve_output_path(repo_root: Path, output_arg: str) -> Path:
    """Resolve a report output path relative to the repository root when needed."""
    output = Path(output_arg)
    if not output.is_absolute():
        output = repo_root / output
    return output.resolve()


def write_json_report(report: dict[str, Any], output: Path | None = None) -> str:
    """Serialize a report, optionally write it, and return the rendered JSON text."""
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    return text


def failed_result_errors(results: Iterable[dict[str, Any]], *, label_key: str = "path") -> list[str]:
    """Build compact root-level error strings from result entries with ok=false."""
    errors: list[str] = []
    for item in results:
        if item.get("ok") is not False:
            continue
        label = str(item.get(label_key) or item.get("name") or item.get("package") or "unknown")
        error = str(item.get("error") or item.get("reason") or "failed")
        errors.append(f"{label}: {error}")
    return errors


def warning_result_messages(results: Iterable[dict[str, Any]], *, label_key: str = "path") -> list[str]:
    """Build compact root-level warning strings from result entries exposing warnings."""
    warnings: list[str] = []
    for item in results:
        raw = item.get("warnings")
        if not raw:
            continue
        label = str(item.get(label_key) or item.get("name") or item.get("package") or "unknown")
        if isinstance(raw, list):
            warnings.extend(f"{label}: {warning}" for warning in raw)
        else:
            warnings.append(f"{label}: {raw}")
    return warnings
