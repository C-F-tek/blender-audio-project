"""RuntimeGateLoopStepsMixin extracted from the heap runtime completeness gate."""
from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    BASE_REQUIREMENTS,
    DEFAULT_BRIDGE_DIR,
    DEFAULT_BRIDGE_JSON,
    DEFAULT_BRIDGE_MD,
    REQUIREMENT_ORDER,
    Any,
    append_unique,
    command_env,
    read_json,
    repo_rel,
    resolve_output_path,
    safe_dict,
    safe_int,
    subprocess,
)
class RuntimeGateLoopStepsMixin:
    def bootstrap(self) -> None:
        self.publish(
            "orchestrator",
            "task_state",
            self.state["task"],
            target="gpu1",
            correlation_id=f"{self.stamp}:task",
            round_id=0,
        )
        if self.request_text():
            request_payload = {
                "id": f"{self.stamp}:user_request",
                "text": self.request_text(),
                "objective": self.args.objective,
                "expected_output": [
                    "response_text",
                    "response_source",
                    "heap_event_refs",
                    "provider_refs",
                    "product_status",
                ],
            }
            self.publish(
                "orchestrator",
                "user_request",
                request_payload,
                target="gpu1",
                correlation_id=f"{self.stamp}:user_request",
                round_id=0,
            )
        budget_fact = {
            "id": "provider_budget_governor_loaded",
            "source": "heap_provider_budget_governor",
            "kind": "provider_budget",
            "value": self.budget_governor.get("decision"),
            "loop_budget": self.budget_governor.get("loop_budget"),
            "provider_lanes": sorted((self.budget_governor.get("provider_lanes") or {}).keys()),
        }
        contract_fact = {
            "id": "provider_invocation_contract_loaded",
            "source": "heap_provider_invocation_contract",
            "kind": "provider_invocation_contract",
            "value": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
            "required_events": safe_dict(
                self.invocation_contract.get("expected_telemetry_contract")
            ).get("events_required", []),
        }
        completeness_fact = {
            "id": "heap_completeness_requirements_loaded",
            "source": "heap_runtime_completeness_gate",
            "kind": "readiness_requirements",
            "value": list(REQUIREMENT_ORDER),
            "budget_max_iterations": self.max_iterations,
        }
        universe_refs = self.write_runtime_universe_report()
        universe_fact = {
            "id": "repo_runtime_universe_loaded",
            "source": "runtime_universe",
            "kind": "repo_runtime_universe",
            "summary": self.repo_runtime_universe.summary(),
            "outputs": universe_refs,
        }
        for fact in (budget_fact, contract_fact, completeness_fact, universe_fact):
            append_unique(self.state["facts"], fact)
            self.publish(
                "deterministic",
                "fact",
                fact,
                target="gpu1",
                correlation_id=f"{self.stamp}:fact:{fact['id']}",
                round_id=0,
            )
        # Startup preload is active heap input, not a post-hoc diagnostic pointer.
        # Publish it before the first snapshot/exchange entry so provider lanes and
        # external observers see a single causally ordered universe from startup.
        self.publish_startup_task_file_context()
        self.publish_startup_memory_context_reload_events()
        self.publish_startup_manifest_evidence()
        self.heap.write_snapshot()
        self.write_heap_exchange_entry()

    def planner_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if self.heap.pending_broker_requests():
            return
        plan_items = self.next_unattempted_plan_items(events)
        if not plan_items:
            return
        for plan_item in plan_items:
            request_id = f"{self.stamp}:{plan_item['id']}"
            need = {
                "id": f"need_{plan_item['requirement']}",
                "owner": "planner",
                "kind": "brokered_runtime_evidence",
                "target": plan_item["tool"],
                "requirement": plan_item["requirement"],
                "reason": plan_item["reason"],
                "budget_ref": "provider_budget_governor_loaded",
                "round": round_id,
            }
            append_unique(self.state["needs"], need)
            self.publish(
                "gpu1",
                "need",
                need,
                target="broker",
                correlation_id=request_id,
                round_id=round_id,
            )
            tool_request = {
                "id": request_id,
                "tool": plan_item["tool"],
                "args": plan_item.get("args") or {},
                "reason": plan_item["reason"],
                "requirement": plan_item["requirement"],
            }
            append_unique(self.state["tool_requests"], tool_request)
            self.publish(
                "gpu1",
                "broker_request",
                tool_request,
                target="broker",
                correlation_id=request_id,
                round_id=round_id,
            )
            self.tool_request_count += 1
            self.append_reload_lifecycle_event(
                plan_item["requirement"], round_id, "requested", plan_item["tool"]
            )
            self.append_heap_exchange_event(
                {
                    "kind": "broker_request",
                    "lane": "gpu1",
                    "target": "broker",
                    "round": round_id,
                    "tool": plan_item["tool"],
                    "requirement": plan_item["requirement"],
                    "summary": f"GPU1 requested broker tool {plan_item['tool']} for {plan_item['requirement']}",
                }
            )

    def run_bridge(self) -> dict[str, Any]:
        bridge_json = resolve_output_path(
            self.repo_root,
            self.path_arg(self.args.bridge_output, DEFAULT_BRIDGE_JSON).format(stamp=self.stamp),
        )
        bridge_md = resolve_output_path(
            self.repo_root,
            self.path_arg(self.args.bridge_markdown_output, DEFAULT_BRIDGE_MD).format(
                stamp=self.stamp
            ),
        )
        command = [
            self.child_python(),
            "python -m Tools.ai provider_runtime_broker_bridge",
            "--repo-root",
            ".",
            "--stamp",
            self.stamp,
            "--events",
            repo_rel(self.repo_root, self.heap.paths.events),
            "--snapshot",
            repo_rel(self.repo_root, self.heap.paths.snapshot),
            "--heap-markdown",
            repo_rel(self.repo_root, self.heap.paths.markdown),
            "--bridge-dir",
            self.path_arg(self.args.bridge_dir, DEFAULT_BRIDGE_DIR),
            "--timeout-seconds",
            str(self.args.timeout_seconds),
            "--max-requests",
            "0",
            "--output",
            repo_rel(self.repo_root, bridge_json),
            "--markdown-output",
            repo_rel(self.repo_root, bridge_md),
        ]
        completed = subprocess.run(
            command,
            cwd=self.repo_root,
            env=command_env(self.repo_root),
            capture_output=True,
            text=True,
            check=False,
            timeout=self.args.timeout_seconds + 30,
        )
        report = read_json(bridge_json)
        self.bridge_reports.append(repo_rel(self.repo_root, bridge_json))
        if completed.returncode != 0:
            self.errors.append(
                f"broker bridge returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1000:]}"
            )
        self.tool_execution_count += safe_int(report.get("tool_execution_count"))
        self.append_reload_lifecycle_event(
            "tool_catalog", 0, "bridge_result", "agent_runtime_tool_broker"
        )
        self.append_heap_exchange_event(
            {
                "kind": "broker_result",
                "lane": "broker",
                "summary": "broker bridge executed pending heap tool requests",
                "tool_execution_count": safe_int(report.get("tool_execution_count")),
                "source_file": repo_rel(self.repo_root, bridge_json),
            }
        )
        return report

    def critic_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        broker_results = self.broker_results(events)
        if not broker_results:
            return
        completed = sorted(self.completed_requirements(events))
        missing = self.missing_requirements(events)
        claim = {
            "id": f"heap_completeness_progress_round_{round_id}",
            "from": "critic",
            "claim": (
                "heap evidence complete" if not missing else "heap evidence still incomplete"
            ),
            "confidence": 0.95 if not missing else 0.78,
            "completed_requirements": completed,
            "missing_requirements": missing,
            "broker_result_count": len(broker_results),
            "tool_execution_count": self.tool_execution_count,
        }
        append_unique(self.state["claims"], claim)
        self.publish(
            "npu",
            "claim",
            claim,
            target="gpu1",
            correlation_id=f"{self.stamp}:critic:{round_id}",
            round_id=round_id,
        )
        self.publish(
            "deterministic",
            "validation_signal",
            claim,
            target="gpu1",
            correlation_id=f"{self.stamp}:validation:{round_id}",
            round_id=round_id,
        )

    def arbiter_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if self.state["decisions"]:
            return
        missing = self.missing_requirements(events)
        unattempted = self.next_unattempted_plan_item(events)
        ready = not missing
        bridge_refs = self.bridge_report_refs(events)
        effective_tool_execution_count = self.effective_tool_execution_count(events)
        if ready and effective_tool_execution_count <= 0:
            missing = [*missing, "broker_tool_execution"]
            ready = False
        if ready and not bridge_refs:
            missing = [*missing, "broker_bridge_reports"]
            ready = False
        if ready and self.request_text() and not self.response_text_complete():
            missing = [*missing, "gpu1_request_response_complete"]
            ready = False
        file_quality = self.response_file_reference_quality(self.response_text())
        if ready and not file_quality.get("passed"):
            missing = [*missing, "verified_unambiguous_source_refs"]
            ready = False
        if (
            ready
            and self.detailed_output_expected()
            and not self.quality_output_passed(self.response_text(), events)
        ):
            missing = [*missing, "provider_quality_output"]
            ready = False
        budget_exhausted = round_id >= self.max_iterations
        no_more_progress = unattempted is None and bool(missing)
        refinement_possible = (
            self.detailed_output_expected()
            and self.provider_reports
            and self.provider_revision_count < int(getattr(self.args, "max_provider_revisions", 0))
            and self.proposal_cycle_requires_refinement(self.response_text(), events)
        )
        if not ready and not budget_exhausted and refinement_possible:
            return
        if not ready and not budget_exhausted and not no_more_progress:
            return
        status = "ready" if ready else "blocked_with_reason"
        decision = {
            "id": "heap_completeness_gate_decision",
            "from": "arbiter",
            "decision": ("product_ready_heap_complete" if ready else "blocked_with_reason"),
            "evidence_refs": [
                "heap:task_state",
                "heap:broker_result",
                "heap:shared_evidence",
                "heap:validation_signal",
                *bridge_refs[-4:],
            ],
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": missing,
            "budget_exhausted": budget_exhausted,
            "budget_decision": self.budget_governor.get("decision"),
            "invocation_gate_decision": safe_dict(
                self.invocation_contract.get("real_run_gate")
            ).get("decision"),
            "provider_generation_permit_allowed": self.budget_governor.get("permit_allowed"),
        }
        append_unique(self.state["decisions"], decision)
        self.decision_count += 1
        self.publish(
            "deterministic",
            "decision",
            decision,
            target="orchestrator",
            correlation_id=f"{self.stamp}:decision",
            round_id=round_id,
        )
        candidate = {
            "id": "candidate_heap_runtime_product_flow",
            "kind": "design_operation",
            "path": "tools/workflow/run_unified_real_product_pr.ps1",
            "status": "ready_for_manual_review" if ready else "blocked",
            "rationale": (
                "gate proves heap/tool/memory/context/validation convergence before product readiness"
                if ready
                else "gate blocked because heap completeness requirements were not all satisfied within budget"
            ),
            "missing_requirements": missing,
        }
        append_unique(self.state["candidate_operations"], candidate)
        self.candidate_operation_count += 1
        self.publish(
            "deterministic",
            "candidate_operation",
            candidate,
            target="orchestrator",
            correlation_id=f"{self.stamp}:candidate",
            round_id=round_id,
        )
        final_response_text = self.build_final_response_text(events)
        self.state["product"] = {
            "required": True,
            "status": status,
            "request_input": self.request_text(),
            "response_text": final_response_text,
            "response_source": self.response_source(),
            "heap_event_refs": [repo_rel(self.repo_root, self.heap.paths.events)],
            "provider_refs": self.provider_refs(),
            "provider_response_texts": self.provider_response_texts(),
            "context_artifact_refs": self.broker_output_refs(events),
            "bridge_reports": bridge_refs,
            "quality_output_signals": self.quality_output_signals(final_response_text, events),
            "quality_output_passed": self.quality_output_passed(final_response_text, events),
            "historical_tool_context_refs": self.historical_tool_context_files(),
            "response_file_reference_quality": self.response_file_reference_quality(
                self.response_text()
            ),
            "provider_role_decisions": self.provider_role_decisions(),
            "toolused": effective_tool_execution_count > 0,
            "shared_memory_written_and_used": "shared_memory"
            in self.completed_requirements(events),
            "gpu0_audit": self.provider_response_text("gpu0_peer"),
            "npu_audit": self.provider_response_text("npu_micro_task_auditor"),
            "reason": (
                "heap loop consumed tool catalog, memory, context/chunks and validation evidence"
                if ready
                else "heap loop stopped by budget/failed requirement before readiness"
            ),
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": missing,
            "budget_exhausted": budget_exhausted,
            "budget_governor": self.budget_governor.get("decision"),
        }
        self.publish(
            "orchestrator",
            "product_signal",
            self.state["product"],
            correlation_id=f"{self.stamp}:product",
            round_id=round_id,
        )

    def base_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        completed = self.completed_requirements(events)
        return all(requirement in completed for requirement in BASE_REQUIREMENTS)
