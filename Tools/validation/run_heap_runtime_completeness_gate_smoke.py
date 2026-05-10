#!/usr/bin/env python3
"""Smoke-test the budget-driven heap runtime completeness gate."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def run_gate(repo_root: Path, label: str, stamp: str, timeout_seconds: int, max_iterations: int, provider_model: str) -> tuple[subprocess.CompletedProcess[str], dict[str, Any], Path]:
    run_dir = repo_root / "output" / "validation" / f"heap_runtime_completeness_gate_{label}_{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    output = run_dir / "heap_runtime_completeness_gate_report.json"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    command = [
        sys.executable,
        "Tools/ai/run_heap_runtime_completeness_gate.py",
        "--repo-root", ".",
        "--stamp", f"{label}_{stamp}",
        "--output-dir", run_dir.as_posix(),
        "--max-iterations", str(max_iterations),
        "--budget-minutes", "5",
        "--max-rounds", str(max_iterations),
        "--timeout-seconds", str(timeout_seconds),
        "--provider-model", provider_model,
    ]
    completed = subprocess.run(command, cwd=repo_root, env=env, capture_output=True, text=True, check=False, timeout=timeout_seconds * max(2, max_iterations))
    return completed, read_json(output), run_dir


def validate_complete(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("passed") is not True:
        errors.append("complete heap runtime gate did not pass")
    if report.get("kind") != "heap_runtime_completeness_gate":
        errors.append("report kind must be heap_runtime_completeness_gate")
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    required_positive = (
        "heap_read_count",
        "heap_write_count",
        "tool_request_count",
        "tool_execution_count",
        "decision_count",
        "candidate_operation_count",
        "shared_evidence_count",
        "shared_memory_evidence_count",
        "shared_context_chunk_evidence_count",
        "tool_catalog_evidence_count",
        "validation_evidence_count",
        "gpu1_provider_evidence_count",
        "gpu0_provider_evidence_count",
        "npu_micro_task_evidence_count",
        "provider_result_count",
        "provider_lane_count",
    )
    for key in required_positive:
        if int(metrics.get(key) or 0) <= 0:
            errors.append(f"metric {key} must be >0")
    if metrics.get("product_status") != "ready":
        errors.append("complete run product_status must be ready")
    if metrics.get("missing_requirements"):
        errors.append("complete run must have no missing requirements")
    if int(metrics.get("completed_requirement_count") or 0) != int(metrics.get("required_requirement_count") or -1):
        errors.append("complete run must satisfy all required requirements")
    if metrics.get("budget_decision") != "deny_provider_generation":
        errors.append("budget_decision must deny provider generation by default")
    state = report.get("state") if isinstance(report.get("state"), dict) else {}
    for key in ("facts", "needs", "tool_requests", "shared_evidence", "provider_results", "claims", "decisions", "candidate_operations"):
        value = state.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"state.{key} must contain at least one item")
    if report.get("provider_execution_performed") is not True or metrics.get("provider_execution_performed") is not True:
        errors.append("complete run must perform observable provider execution")
    if int(metrics.get("provider_lane_count") or 0) < 3:
        errors.append("complete run must include all three provider lanes")
    output_contract = report.get("real_run_output_contract") if isinstance(report.get("real_run_output_contract"), dict) else {}
    if not output_contract.get("heap_event_log") or not output_contract.get("provider_report_outputs"):
        errors.append("complete run must expose real-run-compatible output contract")
    guardrails = report.get("guardrails") if isinstance(report.get("guardrails"), dict) else {}
    for key in ("patch_application_performed", "source_writes_performed"):
        if report.get(key) is not False or guardrails.get(key) is not False:
            errors.append(f"guardrail {key} must be false")
    return errors


def validate_budget_block(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("passed") is not True:
        errors.append("budget-block heap runtime gate should pass as controlled blocked_with_reason")
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    if metrics.get("product_status") != "blocked_with_reason":
        errors.append("budget-block product_status must be blocked_with_reason")
    if not metrics.get("missing_requirements"):
        errors.append("budget-block run must expose missing_requirements")
    if metrics.get("budget_exhausted") is not True:
        errors.append("budget-block run must mark budget_exhausted=true")
    if int(metrics.get("tool_execution_count") or 0) <= 0:
        errors.append("budget-block run must still execute at least one brokered tool")
    return errors


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Runtime Completeness Gate Smoke", "", f"- Passed: `{report.get('passed')}`"]
    for run in report.get("runs") or []:
        lines.extend(["", f"## {run.get('label')}", ""])
        lines.append(f"- Passed: `{run.get('passed')}`")
        lines.append(f"- Run dir: `{run.get('run_dir')}`")
        metrics = run.get("metrics") if isinstance(run.get("metrics"), dict) else {}
        for key in ("product_status", "completed_requirement_count", "required_requirement_count", "missing_requirements", "budget_exhausted", "tool_execution_count"):
            lines.append(f"- {key}: `{metrics.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_runtime_completeness_gate_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/heap_runtime_completeness_gate_smoke.md")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--provider-model", default="qwen2.5-coder:14b")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    stamp = now_stamp()
    runs: list[dict[str, Any]] = []
    errors: list[str] = []

    complete_proc, complete_report, complete_dir = run_gate(repo_root, "complete", stamp, args.timeout_seconds, max_iterations=4, provider_model=args.provider_model)
    complete_errors = []
    if complete_proc.returncode != 0:
        complete_errors.append(f"complete gate returned {complete_proc.returncode}: {(complete_proc.stderr or complete_proc.stdout)[-1500:]}")
    complete_errors.extend(validate_complete(complete_report))
    errors.extend(f"complete: {item}" for item in complete_errors)
    runs.append({
        "label": "complete",
        "passed": not complete_errors,
        "run_dir": complete_dir.relative_to(repo_root).as_posix(),
        "returncode": complete_proc.returncode,
        "metrics": complete_report.get("metrics", {}),
        "errors": complete_errors,
    })

    blocked_proc, blocked_report, blocked_dir = run_gate(repo_root, "budget_block", stamp, args.timeout_seconds, max_iterations=2, provider_model=args.provider_model)
    blocked_errors = []
    if blocked_proc.returncode != 0:
        blocked_errors.append(f"budget_block gate returned {blocked_proc.returncode}: {(blocked_proc.stderr or blocked_proc.stdout)[-1500:]}")
    blocked_errors.extend(validate_budget_block(blocked_report))
    errors.extend(f"budget_block: {item}" for item in blocked_errors)
    runs.append({
        "label": "budget_block",
        "passed": not blocked_errors,
        "run_dir": blocked_dir.relative_to(repo_root).as_posix(),
        "returncode": blocked_proc.returncode,
        "metrics": blocked_report.get("metrics", {}),
        "errors": blocked_errors,
    })

    report = {
        "schema_version": 1,
        "kind": "heap_runtime_completeness_gate_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "runs": runs,
        "provider_execution_performed": any(bool((run.get("metrics") or {}).get("provider_execution_performed")) for run in runs),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
