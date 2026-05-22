"""Manifest and spec discovery for generated patch-spec application."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .apply_common import (
    DENIED_TARGET_PREFIXES,
    DENIED_TARGET_SUFFIXES,
    STAMP_RE,
    load_json,
    repo_relative,
    unique_in_order,
)

def normalize_repo_path(path: str) -> str:
    return str(path or "").strip().replace("\\", "/").lstrip("./")

def is_denied_target(path: str) -> str | None:
    normalized = normalize_repo_path(path)
    lower = normalized.lower()
    if not normalized:
        return "empty target path"
    if any(lower.startswith(prefix.lower()) for prefix in DENIED_TARGET_PREFIXES):
        return "target is generated/runtime/evidence path"
    if lower.endswith(DENIED_TARGET_SUFFIXES):
        return "target is a database/runtime artifact"
    return None

def read_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    data, error = load_json(path)
    if error:
        return None, error
    if not isinstance(data, dict):
        return None, "JSON root must be an object"
    return data, None

def discover_latest_manifest(
    repo_root: Path, roots: list[str], max_files: int, manifest_stamp: str = ""
) -> str:
    candidates: list[Path] = []
    for raw_root in roots:
        root = (repo_root / raw_root).resolve()
        if not root.exists():
            continue
        candidates.extend(path for path in root.rglob("*_manifest.json") if path.is_file())
    candidates = sorted(candidates, key=lambda item: item.stat().st_mtime, reverse=True)
    for path in candidates[:max_files]:
        relative = repo_relative(path, repo_root)
        if manifest_stamp and manifest_stamp not in relative:
            continue
        data, error = read_json_object(path)
        if error or not data:
            continue
        if data.get("kind") in {
            "proposal_patch_spec_manifest",
            "reviewed_patch_spec_manifest",
        }:
            return relative
    return ""

def infer_manifest_stamp(*values: str) -> str:
    for value in values:
        matches = STAMP_RE.findall(str(value or ""))
        if matches:
            return matches[-1]
    return ""

def manifest_spec_paths(data: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for item in data.get("specs") or []:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.append(item["path"])
    for key in ("patch_specs", "reviewed_specs", "spec_paths"):
        value = data.get(key)
        if isinstance(value, list):
            paths.extend(str(item) for item in value if str(item).strip())
    return unique_in_order(paths)
