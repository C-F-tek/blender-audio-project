from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from Tools.ai.patch_product.patch_plan_quality_product.io_utils import read_text, repo_rel, resolve

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _compact_lines(text: str, limit: int = 12) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("```"):
            continue
        lines.append(line[:240])
        if len(lines) >= limit:
            break
    return lines


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        match = HEADING_RE.match(line.strip())
        if match:
            return match.group(2).strip()
    return ""


def _headings(text: str, limit: int = 16) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        match = HEADING_RE.match(line.strip())
        if match:
            out.append(match.group(2).strip()[:160])
        if len(out) >= limit:
            break
    return out


def _objective_hint(text: str) -> str:
    lower_keys = ("obiettivo", "objective", "scope", "focus", "scopo")
    lines = text.splitlines()
    for index, raw in enumerate(lines):
        if any(key in raw.lower() for key in lower_keys):
            window = " ".join(item.strip() for item in lines[index : index + 6] if item.strip())
            return window[:700]
    return " ".join(_compact_lines(text, limit=5))[:700]


def load_task_markdown(repo_root: Path, task_markdown: str) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    path = resolve(repo_root, task_markdown) if task_markdown else Path("")
    text = read_text(path) if task_markdown else ""
    if not task_markdown:
        return {
            "provided": False,
            "path": "",
            "task_digest": "",
            "title": "",
            "headings": [],
            "excerpt": [],
        }, ["task_markdown_not_provided"]
    if not text:
        return {
            "provided": True,
            "path": repo_rel(path, repo_root),
            "task_digest": "",
            "title": "",
            "headings": [],
            "excerpt": [],
        }, [f"task_markdown_missing_or_empty: {repo_rel(path, repo_root)}"]
    digest = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    return {
        "provided": True,
        "path": repo_rel(path, repo_root),
        "task_digest": digest,
        "title": _first_heading(text),
        "headings": _headings(text),
        "excerpt": _compact_lines(text),
        "line_count": text.count("\n") + (0 if text.endswith("\n") else 1),
        "char_count": len(text),
        "objective_hint": _objective_hint(text),
    }, warnings


def build_request_summary(
    task: dict[str, Any], branch: str, commit: str, issue: str
) -> dict[str, Any]:
    return {
        "title": task.get("title") or "Untitled local AI task",
        "input_md_path": task.get("path") or "",
        "task_digest": task.get("task_digest") or "",
        "headings": task.get("headings") or [],
        "excerpt": task.get("excerpt") or [],
        "related_branch": branch,
        "related_commit": commit,
        "related_issue": issue,
    }
