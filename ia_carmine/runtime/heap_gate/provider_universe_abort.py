"""Provider-universe abort helpers for heap runtime gate."""
from __future__ import annotations
from ia_carmine.runtime.heap_gate.arbiter_product import publish_candidate_operation
from ia_carmine.runtime.heap_gate.runtime_common import Any, now_iso, repo_rel, subprocess


PRIMARY_LANE = "gpu1_planner"
RECOVERABLE_SIDECAR_LANES = {"gpu0_peer", "npu_micro_task_auditor"}
HARD_PRIMARY_REASON_MARKERS = (
    "gpu1_primary",
    "gpu1_planner",
    "primary_lane",
    "provider_universe_primary",
    "provider_boot_gate_failed",
    "provider_replight_failed",
)
RECOVERABLE_SIDECAR_REASON_MARKERS = (
    "sidecar_invalid",
    "sidecar_incongruent",
    "gpu0_peer_followup_pending",
    "npu_peer_followup_pending",
    "gpu0_review_invalid_requires_gpu1_retry",
    "gpu0_checked_wrong_gpu1_packet",
    "gpu0_secondary_decision_incongruent",
    "gpu0_secondary_schema_invalid",
    "npu_followup_pending",
)


def provider_universe_abort_reason(prepared: list[dict[str, Any]]) -> str:
    for item in prepared:
        report = item.get("provider_report")
        if not isinstance(report, dict):
            continue
        status = str(report.get("status") or "")
        if status in {"failed", "non_operational"}:
            if recoverable_sidecar_failure_reason(item, report):
                continue
            exact = str(
                report.get("product_blocked_reason")
                or report.get("provider_activity_classification")
                or ""
            )
            if exact:
                return exact
            return f"provider_universe_lane_not_active:{item.get('lane')}:{status}"
    return ""


def recoverable_sidecar_failure_reason(
    item: dict[str, Any] | None,
    report: dict[str, Any] | None = None,
) -> str:
    """Return a recoverable sidecar reason instead of a hard universe abort.

    GPU0/NPU are evidence sidecars. Once a sidecar produced observable work for a
    GPU1 packet, incoherent or invalid output must be consumed by a later GPU1
    congruence/recovery revision, not converted into a terminal provider abort.
    """
    item = item if isinstance(item, dict) else {}
    report = report if isinstance(report, dict) else item.get("provider_report")
    report = report if isinstance(report, dict) else {}
    lane = str(report.get("lane") or item.get("lane") or report.get("provider_id") or "")
    if lane not in RECOVERABLE_SIDECAR_LANES:
        return ""
    if not _sidecar_observed_work(report):
        return ""
    if lane == "gpu0_peer":
        decision = str(
            report.get("gpu0_effective_decision")
            or report.get("gpu0_decision")
            or ""
        ).strip().lower()
        if decision == "incongruent":
            return "sidecar_incongruent:gpu0_peer"
        if report.get("gpu0_secondary_schema_valid") is not True:
            return "sidecar_invalid:gpu0_peer"
        if decision in {"veto", "refine_required"}:
            return f"sidecar_incongruent:gpu0_peer:{decision}"
    if lane == "npu_micro_task_auditor":
        audit = report.get("npu_operational_audit")
        audit = audit if isinstance(audit, dict) else {}
        decision = str(audit.get("decision") or report.get("npu_micro_decision") or "").lower()
        if (
            report.get("provider_rejection_reason")
            or report.get("provider_work_verified") is False
            or report.get("semantic_contract_passed") is False
            or decision.startswith("reject")
            or "reject_until" in str(report.get("response_text") or "").lower()
        ):
            return "sidecar_invalid:npu_micro_task_auditor"
    exact = str(
        report.get("provider_rejection_reason")
        or report.get("product_blocked_reason")
        or ""
    ).strip()
    status = str(report.get("status") or "").strip()
    if exact:
        return f"sidecar_invalid:{lane}:{exact}"
    if status in {"failed", "non_operational"}:
        return f"sidecar_invalid:{lane}:{status}"
    return ""


