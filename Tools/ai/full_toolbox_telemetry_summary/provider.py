"""Provider and peer evidence summaries."""

from __future__ import annotations

from typing import Any

from .common import safe_dict, safe_int

def provider_evidence_summary(
    orchestrator: dict[str, Any], gpu_report: dict[str, Any]
) -> dict[str, Any]:
    gpu_round_count = safe_int(gpu_report.get("round_count"))
    gpu_provider_performed = bool(
        gpu_report.get("provider_execution_performed")
        and gpu_round_count > 0
        and str(gpu_report.get("classification") or "") != "required_provider_artifact_missing"
        and not bool(gpu_report.get("provider_empty_response"))
    )
    npu_audit_count = safe_int(orchestrator.get("npu_audit_count"))
    npu_success_count = safe_int(orchestrator.get("npu_audit_success_count"))
    gpu0_peer_support_count = safe_int(orchestrator.get("gpu0_peer_support_count"))
    gpu0_peer_support_success_count = safe_int(orchestrator.get("gpu0_peer_support_success_count"))
    gpu0_peer_support_overlap_count = safe_int(orchestrator.get("gpu0_peer_support_overlap_count"))
    npu_micro_support_count = safe_int(orchestrator.get("npu_micro_support_count"))
    npu_micro_support_success_count = safe_int(orchestrator.get("npu_micro_support_success_count"))
    npu_micro_support_provider_success_count = safe_int(
        orchestrator.get("npu_micro_support_provider_success_count")
    )
    npu_micro_support_tool_success_count = safe_int(
        orchestrator.get("npu_micro_support_tool_success_count")
    )
    npu_micro_support_overlap_count = safe_int(orchestrator.get("npu_micro_support_overlap_count"))
    npu_micro_support_tool_request_count = safe_int(
        orchestrator.get("npu_micro_support_tool_request_count")
    )
    npu_micro_runtime_tool_execution_count = safe_int(
        orchestrator.get("npu_micro_runtime_tool_execution_count")
    )
    npu_lane = safe_dict(orchestrator.get("npu_lane"))
    legacy_npu_requested = bool(
        orchestrator.get("legacy_npu_auditor_provider_requested")
        or orchestrator.get("npu_auditor_provider_requested")
        or npu_lane.get("provider_requested")
    )
    gpu0_peer_support_performed = gpu0_peer_support_success_count > 0 or bool(
        orchestrator.get("gpu0_peer_support_provider_execution_performed")
    )
    npu_micro_provider_performed = npu_micro_support_provider_success_count > 0 or bool(
        orchestrator.get("npu_micro_support_provider_execution_performed")
    )
    npu_micro_tool_lane_performed = bool(
        orchestrator.get("npu_micro_support_tool_lane_performed")
        or npu_micro_support_tool_success_count > 0
        or npu_micro_runtime_tool_execution_count > 0
        or npu_micro_support_tool_request_count > 0
    )
    legacy_npu_provider_performed = npu_success_count > 0
    npu_provider_performed = bool(legacy_npu_provider_performed or npu_micro_provider_performed)
    degraded_reasons = []
    if isinstance(orchestrator.get("provider_degraded_reasons"), list):
        degraded_reasons.extend(str(item) for item in orchestrator.get("provider_degraded_reasons"))
    if not gpu_provider_performed and (orchestrator or gpu_report):
        degraded_reasons.append(
            "gpu_not_confirmed:"
            f"performed={gpu_report.get('provider_execution_performed')};"
            f"round_count={gpu_round_count};"
            f"classification={gpu_report.get('classification')};"
            f"passed={gpu_report.get('passed')}"
        )
    if (
        legacy_npu_requested
        and orchestrator.get("npu_lane_mode") in {"skipped", "metadata_only", "degraded"}
        and npu_success_count == 0
    ):
        degraded_reasons.append(
            "npu_auditor_not_confirmed:"
            f"audit_count={npu_audit_count};success_count={npu_success_count};"
            f"lane_mode={orchestrator.get('npu_lane_mode')}"
        )
    return {
        "provider_execution_requested": bool(
            orchestrator.get("provider_execution_performed")
            or gpu_report.get("provider_execution_requested")
        ),
        "provider_execution_performed": bool(
            gpu_provider_performed or gpu0_peer_support_performed or npu_provider_performed
        ),
        "gpu_provider_execution_performed": gpu_provider_performed,
        "gpu0_peer_support_provider_execution_performed": gpu0_peer_support_performed,
        "gpu0_peer_support_count": gpu0_peer_support_count,
        "gpu0_peer_support_success_count": gpu0_peer_support_success_count,
        "gpu0_peer_support_overlap_count": gpu0_peer_support_overlap_count,
        "gpu_round_count": gpu_round_count,
        "gpu_returncode": orchestrator.get("gpu_returncode"),
        "gpu_classification": gpu_report.get("classification"),
        "gpu_provider_empty_response": bool(gpu_report.get("provider_empty_response")),
        "legacy_npu_auditor_provider_requested": legacy_npu_requested,
        "npu_provider_execution_performed": npu_provider_performed,
        "legacy_npu_provider_execution_performed": legacy_npu_provider_performed,
        "npu_micro_provider_execution_performed": npu_micro_provider_performed,
        "npu_micro_tool_lane_performed": npu_micro_tool_lane_performed,
        "npu_micro_support_count": npu_micro_support_count,
        "npu_micro_support_success_count": npu_micro_support_success_count,
        "npu_micro_support_provider_success_count": npu_micro_support_provider_success_count,
        "npu_micro_support_tool_success_count": npu_micro_support_tool_success_count,
        "npu_micro_support_overlap_count": npu_micro_support_overlap_count,
        "npu_micro_support_tool_request_count": npu_micro_support_tool_request_count,
        "npu_micro_runtime_tool_execution_count": npu_micro_runtime_tool_execution_count,
        "npu_audit_count": npu_audit_count,
        "npu_audit_success_count": npu_success_count,
        "npu_lane_mode": orchestrator.get("npu_lane_mode"),
        "provider_degraded_reasons": degraded_reasons,
    }

