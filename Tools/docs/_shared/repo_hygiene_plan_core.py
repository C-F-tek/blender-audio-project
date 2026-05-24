#!/usr/bin/env python3
"""Build a repository hygiene plan and optional PatchKit cleanup bundle.

The plan is report-only by default. It classifies old/historical Markdown,
large split snapshots and refactor candidates, then emits a reviewable bundle
with guarded delete_file operations only for high-confidence candidates that
carry an explicit marker already present in the target text.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "output",
    "renders",
    "node_modules",
}
SKIP_PREFIXES = (
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)
CURRENT_DOC_HINTS = (
    "heap-exchange-and-patchkit-operating-model",
    "ai-orientation-map",
    "documentation-panorama-and-staleness-map",
    "unified-local-ai-refactor-launcher",
    "current-capability-depth-map",
    "single-owner-scripts-and-flow-boundaries",
)
OBSOLETE_HINTS = (
    "historical",
    "superseded",
    "obsolete",
    "legacy",
    "forensic context",
    "not the current",
    "not current",
)
DELETE_HINTS = (
    "historical",
    "superseded",
    "obsolete",
)
RISKY_DELETE_PREFIXES = (
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "output/",
    "renders/",
    "indexAI/",
    "Scripting/",
    "Tools/",
)
PROTECTED_CURRENT_DELETE_PREFIXES = (
    "docs/AI_DOCS_ENTRYPOINT.md/",
    "docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/",
)
EXPLICIT_DELETE_MARKERS = (
    "IA-CARMINE-DELETE-CANDIDATE",
    "Status: superseded",
    "Status: obsolete",
    "Status: delete-candidate",
    "status: superseded",
    "status: obsolete",
    "status: delete-candidate",
)
MD_SPLIT_MANIFEST = "_ia_carmine_md_split_manifest.json"
COMMAND_RE = re.compile(r"(?:python|py|python3|powershell(?:\.exe)?|gh|git)\b", re.IGNORECASE)


@dataclass
class HygieneItem:
    path: str
    kind: str
    classification: str
    confidence: str
    recommended_action: str
    reason: str
    line_count: int
    delete_marker: str = ""


def repo_root_from(start: Path) -> Path:
    cur = start.resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"repository root not found from {start}")


def rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def skipped(root: Path, path: Path) -> bool:
    parts = path.parts
    if any(part in SKIP_DIRS for part in parts):
        return True
    r = rel(root, path) if path.exists() else path.as_posix()
    return any(r.startswith(prefix) for prefix in SKIP_PREFIXES)


def iter_files(root: Path, suffixes: tuple[str, ...]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file() or skipped(root, path):
            continue
        if path.suffix.lower() in suffixes:
            yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def line_count(text: str) -> int:
    return len(text.splitlines()) if text else 0


def has_any(text: str, hints: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(hint in lower for hint in hints)


def explicit_delete_marker(text: str) -> str:
    lower = text.lower()
    for marker in EXPLICIT_DELETE_MARKERS:
        index = lower.find(marker.lower())
        if index >= 0:
            return text[index : index + len(marker)]
    return ""


def protected_current_delete_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in PROTECTED_CURRENT_DELETE_PREFIXES)


def classify_markdown(root: Path, path: Path, max_lines: int) -> HygieneItem:
    r = rel(root, path)
    text = read_text(path)
    lines = line_count(text)
    lower_r = r.lower()
    split_manifest = (path.parent / MD_SPLIT_MANIFEST).exists()
    current = has_any(text, CURRENT_DOC_HINTS) or any(hint in lower_r for hint in CURRENT_DOC_HINTS)
    obsolete = (
        has_any(text, OBSOLETE_HINTS) or "next-chat-handoff" in lower_r or "handoff" in lower_r
    )
    delete_marker = explicit_delete_marker(text)
    commands = bool(COMMAND_RE.search(text))

    if r.startswith("CHATGPT/") and ("handoff" in lower_r or "next-chat" in lower_r):
        return HygieneItem(
            r,
            "markdown",
            "historical_chat_handoff",
            "high",
            "archive_or_delete_after_index",
            "handoff file under CHATGPT is forensic context",
            lines,
        )
    if current or protected_current_delete_path(r):
        if lines > max_lines:
            return HygieneItem(
                r,
                "markdown",
                "oversized_current",
                "medium",
                "split_refactor_keep",
                f"current doc exceeds {max_lines} lines",
                lines,
            )
        return HygieneItem(
            r,
            "markdown",
            "current_oriented",
            "high",
            "keep",
            "contains current orientation anchors or protected current path",
            lines,
        )
    if split_manifest and obsolete and has_any(text, DELETE_HINTS):
        if delete_marker:
            return HygieneItem(
                r,
                "markdown",
                "obsolete_split_snapshot",
                "high",
                "delete_with_patchkit_allowlist",
                "split snapshot has explicit delete marker",
                lines,
                delete_marker,
            )
        return HygieneItem(
            r,
            "markdown",
            "obsolete_split_snapshot_needs_marker",
            "medium",
            "review_before_delete_marker",
            "split snapshot has obsolete signals but no explicit delete marker",
            lines,
        )
    if obsolete and not current and not commands:
        return HygieneItem(
            r,
            "markdown",
            "obsolete_reference",
            "medium",
            "delete_or_archive_after_link_check",
            "marked old without current-map anchors or executable commands",
            lines,
        )
    if obsolete and commands:
        return HygieneItem(
            r,
            "markdown",
            "historical_with_commands",
            "medium",
            "classify_then_refactor_or_delete",
            "old document still carries command-like text",
            lines,
        )
    if lines > max_lines and not current:
        return HygieneItem(
            r,
            "markdown",
            "oversized_noncanonical",
            "medium",
            "split_or_demote",
            f"line_count={lines} exceeds {max_lines}",
            lines,
        )
    return HygieneItem(
        r,
        "markdown",
        "unclassified",
        "low",
        "review_later",
        "no strong current or obsolete signal",
        lines,
    )


def classify_split_dirs(root: Path) -> list[HygieneItem]:
    items: list[HygieneItem] = []
    for directory in root.rglob("*"):
        if not directory.is_dir() or skipped(root, directory):
            continue
        parts = sorted(directory.glob("part-*.md"))
        manifest = directory / MD_SPLIT_MANIFEST
        if not parts and not manifest.exists():
            continue
        lines = 0
        text_join = ""
        for part in parts[:4]:
            text = read_text(part)
            text_join += text + "\n"
            lines += line_count(text)
        r = rel(root, directory)
        if directory.name.endswith(".md"):
            layout = "directory_form_split"
            action = "keep_or_classify_parts"
        else:
            layout = "legacy_split_layout"
            action = "migrate_with_refactor_markdown_splits"
        obsolete = has_any(text_join, OBSOLETE_HINTS)
        classification = f"{layout}_obsolete" if obsolete else layout
        confidence = "high" if obsolete or layout == "legacy_split_layout" else "medium"
        items.append(
            HygieneItem(
                r,
                "markdown_split_dir",
                classification,
                confidence,
                action,
                f"part_count={len(parts)}",
                lines,
            )
        )
    return items


def can_delete(item: HygieneItem) -> bool:
    if item.recommended_action != "delete_with_patchkit_allowlist":
        return False
    if item.kind != "markdown":
        return False
    if any(item.path.startswith(prefix) for prefix in RISKY_DELETE_PREFIXES):
        return False
    if protected_current_delete_path(item.path):
        return False
    if not item.delete_marker:
        return False
    return item.confidence == "high"


def build_bundle(report: dict[str, Any], root: Path, bundle_path: Path) -> dict[str, Any]:
    operations = []
    for item in report["items"]:
        if not can_delete(HygieneItem(**item)):
            continue
        marker = str(item.get("delete_marker") or "")
        operations.append(
            {
                "operation": "delete_file",
                "target": item["path"],
                "allow_delete": True,
                "required_marker": marker,
                "reason": item["reason"],
            }
        )
    bundle = {
        "schema_version": 1,
        "kind": "codemod_patch_bundle",
        "purpose": "reviewable repository hygiene cleanup generated from build_repo_hygiene_plan.py",
        "operations": operations,
        "validators": ["git_diff_check"],
    }
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {"path": rel(root, bundle_path), "operation_count": len(operations)}