def _sidecar_observed_work(report: dict[str, Any]) -> bool:
    lane_specific_compute = bool(
        report.get("provider_work_verified")
        or report.get("provider_execution_performed")
        or report.get("operational_provider_activity")
        or report.get("npu_peer_evidence_verified")
        or report.get("npu_peer_activity_performed")
        or report.get("npu_device_workload_performed")
        or report.get("npu_micro_provider_execution_performed")
        or report.get("npu_provider_execution_performed")
        or report.get("semantic_provider_execution_performed")
        or report.get("native_tool_loop_performed")
        or report.get("ollama_compute_verified")
    )
    token_compute = bool(
        (
            _positive_count(report.get("completion_token_count"))
            or _positive_count(report.get("prompt_token_count"))
            or _positive_count(report.get("eval_count"))
            or _positive_count(report.get("prompt_eval_count"))
        )
        and (
            report.get("provider_device_verified")
            or report.get("device_identity_verified")
            or report.get("provider_backend_device_id")
            or report.get("provider_compute_device")
        )
    )
    return bool(lane_specific_compute or token_compute)


def _positive_count(value: Any) -> bool:
    try:
        return int(value or 0) > 0
    except (TypeError, ValueError):
        return False


def primary_provider_report(prepared: list[dict[str, Any]]) -> dict[str, Any]:
    for item in prepared:
        if item.get("lane") == PRIMARY_LANE and isinstance(item.get("provider_report"), dict):
            return item["provider_report"]
    return {}


def primary_provider_block_reason(prepared: list[dict[str, Any]]) -> str:
    report = primary_provider_report(prepared)
    if not report:
        return "provider_universe_primary_lane_missing_report"
    exact = str(
        report.get("product_blocked_reason")
        or report.get("provider_activity_classification")
        or ""
    )
    if report.get("status") != "ready":
        return exact or f"provider_universe_primary_lane_not_ready:{report.get('status')}"
    if not report.get("operational_provider_activity"):
        classification = report.get("provider_activity_classification") or "unknown"
        return f"provider_universe_primary_lane_not_operational:{classification}"
    return ""


def block_unstarted_provider_items(items: list[dict[str, Any]], reason: str) -> None:
    for item in items:
        if item.get("completed") is not None or item.get("started_at"):
            continue
        item["blocked_reason"] = reason
        item["completed_at"] = now_iso()
        item["elapsed_seconds"] = 0.0
        item["completed"] = subprocess.CompletedProcess(
            list(item.get("command") or []),
            130,
            "",
            f"provider lane not started because primary lane blocked universe: {reason}",
        )


def block_provider_universe_run(gate: Any, reason: str, round_id: int, revision: int) -> None:
    if not reason:
        return
    if _provider_recovery_should_run_before_terminal_product(gate, reason):
        gate.provider_universe_deferred_block_reason = reason
        deferred = {
            "reason": reason,
            "revision": revision,
            "round": round_id,
            "deferred_for": "gpu1_recovery_revision",
        }
        state = getattr(gate, "state", None)
        if isinstance(state, dict):
            state.setdefault("provider_universe_deferred_blocks", []).append(deferred)
        if reason not in getattr(gate, "warnings", []):
            gate.warnings.append(reason)
        signal = {
            "id": "provider_universe_block_deferred_for_gpu1_recovery",
            "from": "provider_universe",
            "decision": "defer_terminal_block_until_gpu1_recovery",
            "reason": reason,
            "revision": revision,
            "round": round_id,
        }
        gate.publish(
            "deterministic",
            "validation_signal",
            signal,
            target="gpu1",
            correlation_id=f"{gate.stamp}:provider-universe-recovery-deferred",
            round_id=round_id,
        )
        return
    gate.provider_universe_blocked_reason = reason
    if reason not in gate.errors:
        gate.errors.append(reason)
    decision = {
        "id": "provider_universe_blocked",
        "from": "provider_universe",
        "decision": "blocked_with_reason",
        "reason": reason,
        "revision": revision,
        "round": round_id,
    }
    if not any(item.get("id") == decision["id"] for item in gate.state.get("decisions", [])):
        gate.state["decisions"].append(decision)
        gate.decision_count += 1
        gate.publish(
            "deterministic",
            "decision",
            decision,
            target="orchestrator",
            correlation_id=f"{gate.stamp}:provider-universe-blocked",
            round_id=round_id,
        )
    final_response_text = gate.build_final_response_text(gate.read_events())
    request_input_evidence = gate.request_input_ref_or_tail()
    response_evidence = gate.response_text_ref_or_tail(
        final_response_text,
        name="provider_universe_blocked_response_text",
        kind="blocked_response_text",
        producer="provider_universe_abort",
    )
    provider_response_evidence = gate.provider_response_refs_or_tails()
    product = {
        "required": True,
        "product_kind": "blocked_continuation_product",
        "status": "blocked_with_reason",
        "product_status": "blocked_with_reason",
        "product_blocked_reason": reason,
        "failed_provider": _failed_provider_from_reason(reason),
        **gate.prefixed_text_evidence_fields("request_input", request_input_evidence),
        **gate.prefixed_text_evidence_fields("response_text", response_evidence),
        "response_source": gate.response_source(),
        "heap_event_refs": [repo_rel(gate.repo_root, gate.heap.paths.events)],
        "provider_refs": gate.provider_refs(),
        "provider_replight_required": True,
        "provider_replight_reports": _provider_replight_reports(gate),
        "provider_response_refs_or_tails": provider_response_evidence,
        "provider_role_decisions": gate.provider_role_decisions(),
        "missing_requirements": [reason],
        "reason": reason,
        "provider_universe_blocked": True,
        "continuation_required": True,
        "soft_close_reason": reason,
    }
    gate.state["product"] = product
    gate.publish(
        "orchestrator",
        "product_signal",
        product,
        correlation_id=f"{gate.stamp}:provider-universe-product-blocked",
        round_id=round_id,
    )
    gate.state.setdefault("candidate_operations", [])
    if not hasattr(gate, "candidate_operation_count"):
        gate.candidate_operation_count = 0
    publish_candidate_operation(gate, ready=False, missing=[reason], round_id=round_id)


