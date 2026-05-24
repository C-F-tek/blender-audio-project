"""Absorb completed provider lane reports into the same heap graph."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    append_unique,
    now_iso,
    provider_heap_lane,
    read_json,
    repo_rel,
    subprocess,
    terminate_process_tree,
    write_json_report,
)


def absorb_completed_provider_item(
    gate: Any,
    item: dict[str, Any],
    *,
    launch_manifest: Path,
    work_dir: Path,
    round_id: int,
    revision: int,
    timeout_seconds: int,
) -> bool:
    if item.get("absorbed"):
        return False
    spec = item["spec"]
    lane = str(item["lane"])
    requirement = str(item["requirement"])
    correlation = str(item["correlation"])
    command = list(item["command"])
    completed = _completed_process(item, command, timeout_seconds)
    report_data = read_json(Path(spec["output"]))
    provider_report = gate.summarize_provider_report(spec, completed, report_data)
    provider_report["started_at"] = item.get("started_at")
    provider_report["completed_at"] = item.get("completed_at")
    provider_report["elapsed_seconds"] = item.get("elapsed_seconds")
    provider_report["provider_process_id"] = item.get("pid")
    provider_report["budget_counter_seconds"] = item.get("budget_counter_seconds")
    provider_report["soft_close_after_seconds"] = item.get("soft_close_after_seconds")
    provider_report["watchdog_timeout_seconds"] = item.get("watchdog_timeout_seconds")
    provider_report["closure_owner"] = item.get("closure_owner")
    provider_report["lane_is_closure_owner"] = item.get("lane_is_closure_owner")
    provider_report["lane_tier"] = item.get("lane_tier")
    provider_report["authority"] = item.get("authority")
    provider_report["peer_only"] = item.get("peer_only")
    provider_report["context_budget"] = item.get("context_budget")
    provider_report["primary_closer"] = item.get("primary_closer")
    provider_report["sidecar_lane"] = item.get("sidecar_lane")
    provider_report["micro_audit_only"] = item.get("micro_audit_only")
    provider_report["reviewer_refiner"] = item.get("reviewer_refiner")
    provider_report["native_tool_calling_policy"] = item.get("native_tool_calling_policy")
    provider_report["delta_context_mode"] = item.get("delta_context_mode")
    provider_report["npu_micro_timeout_enforced"] = item.get("npu_micro_timeout_enforced")
    provider_report["time_counter_contract"] = item.get("time_counter_contract")
    provider_report["sidecar_scope_mode"] = (
        item.get("sidecar_scope_mode")
        or ("packet_review_only" if lane in {"gpu0_peer", "npu_micro_task_auditor"} else "")
    )
    provider_report["sidecar_scope_contract"] = item.get("sidecar_scope_contract") or ""
    for key in (
        "provider_backend",
        "provider_compute_device",
        "provider_device_verified",
        "logical_lane",
        "provider_backend_device_id",
        "windows_task_manager_device_hint",
        "vulkan_visible_device",
        "vulkan_device_name",
        "vulkan_vendor_id",
        "device_identity_verified",
        "cpu_provider_fallback_performed",
        "ollama_gpu_layers_requested",
        "ollama_cpu_percent",
        "ollama_gpu_percent",
        "ollama_full_gpu_requested",
        "ollama_full_gpu_verified",
        "ollama_gpu_residency_status",
        "ollama_compute_verified",
        "ollama_vulkan_required",
        "product_blocked_reason",
        "provider_work_verified",
        "provider_rejection_reason",
        "provider_replight_required",
        "provider_id",
        "provider_role",
        "provider_model",
        "provider_loaded",
        "generated_phrase",
        "prompt_token_count",
        "completion_token_count",
        "token_metric_source",
        "tokens_per_second",
        "native_tool_calling_supported",
        "broker_tools_available_count",
        "available_tool_names",
        "functionalities",
        "replight_passed",
        "replight_blocked_reason",
        "gpu0_secondary_schema_valid",
        "gpu0_role",
        "gpu0_decision",
        "gpu0_model_decision",
        "gpu0_effective_decision",
        "role_decision",
        "checked_block_id",
        "checked_gpu1_revision",
        "expected_gpu1_block_id",
        "expected_gpu1_revision",
        "expected_packet_fingerprint",
        "reviewed_gpu1_block_id",
        "reviewed_revision",
        "review_target_pointer",
        "reviewed_packet_fingerprint",
        "gpu0_checked_current_packet",
        "gpu0_review_invalid_requires_gpu1_retry",
        "gpu0_unanchored_reasons",
        "gpu0_decision_override_reason",
        "gpu1_closure_decision_packet",
        "gpu1_closure_decision_packet_present",
        "gpu1_closure_decision_packet_valid",
        "gpu1_closure_decision_packet_fingerprint",
        "gpu0_prompt_scope",
        "gpu0_one_execution_per_packet",
        "missing_required_sections",
        "incongruence_reasons",
        "veto_reasons",
        "required_gpu1_next_action",
        "free_text_evidence",
        "free_text_used_as_product",
        "free_text_used_as_decision",
        "gpu0_raw_response_text",
        "gpu0_server_evidence_source",
        "sidecar_scope_mode",
        "sidecar_scope_contract",
        "sidecar_invalid",
        "sidecar_incongruent",
        "sidecar_product_block_reason",
        "sidecar_recoverable_failure_reason",
        "sidecar_skipped",
        "sidecar_skipped_reason",
    ):
        if key in report_data:
            provider_report[key] = report_data.get(key)
    provider_report["launch_manifest"] = repo_rel(gate.repo_root, launch_manifest)
    provider_report["leader_packet"] = gate.provider_leader_packet_path
    provider_report = gate.enrich_provider_report_with_operational_peer_review(
        provider_report,
        lane,
        work_dir,
        revision,
        gate.read_events(),
    )
    provider_report.update(gate.provider_block_contract(lane, revision, provider_report))
    provider_report["execution_mode"] = "provider_teamwork_unified_parallel"
    provider_report["revision"] = revision
    provider_report["provider_cycle_id"] = revision
    provider_report["revision_semantics"] = (
        "provider_cycle_id_shared_by_lanes_not_peer_ownership"
    )
    provider_report["revision_owner_lane"] = "gpu1_planner"
    provider_report["gpu1_revision_owner"] = bool(
        lane == "gpu1_planner"
        and provider_report.get("passed") is True
        and (
            provider_report.get("provider_work_verified")
            or provider_report.get("gpu1_primary_workload_valid")
            or provider_report.get("semantic_provider_execution_performed")
        )
    )
    provider_report["cannot_open_revision"] = lane != "gpu1_planner"
    provider_report["final_source_allowed"] = lane == "gpu1_planner"
    if lane == "gpu0_peer":
        provider_report["review_for_gpu1_cycle"] = revision
        provider_report["peer_attempt_id"] = provider_report.get("provider_block_id")
        provider_report["final_source_allowed"] = False
        provider_report["cannot_open_revision"] = True
        provider_report["sidecar_target_pointer"] = (
            provider_report.get("review_target_pointer")
            or provider_report.get("reviewed_gpu1_block_id")
            or provider_report.get("checked_block_id")
            or provider_report.get("expected_gpu1_block_id")
            or ""
        )
        if provider_report.get("sidecar_skipped"):
            provider_report["sidecar_incongruent"] = False
            provider_report["sidecar_invalid"] = False
        else:
            provider_report["sidecar_incongruent"] = (
                str(
                    provider_report.get("gpu0_effective_decision")
                    or provider_report.get("gpu0_decision")
                    or ""
                ).strip().lower()
                == "incongruent"
            )
            provider_report["sidecar_invalid"] = bool(
                provider_report.get("gpu0_secondary_schema_valid") is not True
                or provider_report.get("provider_rejection_reason")
                or provider_report.get("product_blocked_reason")
            )
    elif lane == "npu_micro_task_auditor":
        provider_report["audit_for_gpu1_cycle"] = revision
        provider_report["peer_attempt_id"] = provider_report.get("provider_block_id")
        provider_report["npu_lane_contract"] = "microtask_tool_calling_openvino"
        provider_report["npu_decision_authority"] = "non_closer"
        npu_audit = (
            provider_report.get("npu_operational_audit")
            if isinstance(provider_report.get("npu_operational_audit"), dict)
            else {}
        )
        provider_report["sidecar_target_pointer"] = (
            provider_report.get("refines_block_id")
            or provider_report.get("resume_from_block_id")
            or ""
        )
        provider_report["sidecar_incongruent"] = False
        provider_report["sidecar_invalid"] = bool(
            not provider_report.get("sidecar_skipped")
            and (
                provider_report.get("provider_rejection_reason")
                or provider_report.get("product_blocked_reason")
                or provider_report.get("provider_work_verified") is False
                or str(npu_audit.get("decision") or "").lower().startswith("reject")
            )
        )
    if lane in {"gpu0_peer", "npu_micro_task_auditor"}:
        provider_report["sidecar_recoverable_failure_reason"] = (
            ""
            if provider_report.get("sidecar_skipped")
            else _sidecar_failure_reason(lane, provider_report)
        )
    provider_report["report_passed"] = bool(provider_report.get("passed"))
    provider_report["diagnostic_only"] = not bool(
        provider_report.get("operational_provider_activity")
    )
    rejection_reason = str(
        provider_report.get("provider_rejection_reason")
        or provider_report.get("product_blocked_reason")
        or ""
    ).strip()
    work_ready = bool(
        completed.returncode == 0
        and provider_report.get("passed") is True
        and provider_report.get("provider_work_verified") is True
        and not rejection_reason
    )
    provider_report["process_status"] = "completed" if completed.returncode == 0 else "failed"
    provider_report["work_status"] = (
        "ready" if work_ready else "rejected" if rejection_reason else "unverified"
    )
    provider_report["status"] = provider_report["work_status"]
    normalized_output = dict(report_data) if isinstance(report_data, dict) else {}
    normalized_output.update(provider_report)
    write_json_report(normalized_output, Path(spec["output"]))
    item["provider_report"] = provider_report
    gate.provider_reports.append(provider_report)
    append_unique(gate.state["provider_results"], provider_report, key="requirement")
    _publish_provider_report(gate, lane, requirement, correlation, provider_report, round_id, revision)
    item["absorbed"] = True
    return True


def _completed_process(
    item: dict[str, Any],
    command: list[str],
    timeout_seconds: int,
) -> subprocess.CompletedProcess[str]:
    completed = item.get("completed")
    process = item.get("process")
    if completed is not None:
        return completed
    if process is not None:
        try:
            watchdog = float(
                item.get("watchdog_timeout_seconds")
                or item.get("timeout_seconds")
                or timeout_seconds
            )
            stdout, stderr = process.communicate(timeout=None if watchdog <= 0 else watchdog)
            item["completed_at"] = now_iso()
            completed = subprocess.CompletedProcess(command, process.returncode, stdout or "", stderr or "")
        except subprocess.TimeoutExpired:
            terminate_process_tree(process)
            stdout, stderr = process.communicate()
            item["completed_at"] = now_iso()
            completed = subprocess.CompletedProcess(
                command, 124, stdout or "", (stderr or "") + "\nprovider watchdog timeout"
            )
    if completed is None:
        completed = subprocess.CompletedProcess(
            command,
            127,
            "",
            "provider process was not started and no completed process was recorded",
        )
    item["completed"] = completed
    return completed


def _publish_provider_report(
    gate: Any,
    lane: str,
    requirement: str,
    correlation: str,
    provider_report: dict[str, Any],
    round_id: int,
    revision: int,
) -> None:
    gate.publish(
        provider_heap_lane(lane),
        "provider_evidence",
        provider_report,
        target="orchestrator",
        correlation_id=correlation,
        round_id=round_id,
    )
    if provider_report.get("operational_provider_activity"):
        gate.publish(
            provider_heap_lane(lane),
            "provider_peer_block",
            _provider_peer_block_payload(lane, revision, provider_report),
            target="orchestrator",
            correlation_id=f"{correlation}:block",
            round_id=round_id,
        )
    gate.append_heap_exchange_event(
        {
            "kind": "provider_output",
            "lane": lane,
            "round": round_id,
            "requirement": requirement,
            "revision": revision,
            "provider_cycle_id": provider_report.get("provider_cycle_id"),
            "revision_owner_lane": provider_report.get("revision_owner_lane"),
            "gpu1_revision_owner": provider_report.get("gpu1_revision_owner"),
            "review_for_gpu1_cycle": provider_report.get("review_for_gpu1_cycle"),
            "audit_for_gpu1_cycle": provider_report.get("audit_for_gpu1_cycle"),
            "cannot_open_revision": provider_report.get("cannot_open_revision"),
            "final_source_allowed": provider_report.get("final_source_allowed"),
            "execution_mode": "provider_teamwork_unified_parallel",
            "started_at": provider_report.get("started_at"),
            "completed_at": provider_report.get("completed_at"),
            "elapsed_seconds": provider_report.get("elapsed_seconds"),
            "budget_counter_seconds": provider_report.get("budget_counter_seconds"),
            "soft_close_after_seconds": provider_report.get("soft_close_after_seconds"),
            "watchdog_timeout_seconds": provider_report.get("watchdog_timeout_seconds"),
            "closure_owner": provider_report.get("closure_owner"),
            "lane_is_closure_owner": provider_report.get("lane_is_closure_owner"),
            "lane_tier": provider_report.get("lane_tier"),
            "authority": provider_report.get("authority"),
            "peer_only": provider_report.get("peer_only"),
            "context_budget": provider_report.get("context_budget"),
            "sidecar_lane": provider_report.get("sidecar_lane"),
            "micro_audit_only": provider_report.get("micro_audit_only"),
            "sidecar_scope_mode": provider_report.get("sidecar_scope_mode"),
            "sidecar_invalid": provider_report.get("sidecar_invalid"),
            "sidecar_incongruent": provider_report.get("sidecar_incongruent"),
            "sidecar_recoverable_failure_reason": provider_report.get(
                "sidecar_recoverable_failure_reason"
            ),
            "sidecar_target_pointer": provider_report.get("sidecar_target_pointer"),
            "native_tool_calling_policy": provider_report.get("native_tool_calling_policy"),
            "delta_context_mode": provider_report.get("delta_context_mode"),
            "provider_process_id": provider_report.get("provider_process_id"),
            "provider_backend": provider_report.get("provider_backend"),
            "provider_compute_device": provider_report.get("provider_compute_device"),
            "provider_device_verified": provider_report.get("provider_device_verified"),
            "logical_lane": provider_report.get("logical_lane"),
            "provider_backend_device_id": provider_report.get("provider_backend_device_id"),
            "windows_task_manager_device_hint": provider_report.get(
                "windows_task_manager_device_hint"
            ),
            "vulkan_visible_device": provider_report.get("vulkan_visible_device"),
            "vulkan_device_name": provider_report.get("vulkan_device_name"),
            "vulkan_vendor_id": provider_report.get("vulkan_vendor_id"),
            "device_identity_verified": provider_report.get("device_identity_verified"),
            "cpu_provider_fallback_performed": provider_report.get(
                "cpu_provider_fallback_performed"
            ),
            "provider_block_id": provider_report.get("provider_block_id"),
            "proposal_block_id": provider_report.get("proposal_block_id"),
            "block_type": provider_report.get("block_type"),
            "passed": provider_report.get("passed"),
            "operational_provider_activity": provider_report.get("operational_provider_activity"),
            "provider_activity_classification": provider_report.get("provider_activity_classification"),
            "provider_replight_required": provider_report.get("provider_replight_required"),
            "provider_id": provider_report.get("provider_id"),
            "provider_role": provider_report.get("provider_role"),
            "provider_model": provider_report.get("provider_model"),
            "provider_loaded": provider_report.get("provider_loaded"),
            "generated_phrase": provider_report.get("generated_phrase"),
            "prompt_token_count": provider_report.get("prompt_token_count"),
            "completion_token_count": provider_report.get("completion_token_count"),
            "tokens_per_second": provider_report.get("tokens_per_second"),
            "native_tool_calling_supported": provider_report.get(
                "native_tool_calling_supported"
            ),
            "broker_tools_available_count": provider_report.get(
                "broker_tools_available_count"
            ),
            "available_tool_names": provider_report.get("available_tool_names") or [],
            "functionalities": provider_report.get("functionalities") or [],
            "replight_passed": provider_report.get("replight_passed"),
            "replight_blocked_reason": provider_report.get("replight_blocked_reason"),
            "gpu0_secondary_schema_valid": provider_report.get("gpu0_secondary_schema_valid"),
            "gpu0_decision": provider_report.get("gpu0_decision"),
            "gpu0_model_decision": provider_report.get("gpu0_model_decision"),
            "gpu0_effective_decision": provider_report.get("gpu0_effective_decision"),
            "role_decision": provider_report.get("role_decision"),
            "checked_block_id": provider_report.get("checked_block_id"),
            "checked_gpu1_revision": provider_report.get("checked_gpu1_revision"),
            "expected_gpu1_block_id": provider_report.get("expected_gpu1_block_id"),
            "expected_gpu1_revision": provider_report.get("expected_gpu1_revision"),
            "gpu0_checked_current_packet": provider_report.get("gpu0_checked_current_packet"),
            "gpu0_unanchored_reasons": provider_report.get("gpu0_unanchored_reasons") or [],
            "gpu0_decision_override_reason": provider_report.get("gpu0_decision_override_reason"),
            "gpu1_closure_decision_packet_valid": provider_report.get(
                "gpu1_closure_decision_packet_valid"
            ),
            "gpu1_closure_decision_packet_fingerprint": provider_report.get(
                "gpu1_closure_decision_packet_fingerprint"
            ),
            "gpu0_prompt_scope": provider_report.get("gpu0_prompt_scope"),
            "veto_reasons": provider_report.get("veto_reasons") or [],
            "incongruence_reasons": provider_report.get("incongruence_reasons") or [],
            "npu_lane_contract": provider_report.get("npu_lane_contract"),
            "npu_decision_authority": provider_report.get("npu_decision_authority"),
            "source_file": provider_report.get("output"),
            "summary": str(provider_report.get("response_text") or "")[:500],
        }
    )
    _publish_claim(gate, lane, requirement, correlation, provider_report, round_id)


def _provider_peer_block_payload(
    lane: str,
    revision: int,
    provider_report: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "kind": "provider_peer_block",
        "lane": lane,
        "revision": revision,
        "provider_cycle_id": provider_report.get("provider_cycle_id"),
        "revision_owner_lane": provider_report.get("revision_owner_lane"),
        "gpu1_revision_owner": provider_report.get("gpu1_revision_owner"),
        "review_for_gpu1_cycle": provider_report.get("review_for_gpu1_cycle"),
        "audit_for_gpu1_cycle": provider_report.get("audit_for_gpu1_cycle"),
        "cannot_open_revision": provider_report.get("cannot_open_revision"),
        "final_source_allowed": provider_report.get("final_source_allowed"),
        "provider_block_id": provider_report.get("provider_block_id"),
        "proposal_block_id": provider_report.get("proposal_block_id"),
        "role": provider_report.get("role"),
        "block_type": provider_report.get("block_type"),
        "pointer_action": provider_report.get("pointer_action"),
        "refines_block_id": provider_report.get("refines_block_id"),
        "resume_from_block_id": provider_report.get("resume_from_block_id"),
        "target_files": provider_report.get("target_files") or [],
        "decision": provider_report.get("decision"),
        "provider_report": provider_report.get("output"),
        "native_tool_call_count": provider_report.get("native_tool_call_count"),
        "provider_backend": provider_report.get("provider_backend"),
        "provider_compute_device": provider_report.get("provider_compute_device"),
        "provider_device_verified": provider_report.get("provider_device_verified"),
        "logical_lane": provider_report.get("logical_lane"),
        "provider_backend_device_id": provider_report.get("provider_backend_device_id"),
        "windows_task_manager_device_hint": provider_report.get(
            "windows_task_manager_device_hint"
        ),
        "vulkan_visible_device": provider_report.get("vulkan_visible_device"),
        "vulkan_device_name": provider_report.get("vulkan_device_name"),
        "vulkan_vendor_id": provider_report.get("vulkan_vendor_id"),
        "device_identity_verified": provider_report.get("device_identity_verified"),
        "cpu_provider_fallback_performed": provider_report.get(
            "cpu_provider_fallback_performed"
        ),
        "provider_replight_required": provider_report.get("provider_replight_required"),
        "provider_model": provider_report.get("provider_model"),
        "provider_loaded": provider_report.get("provider_loaded"),
        "lane_tier": provider_report.get("lane_tier"),
        "authority": provider_report.get("authority"),
        "closure_owner": provider_report.get("closure_owner"),
        "context_budget": provider_report.get("context_budget"),
        "generated_phrase": provider_report.get("generated_phrase"),
        "prompt_token_count": provider_report.get("prompt_token_count"),
        "completion_token_count": provider_report.get("completion_token_count"),
        "tokens_per_second": provider_report.get("tokens_per_second"),
        "broker_tools_available_count": provider_report.get("broker_tools_available_count"),
        "functionalities": provider_report.get("functionalities") or [],
        "replight_passed": provider_report.get("replight_passed"),
        "replight_blocked_reason": provider_report.get("replight_blocked_reason"),
        "operational_provider_activity": provider_report.get("operational_provider_activity"),
        "gpu0_secondary_schema_valid": provider_report.get("gpu0_secondary_schema_valid"),
        "gpu0_decision": provider_report.get("gpu0_decision"),
        "gpu0_model_decision": provider_report.get("gpu0_model_decision"),
        "gpu0_effective_decision": provider_report.get("gpu0_effective_decision"),
        "role_decision": provider_report.get("role_decision"),
        "checked_block_id": provider_report.get("checked_block_id"),
        "checked_gpu1_revision": provider_report.get("checked_gpu1_revision"),
        "expected_gpu1_block_id": provider_report.get("expected_gpu1_block_id"),
        "expected_gpu1_revision": provider_report.get("expected_gpu1_revision"),
        "expected_packet_fingerprint": provider_report.get("expected_packet_fingerprint"),
        "reviewed_gpu1_block_id": provider_report.get("reviewed_gpu1_block_id"),
        "reviewed_revision": provider_report.get("reviewed_revision"),
        "review_target_pointer": provider_report.get("review_target_pointer"),
        "reviewed_packet_fingerprint": provider_report.get("reviewed_packet_fingerprint"),
        "gpu0_checked_current_packet": provider_report.get("gpu0_checked_current_packet"),
        "gpu0_review_invalid_requires_gpu1_retry": provider_report.get(
            "gpu0_review_invalid_requires_gpu1_retry"
        ),
        "gpu0_unanchored_reasons": provider_report.get("gpu0_unanchored_reasons") or [],
        "gpu0_decision_override_reason": provider_report.get("gpu0_decision_override_reason"),
        "gpu1_closure_decision_packet": provider_report.get("gpu1_closure_decision_packet"),
        "gpu1_closure_decision_packet_valid": provider_report.get(
            "gpu1_closure_decision_packet_valid"
        ),
        "gpu1_closure_decision_packet_fingerprint": provider_report.get(
            "gpu1_closure_decision_packet_fingerprint"
        ),
        "gpu0_prompt_scope": provider_report.get("gpu0_prompt_scope"),
        "veto_reasons": provider_report.get("veto_reasons") or [],
        "incongruence_reasons": provider_report.get("incongruence_reasons") or [],
        "npu_lane_contract": provider_report.get("npu_lane_contract"),
        "npu_decision_authority": provider_report.get("npu_decision_authority"),
        "sidecar_scope_mode": provider_report.get("sidecar_scope_mode"),
        "sidecar_invalid": provider_report.get("sidecar_invalid"),
        "sidecar_incongruent": provider_report.get("sidecar_incongruent"),
        "sidecar_recoverable_failure_reason": provider_report.get(
            "sidecar_recoverable_failure_reason"
        ),
        "sidecar_target_pointer": provider_report.get("sidecar_target_pointer"),
    }
    if lane == "npu_micro_task_auditor":
        payload["npu_micro_provider_execution_performed"] = provider_report.get(
            "npu_micro_provider_execution_performed"
        )
    else:
        payload["semantic_provider_execution_performed"] = provider_report.get(
            "semantic_provider_execution_performed"
        )
    return payload


def _sidecar_failure_reason(lane: str, provider_report: dict[str, Any]) -> str:
    if lane == "gpu0_peer":
        if provider_report.get("sidecar_incongruent"):
            return "sidecar_incongruent:gpu0_peer"
        if provider_report.get("sidecar_invalid"):
            return str(
                provider_report.get("provider_rejection_reason")
                or provider_report.get("product_blocked_reason")
                or "sidecar_invalid:gpu0_peer"
            )
    if lane == "npu_micro_task_auditor" and provider_report.get("sidecar_invalid"):
        return str(
            provider_report.get("provider_rejection_reason")
            or provider_report.get("product_blocked_reason")
            or "sidecar_invalid:npu_micro_task_auditor"
        )
    return ""


def _publish_claim(
    gate: Any,
    lane: str,
    requirement: str,
    correlation: str,
    provider_report: dict[str, Any],
    round_id: int,
) -> None:
    operational = bool(provider_report.get("operational_provider_activity"))
    observed_request_evidence = gate.request_input_ref_or_tail()
    observed_response_evidence = gate.response_text_ref_or_tail(
        str(provider_report.get("response_text") or gate.response_text() or ""),
        name=f"observed_response_{lane}",
        kind="provider_claim_observed_response",
        producer=lane,
    )
    claim = {
        "id": f"{requirement}_claim",
        "from": lane,
        "claim": (
            "provider lane contributed operational heap evidence"
            if operational
            else "provider lane produced non-operational evidence only"
        ),
        "confidence": 0.88 if operational else 0.2,
        "requirement": requirement,
        "evidence_ref": provider_report.get("output"),
        "provider_execution_performed": provider_report.get("provider_execution_performed"),
        "provider_backend": provider_report.get("provider_backend"),
        "provider_compute_device": provider_report.get("provider_compute_device"),
        "provider_device_verified": provider_report.get("provider_device_verified"),
        "logical_lane": provider_report.get("logical_lane"),
        "provider_backend_device_id": provider_report.get("provider_backend_device_id"),
        "windows_task_manager_device_hint": provider_report.get(
            "windows_task_manager_device_hint"
        ),
        "vulkan_visible_device": provider_report.get("vulkan_visible_device"),
        "vulkan_device_name": provider_report.get("vulkan_device_name"),
        "vulkan_vendor_id": provider_report.get("vulkan_vendor_id"),
        "device_identity_verified": provider_report.get("device_identity_verified"),
        "cpu_provider_fallback_performed": provider_report.get(
            "cpu_provider_fallback_performed"
        ),
        "operational_provider_activity": operational,
        "provider_activity_classification": provider_report.get("provider_activity_classification"),
        "provider_replight_required": provider_report.get("provider_replight_required"),
        "provider_model": provider_report.get("provider_model"),
        "provider_loaded": provider_report.get("provider_loaded"),
        "generated_phrase": provider_report.get("generated_phrase"),
        "prompt_token_count": provider_report.get("prompt_token_count"),
        "completion_token_count": provider_report.get("completion_token_count"),
        "tokens_per_second": provider_report.get("tokens_per_second"),
        "native_tool_calling_supported": provider_report.get(
            "native_tool_calling_supported"
        ),
        "broker_tools_available_count": provider_report.get("broker_tools_available_count"),
        "functionalities": provider_report.get("functionalities") or [],
        "replight_passed": provider_report.get("replight_passed"),
        "replight_blocked_reason": provider_report.get("replight_blocked_reason"),
        "gpu1_closure_decision_packet_fingerprint": provider_report.get(
            "gpu1_closure_decision_packet_fingerprint"
        ),
        "gpu0_prompt_scope": provider_report.get("gpu0_prompt_scope"),
        "sidecar_scope_mode": provider_report.get("sidecar_scope_mode"),
        "sidecar_invalid": provider_report.get("sidecar_invalid"),
        "sidecar_incongruent": provider_report.get("sidecar_incongruent"),
        "sidecar_recoverable_failure_reason": provider_report.get(
            "sidecar_recoverable_failure_reason"
        ),
        "sidecar_target_pointer": provider_report.get("sidecar_target_pointer"),
        "leader_packet": provider_report.get("leader_packet"),
        **gate.prefixed_text_evidence_fields(
            "observed_request", observed_request_evidence
        ),
        **gate.prefixed_text_evidence_fields(
            "observed_response", observed_response_evidence
        ),
        "execution_mode": "provider_teamwork_unified_parallel",
    }
    if lane == "npu_micro_task_auditor":
        claim["npu_micro_provider_execution_performed"] = provider_report.get(
            "npu_micro_provider_execution_performed"
        )
    else:
        claim["semantic_provider_execution_performed"] = provider_report.get(
            "semantic_provider_execution_performed"
        )
    append_unique(gate.state["claims"], claim)
    gate.publish(
        provider_heap_lane(lane),
        "claim",
        claim,
        target="deterministic",
        correlation_id=f"{correlation}:claim",
        round_id=round_id,
    )
