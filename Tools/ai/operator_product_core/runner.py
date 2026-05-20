"""Execution and artifact intake for operator product launcher."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from Tools.ai._shared.live_flow_monitor import run_monitored_command
from Tools.ai.heap_context_closure.common import terminate_provider_launch_manifest_processes

from .io_utils import read_json_quiet, write_json, write_text
from .markdown import render_lab_markdown, render_run_markdown
from .models import LauncherConfig
from .profiles import build_heap_command, resolve_config, resolve_project_python, run_dir_for


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
    timeout: int = 3600,
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


def run_heap(config: LauncherConfig, timeout: int = 3600) -> dict[str, Any]:
    cfg = resolve_config(config)
    cfg.final_root.mkdir(parents=True, exist_ok=True)
    command = build_heap_command(cfg)
    run_dir = run_dir_for(cfg)
    run_dir.mkdir(parents=True, exist_ok=True)
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
    report = {
        "schema_version": 1,
        "kind": "operator_product_launcher_run",
        "repo_root": str(cfg.repo_root),
        "profile_name": cfg.profile_name,
        "stamp": cfg.stamp,
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir),
        "final_root": str(cfg.final_root),
        "launcher_summary": str(summary_path) if summary_path.exists() else "",
        "code_product": discover_code_product(run_dir, summary),
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
) -> dict[str, Any]:
    tool_root = Path(__file__).resolve().parents[3]
    output = output_dir / (
        "code_product_apply_safe.json" if apply_safe else "code_product_review.json"
    )
    markdown = output.with_suffix(".md")
    command = [
        resolve_project_python(repo_root),
        "-m",
        "Tools.ai.code_product.artifact_intake",
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
        timeout=600,
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
    timeout: int = 3600,
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
    if metrics.get("exists") and code_product is not None:
        review_report = analyze_code_product(cfg.repo_root, code_product, run_dir)
    errors.extend(code_product_blockers(metrics, review_report))
    passed = bool(run_report.get("passed")) and bool(review_report.get("passed")) and not errors
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "operator_product_lab_summary",
        "repo_root": str(cfg.repo_root),
        "profile_name": cfg.profile_name,
        "stamp": cfg.stamp,
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir),
        "final_root": str(cfg.final_root),
        "code_product": code_product_raw,
        "code_product_metrics": metrics,
        "run_report": run_report,
        "review_report": review_report,
        "safe_apply_report": safe_apply_report,
        "errors": errors,
        "passed": passed,
    }
    write_json(run_dir / "operator_product_lab_summary.json", report)
    write_text(run_dir / "operator_product_lab_summary.md", render_lab_markdown(report))
    return report
