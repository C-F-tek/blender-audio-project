"""Allowlisted inventory, context and validation command builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.ai.provider_mesh_runtime.python_runtime import resolve_child_python

from .common import base_outputs, repo_rel, resolve_path, split_values, truthy

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
        "-m",
        "Tools.ai",
        "build_agent_memory_inventory",
        "--repo-root",
        ".",
        "--objective",
        str(args.get("objective") or "Runtime read-only memory inventory for IA-Carmine planner."),
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
    report, markdown = base_outputs(out_dir, request_id, "agent_agnostic_tool_inventory")
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
    report, markdown = base_outputs(out_dir, request_id, "agent_transient_request_context")
    command = [
        resolve_child_python(repo_root),
        "tools/ai/build_agent_transient_request_context.py",
        "--repo-root",
        ".",
        "--objective",
        str(args.get("objective") or "Runtime request-scoped context for IA-Carmine planner."),
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
    report, markdown = base_outputs(out_dir, request_id, "gpu_planner_json_contract_smoke")
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
        "-m",
        "Tools.ai",
        "build_refactor_duplication_audit",
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
    report, markdown = base_outputs(out_dir, request_id, "selected_semantic_code_chunks")
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
