"""NPU/GPU deep review auditor runner."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .common import now_iso, read_json, repo_rel, resolve_path, write_json, npu_python_path
from .provider import classify_npu_output, dependency_missing, provider_load_attempted, run_command, text_metrics
from .runtime_context import build_context, load_runtime_tool_context_reports
from .tool_requests import (
    build_npu_deterministic_tool_fallback_requests,
    extract_npu_tool_requests_from_text,
    should_use_npu_deterministic_tool_fallback,
)

def run_auditor(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    gpu_review_path = resolve_path(repo_root, args.gpu_review)
    gpu_review = read_json(gpu_review_path)
    context_path = resolve_path(repo_root, args.context_output)
    npu_out = resolve_path(repo_root, args.npu_output)
    npu_notes = resolve_path(repo_root, args.npu_notes_output)
    npu_metadata = resolve_path(repo_root, args.npu_metadata_output)
    npu_python = npu_python_path(args.npu_python)
    runtime_tool_context_reports = load_runtime_tool_context_reports(
        repo_root,
        args.runtime_tool_context_report,
        args.max_runtime_tool_context_chars,
    )
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_text(
        build_context(gpu_review, runtime_tool_context_reports), encoding="utf-8"
    )

    command = [
        str(npu_python),
        "-m",
        "Tools.npu",
        "run_npu_review",
        "--engine",
        "npu",
        "--mode",
        "onepass",
        "--context",
        str(context_path),
        "--out",
        str(npu_out),
        "--notes-out",
        str(npu_notes),
        "--metadata-out",
        str(npu_metadata),
        "--max-context-chars",
        str(args.max_context_chars),
        "--max-prompt-chars",
        str(args.max_prompt_chars),
        "--max-new-tokens",
        str(args.max_new_tokens),
    ]
    if args.metadata_only:
        command.append("--metadata-only")

    returncode = 0
    stdout = ""
    stderr = ""
    error = None
    npu_text = ""
    requested = bool(args.run_npu)
    load_attempted = False
    generated_output_written = False
    npu_python_exists = npu_python.exists()
    if args.run_npu:
        if not npu_python_exists:
            returncode = 1
            error = f"NPU Python not found: {npu_python}"
        else:
            returncode, stdout, stderr, error = run_command(
                command, repo_root, args.timeout_seconds
            )
        load_attempted = provider_load_attempted(stdout, stderr)
        generated_output_written = npu_out.exists() and not args.metadata_only
        if npu_out.exists():
            try:
                npu_text = npu_out.read_text(encoding="utf-8-sig", errors="replace")
            except OSError as exc:
                error = f"{type(exc).__name__}: {exc}"
    else:
        stdout = "NPU auditor skipped by default. Pass --run-npu to execute OpenVINO/NPU."

    classification, warnings = classify_npu_output(
        npu_text, int(returncode or 0), error, stdout, stderr, args.metadata_only
    )
    tool_requests, tool_request_errors = extract_npu_tool_requests_from_text(
        npu_text, args.max_npu_tool_requests
    )
    npu_deterministic_tool_fallback_used = False
    npu_deterministic_tool_fallback_reason = ""
    if should_use_npu_deterministic_tool_fallback(
        run_npu=bool(args.run_npu),
        metadata_only=bool(args.metadata_only),
        runtime_tool_context_reports=runtime_tool_context_reports,
        tool_requests=tool_requests,
        classification=classification,
        disabled=bool(args.disable_npu_tool_fallback),
    ):
        npu_deterministic_tool_fallback_used = True
        npu_deterministic_tool_fallback_reason = (
            "npu_no_tool_requests_with_runtime_context; "
            f"classification={classification}; runtime_tool_context_report_count={len(runtime_tool_context_reports)}"
        )
        tool_requests = build_npu_deterministic_tool_fallback_requests(
            classification=classification,
            runtime_tool_context_reports=runtime_tool_context_reports,
            max_requests=args.max_npu_tool_requests,
        )
    if args.run_npu and not npu_python_exists:
        classification = "npu_python_missing"
        warnings.append(f"NPU Python not found: {npu_python}")
    if not args.run_npu:
        classification = "not_executed"
        warnings = ["NPU auditor was not executed; context artifact was prepared only"]

    dep_missing = dependency_missing(stdout, stderr, error)
    provider_empty_response = classification == "provider_empty_response"
    provider_succeeded = bool(
        args.run_npu
        and not args.metadata_only
        and returncode == 0
        and generated_output_written
        and classification == "usable_audit_text"
    )
    report = {
        "schema_version": 1,
        "kind": "npu_gpu_deep_review_audit",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": warnings,
        "provider_execution_performed": provider_succeeded,
        "provider_execution_requested": requested,
        "provider_load_attempted": load_attempted,
        "provider_execution_succeeded": provider_succeeded,
        "provider_empty_response": provider_empty_response,
        "dependency_missing": dep_missing,
        "npu_python": str(npu_python),
        "npu_python_exists": npu_python_exists,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "runtime_tool_context_seen": bool(runtime_tool_context_reports),
        "runtime_tool_context_report_count": len(runtime_tool_context_reports),
        "runtime_tool_context_reports": runtime_tool_context_reports,
        "tool_request_count": len(tool_requests),
        "valid_tool_request_count": len(tool_requests),
        "invalid_tool_request_count": len(tool_request_errors),
        "tool_requests": tool_requests,
        "invalid_tool_request_errors": tool_request_errors,
        "npu_deterministic_tool_fallback_used": npu_deterministic_tool_fallback_used,
        "npu_deterministic_tool_fallback_reason": npu_deterministic_tool_fallback_reason,
        "npu_deterministic_tool_fallback_count": (
            len(tool_requests) if npu_deterministic_tool_fallback_used else 0
        ),
        "apply_mode": "report_only_non_blocking_npu_audit",
        "non_blocking": True,
        "blocking": False,
        "gpu_review": repo_rel(gpu_review_path, repo_root),
        "context_output": repo_rel(context_path, repo_root),
        "npu_output": repo_rel(npu_out, repo_root),
        "npu_notes_output": repo_rel(npu_notes, repo_root),
        "npu_metadata_output": repo_rel(npu_metadata, repo_root),
        "npu_auditor": {
            "requested": requested,
            "metadata_only": bool(args.metadata_only),
            "returncode": returncode,
            "classification": classification,
            "provider_execution_requested": requested,
            "provider_load_attempted": load_attempted,
            "provider_execution_performed": provider_succeeded,
            "provider_execution_succeeded": provider_succeeded,
            "provider_empty_response": provider_empty_response,
            "dependency_missing": dep_missing,
            "npu_python": str(npu_python),
            "npu_python_exists": npu_python_exists,
            "generated_output_written": generated_output_written,
            "stdout_tail": stdout,
            "stderr_tail": stderr,
            "output_metrics": text_metrics(npu_text),
            "tool_request_count": len(tool_requests),
            "valid_tool_request_count": len(tool_requests),
            "invalid_tool_request_count": len(tool_request_errors),
            "npu_deterministic_tool_fallback_used": npu_deterministic_tool_fallback_used,
            "npu_deterministic_tool_fallback_count": (
                len(tool_requests) if npu_deterministic_tool_fallback_used else 0
            ),
        },
        "decision": {
            "gpu_review_blocked": False,
            "npu_primary_advisory": False,
            "npu_audit_usable": classification == "usable_audit_text",
            "npu_dependency_missing": dep_missing,
            "npu_provider_empty_response": provider_empty_response,
            "npu_python_missing": not npu_python_exists,
            "runtime_tool_context_seen": bool(runtime_tool_context_reports),
            "runtime_tool_context_report_count": len(runtime_tool_context_reports),
            "npu_tool_requests_available": bool(tool_requests),
            "npu_tool_request_count": len(tool_requests),
            "recommendation": "continue_manual_review; treat NPU audit as non-blocking guardrail signal only",
        },
        "guardrails": {
            "non_blocking_auditor": True,
            "npu_primary_advisory": False,
            "provider_execution_requires_run_npu": True,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "runtime_toolbox_context_read_only": True,
            "runtime_toolbox_execution_requires_broker": True,
        },
    }
    return report
