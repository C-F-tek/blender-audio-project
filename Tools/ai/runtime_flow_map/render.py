"""Rendering helpers for runtime flow-map evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import as_dict, as_list

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
