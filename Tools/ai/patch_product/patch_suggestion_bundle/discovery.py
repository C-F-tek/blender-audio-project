"""Suggestion report discovery for the final patch phase."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai.patch_product.patch_suggestion_bundle.common import (
    DEFAULT_CURRENT_SUGGESTION_REPORTS,
    repo_relative,
)


def discover_suggestion_reports(
    repo_root: Path,
    stamp: str | None,
    roots: list[str],
    tokens: list[str],
    max_files: int,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Discover local suggestion/proposal JSON reports by compact artifact stamp.

    Discovery is read-only and accepts both Git-trackable evidence under docs and
    ignored local runtime reports under output. Returned paths are repo-relative.
    """
    if not stamp:
        return [], []
    normalized_tokens = [token.lower() for token in tokens if token]
    discovered: list[tuple[float, str]] = []
    scanned: list[dict[str, Any]] = []

    for raw_root in roots:
        root = (repo_root / raw_root).resolve()
        scan_item: dict[str, Any] = {
            "root": raw_root.replace("\\", "/"),
            "exists": root.exists(),
            "json_candidates": 0,
            "matched": 0,
            "error": None,
        }
        if not root.exists():
            scanned.append(scan_item)
            continue
        try:
            root.relative_to(repo_root.resolve())
        except ValueError:
            scan_item["error"] = "root is outside repository"
            scanned.append(scan_item)
            continue

        for path in root.rglob("*.json"):
            scan_item["json_candidates"] += 1
            rel = repo_relative(path, repo_root)
            lower_rel = rel.lower()
            if stamp.lower() not in lower_rel:
                continue
            if normalized_tokens and not any(token in lower_rel for token in normalized_tokens):
                continue
            discovered.append((path.stat().st_mtime, rel))
            scan_item["matched"] += 1
        scanned.append(scan_item)

    deduped: list[str] = []
    seen: set[str] = set()
    for _, rel in sorted(discovered, reverse=True):
        if rel in seen:
            continue
        seen.add(rel)
        deduped.append(rel)
        if len(deduped) >= max_files:
            break
    return deduped, scanned


def discover_current_suggestion_reports(repo_root: Path, enabled: bool) -> list[str]:
    """Return current non-stamped suggestion/proposal reports if present."""
    if not enabled:
        return []
    out: list[str] = []
    for rel in DEFAULT_CURRENT_SUGGESTION_REPORTS:
        if (repo_root / rel).exists():
            out.append(rel)
    return out
