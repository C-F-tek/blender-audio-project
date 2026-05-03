#!/usr/bin/env python3
"""Build shared-toolbox AI-to-AI final summaries and compact evidence bundles.

Report-only builder for issue #141.

The tool reads existing reports, writes:
- output/analysis/shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
- output/analysis/shared_toolbox_ai_to_ai_final_summary_<STAMP>.md
- docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
- docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md
- optionally output/validation/shared_toolbox_ai_to_ai_bundle_<STAMP>_validation.json

It delegates compact bundle creation to Tools.ai.build_github_evidence_bundle.build_bundle
and optional validation to Tools.validation.check_github_evidence_bundle.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

try:
    from Tools.ai.build_github_evidence_bundle import build_bundle
    from Tools.ai.github_evidence_bundle_io import (
        raw_artifact_content_allowed,
        read_json,
        read_text,
        repo_relative,
        resolve_repo_path,
        split_path_values,
    )
    from Tools.validation.check_github_evidence_bundle import validate_github_evidence_bundles
    from Tools.validation.report_utils import resolve_output_path, write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.build_github_evidence_bundle import build_bundle
    from Tools.ai.github_evidence_bundle_io import (
        raw_artifact_content_allowed,
        read_json,
        read_text,
        repo_relative,
        resolve_repo_path,
        split_path_values,
    )
    from Tools.validation.check_github_evidence_bundle import validate_github_evidence_bundles
    from Tools.validation.report_utils import resolve_output_path, write_json_report


DEFAULT_STAMP_FORMAT = "%Y%m%d-%H%M%S"
DEFAULT_BASENAME_PREFIX = "shared_toolbox_ai_to_ai_bundle"
DEFAULT_FINAL_SUMMARY_PREFIX = "shared_toolbox_ai_to_ai_final_summary"
DEFAULT_CHUNK_SIZE_LINES = 200
DEFAULT_RECURSIVE_MAX_FILES = 120
DEFAULT_RECURSIVE_REPORT_ROOTS: tuple[str, ...] = (
    "output/validation",
    "output/analysis",
    "output/ai_pipeline",
)
DEFAULT_RECURSIVE_ARTIFACT_ROOTS: tuple[str, ...] = (
    "output/analysis",
    "output/ai_pipeline",
    "docs/LOCAL_AI_TASKS",
)
DEFAULT_RECURSIVE_EXCLUDE_GLOBS: tuple[str, ...] = (
    "output/ai_pipeline/*checkpoints*",
    "output/ai_context_packs/*",
    "indexAI/code_chunks/*",
    "indexAI/project_code_chunks/*",
    "renders/*",
    "*.db",
    "*.sqlite",
    "*.sqlite-wal",
    "*.sqlite-shm",
    "*full_analysis*",
    "*analysis_full*",
)

RUNTIME_TOOL_CAPABILITIES: tuple[dict[str, Any], ...] = (
    {
        "tool_name": "build_python_line_count_csv",
        "category": "inventory",
        "safe_default_mode": "report-only",
        "what_it_can_do": [
            "build deterministic Python line-count CSV/JSON/Markdown evidence",
            "support refactor prioritization and large-file drift analysis",
            "provide compact inventory input for local AI review loops",
        ],
        "what_it_must_not_do": ["modify source files", "execute providers", "decide patch application automatically"],
        "recommended_next_use": "Run before large refactor planning to refresh the Python inventory.",
    },
    {
        "tool_name": "build_agent_memory_inventory",
        "category": "memory_inventory",
        "safe_default_mode": "report-only",
        "what_it_can_do": [
            "summarize durable project memory state",
            "surface stale memory assumptions",
            "prepare compact handoff evidence",
        ],
        "what_it_must_not_do": ["write persistent memory", "change SQLite state", "promote advisory lanes"],
        "recommended_next_use": "Use after architecture changes to verify memory alignment.",
    },
    {
        "tool_name": "build_agent_agnostic_tool_inventory",
        "category": "tool_inventory",
        "safe_default_mode": "report-only",
        "what_it_can_do": [
            "inventory local IA tools without provider-specific assumptions",
            "confirm broker/orchestrator tools are discoverable",
            "detect duplicated or missing capabilities",
        ],
        "what_it_must_not_do": ["execute arbitrary shell commands", "run providers", "apply patches"],
        "recommended_next_use": "Use when the shared toolbox surface changes.",
    },
    {
        "tool_name": "build_agent_transient_request_context",
        "category": "context",
        "safe_default_mode": "report-only",
        "what_it_can_do": [
            "assemble request-scoped context packets",
            "combine task Markdown, architecture docs and compact evidence",
            "preserve task intent without relying on chat history",
        ],
        "what_it_must_not_do": ["write persistent memory", "apply patches", "include raw oversized output artifacts unbounded"],
        "recommended_next_use": "Use before GPU/NPU planning when context needs to be refreshed.",
    },
    {
        "tool_name": "check_python_syntax",
        "category": "validation",
        "safe_default_mode": "report-only",
        "what_it_can_do": ["compile-check Python files", "catch syntax regressions", "produce validation JSON evidence"],
        "what_it_must_not_do": ["execute provider workloads", "run Blender runtime", "modify source files"],
        "recommended_next_use": "Run after modifying Python tools or validation smoke tests.",
    },
    {
        "tool_name": "check_validation_report_contract",
        "category": "validation",
        "safe_default_mode": "report-only",
        "what_it_can_do": [
            "validate generated report contract fields",
            "catch malformed guardrail metadata",
            "gate evidence before bundling",
        ],
        "what_it_must_not_do": ["repair reports in place", "run providers", "apply patches"],
        "recommended_next_use": "Run before compact evidence bundle generation.",
    },
    {
        "tool_name": "run_gpu_planner_json_contract_smoke",
        "category": "contract_smoke",
        "safe_default_mode": "no-provider report-only",
        "what_it_can_do": [
            "validate GPU planner JSON/tool request contract handling",
            "exercise malformed/empty output classification",
            "check contract parser behavior without real providers",
        ],
        "what_it_must_not_do": ["call Ollama or other providers", "apply model-proposed patches", "write source code"],
        "recommended_next_use": "Run before provider-backed GPU/NPU planning cycles.",
    },
    {
        "tool_name": "build_code_interpreter_report",
        "category": "static_analysis",
        "safe_default_mode": "report-only",
        "what_it_can_do": [
            "inventory code structure",
            "surface helper reuse/refactor candidates",
            "generate static analysis evidence",
        ],
        "what_it_must_not_do": ["execute generated code", "apply patches", "change provider/model settings"],
        "recommended_next_use": "Use for manual-review refactor planning.",
    },
    {
        "tool_name": "runtime_sqlite_memory",
        "category": "memory_status",
        "safe_default_mode": "read-only status/search",
        "what_it_can_do": [
            "read controlled persistent/operational memory status",
            "confirm no unauthorized persistent writes occurred",
            "produce memory-routing evidence",
        ],
        "what_it_must_not_do": [
            "write persistent memory without explicit authorization",
            "commit SQLite files",
            "bypass broker allowlists",
        ],
        "recommended_next_use": "Use only via broker with action=status/search and explicit scope.",
    },
)

DEFAULT_REPORT_TEMPLATES: tuple[str, ...] = (
    "output/validation/shared_toolbox_python_syntax_{stamp}.json",
    "output/analysis/shared_toolbox_code_interpreter_{stamp}.json",
    "output/validation/shared_toolbox_gpu_contract_smoke_{stamp}.json",
    "output/validation/shared_toolbox_gpu_routing_{stamp}.json",
    "output/validation/shared_toolbox_npu_execution_{stamp}.json",
    "output/validation/shared_toolbox_npu_contract_{stamp}.json",
    "output/validation/npu_provider_environment_shared_toolbox_{stamp}.json",
    "output/ai_pipeline/shared_toolbox_ai_to_ai_{stamp}_orchestrator.json",
    "output/ai_pipeline/shared_toolbox_ai_to_ai_{stamp}_gpu.json",
    "output/analysis/shared_toolbox_gpu_npu_sync_{stamp}.json",
    "output/analysis/shared_toolbox_gpu_contract_replay_{stamp}.json",
)

DEFAULT_ARTIFACT_TEMPLATES: tuple[str, ...] = (
    "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md",
    "docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md",
    "output/analysis/shared_toolbox_code_interpreter_{stamp}.md",
    "output/ai_pipeline/shared_toolbox_ai_to_ai_{stamp}_orchestrator.md",
    "output/ai_pipeline/shared_toolbox_ai_to_ai_{stamp}_gpu.md",
    "output/analysis/shared_toolbox_gpu_npu_sync_{stamp}.md",
    "output/analysis/shared_toolbox_gpu_contract_replay_{stamp}.md",
    "output/analysis/shared_toolbox_ai_to_ai_final_summary_{stamp}.md",
)


def read_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Read a JSON object while reusing shared evidence-bundle IO helpers."""
    data = read_json(path)
    if data is not None:
        return data, None
    if not path.exists():
        return None, "missing"
    text, read_error = read_text(path)
    if read_error:
        return None, read_error
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    if not isinstance(parsed, dict):
        return None, f"expected JSON object, got {type(parsed).__name__}"
    return parsed, None


