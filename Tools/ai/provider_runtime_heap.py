#!/usr/bin/env python3
"""Shared provider runtime heap / blackboard for IA-Carmine.

The heap is a local, append-only JSONL event stream used by provider lanes to
share runtime context without executing tools directly. GPU1, GPU0, NPU,
broker, deterministic validators, telemetry/orchestrator and the startup
context-memory lane can all publish/read structured events.

Guardrails:
- no provider execution;
- no tool execution;
- no patch application;
- no Blender/FFmpeg runtime;
- no Git writes;
- no writes outside the configured heap event/snapshot paths.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.ai.provider_runtime_state import RuntimeState, degraded_lanes, normalize_status
    from tools.validation.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.provider_runtime_state import (  # type: ignore
        RuntimeState,
        degraded_lanes,
        normalize_status,
    )
    from tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

LANES = (
    "gpu1",
    "gpu0",
    "npu",
    "broker",
    "context_memory",
    "deterministic",
    "telemetry",
    "orchestrator",
)
EVENT_TYPES = (
    "user_request",
    "provider_state",
    "task_state",
    "fact",
    "need",
    "tool_catalog_request",
    "tool_catalog_response",
    "evidence_request",
    "evidence_response",
    "lane_evidence",
    "broker_request",
    "broker_result",
    "claim",
    "validation_signal",
    "decision",
    "recommendation",
    "candidate_operation",
    "patch_plan",
    "patch_plan_signal",
    "validation",
    "product_signal",
    "telemetry_signal",
    "startup_task_file_context",
)
DEFAULT_EVENTS = "output/ai_runtime_heap/{stamp}/events.jsonl"
DEFAULT_SNAPSHOT = "output/ai_runtime_heap/{stamp}/snapshot.json"
DEFAULT_MARKDOWN = "output/ai_runtime_heap/{stamp}/snapshot.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if isinstance(value, bool):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
    except ValueError:
        return str(path)


def normalize_lane(value: str) -> str:
    lane = str(value or "").strip().lower()
    if lane not in LANES:
        raise ValueError(f"unsupported provider lane: {value!r}; allowed={list(LANES)}")
    return lane


def normalize_event_type(value: str) -> str:
    event_type = str(value or "").strip().lower()
    if event_type not in EVENT_TYPES:
        raise ValueError(
            f"unsupported runtime heap event type: {value!r}; allowed={list(EVENT_TYPES)}"
        )
    return event_type


def compact_payload(value: Any, max_chars: int = 8000) -> Any:
    text = json.dumps(value, ensure_ascii=False, default=str)
    if len(text) <= max_chars:
        return value
    return {
        "truncated": True,
        "max_chars": max_chars,
        "preview": text[:max_chars],
    }


def load_tool_specs() -> dict[str, Any]:
    """Load the existing broker allowlist lazily to avoid import cycles."""
    try:
        from tools.ai.agent_runtime_tool_broker import (
            TOOL_SPECS,  # pylint: disable=import-outside-toplevel
        )
    except ImportError:
        repo_root_for_import = Path(__file__).resolve().parents[2]
        if str(repo_root_for_import) not in sys.path:
            sys.path.insert(0, str(repo_root_for_import))
        from tools.ai.agent_runtime_tool_broker import (
            TOOL_SPECS,  # type: ignore  # pylint: disable=import-outside-toplevel
        )
    return TOOL_SPECS


def tool_catalog_snapshot() -> dict[str, Any]:
    specs = load_tool_specs()
    tools: list[dict[str, Any]] = []
    for name in sorted(specs):
        spec = specs[name]
        tools.append(
            {
                "tool": spec.name,
                "description": spec.description,
                "allowed_args": list(spec.allowed_args),
                "broker_builder": getattr(spec.builder, "__name__", ""),
                "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker",
            }
        )
    return {
        "schema_version": 1,
        "kind": "semantic_tool_catalog_snapshot",
        "generated_at": now_iso(),
        "tool_count": len(tools),
        "tools": tools,
        "guardrails": {
            "free_shell_exposed": False,
            "broker_allowlist_required": True,
            "provider_direct_tool_execution_allowed": False,
        },
    }


@dataclass(frozen=True)
class RuntimeHeapPaths:
    events: Path
    snapshot: Path
    markdown: Path


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
            snapshot=resolve_output_path(
                repo_root, snapshot_template.format(stamp=stamp)
            ),
            markdown=resolve_output_path(
                repo_root, markdown_template.format(stamp=stamp)
            ),
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
            "payload": compact_payload(safe_dict(payload or {})),
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
                [
                    item
                    for item in events
                    if item.get("kind") == "provider_runtime_event"
                ]
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
            "tool_catalog": tool_catalog_snapshot(),
            "architecture": {
                "gpu1": "primary_advisory_planner",
                "gpu0": "coworker_helper_openvino",
                "npu": "microtask_responder",
                "broker": "single_controlled_executor",
                "context_memory": "startup_context_memory_reload_and_task_file_input",
                "semantic_tools_registry": "agent_runtime_tool_broker.TOOL_SPECS",
                "deterministic_validators": "cpu_authority_validation_lane",
                "telemetry": "append_only_event_stream",
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


def record_lane_diagnostic(
    heap: ProviderRuntimeHeap,
    lane: str,
    status: str,
    message: str,
    details: dict[str, Any] | None = None,
    *,
    round_id: int | None = None,
    target: str | None = "orchestrator",
    correlation_id: str | None = None,
) -> dict[str, Any]:
    """Record one standardized lane diagnostic in the shared runtime heap."""
    normalized_lane = normalize_lane(lane)
    normalized_status = normalize_status(status) or "unknown"
    payload = {
        "lane": normalized_lane,
        "status": normalized_status,
        "message": str(message or ""),
        "details": safe_dict(details or {}),
    }
    return heap.add_event(
        "provider_state",
        payload,
        normalized_lane,
        round_id=round_id,
        target=target,
        correlation_id=correlation_id,
    )


def render_markdown(snapshot: dict[str, Any]) -> str:
    lines = ["# Provider Runtime Heap Snapshot", ""]
    lines.append(f"- Stamp: `{snapshot.get('stamp')}`")
    lines.append(f"- Event count: `{snapshot.get('event_count')}`")
    lines.append(f"- Parse error count: `{snapshot.get('parse_error_count')}`")
    lines.append(
        f"- Pending broker requests: `{snapshot.get('pending_broker_request_count')}`"
    )
    lines.append(f"- Event log: `{snapshot.get('event_log')}`")
    lines.append("")
    runtime_state = safe_dict(snapshot.get("runtime_state"))
    lines.append("## Runtime state")
    lines.append("")
    lines.append(f"- Lane status: `{runtime_state.get('lane_status')}`")
    lines.append(f"- Degraded lanes: `{runtime_state.get('degraded_lanes')}`")
    lines.append(f"- Evidence count: `{runtime_state.get('evidence_count')}`")
    lines.append("")
    lines.append("## Runtime architecture")
    lines.append("")
    for key, value in safe_dict(snapshot.get("architecture")).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Events by lane")
    lines.append("")
    for lane, value in safe_dict(snapshot.get("by_lane")).items():
        lines.append(f"- `{lane}`: `{value}`")
    lines.append("")
    lines.append("## Semantic tools registry")
    lines.append("")
    catalog = safe_dict(snapshot.get("tool_catalog"))
    lines.append(f"- Tool count: `{catalog.get('tool_count')}`")
    for tool in safe_list(catalog.get("tools")):
        if isinstance(tool, dict):
            lines.append(f"- `{tool.get('tool')}`: {tool.get('description')}")
    return "\n".join(lines) + "\n"


def parse_payload(raw: str = "", payload_file: str = "") -> dict[str, Any]:
    if payload_file:
        path = Path(payload_file)
        if not path.is_absolute():
            path = Path.cwd() / path
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            raise ValueError(
                f"payload file unreadable: {path}; error={type(exc).__name__}: {exc}"
            ) from exc

    if not raw:
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        preview = raw[:500].replace("\r", "\\r").replace("\n", "\\n")
        source = f"file={payload_file}" if payload_file else "inline --payload-json"
        raise ValueError(
            f"payload JSON parse failed from {source}; length={len(raw)}; "
            f"preview=[{preview}]; error={exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("payload JSON must be an object")
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--markdown-output", default="")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--source", default="orchestrator")

    append = sub.add_parser("append-event")
    append.add_argument("--source", required=True)
    append.add_argument("--target", default="")
    append.add_argument("--event-type", required=True)
    append.add_argument("--round", type=int, default=None)
    append.add_argument("--correlation-id", default="")
    append.add_argument("--payload-json", default="{}")
    append.add_argument("--payload-file", default="")

    sub.add_parser("snapshot")
    sub.add_parser("tool-catalog")
    sub.add_parser("pending-broker-requests")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(
        repo_root, args.stamp, args.events, args.snapshot, args.markdown_output
    )

    if args.command == "init":
        heap.append_event(
            source=args.source,
            event_type="provider_state",
            payload={
                "state": "heap_initialized",
                "lanes": list(LANES),
                "event_types": list(EVENT_TYPES),
            },
        )
        result = heap.write_snapshot()
    elif args.command == "append-event":
        event = heap.append_event(
            source=args.source,
            target=args.target or None,
            event_type=args.event_type,
            round_id=args.round,
            correlation_id=args.correlation_id or None,
            payload=parse_payload(args.payload_json, args.payload_file),
        )
        result = {"passed": True, "event": event, "snapshot": heap.write_snapshot()}
    elif args.command == "tool-catalog":
        result = tool_catalog_snapshot()
    elif args.command == "pending-broker-requests":
        result = {
            "passed": True,
            "pending_broker_requests": heap.pending_broker_requests(),
        }
    else:
        result = heap.write_snapshot()

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
