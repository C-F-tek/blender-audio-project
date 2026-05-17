"""Peer mesh lane and broker-loop summaries."""

from __future__ import annotations

from typing import Any

from .common import compact_list, safe_int

def npu_support_lane_summary(npu: dict[str, Any], npu_broker: dict[str, Any]) -> dict[str, Any]:
    # Summarize NPU as non-blocking tool-support, not heavy authority.
    auditor = npu.get("npu_auditor") if isinstance(npu.get("npu_auditor"), dict) else {}
    classification = str(auditor.get("classification") or npu.get("classification") or "")
    tool_request_count = safe_int(
        npu.get("tool_request_count") or auditor.get("tool_request_count")
    )
    broker_execution_count = safe_int(npu_broker.get("tool_execution_count"))
    provider_performed = bool(npu.get("provider_execution_performed"))
    provider_requested = bool(npu.get("provider_execution_requested"))
    fallback_used = bool(
        npu.get("npu_deterministic_tool_fallback_used")
        or auditor.get("npu_deterministic_tool_fallback_used")
    )
    slow_or_degraded = bool(
        provider_requested
        and not provider_performed
        and (
            npu.get("provider_empty_response")
            or npu.get("dependency_missing")
            or classification
            in {
                "provider_empty_response",
                "unusable_output",
                "dependency_missing_openvino_genai",
                "npu_python_missing",
            }
        )
    )
    return {
        "role": "npu_non_blocking_tool_support_lane",
        "non_blocking": True,
        "blocking": False,
        "heavy_audit_authority": False,
        "tool_supply_support": bool(tool_request_count or broker_execution_count or fallback_used),
        "tool_request_count": tool_request_count,
        "broker_tool_execution_count": broker_execution_count,
        "provider_execution_requested": provider_requested,
        "provider_execution_performed": provider_performed,
        "provider_slow_or_degraded": slow_or_degraded,
        "classification": classification,
        "deterministic_fallback_used": fallback_used,
        "product_pass_blocker": False,
    }

