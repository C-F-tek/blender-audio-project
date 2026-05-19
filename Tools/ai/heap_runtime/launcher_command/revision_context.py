"""Revision context selection for heap runtime launcher commands."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai._shared.revision_context_prompt import render_revision_context_prompt

from .common import REQUIRED_COMPOSER_JSON, read_optional_json

def is_complete_heap_run_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and path.name.startswith("heap_context_closure_")
        and (path / REQUIRED_COMPOSER_JSON).exists()
    )

def latest_revision_context(repo_root: Path) -> tuple[Path | None, dict[str, Any]]:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return None, {}
    candidates = sorted(
        [
            path / "external_heap_revision_context.json"
            for path in validation_dir.iterdir()
            if is_complete_heap_run_dir(path)
            and (path / "external_heap_revision_context.json").exists()
        ],
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )
    if not candidates:
        return None, {}
    path = candidates[0].resolve()
    return path, read_optional_json(path)

def revision_context_from_profile(
    repo_root: Path, profile: dict[str, Any], explicit_path: str
) -> tuple[Path | None, dict[str, Any]]:
    mode = str(profile.get("revision_context_mode") or "off")
    if mode == "off":
        return None, {}
    if explicit_path.strip():
        path = Path(explicit_path)
        if not path.is_absolute():
            path = repo_root / path
        path = path.resolve()
        return path, read_optional_json(path)
    if mode == "auto_latest":
        return latest_revision_context(repo_root)
    return None, {}

def revision_context_prompt(payload: dict[str, Any], path: Path | None, max_tasks: int) -> str:
    return render_revision_context_prompt(payload, path, max_tasks)
