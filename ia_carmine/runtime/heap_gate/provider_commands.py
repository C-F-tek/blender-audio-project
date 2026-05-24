from __future__ import annotations
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, repo_rel, subprocess
from ia_carmine.runtime.heap_gate.provider_command_specs import build_provider_command_specs
from ia_carmine.runtime.heap_gate.provider_time import build_provider_time_counter_contract
from ia_carmine._shared.provider_tool_schemas import is_api_native_tool_call
from ia_carmine._shared.provider_work_verification import provider_work_status
def _empty_report_value(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}
class RuntimeGateProviderCommandsMixin:
    def provider_time_counter_contract(self) -> dict[str, Any]:
        return build_provider_time_counter_contract(self.args)
    def provider_command_specs(self, work_dir: Path, revision: int = 0, selected_lanes: set[str] | None = None) -> list[dict[str, Any]]:
        return build_provider_command_specs(self, work_dir, revision, selected_lanes)
    def summarize_provider_report(
        self,
        spec: dict[str, Any],
        completed: subprocess.CompletedProcess[str],
        report_data: dict[str, Any],
    ) -> dict[str, Any]:
        lane = str(spec["lane"])
        tool_calls: list[dict[str, Any]] = []
        textual_tool_calls: list[dict[str, Any]] = []
        rejected_non_native_tool_calls: list[dict[str, Any]] = []
        native_tool_loop_requested = bool(report_data.get("native_tool_loop_requested"))
        native_tool_loop_supported = bool(report_data.get("native_tool_loop_supported"))
        native_tool_loop_performed = bool(report_data.get("native_tool_loop_performed"))
        def absorb_tool_loop(payload: dict[str, Any]) -> None:
            nonlocal native_tool_loop_requested
            nonlocal native_tool_loop_supported
            nonlocal native_tool_loop_performed
            native_tool_loop_requested = native_tool_loop_requested or bool(
                payload.get("native_tool_loop_requested")
            )
            native_tool_loop_supported = native_tool_loop_supported or bool(
                payload.get("native_tool_loop_supported")
            )
            native_tool_loop_performed = native_tool_loop_performed or bool(
                payload.get("native_tool_loop_performed")
            )
            calls = payload.get("tool_calls") if isinstance(payload.get("tool_calls"), list) else []
            for call in calls:
                if isinstance(call, dict):
                    if is_api_native_tool_call(call, lane=lane):
                        tool_calls.append(call)
                    else:
                        rejected_non_native_tool_calls.append(
                            {
                                **call,
                                "rejection_reason": "provider_textual_tool_call_not_executable",
                            }
                        )
            text_calls = (
                payload.get("textual_tool_calls")
                if isinstance(payload.get("textual_tool_calls"), list)
                else []
            )
            for call in text_calls:
                if isinstance(call, dict):
                    textual_tool_calls.append(call)
        absorb_tool_loop(report_data)
        backend = str(report_data.get("provider_backend") or "").strip().lower()
        compute_device = str(report_data.get("provider_compute_device") or "")
        provider_execution_attempted = bool(
            report_data.get("provider_execution_performed")
            or report_data.get("provider_execution_attempted")
            or report_data.get("provider_io_observed")
            or (
                lane == "gpu0_peer"
                and backend == "ollama"
                and "gpu0-vulkan" in compute_device
                and report_data.get("provider_work_verified")
            )
            or (
                lane == "npu_micro_task_auditor"
                and (
                    report_data.get("npu_peer_evidence_verified")
                    or report_data.get("npu_provider_execution_performed")
                    or report_data.get("npu_device_workload_performed")
                )
            )
        )
        provider_execution = False
        device_workload_execution = bool(
            report_data.get("device_workload_execution_performed")
            or (
                lane == "npu_micro_task_auditor"
                and report_data.get("npu_device_workload_performed")
            )
        )
        semantic_provider_execution = bool(
            lane != "npu_micro_task_auditor"
            and report_data.get("semantic_provider_execution_performed")
        )
        npu_micro_provider_execution = bool(
            lane == "npu_micro_task_auditor"
            and report_data.get("npu_micro_provider_execution_performed")
        )
        errors = report_data.get("errors") if isinstance(report_data.get("errors"), list) else []
        warnings = (
            report_data.get("warnings") if isinstance(report_data.get("warnings"), list) else []
        )
        standalone_default_fields = (
            report_data.get("standalone_default_fields")
            if isinstance(report_data.get("standalone_default_fields"), list)
            else []
        )
        canonical_provider_evidence = bool(
            report_data.get("canonical_run_provider_evidence")
            and str(report_data.get("canonical_run_fingerprint") or "").strip()
            == str(getattr(self.args, "canonical_run_fingerprint", "") or "").strip()
        )
        if standalone_default_fields and not canonical_provider_evidence:
            reason = (
                "standalone_default_config_not_accepted_as_full_run_provider_evidence:"
                + ",".join(str(item) for item in standalone_default_fields)
            )
            errors.append(reason)
            report_data["errors"] = errors
            report_data["provider_work_verified"] = False
            report_data["provider_role_counted"] = False
            report_data["provider_rejection_reason"] = reason
        elif standalone_default_fields and canonical_provider_evidence:
            report_data["standalone_default_fields_ignored_reason"] = (
                "canonical_run_provider_evidence_fingerprint_verified"
            )
        response_text = self.provider_report_response_text(report_data).strip()
        selected_model = str(report_data.get("selected_model") or "").strip()
        lane_reports = report_data.get("lane_reports")
        if isinstance(lane_reports, list):
            for lane_report in lane_reports:
                if isinstance(lane_report, dict):
                    absorb_tool_loop(lane_report)
                lane_report_lane = str(
                    lane_report.get("lane") or lane_report.get("provider_id") or ""
                ) if isinstance(lane_report, dict) else ""
                if isinstance(lane_report, dict) and lane_report_lane in {"ollama", lane}:
                    selected_model = str(
                        lane_report.get("selected_model")
                        or lane_report.get("model")
                        or selected_model
                    ).strip()
                    response_text = (
                        self.provider_report_response_text(lane_report).strip()
                        or str(lane_report.get("text_preview") or response_text).strip()
                    )
                    if not report_data.get("target_files") and lane_report.get("target_files"):
                        report_data["target_files"] = lane_report.get("target_files")
                    if (
                        not report_data.get("validation_commands")
                        and lane_report.get("validation_commands")
                    ):
                        report_data["validation_commands"] = lane_report.get(
                            "validation_commands"
                        )
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
                        "provider_execution_performed",
                        "provider_execution_attempted",
                        "provider_io_observed",
                        "cpu_provider_fallback_performed",
                        "provider_replight_required",
                        "provider_id",
                        "provider_role",
                        "lane_tier",
                        "authority",
                        "closure_owner",
                        "context_budget",
                        "provider_model",
                        "provider_loaded",
                        "generated_phrase",
                        "prompt_token_count",
                        "completion_token_count",
                        "token_metric_source",
                        "tokens_per_second",
                        "native_tool_calling_supported",
                        "provider_native_tool_call_required",
                        "provider_native_tool_api_attempted",
                        "provider_native_tool_api_completed",
                        "provider_native_tool_api_adapter_available",
                        "provider_native_tool_api_supported",
                        "provider_native_tool_api_error",
                        "provider_native_tool_api_attempt_error",
                        "provider_native_tool_api_unavailable",
                        "provider_native_tool_api_attempt_failed",
                        "provider_native_tool_call_required_unmet",
                        "broker_tools_available_count",
                        "available_tool_names",
                        "functionalities",
                        "replight_passed",
                        "replight_blocked_reason",
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
                        "response_text_ref",
                        "response_text_chars",
                        "response_text_sha256",
                        "response_text_tail",
                        "response_text_tail_chars",
                        "response_text_full_text_in_json",
                        "response_text_transport",
                        "raw_response_chars",
                        "heap_delta_text_present",
                        "heap_delta_text_required",
                        "provider_output_complete",
                        "response_likely_incomplete",
                        "prompt_attempts",
                        "eval_count",
                        "prompt_eval_count",
                    ):
                        if key in lane_report and _empty_report_value(report_data.get(key)):
                            report_data[key] = lane_report.get(key)
                    if response_text:
                        break
        provider_execution_attempted = bool(
            provider_execution_attempted
            or report_data.get("provider_execution_attempted")
            or report_data.get("provider_io_observed")
            or report_data.get("provider_execution_performed")
        )
        provider_execution_claim_seen = provider_execution_attempted
        if (textual_tool_calls or rejected_non_native_tool_calls) and not tool_calls:
            reason = "provider_textual_tool_call_not_executable"
            errors.append(reason)
            report_data["errors"] = errors
            report_data["provider_rejection_reason"] = reason
            report_data["provider_work_verified"] = False
            report_data["provider_role_counted"] = False
        elif report_data.get("provider_native_tool_api_unavailable"):
            reason = (
                str(report_data.get("provider_rejection_reason") or "").strip()
                or "provider_native_tool_api_unavailable"
            )
            errors.append(reason)
            report_data["errors"] = errors
            report_data["provider_rejection_reason"] = reason
            report_data["provider_work_verified"] = False
            report_data["provider_role_counted"] = False
        elif report_data.get("provider_native_tool_api_attempt_failed"):
            reason = (
                str(report_data.get("provider_rejection_reason") or "").strip()
                or "provider_native_tool_api_attempt_failed"
            )
            errors.append(reason)
            report_data["errors"] = errors
            report_data["provider_rejection_reason"] = reason
            report_data["provider_work_verified"] = False
            report_data["provider_role_counted"] = False
        elif report_data.get("provider_native_tool_call_required_unmet"):
            reason = (
                str(report_data.get("provider_rejection_reason") or "").strip()
                or "provider_native_tool_call_required_unmet"
            )
            errors.append(reason)
            report_data["errors"] = errors
            report_data["provider_rejection_reason"] = reason
            report_data["provider_work_verified"] = False
            report_data["provider_role_counted"] = False
        verified_status = provider_work_status(
            lane=lane,
            report=report_data,
            default_role=str(spec.get("provider_role") or spec.get("role") or ""),
        )
        provider_execution = bool(verified_status.get("provider_work_verified"))
        report_data["provider_work_verified"] = provider_execution
        report_data["provider_rejection_reason"] = verified_status.get(
            "provider_rejection_reason"
        )
        report_data["provider_stage"] = verified_status.get("provider_stage")
        report_data["provider_execution_claim_seen"] = provider_execution_claim_seen
        if lane == "gpu1_planner" and provider_execution:
            self.provider_execution_performed = True
        summary = {
            "lane": lane,
            "role": spec.get("role"),
            "requirement": spec.get("requirement"),
            "output": repo_rel(self.repo_root, Path(spec["output"])),
            "returncode": completed.returncode,
            "passed": completed.returncode == 0 and report_data.get("passed") is True,
            "provider_execution_performed": provider_execution,
            "provider_execution_claim_seen": provider_execution_claim_seen,
            "provider_execution_attempted": provider_execution_attempted,
            "provider_io_observed": provider_execution_attempted,
            "provider_backend": report_data.get("provider_backend"),
            "provider_compute_device": report_data.get("provider_compute_device"),
            "provider_device_verified": report_data.get("provider_device_verified"),
            "logical_lane": report_data.get("logical_lane") or lane,
            "provider_backend_device_id": report_data.get("provider_backend_device_id")
            or spec.get("provider_backend_device_id"),
            "windows_task_manager_device_hint": report_data.get(
                "windows_task_manager_device_hint"
            )
            or spec.get("windows_task_manager_device_hint"),
            "vulkan_visible_device": report_data.get("vulkan_visible_device")
            or spec.get("vulkan_visible_device"),
            "vulkan_device_name": report_data.get("vulkan_device_name")
            or spec.get("vulkan_device_name"),
            "vulkan_vendor_id": report_data.get("vulkan_vendor_id")
            or spec.get("vulkan_vendor_id"),
            "device_identity_verified": report_data.get("device_identity_verified")
            if report_data.get("device_identity_verified") is not None
            else spec.get("device_identity_verified"),
            "cpu_provider_fallback_performed": report_data.get(
                "cpu_provider_fallback_performed"
            ),
            "provider_replight_required": report_data.get("provider_replight_required"),
            "provider_id": report_data.get("provider_id"),
            "provider_role": report_data.get("provider_role") or spec.get("provider_role"),
            "lane_tier": report_data.get("lane_tier") or spec.get("lane_tier"),
            "authority": report_data.get("authority") or spec.get("authority"),
            "closure_owner": report_data.get("closure_owner") or spec.get("closure_owner"),
            "context_budget": report_data.get("context_budget") or spec.get("context_budget"),
            "provider_model": report_data.get("provider_model"),
            "provider_loaded": report_data.get("provider_loaded"),
            "generated_phrase": report_data.get("generated_phrase"),
            "prompt_token_count": report_data.get("prompt_token_count"),
            "completion_token_count": report_data.get("completion_token_count"),
            "token_metric_source": report_data.get("token_metric_source"),
            "tokens_per_second": report_data.get("tokens_per_second"),
            "native_tool_calling_supported": report_data.get("native_tool_calling_supported"),
            "broker_tools_available_count": report_data.get("broker_tools_available_count"),
            "available_tool_names": report_data.get("available_tool_names"),
            "functionalities": report_data.get("functionalities"),
            "replight_passed": report_data.get("replight_passed"),
            "replight_blocked_reason": report_data.get("replight_blocked_reason"),
            "ollama_gpu_layers_requested": report_data.get("ollama_gpu_layers_requested"),
            "ollama_cpu_percent": report_data.get("ollama_cpu_percent"),
            "ollama_gpu_percent": report_data.get("ollama_gpu_percent"),
            "ollama_full_gpu_requested": report_data.get("ollama_full_gpu_requested"),
            "ollama_full_gpu_verified": report_data.get("ollama_full_gpu_verified"),
            "ollama_gpu_residency_status": report_data.get("ollama_gpu_residency_status"),
            "ollama_compute_verified": report_data.get("ollama_compute_verified"),
            "ollama_vulkan_required": report_data.get("ollama_vulkan_required"),
            "product_blocked_reason": report_data.get("product_blocked_reason"),
            "provider_work_verified": report_data.get("provider_work_verified"),
            "provider_rejection_reason": report_data.get("provider_rejection_reason"),
            "device_workload_execution_performed": device_workload_execution,
            "report_kind": report_data.get("kind"),
            "response_text_ref": report_data.get("response_text_ref", {}),
            "response_text_chars": report_data.get("response_text_chars", len(response_text)),
            "response_text_sha256": report_data.get("response_text_sha256", ""),
            "response_text_tail": report_data.get("response_text_tail", response_text[-4000:]),
            "response_text_tail_chars": report_data.get("response_text_tail_chars", min(len(response_text), 4000)),
            "response_text_full_text_in_json": False,
            "tool_calls": tool_calls,
            "textual_tool_calls": textual_tool_calls,
            "rejected_non_native_tool_calls": rejected_non_native_tool_calls,
            "native_tool_loop_requested": native_tool_loop_requested,
            "native_tool_loop_supported": native_tool_loop_supported,
            "native_tool_loop_performed": native_tool_loop_performed,
            "provider_native_tool_api_supported": report_data.get(
                "provider_native_tool_api_supported"
            ),
            "provider_native_tool_api_adapter_available": report_data.get(
                "provider_native_tool_api_adapter_available"
            ),
            "provider_native_tool_call_required": report_data.get(
                "provider_native_tool_call_required"
            ),
            "provider_native_tool_api_attempted": report_data.get(
                "provider_native_tool_api_attempted"
            ),
            "provider_native_tool_api_completed": report_data.get(
                "provider_native_tool_api_completed"
            ),
            "provider_native_tool_api_error": report_data.get(
                "provider_native_tool_api_error"
            ),
            "provider_native_tool_api_attempt_error": report_data.get(
                "provider_native_tool_api_attempt_error"
            ),
            "provider_native_tool_api_unavailable": report_data.get(
                "provider_native_tool_api_unavailable"
            ),
            "provider_native_tool_api_attempt_failed": report_data.get(
                "provider_native_tool_api_attempt_failed"
            ),
            "provider_native_tool_call_required_unmet": report_data.get(
                "provider_native_tool_call_required_unmet"
            ),
            "native_tool_loop_classification": (
                report_data.get("native_tool_loop_classification")
                or report_data.get("classification")
                or report_data.get("npu_micro_provider_classification")
                or report_data.get("semantic_provider_classification")
            ),
            "native_tool_call_count": len(tool_calls),
            "textual_tool_call_count": len(textual_tool_calls) + len(rejected_non_native_tool_calls),
            "role_decision": report_data.get("role_decision"),
            "selected_model": selected_model or report_data.get("selected_model"),
            "target_files": report_data.get("target_files") or report_data.get("TARGET_FILES") or [],
            "validation_commands": report_data.get("validation_commands")
            or report_data.get("VALIDATION_COMMANDS")
            or [],
            "npu_device_workload": report_data.get("npu_device_workload"),
            "npu_device_workload_requested": report_data.get("npu_device_workload_requested"),
            "npu_device_workload_performed": report_data.get("npu_device_workload_performed"),
            "npu_provider_execution_performed": report_data.get("npu_provider_execution_performed"),
            "npu_peer_evidence_verified": report_data.get("npu_peer_evidence_verified"),
            "npu_response_schema_valid": report_data.get("npu_response_schema_valid"),
            "npu_native_tool_loop_error": report_data.get("npu_native_tool_loop_error"),
            "npu_native_tool_loop_required": report_data.get("npu_native_tool_loop_required"),
            "npu_peer_followup_required": report_data.get("npu_peer_followup_required"),
            "npu_peer_activity_performed": report_data.get("npu_peer_activity_performed"),
            "npu_device_execution_performed": report_data.get("npu_device_execution_performed"),
            "npu_activity_classification": report_data.get("npu_activity_classification"),
            "errors": errors,
            "warnings": warnings,
            "stdout_tail": (completed.stdout or "")[-1000:],
            "stderr_tail": (completed.stderr or "")[-1000:],
        }
        if lane == "npu_micro_task_auditor":
            summary.update(
                {
                    "npu_micro_provider_execution_performed": npu_micro_provider_execution,
                    "npu_micro_provider_model_loaded": report_data.get(
                        "npu_micro_provider_model_loaded"
                    ),
                    "npu_micro_provider_classification": report_data.get(
                        "npu_micro_provider_classification"
                    ),
                    "npu_micro_task_kind": report_data.get("npu_micro_task_kind"),
                    "npu_micro_decision": report_data.get("npu_micro_decision"),
                    "npu_micro_task_closed": report_data.get("npu_micro_task_closed"),
                    "npu_micro_audit_performed": report_data.get("npu_micro_audit_performed"),
                }
            )
        else:
            summary.update(
                {
                    "semantic_provider_required": report_data.get("semantic_provider_required"),
                    "semantic_provider_execution_performed": semantic_provider_execution,
                    "semantic_provider_model_loaded": report_data.get(
                        "semantic_provider_model_loaded"
                    ),
                    "semantic_provider_classification": report_data.get(
                        "semantic_provider_classification"
                    ),
                }
            )
        return summary
    def build_quality_failure_feedback(self, text: str, events: list[dict[str, Any]]) -> str:
        file_quality = self.response_file_reference_quality(text)
        implementation_quality = self.implementation_quality_report(text, events)
        candidates = self.real_source_file_candidates(events, limit=32)
        base_feedback = (
            "quality gate failure: la risposta precedente non è uscibile come prodotto heap. "
            f"output_artifact_refs={file_quality.get('output_artifact_refs')}; "
            f"unverified_source_file_refs={file_quality.get('unverified_source_file_refs')}; "
            f"no_source_file_refs={file_quality.get('no_source_file_refs')}; "
            f"implementation_quality_errors={implementation_quality.get('errors')}. "
            "Devi rigenerare usando solo file sorgente reali candidati, con proposte concrete agganciate a path repo esistenti. "
            "Se manca codice/patch/comandi, GPU0 deve considerare il blocco non soddisfacente. "
            f"source_candidates={candidates}"
        )
        iteration_feedback = self.proposal_iteration_feedback(events, file_quality)
        concrete_delta_feedback = self.force_concrete_delta_feedback(events)
        return "\n".join(
            part
            for part in (
                base_feedback,
                self.matrix_patch_candidate_feedback(events),
                iteration_feedback,
                concrete_delta_feedback,
            )
            if part
        )
    def force_concrete_delta_feedback(self, events: list[dict[str, Any]]) -> str:
        """Force GPU1 to produce a materially different concrete block after veto loops.
        This is intentionally feedback-only: it does not change provider calls,
        does not apply patches and does not alter the composer format. It raises
        the in-heap contract pressure when repeated proposal chunks are rejected
        for placeholder/stub markers or near-identical revisions.
        """
        report = self.latest_proposal_iteration_report()
        if not report:
            return ""
        implementation = (
            report.get("implementation_quality")
            if isinstance(report.get("implementation_quality"), dict)
            else {}
        )
        progress = (
            report.get("proposal_progress")
            if isinstance(report.get("proposal_progress"), dict)
            else {}
        )
        quality = (
            report.get("response_file_reference_quality")
            if isinstance(report.get("response_file_reference_quality"), dict)
            else {}
        )
        veto = (
            report.get("cross_lane_veto") if isinstance(report.get("cross_lane_veto"), dict) else {}
        )
        def listify(value: Any) -> list[str]:
            if isinstance(value, list):
                return [str(item) for item in value if str(item).strip()]
            if isinstance(value, tuple):
                return [str(item) for item in value if str(item).strip()]
            if isinstance(value, str) and value.strip():
                return [value.strip()]
            return []
        def parse_similarity(value: Any) -> float:
            try:
                return float(str(value or "0").replace(",", "."))
            except ValueError:
                return 0.0
        placeholder_hits = listify(implementation.get("placeholder_hits"))
        implementation_errors = listify(implementation.get("errors"))
        progress_errors = listify(progress.get("errors"))
        unverified_refs = listify(
            quality.get("unverified_source_file_refs") or quality.get("unverified_file_refs")
        )
        veto_reasons = listify(veto.get("reasons"))
        similarity = parse_similarity(progress.get("similarity"))
        has_placeholder = bool(placeholder_hits) or any(
            marker in item.lower()
            for item in implementation_errors + veto_reasons
            for marker in ("placeholder", "todo", "fixme", "bare_pass", "stub")
        )
        repeated = similarity >= 0.95 or any(
            "similarity=" in item.lower() for item in progress_errors + veto_reasons
        )
        vetoed = veto.get("vetoed") is True
        if not (has_placeholder or repeated or vetoed):
            return ""
        candidates = self.real_source_file_candidates(events, limit=18)
        latest_revision = report.get("revision")
        latest_source = report.get("source")
        lines = [
            "FORCED CONCRETE DELTA REQUIRED:",
            f"- Previous proposal revision: {latest_revision}",
            f"- Previous proposal source: {latest_source}",
            f"- Similarity with previous proposal: {similarity:.3f}",
            "- The previous block was rejected by the same heap. Do not repeat it.",
            "- Treat candidate_response_preview as a negative example when prior flags include invented_source_path, unresolved_pointer_placeholder or unresolved_angle_bracket_token.",
            "- Produce a materially different proposal chunk, not a paraphrase.",
            "- Remove every TODO/FIXME/pass/placeholder/stub marker from the proposal text.",
            "- Use concrete repo-relative TARGET_FILES only from the allowed concrete source targets below.",
            "- Copy TARGET_FILES verbatim from the allowed concrete source targets; do not cite rejected refs anywhere in the next proposal.",
            "- Every diff header path must match an allowed concrete source target exactly.",
            "- If the only possible target is unverified or invented, return EXIT_DECISION=NO_PATCHABLE_TARGET instead of inventing a path.",
            "- Never output unresolved angle-bracket placeholders such as <id-or-empty>.",
            "- For each TARGET_FILE include PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, VALIDATION_COMMANDS, RISKS and EXIT_DECISION.",
            "- If no concrete target is patchable from current evidence, return EXIT_DECISION=NO_PATCHABLE_TARGET with explicit reason.",
            "- GPU1 may move backward on previous/refines/resume pointers to propagate imports, symbols, contracts and validation commands, then resume forward.",
            "- GPU0 and NPU vetoes are authoritative quality signals inside this heap loop.",
        ]
        if placeholder_hits:
            lines.append("- Placeholder hits to eliminate: " + ", ".join(placeholder_hits[:12]))
        if implementation_errors:
            lines.append(
                "- Implementation errors to resolve: " + " | ".join(implementation_errors[:8])
            )
        if progress_errors:
            lines.append("- Progress errors to resolve: " + " | ".join(progress_errors[:8]))
        if unverified_refs:
            lines.append(
                "- Rejected/non-allowlisted source refs blacklist: "
                + ", ".join(unverified_refs[:12])
            )
        if veto_reasons:
            lines.append("- Cross-lane veto reasons to resolve: " + " | ".join(veto_reasons[:8]))
        if candidates:
            lines.append("Allowed concrete source targets:")
            lines.extend(f"- {item}" for item in candidates[:18])
        return "\n".join(lines)