def build_peer_mesh_visibility(
    primary: dict[str, Any],
    response: dict[str, Any],
    broker: dict[str, Any],
    npu: dict[str, Any],
    npu_broker: dict[str, Any],
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    # Record what each AI lane can see in the peer-exchange round.
    gpu0_tool_request_count = safe_int(response.get("tool_request_count"))
    gpu0_broker_execution_count = safe_int(broker.get("tool_execution_count"))
    npu_tool_request_count = safe_int(npu.get("tool_request_count"))
    npu_broker_execution_count = safe_int(npu_broker.get("tool_execution_count"))
    npu_seen = bool(npu)
    gpu0_seen = bool(response)
    gpu0_broker_seen = bool(broker)
    npu_broker_seen = bool(npu_broker)
    return {
        "schema_version": 1,
        "kind": "ai_peer_mesh_visibility",
        "all_lanes_visible": bool(
            primary and gpu0_seen and gpu0_broker_seen and (not npu_seen or npu_broker_seen)
        ),
        "gpu1_sees_gpu0_response": gpu0_seen,
        "gpu1_sees_gpu0_broker_results": gpu0_broker_execution_count > 0,
        "gpu1_sees_npu_support_signal": npu_seen,
        "gpu1_sees_npu_broker_results": npu_broker_execution_count > 0,
        "gpu0_sees_gpu1_primary_advisory": bool(primary),
        "gpu0_sees_deterministic_reports": bool(sources),
        "gpu0_produces_tool_requests_for_gpu1": gpu0_tool_request_count > 0,
        "gpu0_tool_requests_broker_consumed": bool(
            gpu0_tool_request_count and gpu0_broker_execution_count > 0
        ),
        "npu_sees_gpu1_gpu0_broker_context": npu_seen,
        "npu_support_tool_requests_available": npu_tool_request_count > 0,
        "npu_tool_requests_broker_consumed": bool(
            npu_tool_request_count and npu_broker_execution_count > 0
        ),
        "deterministic_scripts_visible_to_gpu0": bool(sources),
        "runtime_tool_broker_visible_to_all_lanes": bool(gpu0_broker_seen or npu_broker_seen),
        "npu_non_blocking_support_lane": True,
    }

def build_peer_mesh_lane_state(
    primary: dict[str, Any],
    response: dict[str, Any],
    broker: dict[str, Any],
    npu: dict[str, Any],
    npu_broker: dict[str, Any],
    sources: list[dict[str, Any]],
    peer_mesh_visibility: dict[str, Any],
    npu_support_lane: dict[str, Any],
) -> dict[str, Any]:
    """Return product-facing lane state separate from legacy workload usability."""

    def add_unique(items: list[str], value: str) -> None:
        if value and value not in items:
            items.append(value)

    operational_lanes: list[str] = []
    support_lanes: list[str] = []
    degraded_lanes: list[str] = []
    product_blockers: list[str] = []

    gpu0_broker_exec = safe_int(broker.get("tool_execution_count"))
    npu_broker_exec = safe_int(npu_broker.get("tool_execution_count"))
    gpu0_tool_count = safe_int(response.get("tool_request_count"))
    npu_tool_count = safe_int(npu.get("tool_request_count"))

    if primary.get("passed") is True:
        add_unique(operational_lanes, "gpu1_ollama_primary_advisory")
    else:
        add_unique(product_blockers, "gpu1_primary_advisory_not_proven")

    if response:
        if response.get("provider_execution_performed") is True:
            add_unique(operational_lanes, "gpu0_openvino_peer_companion")
        if (
            response.get("openvino_gpu0_workload_passed") is True
            or response.get("provider_execution_performed") is True
        ):
            add_unique(support_lanes, "gpu0_openvino_numeric_tool_peer")
        if gpu0_tool_count or gpu0_broker_exec:
            add_unique(support_lanes, "gpu0_brokered_tool_supply")
        if "gpu0_peer_semantic_model_unconfigured" in response.get("classifications", []):
            add_unique(degraded_lanes, "gpu0_semantic_companion_model_unconfigured")
    else:
        add_unique(product_blockers, "gpu0_peer_response_missing")

    if gpu0_tool_count and gpu0_broker_exec <= 0:
        add_unique(product_blockers, "gpu0_tool_requests_not_broker_consumed")

    if gpu0_broker_exec or npu_broker_exec:
        add_unique(operational_lanes, "runtime_tool_broker")
    if sources:
        add_unique(operational_lanes, "deterministic_scripts")
    if npu:
        add_unique(operational_lanes, "npu_nonblocking_tool_support")
        if npu_tool_count or npu_broker_exec:
            add_unique(support_lanes, "npu_brokered_tool_supply")
        if npu.get("npu_deterministic_tool_fallback_used") is True:
            add_unique(support_lanes, "npu_deterministic_tool_fallback")
        if npu_support_lane.get("provider_slow_or_degraded") is True:
            add_unique(degraded_lanes, "npu_semantic_provider_slow_or_degraded")

    return {
        "schema_version": 1,
        "kind": "peer_mesh_lane_state",
        "operational_lanes": operational_lanes,
        "support_lanes": support_lanes,
        "degraded_lanes": degraded_lanes,
        "product_blockers": product_blockers,
        "gpu0_broker_tool_execution_count": gpu0_broker_exec,
        "npu_broker_tool_execution_count": npu_broker_exec,
        "broker_runtime_tool_execution_count": gpu0_broker_exec + npu_broker_exec,
        "legacy_usable_lanes_are_workload_quality_only": True,
        "npu_degraded_is_product_blocker": False,
        "npu_heavy_audit_authority": False,
        "all_required_product_lanes_present": not product_blockers,
        "mesh_visibility": peer_mesh_visibility,
        "npu_support_lane": npu_support_lane,
    }

def build_provider_broker_loop(
    primary: dict[str, Any],
    response: dict[str, Any],
    broker: dict[str, Any],
    npu: dict[str, Any],
    npu_broker: dict[str, Any],
    sources: list[dict[str, Any]],
    peer_mesh_lane_state: dict[str, Any],
) -> dict[str, Any]:
    gpu0_exec = safe_int(broker.get("tool_execution_count"))
    npu_exec = safe_int(npu_broker.get("tool_execution_count"))
    gpu0_requests = safe_int(response.get("tool_request_count"))
    npu_requests = safe_int(npu.get("tool_request_count"))
    product_blockers = compact_list(peer_mesh_lane_state.get("product_blockers"), 20)
    loop_steps = [
        {
            "id": "deterministic_baseline",
            "from": "input_md_and_static_scripts",
            "to": "gpu1_primary_advisory",
            "performed": bool(sources),
        },
        {
            "id": "gpu1_primary_advisory",
            "from": "GPU1/Ollama/RTX5080",
            "to": "GPU0/OpenVINO peer task packet",
            "performed": bool(primary.get("passed")),
        },
        {
            "id": "gpu0_peer_response",
            "from": "GPU0/OpenVINO",
            "to": "runtime broker",
            "performed": bool(
                response.get("provider_execution_performed") and (gpu0_requests or gpu0_exec)
            ),
        },
        {
            "id": "gpu0_broker_execution",
            "from": "runtime broker",
            "to": "GPU1/GPU0 read-only context",
            "performed": gpu0_exec > 0,
        },
        {
            "id": "npu_nonblocking_support",
            "from": "NPU/OpenVINO micro support lane",
            "to": "runtime broker",
            "performed": bool(npu and (npu_requests or npu_exec)),
            "blocking": False,
        },
        {
            "id": "npu_broker_execution",
            "from": "runtime broker",
            "to": "final peer exchange context",
            "performed": npu_exec > 0,
            "blocking": False,
        },
        {
            "id": "contract_telemetry_bundle",
            "from": "deterministic validators",
            "to": "patch bundle/evidence handoff",
            "performed": True,
        },
    ]
    active = bool(
        primary.get("passed")
        and response
        and gpu0_exec > 0
        and peer_mesh_lane_state.get("all_required_product_lanes_present") is True
    )
    return {
        "schema_version": 1,
        "kind": "provider_broker_loop",
        "active": active,
        "topology": "input_md -> deterministic_baseline -> GPU1 -> GPU0 -> broker -> NPU_support -> broker -> contract -> telemetry -> bundle -> patch_plan",
        "controlled_executor": "runtime_tool_broker",
        "direct_tool_execution_allowed": False,
        "provider_lanes": {
            "gpu1": "primary_advisory_planner_worker",
            "gpu0": "openvino_peer_companion_tool_request_producer",
            "npu": "nonblocking_micro_tool_support_lane",
        },
        "broker_tool_execution_count": gpu0_exec + npu_exec,
        "gpu0_broker_tool_execution_count": gpu0_exec,
        "npu_broker_tool_execution_count": npu_exec,
        "gpu0_tool_request_count": gpu0_requests,
        "npu_tool_request_count": npu_requests,
        "npu_non_blocking": True,
        "npu_product_pass_blocker": False,
        "deterministic_scripts_heavy_audit_authority": True,
        "product_pass_blockers": product_blockers,
        "loop_steps": loop_steps,
    }
