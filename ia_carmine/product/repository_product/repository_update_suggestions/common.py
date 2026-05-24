"""Shared constants and file readers for repository update suggestions."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/ai_pipeline"
DEFAULT_PACKET_BASENAME = "repository_update_suggestions"
DEFAULT_MAX_CHARS = 6000
IGNORED_PLAN_FILENAMES = {"README.md"}

WORKLOAD_QUALITY_REPORT = "output/validation/ai_workload_report_quality.json"
WORKLOAD_QUALITY_ROUTING_REPORT = "output/validation/ai_workload_quality_lane_routing.json"
NPU_DECODE_REMEDIATION_REPORT = "output/validation/npu_decode_quality_remediation.json"
TRACKED_WORKLOAD_CONTEXT_FILES = (
    "output/ai_packets/npu_real_workload_report.md",
    "output/ai_packets/ollama_gpu_real_workload_report.md",
)

PROFILE_CONTEXT_FILES: dict[str, tuple[str, ...]] = {
    "core": (
        "AGENTS.md",
        "WORKFLOW.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/PROJECT_STATUS_POINT.md",
        "docs/TECH_DEBT_TRACKER.md",
        "docs/REFACTORING_AND_REUSE_PLAN.md",
        "docs/JSON_SCHEMAS.md",
        "tools/npu/pipeline/README.md",
        "Tools/validation/CONTEXT_INDEX.md",
        "Tools/validation/TOOL_CONTEXT.md",
    ),
    "npu": (
        "AGENTS.md",
        "WORKFLOW.md",
        "docs/PROJECT_STATUS_POINT.md",
        "docs/TECH_DEBT_TRACKER.md",
        "docs/REFACTORING_AND_REUSE_PLAN.md",
        "docs/DATA_FLOW.md",
        "docs/JSON_SCHEMAS.md",
        "tools/npu/pipeline/README.md",
        "Tools/validation/CONTEXT_INDEX.md",
        "Tools/validation/TOOL_CONTEXT.md",
        "tools/npu/dual_ai_pipeline/cli.py",
        "tools/npu/provider_mesh/runtime_output_manifest.py",
        "tools/npu/provider_mesh/provider_result_report.py",
        "tools/ai/provider_mesh/local_provider_probe.py",
        "tools/validation/check_ai_workload_report_quality.py",
        "tools/ai/workload_quality.py",
        "tools/ai/build_workload_quality_lane_routing.py",
        "tools/validation/check_npu_decode_quality_remediation.py",
    ),
    "docs": (
        "AGENTS.md",
        "WORKFLOW.md",
        "docs/README.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/PROJECT_STATUS_POINT.md",
        "docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md",
        "docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md",
        "docs/TECH_DEBT_TRACKER.md",
    ),
}

PROFILE_REPORTS: dict[str, tuple[str, ...]] = {
    "core": (
        "output/validation/python_syntax.json",
        "output/validation/ai_pipeline_modules.json",
        "output/validation/npu_pipeline_modules.json",
        "output/validation/npu_pipeline_helper_tests.json",
        "output/validation/npu_pipeline_docs.json",
        "output/validation/provider_result_parsing.json",
        "output/validation/provider_result_report.json",
        WORKLOAD_QUALITY_REPORT,
        WORKLOAD_QUALITY_ROUTING_REPORT,
        NPU_DECODE_REMEDIATION_REPORT,
        "output/validation/npu_runtime_output_manifest.json",
        "output/validation/local_ai_resource_lanes.json",
        "output/validation/local_provider_probe.json",
        "output/validation/execution_plan_status.json",
        "output/validation/validation_report_contract.json",
        "output/validation/docs_links.json",
    ),
    "npu": (
        "output/validation/python_syntax.json",
        "output/validation/npu_pipeline_modules.json",
        "output/validation/npu_pipeline_helper_tests.json",
        "output/validation/npu_pipeline_docs.json",
        "output/validation/provider_result_parsing.json",
        "output/validation/provider_result_report.json",
        WORKLOAD_QUALITY_REPORT,
        WORKLOAD_QUALITY_ROUTING_REPORT,
        NPU_DECODE_REMEDIATION_REPORT,
        "output/validation/npu_runtime_output_manifest.json",
        "output/validation/local_ai_resource_lanes.json",
        "output/validation/local_provider_probe.json",
        "output/validation/execution_plan_status.json",
        "output/validation/validation_report_contract.json",
    ),
    "docs": (
        "output/validation/docs_links.json",
        "output/validation/execution_plan_status.json",
        "output/validation/json_artifacts.json",
        "output/validation/validation_report_contract.json",
    ),
}

def split_path_values(items: list[str]) -> list[str]:
    """Accept repeated args and comma-separated PowerShell values."""

    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out

def unique_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in split_path_values(items):
        normalized = item.replace("\\", "/")
        if normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out

def split_markdown_parts(path: Path) -> list[Path]:
    # Return ordered files for the canonical split Markdown directory layout.
    if not path.is_dir() or not path.name.endswith(".md"):
        return []
    parts: list[Path] = []
    readme = path / "README.md"
    if readme.is_file():
        parts.append(readme)
    parts.extend(sorted(item for item in path.glob("part-*.md") if item.is_file()))
    return parts

def read_split_markdown(path: Path) -> tuple[str, int, str]:
    parts = split_markdown_parts(path)
    if not parts:
        return "", 0, "path is not a file"
    chunks: list[str] = []
    total_chars = 0
    for part in parts:
        text = part.read_text(encoding="utf-8", errors="replace")
        total_chars += len(text)
        chunks.append(f"<!-- split-source: {part.name} -->\n{text.rstrip()}\n")
    return "\n".join(chunks), total_chars, ""

def read_text_if_exists(path: Path, *, max_chars: int) -> dict[str, Any]:
    rel = str(path)
    if not path.exists():
        return {
            "path": rel,
            "exists": False,
            "text": "",
            "chars": 0,
            "truncated": False,
        }

    split_markdown = False
    read_error = ""

    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
        original_len = len(text)
    else:
        text, original_len, read_error = read_split_markdown(path)
        split_markdown = bool(text)
        if read_error:
            return {
                "path": rel,
                "exists": True,
                "text": "",
                "chars": 0,
                "truncated": False,
                "split_markdown": False,
                "read_error": read_error,
            }

    truncated = original_len > max_chars
    if truncated:
        text = text[:max_chars] + "\n...[truncated]"
    return {
        "path": rel,
        "exists": True,
        "text": text,
        "chars": original_len,
        "truncated": truncated,
        "split_markdown": split_markdown,
        "read_error": "",
    }

def read_json_if_exists(path: Path) -> dict[str, Any]:
    rel = str(path)
    if not path.exists():
        return {"path": rel, "exists": False, "data": None, "error": "missing"}
    try:
        return {
            "path": rel,
            "exists": True,
            "data": json.loads(path.read_text(encoding="utf-8-sig")),
            "error": "",
        }
    except Exception as exc:  # noqa: BLE001 - report-only tool.
        return {
            "path": rel,
            "exists": True,
            "data": None,
            "error": f"{type(exc).__name__}: {exc}",
        }

def compact_report_summary(report: dict[str, Any]) -> dict[str, Any]:
    data = report.get("data")
    if not isinstance(data, dict):
        return {
            "path": report["path"],
            "exists": report["exists"],
            "passed": None,
            "error": report.get("error"),
        }
    return {
        "path": report["path"],
        "exists": report["exists"],
        "kind": data.get("kind"),
        "schema_version": data.get("schema_version"),
        "passed": data.get("passed"),
        "errors": (
            data.get("errors", [])[:10]
            if isinstance(data.get("errors"), list)
            else data.get("errors")
        ),
        "warnings": (
            data.get("warnings", [])[:10]
            if isinstance(data.get("warnings"), list)
            else data.get("warnings")
        ),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "checks_keys": (
            sorted((data.get("checks") or {}).keys())[:30]
            if isinstance(data.get("checks"), dict)
            else []
        ),
    }

def _ensure_repo_imports(repo_root: Path) -> None:
    root_text = str(repo_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
