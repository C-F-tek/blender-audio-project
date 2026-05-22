#!/usr/bin/env python3
"""Build advisory repository change proposals.

The tool is intentionally non-mutating. It reads validation reports, local AI
resource-lane reports and current runtime peer evidence, then writes proposal
JSON/Markdown that a human or trusted agent can review.

It never applies patches, never edits source files and never runs providers.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/ai_pipeline"
DEFAULT_BASENAME = "repository_change_proposals"

DEFAULT_REPORTS = (
    "output/validation/python_syntax.json",
    "output/validation/npu_pipeline_modules.json",
    "output/validation/npu_pipeline_helper_tests.json",
    "output/validation/npu_pipeline_docs.json",
    "output/validation/provider_result_parsing.json",
    "output/validation/provider_result_report.json",
    "output/validation/ai_workload_report_quality.json",
    "output/validation/npu_runtime_output_manifest.json",
    "output/validation/local_ai_resource_lanes.json",
    "output/validation/local_provider_probe.json",
    "output/validation/execution_plan_status.json",
    "output/validation/validation_report_contract.json",
    "output/ai_pipeline/repository_update_suggestions.json",
)

RUNTIME_REPORT_PATTERNS = (
    "output/validation/gpu0_ollama_vulkan_peer*.json",
    "output/validation/**/gpu0_ollama_vulkan_peer*.json",
    "output/validation/**/ollama_gpu0_peer*.json",
    "output/validation/openvino_gpu0_workload_*.json",
    "output/validation/openvino_gpu0_provider_support_*.json",
    "output/validation/npu_micro_peer_*.json",
    "output/validation/npu_micro_task_companion*.json",
    "output/validation/npu_gpu_deep_review_audit*.json",
    "output/ai_pipeline/npu_micro_support_parallel/*.json",
    "output/validation/real_product_preflight_runtime_evidence_correlation.json",
    "output/validation/*runtime_evidence_correlation*.json",
    "output/validation/generated_patch_specs_review_pr_apply*.json",
    "output/validation/patch_suggestion_bundle_apply*.json",
    "output/validation/heap_exchange_runtime_lifecycle_*.json",
    "output/validation/*unified_chain_contract*.json",
    "output/local_ai_runs/*/ai_packets/heap_exchange_runtime_entry.json",
    "output/local_ai_runs/*/ai_packets/heap_peer_runtime_manifest.json",
    "output/local_ai_runs/*/ai_packets/heap_exchange_closure_audit.json",
    "output/local_ai_runs/*/ai_packets/heap_exchange_runtime_exit_product.json",
    "output/patch_specs/*_manifest.json",
)

SUPPORTED_SUGGESTION_OUTPUT_KINDS = (
    "python_code",
    "markdown",
    "json",
    "powershell",
    "workflow_yaml",
    "path_group",
    "text_or_config",
)

CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}

STAMP_RE = re.compile(r"\d{8}-\d{6}")


def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out

def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()

def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "path": str(path), "data": None, "error": "missing"}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return {"exists": True, "path": str(path), "data": data, "error": ""}
    except Exception as exc:  # noqa: BLE001 - advisory report.
        return {
            "exists": True,
            "path": str(path),
            "data": None,
            "error": f"{type(exc).__name__}: {exc}",
        }

def with_source_metadata(report: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    copied = dict(data)
    copied.setdefault("_source_path", str(report.get("path") or ""))
    return copied

def report_by_kind(reports: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_kind: dict[str, dict[str, Any]] = {}
    for report in reports:
        data = report.get("data")
        if isinstance(data, dict):
            kind = str(data.get("kind") or Path(report["path"]).stem)
            by_kind[kind] = with_source_metadata(report, data)
    return by_kind

def reports_by_kind(reports: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_kind: dict[str, list[dict[str, Any]]] = {}
    for report in reports:
        data = report.get("data")
        if isinstance(data, dict):
            kind = str(data.get("kind") or Path(report["path"]).stem)
            by_kind.setdefault(kind, []).append(with_source_metadata(report, data))
    return by_kind

def report_passed(report: dict[str, Any] | None) -> bool:
    return isinstance(report, dict) and report.get("passed") is True

def infer_stamp_from_values(*values: str) -> str:
    for value in values:
        matches = STAMP_RE.findall(str(value or ""))
        if matches:
            return matches[-1]
    return ""

def value_contains_stamp(value: Any, stamp: str, *, depth: int = 0, max_depth: int = 6) -> bool:
    if not stamp or depth > max_depth:
        return False
    if isinstance(value, str):
        return stamp in value
    if isinstance(value, (int, float, bool)) or value is None:
        return stamp in str(value)
    if isinstance(value, dict):
        return any(
            value_contains_stamp(item, stamp, depth=depth + 1, max_depth=max_depth)
            for item in value.values()
        )
    if isinstance(value, list):
        return any(
            value_contains_stamp(item, stamp, depth=depth + 1, max_depth=max_depth)
            for item in value
        )
    return False

def report_matches_stamp(path: Path, data: Any, stamp: str) -> bool:
    if not stamp:
        return True
    if stamp in path.as_posix():
        return True
    if isinstance(data, dict):
        for key in ("Stamp", "stamp", "DataStamp", "generated_stamp"):
            if str(data.get(key) or "") == stamp:
                return True
        return value_contains_stamp(data, stamp)
    return False

def report_time_key(report: dict[str, Any]) -> tuple[str, str]:
    return (
        str(
            report.get("generated_at") or report.get("timestamp") or report.get("created_at") or ""
        ),
        str(report.get("_source_path") or ""),
    )

def latest_report(reports: list[dict[str, Any]]) -> dict[str, Any]:
    if not reports:
        return {}
    return sorted(reports, key=report_time_key)[-1]

def discover_runtime_report_paths(repo_root: Path, stamp: str, max_files: int) -> list[str]:
    candidates: list[Path] = []
    for pattern in RUNTIME_REPORT_PATTERNS:
        candidates.extend(path for path in repo_root.glob(pattern) if path.is_file())
    unique = {path.resolve(): path for path in candidates}
    ordered = sorted(unique.values(), key=lambda item: item.stat().st_mtime, reverse=True)
    selected: list[str] = []
    for path in ordered:
        if len(selected) >= max_files:
            break
        loaded = read_json_if_exists(path)
        data = loaded.get("data")
        if loaded.get("error"):
            continue
        if not report_matches_stamp(path, data, stamp):
            continue
        selected.append(repo_relative(path, repo_root))
    return selected

def classify_target_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.endswith("/") or "*" in normalized:
        return "path_group"
    suffix = Path(normalized).suffix.lower()
    if suffix == ".py":
        return "python_code"
    if suffix == ".md":
        return "markdown"
    if suffix == ".json":
        return "json"
    if suffix == ".ps1":
        return "powershell"
    if suffix in {".yml", ".yaml"}:
        return "workflow_yaml"
    return "text_or_config"

def build_suggestion_outputs(target_files: list[str]) -> list[dict[str, str]]:
    return [
        {
            "path": path,
            "artifact_kind": classify_target_path(path),
            "operation": "manual_patch_suggestion",
            "content_status": "proposal_only",
            "write_policy": "manual_review_only",
        }
        for path in target_files
    ]
