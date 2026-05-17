from __future__ import annotations

from .common import *  # noqa: F403
from .npu_micro_tools import (
    execute_npu_micro_live_tool_seed,
    execute_npu_micro_runtime_tool_broker,
)

def should_launch_npu_micro_support(round_id: int, every_rounds: int) -> bool:
    return round_id == 0 or round_id == 1 or round_id % max(1, every_rounds) == 0

def launch_npu_micro_support(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    round_id: int,
    source_report: Path,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    gpu1_active: bool,
) -> bool:
    if not getattr(args, "run_npu_micro_support_provider", False):
        return False
    if round_id in active_supports:
        return False
    if len(active_supports) >= max(1, args.max_concurrent_npu_micro_support):
        return False
    if any(record_round_id(item) == round_id for item in support_records):
        return False

    output_json = npu_micro_support_output_path(args, repo_root, round_id)
    command = build_npu_micro_support_command(args, repo_root, source_report, output_json, round_id)
    process = run_command_async(command, repo_root)
    active_supports[round_id] = process
    record = {
        "round": round_id,
        "source_report": repo_rel(source_report, repo_root),
        "audit_output": repo_rel(output_json, repo_root),
        "audit_markdown": repo_rel(output_json.with_suffix(".md"), repo_root),
        "started_at": now_iso(),
        "status": "running",
        "command": command,
        "launched_while_gpu1_active": bool(gpu1_active),
        "provider_execution_requested": True,
        "provider_execution_performed": False,
        "non_blocking": True,
        "micro_transaction": True,
    }
    support_records.append(record)
    append_runtime_heap_event(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        source="orchestrator",
        target="npu",
        event_type="evidence_request",
        round_id=round_id,
        correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:npu-micro-support-{round_id:03d}",
        payload={
            "summary": "NPU micro support transaction launched by orchestrator.",
            "round": round_id,
            "source_report": repo_rel(source_report, repo_root),
            "output": repo_rel(output_json, repo_root),
            "gpu1_active": bool(gpu1_active),
            "micro_transaction": True,
            "direct_tool_execution": False,
            "provider_lane": "OpenVINO NPU",
        },
    )
    record_runtime_lane_diagnostic(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        lane="npu",
        status="running",
        message="NPU micro support subprocess launched.",
        details={
            "round": round_id,
            "source_report": repo_rel(source_report, repo_root),
            "output": repo_rel(output_json, repo_root),
            "gpu1_active": bool(gpu1_active),
        },
        round_id=round_id,
        correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:npu-micro-support-{round_id:03d}:diagnostic",
    )
    execute_npu_micro_live_tool_seed(
        args=args,
        repo_root=repo_root,
        round_id=round_id,
        record=record,
        warnings=warnings,
        gpu1_active=gpu1_active,
    )
    return True

def launch_due_npu_micro_supports(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    checkpoint_dir: Path,
    launched_rounds: set[int],
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    gpu1_active: bool,
) -> None:
    if not getattr(args, "run_npu_micro_support_provider", False):
        return
    checkpoints = sorted(
        checkpoint_dir.glob("round_*.json"),
        key=lambda path: checkpoint_round(path) or 0,
    )
    for checkpoint in checkpoints:
        round_id = checkpoint_round(checkpoint)
        if round_id is None or round_id in launched_rounds:
            continue
        if not should_launch_npu_micro_support(round_id, args.npu_micro_support_every_rounds):
            launched_rounds.add(round_id)
            continue
        if len(active_supports) >= max(1, args.max_concurrent_npu_micro_support):
            return
        if launch_npu_micro_support(
            args=args,
            repo_root=repo_root,
            round_id=round_id,
            source_report=checkpoint,
            active_supports=active_supports,
            support_records=support_records,
            warnings=warnings,
            gpu1_active=gpu1_active,
        ):
            launched_rounds.add(round_id)