def peer_exchange_summary(
    peer_exchange: dict[str, Any], peer_contract: dict[str, Any]
) -> dict[str, Any]:
    response = (
        peer_exchange.get("gpu0_response")
        if isinstance(peer_exchange.get("gpu0_response"), dict)
        else {}
    )
    broker = (
        peer_exchange.get("runtime_tool_broker")
        if isinstance(peer_exchange.get("runtime_tool_broker"), dict)
        else {}
    )
    npu = (
        peer_exchange.get("npu_micro_response")
        if isinstance(peer_exchange.get("npu_micro_response"), dict)
        else {}
    )
    npu_broker = (
        peer_exchange.get("npu_runtime_tool_broker")
        if isinstance(peer_exchange.get("npu_runtime_tool_broker"), dict)
        else {}
    )
    return {
        "peer_exchange_seen": bool(peer_exchange),
        "peer_exchange_passed": peer_exchange.get("passed"),
        "peer_contract_passed": peer_contract.get("passed"),
        "gpu0_peer_provider_execution_performed": bool(
            response.get("provider_execution_performed")
        ),
        "gpu0_peer_tool_request_count": safe_int(response.get("tool_request_count")),
        "gpu0_peer_tool_execution_count": safe_int(broker.get("tool_execution_count")),
        "npu_micro_non_blocking": bool(npu.get("non_blocking")),
        "npu_micro_provider_execution_performed": bool(npu.get("provider_execution_performed")),
        "npu_micro_tool_request_count": safe_int(npu.get("tool_request_count")),
        "npu_micro_tool_execution_count": safe_int(npu_broker.get("tool_execution_count")),
        "classifications": peer_exchange.get("classifications")
        or peer_contract.get("classifications")
        or [],
    }

def npu_final_review_summary(provider: dict[str, Any], peer: dict[str, Any]) -> dict[str, Any]:
    gpu1_review = bool(provider.get("gpu_provider_execution_performed"))
    gpu0_review = bool(
        provider.get("gpu0_peer_support_provider_execution_performed")
        or peer.get("gpu0_peer_provider_execution_performed")
        or peer.get("gpu0_peer_tool_execution_count")
    )
    npu_support_seen = bool(
        provider.get("npu_micro_tool_lane_performed")
        or provider.get("npu_provider_execution_performed")
        or peer.get("npu_micro_tool_execution_count")
        or peer.get("npu_micro_non_blocking")
    )
    if gpu1_review and gpu0_review:
        classification = "gpu1_gpu0_npu_final_review"
        reviewers = ["gpu1", "gpu0", "deterministic_validators"]
    elif gpu1_review:
        classification = "gpu1_npu_final_review"
        reviewers = ["gpu1", "deterministic_validators"]
    elif gpu0_review:
        classification = "gpu0_npu_final_review"
        reviewers = ["gpu0", "deterministic_validators"]
    else:
        classification = "npu_final_review_missing_gpu_peer"
        reviewers = ["deterministic_validators"]
    return {
        "classification": classification,
        "npu_support_seen": npu_support_seen,
        "npu_self_check_only": False,
        "npu_final_provider_close_path_required": False,
        "final_review_on_performant_lane": classification != "npu_final_review_missing_gpu_peer",
        "reviewers": reviewers,
        "deterministic_validator_acceptance_required": True,
        "product_blocker": not npu_support_seen,
    }
