#!/usr/bin/env python3
"""Report-only runtime tool broker for IA-Carmine planners.

This broker lets local AI planners request existing repository tools through a
strict allowlist. It never exposes a free shell to the model. Every invocation is
translated into a deterministic command with validated arguments.

Guardrails:
- no provider execution;
- no patch application;
- no Blender runtime execution;
- no SQLite writes;
- no persistent memory writes;
- no Git writes;
- no source writes except explicit report artifacts under output/**.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.ai.agent_runtime_tool_broker_execution import execute_command_timed
    from tools.ai.provider_mesh_runtime.python_runtime import resolve_child_python
    from tools.validation.report_utils import (
        read_json_report,
        split_csv_values,
        write_json_report,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.agent_runtime_tool_broker_execution import execute_command_timed  # type: ignore
    from tools.ai.provider_mesh_runtime.python_runtime import resolve_child_python  # type: ignore
    from tools.validation.report_utils import read_json_report, write_json_report


DEFAULT_OUTPUT = "output/validation/agent_runtime_tool_broker.json"
DEFAULT_MARKDOWN = "output/validation/agent_runtime_tool_broker.md"
SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    allowed_args: tuple[str, ...]
    builder: Callable[
        [Path, Path, str, dict[str, Any]], tuple[list[str], dict[str, str]]
    ]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
    except ValueError:
        return str(path)


def safe_id(value: Any, fallback: str) -> str:
    text = str(value or fallback).strip()
    text = SAFE_ID_RE.sub("_", text).strip("._-")
    return text[:80] or fallback


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def split_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = [value]
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def compact_value(value: Any, *, max_chars: int = 2500) -> Any:
    text = json.dumps(value, ensure_ascii=False, default=str)
    if len(text) <= max_chars:
        return value
    if isinstance(value, str):
        return value[:max_chars] + "\n...[truncated]"
    return text[:max_chars] + "\n...[truncated]"


def validate_request_args(
    tool_name: str, request_args: dict[str, Any], allowed_args: tuple[str, ...]
) -> list[str]:
    errors: list[str] = []
    if not isinstance(request_args, dict):
        return [f"{tool_name}: args must be an object"]
    unknown = sorted(set(request_args) - set(allowed_args))
    if unknown:
        errors.append(f"{tool_name}: unsupported args: {', '.join(unknown)}")
    return errors


def base_outputs(out_dir: Path, request_id: str, stem: str) -> tuple[Path, Path]:
    return out_dir / f"{request_id}_{stem}.json", out_dir / f"{request_id}_{stem}.md"


def build_python_line_count_csv(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "python_line_count")
    csv_output = out_dir / f"{request_id}_python_line_count.csv"
    command = [
        resolve_child_python(repo_root),
        "tools/validation/build_python_line_count_csv.py",
        "--repo-root",
        ".",
        "--csv-output",
        str(csv_output),
        "--report-output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    for value in split_values(args.get("exclude_dir")):
        command.extend(["--exclude-dir", value])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "csv_output": repo_rel(csv_output, repo_root),
    }


def build_agent_memory_inventory(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "agent_memory_inventory")
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_agent_memory_inventory.py",
        "--repo-root",
        ".",
        "--objective",
        str(
            args.get("objective")
            or "Runtime read-only memory inventory for IA-Carmine planner."
        ),
        "--memory-db",
        str(args.get("memory_db") or "indexAI/agent_memory/agent_memory.sqlite"),
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def build_agent_agnostic_tool_inventory(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(
        out_dir, request_id, "agent_agnostic_tool_inventory"
    )
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_agent_agnostic_tool_inventory.py",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    for root in split_values(args.get("root")):
        command.extend(["--root", root])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def build_agent_transient_request_context(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(
        out_dir, request_id, "agent_transient_request_context"
    )
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_agent_transient_request_context.py",
        "--repo-root",
        ".",
        "--objective",
        str(
            args.get("objective")
            or "Runtime request-scoped context for IA-Carmine planner."
        ),
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    for note in split_values(args.get("memory_note")):
        command.extend(["--memory-note", note])
    for raw_file in split_values(args.get("raw_file")):
        command.extend(["--raw-file", raw_file])
    for report_file in split_values(args.get("report_file")):
        command.extend(["--report-file", report_file])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def check_python_syntax(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report = out_dir / f"{request_id}_python_syntax.json"
    command = [
        resolve_child_python(repo_root),
        "tools/validation/check_python_syntax.py",
        "--repo-root",
        ".",
        "--output",
        str(report),
    ]
    return command, {"json_report": repo_rel(report, repo_root)}


def check_validation_report_contract(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report = out_dir / f"{request_id}_validation_report_contract.json"
    command = [
        resolve_child_python(repo_root),
        "tools/validation/check_validation_report_contract.py",
        "--repo-root",
        ".",
        "--report-dir",
        str(out_dir),
        "--output",
        str(report),
    ]
    for report_file in split_values(args.get("report_file")):
        command.extend(["--report-file", report_file])
    return command, {"json_report": repo_rel(report, repo_root)}


def run_gpu_planner_json_contract_smoke(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(
        out_dir, request_id, "gpu_planner_json_contract_smoke"
    )
    command = [
        resolve_child_python(repo_root),
        "tools/validation/run_gpu_planner_json_contract_smoke.py",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def build_code_interpreter_report(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "code_interpreter_report")
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_code_interpreter_report.py",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    inputs = split_values(args.get("input")) or [
        "tools/ai",
        "tools/validation",
        "tools/workflow",
        "tools/npu",
    ]
    for item in inputs:
        command.extend(["--input", item])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def build_refactor_duplication_audit(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "refactor_duplication_audit")
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_refactor_duplication_audit.py",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    multi_args = (
        ("root", "--root"),
        ("report", "--report"),
        ("input_audit_report", "--input-audit-report"),
        ("line_count_report", "--line-count-report"),
        ("code_interpreter_report", "--code-interpreter-report"),
        ("python_syntax_report", "--python-syntax-report"),
        ("bundle_smoke_report", "--bundle-smoke-report"),
        ("memory_routing_report", "--memory-routing-report"),
    )
    for key, flag in multi_args:
        for value in split_values(args.get(key)):
            command.extend([flag, value])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def build_semantic_code_chunk_selection(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(
        out_dir, request_id, "selected_semantic_code_chunks"
    )
    command = [
        resolve_child_python(repo_root),
        "tools/ai/select_semantic_code_chunks.py",
        "--repo-root",
        ".",
        "--query",
        str(args.get("query") or "heap runtime provider teamwork memory context"),
        "--output",
        str(args.get("output") or report),
        "--markdown-output",
        str(args.get("markdown_output") or markdown),
        "--max-chunks",
        str(args.get("max_chunks") or 12),
        "--max-total-chars",
        str(args.get("max_total_chars") or 18000),
        "--max-excerpt-chars",
        str(args.get("max_excerpt_chars") or 2200),
    ]
    chunks = str(args.get("chunks") or "").strip()
    if chunks:
        command.extend(["--chunks", chunks])
    for boost in split_values(args.get("path_boost")):
        command.extend(["--path-boost", boost])
    if truthy(args.get("no_code")):
        command.append("--no-code")
    return command, {
        "json_report": repo_rel(
            resolve_path(repo_root, str(args.get("output") or report)), repo_root
        ),
        "markdown_report": repo_rel(
            resolve_path(repo_root, str(args.get("markdown_output") or markdown)),
            repo_root,
        ),
    }


def build_ai_context_pack_tool(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    profile = str(args.get("profile") or "core_ai_backend")
    basename = safe_id(args.get("basename") or request_id, "ai_context_pack")
    output_dir = resolve_path(
        repo_root, str(args.get("output_dir") or out_dir / f"{request_id}_context_pack")
    )
    evidence_dir = resolve_path(
        repo_root,
        str(
            args.get("evidence_dir") or out_dir / f"{request_id}_context_pack_evidence"
        ),
    )
    evidence_basename = safe_id(
        args.get("evidence_basename") or f"{basename}_evidence",
        "ai_context_pack_evidence",
    )
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_ai_context_pack.py",
        "--repo-root",
        ".",
        "--profile",
        profile,
        "--basename",
        basename,
        "--output-dir",
        repo_rel(output_dir, repo_root),
        "--evidence-dir",
        repo_rel(evidence_dir, repo_root),
        "--evidence-basename",
        evidence_basename,
        "--max-total-chars",
        str(args.get("max_total_chars") or 64000),
        "--max-file-chars",
        str(args.get("max_file_chars") or 4000),
    ]
    if truthy(args.get("no_evidence")):
        command.append("--no-evidence")
    pack_json = output_dir / f"{basename}.json"
    pack_md = output_dir / f"{basename}.md"
    evidence_json = evidence_dir / f"{evidence_basename}.json"
    evidence_md = evidence_dir / f"{evidence_basename}.md"
    return command, {
        "json_report": repo_rel(pack_json, repo_root),
        "markdown_report": repo_rel(pack_md, repo_root),
        "evidence_json": repo_rel(evidence_json, repo_root),
        "evidence_markdown": repo_rel(evidence_md, repo_root),
    }


def build_semantic_evidence_chunk_manifest(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    basename = safe_id(args.get("basename") or request_id, "semantic_evidence_chunks")
    output_dir = resolve_path(
        repo_root,
        str(args.get("output_dir") or out_dir / f"{request_id}_semantic_chunks"),
    )
    chunk_dir = resolve_path(
        repo_root,
        str(args.get("chunk_output_dir") or output_dir / f"{basename}_chunks"),
    )
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_semantic_evidence_chunks.py",
        "--repo-root",
        ".",
        "--basename",
        basename,
        "--output-dir",
        repo_rel(output_dir, repo_root),
        "--chunk-output-dir",
        repo_rel(chunk_dir, repo_root),
        "--chunk-max-chars",
        str(args.get("chunk_max_chars") or 12000),
        "--chunk-overlap-lines",
        str(args.get("chunk_overlap_lines") or 12),
        "--no-ollama",
    ]
    for source in split_values(args.get("source")):
        command.extend(["--source", source])
    zip_output = str(args.get("zip_output") or "").strip()
    if zip_output:
        command.extend(["--zip-output", zip_output])
    manifest_json = output_dir / f"{basename}_chunk_manifest.json"
    manifest_md = output_dir / f"{basename}_chunk_manifest.md"
    return command, {
        "json_report": repo_rel(manifest_json, repo_root),
        "markdown_report": repo_rel(manifest_md, repo_root),
        "chunk_output_dir": repo_rel(chunk_dir, repo_root),
    }


def run_agent_runtime_debug_lab(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    request_file = str(args.get("request_file") or "").strip()
    if not request_file:
        request_file = str(
            out_dir / f"{request_id}_agent_runtime_debug_lab_request.json"
        )
    report = resolve_path(
        repo_root,
        str(
            args.get("output") or out_dir / f"{request_id}_agent_runtime_debug_lab.json"
        ),
    )
    markdown = resolve_path(
        repo_root,
        str(
            args.get("markdown_output")
            or out_dir / f"{request_id}_agent_runtime_debug_lab.md"
        ),
    )
    command = [
        resolve_child_python(repo_root),
        "tools/ai/agent_runtime_debug_lab.py",
        "--repo-root",
        ".",
        "--request-file",
        request_file,
        "--output",
        repo_rel(report, repo_root),
        "--markdown-output",
        repo_rel(markdown, repo_root),
    ]
    if args.get("timeout_seconds") is not None:
        command.extend(["--timeout-seconds", str(args.get("timeout_seconds"))])
    if args.get("tail_chars") is not None:
        command.extend(["--tail-chars", str(args.get("tail_chars"))])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "request_file": request_file,
    }


def runtime_sqlite_memory(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "runtime_sqlite_memory")
    command = [
        resolve_child_python(repo_root),
        "tools/ai/agent_runtime_sqlite_memory.py",
        "--repo-root",
        ".",
        "--action",
        str(args.get("action") or "status"),
        "--scope",
        str(args.get("scope") or "operational"),
        "--request-id",
        request_id,
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    for source, flag in (
        ("database", "--database"),
        ("persistent_database", "--persistent-database"),
        ("summary", "--summary"),
        ("content", "--content"),
        ("role", "--role"),
        ("query", "--query"),
        ("confirm", "--confirm"),
    ):
        if args.get(source) is not None:
            command.extend([flag, str(args[source])])
    if args.get("limit") is not None:
        command.extend(["--limit", str(args["limit"])])
    if truthy(args.get("allow_persistent_write")):
        command.append("--allow-persistent-write")
    for tag in split_values(args.get("tag")):
        command.extend(["--tag", tag])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def run_heap_code_execution_matrix(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "heap_code_execution_tool")
    request_output = out_dir / f"{request_id}_heap_code_execution_request.json"
    debug_report = (
        repo_root
        / "output"
        / "validation"
        / "heap_code_execution_tool_debug"
        / f"{request_id}_heap_code_execution_tool_debug_lab.json"
    )
    debug_markdown = debug_report.with_suffix(".md")
    command = [
        resolve_child_python(repo_root),
        "Tools/ai/run_heap_code_execution_tool.py",
        "--repo-root",
        ".",
        "--request-output",
        str(request_output),
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
        "--debug-lab-output",
        repo_rel(debug_report, repo_root),
        "--debug-lab-markdown-output",
        repo_rel(debug_markdown, repo_root),
    ]
    for target_file in split_values(args.get("target_file")):
        command.extend(["--target-file", target_file])
    for validation_script in split_values(args.get("validation_script")):
        command.extend(["--validation-script", validation_script])
    for validation_arg in split_values(args.get("validation_arg")):
        command.extend(["--validation-arg", validation_arg])
    for key, flag in (
        ("timeout_seconds", "--timeout-seconds"),
        ("tail_chars", "--tail-chars"),
        ("max_diff_chars", "--max-diff-chars"),
    ):
        if args.get(key) is not None:
            command.extend([flag, str(args[key])])
    if truthy(args.get("no_execute")):
        command.append("--no-execute")
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "request_file": repo_rel(request_output, repo_root),
        "debug_lab_report": repo_rel(debug_report, repo_root),
        "debug_lab_markdown": repo_rel(debug_markdown, repo_root),
    }


def run_heap_virtual_dev_environment(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "heap_virtual_dev_environment")
    command = [
        resolve_child_python(repo_root),
        "Tools/ai/run_heap_virtual_dev_environment.py",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    for target_file in split_values(args.get("target_file")):
        command.extend(["--target-file", target_file])
    for validation_script in split_values(args.get("validation_script")):
        command.extend(["--validation-script", validation_script])
    for key, flag in (
        ("timeout_seconds", "--timeout-seconds"),
        ("tail_chars", "--tail-chars"),
    ):
        if args.get(key) is not None:
            command.extend([flag, str(args[key])])
    if truthy(args.get("dynamic_import")):
        command.append("--dynamic-import")
    if truthy(args.get("help_probe")):
        command.append("--help-probe")
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


def analyze_code_product_artifact(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "code_product_artifact_intake")
    command = [
        resolve_child_python(repo_root),
        "Tools/ai/analyze_code_product_artifact.py",
        "--repo-root",
        ".",
        "--code-product",
        str(args.get("code_product") or ""),
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    if truthy(args.get("require_all_integrated")):
        command.append("--require-all-integrated")
    if truthy(args.get("apply_safe")) and str(args.get("confirm") or "") == "safe_apply":
        command.append("--apply-safe")
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }


TOOL_SPECS: dict[str, ToolSpec] = {
    "build_python_line_count_csv": ToolSpec(
        name="build_python_line_count_csv",
        description="Build full Python line-count CSV/JSON/MD evidence.",
        allowed_args=("exclude_dir",),
        builder=build_python_line_count_csv,
    ),
    "build_agent_memory_inventory": ToolSpec(
        name="build_agent_memory_inventory",
        description="Read-only SQLite/JSONL agent memory inventory.",
        allowed_args=("objective", "memory_db"),
        builder=build_agent_memory_inventory,
    ),
    "build_agent_agnostic_tool_inventory": ToolSpec(
        name="build_agent_agnostic_tool_inventory",
        description="Inventory existing reusable IA-Carmine tools and guardrails.",
        allowed_args=("root",),
        builder=build_agent_agnostic_tool_inventory,
    ),
    "build_agent_transient_request_context": ToolSpec(
        name="build_agent_transient_request_context",
        description="Build request-scoped context from memory notes, raw files and reports.",
        allowed_args=("objective", "memory_note", "raw_file", "report_file"),
        builder=build_agent_transient_request_context,
    ),
    "check_python_syntax": ToolSpec(
        name="check_python_syntax",
        description="Validate Python syntax across repository.",
        allowed_args=(),
        builder=check_python_syntax,
    ),
    "check_validation_report_contract": ToolSpec(
        name="check_validation_report_contract",
        description="Validate validation report contract for a scoped report-dir or explicit report files.",
        allowed_args=("report_file",),
        builder=check_validation_report_contract,
    ),
    "run_gpu_planner_json_contract_smoke": ToolSpec(
        name="run_gpu_planner_json_contract_smoke",
        description="Run GPU planner JSON contract smoke tests without provider.",
        allowed_args=(),
        builder=run_gpu_planner_json_contract_smoke,
    ),
    "build_code_interpreter_report": ToolSpec(
        name="build_code_interpreter_report",
        description="Build static code-interpreter style report over selected roots.",
        allowed_args=("input",),
        builder=build_code_interpreter_report,
    ),
    "build_refactor_duplication_audit": ToolSpec(
        name="build_refactor_duplication_audit",
        description="Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.",
        allowed_args=(
            "root",
            "report",
            "input_audit_report",
            "line_count_report",
            "code_interpreter_report",
            "python_syntax_report",
            "bundle_smoke_report",
            "memory_routing_report",
        ),
        builder=build_refactor_duplication_audit,
    ),
    "select_semantic_code_chunks": ToolSpec(
        name="select_semantic_code_chunks",
        description="Select bounded semantic code chunks for provider context from the existing chunk index.",
        allowed_args=(
            "query",
            "chunks",
            "output",
            "markdown_output",
            "max_chunks",
            "max_total_chars",
            "max_excerpt_chars",
            "path_boost",
            "no_code",
        ),
        builder=build_semantic_code_chunk_selection,
    ),
    "build_ai_context_pack": ToolSpec(
        name="build_ai_context_pack",
        description="Build a bounded final AI context pack from stable project profiles.",
        allowed_args=(
            "profile",
            "basename",
            "output_dir",
            "evidence_dir",
            "evidence_basename",
            "max_total_chars",
            "max_file_chars",
            "no_evidence",
        ),
        builder=build_ai_context_pack_tool,
    ),
    "build_semantic_evidence_chunks": ToolSpec(
        name="build_semantic_evidence_chunks",
        description="Build linked semantic evidence chunks with previous/next context and deterministic summaries.",
        allowed_args=(
            "basename",
            "source",
            "output_dir",
            "chunk_output_dir",
            "chunk_max_chars",
            "chunk_overlap_lines",
            "zip_output",
        ),
        builder=build_semantic_evidence_chunk_manifest,
    ),
    "agent_runtime_debug_lab": ToolSpec(
        name="agent_runtime_debug_lab",
        description="Run the controlled report-only Python debug lab with an allowlisted request file.",
        allowed_args=(
            "request_file",
            "output",
            "markdown_output",
            "timeout_seconds",
            "tail_chars",
        ),
        builder=run_agent_runtime_debug_lab,
    ),
    "runtime_sqlite_memory": ToolSpec(
        name="runtime_sqlite_memory",
        description="Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.",
        allowed_args=(
            "action",
            "scope",
            "database",
            "persistent_database",
            "summary",
            "content",
            "role",
            "tag",
            "query",
            "limit",
            "confirm",
            "allow_persistent_write",
        ),
        builder=runtime_sqlite_memory,
    ),
    "run_heap_code_execution_matrix": ToolSpec(
        name="run_heap_code_execution_matrix",
        description="Generate and execute a guarded compile/test/diff matrix for concrete heap code proposals.",
        allowed_args=(
            "target_file",
            "validation_script",
            "validation_arg",
            "timeout_seconds",
            "tail_chars",
            "max_diff_chars",
            "no_execute",
        ),
        builder=run_heap_code_execution_matrix,
    ),
    "run_heap_virtual_dev_environment": ToolSpec(
        name="run_heap_virtual_dev_environment",
        description="Probe target scripts in a controlled virtual development environment with AST, import, help, compile and validation evidence.",
        allowed_args=(
            "target_file",
            "validation_script",
            "timeout_seconds",
            "tail_chars",
            "dynamic_import",
            "help_probe",
        ),
        builder=run_heap_virtual_dev_environment,
    ),
    "analyze_code_product_artifact": ToolSpec(
        name="analyze_code_product_artifact",
        description="Analyze CODE_PRODUCT_FULL_PATCH artifacts and optionally apply only safe forward-applicable sections.",
        allowed_args=("code_product", "require_all_integrated", "apply_safe", "confirm"),
        builder=analyze_code_product_artifact,
    ),
}


def extract_tool_requests(data: dict[str, Any]) -> list[dict[str, Any]]:
    requests = data.get("tool_requests", [])
    if not isinstance(requests, list):
        return []
    return [item for item in requests if isinstance(item, dict)]


def first_tool_request_source(tool_requests: list[dict[str, Any]]) -> str:
    for item in tool_requests:
        source = str(item.get("source") or "").strip()
        if source:
            return source
    return ""


def infer_request_source(requests_data: dict[str, Any], request_path: Path) -> str:
    for key in ("source", "source_lane", "target_lane"):
        value = str(requests_data.get(key) or "").strip()
        if value:
            return value

    tool_request_source = first_tool_request_source(
        extract_tool_requests(requests_data)
    )
    if tool_request_source:
        return tool_request_source

    kind = str(requests_data.get("kind") or "").strip()
    if kind == "gpu0_peer_tool_requests":
        return "gpu0_peer_companion"
    if kind == "npu_gpu_deep_review_audit":
        return "npu_micro_peer_assistant"
    if kind == "agent_runtime_tool_requests":
        return "gpu1_primary_advisory"

    path_text = request_path.as_posix().lower()
    if "gpu0" in path_text:
        return "gpu0_peer_companion"
    if "npu_micro" in path_text or "/npu_" in path_text:
        return "npu_micro_peer_assistant"
    if "gpu1" in path_text:
        return "gpu1_primary_advisory"
    return kind or "unknown"


def execute_tool_request(
    *,
    repo_root: Path,
    out_dir: Path,
    index: int,
    request: dict[str, Any],
    timeout_seconds: int,
    dry_run: bool,
) -> dict[str, Any]:
    request_id = safe_id(request.get("id"), f"tool_{index:03d}")
    tool_name = str(request.get("tool") or "")
    request_args = request.get("args") if isinstance(request.get("args"), dict) else {}
    base_result: dict[str, Any] = {
        "id": request_id,
        "tool": tool_name,
        "reason": str(request.get("reason") or ""),
        "requirement": str(request.get("requirement") or ""),
        "requested": True,
        "executed": False,
        "blocked": False,
        "dry_run": dry_run,
        "status": "dry_run_pending" if dry_run else "pending",
        "persistent_memory_write_authorized": False,
        "code_product_safe_apply_authorized": False,
        "returncode": None,
        "errors": [],
        "warnings": [],
        "outputs": {},
        "summary": {},
        "guardrails": {
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "persistent_memory_write_count": 0,
            "persistent_memory_write_requires_explicit_confirm": True,
            "operational_sqlite_write_performed": False,
            "operational_memory_write_performed": False,
            "operational_memory_clear_performed": False,
            "blender_runtime_touched": False,
            "git_write_performed": False,
        },
    }

    base_result["persistent_memory_write_authorized"] = (
        tool_name == "runtime_sqlite_memory"
        and str(request_args.get("action") or "") == "remember"
        and str(request_args.get("scope") or "") == "persistent"
        and truthy(request_args.get("allow_persistent_write"))
        and str(request_args.get("confirm") or "") == "persistent_write"
    )
    base_result["code_product_safe_apply_authorized"] = (
        tool_name == "analyze_code_product_artifact"
        and truthy(request_args.get("apply_safe"))
        and str(request_args.get("confirm") or "") == "safe_apply"
    )

    spec = TOOL_SPECS.get(tool_name)
    if spec is None:
        base_result["blocked"] = True
        base_result["status"] = "blocked_not_allowlisted"
        base_result["errors"] = [f"tool not allowlisted: {tool_name}"]
        return base_result

    arg_errors = validate_request_args(tool_name, request_args, spec.allowed_args)
    if arg_errors:
        base_result["blocked"] = True
        base_result["status"] = "blocked_invalid_args"
        base_result["errors"] = arg_errors
        return base_result

    command, outputs = spec.builder(repo_root, out_dir, request_id, request_args)
    base_result["command"] = command
    base_result["outputs"] = outputs

    if dry_run:
        base_result["status"] = "dry_run"
        return base_result

    timed = execute_command_timed(command, repo_root, timeout_seconds)
    base_result["executed"] = True
    base_result["returncode"] = timed.returncode
    base_result["started_at"] = timed.started_at
    base_result["finished_at"] = timed.finished_at
    base_result["elapsed_seconds"] = timed.elapsed_seconds
    base_result["status"] = (
        "executed_ok" if timed.returncode == 0 else "executed_failed"
    )
    base_result["stdout_tail"] = timed.stdout_tail
    base_result["stderr_tail"] = timed.stderr_tail
    if timed.error:
        base_result["errors"].append(timed.error)
    if timed.returncode != 0:
        base_result["errors"].append(f"tool returned {timed.returncode}")

    json_report = outputs.get("json_report")
    if json_report:
        report_data = read_json_report(resolve_path(repo_root, json_report))
        if report_data:
            base_result["summary"] = {
                "kind": report_data.get("kind"),
                "passed": report_data.get("passed"),
                "errors": compact_value(report_data.get("errors", [])),
                "warnings": compact_value(report_data.get("warnings", [])),
                "decision": compact_value(report_data.get("decision", {})),
                "guardrails": compact_value(report_data.get("guardrails", {})),
            }
            guardrails = (
                report_data.get("guardrails")
                if isinstance(report_data.get("guardrails"), dict)
                else {}
            )
            base_result["guardrails"].update(
                {
                    "provider_execution_performed": bool(
                        report_data.get("provider_execution_performed")
                        or guardrails.get("provider_execution_performed")
                    ),
                    "patch_application_performed": bool(
                        report_data.get("patch_application_performed")
                        or guardrails.get("patch_application_performed")
                    ),
                    "source_writes_performed": bool(
                        report_data.get("source_writes_performed")
                        or guardrails.get("source_writes_performed")
                    ),
                    "sqlite_write_performed": bool(
                        guardrails.get("sqlite_write_performed")
                        or guardrails.get("sqlite_db_committed")
                        or guardrails.get("sqlite_db_touched") is True
                        and not guardrails.get("sqlite_read_only")
                    ),
                    "persistent_memory_write_performed": bool(
                        guardrails.get("persistent_memory_write_performed")
                        or guardrails.get("memory_promotion_performed")
                    ),
                    "operational_sqlite_write_performed": bool(
                        report_data.get("operational_sqlite_write_performed")
                        or guardrails.get("operational_sqlite_write_performed")
                    ),
                    "operational_memory_write_performed": bool(
                        report_data.get("operational_memory_write_performed")
                        or guardrails.get("operational_memory_write_performed")
                    ),
                    "operational_memory_clear_performed": bool(
                        report_data.get("operational_memory_clear_performed")
                        or guardrails.get("operational_memory_clear_performed")
                    ),
                    "blender_runtime_touched": bool(
                        guardrails.get("blender_runtime_touched")
                    ),
                }
            )
    return base_result


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    request_path = resolve_path(repo_root, args.request_file)
    requests_data = read_json_report(request_path)
    tool_requests = extract_tool_requests(requests_data)
    request_source = infer_request_source(requests_data, request_path)
    stamp = args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = resolve_path(
        repo_root, args.tool_output_dir or f"output/ai_runtime_tools/{stamp}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    results = [
        execute_tool_request(
            repo_root=repo_root,
            out_dir=out_dir,
            index=index,
            request=request,
            timeout_seconds=args.timeout_seconds,
            dry_run=args.dry_run,
        )
        for index, request in enumerate(tool_requests, start=1)
    ]

    blocked = [item for item in results if item.get("blocked")]
    executed = [item for item in results if item.get("executed")]
    failed = [
        item for item in results if item.get("errors") and not item.get("blocked")
    ]
    dangerous_guardrail = [
        item
        for item in results
        if item.get("guardrails", {}).get("provider_execution_performed")
        or (
            item.get("guardrails", {}).get("patch_application_performed")
            and not item.get("code_product_safe_apply_authorized")
        )
        or (
            item.get("guardrails", {}).get("source_writes_performed")
            and not item.get("code_product_safe_apply_authorized")
        )
        or (
            item.get("guardrails", {}).get("sqlite_write_performed")
            and not item.get("persistent_memory_write_authorized")
        )
        or (
            item.get("guardrails", {}).get("persistent_memory_write_performed")
            and not item.get("persistent_memory_write_authorized")
        )
        or item.get("guardrails", {}).get("blender_runtime_touched")
        or item.get("guardrails", {}).get("git_write_performed")
    ]
    operational_sqlite_write_count = sum(
        1
        for item in results
        if item.get("guardrails", {}).get("operational_sqlite_write_performed")
    )
    persistent_memory_write_count = sum(
        1
        for item in results
        if item.get("guardrails", {}).get("persistent_memory_write_performed")
    )
    source_write_count = sum(
        1 for item in results if item.get("guardrails", {}).get("source_writes_performed")
    )
    patch_application_count = sum(
        1 for item in results if item.get("guardrails", {}).get("patch_application_performed")
    )
    operational_memory_clear_count = sum(
        1
        for item in results
        if item.get("guardrails", {}).get("operational_memory_clear_performed")
    )

    return {
        "schema_version": 1,
        "kind": "agent_runtime_tool_broker",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "request_file": repo_rel(request_path, repo_root),
        "request_kind": requests_data.get("kind"),
        "source": request_source,
        "source_classification": request_source,
        "tool_output_dir": repo_rel(out_dir, repo_root),
        "passed": not failed and not dangerous_guardrail,
        "errors": [
            f"{item.get('id')}: {err}"
            for item in failed
            for err in item.get("errors", [])
        ]
        + [f"{item.get('id')}: guardrail violation" for item in dangerous_guardrail],
        "warnings": [
            f"{item.get('id')}: blocked {item.get('errors')}" for item in blocked
        ],
        "provider_execution_performed": False,
        "patch_application_performed": patch_application_count > 0,
        "source_writes_performed": source_write_count > 0,
        "sqlite_write_performed": persistent_memory_write_count > 0,
        "persistent_memory_write_performed": persistent_memory_write_count > 0,
        "operational_sqlite_write_performed": operational_sqlite_write_count > 0,
        "operational_sqlite_write_count": operational_sqlite_write_count,
        "persistent_memory_write_count": persistent_memory_write_count,
        "operational_memory_clear_count": operational_memory_clear_count,
        "blender_runtime_execution_performed": False,
        "git_write_performed": False,
        "dry_run": bool(args.dry_run),
        "tool_request_count": len(tool_requests),
        "tool_execution_count": len(executed),
        "blocked_tool_count": len(blocked),
        "failed_tool_count": len(failed),
        "allowlisted_tools": sorted(TOOL_SPECS),
        "tool_results": results,
        "guardrails": {
            "free_shell_exposed": False,
            "allowlist_enforced": True,
            "provider_execution_performed": False,
            "patch_application_performed": patch_application_count > 0,
            "source_writes_performed": source_write_count > 0,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "operational_sqlite_write_allowed_under_output": True,
            "operational_sqlite_write_performed": operational_sqlite_write_count > 0,
            "operational_memory_clear_count": operational_memory_clear_count,
            "blender_runtime_touched": False,
            "git_write_performed": False,
            "manual_review_required": True,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Runtime Tool Broker", ""]
    for key in (
        "passed",
        "dry_run",
        "request_file",
        "request_kind",
        "source",
        "source_classification",
        "tool_request_count",
        "tool_execution_count",
        "blocked_tool_count",
        "failed_tool_count",
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
        "sqlite_write_performed",
        "persistent_memory_write_performed",
        "operational_sqlite_write_performed",
        "operational_sqlite_write_count",
        "operational_memory_clear_count",
        "blender_runtime_execution_performed",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.append("")
    lines.append("## Tool results")
    lines.append("")
    for item in report.get("tool_results", []):
        lines.append(f"### `{item.get('id')}` — `{item.get('tool')}`")
        lines.append("")
        lines.append(f"- Executed: `{item.get('executed')}`")
        lines.append(f"- Blocked: `{item.get('blocked')}`")
        lines.append(f"- Return code: `{item.get('returncode')}`")
        lines.append(f"- Outputs: `{item.get('outputs')}`")
        if item.get("errors"):
            lines.append(f"- Errors: `{item.get('errors')}`")
        lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    for key, value in report.get("guardrails", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", required=True)
    parser.add_argument("--tool-output-dir", default=None)
    parser.add_argument("--stamp", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    write_json_report(report, output)
    markdown.write_text(render_markdown(report), encoding="utf-8")

    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown),
                "tool_request_count": report["tool_request_count"],
                "tool_execution_count": report["tool_execution_count"],
                "blocked_tool_count": report["blocked_tool_count"],
                "failed_tool_count": report["failed_tool_count"],
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "sqlite_write_performed": report["sqlite_write_performed"],
                "persistent_memory_write_performed": report[
                    "persistent_memory_write_performed"
                ],
                "persistent_memory_write_count": report.get(
                    "persistent_memory_write_count", 0
                ),
                "operational_sqlite_write_performed": report[
                    "operational_sqlite_write_performed"
                ],
                "operational_sqlite_write_count": report[
                    "operational_sqlite_write_count"
                ],
                "operational_memory_clear_count": report[
                    "operational_memory_clear_count"
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
