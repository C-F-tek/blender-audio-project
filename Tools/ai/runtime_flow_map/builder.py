"""Flow-map report builder."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from tools.validation.report_utils import resolve_output_path

from .common import (
    CANONICAL_COMPONENTS,
    add_edge,
    add_node,
    infer_stamp,
    now_iso,
    read_json,
)
from .process import process_report

def build_flow(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    report_values = [str(item) for item in args.report]
    stamp = args.stamp or infer_stamp(report_values)

    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[tuple[str, str, str], dict[str, Any]] = {}
    events: list[dict[str, Any]] = []
    counters: Counter[str] = Counter()
    reports: list[dict[str, Any]] = []

    for node_id, meta in CANONICAL_COMPONENTS.items():
        add_node(nodes, node_id, str(meta["type"]), str(meta["label"]))

    add_edge(edges, "orchestrator", "heap", "exchange_in", 1)
    add_edge(edges, "heap", "gpu_planner", "context_read", 1)
    add_edge(edges, "gpu_planner", "gpu0_peer", "peer_request", 1)
    add_edge(edges, "gpu_planner", "npu_peer", "microtask_request", 1)
    add_edge(edges, "gpu_planner", "decision_loop", "decision", 1)
    add_edge(edges, "decision_loop", "patch_plan", "patch_plan", 1)
    add_edge(edges, "patch_plan", "validation", "validation", 1)

    for raw_report in args.report:
        path = resolve_output_path(repo_root, raw_report)
        data, parse_error = read_json(path)
        reports.append(
            process_report(
                repo_root=repo_root,
                path=path,
                data=data,
                parse_error=parse_error,
                nodes=nodes,
                edges=edges,
                events=events,
                counters=counters,
            )
        )

    summary = {
        "report_count": counters["report_count"],
        "parse_error_count": counters["parse_error_count"],
        "failed_report_count": counters["failed_report_count"],
        "round_count": counters["round_count"],
        "provider_call_count": counters["provider_call_count"],
        "tool_request_count": counters["tool_request_count"],
        "tool_execution_count": counters["tool_execution_count"],
        "heap_event_count": counters["heap_event_count"],
        "heap_read_count": counters["heap_read_count"],
        "heap_write_count": counters["heap_write_count"],
        "decision_count": sum(1 for event in events if event.get("action") == "decision"),
        "recommendation_count": counters["recommendation_count"],
        "patch_plan_count": counters["patch_plan_count"],
    }

    return {
        "schema_version": 1,
        "kind": "ia_carmine_runtime_flow",
        "generated_at": now_iso(),
        "stamp": stamp,
        "entrypoint": args.entrypoint,
        "nodes": sorted(nodes.values(), key=lambda item: str(item.get("id"))),
        "edges": sorted(
            edges.values(),
            key=lambda item: (
                str(item.get("from")),
                str(item.get("to")),
                str(item.get("kind")),
            ),
        ),
        "events": events,
        "reports": reports,
        "summary": summary,
        "guardrails": {
            "raw_trace_embedded": False,
            "large_runtime_artifacts_embedded": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