def bool_from_report(data: dict[str, Any], key: str) -> bool:
    return data.get(key) is True


def existing_report_paths(repo_root: Path, raw_paths: list[str], *, include_missing_optional: bool) -> tuple[list[str], list[dict[str, Any]]]:
    reports: list[str] = []
    missing: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_paths:
        path = resolve_repo_path(repo_root, raw)
        rel = repo_relative(path, repo_root)
        if rel in seen:
            continue
        seen.add(rel)
        if path.exists():
            reports.append(rel)
        else:
            missing.append({"path": rel, "reason": "optional report missing"})
            if include_missing_optional:
                reports.append(rel)
    return reports, missing


def existing_artifact_paths(repo_root: Path, raw_paths: list[str], *, include_missing_optional: bool) -> tuple[list[str], list[dict[str, Any]]]:
    artifacts: list[str] = []
    missing: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_paths:
        path = resolve_repo_path(repo_root, raw)
        rel = repo_relative(path, repo_root)
        if rel in seen:
            continue
        seen.add(rel)
        if path.exists():
            artifacts.append(rel)
        else:
            missing.append({"path": rel, "reason": "optional artifact missing"})
            if include_missing_optional:
                artifacts.append(rel)
    return artifacts, missing


def report_templates_for_stamp(stamp: str) -> list[str]:
    return [item.format(stamp=stamp) for item in DEFAULT_REPORT_TEMPLATES]