def _provider_recovery_should_run_before_terminal_product(gate: Any, reason: str) -> bool:
    if not _recoverable_sidecar_terminal_reason(reason):
        return False
    try:
        from ia_carmine.runtime.heap_gate.provider_recovery import provider_recovery_status

        status = provider_recovery_status(gate, gate.read_events())
    except Exception:
        return False
    return bool(
        status.get("provider_recovery_required")
        and status.get("sidecar_recoverable_failure")
        and not status.get("provider_recovery_attempted")
        and not status.get("provider_revision_budget_exhausted")
    )


def _recoverable_sidecar_terminal_reason(reason: str) -> bool:
    lowered = str(reason or "").strip().lower()
    if not lowered:
        return False
    if any(marker in lowered for marker in HARD_PRIMARY_REASON_MARKERS):
        return False
    if any(marker in lowered for marker in RECOVERABLE_SIDECAR_REASON_MARKERS):
        return True
    return bool(
        ("gpu0" in lowered or "npu" in lowered or "sidecar" in lowered)
        and any(token in lowered for token in ("followup", "retry", "refine", "veto", "incongruent", "invalid"))
    )


def _failed_provider_from_reason(reason: str) -> str:
    parts = str(reason or "").split(":")
    if len(parts) >= 2 and parts[0] == "provider_replight_failed":
        return parts[1]
    if len(parts) >= 2 and parts[0] == "provider_boot_gate_failed":
        return parts[1]
    for lane in ("gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"):
        if lane in str(reason or ""):
            return lane
    return ""


def _provider_replight_reports(gate: Any) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for report in (
        list(getattr(gate, "provider_replight_reports", []) or [])
        + list(getattr(gate, "provider_reports", []) or [])
    ):
        if not isinstance(report, dict):
            continue
        reports.append(
            {
                "provider_id": report.get("provider_id") or report.get("lane"),
                "provider_role": report.get("provider_role") or report.get("role"),
                "provider_model": report.get("provider_model") or report.get("selected_model"),
                "requested_provider_model": report.get("requested_provider_model"),
                "selected_provider_model": report.get("selected_provider_model") or report.get("selected_model"),
                "model_switch_reason": report.get("model_switch_reason"),
                "provider_backend": report.get("provider_backend"),
                "provider_compute_device": report.get("provider_compute_device"),
                "full_gpu_residency_required": report.get("full_gpu_residency_required"),
                "full_gpu_residency_verified": report.get("full_gpu_residency_verified"),
                "device_workload_performed": report.get("device_workload_execution_performed")
                or report.get("npu_device_workload_performed"),
                "semantic_provider_model_loaded": report.get("semantic_provider_model_loaded")
                or report.get("npu_micro_provider_model_loaded"),
                "provider_loaded": report.get("provider_loaded"),
                "generated_phrase": report.get("generated_phrase"),
                "prompt_token_count": report.get("prompt_token_count"),
                "completion_token_count": report.get("completion_token_count"),
                "tokens_per_second": report.get("tokens_per_second"),
                "native_tool_calling_supported": report.get(
                    "native_tool_calling_supported"
                ),
                "broker_tools_available_count": report.get(
                    "broker_tools_available_count"
                ),
                "available_tool_names": report.get("available_tool_names") or [],
                "functionalities": report.get("functionalities") or [],
                "replight_passed": report.get("replight_passed"),
                "replight_blocked_reason": report.get("replight_blocked_reason"),
            }
        )
    return reports
