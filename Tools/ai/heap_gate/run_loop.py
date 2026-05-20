"""RuntimeGateRunLoopMixin extracted from the heap runtime completeness gate."""
from __future__ import annotations
from Tools.ai.heap_gate.run_loop_metrics import build_provider_lane_metrics
from Tools.ai.heap_gate.runtime_common import Any, evaluate_terminal_invariants, now_iso, record_lane_diagnostic, repo_rel, runtime_state_lane_gate, safe_dict, safe_int
class RuntimeGateRunLoopMixin:
    def run(self) -> dict[str, Any]:
        self.bootstrap()
        last_round = 0
        round_id = 0
        while True:
            round_id += 1
            last_round = round_id
            events = self.read_events()
            self.planner_step(round_id, events)
            if self.heap.pending_broker_requests():
                self.run_bridge()
            events = self.read_events()
            self.publish_shared_evidence_facts(round_id, events)
            if self.heap.pending_broker_requests():
                self.run_bridge()
                events = self.read_events()
                self.publish_shared_evidence_facts(round_id, events)
            if self.provider_start_requirements_complete(events) and not self.provider_reports:
                self.run_provider_teamwork(round_id)
                if self.provider_universe_blocked_reason:
                    break
                events = self.read_events()
                if self.publish_provider_native_tool_calls(round_id, events):
                    if self.heap.pending_broker_requests():
                        self.run_bridge()
                    events = self.read_events()
                self.publish_shared_evidence_facts(round_id, events)
                if self.heap.pending_broker_requests():
                    self.run_bridge()
                    events = self.read_events()
                    self.publish_shared_evidence_facts(round_id, events)
                if self.detailed_output_expected() and self.response_text():
                    events = self.persist_current_gpu1_proposal_iteration(
                        revision=0,
                        events=events,
                        source="gpu1_initial",
                    )
            if (
                self.base_requirements_complete(events)
                and self.provider_reports
                and self.provider_revision_evidence_ready(events)
            ):
                events = self.maybe_run_provider_quality_revisions(round_id, events)
                if self.provider_universe_blocked_reason:
                    break
                if self.publish_provider_native_tool_calls(round_id, events):
                    if self.heap.pending_broker_requests():
                        self.run_bridge()
                    events = self.read_events()
            self.critic_step(round_id, events)
            self.arbiter_step(round_id, events)
            if self.state["product"].get("status") in {"ready", "blocked_with_reason"} and self.minimum_runtime_depth_satisfied(round_id):
                break
        if self.state["product"].get("status") == "not_ready":
            events = self.read_events()
            self.arbiter_step(last_round or self.max_iterations, events)
        snapshot = self.heap.write_snapshot()
        runtime_state = safe_dict(snapshot.get("runtime_state"))
        lane_gate = runtime_state_lane_gate(
            safe_dict(runtime_state.get("lane_status")),
            self.args.max_degraded_lanes,
        )
        record_lane_diagnostic(
            self.heap,
            "orchestrator",
            "ready" if lane_gate["passed"] else "failed",
            "Runtime lane viability evaluated; degraded/unavailable lanes are unviable in complete/full mode.",
            lane_gate,
            correlation_id=f"{self.stamp}:runtime-state-gate",
        )
        snapshot = self.heap.write_snapshot()
        final_events = self.read_events()
        if self.detailed_output_expected():
            final_revision = max(0, int(self.provider_revision_count))
            final_provider_text = self.response_text()
            if final_provider_text:
                self.write_proposal_iteration_artifact(
                    final_revision,
                    final_provider_text,
                    self.response_file_reference_quality(final_provider_text),
                    final_events,
                    source="gpu1_final",
                )
                final_events = self.read_events()
        completed_all = sorted(self.completed_requirements(final_events))
        required_order = self.required_requirements_order()
        required_set = set(required_order)
        completed_set = set(completed_all)
        completed = [requirement for requirement in required_order if requirement in completed_all]
        optional_completed = [
            requirement for requirement in completed_all if requirement not in required_set
        ]
        missing = self.missing_requirements(final_events)
        final_bridge_reports = self.bridge_report_refs(final_events)
        final_tool_request_count = self.effective_tool_request_count(final_events)
        final_tool_execution_count = self.effective_tool_execution_count(final_events)
        final_response_text = self.build_final_response_text(final_events)
        final_quality_signals = self.quality_output_signals(final_response_text, final_events)
        provider_reports_by_lane = {
            str(item.get("lane") or "unknown"): item for item in self.provider_reports
        }
        latest_provider_reports = list(provider_reports_by_lane.values())
        provider_lane_metrics = build_provider_lane_metrics(
            self, provider_reports_by_lane, latest_provider_reports
        )
        metrics = {
            "heap_read_count": self.heap_read_count,
            "heap_write_count": self.heap_write_count,
            "tool_request_count": final_tool_request_count,
            "tool_execution_count": final_tool_execution_count,
            "decision_count": self.decision_count,
            "candidate_operation_count": self.candidate_operation_count,
            "product_status": self.state["product"].get("status"),
            "budget_decision": self.budget_governor.get("decision"),
            "budget_max_iterations": self.max_iterations,
            "completed_requirement_count": len(completed),
            "required_requirement_count": len(required_order),
            "completed_requirements": completed,
            "optional_completed_requirements": optional_completed,
            "missing_requirements": missing,
            "request_input": self.request_text(),
            "response_text": final_response_text,
            "provider_raw_response_text": self.response_text(),
            "response_source": self.response_source(),
            "response_text_present": bool(final_response_text),
            "detailed_output_expected": self.detailed_output_expected(),
            "quality_output_passed": self.quality_output_passed(final_response_text, final_events),
            "quality_output_signals": final_quality_signals,
            "virtual_dev_environment_required": self.virtual_dev_environment_required(),
            "virtual_dev_environment_passed": self.virtual_dev_environment_passed(final_events),
            "virtual_dev_environment_reports": self.virtual_dev_environment_reports(final_events),
            "code_execution_matrix_required": self.code_execution_matrix_required(),
            "code_execution_matrix_passed": self.code_execution_matrix_passed(final_events),
            "code_execution_matrix_reports": self.code_execution_matrix_reports(final_events),
            "matrix_verified_target_count": self.code_execution_matrix_metric_count(
                final_events, "verified_target_count"
            ),
            "concrete_code_proposal_count": self.code_execution_matrix_metric_count(
                final_events, "concrete_code_proposal_count"
            ),
            "patch_candidate_synthesis_required": self.patch_candidate_synthesis_required(),
            "patch_candidate_synthesis_passed_count": self.code_execution_matrix_metric_count(
                final_events, "patch_candidate_synthesis_passed_count"
            ),
            "runtime_universe": self.repo_runtime_universe.summary(),
            "runtime_universe_reports": self.runtime_universe_report_refs,
            "runtime_debug_lab_required": self.runtime_debug_lab_required(),
            "runtime_debug_lab_passed": self.runtime_debug_lab_passed(final_events),
            "runtime_debug_lab_reports": self.runtime_debug_lab_reports(final_events),
            "proposal_iteration_artifacts": self.proposal_iteration_artifacts(),
            "historical_tool_context_refs": self.historical_tool_context_files(),
            "response_file_reference_quality": self.response_file_reference_quality(
                self.response_text()
            ),
            "provider_refs": self.provider_refs(),
            "provider_response_texts": self.provider_response_texts(),
            "context_artifact_refs": self.broker_output_refs(final_events),
            "shared_evidence_count": len(self.state["shared_evidence"]),
            "shared_memory_evidence_count": 1 if "shared_memory" in completed else 0,
            "persistent_memory_status_count": 1 if "persistent_memory_status" in completed else 0,
            "persistent_memory_search_count": 1 if "persistent_memory_search" in completed else 0,
            "shared_context_chunk_evidence_count": (
                1 if "shared_context_chunks" in completed else 0
            ),
            "semantic_code_chunk_evidence_count": (1 if "semantic_code_chunks" in completed else 0),
            "ai_context_pack_evidence_count": (1 if "ai_context_pack" in completed else 0),
            "semantic_evidence_chunk_count": (1 if "semantic_evidence_chunks" in completed else 0),
            "runtime_file_refs_evidence_count": (1 if "runtime_file_refs" in completed else 0),
            "operational_memory_write_count": (1 if "operational_memory_write" in completed else 0),
            "operational_memory_search_count": 1 if "operational_memory_search" in completed else 0,
            "tool_catalog_evidence_count": 1 if "tool_catalog" in completed else 0,
            "tool_evidence_memory_write_count": 1 if "tool_evidence_memory_write" in completed_set else 0,
            "python_line_count_evidence_count": 1 if "python_line_count_evidence" in completed_set else 0,
            "python_syntax_evidence_count": 1 if "python_syntax_evidence" in completed_set else 0,
            "code_interpreter_report_count": 1 if "code_interpreter_evidence" in completed_set else 0,
            "refactor_duplication_audit_count": 1 if "refactor_duplication_audit_evidence" in completed_set else 0,
            "virtual_dev_environment_count": (1 if "virtual_dev_environment" in completed else 0),
            "code_execution_matrix_count": (1 if "code_execution_matrix" in completed else 0),
            "gpu1_provider_evidence_count": (1 if "gpu1_provider_planner" in completed else 0),
            "gpu0_provider_evidence_count": (1 if "gpu0_provider_peer" in completed else 0),
            "npu_micro_task_evidence_count": (1 if "npu_micro_task_auditor" in completed else 0),
            "provider_result_count": len(self.provider_reports),
            "provider_revision_count": self.provider_revision_count,
            "provider_revision_counter_semantics": (
                "positive_evidence_counter_not_loop_cutoff"
            ),
            **provider_lane_metrics,
            "budget_exhausted": bool(missing and self.runtime_soft_close_reached()),
            "invocation_contract_ready": bool(self.invocation_contract.get("passed")),
            "invocation_gate_decision": safe_dict(
                self.invocation_contract.get("real_run_gate")
            ).get("decision"),
            "runtime_state_lane_status": lane_gate["lane_status"],
            "runtime_state_unviable_lanes": lane_gate["unviable_lanes"],
            "runtime_state_unviable_lane_count": lane_gate["unviable_lane_count"],
            "runtime_state_degraded_lanes": lane_gate["degraded_lanes"],
            "runtime_state_degraded_lane_count": lane_gate["degraded_lane_count"],
            "max_degraded_lanes": lane_gate["max_degraded_lanes"],
            "configured_max_degraded_lanes": lane_gate["configured_max_degraded_lanes"],
            "runtime_state_gate_passed": lane_gate["passed"],
            "response_text_complete": self.response_text_complete(),
        }
        exit_output_product = self.write_exit_output_product(
            final_response_text, final_events, metrics
        )
        heap_exchange_exit_product = self.build_heap_exchange_exit_product(
            require_concrete_product=metrics.get("product_status") == "ready"
        )
        metrics["heap_exchange_runtime_entry"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["runtime_entry"]
        )
        metrics["heap_exchange_runtime_state"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["runtime_state"]
        )
        metrics["heap_runtime_exit_output"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["exit_output"]
        )
        metrics["heap_exchange_runtime_exit_product"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["exit_product"]
        )
        metrics["heap_exchange_exit_passed"] = heap_exchange_exit_product.get("passed")
        self.errors.extend(
            evaluate_terminal_invariants(
                metrics=metrics,
                missing_requirements=missing,
                lane_gate_passed=bool(lane_gate["passed"]),
                degraded_lanes=list(lane_gate["unviable_lanes"]),
                final_bridge_reports=final_bridge_reports,
                allow_provider_generation=bool(self.args.allow_provider_generation),
                provider_execution_performed=bool(self.provider_execution_performed),
                detailed_output_expected=bool(self.detailed_output_expected()),
            )
        )
        return {
            "schema_version": 1,
            "kind": "heap_runtime_completeness_gate",
            "generated_at": now_iso(),
            "repo_root": self.repo_root.as_posix(),
            "stamp": self.stamp,
            "passed": not self.errors,
            "metrics": metrics,
            "state": self.state,
            "budget_governor": self.budget_governor,
            "heap_snapshot": {
                "event_count": snapshot.get("event_count"),
                "event_log": snapshot.get("event_log"),
                "runtime_state": snapshot.get("runtime_state"),
                "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
            },
            "bridge_reports": final_bridge_reports,
            "provider_reports": self.provider_reports,
            "heap_runtime_exit_output": exit_output_product,
            "heap_exchange_runtime_exit_product": heap_exchange_exit_product,
            "real_run_input_contract": {
                "kind": "heap_runtime_completeness_gate_input_contract",
                "task_file": self.args.task_file,
                "objective": self.args.objective,
                "request": self.request_text(),
                "stamp": self.stamp,
                "budget_minutes": self.args.budget_minutes,
                "max_iterations": self.max_iterations,
                "entry_files": [
                    "AGENTS.md",
                    "README.md",
                    *self.historical_tool_context_files(),
                ],
            },
            "real_run_output_contract": {
                "kind": "heap_runtime_completeness_gate_output_contract",
                "heap_event_log": snapshot.get("event_log"),
                "heap_snapshot": snapshot.get("snapshot"),
                "bridge_reports": final_bridge_reports,
                "provider_report_outputs": [item.get("output") for item in self.provider_reports],
                "request_input": self.request_text(),
                "response_text": final_response_text,
                "provider_raw_response_text": self.response_text(),
                "response_source": self.response_source(),
                "quality_output_signals": final_quality_signals,
                "response_file_reference_quality": self.response_file_reference_quality(
                    self.response_text()
                ),
                "virtual_dev_environment_required": metrics.get("virtual_dev_environment_required"),
                "virtual_dev_environment_passed": metrics.get("virtual_dev_environment_passed"),
                "virtual_dev_environment_reports": metrics.get("virtual_dev_environment_reports"),
                "runtime_debug_lab_required": metrics.get("runtime_debug_lab_required"),
                "runtime_debug_lab_passed": metrics.get("runtime_debug_lab_passed"),
                "runtime_debug_lab_reports": metrics.get("runtime_debug_lab_reports"),
                "code_execution_matrix_required": metrics.get("code_execution_matrix_required"),
                "code_execution_matrix_passed": metrics.get("code_execution_matrix_passed"),
                "code_execution_matrix_reports": metrics.get("code_execution_matrix_reports"),
                "proposal_iteration_artifacts": metrics.get("proposal_iteration_artifacts"),
                "heap_runtime_exit_output": repo_rel(
                    self.repo_root, self.heap_exchange_paths()["exit_output"]
                ),
                "heap_exchange_runtime_exit_product": repo_rel(
                    self.repo_root, self.heap_exchange_paths()["exit_product"]
                ),
                "heap_exchange_runtime_state": repo_rel(
                    self.repo_root, self.heap_exchange_paths()["runtime_state"]
                ),
                "provider_refs": self.provider_refs(),
                "provider_response_texts": self.provider_response_texts(),
                "context_artifact_refs": self.broker_output_refs(final_events),
                "product_status": self.state["product"].get("status"),
                "completed_requirements": completed,
                "missing_requirements": missing,
            },
            "provider_execution_performed": self.provider_execution_performed,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "errors": self.errors,
            "warnings": self.warnings,
            "guardrails": {
                "heap_completeness_gate": True,
                "provider_teamwork_universe_required": True,
                "provider_execution_performed": self.provider_execution_performed,
                "patch_application_performed": False,
                "source_writes_performed": False,
            },
        }
    def minimum_runtime_depth_satisfied(self, round_id: int) -> bool:
        min_rounds = max(1, int(getattr(self.args, "min_runtime_rounds", 1)))
        min_proposals = max(0, int(getattr(self.args, "min_proposal_iterations", 0)))
        proposal_json_count = len(
            [path for path in self.proposal_iteration_artifacts() if str(path).endswith(".json")]
        )
        return round_id >= min_rounds and proposal_json_count >= min_proposals
