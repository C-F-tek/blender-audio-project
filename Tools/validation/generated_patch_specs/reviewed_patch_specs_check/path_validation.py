"""Path and replacement validation helpers for reviewed patch specs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import normalize_repo_path
from .constants import (
    FORBIDDEN_COMMAND_FRAGMENTS,
    FORBIDDEN_TARGET_EXACT,
    FORBIDDEN_TARGET_FRAGMENTS,
    FORBIDDEN_TARGET_PREFIXES,
    SUPPORTED_REPLACEMENT_TYPES,
)

def target_path_errors(path: str, repo_root: Path) -> list[str]:
    normalized = normalize_repo_path(path)
    errors: list[str] = []
    if not normalized:
        return ["target path is empty"]
    if Path(normalized).is_absolute():
        errors.append("absolute target paths are not allowed")
    full = (repo_root / normalized).resolve()
    try:
        full.relative_to(repo_root)
    except ValueError:
        errors.append("target path escapes repository root")
    if normalized in FORBIDDEN_TARGET_EXACT:
        errors.append(f"forbidden target path: {normalized}")
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_TARGET_PREFIXES):
        errors.append(f"forbidden target prefix: {normalized}")
    lower = normalized.lower()
    if any(fragment in lower for fragment in FORBIDDEN_TARGET_FRAGMENTS) and lower.endswith(
        ".json"
    ):
        errors.append(f"forbidden full-analysis JSON target: {normalized}")
    if "*" in normalized or normalized.endswith("/"):
        errors.append("target must be a concrete file, not a glob or directory")
    if not full.exists():
        errors.append("target file does not exist")
    elif not full.is_file():
        errors.append("target is not a file")
    return errors


def validation_command_errors(command: Any) -> list[str]:
    lower = str(command).lower()
    return [
        f"forbidden command fragment: {fragment}"
        for fragment in FORBIDDEN_COMMAND_FRAGMENTS
        if fragment.lower() in lower
    ]


def replacement_errors(replacement: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(replacement, dict):
        return ["replacement must be an object"]
    kind = replacement.get("type", "exact")
    if kind not in SUPPORTED_REPLACEMENT_TYPES:
        errors.append(f"unsupported replacement type: {kind}")
    try:
        if int(replacement.get("count", 1)) < 1:
            errors.append("replacement count must be >= 1")
    except (TypeError, ValueError):
        errors.append("replacement count must be an integer")
    if kind in {"exact", "regex"} and not isinstance(replacement.get("new"), str):
        errors.append(f"{kind} replacement requires new string")
    if kind == "exact" and not isinstance(replacement.get("old"), str):
        errors.append("exact replacement requires old string")
    if kind == "regex" and not isinstance(replacement.get("pattern"), str):
        errors.append("regex replacement requires pattern string")
    if kind in {"insert_after", "insert_before"}:
        if not isinstance(replacement.get("anchor"), str) or not isinstance(
            replacement.get("insert"), str
        ):
            errors.append(f"{kind} replacement requires anchor and insert strings")
    return errors
