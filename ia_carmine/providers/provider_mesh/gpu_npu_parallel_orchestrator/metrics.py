from __future__ import annotations

from types import SimpleNamespace

from .common import safe_int
from .diagnostics import npu_lane_diagnostics
from .state import OrchestratorRunState


def build_orchestrator_metrics(args, state: OrchestratorRunState) -> SimpleNamespace:
    audit_records = state.audit_records
    gpu0_support_records = state.gpu0_support_records
    npu_micro_support_records = state.npu_micro_support_records
    gpu_runtime_tool_brokers = state.gpu_runtime_tool_brokers
    gpu_report = state.gpu_report
    gpu_process = state.gpu_process
    orchestrator_runtime_tool_bootstrap = state.orchestrator_runtime_tool_bootstrap
    npu_success_count = sum(
        1
        for item in audit_records
        if item.get("provider_execution_succeeded") is True
        or item.get("classification") == "usable_audit_text"
    )
    npu_tool_context_seen_count = sum(
        1 for item in audit_records if item.get("runtime_tool_context_seen") is True
    )
    npu_tool_request_count = sum(
        int(item.get("npu_tool_request_count") or 0) for item in audit_records
    )
    npu_deterministic_tool_fallback_count = sum(
        int(item.get("npu_deterministic_tool_fallback_count") or 0) for item in audit_records
    )
    npu_runtime_brokers = [
        item.get("npu_runtime_tool_broker", {})
        for item in audit_records
        if item.get("npu_runtime_tool_broker")
    ]
    npu_runtime_tool_request_count = sum(
        int(item.get("requested_tool_count") or 0) for item in npu_runtime_brokers
    )
    npu_runtime_tool_execution_count = sum(
        int(item.get("tool_execution_count") or 0) for item in npu_runtime_brokers
    )
    npu_runtime_tool_failed_count = sum(
        int(item.get("failed_tool_count") or 0) for item in npu_runtime_brokers
    )
    npu_runtime_tool_blocked_count = sum(
        int(item.get("blocked_tool_count") or 0) for item in npu_runtime_brokers
    )
    npu_runtime_tool_result_count = sum(
        len(item.get("tool_results", [])) for item in npu_runtime_brokers
    )
    gpu0_peer_support_count = len(gpu0_support_records)
    gpu0_peer_support_success_count = sum(
        1
        for item in gpu0_support_records
        if item.get("returncode") == 0
        and item.get("terminated_after_close_barrier") is not True
        and (
            item.get("provider_execution_performed") is True
            or item.get("provider_work_verified") is True
        )
    )
    gpu0_peer_support_provider_execution_performed = gpu0_peer_support_success_count > 0
    gpu0_peer_support_overlap_count = sum(
        1 for item in gpu0_support_records if item.get("launched_while_gpu1_active") is True
    )
    npu_micro_support_count = len(npu_micro_support_records)
    npu_micro_support_provider_success_count = sum(
        1
        for item in npu_micro_support_records
        if item.get("returncode") == 0
        and item.get("terminated_after_close_barrier") is not True
        and (
            item.get("provider_execution_performed") is True
            or item.get("provider_execution_succeeded") is True
            or item.get("classification") == "usable_audit_text"
        )
    )
    npu_micro_support_overlap_count = sum(
        1 for item in npu_micro_support_records if item.get("launched_while_gpu1_active") is True
    )
    npu_micro_support_tool_request_count = sum(
        int(item.get("npu_tool_request_count") or 0) for item in npu_micro_support_records
    )
    npu_micro_support_deterministic_tool_fallback_count = sum(
        int(item.get("npu_deterministic_tool_fallback_count") or 0)
        for item in npu_micro_support_records
    )
    npu_micro_live_seed_brokers = [
        item.get("npu_live_seed_runtime_tool_broker", {})
        for item in npu_micro_support_records
        if item.get("npu_live_seed_runtime_tool_broker")
    ]
    npu_micro_live_tool_seed_count = len(npu_micro_live_seed_brokers)
    npu_micro_runtime_brokers = [
        item.get("npu_runtime_tool_broker", {})
        for item in npu_micro_support_records
        if item.get("npu_runtime_tool_broker")
    ] + npu_micro_live_seed_brokers
    npu_micro_runtime_tool_request_count = sum(
        int(item.get("requested_tool_count") or 0) for item in npu_micro_runtime_brokers
    )
    npu_micro_runtime_tool_execution_count = sum(
        int(item.get("tool_execution_count") or 0) for item in npu_micro_runtime_brokers
    )
    npu_micro_runtime_tool_failed_count = sum(
        int(item.get("failed_tool_count") or 0) for item in npu_micro_runtime_brokers
    )
    npu_micro_runtime_tool_blocked_count = sum(
        int(item.get("blocked_tool_count") or 0) for item in npu_micro_runtime_brokers
    )
    npu_micro_runtime_tool_result_count = sum(
        len(item.get("tool_results", [])) for item in npu_micro_runtime_brokers
    )
    npu_micro_runtime_tool_live_request_count = sum(
        int(item.get("requested_tool_count") or 0)
        for item in npu_micro_runtime_brokers
        if item.get("executed_while_gpu1_active") is True
    )
    npu_micro_runtime_tool_live_execution_count = sum(
        int(item.get("tool_execution_count") or 0)
        for item in npu_micro_runtime_brokers
        if item.get("executed_while_gpu1_active") is True
    )
    npu_micro_runtime_tool_live_result_count = sum(
        len(item.get("tool_results", []))
        for item in npu_micro_runtime_brokers
        if item.get("executed_while_gpu1_active") is True
    )
    npu_micro_support_tool_success_count = sum(
        1
        for item in npu_micro_support_records
        if int(item.get("npu_tool_request_count") or 0) > 0
        or int(item.get("npu_deterministic_tool_fallback_count") or 0) > 0
        or (
            isinstance(item.get("npu_runtime_tool_broker"), dict)
            and int(item.get("npu_runtime_tool_broker", {}).get("tool_execution_count") or 0) > 0
        )
    )
    npu_micro_support_success_count = sum(
        1
        for item in npu_micro_support_records
        if (
            (
                item.get("returncode") == 0
                and item.get("terminated_after_close_barrier") is not True
                and (
                    item.get("provider_execution_performed") is True
                    or item.get("provider_execution_succeeded") is True
                    or item.get("classification") == "usable_audit_text"
                )
            )
            or int(item.get("npu_tool_request_count") or 0) > 0
            or int(item.get("npu_deterministic_tool_fallback_count") or 0) > 0
            or (
                isinstance(item.get("npu_runtime_tool_broker"), dict)
                and int(item.get("npu_runtime_tool_broker", {}).get("tool_execution_count") or 0)
                > 0
            )
        )
    )
    npu_micro_support_provider_execution_performed = npu_micro_support_provider_success_count > 0
    npu_micro_support_tool_lane_performed = bool(
        npu_micro_support_tool_success_count > 0
        or npu_micro_runtime_tool_execution_count > 0
        or npu_micro_support_deterministic_tool_fallback_count > 0
    )
    gpu_orchestrated_runtime_tool_request_count = sum(
        int(item.get("requested_tool_count") or 0) for item in gpu_runtime_tool_brokers
    )
    gpu_orchestrated_runtime_tool_execution_count = sum(
        int(item.get("tool_execution_count") or 0) for item in gpu_runtime_tool_brokers
    )
    gpu_orchestrated_runtime_tool_failed_count = sum(
        int(item.get("failed_tool_count") or 0) for item in gpu_runtime_tool_brokers
    )
    gpu_orchestrated_runtime_tool_blocked_count = sum(
        int(item.get("blocked_tool_count") or 0) for item in gpu_runtime_tool_brokers
    )
    gpu_orchestrated_runtime_tool_result_count = sum(
        len(item.get("tool_results", [])) for item in gpu_runtime_tool_brokers
    )
    orchestrator_runtime_tool_bootstrap_request_count = int(
        orchestrator_runtime_tool_bootstrap.get("requested_tool_count") or 0
    )
    orchestrator_runtime_tool_bootstrap_execution_count = int(
        orchestrator_runtime_tool_bootstrap.get("tool_execution_count") or 0
    )
    orchestrator_runtime_tool_bootstrap_failed_count = int(
        orchestrator_runtime_tool_bootstrap.get("failed_tool_count") or 0
    )
    orchestrator_runtime_tool_bootstrap_blocked_count = int(
        orchestrator_runtime_tool_bootstrap.get("blocked_tool_count") or 0
    )
    orchestrator_runtime_tool_bootstrap_result_count = len(
        orchestrator_runtime_tool_bootstrap.get("tool_results", [])
    )
    gpu_recommendation_count = gpu_report.get("recommendation_count")
    gpu_empty_recommendations_reason = gpu_report.get("empty_recommendations_reason", "")
    gpu_evidence_ready_count = gpu_report.get("evidence_ready_for_manual_patch_count", 0)
    gpu_recommended_next_layer = gpu_report.get("decision", {}).get(
        "recommended_next_layer"
    ) or gpu_report.get("recommended_next_layer")
    gpu_runtime_tool_broker_enabled = bool(gpu_report.get("runtime_tool_broker_enabled"))
    gpu_runtime_tool_request_count = int(gpu_report.get("runtime_tool_request_count") or 0)
    gpu_runtime_tool_execution_count = int(gpu_report.get("runtime_tool_execution_count") or 0)
    gpu_runtime_tool_failed_count = int(gpu_report.get("runtime_tool_failed_count") or 0)
    gpu_runtime_tool_blocked_count = int(gpu_report.get("runtime_tool_blocked_count") or 0)
    gpu_runtime_tool_result_count = int(gpu_report.get("runtime_tool_result_count") or 0)

    gpu_runtime_tool_bootstrap_executed = bool(gpu_report.get("runtime_tool_bootstrap_executed"))
    gpu_runtime_tool_bootstrap_passed = gpu_report.get("runtime_tool_bootstrap_passed")
    gpu_runtime_tool_bootstrap_request_count = int(
        gpu_report.get("runtime_tool_bootstrap_request_count") or 0
    )
    gpu_runtime_tool_bootstrap_execution_count = int(
        gpu_report.get("runtime_tool_bootstrap_execution_count") or 0
    )
    gpu_runtime_tool_bootstrap_failed_count = int(
        gpu_report.get("runtime_tool_bootstrap_failed_count") or 0
    )
    gpu_runtime_tool_bootstrap_blocked_count = int(
        gpu_report.get("runtime_tool_bootstrap_blocked_count") or 0
    )

    orchestrator_runtime_tool_bootstrap_executed = bool(
        orchestrator_runtime_tool_bootstrap.get("executed")
    )
    orchestrator_runtime_tool_bootstrap_enabled = bool(
        orchestrator_runtime_tool_bootstrap.get("enabled")
    )

    runtime_tool_bootstrap_executed = bool(
        gpu_runtime_tool_bootstrap_executed or orchestrator_runtime_tool_bootstrap_executed
    )
    runtime_tool_bootstrap_passed = (
        orchestrator_runtime_tool_bootstrap.get("passed")
        if orchestrator_runtime_tool_bootstrap_executed
        else gpu_runtime_tool_bootstrap_passed
    )
    runtime_tool_bootstrap_request_count = (
        gpu_runtime_tool_bootstrap_request_count + orchestrator_runtime_tool_bootstrap_request_count
    )
    runtime_tool_bootstrap_execution_count = (
        gpu_runtime_tool_bootstrap_execution_count
        + orchestrator_runtime_tool_bootstrap_execution_count
    )
    runtime_tool_bootstrap_failed_count = (
        gpu_runtime_tool_bootstrap_failed_count + orchestrator_runtime_tool_bootstrap_failed_count
    )
    runtime_tool_bootstrap_blocked_count = (
        gpu_runtime_tool_bootstrap_blocked_count + orchestrator_runtime_tool_bootstrap_blocked_count
    )

    runtime_tool_provider_request_count = (
        gpu_orchestrated_runtime_tool_request_count
        + npu_runtime_tool_request_count
        + npu_micro_runtime_tool_request_count
    )
    runtime_tool_provider_request_execution_count = (
        gpu_orchestrated_runtime_tool_execution_count
        + npu_runtime_tool_execution_count
        + npu_micro_runtime_tool_execution_count
    )
    runtime_tool_provider_request_failed_count = (
        gpu_orchestrated_runtime_tool_failed_count
        + npu_runtime_tool_failed_count
        + npu_micro_runtime_tool_failed_count
    )
    runtime_tool_provider_request_blocked_count = (
        gpu_orchestrated_runtime_tool_blocked_count
        + npu_runtime_tool_blocked_count
        + npu_micro_runtime_tool_blocked_count
    )
    runtime_tool_provider_request_result_count = (
        gpu_orchestrated_runtime_tool_result_count
        + npu_runtime_tool_result_count
        + npu_micro_runtime_tool_result_count
    )
    deterministic_runtime_tool_fallback_request_count = int(
        gpu_report.get("deterministic_runtime_tool_fallback_request_count") or 0
    )
    deterministic_runtime_tool_fallback_execution_count = int(
        gpu_report.get("deterministic_runtime_tool_fallback_execution_count") or 0
    )
    deterministic_runtime_tool_fallback_failed_count = int(
        gpu_report.get("deterministic_runtime_tool_fallback_failed_count") or 0
    )
    deterministic_runtime_tool_fallback_blocked_count = int(
        gpu_report.get("deterministic_runtime_tool_fallback_blocked_count") or 0
    )

    runtime_tool_broker_enabled = bool(
        getattr(args, "enable_runtime_tool_broker", False)
        or gpu_runtime_tool_broker_enabled
        or orchestrator_runtime_tool_bootstrap_enabled
        or orchestrator_runtime_tool_bootstrap_executed
        or gpu_runtime_tool_brokers
        or npu_runtime_brokers
        or npu_micro_runtime_brokers
    )
    runtime_tool_request_count = (
        gpu_runtime_tool_request_count
        + runtime_tool_bootstrap_request_count
        + runtime_tool_provider_request_count
    )
    runtime_tool_execution_count = (
        gpu_runtime_tool_execution_count
        + runtime_tool_bootstrap_execution_count
        + runtime_tool_provider_request_execution_count
    )
    runtime_tool_failed_count = (
        gpu_runtime_tool_failed_count
        + runtime_tool_bootstrap_failed_count
        + runtime_tool_provider_request_failed_count
    )
    runtime_tool_blocked_count = (
        gpu_runtime_tool_blocked_count
        + runtime_tool_bootstrap_blocked_count
        + runtime_tool_provider_request_blocked_count
    )
    runtime_tool_result_count = (
        gpu_runtime_tool_result_count
        + orchestrator_runtime_tool_bootstrap_result_count
        + runtime_tool_provider_request_result_count
    )
    gpu_provider_execution_performed = bool(
        gpu_report.get("provider_execution_performed")
        and gpu_process.returncode == 0
        and safe_int(gpu_report.get("round_count")) > 0
        and str(gpu_report.get("classification") or "") != "required_provider_artifact_missing"
    )
    legacy_npu_provider_execution_performed = bool(npu_success_count > 0)
    npu_provider_execution_performed = bool(
        legacy_npu_provider_execution_performed or npu_micro_support_provider_execution_performed
    )
    provider_execution_observed = bool(
        gpu_provider_execution_performed
        or gpu0_peer_support_provider_execution_performed
        or npu_provider_execution_performed
    )
    provider_degraded_reasons: list[str] = []
    if not gpu_provider_execution_performed:
        provider_degraded_reasons.append(
            "gpu_provider_not_confirmed:"
            f"returncode={gpu_process.returncode};"
            f"round_count={safe_int(gpu_report.get('round_count'))};"
            f"performed={gpu_report.get('provider_execution_performed')};"
            f"classification={gpu_report.get('classification')}"
        )
    if (
        getattr(args, "run_gpu0_peer_support_provider", False)
        and not gpu0_peer_support_provider_execution_performed
    ):
        provider_degraded_reasons.append(
            "gpu0_peer_support_not_confirmed:"
            f"support_count={gpu0_peer_support_count};"
            f"success_count={gpu0_peer_support_success_count};"
            f"overlap_count={gpu0_peer_support_overlap_count}"
        )
    if (
        getattr(args, "run_npu_micro_support_provider", False)
        and not npu_micro_support_provider_execution_performed
        and not npu_micro_support_tool_lane_performed
    ):
        provider_degraded_reasons.append(
            "npu_micro_support_not_confirmed:"
            f"support_count={npu_micro_support_count};"
            f"success_count={npu_micro_support_success_count};"
            f"overlap_count={npu_micro_support_overlap_count}"
        )
    if (
        getattr(args, "run_npu_auditor_provider", False)
        and not legacy_npu_provider_execution_performed
    ):
        provider_degraded_reasons.append(
            "npu_auditor_not_confirmed:"
            f"audit_count={len(audit_records)};success_count={npu_success_count};"
            f"lane_mode={npu_lane_diagnostics(args, audit_records).get('mode')}"
        )
    excluded = {"args", "state", "audit_records", "gpu0_support_records", "npu_micro_support_records", "gpu_runtime_tool_brokers", "gpu_report", "gpu_process", "orchestrator_runtime_tool_bootstrap", "excluded"}
    return SimpleNamespace(**{key: value for key, value in locals().items() if key not in excluded})
