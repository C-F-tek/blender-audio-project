#!/usr/bin/env python3
"""Synthesize schema-valid GPU planner recommendations from evidence reports.

This tool is deliberately deterministic and report-only. It is the bridge between
runtime evidence/tool reports and the GPU planner JSON recommendation contract
when the provider returned zero usable recommendations because of parse or schema
failures.

It never executes providers, never applies patches, never writes SQLite memory,
never runs Blender and never creates GitHub PRs.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai._shared.code_patch_plan_common import normalize_repo_path, read_json_object
    from Tools.ai._shared.gpu_planner_json_contract import validate_recommendation_object
    from Tools.validation._shared.report_utils import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai._shared.code_patch_plan_common import (  # type: ignore
        normalize_repo_path,
        read_json_object,
    )
    from Tools.ai._shared.gpu_planner_json_contract import validate_recommendation_object  # type: ignore
    from Tools.validation._shared.report_utils import write_json_report, write_text_report  # type: ignore

DEFAULT_EVIDENCE = "output/ai_pipeline/agent_review_evidence_sufficiency.json"
DEFAULT_ORCHESTRATOR = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json"
DEFAULT_OUTPUT = "output/ai_pipeline/deterministic_recommendations.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/deterministic_recommendations.md"

REPORT_KIND = "deterministic_recommendation_synthesizer"
DEFAULT_VALIDATION_COMMANDS = [
    "python -m Tools.validation check_python_syntax --repo-root . --output output/validation/python_syntax.json",
    "python -m Tools.validation check_validation_report_contract --repo-root . --output output/validation/validation_report_contract.json",
    "git diff --check",
    "git status --short",
]
SUBSTANTIVE_CONSISTENCY_FINDING_PRIORITIES = {
    "python_import_missing": 10,
    "python_import_symbol_missing": 11,
    "md_python_command_script_missing": 20,
    "md_mentions_missing_powershell_path": 30,
    "md_cli_arg_not_in_argparse": 40,
    "md_mentions_missing_python_path": 50,
    "md_mentions_missing_markdown_path": 60,
    "documented_python_script_without_obvious_smoke": 70,
}
COSMETIC_FINDING_KEYWORDS = (
    "whitespace",
    "space-only",
    "spacing-only",
    "tag spacing",
    "tag-spacing",
    "formatting-only",
    "cosmetic",
)
FORBIDDEN_TARGET_PREFIXES = (
    "output/",
    "renders/",
    ".git/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)
FORBIDDEN_TARGET_FRAGMENTS = (
    "full_analysis",
    "analysis_full",
)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()

def load_report(path: Path, *, missing_is_error: bool = True) -> tuple[dict[str, Any], list[str]]:
    data, errors = read_json_object(path, missing_is_error=missing_is_error)
    return data, [f"{repo_rel(path, path.parents[0])}: {error}" for error in errors]

def load_report_at(
    repo_root: Path, value: str | Path, *, missing_is_error: bool = True
) -> tuple[dict[str, Any], list[str]]:
    path = resolve_path(repo_root, value)
    data, errors = read_json_object(path, missing_is_error=missing_is_error)
    return data, [f"{repo_rel(path, repo_root)}: {error}" for error in errors]

def unique_strings(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = normalize_repo_path(value)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result

def target_path_error(path_value: str, repo_root: Path) -> str | None:
    normalized = normalize_repo_path(path_value)
    if not normalized:
        return "empty target path"
    if Path(normalized).is_absolute():
        return "absolute target paths are not allowed"
    full = (repo_root / normalized).resolve(strict=False)
    try:
        full.relative_to(repo_root.resolve(strict=False))
    except ValueError:
        return "target path escapes repository root"
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_TARGET_PREFIXES):
        return f"forbidden generated/runtime target prefix: {normalized}"
    lower = normalized.lower()
    if any(fragment in lower for fragment in FORBIDDEN_TARGET_FRAGMENTS) and lower.endswith(
        ".json"
    ):
        return f"forbidden full-analysis JSON target: {normalized}"
    if "*" in normalized or normalized.endswith("/"):
        return "target is a glob or directory, not a concrete file"
    if not full.exists():
        return "target file does not exist"
    if not full.is_file():
        return "target is not a file"
    return None

def evidence_ready_for_manual_patch_count(evidence: dict[str, Any]) -> int:
    explicit_counts: list[int] = []
    ready_items = 0

    def visit(value: Any) -> None:
        nonlocal ready_items
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "ready_for_manual_patch_count" and isinstance(child, int):
                    explicit_counts.append(child)
                visit(child)
            if value.get("evidence_sufficient") is True:
                ready_items += 1
            status = value.get("status") or value.get("classification")
            if isinstance(status, str) and status in {
                "ready_for_manual_patch",
                "ready_for_patch_plan",
            }:
                ready_items += 1
            decision = value.get("decision")
            if isinstance(decision, dict):
                if (
                    decision.get("ready_for_manual_patch") is True
                    or decision.get("ready_for_patch_plan") is True
                ):
                    ready_items += 1
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(evidence)
    if explicit_counts:
        return max(explicit_counts)
    return ready_items

def compact_evidence_files(item: dict[str, Any]) -> list[str]:
    compact: list[str] = []
    raw = item.get("evidence_files")
    if not isinstance(raw, list):
        return compact
    for evidence_file in raw[:8]:
        if not isinstance(evidence_file, dict):
            continue
        path = normalize_repo_path(evidence_file.get("path"))
        if path:
            compact.append(path)
    return compact

def npu_audit_refs(orchestrator: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    raw_audits = orchestrator.get("npu_audits")
    if not isinstance(raw_audits, list):
        return refs
    for audit in raw_audits[:8]:
        if not isinstance(audit, dict):
            continue
        refs.append(
            {
                "round": audit.get("round"),
                "status": audit.get("status"),
                "classification": audit.get("classification"),
                "runtime_tool_context_seen": audit.get("runtime_tool_context_seen"),
                "npu_tool_request_count": audit.get("npu_tool_request_count"),
                "npu_runtime_tool_execution_count": audit.get("npu_runtime_tool_execution_count"),
                "npu_runtime_tool_failed_count": audit.get("npu_runtime_tool_failed_count"),
                "npu_runtime_tool_blocked_count": audit.get("npu_runtime_tool_blocked_count"),
            }
        )
    return refs

def summarize_tool_report(path: Path, repo_root: Path, data: dict[str, Any]) -> dict[str, Any]:
    summary = data.get("summary") if isinstance(data.get("summary"), dict) else {}
    return {
        "path": repo_rel(path, repo_root),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "tool_request_count": data.get("tool_request_count") or summary.get("tool_request_count"),
        "tool_execution_count": data.get("tool_execution_count")
        or summary.get("tool_execution_count"),
        "failed_tool_count": data.get("failed_tool_count") or summary.get("failed_tool_count"),
        "blocked_tool_count": data.get("blocked_tool_count") or summary.get("blocked_tool_count"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "patch_application_performed": data.get("patch_application_performed"),
    }

def recommendation_schema_errors(rec: dict[str, Any], index: int, repo_root: Path) -> list[str]:
    errors = validate_recommendation_object(rec, index)
    for target in rec.get("target_files", []) if isinstance(rec.get("target_files"), list) else []:
        target_error = target_path_error(str(target), repo_root)
        if target_error:
            errors.append(f"recommendations[{index}].target_files {target!r}: {target_error}")
    return errors

def recommendation_key(rec: dict[str, Any]) -> str:
    return json.dumps(
        [
            rec.get("area"),
            rec.get("status"),
            rec.get("target_files"),
            rec.get("proposed_strategy"),
        ],
        sort_keys=True,
        ensure_ascii=False,
    )