def harvest_finished_npu_micro_supports(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    gpu1_active: bool = False,
) -> None:
    for round_id, process in list(active_supports.items()):
        if process.poll() is None:
            continue
        stdout, stderr = collect_stdout_stderr(process)
        record = next(
            (item for item in support_records if record_round_id(item) == round_id),
            None,
        )
        if record is None:
            active_supports.pop(round_id, None)
            continue
        record.update(
            {
                "finished_at": now_iso(),
                "status": "finished",
                "returncode": process.returncode,
                "stdout_tail": stdout,
                "stderr_tail": stderr,
            }
        )
        record["elapsed_seconds"] = audit_elapsed_seconds(record)
        output_path = resolve_path(repo_root, str(record.get("audit_output") or ""))
        if output_path.exists():
            try:
                data = read_json(output_path)
                auditor = (
                    data.get("npu_auditor") if isinstance(data.get("npu_auditor"), dict) else {}
                )
                tool_requests = (
                    data.get("tool_requests") if isinstance(data.get("tool_requests"), list) else []
                )
                record.update(
                    {
                        "passed": data.get("passed"),
                        "classification": auditor.get("classification")
                        or data.get("classification"),
                        "provider_execution_requested": data.get("provider_execution_requested"),
                        "provider_load_attempted": data.get("provider_load_attempted"),
                        "provider_execution_performed": data.get("provider_execution_performed"),
                        "provider_execution_succeeded": data.get("provider_execution_succeeded"),
                        "provider_empty_response": data.get("provider_empty_response"),
                        "dependency_missing": data.get("dependency_missing"),
                        "npu_python_exists": data.get("npu_python_exists"),
                        "runtime_tool_context_seen": data.get("runtime_tool_context_seen"),
                        "runtime_tool_context_report_count": data.get(
                            "runtime_tool_context_report_count"
                        ),
                        "npu_tool_requests": tool_requests,
                        "npu_tool_request_count": len(tool_requests),
                        "npu_deterministic_tool_fallback_used": data.get(
                            "npu_deterministic_tool_fallback_used"
                        ),
                        "npu_deterministic_tool_fallback_count": data.get(
                            "npu_deterministic_tool_fallback_count"
                        ),
                        "non_blocking": data.get("non_blocking"),
                        "errors": data.get("errors", []),
                        "warnings": data.get("warnings", []),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                record["error"] = f"{type(exc).__name__}: {exc}"
        else:
            record["error"] = "npu_micro_support_output_missing"
        if process.returncode not in (None, 0):
            warnings.append(f"NPU micro support round {round_id}: returncode={process.returncode}")
        diagnostic_status = (
            "ready"
            if process.returncode == 0
            and (
                record.get("provider_execution_performed") is True
                or record.get("provider_execution_succeeded") is True
                or record.get("classification") == "usable_audit_text"
                or int(record.get("npu_tool_request_count") or 0) > 0
                or int(record.get("npu_deterministic_tool_fallback_count") or 0) > 0
            )
            else "degraded"
        )
        record_runtime_lane_diagnostic(
            args=args,
            repo_root=repo_root,
            warnings=warnings,
            lane="npu",
            status=diagnostic_status,
            message="NPU micro support provider transaction completed.",
            details={
                "round": round_id,
                "returncode": process.returncode,
                "passed": record.get("passed"),
                "classification": record.get("classification"),
                "output": record.get("audit_output"),
                "errors": record.get("errors", []),
                "warnings": record.get("warnings", []),
            },
            round_id=round_id,
            correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:npu-micro-support-{round_id:03d}:final-diagnostic",
        )
        append_runtime_heap_event(
            args=args,
            repo_root=repo_root,
            warnings=warnings,
            source="npu",
            target="gpu1",
            event_type="evidence_response",
            round_id=round_id,
            correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:npu-micro-support-{round_id:03d}",
            payload={
                "summary": "NPU micro support provider transaction completed.",
                "round": round_id,
                "passed": record.get("passed"),
                "classification": record.get("classification"),
                "provider_execution_performed": record.get("provider_execution_performed"),
                "tool_request_count": record.get("npu_tool_request_count"),
                "output": record.get("audit_output"),
                "launched_while_gpu1_active": record.get("launched_while_gpu1_active"),
                "micro_transaction": True,
                "direct_tool_execution": False,
            },
        )
        for request in (
            record.get("npu_tool_requests", [])
            if isinstance(record.get("npu_tool_requests"), list)
            else []
        ):
            if not isinstance(request, dict):
                continue
            request_id = str(request.get("id") or request.get("request_id") or "")
            append_runtime_heap_event(
                args=args,
                repo_root=repo_root,
                warnings=warnings,
                source="npu",
                target="broker",
                event_type="broker_request",
                round_id=round_id,
                correlation_id=request_id,
                payload={
                    "request_id": request_id,
                    "tool": request.get("tool"),
                    "args": request.get("args", {}),
                    "reason": request.get("reason"),
                    "source": "npu_micro_support",
                    "direct_execution": False,
                    "broker_required": True,
                },
            )
        execute_npu_micro_runtime_tool_broker(
            args=args,
            repo_root=repo_root,
            micro=record,
            warnings=warnings,
            gpu1_active=gpu1_active,
        )
        active_supports.pop(round_id, None)
