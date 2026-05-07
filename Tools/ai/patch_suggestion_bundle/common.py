"""Shared model, constants and small utilities for patch suggestion apply."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DENY_PREFIXES = (
    ".git/",
    "output/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "renders/",
)

DENY_FRAGMENTS = (
    ".sqlite",
    ".sqlite-wal",
    ".sqlite-shm",
    ".db",
)

SUPPORTED_OPERATIONS = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}

PROPOSAL_ONLY_OPERATIONS = {
    "manual_patch_suggestion",
    "proposal_only",
    "manual_review_only",
}

DEFAULT_DISCOVER_SUGGESTION_ROOTS = (
    "docs/LOCAL_VALIDATION_EVIDENCE",
    "output/patch_specs",
    "output/validation",
    "output/ai_pipeline",
    "output/ai_packets",
)

DEFAULT_DISCOVER_SUGGESTION_TOKENS = (
    "patch_notes_quality_product",
    "patch_suggestion",
    "suggestion",
    "proposal",
    "recommendation",
    "patch_plan",
    "agent_review",
)

DEFAULT_CURRENT_SUGGESTION_REPORTS = (
    "output/ai_pipeline/repository_update_suggestions.json",
    "output/ai_pipeline/repository_change_proposals.json",
)


@dataclass
class PatchOperation:
    """Normalized deterministic patch operation."""

    operation: str
    path: str
    content: str | None = None
    find: str | None = None
    replace: str | None = None
    marker: str | None = None
    source_id: str | None = None
    family: str | None = None
    description: str | None = None


def compact_artifact_stamp(stamp: str, max_chars: int = 56) -> str:
    """Match the full-toolbox Python engine artifact-stamp normalization."""
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", stamp.strip() or "run").strip("._-")
    if len(safe) <= max_chars:
        return safe
    digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10]
    head = safe[: max(12, max_chars - len(digest) - 1)].rstrip("._-")
    return f"{head}-{digest}"


def run_git(repo_root: Path, *args: str) -> str:
    """Run a git command and return stdout, or an empty string on failure."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def current_branch(repo_root: Path) -> str:
    """Return current branch name when available."""
    return run_git(repo_root, "branch", "--show-current") or "unknown"


def git_status_short(repo_root: Path) -> str:
    """Return git status --short output."""
    return run_git(repo_root, "status", "--short")


def split_values(values: list[str] | tuple[str, ...]) -> list[str]:
    """Split repeatable/comma-separated CLI values while preserving order."""
    out: list[str] = []
    for value in values:
        for part in str(value).split(","):
            cleaned = part.strip().strip("'\"")
            if cleaned:
                out.append(cleaned)
    return out


def unique_in_order(items: list[str] | tuple[str, ...]) -> list[str]:
    """Return unique non-empty normalized path-ish values in order."""
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        normalized = str(item).replace("\\", "/").strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            out.append(normalized)
    return out


def repo_relative(path: Path, repo_root: Path) -> str:
    """Return a normalized repository-relative path."""
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def load_json(path: Path) -> tuple[Any | None, str | None]:
    """Read JSON, returning data or error."""
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")), None
    except Exception as exc:  # noqa: BLE001 - report exact failure
        return None, f"{type(exc).__name__}: {exc}"


def first_string(data: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    """Return the first non-empty string from any accepted key."""
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def as_string_list(value: Any) -> list[str]:
    """Normalize string/list values into strings."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item is not None and str(item)]
    return []
