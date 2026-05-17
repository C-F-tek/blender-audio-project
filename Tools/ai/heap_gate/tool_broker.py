"""RuntimeGateToolBrokerMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    PROVIDER_REQUIREMENTS,
    REQUIREMENT_ORDER,
    Any,
    append_unique,
    event_payloads_by_type,
    provider_heap_lane,
    provider_patch_synthesis_plan,
    repo_rel,
    safe_int,
)
from Tools.ai.heap_gate.tool_plan_builder import build_tool_plan


class RuntimeGateToolBrokerMixin:
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
        for item in self.tool_plan():
            if item["tool"] == tool_name:
                return str(item["requirement"])
        return "unknown"

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
        sources: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement not in {
                "shared_context_chunks",
                "semantic_code_chunks",
                "ai_context_pack",
                "operational_memory_search",
            }:
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in (
                "json_report",
                "markdown_report",
                "evidence_json",
                "evidence_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value and value not in sources:
                    sources.append(value)
        return sources[:8]

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
                    "chunk_max_chars": min(max(int(self.args.max_chars_per_file), 4000), 12000),
                    "chunk_overlap_lines": 12,
                }
            )
        item["args"] = args
        return item

    def provider_plan_item_for_tool_call(
        self, call: dict[str, Any], events: list[dict[str, Any]]
    ) -> dict[str, Any] | None:
        tool_name = str(call.get("tool") or "").strip()
        requirement = str(call.get("requirement") or "").strip()
        for item in self.tool_plan():
            if item["tool"] == tool_name or (requirement and item["requirement"] == requirement):
                enriched = self.enrich_plan_item_args(item, events)
                provider_args = call.get("args") if isinstance(call.get("args"), dict) else {}
                merged_args = dict(provider_args)
                merged_args.update(dict(enriched.get("args") or {}))
                enriched["args"] = merged_args
                return enriched
        if tool_name == "synthesize_patch_candidates":
            return provider_patch_synthesis_plan(
                call=call,
                target_files=self.code_execution_matrix_targets(),
                operator_request=self.request_text(),
                files_per_round=int(self.args.files_per_round),
                timeout_seconds=int(self.args.timeout_seconds),
            )
        return None

    def publish_provider_native_tool_calls(
        self, round_id: int, events: list[dict[str, Any]]
    ) -> int:
        published = 0
        for report in self.provider_reports:
            lane = str(report.get("lane") or "provider")
            source = provider_heap_lane(lane)
            output = str(report.get("output") or "")
            calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
            for index, call in enumerate(calls, start=1):
                if not isinstance(call, dict):
                    continue
                tool_name = str(call.get("tool") or "").strip()
                call_id = str(call.get("id") or f"{tool_name}_{index:03d}")
                unique_id = f"{output}:{call_id}:{tool_name}"
                if unique_id in self.provider_native_tool_call_ids:
                    continue
                self.provider_native_tool_call_ids.add(unique_id)
                plan_item = self.provider_plan_item_for_tool_call(call, events)
                if not plan_item:
                    self.errors.append(
                        f"provider_native_tool_call_unmapped:{lane}:{tool_name or '<empty>'}"
                    )
                    self.publish(
                        source,
                        "validation_signal",
                        {
                            "kind": "provider_native_tool_call_unmapped",
                            "lane": lane,
                            "tool_call": call,
                            "provider_report": output,
                        },
                        target="deterministic",
                        correlation_id=unique_id,
                        round_id=round_id,
                    )
                    continue
                request_id = f"{self.stamp}:provider-native:{call_id}:{plan_item['tool']}"
                need = {
                    "id": f"need_provider_native_{plan_item['requirement']}_{call_id}",
                    "owner": lane,
                    "kind": "provider_native_tool_call",
                    "target": plan_item["tool"],
                    "requirement": plan_item["requirement"],
                    "reason": call.get("reason")
                    or plan_item.get("reason")
                    or "provider native tool call requested broker evidence",
                    "provider_report": output,
                    "round": round_id,
                }
                append_unique(self.state["needs"], need)
                self.publish(
                    source,
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
                    "reason": need["reason"],
                    "requirement": plan_item["requirement"],
                    "provider_native_tool_call": True,
                    "provider_report": output,
                }
                append_unique(self.state["tool_requests"], tool_request)
                self.publish(
                    source,
                    "broker_request",
                    tool_request,
                    target="broker",
                    correlation_id=request_id,
                    round_id=round_id,
                )
                self.tool_request_count += 1
                published += 1
        return published

    def next_unattempted_plan_items(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        attempted = self.attempted_requirements(events)
        pending = [item for item in self.tool_plan() if item["requirement"] not in attempted]
        if not pending:
            return []
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

    def publish_shared_evidence_facts(self, round_id: int, events: list[dict[str, Any]]) -> None:
        existing = {item.get("requirement") for item in self.state["shared_evidence"]}
        completed = self.completed_requirements(events)
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
