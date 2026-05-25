"""Allowlisted runtime matrix, patch synthesis and code-product builders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import write_text_artifact
from ia_carmine.providers.provider_mesh.runtime.python_runtime import resolve_child_python

from .common import (
    base_outputs,
    normalized_child_path,
    real_source_target_path,
    repo_rel,
    resolve_path,
    split_values,
    truthy,
)


def append_cli_value(command: list[str], flag: str, value: Any) -> None:
    text = str(value)
    if text.startswith("-"):
        command.append(f"{flag}={text}")
    else:
        command.extend([flag, text])


def _concrete_tool_command(
    repo_root: Path,
    out_dir: Path,
    request_id: str,
    args: dict[str, Any],
    tool_name: str,
) -> tuple[list[str], dict[str, Any]]:
    report, markdown = base_outputs(out_dir, request_id, tool_name)
    args_file = out_dir / f"{request_id}_{tool_name}_args.json"
    args_file.parent.mkdir(parents=True, exist_ok=True)
    args_file.write_text(json.dumps(args, indent=2, ensure_ascii=False), encoding="utf-8")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine.runtime.runtime_tool.broker.concrete_tool_cli",
        "--repo-root",
        ".",
        "--tool",
        tool_name,
        "--args-file",
        repo_rel(args_file, repo_root),
        "--output",
        repo_rel(report, repo_root),
        "--markdown-output",
        repo_rel(markdown, repo_root),
    ]
    if args.get("timeout_seconds") is not None:
        command.extend(["--timeout-seconds", str(args["timeout_seconds"])])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "args_file": repo_rel(args_file, repo_root),
    }


def repo_toolchain_probe(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    return _concrete_tool_command(repo_root, out_dir, request_id, args, "repo_toolchain_probe")


def repo_toolchain_command(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    return _concrete_tool_command(repo_root, out_dir, request_id, args, "repo_toolchain_command")


def repo_search_rg(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    return _concrete_tool_command(repo_root, out_dir, request_id, args, "repo_search_rg")


def repo_search_git_grep(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    return _concrete_tool_command(repo_root, out_dir, request_id, args, "repo_search_git_grep")


def repo_find_fd(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    return _concrete_tool_command(repo_root, out_dir, request_id, args, "repo_find_fd")


def repo_json_query_jq(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    return _concrete_tool_command(repo_root, out_dir, request_id, args, "repo_json_query_jq")


def repo_powershell_readonly(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    return _concrete_tool_command(repo_root, out_dir, request_id, args, "repo_powershell_readonly")


def run_heap_code_execution_matrix(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
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
        "ia_carmine",
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
    operator_request_file = str(args.get("operator_request_file") or "").strip()
    operator_request = str(args.get("operator_request") or "")
    transport_refs: list[dict[str, Any]] = []
    if operator_request and not operator_request_file:
        request_ref = write_text_artifact(
            repo_root,
            out_dir / f"{request_id}_transport_payload",
            name="operator_request",
            text=operator_request,
            kind="operator_request",
            producer="run_heap_code_execution_matrix",
            suffix=".md",
        )
        operator_request_file = str(request_ref["path"])
        transport_refs.append(request_ref)
    if operator_request_file:
        command.extend(["--operator-request-file", operator_request_file])
    for key, flag in (
        ("timeout_seconds", "--timeout-seconds"),
        ("tail_chars", "--tail-chars"),
        ("max_diff_chars", "--max-diff-chars"),
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
        "transport_artifact_refs": transport_refs,
    }


def synthesize_patch_candidates(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    report, markdown = base_outputs(out_dir, request_id, "patch_candidate_synthesis")
    candidate_dir = out_dir / f"{request_id}_patch_candidate_diffs"
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
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
    operator_request_file = str(args.get("operator_request_file") or "").strip()
    operator_request = str(args.get("operator_request") or "")
    transport_refs: list[dict[str, Any]] = []
    if operator_request and not operator_request_file:
        request_ref = write_text_artifact(
            repo_root,
            out_dir / f"{request_id}_transport_payload",
            name="operator_request",
            text=operator_request,
            kind="operator_request",
            producer="synthesize_patch_candidates",
            suffix=".md",
        )
        operator_request_file = str(request_ref["path"])
        transport_refs.append(request_ref)
    if operator_request_file:
        command.extend(["--operator-request-file", operator_request_file])
    for key, flag in (
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
        "transport_artifact_refs": transport_refs,
    }


def generic_write(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    report, markdown = base_outputs(out_dir, request_id, "generic_write_md")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
        "generic_write",
        "--repo-root",
        ".",
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    for evidence_report in split_values(args.get("evidence_report")):
        command.extend(["--evidence-report", evidence_report])
    transport_refs: list[dict[str, Any]] = []
    request_file = str(args.get("request_file") or "").strip()
    operator_request = str(args.get("operator_request") or "")
    if operator_request and not request_file:
        request_ref = write_text_artifact(
            repo_root,
            out_dir / f"{request_id}_transport_payload",
            name="operator_request",
            text=operator_request,
            kind="operator_request",
            producer="generic_write",
            suffix=".md",
        )
        request_file = str(request_ref["path"])
        transport_refs.append(request_ref)
    if request_file:
        command.extend(["--request-file", request_file])
    proposal_text_file = str(args.get("proposal_text_file") or "").strip()
    proposal_text = str(args.get("proposal_text") or "")
    if proposal_text and not proposal_text_file:
        proposal_ref = write_text_artifact(
            repo_root,
            out_dir / f"{request_id}_transport_payload",
            name="proposal_text",
            text=proposal_text,
            kind="provider_proposal_text",
            producer="generic_write",
            suffix=".md",
        )
        proposal_text_file = str(proposal_ref["path"])
        transport_refs.append(proposal_ref)
    if proposal_text_file:
        command.extend(["--proposal-text-file", proposal_text_file])
    for key, flag in (
        ("provider_report", "--provider-report"),
        ("capture_mode", "--capture-mode"),
        ("source_lane", "--source-lane"),
        ("source_revision", "--source-revision"),
        ("gpu1_followup_required", "--gpu1-followup-required"),
        ("peer_followup_required", "--peer-followup-required"),
        ("provider_role", "--provider-role"),
        ("reason", "--reason"),
    ):
        if args.get(key) is not None:
            command.extend([flag, str(args[key])])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "transport_artifact_refs": transport_refs,
    }


def run_heap_virtual_dev_environment(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    report, markdown = base_outputs(out_dir, request_id, "heap_virtual_dev_environment")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
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
) -> tuple[list[str], dict[str, Any]]:
    report, markdown = base_outputs(out_dir, request_id, "runtime_file_refs")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
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
    transport_refs: list[dict[str, Any]] = []
    transport_dir = out_dir / f"{request_id}_transport_payload"
    for index, chunk in enumerate(text_chunks, start=1):
        ref = write_text_artifact(
            repo_root,
            transport_dir,
            name=f"text_{index:03d}",
            text=chunk,
            kind="runtime_file_refs_text",
            producer="runtime_file_refs",
            suffix=".txt",
        )
        command.extend(["--text-file", str(ref["path"])])
        transport_refs.append(ref)
    for value in split_values(args.get("path")):
        rel_path = normalized_child_path(repo_root, value)
        if rel_path and real_source_target_path(rel_path):
            command.extend(["--target-file", rel_path])
        else:
            command.extend(["--text-file", rel_path or value])
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
        "transport_artifact_refs": transport_refs,
    }


def analyze_code_product_artifact(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    report, markdown = base_outputs(out_dir, request_id, "code_product_artifact_intake")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
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


def runtime_file_window(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    report, markdown = base_outputs(out_dir, request_id, "runtime_file_window")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
        "runtime_file_window",
        "--repo-root",
        ".",
        "--path",
        str(args.get("path") or ""),
        "--offset",
        str(args.get("offset") or 0),
        "--limit",
        str(args.get("limit") or 16000),
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }
