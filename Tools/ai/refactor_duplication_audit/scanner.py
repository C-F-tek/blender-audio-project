"""Python source scanning for refactor duplication audits."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

from .common import (
    DEFAULT_EXCLUDE_PARTS,
    LINE_COUNT_SHARED_DELEGATION_TOKENS,
    read_text,
    repo_rel,
    resolve_path,
)

def iter_python_files(repo_root: Path, roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_root in roots:
        root = resolve_path(repo_root, raw_root)
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() == ".py":
            files.append(root)
            continue
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            rel_parts = (
                set(path.relative_to(repo_root).parts)
                if path.is_relative_to(repo_root)
                else set(path.parts)
            )
            if any(part in rel_parts for part in DEFAULT_EXCLUDE_PARTS):
                continue
            files.append(path)
    unique: dict[str, Path] = {}
    for path in files:
        unique[path.resolve(strict=False).as_posix()] = path
    return sorted(unique.values(), key=lambda item: repo_rel(item, repo_root).lower())

def collect_functions(repo_root: Path, files: list[Path]) -> tuple[list[dict[str, Any]], list[str]]:
    functions: list[dict[str, Any]] = []
    warnings: list[str] = []
    for path in files:
        text, error = read_text(path)
        if error:
            warnings.append(f"{repo_rel(path, repo_root)}: {error}")
            continue
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            warnings.append(
                f"{repo_rel(path, repo_root)}: SyntaxError line {exc.lineno}: {exc.msg}"
            )
            continue
        lines = text.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            start = getattr(node, "lineno", 1)
            end = getattr(node, "end_lineno", start)
            body = "\n".join(lines[max(start - 1, 0) : min(end, len(lines))])
            functions.append(
                {
                    "name": node.name,
                    "path": repo_rel(path, repo_root),
                    "line_start": start,
                    "line_end": end,
                    "line_count": max(1, end - start + 1),
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "body_hash_seed": re.sub(r"\s+", " ", body.strip())[:500],
                    "uses_shared_line_count_helper": any(
                        token in body for token in LINE_COUNT_SHARED_DELEGATION_TOKENS
                    ),
                }
            )
    return functions, warnings

def files_involved(items: list[dict[str, Any]], limit: int = 16) -> list[str]:
    values = [f"{item['path']}#L{item['line_start']}-L{item['line_end']}" for item in items]
    return values[:limit]
