#!/usr/bin/env python3
"""Build compact runtime-flow evidence from IA-Carmine reports.

This is a semantic flow-map builder, not a profiler. Heavy traces such as
VizTracer, pyinstrument, Nsight or OpenTelemetry exports can remain under
output/** and be summarized into the compact JSON/MD/MMD artifacts produced by
this tool.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.validation.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:
    import sys

    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

DEFAULT_OUTPUT_DIR = "docs/LOCAL_VALIDATION_EVIDENCE"
DEFAULT_ENTRYPOINT = "tools/ai/run_agent_gpu_npu_parallel_orchestrator.py"
STAMP_RE = re.compile(r"\d{8}-\d{6}")

CANONICAL_COMPONENTS = {
    "orchestrator": {"type": "process", "label": "orchestrator"},
    "gpu_planner": {"type": "provider", "label": "GPU1 / Ollama planner"},
    "gpu0_peer": {"type": "provider", "label": "GPU0 / OpenVINO peer"},
    "npu_peer": {"type": "provider", "label": "NPU / OpenVINO micro-peer"},
    "broker": {"type": "broker", "label": "runtime tool broker"},
    "heap": {"type": "exchange_memory", "label": "runtime heap / exchange"},
    "decision_loop": {"type": "decision", "label": "decision loop"},
    "recommendations": {"type": "artifact", "label": "recommendations"},
    "patch_plan": {"type": "artifact", "label": "patch plan"},
    "validation": {"type": "validator", "label": "validation"},
    "evidence_bundle": {"type": "artifact", "label": "evidence bundle"},
}


def now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
    except ValueError:
        return str(path)


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def infer_stamp(values: list[str]) -> str:
    for value in values:
        matches = STAMP_RE.findall(str(value or ""))
        if matches:
            return matches[-1]
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if isinstance(value, bool):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    if not path.exists():
        return {}, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (
        Exception
    ) as exc:  # noqa: BLE001 - evidence summary should capture parse failures.
        return {}, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return {}, "json root is not an object"
    return data, ""


def component_from_report(path: str, data: dict[str, Any]) -> str:
    lower_path = path.lower().replace("\\", "/")
    kind = str(data.get("kind") or "").lower()
    if (
        "runtime_heap" in kind
        or "ai_runtime_heap" in lower_path
        or "heap" in lower_path
    ):
        return "heap"
    if "orchestrator" in kind or "orchestrator" in lower_path:
        return "orchestrator"
    if (
        "parallel_gpu" in lower_path
        or "gpu_deep" in lower_path
        or "gpu_planner" in lower_path
    ):
        return "gpu_planner"
    if "gpu0" in lower_path or "openvino_gpu0" in kind:
        return "gpu0_peer"
    if "npu" in lower_path or "npu" in kind:
        return "npu_peer"
    if "broker" in kind or "broker" in lower_path or "runtime_tool" in lower_path:
        return "broker"
    if "decision" in kind or "decision_loop" in lower_path:
        return "decision_loop"
    if (
        "patch_plan" in kind
        or "patch_plan" in lower_path
        or "patch_specs" in lower_path
    ):
        return "patch_plan"
    if (
        "recommend" in kind
        or "proposal" in kind
        or "recommend" in lower_path
        or "proposal" in lower_path
    ):
        return "recommendations"
    if "bundle" in kind or "evidence_bundle" in lower_path:
        return "evidence_bundle"
    if "validation" in lower_path or kind.startswith("check_"):
        return "validation"
    return "validation"


def add_node(
    nodes: dict[str, dict[str, Any]],
    node_id: str,
    node_type: str,
    label: str,
    **extra: Any,
) -> None:
    item = nodes.setdefault(
        "node:" + node_id, {"id": node_id, "type": node_type, "label": label}
    )
    item.update(
        {key: value for key, value in extra.items() if value not in (None, "", [])}
    )


def add_edge(
    edges: dict[tuple[str, str, str], dict[str, Any]],
    source: str,
    target: str,
    kind: str,
    count: int = 1,
    **extra: Any,
) -> None:
    key = (source, target, kind)
    item = edges.setdefault(
        key, {"from": source, "to": target, "kind": kind, "count": 0}
    )
    item["count"] = safe_int(item.get("count")) + max(1, count)
    for extra_key, value in extra.items():
        if value not in (None, "", []):
            item[extra_key] = value


def append_event(
    events: list[dict[str, Any]],
    *,
    component: str,
    action: str,
    status: str = "observed",
    span: str = "",
    duration_ms: int | None = None,
    **extra: Any,
) -> None:
    event: dict[str, Any] = {
        "ts": now_iso(),
        "span": span,
        "component": component,
        "action": action,
        "status": status,
    }
    if duration_ms is not None:
        event["duration_ms"] = duration_ms
    event.update(
        {key: value for key, value in extra.items() if value not in (None, "", [])}
    )
    events.append(event)


def compact_report_summary(
    path: str, data: dict[str, Any], parse_error: str
) -> dict[str, Any]:
    return {
        "path": path,
        "exists": parse_error != "missing",
        "json_ok": not parse_error,
        "parse_error": parse_error,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "patch_application_performed": data.get("patch_application_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "errors": as_list(data.get("errors"))[:10],
        "warnings": as_list(data.get("warnings"))[:10],
    }


def process_report(
    *,
    repo_root: Path,
    path: Path,
    data: dict[str, Any],
    parse_error: str,
    nodes: dict[str, dict[str, Any]],
    edges: dict[tuple[str, str, str], dict[str, Any]],
    events: list[dict[str, Any]],
    counters: Counter[str],
) -> dict[str, Any]:
    rel = repo_rel(path, repo_root)
    component = component_from_report(rel, data)
    report_node = f"report:{rel}"
    add_node(nodes, report_node, "report", rel, path=rel, kind=data.get("kind"))
    add_edge(edges, component, report_node, "emits_report", 1)
    append_event(
        events,
        component=component,
        action="report_observed",
        status="error" if parse_error else "ok",
        span=rel,
        report_path=rel,
        kind=data.get("kind"),
    )

    if parse_error:
        counters["parse_error_count"] += 1
        return compact_report_summary(rel, data, parse_error)

    counters["report_count"] += 1
    if data.get("passed") is False:
        counters["failed_report_count"] += 1

    round_count = safe_int(
        data.get("round_count")
        or data.get("gpu_round_count")
        or len(as_list(data.get("rounds")))
    )
    if round_count:
        counters["round_count"] = max(counters["round_count"], round_count)
        add_edge(edges, "orchestrator", "gpu_planner", "round_loop", round_count)

    recommendation_count = safe_int(
        data.get("recommendation_count")
        or data.get("gpu_recommendation_count")
        or data.get("proposal_count")
    )
    if recommendation_count:
        counters["recommendation_count"] += recommendation_count
        add_edge(edges, component, "recommendations", "produces", recommendation_count)
        append_event(
            events,
            component=component,
            action="recommendation",
            status="observed",
            span=rel,
            count=recommendation_count,
        )

    patch_plan_count = safe_int(
        data.get("patch_plan_count") or len(as_list(data.get("patch_plans")))
    )
    if patch_plan_count:
        counters["patch_plan_count"] += patch_plan_count
        add_edge(edges, component, "patch_plan", "produces", patch_plan_count)
        append_event(
            events,
            component=component,
            action="patch_plan",
            status="observed",
            span=rel,
            count=patch_plan_count,
        )

    tool_request_count = safe_int(
        data.get("tool_request_count") or data.get("requested_tool_count")
    )
    tool_execution_count = safe_int(data.get("tool_execution_count"))
    if tool_request_count:
        counters["tool_request_count"] += tool_request_count
        add_edge(edges, component, "broker", "tool_request", tool_request_count)
        append_event(
            events,
            component=component,
            action="tool_request",
            status="observed",
            span=rel,
            count=tool_request_count,
        )
    if tool_execution_count:
        counters["tool_execution_count"] += tool_execution_count
        add_edge(edges, "broker", component, "tool_result", tool_execution_count)
        append_event(
            events,
            component="broker",
            action="tool_execution",
            status="observed",
            span=rel,
            count=tool_execution_count,
        )

    if data.get("provider_execution_performed") is True:
        counters["provider_call_count"] += 1
        append_event(
            events, component=component, action="provider_call", status="ok", span=rel
        )

    heap_event_count = safe_int(data.get("event_count"))
    by_lane = as_dict(data.get("by_lane"))
    if heap_event_count or by_lane:
        counters["heap_event_count"] += heap_event_count
        for lane, lane_data in by_lane.items():
            lane_component = {
                "gpu1": "gpu_planner",
                "gpu0": "gpu0_peer",
                "npu": "npu_peer",
                "broker": "broker",
                "orchestrator": "orchestrator",
                "deterministic": "validation",
            }.get(str(lane), str(lane))
            event_count = safe_int(as_dict(lane_data).get("event_count"), 1)
            add_edge(edges, lane_component, "heap", "heap_write", event_count)
            counters["heap_write_count"] += event_count
        append_event(
            events,
            component="heap",
            action="heap_snapshot",
            status="observed",
            span=rel,
            count=heap_event_count,
        )

    for round_item in as_list(data.get("rounds"))[:200]:
        if not isinstance(round_item, dict):
            continue
        round_id = safe_int(round_item.get("round"))
        span = f"round_{round_id:03d}" if round_id >= 0 else rel
        json_ok = round_item.get("json_ok")
        status = "ok" if json_ok is True or json_ok is None else "error"
        append_event(
            events, component=component, action="round", status=status, span=span
        )

    return compact_report_summary(rel, data, parse_error)


def build_markdown(flow: dict[str, Any]) -> str:
    summary = as_dict(flow.get("summary"))
    lines = ["# IA-Carmine Runtime Flow", ""]
    lines.append(f"- Stamp: `{flow.get('stamp')}`")
    lines.append(f"- Entrypoint: `{flow.get('entrypoint')}`")
    lines.append(f"- Node count: `{len(as_list(flow.get('nodes')))}`")
    lines.append(f"- Edge count: `{len(as_list(flow.get('edges')))}`")
    lines.append(f"- Event count: `{len(as_list(flow.get('events')))}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    for key in sorted(summary):
        lines.append(f"- `{key}`: `{summary[key]}`")
    lines.append("")
    lines.append("## Nodes")
    lines.append("")
    lines.append("| id | type | label |")
    lines.append("|---|---|---|")
    for node in as_list(flow.get("nodes")):
        if isinstance(node, dict):
            lines.append(
                f"| `{node.get('id')}` | `{node.get('type')}` | {node.get('label') or ''} |"
            )
    lines.append("")
    lines.append("## Edges")
    lines.append("")
    lines.append("| from | to | kind | count |")
    lines.append("|---|---|---|---:|")
    for edge in as_list(flow.get("edges")):
        if isinstance(edge, dict):
            lines.append(
                f"| `{edge.get('from')}` | `{edge.get('to')}` | `{edge.get('kind')}` | {edge.get('count') or 0} |"
            )
    lines.append("")
    lines.append("## Reports")
    lines.append("")
    for report in as_list(flow.get("reports")):
        if isinstance(report, dict):
            lines.append(
                f"- `{report.get('path')}` kind=`{report.get('kind')}` passed=`{report.get('passed')}` json_ok=`{report.get('json_ok')}`"
            )
    lines.append("")
    return "\n".join(lines)


def mermaid_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def build_mermaid(flow: dict[str, Any]) -> str:
    lines = ["flowchart TD"]
    for node in as_list(flow.get("nodes")):
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("id") or "node")
        label = str(node.get("label") or node_id).replace('"', "'")
        lines.append(f'  {mermaid_id(node_id)}["{label}"]')
    for edge in as_list(flow.get("edges")):
        if not isinstance(edge, dict):
            continue
        src = mermaid_id(str(edge.get("from") or "unknown"))
        dst = mermaid_id(str(edge.get("to") or "unknown"))
        kind = str(edge.get("kind") or "flow")
        count = edge.get("count") or 0
        lines.append(f"  {src} -->|{kind}: {count}| {dst}")
    return "\n".join(lines) + "\n"


def write_jsonl(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


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
        "decision_count": sum(
            1 for event in events if event.get("action") == "decision"
        ),
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--entrypoint", default=DEFAULT_ENTRYPOINT)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default="")
    parser.add_argument("--report", action="append", default=[])
    parser.add_argument("--output", default="")
    parser.add_argument("--jsonl-output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--mermaid-output", default="")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    flow = build_flow(args)
    stamp = str(flow["stamp"])
    basename = args.basename or f"runtime_flow_{stamp}"
    output_dir = resolve_output_path(repo_root, args.output_dir)
    json_output = (
        resolve_output_path(repo_root, args.output)
        if args.output
        else output_dir / f"{basename}.json"
    )
    jsonl_output = (
        resolve_output_path(repo_root, args.jsonl_output)
        if args.jsonl_output
        else output_dir / f"{basename}.jsonl"
    )
    md_output = (
        resolve_output_path(repo_root, args.markdown_output)
        if args.markdown_output
        else output_dir / f"{basename}.md"
    )
    mmd_output = (
        resolve_output_path(repo_root, args.mermaid_output)
        if args.mermaid_output
        else output_dir / f"{basename}.mmd"
    )

    write_json_report(flow, json_output)
    write_jsonl(jsonl_output, as_list(flow.get("events")))
    write_text_report(build_markdown(flow), md_output)
    write_text_report(build_mermaid(flow), mmd_output)

    result = {
        "passed": True,
        "kind": "ia_carmine_runtime_flow_build",
        "stamp": stamp,
        "json": str(json_output),
        "jsonl": str(jsonl_output),
        "markdown": str(md_output),
        "mermaid": str(mmd_output),
        "summary": flow.get("summary"),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
