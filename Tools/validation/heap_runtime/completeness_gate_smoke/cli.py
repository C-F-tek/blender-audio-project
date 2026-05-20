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
    from Tools.ai._shared.process_tree import terminate_process_tree
    from Tools.validation.heap_runtime.completeness_gate_contract import validate_contract_only
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.ai._shared.process_tree import terminate_process_tree  # type: ignore
    from Tools.validation.heap_runtime.completeness_gate_contract import (  # type: ignore
        validate_contract_only,
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
    request_text: str = "",
) -> tuple[subprocess.CompletedProcess[str], dict[str, Any], Path]:
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
    process = subprocess.Popen(
        command,
        cwd=repo_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        watchdog = timeout_seconds * max(2, max_iterations) if timeout_seconds > 0 else None
        stdout, stderr = process.communicate(timeout=watchdog)
        completed = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        terminate_process_tree(process)
        stdout, stderr = process.communicate()
        completed = subprocess.CompletedProcess(
            command,
            124,
            stdout or "",
            (stderr or "") + "\nheap runtime smoke outer watchdog expired",
        )
    return completed, read_json(output), run_dir


def complete_smoke_request(repo_root: Path) -> str:
    target = repo_root / "Tools" / "ai" / "provider_tool_loop.py"
    if not target.is_file():
        target = repo_root / "Tools" / "ai" / "heap_runtime" / "completeness_gate" / "cli.py"
    rel_target = target.relative_to(repo_root).as_posix()
    return f"""
# Heap Runtime Complete Smoke Request

Operate inside the existing IA-Carmine heap/pointer/veto loop, not as a JSON-only or tool-only probe.
Use runtime universe, shared memory evidence, provider peers and brokered tool evidence as the working context.

Concrete local scope:
- Inspect and reason about the existing repo file `{rel_target}`.
- TARGET_FILES must be exactly `{rel_target}` unless you return EXIT_DECISION=NO_PATCHABLE_TARGET.
- Do not invent Java, Gradle, placeholder paths, output/**, indexAI/**, or docs/LOCAL_VALIDATION_EVIDENCE/** as patch targets.
- If a tool is useful, request it through the native provider tool-call continuation; prose is not tool execution.

Required response shape:
- # HEAP_DELTA_PROPOSAL
- EXIT_DECISION=PATCHABLE_TARGET or EXIT_DECISION=NO_PATCHABLE_TARGET
- POINTER_ACTION=STAY_FORWARD | BACKTRACK_PROPAGATE | RESUME_FORWARD | SPLIT_TASKS | NO_PATCHABLE_TARGET
- TARGET_FILES, PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, PATCH_SKETCH, VALIDATION_COMMANDS, RISKS
""".strip()


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


def validate_provider_gate_block(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    if report.get("passed") is not False:
        errors.append("provider-gate block must not pass as a complete runtime product")
    if metrics.get("product_status") != "blocked_with_reason":
        errors.append("provider-gate block product_status must be blocked_with_reason")
    if metrics.get("budget_decision") != "provider_generation_blocked_missing_operator_intent":
        errors.append("provider-gate block must expose missing operator intent")
    if metrics.get("provider_execution_performed") is True:
        errors.append("provider-gate block must not claim provider execution")
    return errors


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Runtime Completeness Gate Smoke", "", f"- Passed: `{report.get('passed')}`"]
    for run in report.get("runs") or []:
        lines.extend(["", f"## {run.get('label')}", ""])
        lines.append(f"- Passed: `{run.get('passed')}`")
        lines.append(f"- Run dir: `{run.get('run_dir')}`")
        metrics = run.get("metrics") if isinstance(run.get("metrics"), dict) else {}
        for key in (
            "product_status",
            "completed_requirement_count",
            "required_requirement_count",
            "missing_requirements",
            "budget_exhausted",
            "tool_execution_count",
        ):
            lines.append(f"- {key}: `{metrics.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


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
    parser.add_argument("--contract-only", action="store_true")
    parser.add_argument("--include-provider-gate-block", action="store_true")
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
        }
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

    complete_proc, complete_report, complete_dir = run_gate(
        repo_root,
        "complete",
        stamp,
        args.timeout_seconds,
        max_iterations=4,
        provider_model=args.provider_model,
        allow_provider_generation=True,
        operator_intent=True,
        request_text=request_text,
    )
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
            "metrics": complete_report.get("metrics", {}),
            "errors": complete_errors,
        }
    )

    if args.include_provider_gate_block:
        blocked_proc, blocked_report, blocked_dir = run_gate(
            repo_root, "provider_gate_block", stamp, args.timeout_seconds,
            max_iterations=2, provider_model=args.provider_model,
            allow_provider_generation=True, operator_intent=False,
            request_text=request_text,
        )
        blocked_errors = []
        if blocked_proc.returncode == 0:
            blocked_errors.append("provider_gate_block returned 0 but missing operator intent must block")
        if blocked_proc.returncode not in {0, 2}:
            blocked_errors.append(f"provider_gate_block returned {blocked_proc.returncode}: {(blocked_proc.stderr or blocked_proc.stdout)[-1500:]}")
        blocked_errors.extend(validate_provider_gate_block(blocked_report))
        errors.extend(f"provider_gate_block: {item}" for item in blocked_errors)
        runs.append({
            "label": "provider_gate_block",
            "passed": not blocked_errors,
            "run_dir": blocked_dir.relative_to(repo_root).as_posix(),
            "returncode": blocked_proc.returncode,
            "metrics": blocked_report.get("metrics", {}),
            "errors": blocked_errors,
        })

    report = {
        "schema_version": 1,
        "kind": "heap_runtime_completeness_gate_smoke",
        "mode": (
            "complete_with_provider_gate_block"
            if args.include_provider_gate_block
            else "complete_only"
        ),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "runs": runs,
        "provider_execution_performed": any(
            bool((run.get("metrics") or {}).get("provider_execution_performed")) for run in runs
        ),
    }
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
