#!/usr/bin/env python3
"""Artifact manifest and bounded artifact-content helpers for evidence bundles."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai.github_evidence_bundle_io import (
    CONTENT_EXTENSION_ALLOWLIST,
    MAX_ARTIFACT_PREVIEW_CHARS,
    line_count,
    normalize_manifest_path,
    raw_artifact_content_allowed,
    read_json,
    read_text,
    resolve_repo_path,
    sha256_file,
)


def base_artifact_entry(path: Path, repo_root: Path, role: str) -> dict[str, Any]:
    """Return common artifact metadata fields."""
    return {
        "path": normalize_manifest_path(path, repo_root),
        "exists": path.exists(),
        "suffix": path.suffix.lower(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
        "sha256": sha256_file(path),
        "role": role,
    }


def summarize_artifact(path: Path, repo_root: Path) -> dict[str, Any]:
    """Return a compact manifest entry for a local artifact/report path."""
    item = base_artifact_entry(path, repo_root, "local_artifact_reference")
    item["content_included"] = False

    if not path.exists() or not path.is_file():
        return item

    rel = str(item["path"])
    if path.suffix.lower() in CONTENT_EXTENSION_ALLOWLIST and raw_artifact_content_allowed(rel):
        text, error = read_text(path)
        if error:
            item["read_error"] = error
            return item
        item["preview"] = text[:MAX_ARTIFACT_PREVIEW_CHARS]
        item["preview_chars"] = min(len(text), MAX_ARTIFACT_PREVIEW_CHARS)
        item["line_count"] = line_count(text)
        item["content_included"] = bool(item["preview"])

    return item


def build_included_artifact(path: Path, repo_root: Path, *, max_chars: int, role: str) -> dict[str, Any]:
    """Return bounded artifact content for explicit/auto-related bundle artifacts."""
    item = base_artifact_entry(path, repo_root, role)
    item["content_included"] = False
    item["content_truncated"] = False
    if not path.exists() or not path.is_file():
        return item
    rel = str(item["path"])
    if path.suffix.lower() not in CONTENT_EXTENSION_ALLOWLIST:
        item["skip_reason"] = "suffix_not_text_allowlisted"
        return item
    if not raw_artifact_content_allowed(rel):
        item["skip_reason"] = "raw_artifact_content_denied_by_policy"
        return item
    text, error = read_text(path)
    if error:
        item["read_error"] = error
        return item
    item["line_count"] = line_count(text)
    item["raw_chars"] = len(text)
    item["included_chars"] = min(len(text), max_chars)
    item["content"] = text[:max_chars]
    item["content_truncated"] = len(text) > max_chars
    item["content_included"] = True
    return item


def append_declared_artifacts(discovered: list[Path], repo_root: Path, data: dict[str, Any]) -> None:
    """Append report-declared related artifacts to a discovered path list."""
    for key in ("markdown_output", "markdown_report", "csv_written"):
        value = data.get(key)
        if isinstance(value, str):
            discovered.append(resolve_repo_path(repo_root, value))
    inputs = data.get("inputs") if isinstance(data.get("inputs"), dict) else {}
    for value in inputs.values():
        if isinstance(value, str) and value:
            path = resolve_repo_path(repo_root, value)
            if path.exists() and path.is_file():
                discovered.append(path)


def discover_related_artifacts(repo_root: Path, report_paths: list[Path]) -> list[Path]:
    """Discover useful sibling/declared artifacts for bounded bundle inclusion."""
    discovered: list[Path] = []
    for report in report_paths:
        if report.suffix.lower() == ".json":
            sibling_md = report.with_suffix(".md")
            if sibling_md.exists():
                discovered.append(sibling_md)
        data = read_json(report)
        if data:
            append_declared_artifacts(discovered, repo_root, data)
    unique: dict[str, Path] = {}
    for path in discovered:
        key = path.resolve().as_posix() if path.exists() else path.as_posix()
        unique[key] = path
    return sorted(unique.values(), key=lambda item: normalize_manifest_path(item, repo_root).lower())


def build_included_artifacts(
    repo_root: Path,
    report_paths: list[Path],
    artifact_paths: list[Path],
    *,
    auto_include_related: bool,
    max_chars: int,
    max_artifacts: int,
) -> list[dict[str, Any]]:
    """Build deduplicated bounded included-artifact entries."""
    auto_artifacts = discover_related_artifacts(repo_root, report_paths) if auto_include_related else []
    included_candidates: list[tuple[Path, str]] = [(path, "explicit_artifact") for path in artifact_paths]
    included_candidates.extend((path, "auto_related_artifact") for path in auto_artifacts)
    deduped: dict[str, tuple[Path, str]] = {}
    for path, role in included_candidates:
        key = path.resolve().as_posix() if path.exists() else path.as_posix()
        deduped[key] = (path, role)
    return [
        build_included_artifact(path, repo_root, max_chars=max_chars, role=role)
        for path, role in list(deduped.values())[:max_artifacts]
    ]
