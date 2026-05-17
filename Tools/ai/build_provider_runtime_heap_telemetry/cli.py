#!/usr/bin/env python3
"""Build collaboration telemetry from the provider runtime heap event stream."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict
    from tools.validation.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict  # type: ignore
    from tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

DEFAULT_OUTPUT = "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_{stamp}.json"
DEFAULT_MARKDOWN = "docs/LOCAL_VALIDATION_EVIDENCE/provider_runtime_heap_telemetry_{stamp}.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def count_edges(events: list[dict[str, Any]]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for event in events:
        if event.get("kind") != "provider_runtime_event":
            continue
        source = str(event.get("source") or "unknown")
        target = str(event.get("target") or "none")
        event_type = str(event.get("event_type") or "unknown")
        counter[f"{source}->{target}:{event_type}"] += 1
    return dict(sorted(counter.items()))


def count_by(events: list[dict[str, Any]], key: str) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for event in events:
        if event.get("kind") == "provider_runtime_event":
            counter[str(event.get(key) or "unknown")] += 1
    return dict(sorted(counter.items()))


def correlated_complete(events: list[dict[str, Any]], request_type: str, response_type: str) -> int:
    requests = {
        str(event.get("correlation_id") or "")
        for event in events
        if event.get("event_type") == request_type and event.get("correlation_id")
    }
    responses = {
        str(event.get("correlation_id") or "")
        for event in events
        if event.get("event_type") == response_type and event.get("correlation_id")
    }
    return len(requests & responses)


def gpu_peer_exchange_metrics(events: list[dict[str, Any]]) -> dict[str, Any]:
    gpu1_to_gpu0 = [
        event for event in events if event.get("source") == "gpu1" and event.get("target") == "gpu0"
    ]
    gpu0_to_gpu1 = [
        event for event in events if event.get("source") == "gpu0" and event.get("target") == "gpu1"
    ]
    request_ids = {
        str(event.get("correlation_id") or "")
        for event in gpu1_to_gpu0
        if event.get("correlation_id")
    }
    response_ids = {
        str(event.get("correlation_id") or "")
        for event in gpu0_to_gpu1
        if event.get("correlation_id")
    }
    return {
        "gpu1_to_gpu0_event_count": len(gpu1_to_gpu0),
        "gpu0_to_gpu1_event_count": len(gpu0_to_gpu1),
        "gpu1_gpu0_bidirectional": bool(gpu1_to_gpu0 and gpu0_to_gpu1),
        "gpu1_gpu0_correlated_exchange_count": len(request_ids & response_ids),
        "gpu1_gpu0_request_event_types": sorted(
            {str(event.get("event_type") or "") for event in gpu1_to_gpu0}
        ),
        "gpu1_gpu0_response_event_types": sorted(
            {str(event.get("event_type") or "") for event in gpu0_to_gpu1}
        ),
    }


def direct_execution_violations(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for event in events:
        if event.get("kind") != "provider_runtime_event":
            continue
        payload = safe_dict(event.get("payload"))
        guardrails = safe_dict(event.get("guardrails"))
        if (
            payload.get("direct_execution") is True
            or guardrails.get("direct_tool_execution_allowed") is True
        ):
            violations.append(
                {
                    "source": event.get("source"),
                    "target": event.get("target"),
                    "event_type": event.get("event_type"),
                    "correlation_id": event.get("correlation_id"),
                    "payload_preview": payload,
                }
            )
    return violations


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(
        repo_root, args.stamp, args.events, args.snapshot, args.heap_markdown
    )
    snapshot = heap.write_snapshot()
    events = heap.read_events()
    runtime_events = [event for event in events if event.get("kind") == "provider_runtime_event"]
    violations = direct_execution_violations(runtime_events)
    broker_request_count = sum(
        1 for event in runtime_events if event.get("event_type") == "broker_request"
    )
    broker_result_count = sum(
        1 for event in runtime_events if event.get("event_type") == "broker_result"
    )
    validation_signal_count = sum(
        1 for event in runtime_events if event.get("event_type") == "validation_signal"
    )
    gpu_peer_metrics = gpu_peer_exchange_metrics(runtime_events)
    return {
        "schema_version": 1,
        "kind": "provider_runtime_heap_telemetry",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "passed": not violations,
        "errors": [f"direct execution violation: {item}" for item in violations],
        "warnings": [],
        "event_count": len(runtime_events),
        "parse_error_count": snapshot.get("parse_error_count"),
        "lanes_observed": sorted(count_by(runtime_events, "source")),
        "events_by_lane": count_by(runtime_events, "source"),
        "events_by_type": count_by(runtime_events, "event_type"),
        "interaction_edges": count_edges(runtime_events),
        "tool_catalog_exchange_complete_count": correlated_complete(
            runtime_events, "tool_catalog_request", "tool_catalog_response"
        ),
        "gpu1_to_gpu0_event_count": gpu_peer_metrics["gpu1_to_gpu0_event_count"],
        "gpu0_to_gpu1_event_count": gpu_peer_metrics["gpu0_to_gpu1_event_count"],
        "gpu1_gpu0_bidirectional": gpu_peer_metrics["gpu1_gpu0_bidirectional"],
        "gpu1_gpu0_correlated_exchange_count": gpu_peer_metrics[
            "gpu1_gpu0_correlated_exchange_count"
        ],
        "gpu1_gpu0_request_event_types": gpu_peer_metrics["gpu1_gpu0_request_event_types"],
        "gpu1_gpu0_response_event_types": gpu_peer_metrics["gpu1_gpu0_response_event_types"],
        "broker_request_count": broker_request_count,
        "broker_result_count": broker_result_count,
        "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
        "validation_signal_count": validation_signal_count,
        "direct_execution_violation_count": len(violations),
        "tool_catalog_tool_count": safe_dict(snapshot.get("tool_catalog")).get("tool_count"),
        "architecture": snapshot.get("architecture"),
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "direct_tool_execution_allowed": False,
            "broker_required_for_tool_execution": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Runtime Heap Telemetry", ""]
    for key in (
        "passed",
        "stamp",
        "event_count",
        "parse_error_count",
        "tool_catalog_exchange_complete_count",
        "gpu1_to_gpu0_event_count",
        "gpu0_to_gpu1_event_count",
        "gpu1_gpu0_bidirectional",
        "gpu1_gpu0_correlated_exchange_count",
        "broker_request_count",
        "broker_result_count",
        "pending_broker_request_count",
        "validation_signal_count",
        "direct_execution_violation_count",
        "tool_catalog_tool_count",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.extend(["", "## Events by lane", ""])
    for key, value in report.get("events_by_lane", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Events by type", ""])
    for key, value in report.get("events_by_type", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Interaction edges", ""])
    for key, value in report.get("interaction_edges", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp))
    markdown = resolve_output_path(repo_root, args.markdown_output.format(stamp=args.stamp))
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
