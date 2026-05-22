#!/usr/bin/env python3
"""Run an explicit Ollama/GPU deep planning review over repository evidence.

This is the first long-running deliberative layer for IA-Carmine. Unlike smoke
validators, it is intended to keep a local Ollama model active while repeatedly
reviewing Markdown, code and previously generated agnostic artifacts.

It is still non-destructive:

- provider execution only with --use-ollama;
- no patch application;
- no GitHub PR creation;
- no SQLite writes;
- no persistent memory promotion;
- no Blender runtime execution.
"""

from __future__ import annotations

try:
    from ia_carmine.validation_contracts.schema_repair import build_schema_repair_context_stack
except ImportError:
    import sys as _schema_repair_sys

    _schema_repair_repo_root = Path(__file__).resolve().parents[2]
    if str(_schema_repair_repo_root) not in _schema_repair_sys.path:
        _schema_repair_sys.path.insert(0, str(_schema_repair_repo_root))
    from ia_carmine.validation_contracts.schema_repair import build_schema_repair_context_stack  # type: ignore

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from ia_carmine._shared.runtime_tool_guidance import deterministic_fallback_tool_requests
except ImportError:  # Script-style execution from tools/ai.
    from ia_carmine._shared.runtime_tool_guidance import deterministic_fallback_tool_requests  # type: ignore

try:
    from ia_carmine._shared.gpu_planner_json_contract import (
        result_to_dict,
        validate_model_response_contract,
        validate_recommendation_object,
        validate_tool_request_object,
    )
    from ia_carmine._shared.runtime_tool_guidance import (
        ALLOWED_RUNTIME_TOOLS,
        TOOL_REQUEST_DECISION_GUIDE,
        build_provider_tool_guidance_payload,
    )
    from ia_carmine.providers.ollama.config import DEFAULT_BASE_URL, normalize_base_url
    from ia_carmine.providers.ollama.manager import OllamaModelManager
except ImportError:  # Script-style execution from tools/ai.
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine._shared.gpu_planner_json_contract import (  # type: ignore
        result_to_dict,
        validate_model_response_contract,
        validate_recommendation_object,
        validate_tool_request_object,
    )
    from ia_carmine._shared.runtime_tool_guidance import (  # type: ignore
        ALLOWED_RUNTIME_TOOLS,
        TOOL_REQUEST_DECISION_GUIDE,
        build_provider_tool_guidance_payload,
    )
    from ia_carmine.providers.ollama.config import DEFAULT_BASE_URL, normalize_base_url  # type: ignore
    from ia_carmine.providers.ollama.manager import OllamaModelManager  # type: ignore

DEFAULT_EVIDENCE = "output/ai_pipeline/agent_review_evidence_sufficiency.json"
DEFAULT_REFINED = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review.json"
DEFAULT_OUTPUT = "output/ai_pipeline/agent_gpu_deep_planning_review.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_gpu_deep_planning_review.md"
TEXT_EXTENSIONS = {".md", ".py", ".ps1", ".sh", ".json", ".yaml", ".yml", ".txt"}
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "renders",
}
EMPTY_RECOMMENDATION_REASONS = {
    "context_echo_detected",
    "json_parse_failure",
    "model_output_schema_mismatch",
    "valid_json_empty_recommendations",
    "recommendations_filtered_out",
    "evidence_ready_but_no_gpu_plan",
    "evidence_ready_but_no_tool_requests",
    "model_output_missing_required_fields",
    "repair_attempt_failed",
    "tool_requests_pending",
}


@dataclass(frozen=True)
class ContextFile:
    path: str
    exists: bool
    chars: int
    lines: int
    preview: str


class ContextFile:
    path: str
    exists: bool
    chars: int
    lines: int
    preview: str
def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def safe_read_text(path: Path, max_chars: int) -> tuple[str, bool, str | None]:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return "", False, f"{type(exc).__name__}: {exc}"
    truncated = max_chars > 0 and len(text) > max_chars
    if truncated:
        text = text[:max_chars]
    return text, truncated, None

