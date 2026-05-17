"""Shared helpers for runtime SQLite memory."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OPERATIONAL_DB = "output/ai_runtime_memory/operational_context.sqlite"
DEFAULT_PERSISTENT_DB = "indexAI/agent_memory/agent_memory.sqlite"
DEFAULT_OUTPUT = "output/validation/agent_runtime_sqlite_memory.json"
DEFAULT_MARKDOWN = "output/validation/agent_runtime_sqlite_memory.md"
SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def read_arg_file(repo_root: Path, value: str) -> str:
    if not value:
        return ""
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig", errors="replace")

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False

def safe_id(value: str) -> str:
    text = SAFE_ID_RE.sub("_", str(value or "").strip()).strip("._-")
    return text[:80] or "runtime_memory"

def parse_tags(values: list[str]) -> list[str]:
    tags: list[str] = []
    for value in values:
        for part in str(value).split(","):
            normalized = part.strip()
            if normalized and normalized not in tags:
                tags.append(normalized)
    return tags
