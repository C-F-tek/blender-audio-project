"""Shared constants and path policy for the Ollama tool gateway."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_MODEL = ""
DEFAULT_OLLAMA_URL = ""
DEFAULT_OUTPUT_DIR = "output/ollama_tool_gateway"
MAX_FILE_CHARS = 12000
MAX_SEARCH_RESULTS = 20
DENY_PREFIXES = (
    ".git/",
    ".venv/",
    "venv/",
    "output/",
    "renders/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "__pycache__/",
)
DENY_EXACT = {".claude/settings.local.json", ".env"}
DENY_FRAGMENTS = (
    "secret",
    "token",
    "password",
    "credential",
    "full_analysis",
    "analysis_full",
    ".sqlite",
    ".db",
)
TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".ps1",
    ".sh",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".csv",
    ".toml",
}

@dataclass
class GatewayConfig:
    repo_root: Path
    model: str
    ollama_url: str
    output_dir: Path
    max_rounds: int
    max_file_chars: int
    max_search_results: int
    allow_output_read: bool

def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def resolve_repo_path(repo_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)

def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False

def path_policy_error(rel_path: str, *, allow_output_read: bool = False) -> str:
    normalized = rel_path.replace("\\", "/").strip()
    lower = normalized.lower()
    if not normalized:
        return "empty path"
    if Path(normalized).is_absolute():
        return "absolute paths are not allowed"
    if normalized in DENY_EXACT:
        return "path is explicitly denied"
    prefixes = (
        DENY_PREFIXES
        if not allow_output_read
        else tuple(p for p in DENY_PREFIXES if p != "output/")
    )
    if any(lower.startswith(prefix.lower()) for prefix in prefixes):
        return "path prefix is denied"
    if any(fragment in lower for fragment in DENY_FRAGMENTS):
        return "path fragment is denied"
    return ""

def compact_text(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars] + "\n...[truncated]", True
