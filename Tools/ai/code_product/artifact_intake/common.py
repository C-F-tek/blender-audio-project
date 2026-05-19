from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = "output/validation/code_product_artifact_intake.json"
DEFAULT_MARKDOWN = "output/validation/code_product_artifact_intake.md"
DENY_PREFIXES = ("output/", "renders/", "indexAI/code_chunks/", "indexAI/project_code_chunks/")
DENY_SUFFIXES = (".db", ".sqlite", ".sqlite3", ".sqlite-wal", ".sqlite-shm")
SAFE_PREFIXES = ("Tools/", "docs/", "config/")
INTEGRATED_STATUSES = (
    "already_integrated",
    "already_integrated_with_context_drift",
    "already_integrated_truncated_dump",
    "already_integrated_no_worktree_diff",
    "verified_target_no_worktree_diff",
)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return text if limit is None else text[:limit]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def repo_rel(repo_root: Path, value: str | Path) -> str:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(value).replace("\\", "/")


def normalize_target(raw: str) -> str:
    return str(raw or "").strip().strip("`").replace("\\", "/")


def target_error(target: str) -> str:
    normalized = normalize_target(target)
    lower = normalized.lower()
    if not normalized:
        return "empty target"
    if Path(normalized).is_absolute():
        return "target is absolute"
    if ".." in Path(normalized).parts:
        return "target escapes repository"
    if any(lower.startswith(prefix.lower()) for prefix in DENY_PREFIXES):
        return "target prefix is denied"
    if any(lower.endswith(suffix) for suffix in DENY_SUFFIXES):
        return "target suffix is denied"
    if not any(normalized.startswith(prefix) for prefix in SAFE_PREFIXES):
        return "target prefix is not allowlisted"
    return ""
