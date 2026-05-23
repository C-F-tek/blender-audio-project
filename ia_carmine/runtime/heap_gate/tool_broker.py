"""RuntimeGateToolBrokerMixin extracted from the heap runtime completeness gate."""
from __future__ import annotations
from ia_carmine.runtime.heap_gate.runtime_common import (
    BASE_REQUIREMENTS,
    PROVIDER_REQUIREMENTS,
    PROVIDER_START_REQUIREMENTS,
    REQUIREMENT_ORDER,
    Any,
    append_unique,
    event_payloads_by_type,
    hashlib,
    json,
    repo_rel,
    safe_int,
)
from ia_carmine.runtime.heap_gate.tool_plan_builder import (
    STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT,
    build_tool_plan,
)
from ia_carmine.runtime.heap_gate.tool_broker_evidence import semantic_evidence_sources
from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
    provider_plan_item_for_tool_call,
    publish_provider_native_tool_calls,
)
from ia_carmine._shared.provider_work_verification import provider_work_status
TOOL_REQUIREMENT_FALLBACKS = {"agent_runtime_debug_lab": "runtime_debug_lab", "ai_context_pack": "ai_context_pack", "build_agent_agnostic_tool_inventory": "tool_catalog", "build_agent_memory_inventory": "shared_memory", "build_agent_transient_request_context": "shared_context_chunks", "build_code_interpreter_report": "code_interpreter_evidence", "check_python_syntax": "python_syntax_evidence", "generic_write": "generic_write_refinement", "rag_context_pack": "rag_context_pack", "refactor_duplication_audit": "refactor_duplication_audit_evidence", "run_heap_code_execution_matrix": "code_execution_matrix", "run_heap_code_execution_tool": "code_execution_matrix", "run_heap_virtual_dev_environment": "virtual_dev_environment", "runtime_file_refs": "runtime_file_refs", "select_semantic_code_chunks": "semantic_code_chunks", "semantic_evidence_chunks": "semantic_evidence_chunks"}
PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT = STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT
PROVIDER_INPUT_HARD_REQUIREMENTS = (
    "runtime_file_refs",
    PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT,
)


def _compact_json_value(value: Any, limit: int = 900) -> Any:
    if not isinstance(value, (dict, list)):
        text = str(value or "")
        return text[:limit] if len(text) > limit else value
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return text[:limit] if len(text) > limit else value