def context_file(repo_root: Path, path_value: str, max_chars: int) -> ContextFile:
    path = resolve_path(repo_root, path_value)
    if not path.exists() or not path.is_file():
        return ContextFile(
            path=repo_rel(path, repo_root), exists=False, chars=0, lines=0, preview=""
        )
    text, truncated, error = safe_read_text(path, max_chars)
    suffix = "\n...[truncated]" if truncated else ""
    if error:
        suffix = f"\n...[read error: {error}]"
    return ContextFile(
        path=repo_rel(path, repo_root),
        exists=True,
        chars=len(text),
        lines=len(text.splitlines()),
        preview=text + suffix,
    )

def context_to_dict(item: ContextFile) -> dict[str, Any]:
    return {
        "path": item.path,
        "exists": item.exists,
        "chars": item.chars,
        "lines": item.lines,
        "preview": item.preview,
    }

def should_include(path: Path, repo_root: Path) -> bool:
    try:
        rel_parts = path.relative_to(repo_root).parts
    except ValueError:
        return False
    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return False
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    return path.is_file()

def collect_repo_context(
    repo_root: Path, roots: list[str], max_files: int, max_chars_per_file: int
) -> list[ContextFile]:
    results: list[ContextFile] = []
    seen: set[str] = set()
    for root_value in roots:
        root = resolve_path(repo_root, root_value)
        if root.is_file() and should_include(root, repo_root):
            rel = repo_rel(root, repo_root)
            if rel not in seen:
                seen.add(rel)
                results.append(context_file(repo_root, rel, max_chars_per_file))
            continue
        if not root.exists() or not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if len(results) >= max_files:
                return results
            if not should_include(path, repo_root):
                continue
            rel = repo_rel(path, repo_root)
            if rel in seen:
                continue
            seen.add(rel)
            results.append(context_file(repo_root, rel, max_chars_per_file))
    return results

def extract_evidence_files(evidence: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for area in evidence.get("areas", {}).values():
        for item in area.get("items", []) if isinstance(area, dict) else []:
            for file_info in item.get("evidence_files", []):
                path = file_info.get("path") if isinstance(file_info, dict) else None
                if path and path not in paths:
                    paths.append(str(path))
    return paths

def evidence_ready_for_manual_patch_count(evidence: dict[str, Any]) -> int:
    """Return an evidence-ready count without assuming a single report shape.

    Historical evidence reports have used both a root/summary integer and per-item
    readiness markers. The GPU planner should not invent recommendations, but it
    must know whether another deterministic layer already has ready candidates.
    """

    explicit_counts: list[int] = []
    ready_items = 0

    def visit(value: Any) -> None:
        nonlocal ready_items
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "ready_for_manual_patch_count" and isinstance(child, int):
                    explicit_counts.append(child)
                elif (
                    key == "ready_count"
                    and isinstance(child, int)
                    and value.get("kind") == "agent_review_evidence_sufficiency"
                ):
                    explicit_counts.append(child)
                visit(child)
            status = value.get("status") or value.get("classification")
            if isinstance(status, str) and status in {
                "ready_for_manual_patch",
                "ready_for_patch_plan",
            }:
                ready_items += 1
            decision = value.get("decision")
            if isinstance(decision, str) and decision in {
                "ready_for_manual_patch",
                "ready_for_patch_plan",
            }:
                ready_items += 1
            elif isinstance(decision, dict):
                ready = decision.get("ready_for_manual_patch") or decision.get(
                    "ready_for_patch_plan"
                )
                if ready is True:
                    ready_items += 1
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(evidence)
    if explicit_counts:
        return max(explicit_counts)
    return ready_items

def compact_json(data: Any, max_chars: int) -> str:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]"
    return text

def split_batches(items: list[ContextFile], batch_size: int) -> list[list[ContextFile]]:
    if batch_size <= 0:
        return [items]
    return [items[index : index + batch_size] for index in range(0, len(items), batch_size)]
