"""Duplicate-code signal refinement."""

from __future__ import annotations

from typing import Any

from .common import ALLOW_DUPLICATE_SYMBOLS, BACKUP_OR_GENERATED_SEGMENTS

def is_backup_or_generated_path(path: str) -> bool:
    return any(segment in path for segment in BACKUP_OR_GENERATED_SEGMENTS)

def path_group(path: str) -> str:
    parts = path.split("/")
    if len(parts) >= 3 and parts[0] == "Tools":
        return "/".join(parts[:2])
    if len(parts) >= 3 and parts[0] == "Scripting":
        return "/".join(parts[:2])
    return parts[0] if parts else path

def is_low_signal_duplicate(symbol: str, paths: list[str]) -> bool:
    if symbol in ALLOW_DUPLICATE_SYMBOLS:
        return True
    if symbol.startswith("_") and len(paths) <= 4:
        return True
    if (
        symbol.startswith(
            (
                "add_",
                "build_",
                "check_",
                "classify_",
                "configure_",
                "create_",
                "extract_",
                "find_",
                "format_",
            )
        )
        and len(paths) <= 6
    ):
        return True
    if any(is_backup_or_generated_path(path) for path in paths):
        return True
    groups = {path_group(path) for path in paths}
    if len(groups) > 1 and len(paths) <= 6:
        return True
    return False

def refine_code_code(
    review: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    duplicates = review.get("code_code_consistency", {}).get("duplicate_symbols", []) or []
    actionable = []
    ignored = []
    for item in duplicates:
        symbol = str(item.get("symbol") or "")
        paths = [str(path) for path in item.get("paths", [])]
        if is_low_signal_duplicate(symbol, paths):
            ignored.append({**item, "reason": "generic_generated_or_cross_package_duplicate"})
        elif paths and all(is_backup_or_generated_path(path) for path in paths):
            ignored.append({**item, "reason": "backup_or_generated_only"})
        elif any("Scripting/v61b_backgood/" in path for path in paths) and any(
            "Scripting/v61b/" in path for path in paths
        ):
            ignored.append({**item, "reason": "active_vs_backup_tree_duplicate"})
        else:
            actionable.append(item)
    findings = []
    if actionable:
        findings.append(
            {
                "severity": "low",
                "area": "code_code",
                "title": "Duplicate code symbols remain after generic/generated filtering",
                "details": [
                    f"{item.get('symbol')} -> {item.get('paths')}" for item in actionable[:30]
                ],
            }
        )
    return findings, {
        "actionable": actionable[:120],
        "ignored_count": len(ignored),
        "ignored_sample": ignored[:80],
    }
