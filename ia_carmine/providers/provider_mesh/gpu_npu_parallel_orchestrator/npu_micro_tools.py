from __future__ import annotations

from .common import *  # noqa: F403
from .npu_audits import run_npu_runtime_tool_broker_for_audit

def append_npu_micro_broker_result_events(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    micro: dict[str, Any],
    broker: dict[str, Any],
    warnings: list[str],
) -> None:
    round_id = record_round_id(micro)
    append_runtime_heap_event(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        source="broker",
        target="npu",
        event_type="broker_result",
        round_id=round_id,
        correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:npu-micro-broker-{round_id:03d}",
        payload={
            "summary": "Broker executed deterministic tools for NPU micro support.",
            "round": micro.get("round"),
            "tool_execution_count": broker.get("tool_execution_count"),
            "failed_tool_count": broker.get("failed_tool_count"),
            "blocked_tool_count": broker.get("blocked_tool_count"),
            "broker_output": broker.get("broker_output"),
            "executed_while_gpu1_active": broker.get("executed_while_gpu1_active"),
            "direct_execution": False,
        },
    )
    requests = micro.get("npu_tool_requests", [])
    for request in requests if isinstance(requests, list) else []:
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        if not request_id:
            continue
        append_runtime_heap_event(
            args=args,
            repo_root=repo_root,
            warnings=warnings,
            source="broker",
            target="npu",
            event_type="broker_result",
            round_id=round_id,
            correlation_id=request_id,
            payload={
                "summary": "Broker completed one NPU micro-support tool request.",
                "request_id": request_id,
                "tool": request.get("tool"),
                "round": micro.get("round"),
                "broker_output": broker.get("broker_output"),
                "tool_execution_count": broker.get("tool_execution_count"),
                "failed_tool_count": broker.get("failed_tool_count"),
                "blocked_tool_count": broker.get("blocked_tool_count"),
                "executed_while_gpu1_active": broker.get("executed_while_gpu1_active"),
                "direct_execution": False,
            },
        )

def execute_npu_micro_runtime_tool_broker(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    micro: dict[str, Any],
    warnings: list[str],
    gpu1_active: bool,
) -> None:
    if not micro.get("npu_tool_requests") or micro.get("npu_runtime_tool_broker"):
        return
    micro["npu_runtime_tool_broker"] = run_npu_runtime_tool_broker_for_audit(
        args=args,
        repo_root=repo_root,
        audit_record=micro,
    )
    broker = micro["npu_runtime_tool_broker"]
    broker["executed_while_gpu1_active"] = bool(gpu1_active)
    micro["npu_runtime_tool_broker_executed_while_gpu1_active"] = bool(gpu1_active)
    micro["npu_runtime_tool_broker_completed_at"] = now_iso()
    if broker.get("error"):
        warnings.append(
            f"NPU micro runtime tool broker round {micro.get('round')}: {broker.get('error')}"
        )
    if broker.get("returncode") not in (None, 0):
        warnings.append(
            f"NPU micro runtime tool broker round {micro.get('round')}: returncode={broker.get('returncode')}"
        )
    if broker.get("executed"):
        append_npu_micro_broker_result_events(
            args=args,
            repo_root=repo_root,
            micro=micro,
            broker=broker,
            warnings=warnings,
        )
        write_runtime_heap_snapshot(args=args, repo_root=repo_root, warnings=warnings)

def execute_npu_micro_live_tool_seed(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    round_id: int,
    record: dict[str, Any],
    warnings: list[str],
    gpu1_active: bool,
) -> None:
    if not getattr(args, "enable_runtime_tool_broker", False):
        return
    if getattr(args, "npu_micro_live_tool_seeded", False):
        return
    requests = deterministic_fallback_tool_requests(
        "NPU micro provider is non-blocking and may finish after GPU1; seed broker-controlled micro evidence while GPU1 is active.",
        max_requests=min(
            3, max(1, int(getattr(args, "npu_micro_support_max_tool_requests", 3) or 3))
        ),
    )
    for index, request in enumerate(requests, start=1):
        request["id"] = f"npu_live_seed_{round_id:03d}_{index:03d}_{request.get('id')}"
        request["source"] = "npu_micro_live_tool_seed"
        request["reason"] = f"NPU live micro-tool seed: {request.get('reason')}"
    micro = {
        "round": -1,
        "source_round": round_id,
        "npu_micro_live_tool_seed": True,
        "launched_while_gpu1_active": bool(gpu1_active),
        "npu_tool_requests": requests,
        "npu_tool_request_count": len(requests),
        "npu_deterministic_tool_fallback_used": True,
        "npu_deterministic_tool_fallback_count": len(requests),
    }
    execute_npu_micro_runtime_tool_broker(
        args=args,
        repo_root=repo_root,
        micro=micro,
        warnings=warnings,
        gpu1_active=gpu1_active,
    )
    record["npu_live_seed_runtime_tool_broker"] = micro.get("npu_runtime_tool_broker", {})
    record["npu_live_seed_runtime_tool_broker_executed_while_gpu1_active"] = bool(gpu1_active)
    record["npu_live_seed_tool_request_count"] = len(requests)
    args.npu_micro_live_tool_seeded = True
