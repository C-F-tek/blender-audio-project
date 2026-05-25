"""Execution and artifact intake for operator product launcher."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from ia_carmine._shared.live_flow_monitor import run_monitored_command
from ia_carmine.runtime.heap_context_closure.common import terminate_provider_launch_manifest_processes
from Tools.validation._shared.codex_failure_counters import (
    apply_codex_failure_counter_updates,
    classify_codex_failure_counters,
)

from .io_utils import read_json_quiet, write_json, write_text
from .markdown import render_lab_markdown, render_run_markdown
from .models import LauncherConfig
from .public_documents import default_public_documents_root, mirror_public_documents_package
from .direct_command import (
    build_heap_command,
    canonical_run_metadata,
    canonical_run_metadata_path,
    resolve_config,
    resolve_project_python,
    run_dir_for,
)


def command_env(repo_root: Path, python_exe: str) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    env["IA_CARMINE_PYTHON"] = python_exe
    return env


def run_command(
    command: list[str],
    cwd: Path,
    timeout: int | None = None,
    *,
    flow_dir: Path | None = None,
    phase: str = "operator_command",
) -> dict[str, Any]:
    return run_monitored_command(
        command,
        cwd=cwd,
        env=command_env(cwd, command[0]),
        timeout_seconds=timeout,
        flow_dir=flow_dir,
        status_name="operator_product_live_flow",
        phase=phase,
        tail_chars=6000,
        keyboard_interrupt="return",
    )


def discover_code_product(run_dir: Path, summary: dict[str, Any]) -> str:
    outputs = summary.get("final_readable_product_documents_outputs")
    if isinstance(outputs, dict) and outputs.get("documents_code_product"):
        return str(outputs["documents_code_product"])
    for key in ("composer_documents_dir", "run_dir"):
        value = str(summary.get(key) or "")
        if value:
            candidate = Path(value) / "CODE_PRODUCT_FULL_PATCH.md"
            if candidate.exists():
                return str(candidate)
    candidate = run_dir / "CODE_PRODUCT_FULL_PATCH.md"
    return str(candidate) if candidate.exists() else ""


def code_product_metrics(code_product: Path | None) -> dict[str, Any]:
    exists = bool(code_product and code_product.is_file())
    report: dict[str, Any] = {
        "path": str(code_product) if code_product else "",
        "exists": exists,
        "size_bytes": 0,
        "line_count": 0,
        "diff_git_blocks": 0,
        "empty_code_product_marker": False,
        "no_applicable_marker": False,
        "truncation_marker": False,
    }
    if not exists or code_product is None:
        return report
    text = code_product.read_text(encoding="utf-8-sig", errors="replace")
    report.update(
        {
            "size_bytes": code_product.stat().st_size,
            "line_count": len(re.split(r"\r?\n", text)),
            "diff_git_blocks": len(re.findall(r"diff --git", text)),
            "empty_code_product_marker": "EMPTY CODE PRODUCT" in text
            or "Nessun diff/code effettivo" in text,
            "no_applicable_marker": "NO_APPLICABLE_CODE_PRODUCT" in text
            or "NO_TARGETS_OR_CODE_PRODUCT" in text,
            "truncation_marker": "[truncated]" in text.lower()
            or "[diff truncated]" in text.lower()
            or "[code product excerpt truncated" in text.lower(),
        }
    )
    return report


def code_product_blockers(
    metrics: dict[str, Any],
    review_report: dict[str, Any] | None = None,
) -> list[str]:
    review = review_report or {}
    all_integrated = review.get("all_integrated") is True
    blockers: list[str] = []
    if not metrics.get("exists"):
        return ["CODE_PRODUCT_FULL_PATCH was not produced"]
    if int(metrics.get("diff_git_blocks") or 0) <= 0 and not all_integrated:
        blockers.append("CODE_PRODUCT_FULL_PATCH has no real diff --git block")
    if metrics.get("empty_code_product_marker") and not all_integrated:
        blockers.append("CODE_PRODUCT_FULL_PATCH declares no effective diff/code")
    if metrics.get("no_applicable_marker") and not all_integrated:
        blockers.append("CODE_PRODUCT_FULL_PATCH declares no applicable code product")
    if metrics.get("truncation_marker"):
        blockers.append("CODE_PRODUCT_FULL_PATCH contains a truncation marker")
    return blockers


def reviewable_code_product(metrics: dict[str, Any]) -> bool:
    return (
        bool(metrics.get("exists"))
        and int(metrics.get("diff_git_blocks") or 0) > 0
        and not metrics.get("empty_code_product_marker")
        and not metrics.get("no_applicable_marker")
        and not metrics.get("truncation_marker")
    )


def blocked_reason(summary: dict[str, Any], result: dict[str, Any]) -> str:
    if summary.get("product_blocked_reason"):
        return str(summary.get("product_blocked_reason"))
    if summary.get("continuation_required"):
        return str(summary.get("soft_close_reason") or "continuation_required")
    if result.get("passed") is not True:
        return "heap_context_closure_failed"
    if summary.get("provider_execution_performed") is False:
        return "provider_execution_missing"
    roles = summary.get("all_roles_present") or summary.get("roles_present")
    if isinstance(roles, list):
        required = {"gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"}
        if not required.issubset({str(role) for role in roles}):
            return "provider_roles_missing"
    if summary.get("pointer_block_count") == 0:
        return "pointer_blocks_missing"
    if summary.get("pointer_reconstruction_passed") is False:
        return "pointer_reconstruction_failed"
    return ""


def run_heap(config: LauncherConfig, timeout: int | None = None) -> dict[str, Any]:
    cfg = resolve_config(config)
    cfg.final_root.mkdir(parents=True, exist_ok=True)
    run_dir = run_dir_for(cfg)
    run_dir.mkdir(parents=True, exist_ok=True)
    write_json(canonical_run_metadata_path(cfg), canonical_run_metadata(cfg))
    command = build_heap_command(cfg)
    result = run_command(
        command,
        cfg.repo_root,
        timeout=timeout,
        flow_dir=run_dir,
        phase="operator_heap_context_closure",
    )
    summary_path = run_dir / "heap_runtime_context_closure_launcher.json"
    provider_orphan_cleanup: dict[str, Any] = {}
    if not result.get("passed") or not summary_path.exists():
        provider_orphan_cleanup = terminate_provider_launch_manifest_processes(
            run_dir=run_dir,
            repo_root=cfg.repo_root,
            reason="operator product wrapper observed failed or incomplete heap closure",
        )
    summary = read_json_quiet(summary_path)
    if isinstance(summary, dict):
        if cfg.effective_universe_config is not None:
            summary["effective_universe_config"] = cfg.effective_universe_config
        if cfg.field_sources is not None:
            summary["field_sources"] = cfg.field_sources
        if summary_path.exists():
            write_json(summary_path, summary)
    provider_requested = "--allow-provider-generation" in command
    product_blocked_reason = blocked_reason(summary, result)
    product_status = str(summary.get("product_status") or "").strip()
    if not product_status:
        product_status = "blocked_with_reason" if product_blocked_reason else "heap_completed"
    report = {
        "schema_version": 1,
        "kind": "operator_product_launcher_run",
        "repo_root": str(cfg.repo_root),
        "run_label": cfg.run_label,
        "stamp": cfg.stamp,
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir),
        "final_root": str(cfg.final_root),
        "public_documents_root": str(default_public_documents_root(cfg.stamp)),
        "effective_universe_config": cfg.effective_universe_config or {},
        "field_sources": cfg.field_sources or {},
        "launcher_summary": str(summary_path) if summary_path.exists() else "",
        "code_product": discover_code_product(run_dir, summary),
        "provider_generation_required": True,
        "provider_generation_requested": provider_requested,
        "product_kind": summary.get("product_kind") or "diagnostic_decision_product",
        "product_status": product_status,
        "product_approval_status": summary.get("product_approval_status") or "",
        "product_approval_evidence": summary.get("product_approval_evidence") or {},
        "resume_from_block_id": summary.get("resume_from_block_id") or "",
        "continuation_required": bool(summary.get("continuation_required")),
        "soft_close_reason": summary.get("soft_close_reason") or "",
        "product_blocked_reason": product_blocked_reason,
        "run_result": result,
        "provider_orphan_cleanup": provider_orphan_cleanup,
        "launcher_summary_payload": summary,
        "passed": bool(result.get("passed")) and bool(summary.get("launcher_passed")),
    }
    write_json(run_dir / "operator_product_launcher_run.json", report)
    write_text(run_dir / "operator_product_launcher_run.md", render_run_markdown(report))
    return report


def analyze_code_product(
    repo_root: Path,
    code_product: Path,
    output_dir: Path,
    apply_safe: bool = False,
    require_all_integrated: bool = False,
    timeout: int | None = None,
) -> dict[str, Any]:
    tool_root = Path(__file__).resolve().parents[3]
    output = output_dir / (
        "code_product_apply_safe.json" if apply_safe else "code_product_review.json"
    )
    markdown = output.with_suffix(".md")
    command = [
        resolve_project_python(repo_root),
        "-m",
        "ia_carmine.product.code_product.artifact_intake",
        "--repo-root",
        str(repo_root),
        "--code-product",
        str(code_product),
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
    ]
    if apply_safe:
        command.append("--apply-safe")
    if require_all_integrated:
        command.append("--require-all-integrated")
    result = run_command(
        command,
        tool_root,
        timeout=timeout,
        flow_dir=output_dir,
        phase="operator_code_product_intake",
    )
    payload = read_json_quiet(output)
    payload["operator_launcher_command_result"] = result
    write_json(output, payload)
    return payload


def run_operator_lab(
    config: LauncherConfig,
    *,
    timeout: int | None = None,
) -> dict[str, Any]:
    cfg = resolve_config(config)
    run_report = run_heap(cfg, timeout=timeout)
    run_dir = run_dir_for(cfg)
    code_product_raw = str(run_report.get("code_product") or "").strip()
    code_product = Path(code_product_raw) if code_product_raw else None
    metrics = code_product_metrics(code_product)
    review_report: dict[str, Any] = {}
    safe_apply_report: dict[str, Any] = {}
    errors: list[str] = []
    product_kind = str(run_report.get("product_kind") or "")
    review_required = reviewable_code_product(metrics) or product_kind in {
        "code_patch_product",
        "text_and_code_product",
    }
    artifact_intake_performed = False
    artifact_intake_skipped_reason = ""
    if reviewable_code_product(metrics) and code_product is not None:
        review_report = analyze_code_product(cfg.repo_root, code_product, run_dir, timeout=timeout)
        artifact_intake_performed = True
    else:
        artifact_intake_skipped_reason = (
            "upstream_heap_failed_without_reviewable_code_product"
            if not run_report.get("passed")
            else "no_reviewable_code_product"
        )
    code_product_blocker_details = (
        code_product_blockers(metrics, review_report) if review_required else []
    )
    if review_required:
        errors.extend(code_product_blocker_details)
    product_blocked_reason = str(run_report.get("product_blocked_reason") or "")
    if not product_blocked_reason and errors:
        product_blocked_reason = errors[0]
    review_passed = bool(review_report.get("passed")) if review_required else True
    passed = bool(run_report.get("passed")) and review_passed and not errors
    if passed:
        product_status = "reviewable_product"
    elif run_report.get("continuation_required"):
        product_status = "blocked_continuation_product"
    else:
        product_status = "blocked_with_reason"
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "operator_product_lab_summary",
        "repo_root": str(cfg.repo_root),
        "run_label": cfg.run_label,
        "stamp": cfg.stamp,
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir),
        "final_root": str(cfg.final_root),
        "public_documents_root": str(default_public_documents_root(cfg.stamp)),
        "effective_universe_config": cfg.effective_universe_config or {},
        "field_sources": cfg.field_sources or {},
        "code_product": code_product_raw,
        "code_product_metrics": metrics,
        "provider_generation_required": True,
        "provider_generation_requested": bool(run_report.get("provider_generation_requested")),
        "product_kind": run_report.get("product_kind") or "diagnostic_decision_product",
        "review_required": review_required,
        "artifact_intake_performed": artifact_intake_performed,
        "artifact_intake_skipped_reason": artifact_intake_skipped_reason,
        "code_product_blockers": code_product_blocker_details,
        "product_status": product_status,
        "product_approval_status": run_report.get("product_approval_status") or "",
        "product_approval_evidence": run_report.get("product_approval_evidence") or {},
        "resume_from_block_id": run_report.get("resume_from_block_id") or "",
        "continuation_required": bool(run_report.get("continuation_required")),
        "soft_close_reason": run_report.get("soft_close_reason") or "",
        "product_blocked_reason": product_blocked_reason,
        "run_report": run_report,
        "review_report": review_report,
        "safe_apply_report": safe_apply_report,
        "errors": errors,
        "passed": passed,
    }
    run_result = run_report.get("run_result") if isinstance(run_report.get("run_result"), dict) else {}
    review_result = (
        review_report.get("operator_launcher_command_result")
        if isinstance(review_report.get("operator_launcher_command_result"), dict)
        else {}
    )
    launcher_summary = (
        run_report.get("launcher_summary_payload")
        if isinstance(run_report.get("launcher_summary_payload"), dict)
        else {}
    )
    report_warnings: list[Any] = []
    for item in (launcher_summary, review_report):
        warnings = item.get("warnings") if isinstance(item, dict) else None
        if isinstance(warnings, list):
            report_warnings.extend(warnings)
    launcher_errors = launcher_summary.get("launcher_contract_errors")
    if isinstance(launcher_errors, list):
        report_warnings.extend(launcher_errors)
    preflight_diagnostics = launcher_summary.get("preflight_diagnostic_failures")
    if isinstance(preflight_diagnostics, list):
        report_warnings.extend(
            f"diagnostic preflight failed: {item.get('name')}"
            for item in preflight_diagnostics
            if isinstance(item, dict)
        )
    report["codex_failure_counters"] = classify_codex_failure_counters(
        returncodes=[run_result.get("returncode"), review_result.get("returncode")],
        errors=[
            *errors,
            product_blocked_reason,
            run_result.get("stderr_tail", ""),
            review_result.get("stderr_tail", ""),
        ],
        warnings=report_warnings,
        user_interrupted=bool(
            run_result.get("keyboard_interrupt") or review_result.get("keyboard_interrupt")
        ),
    )
    report["codex_failure_counter_markdown_updates"] = apply_codex_failure_counter_updates(
        cfg.repo_root,
        report["codex_failure_counters"],
    )
    report.update(mirror_public_documents_package(cfg, run_report, report))
    write_json(run_dir / "operator_product_lab_summary.json", report)
    write_text(run_dir / "operator_product_lab_summary.md", render_lab_markdown(report))
    return report
