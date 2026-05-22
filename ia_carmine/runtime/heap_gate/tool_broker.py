"""RuntimeGateToolBrokerMixin extracted from the heap runtime completeness gate."""
from __future__ import annotations
from ia_carmine.runtime.heap_gate.runtime_common import (
    BASE_REQUIREMENTS,
    PROVIDER_REQUIREMENTS,
    REQUIREMENT_ORDER,
    Any,
    append_unique,
    event_payloads_by_type,
    hashlib,
    json,
    repo_rel,
    safe_int,
)
from ia_carmine.runtime.heap_gate.tool_plan_builder import build_tool_plan
from ia_carmine.runtime.heap_gate.tool_broker_evidence import semantic_evidence_sources
from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
    provider_plan_item_for_tool_call,
    publish_provider_native_tool_calls,
)
TOOL_REQUIREMENT_FALLBACKS = {"agent_runtime_debug_lab": "runtime_debug_lab", "ai_context_pack": "ai_context_pack", "build_agent_agnostic_tool_inventory": "tool_catalog", "build_agent_memory_inventory": "shared_memory", "build_agent_transient_request_context": "shared_context_chunks", "build_code_interpreter_report": "code_interpreter_evidence", "check_python_syntax": "python_syntax_evidence", "refactor_duplication_audit": "refactor_duplication_audit_evidence", "run_heap_code_execution_matrix": "code_execution_matrix", "run_heap_code_execution_tool": "code_execution_matrix", "run_heap_virtual_dev_environment": "virtual_dev_environment", "runtime_file_refs": "runtime_file_refs", "select_semantic_code_chunks": "semantic_code_chunks", "semantic_evidence_chunks": "semantic_evidence_chunks"}
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
            if provider_report.get("passed") is not True:
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
        completed = self.completed_requirements(events)
        return [item for item in self.required_requirements_order() if item not in completed]

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
        base_pending = [item for item in pending if item["requirement"] in BASE_REQUIREMENTS]
        if base_pending:
            pending = base_pending
        elif (
            self.args.allow_provider_generation
            and not self.provider_reports
            and self.base_requirements_complete(events)
        ):
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
            tool_name = str(payload.get("tool") or "")
            memory_request_id = f"{self.stamp}:sqlite-index:{digest}"
            already_requested = any(
                request.get("id") == memory_request_id
                for request in self.state.get("tool_requests", [])
            ) or any(
                str(result.get("request_id") or "") == memory_request_id
                for result in self.broker_results(events)
            )
            if tool_name and tool_name != "runtime_sqlite_memory" and not already_requested:
                memory_need = {
                    "id": f"need_operational_memory_index_{digest}",
                    "owner": "deterministic",
                    "kind": "broker_result_memory_index",
                    "target": "runtime_sqlite_memory",
                    "requirement": "tool_evidence_memory_write",
                    "reason": "index broker result as operational SQLite/FTS evidence ref",
                    "provider_block_id": payload.get("provider_block_id"),
                    "proposal_block_id": payload.get("proposal_block_id"),
                    "round": round_id,
                }
                append_unique(self.state["needs"], memory_need)
                self.publish(
                    "deterministic",
                    "need",
                    memory_need,
                    target="broker",
                    correlation_id=memory_request_id,
                    round_id=round_id,
                )
                memory_request = {
                    "id": memory_request_id,
                    "tool": "runtime_sqlite_memory",
                    "args": {
                        "action": "remember",
                        "scope": "operational",
                        "summary": f"broker evidence ref: {tool_name}/{requirement}",
                        "content": json.dumps(
                            {
                                "tool": tool_name,
                                "requirement": requirement,
                                "outputs": payload.get("outputs"),
                                "summary": payload.get("summary"),
                                "provider_block_id": payload.get("provider_block_id"),
                                "proposal_block_id": payload.get("proposal_block_id"),
                                "broker_report": payload.get("broker_report"),
                            },
                            ensure_ascii=False,
                            default=str,
                        ),
                        "role": "heap_runtime_tool_evidence",
                        "tag": ["heap", "tool_evidence", requirement],
                    },
                    "reason": "index broker result as operational SQLite/FTS evidence ref",
                    "requirement": "tool_evidence_memory_write",
                    "nonblocking": True,
                    "provider_block_id": payload.get("provider_block_id"),
                    "proposal_block_id": payload.get("proposal_block_id"),
                }
                append_unique(self.state["tool_requests"], memory_request)
                self.publish(
                    "deterministic",
                    "broker_request",
                    memory_request,
                    target="broker",
                    correlation_id=memory_request_id,
                    round_id=round_id,
                )
                self.tool_request_count += 1
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
