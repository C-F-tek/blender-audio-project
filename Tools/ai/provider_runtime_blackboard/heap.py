"""Provider runtime blackboard implementation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .state import RuntimeState
from .sqlite_index import index_runtime_heap_event, runtime_heap_index_summary
from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report

from .common import (
    DEFAULT_EVENTS,
    DEFAULT_MARKDOWN,
    DEFAULT_SNAPSHOT,
    RuntimeHeapPaths,
    compact_payload,
    normalize_event_type,
    normalize_lane,
    now_iso,
    repo_rel,
    safe_dict,
    safe_int,
    tool_catalog_snapshot,
)
from .render import render_markdown

@dataclass
class ProviderRuntimeHeap:
    repo_root: Path
    stamp: str
    paths: RuntimeHeapPaths
    runtime_state: RuntimeState = field(default_factory=RuntimeState)

    @classmethod
    def from_args(
        cls,
        repo_root: Path,
        stamp: str,
        events_path: str = "",
        snapshot_path: str = "",
        markdown_path: str = "",
    ) -> ProviderRuntimeHeap:
        event_template = events_path or DEFAULT_EVENTS
        snapshot_template = snapshot_path or DEFAULT_SNAPSHOT
        markdown_template = markdown_path or DEFAULT_MARKDOWN
        paths = RuntimeHeapPaths(
            events=resolve_output_path(repo_root, event_template.format(stamp=stamp)),
            snapshot=resolve_output_path(repo_root, snapshot_template.format(stamp=stamp)),
            markdown=resolve_output_path(repo_root, markdown_template.format(stamp=stamp)),
        )
        # Initialise shared runtime state for lane diagnostics and evidence collection
        runtime_state = RuntimeState()
        return cls(repo_root=repo_root, stamp=stamp, paths=paths, runtime_state=runtime_state)

    def append_event(
        self,
        *,
        source: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        round_id: int | None = None,
        target: str | None = None,
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        source_lane = normalize_lane(source)
        normalized_type = normalize_event_type(event_type)
        target_lane = normalize_lane(target) if target else None
        raw_payload = safe_dict(payload or {})
        compacted_payload = compact_payload(raw_payload)
        raw_payload_json = json.dumps(raw_payload, ensure_ascii=False, sort_keys=True, default=str)
        compacted_payload_json = json.dumps(
            compacted_payload, ensure_ascii=False, sort_keys=True, default=str
        )
        event = {
            "schema_version": 1,
            "kind": "provider_runtime_event",
            "stamp": self.stamp,
            "created_at": now_iso(),
            "source": source_lane,
            "target": target_lane,
            "round": round_id,
            "event_type": normalized_type,
            "correlation_id": correlation_id or "",
            "payload": compacted_payload,
            "payload_index": {
                "sqlite_sidecar": repo_rel(self.repo_root, self.sqlite_index_path()),
                "table": "payload_blobs",
                "full_payload_indexed": True,
                "payload_compacted": raw_payload_json != compacted_payload_json,
                "payload_chars": len(raw_payload_json),
            },
            "guardrails": {
                "provider_execution_performed": False,
                "direct_tool_execution_allowed": False,
                "broker_required_for_tool_execution": True,
                "patch_application_performed": False,
                "source_writes_performed": False,
            },
        }
        self.paths.events.parent.mkdir(parents=True, exist_ok=True)
        with self.paths.events.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        self.runtime_state.apply_event(event)
        self._index_event(event, raw_payload)
        return event

    def add_event(
        self,
        event_type: str,
        payload: dict[str, Any] | None = None,
        lane: str = "orchestrator",
        *,
        round_id: int | None = None,
        target: str | None = None,
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        """Append an event using the lane-first API expected by lane modules."""
        return self.append_event(
            source=lane,
            target=target,
            event_type=event_type,
            round_id=round_id,
            correlation_id=correlation_id,
            payload=payload or {},
        )

    def read_events(self) -> list[dict[str, Any]]:
        if not self.paths.events.exists():
            return []
        events: list[dict[str, Any]] = []
        with self.paths.events.open("r", encoding="utf-8-sig") as handle:
            for line_number, raw in enumerate(handle, start=1):
                text = raw.strip()
                if not text:
                    continue
                try:
                    data = json.loads(text)
                except json.JSONDecodeError as exc:
                    events.append(
                        {
                            "schema_version": 1,
                            "kind": "provider_runtime_event_parse_error",
                            "stamp": self.stamp,
                            "line_number": line_number,
                            "error": str(exc),
                            "raw_preview": text[:500],
                        }
                    )
                    continue
                if isinstance(data, dict):
                    events.append(data)
        return events

    def latest_by_type(self, event_type: str) -> dict[str, Any] | None:
        normalized = normalize_event_type(event_type)
        for event in reversed(self.read_events()):
            if event.get("event_type") == normalized:
                return event
        return None

    def sqlite_index_path(self) -> Path:
        return self.paths.events.with_name("runtime_heap.sqlite3")

    def sqlite_index_summary(self) -> dict[str, Any]:
        return runtime_heap_index_summary(self.sqlite_index_path())

    def _index_event(self, event: dict[str, Any], raw_payload: dict[str, Any]) -> None:
        index_runtime_heap_event(self.sqlite_index_path(), event, full_payload=raw_payload)

    def pending_broker_requests(self) -> list[dict[str, Any]]:
        events = self.read_events()
        result_ids = {
            str(
                event.get("correlation_id")
                or safe_dict(event.get("payload")).get("request_id")
                or ""
            )
            for event in events
            if event.get("event_type") == "broker_result"
        }
        pending: list[dict[str, Any]] = []
        for event in events:
            if event.get("event_type") != "broker_request":
                continue
            request_id = str(
                event.get("correlation_id")
                or safe_dict(event.get("payload")).get("request_id")
                or ""
            )
            if request_id and request_id in result_ids:
                continue
            pending.append(event)
        return pending

    def provider_state_snapshot(self) -> dict[str, Any]:
        events = self.read_events()
        runtime_state = RuntimeState.from_events(events)
        self.runtime_state = runtime_state
        by_lane: dict[str, dict[str, Any]] = {}
        by_type: dict[str, int] = {}
        for event in events:
            if event.get("kind") != "provider_runtime_event":
                continue
            lane = str(event.get("source") or "unknown")
            event_type = str(event.get("event_type") or "unknown")
            lane_state = by_lane.setdefault(
                lane, {"event_count": 0, "latest_event_at": "", "event_types": {}}
            )
            lane_state["event_count"] += 1
            lane_state["latest_event_at"] = str(
                event.get("created_at") or lane_state["latest_event_at"]
            )
            lane_state["event_types"][event_type] = (
                safe_int(lane_state["event_types"].get(event_type)) + 1
            )
            by_type[event_type] = safe_int(by_type.get(event_type)) + 1
        return {
            "schema_version": 1,
            "kind": "provider_runtime_heap_snapshot",
            "generated_at": now_iso(),
            "stamp": self.stamp,
            "event_log": repo_rel(self.repo_root, self.paths.events),
            "event_count": len(
                [item for item in events if item.get("kind") == "provider_runtime_event"]
            ),
            "parse_error_count": len(
                [
                    item
                    for item in events
                    if item.get("kind") == "provider_runtime_event_parse_error"
                ]
            ),
            "by_lane": by_lane,
            "by_event_type": by_type,
            "pending_broker_request_count": len(self.pending_broker_requests()),
            "pending_broker_requests": self.pending_broker_requests()[:20],
            "runtime_state": runtime_state.as_dict(),
            "sqlite_index": self.sqlite_index_summary(),
            "tool_catalog": tool_catalog_snapshot(),
            "architecture": {
                "gpu1": "primary_advisory_planner",
                "gpu0": "coworker_helper_openvino",
                "npu": "microtask_responder",
                "broker": "single_controlled_executor",
                "context_memory": "startup_context_memory_reload_and_task_file_input",
                "semantic_tools_registry": "agent_runtime_tool_broker.TOOL_SPECS",
                "deterministic_validators": "cpu_authority_validation_lane",
            },
            "guardrails": {
                "report_only": True,
                "provider_execution_performed": False,
                "direct_tool_execution_allowed": False,
                "broker_required_for_tool_execution": True,
                "patch_application_performed": False,
                "source_writes_performed": False,
            },
        }

    def write_snapshot(self) -> dict[str, Any]:
        snapshot = self.provider_state_snapshot()
        write_json_report(snapshot, self.paths.snapshot)
        write_text_report(render_markdown(snapshot), self.paths.markdown)
        return snapshot
