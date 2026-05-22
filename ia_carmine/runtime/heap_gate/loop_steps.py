"""RuntimeGateLoopStepsMixin extracted from the heap runtime completeness gate."""
from __future__ import annotations
from ia_carmine.runtime.heap_gate.arbiter_product import (
    build_arbiter_product,
    publish_candidate_operation,
)
from ia_carmine.runtime.heap_gate.pointer_soft_lock import runtime_soft_lock_state
from ia_carmine.runtime.heap_gate.runtime_common import (
    BASE_REQUIREMENTS,
    DEFAULT_BRIDGE_DIR,
    DEFAULT_BRIDGE_JSON,
    DEFAULT_BRIDGE_MD,
    PROVIDER_START_REQUIREMENTS,
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
                self.invocation_contract.get("expected_evidence_event_contract")
            ).get("events_required", []),
        }
        completeness_fact = {
            "id": "heap_completeness_requirements_loaded",
            "source": "heap_runtime_completeness_gate",
            "kind": "readiness_requirements",
            "value": self.required_requirements_order(),
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
                "lane": str(plan_item.get("lane") or "gpu1_planner"),
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
                "lane": str(plan_item.get("lane") or "gpu1_planner"),
                "proposal_block_id": str(plan_item.get("proposal_block_id") or ""),
                "provider_block_id": str(plan_item.get("provider_block_id") or ""),
            }
            if plan_item.get("nonblocking"):
                tool_request["nonblocking"] = True
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
            "-m",
            "ia_carmine",
            "provider_runtime_broker_bridge",
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
            str(min(max(int(self.args.timeout_seconds), 60), 900)),
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
            timeout=min(max(int(self.args.timeout_seconds), 60), 900) + 30,
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
        signature = (
            tuple(completed),
            tuple(missing),
            len(broker_results),
            self.tool_execution_count,
        )
        if getattr(self, "_last_critic_progress_signature", None) == signature:
            return
        self._last_critic_progress_signature = signature
        append_unique(self.state["claims"], claim)
        self.publish(
            "deterministic",
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
        soft_lock_state = runtime_soft_lock_state(self, events)
        if ready and int(soft_lock_state.get("open_pointer_count_final") or 0) > 0:
            missing = [*missing, "open_pointer_closure"]
            ready = False
        closure_quorum_status = str(soft_lock_state.get("closure_quorum_status") or "")
        closure_can_exit = closure_quorum_status in {
            "ready_to_close",
            "blocked_continuation_ready",
            "blocked_with_reason",
        }
        if (
            ready
            and self.detailed_output_expected()
            and not self.quality_output_passed(self.response_text(), events)
        ):
            missing = [*missing, "provider_quality_output"]
            ready = False
        budget_exhausted = bool(getattr(self, "runtime_soft_close_reached", lambda: False)())
        no_more_progress = unattempted is None and bool(missing)
        refinement_possible = (
            self.detailed_output_expected()
            and self.provider_reports
            and self.proposal_cycle_requires_refinement(self.response_text(), events)
        )
        if not ready and refinement_possible and not closure_can_exit:
            return
        if not ready and not budget_exhausted and not no_more_progress:
            if not closure_can_exit:
                return
        if closure_quorum_status == "blocked_continuation_ready":
            missing = list(dict.fromkeys([*missing, "blocked_continuation_product"]))
        elif closure_quorum_status == "blocked_with_reason":
            reason = str(soft_lock_state.get("closure_quorum_reason") or "")
            if reason:
                missing = list(dict.fromkeys([*missing, reason]))
        if not ready and not budget_exhausted and not no_more_progress and not closure_can_exit:
            return
        status = "ready" if ready else "blocked_with_reason"
        product_kind = (
            "final_product_approved"
            if ready
            else (
                "blocked_continuation_product"
                if closure_quorum_status == "blocked_continuation_ready"
                else "blocked_with_reason"
            )
        )
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
            "invocation_gate_decision": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
            "provider_generation_permit_allowed": self.budget_governor.get("permit_allowed"),
            "product_kind": product_kind,
            **soft_lock_state,
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
        publish_candidate_operation(self, ready=ready, missing=missing, round_id=round_id)
        self.state["product"] = build_arbiter_product(
            self,
            events,
            ready=ready,
            product_kind=product_kind,
            status=status,
            missing=missing,
            budget_exhausted=budget_exhausted,
            bridge_refs=bridge_refs,
            effective_tool_execution_count=effective_tool_execution_count,
            soft_lock_state=soft_lock_state,
        )
        self.publish(
            "orchestrator",
            "product_signal",
            self.state["product"],
            correlation_id=f"{self.stamp}:product",
            round_id=round_id,
        )
    def base_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        return all(req in self.completed_requirements(events) for req in BASE_REQUIREMENTS)
    def provider_start_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        return all(req in self.completed_requirements(events) for req in PROVIDER_START_REQUIREMENTS)
