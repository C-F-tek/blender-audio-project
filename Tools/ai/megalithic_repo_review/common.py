#!/usr/bin/env python3
"""Run an explicit all-resources repository review.

This is an artifact-first IA-Carmine helper. It can inspect Markdown, code,
RAW/output artifacts, generated indexes, SQLite memory databases in read-only
mode, NPU/OpenVINO tool definitions and GPU/Ollama tool definitions.

Default behavior is CPU-only and report-only:

- no provider execution unless --use-ollama is explicitly passed;
- no live NPU execution;
- no patch application;
- no source writes except requested JSON/Markdown review outputs;
- no Blender runtime execution;
- no full analysis JSON edits;
- no SQLite DB writes or commits.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sqlite3
import sys
import warnings
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_JSON = "output/ai_pipeline/megalithic_repo_review.json"
DEFAULT_OUTPUT_MD = "output/ai_pipeline/megalithic_repo_review.md"
DEFAULT_PROPOSALS_JSON = "output/ai_pipeline/megalithic_repo_review_proposals.json"

DOC_EXTENSIONS = {".md"}
CODE_EXTENSIONS = {".py", ".ps1", ".sh", ".yaml", ".yml", ".json"}
RAW_EXTENSIONS = {".json", ".jsonl", ".md", ".txt", ".log", ".csv", ".yaml", ".yml"}
SQLITE_EXTENSIONS = {".db", ".sqlite", ".sqlite3"}
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "renders",
}
DEFAULT_REPORTS = (
    "output/validation/docs_contract_drift.json",
    "output/validation/code_contract_drift.json",
    "output/validation/ai_workload_report_quality.json",
    "output/validation/validation_report_contract.json",
    "output/validation/local_ai_resource_lanes.json",
    "output/validation/local_provider_probe.json",
    "output/validation/ai_workload_quality_lane_routing.json",
    "output/validation/npu_decode_quality_remediation.json",
    "output/validation/npu_review_metadata.json",
)
CANONICAL_DOCS = (
    "AGENTS.md",
    "WORKFLOW.md",
    "docs/AI_DOCS_ENTRYPOINT.md",
    "docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md",
    "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md",
    "docs/JSON_SCHEMAS.md",
    "tools/validation/README.md",
)
CONTRACT_TERMS = (
    "provider_execution_performed",
    "patch_application_performed",
    "manual_review_only",
    "ai_workload_report_quality",
    "code_contract_drift",
    "docs_contract_drift",
    "NPU",
    "Ollama",
)
PROVIDER_TERMS = {
    "npu": ("NPU", "OpenVINO", "openvino", "openvino_genai", "npu"),
    "gpu_cuda": ("Ollama", "ollama", "gpu_cuda", "CUDA", "cuda", "GPU"),
    "cpu": ("CPU", "cpu", "validation", "contract", "report"),
}
COMMON_DUPLICATE_SYMBOLS = {
    "main",
    "read_text",
    "read_json_if_exists",
    "render_markdown",
    "now_iso",
    "split_path_values",
    "resolve_output_path",
    "write_json_report",
}
PATH_RE = re.compile(r"(?:[A-Za-z0-9_.-]+/)+(?:[A-Za-z0-9_.-]+)(?:\.[A-Za-z0-9_.-]+)?")
POWERSHELL_FUNC_RE = re.compile(r"(?im)^\s*function\s+([A-Za-z0-9_-]+)\s*(?:\{|$)")
SHELL_FUNC_RE = re.compile(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\)\s*\{")
MD_HEADING_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")


@dataclass(frozen=True)
class FileRecord:
    path: str
    extension: str
    kind: str
    chars: int
    lines: int
    symbols: tuple[str, ...]
    headings: tuple[str, ...]
def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized.replace("\\", "/"))
    return out

def is_excluded(path: Path, repo_root: Path, *, include_output: bool, include_index: bool) -> bool:
    rel_parts = path.relative_to(repo_root).parts
    excludes = set(DEFAULT_EXCLUDE_DIRS)
    if not include_output:
        excludes.add("output")
    if not include_index:
        excludes.add("indexAI")
    return any(part in excludes for part in rel_parts)

def iter_files(
    repo_root: Path,
    *,
    include_all_docs: bool,
    include_all_code: bool,
    include_output: bool,
    include_index: bool,
    include_raw: bool,
    include_sqlite_memory: bool,
    max_files: int,
) -> tuple[list[Path], list[Path], list[Path], list[Path]]:
    docs: list[Path] = []
    code: list[Path] = []
    raw: list[Path] = []
    sqlite_files: list[Path] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        if is_excluded(
            path,
            repo_root,
            include_output=include_output or include_raw,
            include_index=include_index,
        ):
            continue
        suffix = path.suffix.lower()
        rel = path.relative_to(repo_root).as_posix()
        if suffix in DOC_EXTENSIONS and (
            include_all_docs or rel.startswith(("docs/", "tools/", "AGENTS", "WORKFLOW"))
        ):
            docs.append(path)
        elif suffix in CODE_EXTENSIONS and (
            include_all_code or rel.startswith(("tools/", "Scripting/", "docs/"))
        ):
            code.append(path)
        if (
            include_raw
            and suffix in RAW_EXTENSIONS
            and rel.startswith(("output/", "docs/LOCAL_VALIDATION_EVIDENCE/", "indexAI/"))
        ):
            raw.append(path)
        if include_sqlite_memory and suffix in SQLITE_EXTENSIONS:
            sqlite_files.append(path)
        if max_files > 0 and len(docs) + len(code) + len(raw) + len(sqlite_files) >= max_files:
            break
    return docs, code, raw, sqlite_files

def read_text(path: Path, max_chars: int = 0) -> tuple[str, bool, str | None]:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return "", False, f"{type(exc).__name__}: {exc}"
    truncated = bool(max_chars > 0 and len(text) > max_chars)
    if truncated:
        text = text[:max_chars]
    return text, truncated, None

def python_symbols(text: str) -> tuple[str, ...]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(text)
    except SyntaxError:
        return tuple(
            sorted(set(re.findall(r"(?m)^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", text)))
        )
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(node.name)
    return tuple(sorted(set(names)))

def extract_symbols(path: Path, text: str) -> tuple[str, ...]:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return python_symbols(text)
    if suffix == ".ps1":
        return tuple(sorted(set(POWERSHELL_FUNC_RE.findall(text))))
    if suffix == ".sh":
        return tuple(sorted(set(SHELL_FUNC_RE.findall(text))))
    return ()

def extract_headings(text: str) -> tuple[str, ...]:
    return tuple(item.strip()[:160] for item in MD_HEADING_RE.findall(text))

def build_file_records(
    repo_root: Path, files: Iterable[Path], *, max_chars_per_file: int
) -> list[FileRecord]:
    records: list[FileRecord] = []
    for path in files:
        text, _truncated, error = read_text(path, max_chars_per_file)
        if error:
            continue
        rel = path.relative_to(repo_root).as_posix()
        suffix = path.suffix.lower()
        kind = "doc" if suffix in DOC_EXTENSIONS else "code"
        records.append(
            FileRecord(
                path=rel,
                extension=suffix,
                kind=kind,
                chars=len(text),
                lines=len(text.splitlines()),
                symbols=extract_symbols(path, text),
                headings=extract_headings(text) if suffix in DOC_EXTENSIONS else (),
            )
        )
    return records

def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "data": None, "error": "missing"}
    try:
        return {
            "path": str(path),
            "exists": True,
            "data": json.loads(path.read_text(encoding="utf-8-sig")),
            "error": "",
        }
    except Exception as exc:
        return {
            "path": str(path),
            "exists": True,
            "data": None,
            "error": f"{type(exc).__name__}: {exc}",
        }
