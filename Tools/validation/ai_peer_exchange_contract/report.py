"""Report assembly for AI peer exchange contract validation."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import resolve_output_path

from .common import add, now_iso, read_json, safe_int
from .evaluators import evaluate_peer_mesh_visibility, evaluate_provider_broker_loop, evidence

def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    primary_path = resolve_output_path(repo_root, args.primary_advisory.format(stamp=args.stamp))
    task_path = resolve_output_path(repo_root, args.task_packet.format(stamp=args.stamp))
    response_path = resolve_output_path(repo_root, args.gpu0_response.format(stamp=args.stamp))
    tool_requests_path = resolve_output_path(
        repo_root, args.gpu0_tool_requests.format(stamp=args.stamp)
    )
    broker_path = (
        resolve_output_path(repo_root, args.broker_report.format(stamp=args.stamp))
        if args.broker_report
        else None
    )
    exchange_path = resolve_output_path(repo_root, args.peer_exchange.format(stamp=args.stamp))
    npu_path = (
        resolve_output_path(repo_root, args.npu_response.format(stamp=args.stamp))
        if args.npu_response
        else None
    )
    npu_broker_path = (
        resolve_output_path(repo_root, args.npu_broker_report.format(stamp=args.stamp))
        if args.npu_broker_report
        else None
    )
    primary, primary_error = read_json(primary_path)
    task, task_error = read_json(task_path)
    response, response_error = read_json(response_path)
    tool_requests, tool_requests_error = read_json(tool_requests_path)
    broker, broker_error = read_json(broker_path) if broker_path else ({}, "not_configured")
    exchange, exchange_error = read_json(exchange_path)
    npu, npu_error = read_json(npu_path) if npu_path else ({}, "not_configured")
    npu_broker, npu_broker_error = (
        read_json(npu_broker_path) if npu_broker_path else ({}, "not_configured")
    )
    errors: list[str] = []
    warnings: list[str] = []
    classifications: list[str] = []

    if primary.get("kind") != "gpu1_primary_advisory":
        errors.append(f"primary_advisory_invalid: {primary_error}")
        add(classifications, "gpu1_primary_advisory_missing")
    if primary.get("passed") is not True:
        add(classifications, "gpu1_primary_advisory_not_proven")
        errors.append("gpu1_primary_advisory_not_proven")
    if task.get("kind") != "gpu0_peer_task_packet":
        errors.append(f"gpu0_peer_task_packet_invalid: {task_error}")
        add(classifications, "gpu1_gpu0_roundtrip_missing")
    if safe_int(task.get("task_count")) <= 0:
        errors.append("gpu0_peer_task_packet_empty")
        add(classifications, "gpu1_gpu0_roundtrip_missing")
    if response.get("kind") != "gpu0_peer_response":
        errors.append(f"gpu0_peer_response_invalid: {response_error}")
        add(classifications, "gpu1_gpu0_roundtrip_missing")
    if response.get("passed") is not True:
        errors.append("gpu0_peer_response_not_passed")
        add(classifications, "gpu0_peer_response_degraded")
    if response.get("provider_execution_performed") is not True:
        add(classifications, "gpu0_peer_openvino_execution_not_proven")
        errors.append("gpu0_peer_openvino_execution_not_proven")
    if tool_requests.get("kind") != "gpu0_peer_tool_requests":
        errors.append(f"gpu0_tool_requests_invalid: {tool_requests_error}")
        add(classifications, "gpu0_tool_requests_missing")
    tool_count = (
        len(tool_requests.get("tool_requests", []))
        if isinstance(tool_requests.get("tool_requests"), list)
        else 0
    )
    if tool_count <= 0:
        errors.append("gpu0_tool_requests_empty")
        add(classifications, "gpu0_tool_requests_missing")
    broker_exec = safe_int(broker.get("tool_execution_count"))
    if args.require_broker_execution and broker_exec <= 0:
        errors.append(f"gpu0_tool_requests_not_broker_consumed: {broker_error}")
        add(classifications, "gpu0_tool_requests_not_broker_consumed")
    if exchange.get("kind") != "ai_peer_exchange":
        errors.append(f"ai_peer_exchange_invalid: {exchange_error}")
        add(classifications, "ai_peer_exchange_missing")
    collaboration = (
        exchange.get("collaboration_round")
        if isinstance(exchange.get("collaboration_round"), dict)
        else {}
    )
    if collaboration.get("synchronized_visibility") is not True:
        errors.append("collaboration_round_missing_synchronized_visibility")
        add(classifications, "ai_peer_collaboration_round_missing")
    peer_mesh_contract = evaluate_peer_mesh_visibility(exchange, npu, npu_broker)
    peer_mesh_lane_state = (
        exchange.get("peer_mesh_lane_state")
        if isinstance(exchange.get("peer_mesh_lane_state"), dict)
        else {}
    )
    peer_mesh_product_blockers = (
        peer_mesh_lane_state.get("product_blockers")
        if isinstance(peer_mesh_lane_state.get("product_blockers"), list)
        else []
    )
    provider_broker_loop = (
        exchange.get("provider_broker_loop")
        if isinstance(exchange.get("provider_broker_loop"), dict)
        else {}
    )
    provider_broker_loop_contract = evaluate_provider_broker_loop(exchange, provider_broker_loop)
    errors.extend(peer_mesh_contract["errors"])
    errors.extend(str(item) for item in peer_mesh_product_blockers if item)
    warnings.extend(peer_mesh_contract["warnings"])
    for item in peer_mesh_contract["classifications"]:
        add(classifications, item)
    errors.extend(provider_broker_loop_contract["errors"])
    warnings.extend(provider_broker_loop_contract["warnings"])
    for item in provider_broker_loop_contract["classifications"]:
        add(classifications, item)
    if peer_mesh_lane_state.get("degraded_lanes"):
        add(classifications, "peer_mesh_degraded_lanes_present_non_blocking")
    if npu_path and npu_path.exists():
        if npu.get("non_blocking") is not True:
            warnings.append(f"npu_micro_lane_non_blocking_flag_missing: {npu_error}")
        decision = npu.get("decision") if isinstance(npu.get("decision"), dict) else {}
        if decision.get("npu_primary_advisory") is True:
            errors.append("npu_micro_lane_promoted_to_primary_advisory")
            add(classifications, "npu_micro_lane_guardrail_violation")
        if (
            npu_broker_path
            and npu_broker_path.exists()
            and safe_int(npu.get("tool_request_count")) > 0
            and safe_int(npu_broker.get("tool_execution_count")) <= 0
        ):
            warnings.append(f"npu_micro_tool_requests_not_broker_consumed: {npu_broker_error}")
    else:
        warnings.append("npu_micro_lane_missing_or_pending_non_blocking")
    if (
        exchange.get("patch_application_performed") is True
        or response.get("patch_application_performed") is True
    ):
        errors.append("patch_application_performed_in_peer_exchange")
        add(classifications, "peer_exchange_guardrail_violation")
    if (
        exchange.get("source_writes_performed") is True
        or response.get("source_writes_performed") is True
    ):
        errors.append("source_writes_performed_in_peer_exchange")
        add(classifications, "peer_exchange_guardrail_violation")
    for item in (
        response.get("classifications", [])
        if isinstance(response.get("classifications"), list)
        else []
    ):
        if str(item).endswith("_unconfigured"):
            add(classifications, str(item))
            warnings.append(str(item))
    return {
        "schema_version": 1,
        "kind": "ai_peer_exchange_contract",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "repo_root": str(repo_root),
        "passed": not errors,
        "classifications": classifications,
        "errors": errors,
        "warnings": warnings,
        "peer_mesh_visibility_contract": peer_mesh_contract,
        "peer_mesh_lane_state": peer_mesh_lane_state,
        "peer_mesh_operational_lanes": peer_mesh_lane_state.get("operational_lanes", []),
        "peer_mesh_support_lanes": peer_mesh_lane_state.get("support_lanes", []),
        "peer_mesh_degraded_lanes": peer_mesh_lane_state.get("degraded_lanes", []),
        "peer_mesh_product_blockers": peer_mesh_lane_state.get("product_blockers", []),
        "provider_broker_loop_contract": provider_broker_loop_contract,
        "provider_broker_loop": provider_broker_loop_contract.get("provider_broker_loop", {}),
        "provider_execution_performed": bool(
            primary.get("provider_execution_performed")
            or response.get("provider_execution_performed")
        ),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "evidence": [
            evidence(repo_root, "gpu1_primary_advisory", primary_path),
            evidence(repo_root, "gpu0_peer_task_packet", task_path),
            evidence(repo_root, "gpu0_peer_response", response_path),
            evidence(repo_root, "gpu0_tool_requests", tool_requests_path),
            evidence(repo_root, "gpu0_runtime_tool_broker", broker_path)
            if broker_path
            else {
                "name": "gpu0_runtime_tool_broker",
                "path": "",
                "exists": False,
                "error": "not_configured",
            },
            evidence(repo_root, "npu_micro_response", npu_path)
            if npu_path
            else {
                "name": "npu_micro_response",
                "path": "",
                "exists": False,
                "error": "not_configured",
            },
            evidence(repo_root, "npu_runtime_tool_broker", npu_broker_path)
            if npu_broker_path
            else {
                "name": "npu_runtime_tool_broker",
                "path": "",
                "exists": False,
                "error": "not_configured",
            },
            evidence(repo_root, "ai_peer_exchange", exchange_path),
        ],
        "guardrails": {
            "report_only": True,
            "gpu1_primary_advisory_required": True,
            "gpu0_peer_response_required": True,
            "gpu0_broker_execution_required": bool(args.require_broker_execution),
            "npu_micro_lane_non_blocking": True,
            "npu_micro_lane_not_heavy_authority": True,
            "npu_support_tool_supply_non_blocking": True,
            "npu_slow_or_degraded_not_product_blocker": True,
            "peer_mesh_visibility_required": True,
            "deterministic_scripts_heavy_audit_authority": True,
            "provider_broker_loop_required": True,
            "provider_broker_loop_controlled_executor_required": "runtime_tool_broker",
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }

def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AI Peer Exchange Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Classifications: `{report.get('classifications')}`",
        "",
        "## Evidence",
        "",
    ]
    for item in report.get("evidence", []):
        lines.append(
            f"- `{item.get('name')}` exists=`{item.get('exists')}` passed=`{item.get('passed')}` path=`{item.get('path')}`"
        )
    mesh_contract = (
        report.get("peer_mesh_visibility_contract")
        if isinstance(report.get("peer_mesh_visibility_contract"), dict)
        else {}
    )
    if mesh_contract:
        lines.extend(["", "## Peer mesh visibility", ""])
        lines.append(f"- Passed: `{mesh_contract.get('passed')}`")
        mesh = (
            mesh_contract.get("mesh_visibility")
            if isinstance(mesh_contract.get("mesh_visibility"), dict)
            else {}
        )
        support = (
            mesh_contract.get("npu_support_lane")
            if isinstance(mesh_contract.get("npu_support_lane"), dict)
            else {}
        )
        lines.append(f"- GPU1 sees GPU0 response: `{mesh.get('gpu1_sees_gpu0_response')}`")
        lines.append(
            f"- GPU1 sees NPU support signal: `{mesh.get('gpu1_sees_npu_support_signal')}`"
        )
        lines.append(
            f"- GPU0 sees GPU1 primary advisory: `{mesh.get('gpu0_sees_gpu1_primary_advisory')}`"
        )
        lines.append(
            f"- NPU sees GPU1/GPU0/broker context: `{mesh.get('npu_sees_gpu1_gpu0_broker_context')}`"
        )
        lines.append(f"- NPU support tool supply: `{support.get('tool_supply_support')}`")
        lines.append(
            f"- NPU slow/degraded non-blocking: `{support.get('provider_slow_or_degraded')}`"
        )
        lines.append(
            f"- Peer mesh operational lanes: `{report.get('peer_mesh_operational_lanes')}`"
        )
        lines.append(f"- Peer mesh support lanes: `{report.get('peer_mesh_support_lanes')}`")
        lines.append(f"- Peer mesh degraded lanes: `{report.get('peer_mesh_degraded_lanes')}`")
        lines.append(f"- Peer mesh product blockers: `{report.get('peer_mesh_product_blockers')}`")
    loop_contract = (
        report.get("provider_broker_loop_contract")
        if isinstance(report.get("provider_broker_loop_contract"), dict)
        else {}
    )
    if loop_contract:
        loop = (
            loop_contract.get("provider_broker_loop")
            if isinstance(loop_contract.get("provider_broker_loop"), dict)
            else {}
        )
        lines.extend(["", "## Provider-broker loop", ""])
        lines.append(f"- Passed: `{loop_contract.get('passed')}`")
        lines.append(f"- Active: `{loop.get('active')}`")
        lines.append(f"- Controlled executor: `{loop.get('controlled_executor')}`")
        lines.append(
            f"- Direct tool execution allowed: `{loop.get('direct_tool_execution_allowed')}`"
        )
        lines.append(f"- Broker tool executions: `{loop.get('broker_tool_execution_count')}`")
        lines.append(f"- GPU0 broker executions: `{loop.get('gpu0_broker_tool_execution_count')}`")
        lines.append(f"- NPU broker executions: `{loop.get('npu_broker_tool_execution_count')}`")
        lines.append(f"- NPU non-blocking: `{loop.get('npu_non_blocking')}`")
        lines.append(f"- NPU product pass blocker: `{loop.get('npu_product_pass_blocker')}`")
        lines.append(
            f"- Deterministic scripts heavy audit authority: `{loop.get('deterministic_scripts_heavy_audit_authority')}`"
        )
        lines.append(f"- Product blockers: `{loop.get('product_pass_blockers')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    lines.append("")
    return "\n".join(lines)
