"""Peer mesh and broker-loop evaluators."""

from __future__ import annotations

from typing import Any

from .common import add, safe_int

def evaluate_peer_mesh_visibility(
    exchange: dict[str, Any], npu: dict[str, Any], npu_broker: dict[str, Any]
) -> dict[str, Any]:
    # Validate GPU1/GPU0/NPU mesh visibility without letting slow NPU block output.
    collaboration = (
        exchange.get("collaboration_round")
        if isinstance(exchange.get("collaboration_round"), dict)
        else {}
    )
    mesh = (
        exchange.get("peer_mesh_visibility")
        if isinstance(exchange.get("peer_mesh_visibility"), dict)
        else {}
    )
    if not mesh and isinstance(collaboration.get("mesh_visibility"), dict):
        mesh = collaboration["mesh_visibility"]
    npu_support = (
        exchange.get("npu_support_lane")
        if isinstance(exchange.get("npu_support_lane"), dict)
        else {}
    )
    if not npu_support and isinstance(collaboration.get("npu_support_lane"), dict):
        npu_support = collaboration["npu_support_lane"]

    errors: list[str] = []
    warnings: list[str] = []
    classifications: list[str] = []

    required_true = {
        "gpu1_sees_gpu0_response": mesh.get("gpu1_sees_gpu0_response"),
        "gpu1_sees_gpu0_broker_results": mesh.get("gpu1_sees_gpu0_broker_results"),
        "gpu0_sees_gpu1_primary_advisory": mesh.get("gpu0_sees_gpu1_primary_advisory"),
        "runtime_tool_broker_visible_to_all_lanes": mesh.get(
            "runtime_tool_broker_visible_to_all_lanes"
        ),
    }
    for key, value in required_true.items():
        if value is not True:
            errors.append(f"peer_mesh_visibility_missing:{key}")
            add(classifications, "peer_mesh_visibility_incomplete")

    if npu:
        if mesh.get("npu_sees_gpu1_gpu0_broker_context") is not True:
            errors.append("peer_mesh_visibility_missing:npu_sees_gpu1_gpu0_broker_context")
            add(classifications, "npu_context_visibility_missing")
        if npu.get("non_blocking") is not True:
            warnings.append("npu_support_lane_non_blocking_flag_missing")
            add(classifications, "npu_support_lane_degraded")
        if (
            safe_int(npu.get("tool_request_count")) > 0
            and safe_int(npu_broker.get("tool_execution_count")) <= 0
        ):
            warnings.append("npu_support_tool_requests_not_broker_consumed_non_blocking")
            add(classifications, "npu_support_tool_supply_degraded")
        provider_requested = bool(npu.get("provider_execution_requested"))
        provider_performed = bool(npu.get("provider_execution_performed"))
        if provider_requested and not provider_performed:
            warnings.append("npu_provider_slow_or_degraded_non_blocking_support_lane")
            add(classifications, "npu_provider_slow_or_degraded_non_blocking")
    if npu_support.get("product_pass_blocker") is True:
        errors.append("npu_support_lane_marked_product_blocker")
        add(classifications, "npu_support_lane_guardrail_violation")

    return {
        "passed": not errors,
        "mesh_visibility": mesh,
        "npu_support_lane": npu_support,
        "errors": errors,
        "warnings": warnings,
        "classifications": classifications,
    }

def evaluate_provider_broker_loop(
    exchange: dict[str, Any], provider_broker_loop: dict[str, Any]
) -> dict[str, Any]:
    """Validate the provider -> broker cooperative loop as product contract."""

    collaboration = (
        exchange.get("collaboration_round")
        if isinstance(exchange.get("collaboration_round"), dict)
        else {}
    )
    if not provider_broker_loop and isinstance(collaboration.get("provider_broker_loop"), dict):
        provider_broker_loop = collaboration["provider_broker_loop"]

    errors: list[str] = []
    warnings: list[str] = []
    classifications: list[str] = []

    if not provider_broker_loop:
        errors.append("provider_broker_loop_missing")
        add(classifications, "provider_broker_loop_missing")
        return {
            "passed": False,
            "provider_broker_loop": {},
            "errors": errors,
            "warnings": warnings,
            "classifications": classifications,
        }

    if provider_broker_loop.get("active") is not True:
        errors.append("provider_broker_loop_not_active")
        add(classifications, "provider_broker_loop_not_active")
    if provider_broker_loop.get("controlled_executor") != "runtime_tool_broker":
        errors.append("provider_broker_loop_controlled_executor_not_runtime_broker")
        add(classifications, "provider_broker_loop_guardrail_violation")
    if provider_broker_loop.get("direct_tool_execution_allowed") is not False:
        errors.append("provider_broker_loop_direct_tool_execution_allowed")
        add(classifications, "provider_broker_loop_guardrail_violation")
    if safe_int(provider_broker_loop.get("gpu0_broker_tool_execution_count")) <= 0:
        errors.append("provider_broker_loop_gpu0_broker_execution_missing")
        add(classifications, "gpu0_tool_requests_not_broker_consumed")
    if safe_int(provider_broker_loop.get("broker_tool_execution_count")) <= 0:
        errors.append("provider_broker_loop_broker_execution_missing")
        add(classifications, "provider_broker_loop_broker_execution_missing")
    if provider_broker_loop.get("npu_non_blocking") is not True:
        warnings.append("provider_broker_loop_npu_non_blocking_flag_missing")
        add(classifications, "npu_support_lane_degraded")
    if provider_broker_loop.get("npu_product_pass_blocker") is True:
        errors.append("provider_broker_loop_npu_marked_product_blocker")
        add(classifications, "npu_support_lane_guardrail_violation")
    if provider_broker_loop.get("deterministic_scripts_heavy_audit_authority") is not True:
        errors.append("provider_broker_loop_deterministic_authority_missing")
        add(classifications, "deterministic_authority_missing")

    blockers = provider_broker_loop.get("product_pass_blockers")
    if isinstance(blockers, list):
        errors.extend(str(item) for item in blockers if item)

    return {
        "passed": not errors,
        "provider_broker_loop": provider_broker_loop,
        "errors": errors,
        "warnings": warnings,
        "classifications": classifications,
    }

def evidence(repo_root: Path, name: str, path: Path) -> dict[str, Any]:
    data, error = read_json(path)
    item: dict[str, Any] = {
        "name": name,
        "path": repo_rel(repo_root, path),
        "exists": path.exists(),
        "error": error,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "classifications": data.get("classifications", []),
    }
    for key in (
        "task_count",
        "response_count",
        "tool_request_count",
        "tool_execution_count",
        "runtime_tool_execution_count",
    ):
        if key in data:
            item[key] = data.get(key)
    return item
