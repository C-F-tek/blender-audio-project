#!/usr/bin/env python3
"""Smoke-test the budget-driven heap runtime completeness gate."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation.heap_runtime.completeness_gate_contract import validate_contract_only
    from Tools.validation.heap_runtime.completeness_gate_smoke.process_watch import (
        outer_watchdog_seconds,
        run_with_progress_watch,
    )
    from Tools.validation.heap_runtime.completeness_gate_smoke.markdown import render_markdown
    from Tools.validation.heap_runtime.completeness_gate_smoke.request import complete_smoke_request
    from Tools.validation._shared.codex_failure_counters import (
        apply_codex_failure_counter_updates,
        classify_codex_failure_counters,
    )
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.heap_runtime.completeness_gate_contract import (  # type: ignore
        validate_contract_only,
    )
    from Tools.validation.heap_runtime.completeness_gate_smoke.process_watch import (  # type: ignore
        outer_watchdog_seconds,
        run_with_progress_watch,
    )
    from Tools.validation.heap_runtime.completeness_gate_smoke.markdown import (  # type: ignore
        render_markdown,
    )
    from Tools.validation.heap_runtime.completeness_gate_smoke.request import (  # type: ignore
        complete_smoke_request,
    )
    from Tools.validation._shared.codex_failure_counters import (  # type: ignore
        apply_codex_failure_counter_updates,
        classify_codex_failure_counters,
    )
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def provider_child_python_and_env(repo_root: Path) -> tuple[str, dict[str, str]]:
    repo_path = str(repo_root)
    if repo_path not in sys.path:
        sys.path.insert(0, repo_path)
    from Tools.ai.provider_mesh.runtime.python_runtime import command_env, resolve_child_python

    return resolve_child_python(repo_root), command_env(repo_root)


def run_gate(
    repo_root: Path,
    label: str,
    stamp: str,
    timeout_seconds: int,
    max_iterations: int,
    provider_model: str,
    allow_provider_generation: bool,
    operator_intent: bool,
    idle_stall_seconds: int,
    request_text: str = "",
) -> tuple[subprocess.CompletedProcess[str], dict[str, Any], Path, dict[str, Any]]:
    run_dir = (
        repo_root / "output" / "validation" / f"heap_runtime_completeness_gate_{label}_{stamp}"
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    output = run_dir / "heap_runtime_completeness_gate_report.json"
    child_python, env = provider_child_python_and_env(repo_root)
    command = [
        child_python,
        "Tools/ai/heap_runtime/completeness_gate/cli.py",
        "--repo-root",
        ".",
        "--stamp",
        f"{label}_{stamp}",
        "--output-dir",
        run_dir.as_posix(),
        "--max-iterations",
        str(max_iterations),
        "--budget-minutes",
        "5",
        "--max-rounds",
        str(max_iterations),
        "--timeout-seconds",
        str(timeout_seconds),
        "--provider-model",
        provider_model,
    ]
    if allow_provider_generation:
        command.append("--allow-provider-generation")
    if operator_intent:
        command.append("--operator-intent")
    if request_text.strip():
        command.extend(["--request", request_text.strip()])
    completed, watch = run_with_progress_watch(
        command,
        repo_root=repo_root,
        env=env,
        run_dir=run_dir,
        timeout_seconds=timeout_seconds,
        idle_stall_seconds=idle_stall_seconds,
    )
    return completed, read_json(output), run_dir, watch


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
        errors.append(
            "complete smoke must not pass a blocked/non-product runtime; "
            f"product_status={metrics.get('product_status')}"
        )
    if metrics.get("quality_output_passed") is not True:
        errors.append("complete smoke must fail when GPU1/pointer product quality is false")
    if metrics.get("latest_proposal_quality_passed") is False:
        errors.append(
            "complete smoke must fail when latest provider proposal iteration is rejected"
        )
    if metrics.get("latest_gpu0_review_decision", "").startswith("reject"):
        errors.append("complete smoke must fail when GPU0 rejects the GPU1 delta")
    if metrics.get("missing_requirements"):
        errors.append("complete run must have no missing requirements")
    if int(metrics.get("completed_requirement_count") or 0) != int(
        metrics.get("required_requirement_count") or -1
    ):
        errors.append("complete run must satisfy all required requirements")
    if metrics.get("budget_decision") != "allow_provider_generation":
        errors.append("complete run must use positive provider permit and operator intent")
    state = report.get("state") if isinstance(report.get("state"), dict) else {}
    for key in (
        "facts",
        "needs",
        "tool_requests",
        "shared_evidence",
        "provider_results",
        "claims",
        "decisions",
        "candidate_operations",
    ):
        value = state.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"state.{key} must contain at least one item")
    if (
        report.get("provider_execution_performed") is not True
        or metrics.get("provider_execution_performed") is not True
    ):
        errors.append("complete run must perform observable provider execution")
    lanes = set(metrics.get("provider_lane_names") or [])
    required_lanes = {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}
    if int(metrics.get("provider_lane_count") or 0) < 3 or not required_lanes <= lanes:
        errors.append("complete run must include all three provider lanes")
    output_contract = (
        report.get("real_run_output_contract")
        if isinstance(report.get("real_run_output_contract"), dict)
        else {}
    )
    if not output_contract.get("heap_event_log") or not output_contract.get(
        "provider_report_outputs"
    ):
        errors.append("complete run must expose real-run-compatible output contract")
    guardrails = report.get("guardrails") if isinstance(report.get("guardrails"), dict) else {}
    for key in ("patch_application_performed", "source_writes_performed"):
        if report.get(key) is not False or guardrails.get(key) is not False:
            errors.append(f"guardrail {key} must be false")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_runtime_completeness_gate_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_runtime_completeness_gate_smoke.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=0)
    parser.add_argument("--provider-model", default="qwen2.5-coder:14b")
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--idle-stall-seconds", type=int, default=0)
    parser.add_argument("--contract-only", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    stamp = now_stamp()
    if args.contract_only:
        errors = validate_contract_only(repo_root)
        contract_run = {
            "label": "contract_only",
            "passed": not errors,
            "run_dir": "",
            "returncode": 0 if not errors else 2,
            "scope": "static_contract_only_no_runtime_execution",
        }
        if errors:
            contract_run["errors"] = errors
        report = {
            "schema_version": 1,
            "kind": "heap_runtime_completeness_gate_smoke",
            "mode": "contract_only",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "repo_root": repo_root.as_posix(),
            "passed": not errors,
            "runs": [contract_run],
            "codex_failure_counters": classify_codex_failure_counters(
                returncodes=[contract_run["returncode"]],
                errors=errors,
                warnings=[],
                user_interrupted=False,
            ),
        }
        report["codex_failure_counter_markdown_updates"] = (
            apply_codex_failure_counter_updates(
                repo_root,
                report["codex_failure_counters"],
            )
        )
        if errors:
            report["errors"] = errors
        output = resolve_output_path(repo_root, args.output)
        markdown = resolve_output_path(repo_root, args.markdown_output)
        write_json_report(report, output)
        write_text_report(render_markdown(report), markdown)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["passed"] else 2

    request_text = complete_smoke_request(repo_root)
    runs: list[dict[str, Any]] = []
    errors: list[str] = []

    try:
        complete_proc, complete_report, complete_dir, complete_watch = run_gate(
            repo_root,
            "complete",
            stamp,
            args.timeout_seconds,
            max_iterations=max(1, int(args.max_iterations)),
            provider_model=args.provider_model,
            allow_provider_generation=True,
            operator_intent=True,
            idle_stall_seconds=args.idle_stall_seconds,
            request_text=request_text,
        )
    except KeyboardInterrupt:
        interrupted_report = {
            "schema_version": 1,
            "kind": "heap_runtime_completeness_gate_smoke",
            "mode": "complete_only",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "repo_root": repo_root.as_posix(),
            "passed": False,
            "runs": [
                {
                    "label": "complete",
                    "passed": False,
                    "run_dir": "",
                    "returncode": 130,
                    "errors": ["operator/user interrupted complete smoke run"],
                }
            ],
            "provider_execution_performed": False,
            "codex_failure_counters": classify_codex_failure_counters(
                returncodes=[],
                errors=["operator/user interrupted complete smoke run"],
                warnings=[],
                user_interrupted=True,
            ),
            "errors": ["complete: operator/user interrupted complete smoke run"],
        }
        interrupted_report["codex_failure_counter_markdown_updates"] = (
            apply_codex_failure_counter_updates(
                repo_root,
                interrupted_report["codex_failure_counters"],
            )
        )
        output = resolve_output_path(repo_root, args.output)
        markdown = resolve_output_path(repo_root, args.markdown_output)
        write_json_report(interrupted_report, output)
        write_text_report(render_markdown(interrupted_report), markdown)
        print(json.dumps(interrupted_report, indent=2, ensure_ascii=False))
        return 130
    complete_errors = []
    if complete_proc.returncode != 0:
        complete_errors.append(
            f"complete gate returned {complete_proc.returncode}: {(complete_proc.stderr or complete_proc.stdout)[-1500:]}"
        )
    complete_errors.extend(validate_complete(complete_report))
    errors.extend(f"complete: {item}" for item in complete_errors)
    runs.append(
        {
            "label": "complete",
            "passed": not complete_errors,
            "run_dir": complete_dir.relative_to(repo_root).as_posix(),
            "returncode": complete_proc.returncode,
            "outer_watchdog_seconds": outer_watchdog_seconds(args.timeout_seconds),
            "max_iterations": max(1, int(args.max_iterations)),
            "process_watch": complete_watch,
            "metrics": complete_report.get("metrics", {}),
            "errors": complete_errors,
        }
    )

    report = {
        "schema_version": 1,
        "kind": "heap_runtime_completeness_gate_smoke",
        "mode": "complete_only",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "runs": runs,
        "provider_execution_performed": any(
            bool((run.get("metrics") or {}).get("provider_execution_performed")) for run in runs
        ),
        "codex_failure_counters": classify_codex_failure_counters(
            returncodes=[run.get("returncode") for run in runs],
            errors=errors,
            warnings=[],
            user_interrupted=False,
        ),
    }
    report["codex_failure_counter_markdown_updates"] = apply_codex_failure_counter_updates(
        repo_root,
        report["codex_failure_counters"],
    )
    if errors:
        report["errors"] = errors
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