def artifact_templates_for_stamp(stamp: str) -> list[str]:
    return [item.format(stamp=stamp) for item in DEFAULT_ARTIFACT_TEMPLATES]


def path_matches_any_glob(rel_path: str, patterns: tuple[str, ...] | list[str]) -> bool:
    normalized = rel_path.replace("\\", "/")
    return any(fnmatch(normalized, pattern.replace("\\", "/")) for pattern in patterns)


def discover_recursive_files(
    repo_root: Path,
    roots: list[str],
    suffixes: tuple[str, ...],
    *,
    stamp: str,
    max_files: int,
    include_unstamped: bool,
    exclude_globs: tuple[str, ...] | list[str] = DEFAULT_RECURSIVE_EXCLUDE_GLOBS,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Discover bounded recursive default files under safe roots."""
    discovered: list[str] = []
    skipped: list[dict[str, Any]] = []
    seen: set[str] = set()

    for root in roots:
        root_path = resolve_repo_path(repo_root, root)
        root_rel = repo_relative(root_path, repo_root)
        if not root_path.exists():
            skipped.append({"path": root_rel, "reason": "recursive root missing"})
            continue
        if not root_path.is_dir():
            skipped.append({"path": root_rel, "reason": "recursive root is not a directory"})
            continue
        for path in sorted(root_path.rglob("*")):
            if len(discovered) >= max_files:
                skipped.append({"path": root_rel, "reason": f"recursive max files reached: {max_files}"})
                return discovered, skipped
            if not path.is_file():
                continue
            if path.suffix.lower() not in suffixes:
                continue
            rel = repo_relative(path, repo_root)
            if path_matches_any_glob(rel, exclude_globs):
                skipped.append({"path": rel, "reason": "excluded by recursive guardrail"})
                continue
            if not raw_artifact_content_allowed(rel):
                skipped.append({"path": rel, "reason": "content denied by shared evidence-bundle policy"})
                continue
            if not include_unstamped and stamp not in path.name and stamp not in rel:
                skipped.append({"path": rel, "reason": "stamp not present in file name/path"})
                continue
            if rel in seen:
                continue
            discovered.append(rel)
            seen.add(rel)
    return discovered, skipped


def file_line_count(path: Path) -> int | None:
    """Return physical line count using shared defensive text reader."""
    text, error = read_text(path)
    if error:
        return None
    return len(text.splitlines())


def build_chunked_file_index(
    repo_root: Path,
    paths: list[str],
    *,
    max_lines_per_chunk: int,
) -> list[dict[str, Any]]:
    """Build pointer-style chunk metadata for large JSON/Markdown artifacts."""
    index: list[dict[str, Any]] = []
    if max_lines_per_chunk <= 0:
        return index

    seen: set[str] = set()
    for rel in paths:
        path = resolve_repo_path(repo_root, rel)
        normalized = repo_relative(path, repo_root)
        if normalized in seen or path.suffix.lower() not in {".json", ".md"}:
            continue
        seen.add(normalized)
        line_count = file_line_count(path)
        if line_count is None or line_count <= max_lines_per_chunk:
            continue

        chunks: list[dict[str, Any]] = []
        chunk_count = (line_count + max_lines_per_chunk - 1) // max_lines_per_chunk
        for index_number in range(chunk_count):
            start = index_number * max_lines_per_chunk + 1
            end = min((index_number + 1) * max_lines_per_chunk, line_count)
            chunk_id = f"{normalized}#L{start}-L{end}"
            previous_id = None
            next_id = None
            if index_number > 0:
                prev_start = (index_number - 1) * max_lines_per_chunk + 1
                prev_end = min(index_number * max_lines_per_chunk, line_count)
                previous_id = f"{normalized}#L{prev_start}-L{prev_end}"
            if index_number + 1 < chunk_count:
                next_start = (index_number + 1) * max_lines_per_chunk + 1
                next_end = min((index_number + 2) * max_lines_per_chunk, line_count)
                next_id = f"{normalized}#L{next_start}-L{next_end}"
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "path": normalized,
                    "line_start": start,
                    "line_end": end,
                    "previous_chunk_id": previous_id,
                    "next_chunk_id": next_id,
                    "has_previous": previous_id is not None,
                    "has_next": next_id is not None,
                }
            )
        index.append(
            {
                "path": normalized,
                "suffix": path.suffix.lower(),
                "line_count": line_count,
                "chunk_size_lines": max_lines_per_chunk,
                "chunk_count": len(chunks),
                "chunks": chunks,
            }
        )
    return index


def coalesce_list(*values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for items in values:
        for item in split_path_values(items):
            if item not in seen:
                result.append(item)
                seen.add(item)
    return result


def collect_report_facts(repo_root: Path, report_paths: list[str]) -> dict[str, Any]:
    reports_generated: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    provider_execution_performed = False
    patch_application_performed = False
    source_writes_performed = False
    sqlite_write_performed = False
    persistent_memory_write_performed = False
    blender_runtime_execution_performed = False
    tool_requests: list[dict[str, Any]] = []

    for rel in report_paths:
        path = resolve_repo_path(repo_root, rel)
        data, parse_error = read_json_object(path)
        entry: dict[str, Any] = {
            "path": repo_relative(path, repo_root),
            "exists": path.exists(),
            "json_ok": data is not None,
            "kind": data.get("kind") if data else None,
            "passed": data.get("passed") if data else None,
        }
        if parse_error and parse_error != "missing":
            entry["parse_error"] = parse_error
            warnings.append(f"{entry['path']}: {parse_error}")
        if data:
            provider_execution_performed = provider_execution_performed or bool_from_report(data, "provider_execution_performed")
            patch_application_performed = patch_application_performed or bool_from_report(data, "patch_application_performed")
            source_writes_performed = source_writes_performed or bool_from_report(data, "source_writes_performed")
            sqlite_write_performed = sqlite_write_performed or bool_from_report(data, "sqlite_write_performed")
            persistent_memory_write_performed = persistent_memory_write_performed or bool_from_report(data, "persistent_memory_write_performed")
            blender_runtime_execution_performed = blender_runtime_execution_performed or bool_from_report(data, "blender_runtime_execution_performed")
            if isinstance(data.get("errors"), list):
                errors.extend(str(item) for item in data.get("errors", []) if item)
            if isinstance(data.get("warnings"), list):
                warnings.extend(str(item) for item in data.get("warnings", []) if item)
            for key in ("tool_requests", "runtime_tool_requests"):
                raw = data.get(key)
                if isinstance(raw, list):
                    for request in raw:
                        if isinstance(request, dict):
                            tool_requests.append(
                                {
                                    "source_report": repo_relative(path, repo_root),
                                    "id": request.get("id"),
                                    "tool": request.get("tool"),
                                    "reason": request.get("reason"),
                                    "args": request.get("args") if isinstance(request.get("args"), dict) else {},
                                }
                            )
        reports_generated.append(entry)

    return {
        "reports_generated": reports_generated,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": provider_execution_performed,
        "patch_application_performed": patch_application_performed,
        "source_writes_performed": source_writes_performed,
        "sqlite_write_performed": sqlite_write_performed,
        "persistent_memory_write_performed": persistent_memory_write_performed,
        "blender_runtime_execution_performed": blender_runtime_execution_performed,
        "tool_requests_executed_or_proposed": tool_requests,
    }


def default_tool_requests() -> list[dict[str, Any]]:
    return [
        {
            "id": "request_python_syntax_shared_toolbox",
            "tool": "check_python_syntax",
            "reason": "Validate Python source syntax before bundling shared-toolbox evidence.",
            "args": {},
            "status": "proposed_or_reported",
        },
        {
            "id": "request_validation_contract_shared_toolbox",
            "tool": "check_validation_report_contract",
            "reason": "Validate generated JSON report contracts before compact bundle assembly.",
            "args": {},
            "status": "proposed_or_reported",
        },
        {
            "id": "request_code_interpreter_shared_toolbox",
            "tool": "build_code_interpreter_report",
            "reason": "Build report-only static analysis evidence for shared toolbox AI-to-AI review.",
            "args": {"inputs": ["Tools/ai", "Tools/validation", "Tools/workflow", "Tools/npu"]},
            "status": "proposed_or_reported",
        },
    ]


def build_remaining_gaps(
    missing_reports: list[dict[str, Any]],
    missing_artifacts: list[dict[str, Any]],
    facts: dict[str, Any],
) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    gaps.extend(missing_reports)
    gaps.extend(missing_artifacts)
    if not any(item.get("tool") for item in facts.get("tool_requests_executed_or_proposed", [])):
        gaps.append(
            {
                "gap": "runtime tool requests not proven in provider-backed run",
                "detail": "No concrete tool_requests were found in the included reports.",
            }
        )
    if facts.get("patch_application_performed"):
        gaps.append({"gap": "patch application detected", "detail": "Expected report-only execution."})
    if facts.get("sqlite_write_performed") or facts.get("persistent_memory_write_performed"):
        gaps.append({"gap": "SQLite or persistent memory write detected", "detail": "Expected read-only/report-only behavior."})
    return gaps


def build_final_summary(
    *,
    repo_root: Path,
    stamp: str,
    report_paths: list[str],
    artifact_paths: list[str],
    bundle_paths: list[str],
    recommended_next_task_md: str,
    missing_reports: list[dict[str, Any]],
    missing_artifacts: list[dict[str, Any]],
    recursive_defaults: dict[str, Any] | None = None,
    chunked_file_index: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    facts = collect_report_facts(repo_root, report_paths)
    tool_requests = facts.get("tool_requests_executed_or_proposed") or default_tool_requests()
    remaining_gaps = build_remaining_gaps(missing_reports, missing_artifacts, facts)
    passed = not (
        facts.get("patch_application_performed")
        or facts.get("sqlite_write_performed")
        or facts.get("persistent_memory_write_performed")
        or facts.get("blender_runtime_execution_performed")
    )
    return {
        "schema_version": 1,
        "kind": "shared_toolbox_ai_to_ai_final_summary",
        "stamp": stamp,
        "passed": passed,
        "tools_available": [item["tool_name"] for item in RUNTIME_TOOL_CAPABILITIES],
        "tool_capabilities": list(RUNTIME_TOOL_CAPABILITIES),
        "tool_requests_executed_or_proposed": tool_requests,
        "reports_generated": facts.get("reports_generated", []),
        "remaining_gaps": remaining_gaps,
        "recommended_next_task_md": recommended_next_task_md,
        "compact_bundle_paths": bundle_paths,
        "provider_execution_performed": bool(facts.get("provider_execution_performed")),
        "patch_application_performed": bool(facts.get("patch_application_performed")),
        "source_writes_performed": bool(facts.get("source_writes_performed")),
        "sqlite_write_performed": bool(facts.get("sqlite_write_performed")),
        "persistent_memory_write_performed": bool(facts.get("persistent_memory_write_performed")),
        "blender_runtime_execution_performed": bool(facts.get("blender_runtime_execution_performed")),
        "artifact_paths_considered": artifact_paths,
        "recursive_defaults": recursive_defaults or {},
        "chunked_file_index": chunked_file_index or [],
        "errors": facts.get("errors", []),
        "warnings": facts.get("warnings", []),
    }


def render_final_summary_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = ["# Shared Toolbox AI-to-AI Final Summary", ""]
    for key in (
        "stamp",
        "passed",
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
        "sqlite_write_performed",
        "persistent_memory_write_performed",
        "blender_runtime_execution_performed",
    ):
        lines.append(f"- {key}: {summary.get(key)}")
    lines.append("")
    lines.append("## Tools available")
    lines.append("")
    for tool in summary.get("tool_capabilities", []):
        lines.append(f"### {tool.get('tool_name')}")
        lines.append("")
        lines.append(f"- Category: {tool.get('category')}")
        lines.append(f"- Safe default mode: {tool.get('safe_default_mode')}")
        lines.append(f"- Recommended next use: {tool.get('recommended_next_use')}")
        lines.append("- Can do:")
        for item in tool.get("what_it_can_do", []):
            lines.append(f"  - {item}")
        lines.append("- Must not do:")
        for item in tool.get("what_it_must_not_do", []):
            lines.append(f"  - {item}")
        lines.append("")
    lines.append("## Tool requests executed or proposed")
    lines.append("")
    for request in summary.get("tool_requests_executed_or_proposed", []):
        lines.append(f"- {request.get('id')}: {request.get('tool')} - {request.get('reason')}")
    lines.append("")
    lines.append("## Reports generated")
    lines.append("")
    for report in summary.get("reports_generated", []):
        lines.append(
            f"- {report.get('path')} exists={report.get('exists')} json_ok={report.get('json_ok')} "
            f"kind={report.get('kind')} passed={report.get('passed')}"
        )
    lines.append("")
    lines.append("## Remaining gaps")
    lines.append("")
    gaps = summary.get("remaining_gaps") or []
    if gaps:
        for gap in gaps:
            if isinstance(gap, dict):
                label = gap.get("gap") or gap.get("path") or "gap"
                detail = gap.get("detail") or gap.get("reason") or ""
                lines.append(f"- {label}: {detail}")
            else:
                lines.append(f"- {gap}")
    else:
        lines.append("- No blocking report-only guardrail gaps detected.")
    lines.append("")
    lines.append("## Recommended next task")
    lines.append("")
    lines.append(str(summary.get("recommended_next_task_md") or ""))
    lines.append("")
    chunked = summary.get("chunked_file_index") or []
    lines.append("## Chunked large JSON/Markdown files")
    lines.append("")
    if chunked:
        for item in chunked:
            lines.append(
                f"- {item.get('path')} lines={item.get('line_count')} "
                f"chunks={item.get('chunk_count')} chunk_size={item.get('chunk_size_lines')}"
            )
            for chunk in item.get("chunks", []):
                pointer = chunk.get("next_chunk_id") or "END"
                lines.append(
                    f"  - {chunk.get('chunk_id')} -> next: {pointer}"
                )
    else:
        lines.append("- No JSON/Markdown file above the chunk threshold was detected.")
    lines.append("")
    lines.append("## Compact bundle paths")
    lines.append("")
    for path in summary.get("compact_bundle_paths", []):
        lines.append(f"- {path}")
    lines.append("")
    return "\n".join(lines)


def write_final_summary(repo_root: Path, summary: dict[str, Any]) -> tuple[Path, Path]:
    stamp = str(summary["stamp"])
    output_dir = repo_root / "output" / "analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{DEFAULT_FINAL_SUMMARY_PREFIX}_{stamp}.json"
    md_path = output_dir / f"{DEFAULT_FINAL_SUMMARY_PREFIX}_{stamp}.md"
    write_json_report(summary, json_path)
    md_path.write_text(render_final_summary_markdown(summary), encoding="utf-8")
    return json_path, md_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default=None)
    parser.add_argument("--basename", default=None)
    parser.add_argument("--output-dir", default="docs/LOCAL_VALIDATION_EVIDENCE")
    parser.add_argument("--task-md", default="docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md")
    parser.add_argument("--architecture-md", default="docs/LOCAL_AI_TASKS/shared-runtime-toolbox-orchestration-architecture.md")
    parser.add_argument("--orchestrator-report", action="append", default=[])
    parser.add_argument("--gpu-report", action="append", default=[])
    parser.add_argument("--sync-report", action="append", default=[])
    parser.add_argument("--contract-replay-report", action="append", default=[])
    parser.add_argument("--code-interpreter-report", action="append", default=[])
    parser.add_argument("--python-syntax-report", action="append", default=[])
    parser.add_argument("--report", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--include-missing-optional", action="store_true")
    parser.add_argument("--validate-bundle", action="store_true")
    parser.add_argument("--validation-output", default=None)
    parser.add_argument("--max-included-artifact-chars", type=int, default=14000)
    parser.add_argument("--max-included-artifacts", type=int, default=40)
    parser.add_argument("--no-recursive-defaults", action="store_true", help="Disable bounded recursive default discovery for stamped JSON/Markdown files.")
    parser.add_argument("--recursive-report-root", action="append", default=[], help="Extra recursive root for stamped JSON reports; repeatable or comma-separated.")
    parser.add_argument("--recursive-artifact-root", action="append", default=[], help="Extra recursive root for stamped Markdown/JSON artifacts; repeatable or comma-separated.")
    parser.add_argument("--recursive-include-unstamped", action="store_true", help="Allow recursive discovery of files without the stamp in their path. Use only on narrow roots.")
    parser.add_argument("--recursive-max-files", type=int, default=DEFAULT_RECURSIVE_MAX_FILES)
    parser.add_argument("--chunk-large-files-lines", type=int, default=DEFAULT_CHUNK_SIZE_LINES, help="Build pointer-style chunk metadata for JSON/Markdown files above this line count. Set 0 to disable.")
    return parser.parse_args(argv)


def build_shared_toolbox_bundle(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or datetime.now().strftime(DEFAULT_STAMP_FORMAT)
    basename = args.basename or f"{DEFAULT_BASENAME_PREFIX}_{stamp}"
    output_dir = resolve_output_path(repo_root, args.output_dir)

    explicit_reports = coalesce_list(
        list(args.report or []),
        list(args.orchestrator_report or []),
        list(args.gpu_report or []),
        list(args.sync_report or []),
        list(args.contract_replay_report or []),
        list(args.code_interpreter_report or []),
        list(args.python_syntax_report or []),
    )
    report_candidates = coalesce_list(explicit_reports, report_templates_for_stamp(stamp))
    recursive_report_paths: list[str] = []
    recursive_artifact_paths: list[str] = []
    recursive_skipped: list[dict[str, Any]] = []
    if not args.no_recursive_defaults:
        report_roots = coalesce_list(list(DEFAULT_RECURSIVE_REPORT_ROOTS), list(args.recursive_report_root or []))
        recursive_report_paths, report_skipped = discover_recursive_files(
            repo_root,
            report_roots,
            (".json",),
            stamp=stamp,
            max_files=int(args.recursive_max_files),
            include_unstamped=bool(args.recursive_include_unstamped),
        )
        recursive_skipped.extend(report_skipped)
        report_candidates = coalesce_list(report_candidates, recursive_report_paths)
    reports, missing_reports = existing_report_paths(
        repo_root,
        report_candidates,
        include_missing_optional=bool(args.include_missing_optional),
    )

    initial_bundle_paths = [
        repo_relative(output_dir / f"{basename}.json", repo_root),
        repo_relative(output_dir / f"{basename}.md", repo_root),
    ]
    artifact_candidates = coalesce_list(
        [args.task_md, args.architecture_md],
        list(args.artifact or []),
        artifact_templates_for_stamp(stamp),
    )
    if not args.no_recursive_defaults:
        artifact_roots = coalesce_list(list(DEFAULT_RECURSIVE_ARTIFACT_ROOTS), list(args.recursive_artifact_root or []))
        recursive_artifact_paths, artifact_skipped = discover_recursive_files(
            repo_root,
            artifact_roots,
            (".md", ".json"),
            stamp=stamp,
            max_files=int(args.recursive_max_files),
            include_unstamped=bool(args.recursive_include_unstamped),
        )
        recursive_skipped.extend(artifact_skipped)
        artifact_candidates = coalesce_list(artifact_candidates, recursive_artifact_paths)
    artifacts, missing_artifacts = existing_artifact_paths(
        repo_root,
        artifact_candidates,
        include_missing_optional=bool(args.include_missing_optional),
    )

    chunked_index = build_chunked_file_index(
        repo_root,
        coalesce_list(reports, artifacts),
        max_lines_per_chunk=int(args.chunk_large_files_lines),
    )
    recursive_defaults = {
        "enabled": not args.no_recursive_defaults,
        "report_roots": coalesce_list(list(DEFAULT_RECURSIVE_REPORT_ROOTS), list(args.recursive_report_root or [])) if not args.no_recursive_defaults else [],
        "artifact_roots": coalesce_list(list(DEFAULT_RECURSIVE_ARTIFACT_ROOTS), list(args.recursive_artifact_root or [])) if not args.no_recursive_defaults else [],
        "include_unstamped": bool(args.recursive_include_unstamped),
        "max_files": int(args.recursive_max_files),
        "discovered_reports": recursive_report_paths,
        "discovered_artifacts": recursive_artifact_paths,
        "skipped": recursive_skipped[:80],
        "skipped_count": len(recursive_skipped),
    }
    summary = build_final_summary(
        repo_root=repo_root,
        stamp=stamp,
        report_paths=reports,
        artifact_paths=artifacts,
        bundle_paths=initial_bundle_paths,
        recommended_next_task_md=args.task_md,
        missing_reports=missing_reports,
        missing_artifacts=missing_artifacts,
        recursive_defaults=recursive_defaults,
        chunked_file_index=chunked_index,
    )
    final_json, final_md = write_final_summary(repo_root, summary)
    reports_with_summary = coalesce_list(reports, [repo_relative(final_json, repo_root)])
    artifacts_with_summary = coalesce_list(artifacts, [repo_relative(final_md, repo_root)])

    bundle, outputs_text = build_bundle(
        repo_root,
        reports_with_summary,
        basename,
        output_dir,
        [],
        artifacts_with_summary,
        True,
        int(args.max_included_artifact_chars),
        int(args.max_included_artifacts),
    )
    bundle_paths = outputs_text.splitlines()
    summary["compact_bundle_paths"] = [repo_relative(Path(path), repo_root) for path in bundle_paths]
    final_json, final_md = write_final_summary(repo_root, summary)

    validation_report: dict[str, Any] | None = None
    validation_output_path: Path | None = None
    if args.validate_bundle:
        bundle_json = output_dir / f"{basename}.json"
        validation_report = validate_github_evidence_bundles(repo_root, [bundle_json])
        validation_output = args.validation_output or f"output/validation/{basename}_validation.json"
        validation_output_path = resolve_output_path(repo_root, validation_output)
        write_json_report(validation_report, validation_output_path)

    return {
        "schema_version": 1,
        "kind": "shared_toolbox_ai_to_ai_bundle_builder_result",
        "repo_root": str(repo_root),
        "stamp": stamp,
        "passed": bool(summary.get("passed")) and (validation_report is None or bool(validation_report.get("passed"))),
        "final_summary_json": repo_relative(final_json, repo_root),
        "final_summary_markdown": repo_relative(final_md, repo_root),
        "bundle_outputs": [repo_relative(Path(path), repo_root) for path in bundle_paths],
        "validation_output": repo_relative(validation_output_path, repo_root) if validation_output_path else None,
        "bundle_decision": bundle.get("decision"),
        "provider_execution_performed": bool(summary.get("provider_execution_performed")),
        "patch_application_performed": bool(summary.get("patch_application_performed")),
        "sqlite_write_performed": bool(summary.get("sqlite_write_performed")),
        "persistent_memory_write_performed": bool(summary.get("persistent_memory_write_performed")),
        "errors": list(summary.get("errors") or []) + list((validation_report or {}).get("errors") or []),
        "warnings": list(summary.get("warnings") or []) + list((validation_report or {}).get("warnings") or []),
        "recursive_default_report_count": len(recursive_report_paths),
        "recursive_default_artifact_count": len(recursive_artifact_paths),
        "chunked_file_count": len(chunked_index),
        "missing_reports": missing_reports,
        "missing_artifacts": missing_artifacts,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = build_shared_toolbox_bundle(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
