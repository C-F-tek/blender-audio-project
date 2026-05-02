#!/usr/bin/env python3
"""Run GPU deep planning and NPU checkpoint audits in parallel.

This is the non-blocking orchestration prototype:

- GPU/Ollama planner runs continuously in its own process;
- checkpoint files are monitored as they appear;
- NPU audits are launched as separate best-effort subprocesses;
- GPU planning does not wait for NPU audit completion;
- NPU audit concurrency is capped to avoid overloading the NPU/runtime;
- final report joins GPU output plus all completed NPU audits.

No patches are applied and no PR is created.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator.md"
DEFAULT_GPU_OUTPUT = "output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.json"
DEFAULT_GPU_MARKDOWN = "output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.md"
DEFAULT_CHECKPOINT_DIR = "output/ai_pipeline/gpu_deep_planning_parallel_checkpoints"
ROUND_RE = re.compile(r"round_(\d{3})\.json$")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_command_async(command: list[str], repo_root: Path) -> subprocess.Popen[str]:
    return subprocess.Popen(
        command,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )


def checkpoint_round(path: Path) -> int | None:
    match = ROUND_RE.search(path.name)
    if not match:
        return None
    return int(match.group(1))


def collect_stdout_stderr(process: subprocess.Popen[str]) -> tuple[str, str]:
    stdout = ""
    stderr = ""
    try:
        out, err = process.communicate(timeout=1)
        stdout = out or ""
        stderr = err or ""
    except subprocess.TimeoutExpired:
        return "", ""
    return stdout[-12000:], stderr[-12000:]


def build_gpu_command(args: argparse.Namespace, repo_root: Path, checkpoint_dir: Path, gpu_output: Path, gpu_markdown: Path) -> list[str]:
    command = [
        sys.executable,
        "Tools/ai/run_agent_gpu_deep_planning_supervised.py",
        "--repo-root",
        ".",
        "--use-ollama",
        "--budget-minutes",
        str(args.budget_minutes),
        "--max-rounds",
        str(args.max_rounds),
        "--files-per-round",
        str(args.files_per_round),
        "--max-context-files",
        str(args.max_context_files),
        "--max-chars-per-file",
        str(args.max_chars_per_file),
        "--max-new-tokens",
        str(args.max_new_tokens),
        "--keep-alive",
        args.keep_alive,
        "--evidence",
        args.evidence,
        "--refined-review",
        args.refined_review,
        "--checkpoint-dir",
        str(checkpoint_dir),
        "--output",
        str(gpu_output),
        "--markdown-output",
        str(gpu_markdown),
    ]
    if args.ollama_model:
        command.extend(["--ollama-model", args.ollama_model])
    if args.ollama_base_url:
        command.extend(["--ollama-base-url", args.ollama_base_url])
    if args.enable_runtime_tool_broker:
        command.append("--enable-runtime-tool-broker")
        command.extend(["--runtime-tool-output-dir", args.runtime_tool_output_dir])
        command.extend(["--runtime-tool-timeout-seconds", str(args.runtime_tool_timeout_seconds)])
        command.extend(["--runtime-tool-max-requests-per-round", str(args.runtime_tool_max_requests_per_round)])
        if args.disable_runtime_tool_bootstrap:
            command.append("--disable-runtime-tool-bootstrap")
    for report_file in args.report_file:
        command.extend(["--report-file", report_file])
    for context_root in args.context_root:
        command.extend(["--context-root", context_root])
    return command


def collect_runtime_tool_context_reports(args: argparse.Namespace, repo_root: Path, round_id: int) -> list[Path]:
    if not getattr(args, "enable_runtime_tool_broker", False):
        return []
    base = resolve_path(repo_root, args.runtime_tool_output_dir)
    candidates = [
        base / "round_000" / "round_000_runtime_tool_broker.json",
        base / f"round_{round_id:03d}" / f"round_{round_id:03d}_runtime_tool_broker.json",
    ]
    reports: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate.resolve(strict=False))
        if key in seen or not candidate.exists():
            continue
        seen.add(key)
        reports.append(candidate)
    return reports


def build_npu_command(args: argparse.Namespace, repo_root: Path, checkpoint: Path, audit_json: Path) -> list[str]:
    command = [
        sys.executable,
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        str(checkpoint),
        "--output",
        str(audit_json),
        "--markdown-output",
        str(audit_json.with_suffix(".md")),
        "--context-output",
        str(audit_json.with_name(audit_json.stem + "_context.md")),
        "--npu-output",
        str(audit_json.with_name(audit_json.stem + "_npu.md")),
        "--npu-notes-output",
        str(audit_json.with_name(audit_json.stem + "_npu_notes.md")),
        "--npu-metadata-output",
        str(audit_json.with_name(audit_json.stem + "_metadata.json")),
        "--timeout-seconds",
        str(args.npu_auditor_timeout_seconds),
        "--max-context-chars",
        str(args.npu_max_context_chars),
        "--max-prompt-chars",
        str(args.npu_max_prompt_chars),
        "--max-new-tokens",
        str(args.npu_max_new_tokens),
    ]
    round_id = checkpoint_round(checkpoint) or 0
    for context_report in collect_runtime_tool_context_reports(args, repo_root, round_id):
        command.extend(["--runtime-tool-context-report", str(context_report)])
    if args.run_npu_auditor_provider:
        command.append("--run-npu")
    else:
        command.extend(["--run-npu", "--metadata-only"])
    if args.npu_python:
        command.extend(["--npu-python", args.npu_python])
    return command


def should_launch_npu_audit(round_id: int, every_rounds: int) -> bool:
    return round_id == 1 or round_id % max(1, every_rounds) == 0


def launch_due_audits(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    checkpoint_dir: Path,
    launched_rounds: set[int],
    active_audits: dict[int, subprocess.Popen[str]],
    audit_records: list[dict[str, Any]],
) -> None:
    if len(active_audits) >= args.max_concurrent_npu_audits:
        return
    checkpoints = sorted(checkpoint_dir.glob("round_*.json"), key=lambda path: checkpoint_round(path) or 0)
    for checkpoint in checkpoints:
        round_id = checkpoint_round(checkpoint)
        if round_id is None or round_id in launched_rounds:
            continue
        if not should_launch_npu_audit(round_id, args.npu_auditor_every_rounds):
            launched_rounds.add(round_id)
            continue
        if len(active_audits) >= args.max_concurrent_npu_audits:
            return
        audit_json = checkpoint.with_name(f"round_{round_id:03d}_npu_async_audit.json")
        command = build_npu_command(args, repo_root, checkpoint, audit_json)
        process = run_command_async(command, repo_root)
        launched_rounds.add(round_id)
        active_audits[round_id] = process
        audit_records.append(
            {
                "round": round_id,
                "checkpoint": repo_rel(checkpoint, repo_root),
                "audit_output": repo_rel(audit_json, repo_root),
                "started_at": now_iso(),
                "status": "running",
                "command": command,
            }
        )


def harvest_finished_audits(
    *,
    repo_root: Path,
    active_audits: dict[int, subprocess.Popen[str]],
    audit_records: list[dict[str, Any]],
) -> None:
    for round_id, process in list(active_audits.items()):
        if process.poll() is None:
            continue
        stdout, stderr = collect_stdout_stderr(process)
        for record in audit_records:
            if record.get("round") == round_id and record.get("status") == "running":
                record["finished_at"] = now_iso()
                record["status"] = "finished"
                record["returncode"] = process.returncode
                record["stdout_tail"] = stdout
                record["stderr_tail"] = stderr
                audit_path = resolve_path(repo_root, record["audit_output"])
                if audit_path.exists():
                    try:
                        data = read_json(audit_path)
                        nested = data.get("npu_auditor", {})
                        record.update(
                            {
                                "classification": nested.get("classification"),
                                "provider_execution_requested": data.get("provider_execution_requested", nested.get("provider_execution_requested")),
                                "provider_load_attempted": data.get("provider_load_attempted", nested.get("provider_load_attempted")),
                                "provider_execution_succeeded": data.get("provider_execution_succeeded", nested.get("provider_execution_succeeded")),
                                "provider_execution_performed": data.get("provider_execution_performed", nested.get("provider_execution_performed")),
                                "dependency_missing": data.get("dependency_missing", nested.get("dependency_missing")),
                                "warnings": data.get("warnings", []),
                                "runtime_tool_context_seen": data.get("runtime_tool_context_seen"),
                                "runtime_tool_context_report_count": data.get("runtime_tool_context_report_count"),
                                "gpu_review_blocked": data.get("decision", {}).get("gpu_review_blocked"),
                            }
                        )
                    except Exception as exc:  # noqa: BLE001
                        record["parse_error"] = f"{type(exc).__name__}: {exc}"
                break
        del active_audits[round_id]


def build_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent GPU/NPU Parallel Orchestrator", ""]
    for key in [
        "passed",
        "provider_execution_performed",
        "patch_application_performed",
        "gpu_returncode",
        "elapsed_seconds",
        "npu_audit_count",
        "npu_audit_success_count",
        "npu_tool_context_seen_count",
        "gpu_recommendation_count",
        "gpu_empty_recommendations_reason",
        "gpu_evidence_ready_for_manual_patch_count",
        "runtime_tool_broker_enabled",
        "runtime_tool_request_count",
        "runtime_tool_execution_count",
        "runtime_tool_failed_count",
        "runtime_tool_blocked_count",
        "runtime_tool_result_count",
    ]:
        lines.append(f"- `{key}`: `{report.get(key)}`")
    lines.append("")
    lines.append("## Decision")
    for key, value in report.get("decision", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## NPU Audits")
    for audit in report.get("npu_audits", []):
        lines.append(f"- round `{audit.get('round')}` status=`{audit.get('status')}` class=`{audit.get('classification')}` success=`{audit.get('provider_execution_succeeded')}`")
    return "\n".join(lines) + "\n"


def run_orchestrator(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    start = time.perf_counter()
    checkpoint_dir = resolve_path(repo_root, args.checkpoint_dir)
    gpu_output = resolve_path(repo_root, args.gpu_output)
    gpu_markdown = resolve_path(repo_root, args.gpu_markdown_output)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    gpu_command = build_gpu_command(args, repo_root, checkpoint_dir, gpu_output, gpu_markdown)
    gpu_process = run_command_async(gpu_command, repo_root)
    launched_rounds: set[int] = set()
    active_audits: dict[int, subprocess.Popen[str]] = {}
    audit_records: list[dict[str, Any]] = []
    warnings: list[str] = []
    errors: list[str] = []

    try:
        while gpu_process.poll() is None:
            launch_due_audits(
                args=args,
                repo_root=repo_root,
                checkpoint_dir=checkpoint_dir,
                launched_rounds=launched_rounds,
                active_audits=active_audits,
                audit_records=audit_records,
            )
            harvest_finished_audits(repo_root=repo_root, active_audits=active_audits, audit_records=audit_records)
            time.sleep(args.poll_seconds)
    except KeyboardInterrupt:
        warnings.append("KeyboardInterrupt received; terminating GPU process and active NPU audits")
        gpu_process.terminate()
        for process in active_audits.values():
            process.terminate()

    gpu_stdout, gpu_stderr = collect_stdout_stderr(gpu_process)
    # Launch audits for final checkpoints that appeared just before GPU exit.
    launch_due_audits(
        args=args,
        repo_root=repo_root,
        checkpoint_dir=checkpoint_dir,
        launched_rounds=launched_rounds,
        active_audits=active_audits,
        audit_records=audit_records,
    )
    audit_deadline = time.perf_counter() + max(0, args.npu_final_wait_seconds)
    while active_audits and time.perf_counter() < audit_deadline:
        harvest_finished_audits(repo_root=repo_root, active_audits=active_audits, audit_records=audit_records)
        time.sleep(args.poll_seconds)
    for round_id, process in list(active_audits.items()):
        process.terminate()
        warnings.append(f"NPU audit round {round_id} terminated after final wait budget")
    harvest_finished_audits(repo_root=repo_root, active_audits=active_audits, audit_records=audit_records)

    gpu_report: dict[str, Any] = {}
    if gpu_output.exists():
        try:
            gpu_report = read_json(gpu_output)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"unable to parse GPU report: {type(exc).__name__}: {exc}")
    else:
        errors.append(f"GPU output missing: {repo_rel(gpu_output, repo_root)}")

    npu_success_count = sum(1 for item in audit_records if item.get("provider_execution_succeeded") is True or item.get("classification") == "usable_audit_text")
    npu_tool_context_seen_count = sum(1 for item in audit_records if item.get("runtime_tool_context_seen") is True)
    gpu_recommendation_count = gpu_report.get("recommendation_count")
    gpu_empty_recommendations_reason = gpu_report.get("empty_recommendations_reason", "")
    gpu_evidence_ready_count = gpu_report.get("evidence_ready_for_manual_patch_count", 0)
    gpu_recommended_next_layer = gpu_report.get("decision", {}).get("recommended_next_layer") or gpu_report.get("recommended_next_layer")
    runtime_tool_broker_enabled = bool(gpu_report.get("runtime_tool_broker_enabled"))
    runtime_tool_request_count = int(gpu_report.get("runtime_tool_request_count") or 0)
    runtime_tool_execution_count = int(gpu_report.get("runtime_tool_execution_count") or 0)
    runtime_tool_failed_count = int(gpu_report.get("runtime_tool_failed_count") or 0)
    runtime_tool_blocked_count = int(gpu_report.get("runtime_tool_blocked_count") or 0)
    runtime_tool_result_count = int(gpu_report.get("runtime_tool_result_count") or 0)
    runtime_tool_bootstrap_executed = bool(gpu_report.get("runtime_tool_bootstrap_executed"))
    runtime_tool_bootstrap_passed = gpu_report.get("runtime_tool_bootstrap_passed")
    runtime_tool_bootstrap_request_count = int(gpu_report.get("runtime_tool_bootstrap_request_count") or 0)
    runtime_tool_bootstrap_execution_count = int(gpu_report.get("runtime_tool_bootstrap_execution_count") or 0)
    runtime_tool_bootstrap_failed_count = int(gpu_report.get("runtime_tool_bootstrap_failed_count") or 0)
    runtime_tool_bootstrap_blocked_count = int(gpu_report.get("runtime_tool_bootstrap_blocked_count") or 0)
    report = {
        "schema_version": 1,
        "kind": "agent_gpu_npu_parallel_orchestrator",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors and gpu_process.returncode == 0,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
        "elapsed_seconds": round(time.perf_counter() - start, 3),
        "gpu_returncode": gpu_process.returncode,
        "gpu_stdout_tail": gpu_stdout,
        "gpu_stderr_tail": gpu_stderr,
        "gpu_output": repo_rel(gpu_output, repo_root),
        "gpu_markdown": repo_rel(gpu_markdown, repo_root),
        "gpu_recommendation_count": gpu_recommendation_count,
        "gpu_empty_recommendations_reason": gpu_empty_recommendations_reason,
        "gpu_evidence_ready_for_manual_patch_count": gpu_evidence_ready_count,
        "gpu_recommended_next_layer": gpu_recommended_next_layer,
        "runtime_tool_broker_enabled": runtime_tool_broker_enabled,
        "runtime_tool_bootstrap_executed": runtime_tool_bootstrap_executed,
        "runtime_tool_bootstrap_passed": runtime_tool_bootstrap_passed,
        "runtime_tool_bootstrap_request_count": runtime_tool_bootstrap_request_count,
        "runtime_tool_bootstrap_execution_count": runtime_tool_bootstrap_execution_count,
        "runtime_tool_bootstrap_failed_count": runtime_tool_bootstrap_failed_count,
        "runtime_tool_bootstrap_blocked_count": runtime_tool_bootstrap_blocked_count,
        "runtime_tool_request_count": runtime_tool_request_count,
        "runtime_tool_execution_count": runtime_tool_execution_count,
        "runtime_tool_failed_count": runtime_tool_failed_count,
        "runtime_tool_blocked_count": runtime_tool_blocked_count,
        "runtime_tool_result_count": runtime_tool_result_count,
        "gpu_summary": {
            "passed": gpu_report.get("passed"),
            "round_count": gpu_report.get("round_count"),
            "recommendation_count": gpu_recommendation_count,
            "raw_recommendation_candidate_count": gpu_report.get("raw_recommendation_candidate_count"),
            "filtered_recommendation_count": gpu_report.get("filtered_recommendation_count"),
            "json_parse_error_count": gpu_report.get("json_parse_error_count"),
            "repair_attempt_count": gpu_report.get("repair_attempt_count"),
            "empty_recommendations_reason": gpu_empty_recommendations_reason,
            "evidence_ready_for_manual_patch_count": gpu_evidence_ready_count,
            "recommended_next_layer": gpu_recommended_next_layer,
            "runtime_tool_broker_enabled": runtime_tool_broker_enabled,
            "runtime_tool_request_count": runtime_tool_request_count,
            "runtime_tool_execution_count": runtime_tool_execution_count,
            "runtime_tool_failed_count": runtime_tool_failed_count,
            "runtime_tool_blocked_count": runtime_tool_blocked_count,
            "runtime_tool_result_count": runtime_tool_result_count,
            "decision": gpu_report.get("decision", {}),
        },
        "checkpoint_dir": repo_rel(checkpoint_dir, repo_root),
        "npu_audit_count": len(audit_records),
        "npu_audit_success_count": npu_success_count,
        "npu_tool_context_seen_count": npu_tool_context_seen_count,
        "npu_audits": audit_records,
        "decision": {
            "gpu_review_blocked_by_npu": False,
            "npu_auditor_mode": "parallel_best_effort",
            "npu_audit_success_count": npu_success_count,
            "npu_tool_context_seen_count": npu_tool_context_seen_count,
            "ready_for_patch_plan": bool(gpu_report.get("decision", {}).get("ready_for_patch_plan")),
            "fallback_patch_plan_recommended": bool(gpu_report.get("decision", {}).get("fallback_patch_plan_recommended")),
            "recommended_next_layer": gpu_recommended_next_layer,
            "gpu_empty_recommendations_reason": gpu_empty_recommendations_reason,
            "runtime_tool_broker_enabled": runtime_tool_broker_enabled,
            "runtime_tool_result_count": runtime_tool_result_count,
            "manual_review_required": True,
        },
        "guardrails": {
            "gpu_continues_without_waiting_for_npu": True,
            "npu_auditor_non_blocking": True,
            "npu_primary_advisory": False,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "runtime_tool_broker_report_only": True,
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--budget-minutes", type=int, default=30)
    parser.add_argument("--max-rounds", type=int, default=24)
    parser.add_argument("--files-per-round", type=int, default=10)
    parser.add_argument("--max-context-files", type=int, default=300)
    parser.add_argument("--max-chars-per-file", type=int, default=8000)
    parser.add_argument("--max-new-tokens", type=int, default=4800)
    parser.add_argument("--keep-alive", default="35m")
    parser.add_argument("--ollama-model", default=None)
    parser.add_argument("--ollama-base-url", default=None)
    parser.add_argument("--evidence", default="output/ai_pipeline/agent_review_evidence_sufficiency.json")
    parser.add_argument("--refined-review", default="output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json")
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--context-root", action="append", default=[])
    parser.add_argument("--enable-runtime-tool-broker", action="store_true")
    parser.add_argument("--runtime-tool-output-dir", default="output/ai_runtime_tools/gpu_planner_runtime_tools")
    parser.add_argument("--runtime-tool-timeout-seconds", type=int, default=300)
    parser.add_argument("--runtime-tool-max-requests-per-round", type=int, default=8)
    parser.add_argument("--run-npu-auditor-provider", action="store_true")
    parser.add_argument("--npu-python", default=None)
    parser.add_argument("--npu-auditor-every-rounds", type=int, default=4)
    parser.add_argument("--max-concurrent-npu-audits", type=int, default=1)
    parser.add_argument("--npu-auditor-timeout-seconds", type=int, default=600)
    parser.add_argument("--npu-max-context-chars", type=int, default=12000)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=8000)
    parser.add_argument("--npu-max-new-tokens", type=int, default=512)
    parser.add_argument("--npu-final-wait-seconds", type=int, default=120)
    parser.add_argument("--poll-seconds", type=float, default=2.0)
    parser.add_argument("--checkpoint-dir", default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--gpu-output", default=DEFAULT_GPU_OUTPUT)
    parser.add_argument("--gpu-markdown-output", default=DEFAULT_GPU_MARKDOWN)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_orchestrator(args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(build_markdown(report), encoding="utf-8")
    print(json.dumps({
        "passed": report["passed"],
        "output": str(output),
        "markdown": str(markdown),
        "provider_execution_performed": report["provider_execution_performed"],
        "patch_application_performed": report["patch_application_performed"],
        "elapsed_seconds": report["elapsed_seconds"],
        "gpu_returncode": report["gpu_returncode"],
        "gpu_round_count": report["gpu_summary"].get("round_count"),
        "gpu_recommendation_count": report["gpu_summary"].get("recommendation_count"),
        "gpu_empty_recommendations_reason": report.get("gpu_empty_recommendations_reason"),
        "gpu_evidence_ready_for_manual_patch_count": report.get("gpu_evidence_ready_for_manual_patch_count"),
        "gpu_recommended_next_layer": report.get("gpu_recommended_next_layer"),
        "runtime_tool_broker_enabled": report.get("runtime_tool_broker_enabled"),
        "runtime_tool_bootstrap_executed": report.get("runtime_tool_bootstrap_executed"),
        "runtime_tool_bootstrap_passed": report.get("runtime_tool_bootstrap_passed"),
        "runtime_tool_bootstrap_request_count": report.get("runtime_tool_bootstrap_request_count"),
        "runtime_tool_bootstrap_execution_count": report.get("runtime_tool_bootstrap_execution_count"),
        "runtime_tool_bootstrap_failed_count": report.get("runtime_tool_bootstrap_failed_count"),
        "runtime_tool_bootstrap_blocked_count": report.get("runtime_tool_bootstrap_blocked_count"),
        "runtime_tool_request_count": report.get("runtime_tool_request_count"),
        "runtime_tool_execution_count": report.get("runtime_tool_execution_count"),
        "runtime_tool_failed_count": report.get("runtime_tool_failed_count"),
        "runtime_tool_blocked_count": report.get("runtime_tool_blocked_count"),
        "runtime_tool_result_count": report.get("runtime_tool_result_count"),
        "npu_audit_count": report["npu_audit_count"],
        "npu_audit_success_count": report["npu_audit_success_count"],
        "npu_tool_context_seen_count": report.get("npu_tool_context_seen_count"),
        "gpu_review_blocked_by_npu": report["decision"]["gpu_review_blocked_by_npu"],
    }, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
