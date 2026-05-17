"""Markdown rendering for provider runtime blackboard snapshots."""

from __future__ import annotations

from typing import Any

from .common import safe_dict, safe_list

def render_markdown(snapshot: dict[str, Any]) -> str:
    lines = ["# Provider Runtime Heap Snapshot", ""]
    lines.append(f"- Stamp: `{snapshot.get('stamp')}`")
    lines.append(f"- Event count: `{snapshot.get('event_count')}`")
    lines.append(f"- Parse error count: `{snapshot.get('parse_error_count')}`")
    lines.append(f"- Pending broker requests: `{snapshot.get('pending_broker_request_count')}`")
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