class RuntimeGateToolBrokerMixin:
    def broker_result_digest(self, payload: dict[str, Any]) -> str:
        normalized = {
            "tool": payload.get("tool"),
            "requirement": payload.get("requirement"),
            "outputs": payload.get("outputs"),
            "summary": payload.get("summary"),
            "provider_block_id": payload.get("provider_block_id"),
            "proposal_block_id": payload.get("proposal_block_id"),
        }
        text = json.dumps(normalized, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]
    def tool_plan(self) -> list[dict[str, Any]]:
        return build_tool_plan(self)
    def read_events(self) -> list[dict[str, Any]]:
        self.heap_read_count += 1
        return self.heap.read_events()
    def publish(
        self,
        source: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        target: str = "",
        correlation_id: str = "",
        round_id: int | None = None,
    ) -> None:
        self.heap.append_event(
            source=source,
            target=target or None,
            event_type=event_type,
            correlation_id=correlation_id or None,
            round_id=round_id,
            payload=payload,
        )
        self.heap_write_count += 1

    def broker_results(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return event_payloads_by_type(events, "broker_result")

    def broker_request_count_from_events(self, events: list[dict[str, Any]]) -> int:
        return sum(1 for event in events if event.get("event_type") == "broker_request")

    def broker_execution_count_from_events(self, events: list[dict[str, Any]]) -> int:
        count = 0
        for payload in self.broker_results(events):
            if payload.get("blocked"):
                continue
            if (
                safe_int(payload.get("returncode"), default=1) == 0
                or payload.get("executed") is True
            ):
                count += 1
        return count

    def bridge_report_refs(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for ref in self.bridge_reports:
            if ref and ref not in refs:
                refs.append(ref)
        for payload in self.broker_results(events):
            ref = str(payload.get("broker_report") or "").strip()
            if ref and ref not in refs:
                refs.append(ref)
        return refs

    def effective_tool_request_count(self, events: list[dict[str, Any]]) -> int:
        return max(self.tool_request_count, self.broker_request_count_from_events(events))

    def effective_tool_execution_count(self, events: list[dict[str, Any]]) -> int:
        return max(self.tool_execution_count, self.broker_execution_count_from_events(events))

    def requirement_for_tool(self, tool_name: str) -> str:
        return TOOL_REQUIREMENT_FALLBACKS.get(tool_name, "unknown")

    def completed_requirements(self, events: list[dict[str, Any]]) -> set[str]:
        completed: set[str] = set()
        for payload in self.broker_results(events):
            tool = str(payload.get("tool") or "")
            if payload.get("blocked"):
                continue
            if safe_int(payload.get("returncode"), default=1) != 0:
                continue
            errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
            if errors:
                continue
            requirement = str(payload.get("requirement") or self.requirement_for_tool(tool))
            if requirement != "unknown":
                completed.add(requirement)
        for provider_report in self.provider_reports:
            lane = str(provider_report.get("lane") or provider_report.get("provider_id") or "")
            if not provider_work_status(lane=lane, report=provider_report).get(
                "provider_work_verified"
            ):
                continue
            requirement = str(provider_report.get("requirement") or "")
            if requirement in REQUIREMENT_ORDER:
                completed.add(requirement)
        return completed

    def attempted_requirements(self, events: list[dict[str, Any]]) -> set[str]:
        attempted: set[str] = set()
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "unknown":
                attempted.add(requirement)
        for provider_report in self.provider_reports:
            requirement = str(provider_report.get("requirement") or "")
            if requirement in PROVIDER_REQUIREMENTS:
                attempted.add(requirement)
        return attempted

    def missing_requirements(self, events: list[dict[str, Any]]) -> list[str]:
        return self.unattempted_requirements(events)

    def unattempted_requirements(self, events: list[dict[str, Any]]) -> list[str]:
        attempted = self.attempted_requirements(events)
        order = list(self.required_requirements_order())
        if self.provider_input_gate_enabled():
            for requirement in PROVIDER_INPUT_HARD_REQUIREMENTS:
                if requirement not in order:
                    order.append(requirement)
        return [item for item in order if item not in attempted]

    def failed_requirements(self, events: list[dict[str, Any]]) -> list[str]:
        completed = self.completed_requirements(events)
        attempted = self.attempted_requirements(events)
        order = list(self.required_requirements_order())
        if self.provider_input_gate_enabled():
            for requirement in PROVIDER_INPUT_HARD_REQUIREMENTS:
                if requirement not in order:
                    order.append(requirement)
        return [item for item in order if item in attempted and item not in completed]

    def unsatisfied_requirements(self, events: list[dict[str, Any]]) -> list[str]:
        completed = self.completed_requirements(events)
        order = list(self.required_requirements_order())
        if self.provider_input_gate_enabled():
            for requirement in PROVIDER_INPUT_HARD_REQUIREMENTS:
                if requirement not in order:
                    order.append(requirement)
        return [item for item in order if item not in completed]

    def provider_input_gate_enabled(self) -> bool:
        return bool(getattr(self.args, "allow_provider_generation", False))

    def pre_provider_hard_requirements(self) -> tuple[str, ...]:
        if not self.provider_input_gate_enabled():
            return tuple(BASE_REQUIREMENTS)
        return tuple(
            dict.fromkeys(
                [
                    *BASE_REQUIREMENTS,
                    PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT,
                ]
            )
        )

    def provider_input_hard_requirements(self) -> tuple[str, ...]:
        if not self.provider_input_gate_enabled():
            return tuple(PROVIDER_START_REQUIREMENTS)
        return tuple(
            dict.fromkeys(
                [
                    *PROVIDER_START_REQUIREMENTS,
                    *PROVIDER_INPUT_HARD_REQUIREMENTS,
                ]
            )
        )

    def base_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        completed = self.completed_requirements(events)
        return all(req in completed for req in self.pre_provider_hard_requirements())

    def startup_base_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        completed = self.completed_requirements(events)
        return all(req in completed for req in BASE_REQUIREMENTS)

    def provider_start_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        completed = self.completed_requirements(events)
        return all(req in completed for req in self.provider_input_hard_requirements())

    def broker_output_refs(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in (
                "json_report",
                "markdown_report",
                "evidence_json",
                "evidence_markdown",
                "chunk_output_dir",
                "request_file",
                "debug_lab_report",
                "debug_lab_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def semantic_evidence_sources(self, events: list[dict[str, Any]]) -> list[str]:
        return semantic_evidence_sources(self, events)

    def enrich_plan_item_args(
        self, plan_item: dict[str, Any], events: list[dict[str, Any]]
    ) -> dict[str, Any]:
        item = dict(plan_item)
        args = dict(item.get("args") or {})
        if item.get("requirement") == "shared_context_chunks":
            refs = self.broker_output_refs(events)
            if refs:
                args["report_file"] = refs[:10]
        if item.get("requirement") == "semantic_evidence_chunks":
            sources = self.semantic_evidence_sources(events)
            args.update(
                {
                    "basename": f"heap_runtime_semantic_evidence_{self.stamp}",
                    "source": sources,
                    "output_dir": repo_rel(
                        self.repo_root,
                        self.runtime_context_dir() / "semantic_evidence_chunks",
                    ),
                    "chunk_output_dir": repo_rel(
                        self.repo_root,
                        self.runtime_context_dir() / "semantic_evidence_chunks" / "chunks",
                    ),
                    "chunk_max_chars": max(safe_int(self.args.max_chars_per_file, 12000), 4000),
                    "chunk_overlap_lines": 12,
                }
            )
        if item.get("requirement") in {"code_execution_matrix", "patch_candidate_synthesis"}:
            existing = args.get("evidence_report")
            evidence_reports = list(existing if isinstance(existing, list) else ([existing] if existing else []))
            for ref in [*self.provider_refs(), *self.proposal_iteration_artifacts()]:
                if ref and ref not in evidence_reports:
                    evidence_reports.append(ref)
            if evidence_reports:
                args["evidence_report"] = evidence_reports
        if item.get("requirement") == "tool_evidence_memory_write":
            refs = self.broker_output_refs(events)
            if refs:
                args["content"] = "\n".join(refs[:40])
        if item.get("requirement") == PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT:
            args["content"] = self.provider_input_memory_batch_content(events)
        if item.get("requirement") == "refactor_duplication_audit_evidence":
            refs = [ref for ref in self.broker_output_refs(events) if ref.endswith(".json")]
            if refs:
                args["report"] = refs[:20]
        item["args"] = args
        return item

    def provider_plan_item_for_tool_call(
        self, call: dict[str, Any], events: list[dict[str, Any]]
    ) -> dict[str, Any] | None:
        return provider_plan_item_for_tool_call(self, call, events)

    def publish_provider_native_tool_calls(
        self, round_id: int, events: list[dict[str, Any]]
    ) -> int:
        return publish_provider_native_tool_calls(self, round_id, events)

    def next_unattempted_plan_items(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        attempted = self.attempted_requirements(events)
        provider_started = bool(self.provider_reports) or self.provider_launch_started(events)
        pending = [
            item
            for item in self.tool_plan()
            if item["requirement"] not in attempted
            and (provider_started or not item.get("post_provider"))
        ]
        if not pending:
            return []
        required = set(self.required_requirements_order())
        base_pending = [
            item
            for item in pending
            if item["requirement"] in BASE_REQUIREMENTS
            and item["requirement"] != PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT
        ]
        if base_pending:
            pending = base_pending
        elif self.args.allow_provider_generation and not self.provider_reports:
            baseline_pending = [item for item in pending if item.get("pre_provider_baseline")]
            if baseline_pending:
                pending = baseline_pending
            else:
                provider_input_pending = [
                    item
                    for item in pending
                    if item["requirement"] in PROVIDER_INPUT_HARD_REQUIREMENTS
                ]
                if provider_input_pending:
                    pending = provider_input_pending
                elif self.provider_start_requirements_complete(events):
                    return []
                elif self.startup_base_requirements_complete(events):
                    return []
        else:
            required_pending = [item for item in pending if item["requirement"] in required]
            if required_pending:
                pending = required_pending
        if self.max_iterations < 4:
            return [self.enrich_plan_item_args(pending[0], events)]
        stage = min(int(item.get("stage") or 1) for item in pending)
        return [
            self.enrich_plan_item_args(item, events)
            for item in pending
            if int(item.get("stage") or 1) == stage
        ]

    def next_unattempted_plan_item(self, events: list[dict[str, Any]]) -> dict[str, Any] | None:
        items = self.next_unattempted_plan_items(events)
        return items[0] if items else None

    def provider_launch_started(self, events: list[dict[str, Any]]) -> bool:
        for event in events:
            if event.get("event_type") != "provider_state":
                continue
            payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
            if payload.get("lane") in {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}:
                return True
        return False

    def publish_shared_evidence_facts(self, round_id: int, events: list[dict[str, Any]]) -> None:
        existing = {item.get("requirement") for item in self.state["shared_evidence"]}
        existing_ids = {item.get("id") for item in self.state["shared_evidence"]}
        completed = self.completed_requirements(events)
        for payload in self.broker_results(events):
            if payload.get("blocked"):
                continue
            if safe_int(payload.get("returncode"), default=1) != 0:
                continue
            errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
            if errors:
                continue
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement == "unknown":
                continue
            digest = self.broker_result_digest(payload)
            evidence_id = f"shared_evidence_{requirement}_{digest}"
            if evidence_id not in existing_ids:
                evidence = {
                    "id": evidence_id,
                    "requirement": requirement,
                    "kind": "shared_runtime_evidence",
                    "source": "broker_result",
                    "status": "available",
                    "tool": payload.get("tool"),
                    "outputs": payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {},
                    "summary": payload.get("summary") if isinstance(payload.get("summary"), dict) else payload.get("summary"),
                    "provider_block_id": payload.get("provider_block_id"),
                    "proposal_block_id": payload.get("proposal_block_id"),
                    "broker_report": payload.get("broker_report"),
                    "indexed_in_sqlite": False,
                    "chunked": requirement == "semantic_evidence_chunks",
                }
                append_unique(self.state["shared_evidence"], evidence)
                self.publish(
                    "deterministic",
                    "fact",
                    evidence,
                    target="gpu1",
                    correlation_id=f"{self.stamp}:shared:{requirement}:{digest}",
                    round_id=round_id,
                )
                existing_ids.add(evidence_id)
        for requirement in REQUIREMENT_ORDER:
            if requirement not in completed or requirement in existing:
                continue
            evidence = {
                "id": f"shared_evidence_{requirement}",
                "requirement": requirement,
                "kind": "shared_runtime_evidence",
                "source": "broker_result",
                "status": "available",
            }
            append_unique(self.state["shared_evidence"], evidence)
            self.publish(
                "deterministic",
                "fact",
                evidence,
                target="gpu1",
                correlation_id=f"{self.stamp}:shared:{requirement}",
                round_id=round_id,
            )
        self.publish_provider_input_readiness(round_id, events)

    def provider_input_memory_batch_payload(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        artifact_refs: list[dict[str, Any]] = []
        completed = sorted(self.completed_requirements(events))
        for payload in self.broker_results(events):
            if payload.get("blocked"):
                continue
            if safe_int(payload.get("returncode"), default=1) != 0:
                continue
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement in {"unknown", PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT}:
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            artifact_refs.append(
                {
                    "tool": str(payload.get("tool") or ""),
                    "requirement": requirement,
                    "digest": self.broker_result_digest(payload),
                    "outputs": {
                        key: value
                        for key, value in outputs.items()
                        if str(value or "").strip()
                    },
                    "summary": _compact_json_value(payload.get("summary"), 700),
                    "broker_report": str(payload.get("broker_report") or ""),
                }
            )
        return {
            "schema_version": 1,
            "kind": PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT,
            "stamp": self.stamp,
            "purpose": "single pre-provider SQLite/FTS5 index batch for provider-consumable evidence",
            "hard_gates": list(self.provider_input_hard_requirements()),
            "completed_requirements": completed,
            "artifact_ref_count": len(artifact_refs),
            "artifact_refs": artifact_refs[:80],
            "runtime_file_refs_required": "runtime_file_refs" in self.provider_input_hard_requirements(),
            "post_provider_validation_boundary": {
                "code_execution_matrix": "final_product_validation_after_provider_proposal",
            },
        }

    def provider_input_memory_batch_content(self, events: list[dict[str, Any]]) -> str:
        return json.dumps(
            self.provider_input_memory_batch_payload(events),
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        )

    def publish_provider_input_readiness(
        self, round_id: int, events: list[dict[str, Any]]
    ) -> None:
        if not self.provider_input_gate_enabled():
            return
        completed = self.completed_requirements(events)
        hard_requirements = list(self.provider_input_hard_requirements())
        missing = [item for item in hard_requirements if item not in completed]
        signature = (tuple(sorted(completed)), tuple(missing))
        if getattr(self, "_provider_input_readiness_signature", None) == signature:
            return
        self._provider_input_readiness_signature = signature
        payload = {
            "id": f"{self.stamp}:provider_input_readiness",
            "kind": "provider_input_readiness",
            "provider_consumable_evidence_ready": not missing,
            "provider_start_hard_requirements": hard_requirements,
            "provider_start_missing_requirements": missing,
            "runtime_file_refs_ready": "runtime_file_refs" in completed,
            "memory_index_batch_ready": (
                PROVIDER_INPUT_MEMORY_INDEX_BATCH_REQUIREMENT in completed
            ),
            "post_provider_validation_boundary": (
                "code_execution_matrix remains final product validation after provider proposal"
            ),
        }
        self.publish(
            "deterministic",
            "validation_signal",
            payload,
            target="gpu1",
            correlation_id=f"{self.stamp}:provider-input-readiness",
            round_id=round_id,
        )
