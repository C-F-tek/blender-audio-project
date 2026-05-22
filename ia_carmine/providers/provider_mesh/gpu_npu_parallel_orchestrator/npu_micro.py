from __future__ import annotations

from .common import *  # noqa: F403
from .npu_micro_tools import (
    execute_npu_micro_live_tool_seed,
    execute_npu_micro_runtime_tool_broker,
)
from .support_lanes import (
    harvest_support_records,
    launch_due_checkpoint_supports,
    launch_support_with_record,
    support_diagnostic_details,
    support_launch_blocked,
    support_response_payload,
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
    if support_launch_blocked(
        args=args,
        round_id=round_id,
        active_supports=active_supports,
        support_records=support_records,
        enabled_attr="run_npu_micro_support_provider",
        max_concurrent_attr="max_concurrent_npu_micro_support",
    ):
        return False

    output_json = npu_micro_support_output_path(args, repo_root, round_id)
    command = build_npu_micro_support_command(args, repo_root, source_report, output_json, round_id)
    record = _new_npu_record(
        repo_root=repo_root,
        round_id=round_id,
        source_report=source_report,
        output_json=output_json,
        command=command,
        gpu1_active=gpu1_active,
    )
    correlation_id = f"{getattr(args, 'runtime_heap_stamp', '')}:npu-micro-support-{round_id:03d}"
    launch_support_with_record(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        round_id=round_id,
        active_supports=active_supports,
        support_records=support_records,
        command=command,
        record=record,
        lane="npu",
        correlation_id=correlation_id,
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
        diagnostic_message="NPU micro support subprocess launched.",
        diagnostic_details={
            "round": round_id,
            "source_report": repo_rel(source_report, repo_root),
            "output": repo_rel(output_json, repo_root),
            "gpu1_active": bool(gpu1_active),
        },
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
    launch_due_checkpoint_supports(
        args=args,
        repo_root=repo_root,
        checkpoint_dir=checkpoint_dir,
        launched_rounds=launched_rounds,
        active_supports=active_supports,
        support_records=support_records,
        warnings=warnings,
        gpu1_active=gpu1_active,
        enabled_attr="run_npu_micro_support_provider",
        every_rounds=args.npu_micro_support_every_rounds,
        max_concurrent_attr="max_concurrent_npu_micro_support",
        should_launch=should_launch_npu_micro_support,
        launch_support=launch_npu_micro_support,
        checkpoint_parameter="source_report",
    )


def harvest_finished_npu_micro_supports(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    gpu1_active: bool = False,
) -> None:
    harvest_support_records(
        args=args,
        repo_root=repo_root,
        active_supports=active_supports,
        support_records=support_records,
        warnings=warnings,
        output_key="audit_output",
        lane="npu",
        label="NPU micro support",
        correlation_prefix=f"{getattr(args, 'runtime_heap_stamp', '')}:npu-micro-support",
        diagnostic_message="NPU micro support provider transaction completed.",
        absorb_report=_absorb_npu_micro_report,
        status_builder=_npu_diagnostic_status,
        diagnostic_details=lambda round_id, process, record: support_diagnostic_details(
            round_id,
            process,
            record,
            output_key="audit_output",
            extra_keys=("classification",),
        ),
        response_payload=lambda round_id, _process, record: support_response_payload(
            round_id,
            record,
            summary="NPU micro support provider transaction completed.",
            output_key="audit_output",
            extra_keys=("classification", "provider_execution_performed"),
            field_map={"tool_request_count": "npu_tool_request_count"},
            constants={"micro_transaction": True, "direct_tool_execution": False},
        ),
        after_record=lambda round_id, _process, record: _after_npu_record(
            args, repo_root, warnings, gpu1_active, round_id, record
        ),
    )


def _new_npu_record(
    *,
    repo_root: Path,
    round_id: int,
    source_report: Path,
    output_json: Path,
    command: list[str],
    gpu1_active: bool,
) -> dict[str, Any]:
    return {
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


def _absorb_npu_micro_report(record: dict[str, Any], output_path: Path) -> None:
    if not output_path.exists():
        record["error"] = "npu_micro_support_output_missing"
        return
    try:
        data = read_json(output_path)
    except Exception as exc:  # noqa: BLE001
        record["error"] = f"{type(exc).__name__}: {exc}"
        return
    auditor = data.get("npu_auditor") if isinstance(data.get("npu_auditor"), dict) else {}
    tool_requests = data.get("tool_requests") if isinstance(data.get("tool_requests"), list) else []
    record.update(
        {
            "passed": data.get("passed"),
            "classification": auditor.get("classification") or data.get("classification"),
            "provider_execution_requested": data.get("provider_execution_requested"),
            "provider_load_attempted": data.get("provider_load_attempted"),
            "provider_execution_performed": data.get("provider_execution_performed"),
            "provider_execution_succeeded": data.get("provider_execution_succeeded"),
            "provider_empty_response": data.get("provider_empty_response"),
            "dependency_missing": data.get("dependency_missing"),
            "npu_python_exists": data.get("npu_python_exists"),
            "runtime_tool_context_seen": data.get("runtime_tool_context_seen"),
            "runtime_tool_context_report_count": data.get("runtime_tool_context_report_count"),
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


def _npu_diagnostic_status(process: subprocess.Popen[str], record: dict[str, Any]) -> str:
    ready = process.returncode == 0 and (
        record.get("provider_execution_performed") is True
        or record.get("provider_execution_succeeded") is True
        or record.get("classification") == "usable_audit_text"
        or int(record.get("npu_tool_request_count") or 0) > 0
        or int(record.get("npu_deterministic_tool_fallback_count") or 0) > 0
    )
    return "ready" if ready else "degraded"


def _after_npu_record(
    args: argparse.Namespace,
    repo_root: Path,
    warnings: list[str],
    gpu1_active: bool,
    round_id: int,
    record: dict[str, Any],
) -> None:
    _append_npu_broker_requests(args, repo_root, warnings, round_id, record)
    execute_npu_micro_runtime_tool_broker(
        args=args,
        repo_root=repo_root,
        micro=record,
        warnings=warnings,
        gpu1_active=gpu1_active,
    )


def _append_npu_broker_requests(
    args: argparse.Namespace,
    repo_root: Path,
    warnings: list[str],
    round_id: int,
    record: dict[str, Any],
) -> None:
    for request in record.get("npu_tool_requests", []):
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
