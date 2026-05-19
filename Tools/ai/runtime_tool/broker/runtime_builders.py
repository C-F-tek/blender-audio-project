"""Allowlisted runtime matrix, patch synthesis and code-product builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai.provider_mesh.runtime.python_runtime import resolve_child_python

from .common import base_outputs, repo_rel, resolve_path, split_values, truthy


def append_cli_value(command: list[str], flag: str, value: Any) -> None:
    text = str(value)
    if text.startswith("-"):
        command.append(f"{flag}={text}")
    else:
        command.extend([flag, text])


def run_heap_code_execution_matrix(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "heap_code_execution_tool")
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
        "-m",
        "Tools.ai",
        "run_heap_code_execution_tool",
        "--repo-root",
        ".",
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
        append_cli_value(command, "--validation-arg", validation_arg)
    for evidence_report in split_values(args.get("evidence_report")):
        command.extend(["--evidence-report", evidence_report])
    for key, flag in (
        ("timeout_seconds", "--timeout-seconds"),
        ("tail_chars", "--tail-chars"),
        ("max_diff_chars", "--max-diff-chars"),
        ("operator_request", "--operator-request"),
        ("operator_request_file", "--operator-request-file"),
        ("max_patch_candidates", "--max-patch-candidates"),
    ):
        if args.get(key) is not None:
            command.extend([flag, str(args[key])])
    if truthy(args.get("synthesize_patch_candidates")):
        command.append("--synthesize-patch-candidates")
    if truthy(args.get("force_patch_candidate_synthesis")):
        command.append("--force-patch-candidate-synthesis")
    if truthy(args.get("no_execute")):
        command.append("--no-execute")
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "debug_lab_report": repo_rel(debug_report, repo_root),
        "debug_lab_markdown": repo_rel(debug_markdown, repo_root),
    }


def synthesize_patch_candidates(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "patch_candidate_synthesis")
    candidate_dir = out_dir / f"{request_id}_patch_candidate_diffs"
    command = [
        resolve_child_python(repo_root),
        "-m",
        "Tools.ai",
        "synthesize_patch_candidates",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
        "--candidate-dir",
        str(candidate_dir),
    ]
    for target_file in split_values(args.get("target_file")):
        command.extend(["--target-file", target_file])
    for evidence_report in split_values(args.get("evidence_report")):
        command.extend(["--evidence-report", evidence_report])
    for key, flag in (
        ("operator_request", "--operator-request"),
        ("operator_request_file", "--operator-request-file"),
        ("matrix_report", "--matrix-report"),
        ("max_candidates", "--max-candidates"),
        ("timeout_seconds", "--timeout-seconds"),
    ):
        if args.get(key) is not None:
            command.extend([flag, str(args[key])])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "candidate_dir": repo_rel(candidate_dir, repo_root),
    }


def run_heap_virtual_dev_environment(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "heap_virtual_dev_environment")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "Tools.ai",
        "run_heap_virtual_dev_environment",
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


def runtime_file_refs(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "runtime_file_refs")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "Tools.ai",
        "runtime_file_refs",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    text_values = args.get("text")
    text_chunks = (
        [str(item) for item in text_values if str(item).strip()]
        if isinstance(text_values, list)
        else ([str(text_values)] if str(text_values or "").strip() else [])
    )
    for chunk in text_chunks[:4]:
        command.extend(["--text", chunk[:4000]])
    for value in split_values(args.get("text_file")):
        command.extend(["--text-file", value])
    for key, flag in (
        ("target_file", "--target-file"),
        ("validation_script", "--validation-script"),
        ("provenance", "--provenance"),
    ):
        for value in split_values(args.get(key)):
            command.extend([flag, value])
    if truthy(args.get("strict_patchable_targets")):
        command.append("--strict-patchable-targets")
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
        "-m",
        "Tools.ai",
        "code_product_artifact_intake",
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
