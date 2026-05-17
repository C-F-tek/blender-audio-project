"""AI peer exchange report assembly."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .common import now_iso, read_json, repo_rel, resolve_output_path, safe_int
from .lanes import (
    build_peer_mesh_lane_state,
    build_peer_mesh_visibility,
    build_provider_broker_loop,
    npu_support_lane_summary,
)
from .primary import primary_advisory, source_summaries
from .tasks import build_tasks, tool_request_templates

def build_exchange(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    primary_path = resolve_output_path(repo_root, args.primary_output.format(stamp=args.stamp))
    task_path = resolve_output_path(repo_root, args.task_output.format(stamp=args.stamp))
    response_path = (
        resolve_output_path(repo_root, args.response_report.format(stamp=args.stamp))
        if args.response_report
        else None
    )
    broker_path = (
        resolve_output_path(repo_root, args.broker_report.format(stamp=args.stamp))
        if args.broker_report
        else None
    )
    npu_path = (
        resolve_output_path(repo_root, args.npu_report.format(stamp=args.stamp))
        if args.npu_report
        else None
    )
    npu_broker_path = (
        resolve_output_path(repo_root, args.npu_broker_report.format(stamp=args.stamp))
        if args.npu_broker_report
        else None
    )
    contract_path = (
        resolve_output_path(repo_root, args.contract_report.format(stamp=args.stamp))
        if args.contract_report
        else None
    )
    primary = primary_advisory(
        repo_root,
        args.stamp,
        resolve_output_path(repo_root, args.gpu_report),
        resolve_output_path(repo_root, args.gpu_markdown or ""),
    )
    sources = source_summaries(repo_root, args.source_report)
    tasks = build_tasks(primary, sources)
    existing_source_paths = [item["path"] for item in sources if item.get("exists")]
    passed_source_paths = [
        item["path"] for item in sources if item.get("exists") and item.get("passed") is not False
    ]
    templates = tool_request_templates(existing_source_paths, passed_source_paths)
    task_packet = {
        "schema_version": 1,
        "kind": "gpu0_peer_task_packet",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "source_lane": "gpu1_master_primary_advisory_worker",
        "target_lane": "gpu0_openvino_peer_worker",
        "passed": bool(tasks),
        "primary_advisory_report": repo_rel(repo_root, primary_path),
        "task_count": len(tasks),
        "tasks": tasks,
        "tool_request_templates": templates,
        "source_reports": sources,
        "peer_visibility": {
            "gpu0_sees_gpu1_primary_advisory": True,
            "gpu0_sees_deterministic_reports": bool(sources),
            "gpu0_produces_tool_requests_for_gpu1": True,
            "gpu0_must_return_response_for_gpu1": True,
            "gpu1_must_consume_gpu0_response": True,
            "npu_must_see_gpu1_gpu0_broker_context_when_present": True,
            "npu_is_non_blocking_tool_support_lane": True,
            "npu_slow_or_degraded_must_not_block_product": True,
            "runtime_tool_broker_required_for_tool_requests": True,
            "runtime_tool_broker_visible_to_gpu1_gpu0_npu": True,
        },
        "guardrails": {
            "report_only": True,
            "runtime_tool_broker_required_for_tool_requests": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "openvino_gpu1_workload_allowed": False,
        },
    }
    response = read_json(response_path) if response_path else {}
    broker = read_json(broker_path) if broker_path else {}
    npu = read_json(npu_path) if npu_path else {}
    npu_broker = read_json(npu_broker_path) if npu_broker_path else {}
    contract = read_json(contract_path) if contract_path else {}
    classifications = list(primary.get("classifications") or [])
    warnings: list[str] = []
    if response_path and response_path.exists():
        classifications.extend(
            str(item) for item in response.get("classifications", []) if item not in classifications
        )
    else:
        classifications.append("gpu1_gpu0_roundtrip_missing")
    tool_count = safe_int(response.get("tool_request_count"))
    broker_exec = safe_int(broker.get("tool_execution_count"))
    if tool_count and broker_exec <= 0:
        classifications.append("gpu0_tool_requests_not_broker_consumed")
    if npu_path and npu_path.exists():
        if npu.get("non_blocking") is not True:
            warnings.append("npu_micro_lane_present_but_non_blocking_flag_missing")
        if npu.get("decision", {}).get("npu_primary_advisory") is True:
            warnings.append("npu_micro_lane_attempted_primary_advisory_promotion")
    else:
        warnings.append("npu_micro_lane_missing_or_pending_non_blocking")
    collaboration_round = {
        "kind": "ai_peer_collaboration_round",
        "synchronized_visibility": True,
        "gpu1": {
            "role": "gpu1_master_planner_worker",
            "works_and_plans": True,
            "sees_gpu0_response": bool(response),
            "sees_gpu0_broker_results": broker_exec > 0,
            "sees_npu_micro_signal": bool(npu),
        },
        "gpu0": {
            "role": "gpu0_companion_tool_request_producer",
            "provider_execution_performed": bool(response.get("provider_execution_performed")),
            "produces_tool_requests": tool_count > 0,
            "broker_tool_executions": broker_exec,
        },
        "npu": {
            "role": "npu_support_tool_micro_lane_non_blocking",
            "non_blocking": True,
            "report_seen": bool(npu),
            "provider_execution_requested": bool(npu.get("provider_execution_requested")),
            "provider_execution_performed": bool(npu.get("provider_execution_performed")),
            "tool_request_count": safe_int(npu.get("tool_request_count")),
            "broker_tool_executions": safe_int(npu_broker.get("tool_execution_count")),
        },
        "deterministic_scripts": {
            "role": "tool_agnostic_heavy_audit_and_validation_authority",
            "source_report_count": len(sources),
        },
        "runtime_tool_broker": {
            "role": "controlled_tool_execution_for_gpu1_gpu0_npu_requests",
            "gpu0_tool_execution_count": broker_exec,
            "npu_tool_execution_count": safe_int(npu_broker.get("tool_execution_count")),
        },
    }
    npu_support_lane = npu_support_lane_summary(npu, npu_broker)
    peer_mesh_visibility = build_peer_mesh_visibility(
        primary, response, broker, npu, npu_broker, sources
    )
    peer_mesh_lane_state = build_peer_mesh_lane_state(
        primary,
        response,
        broker,
        npu,
        npu_broker,
        sources,
        peer_mesh_visibility,
        npu_support_lane,
    )
    provider_broker_loop = build_provider_broker_loop(
        primary,
        response,
        broker,
        npu,
        npu_broker,
        sources,
        peer_mesh_lane_state,
    )
    collaboration_round["mesh_visibility"] = peer_mesh_visibility
    collaboration_round["npu_support_lane"] = npu_support_lane
    collaboration_round["peer_mesh_lane_state"] = peer_mesh_lane_state
    collaboration_round["provider_broker_loop"] = provider_broker_loop

    exchange = {
        "schema_version": 1,
        "kind": "ai_peer_exchange",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "passed": bool(
            primary.get("passed")
            and response.get("passed") is True
            and (not tool_count or broker_exec > 0)
        ),
        "primary_advisory": primary,
        "task_packet": task_packet,
        "gpu0_response": response,
        "runtime_tool_broker": broker,
        "npu_micro_response": npu,
        "npu_runtime_tool_broker": npu_broker,
        "collaboration_round": collaboration_round,
        "peer_mesh_visibility": peer_mesh_visibility,
        "npu_support_lane": npu_support_lane,
        "peer_mesh_lane_state": peer_mesh_lane_state,
        "provider_broker_loop": provider_broker_loop,
        "provider_broker_loop_active": provider_broker_loop.get("active"),
        "peer_mesh_operational_lanes": peer_mesh_lane_state.get("operational_lanes", []),
        "peer_mesh_support_lanes": peer_mesh_lane_state.get("support_lanes", []),
        "peer_mesh_degraded_lanes": peer_mesh_lane_state.get("degraded_lanes", []),
        "peer_mesh_product_blockers": peer_mesh_lane_state.get("product_blockers", []),
        "contract": contract,
        "classifications": list(dict.fromkeys(classifications)),
        "errors": [],
        "warnings": warnings,
        "provider_execution_performed": bool(
            primary.get("provider_execution_performed")
            or response.get("provider_execution_performed")
            or npu.get("provider_execution_performed")
        ),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "paths": {
            "primary_advisory": repo_rel(repo_root, primary_path),
            "task_packet": repo_rel(repo_root, task_path),
            "gpu0_response": (repo_rel(repo_root, response_path) if response_path else ""),
            "gpu0_runtime_tool_broker": (repo_rel(repo_root, broker_path) if broker_path else ""),
            "npu_micro_response": repo_rel(repo_root, npu_path) if npu_path else "",
            "npu_runtime_tool_broker": (
                repo_rel(repo_root, npu_broker_path) if npu_broker_path else ""
            ),
            "contract": repo_rel(repo_root, contract_path) if contract_path else "",
        },
        "guardrails": {
            "report_only": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "openvino_gpu1_workload_allowed": False,
            "npu_micro_lane_non_blocking": True,
        },
    }
    return {"primary": primary, "task_packet": task_packet, "exchange": exchange}
