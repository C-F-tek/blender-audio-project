"""Markdown rendering for runtime tool broker reports."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Runtime Tool Broker", ""]
    for key in (
        "passed",
        "dry_run",
        "request_file",
        "request_kind",
        "source",
        "source_classification",
        "tool_request_count",
        "tool_execution_count",
        "blocked_tool_count",
        "failed_tool_count",
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
        "sqlite_write_performed",
        "persistent_memory_write_performed",
        "operational_sqlite_write_performed",
        "operational_sqlite_write_count",
        "operational_memory_clear_count",
        "blender_runtime_execution_performed",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.append("")
    lines.append("## Tool results")
    lines.append("")
    for item in report.get("tool_results", []):
        lines.append(f"### `{item.get('id')}` — `{item.get('tool')}`")
        lines.append("")
        lines.append(f"- Executed: `{item.get('executed')}`")
        lines.append(f"- Blocked: `{item.get('blocked')}`")
        lines.append(f"- Return code: `{item.get('returncode')}`")
        lines.append(f"- Outputs: `{item.get('outputs')}`")
        if item.get("errors"):
            lines.append(f"- Errors: `{item.get('errors')}`")
        lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    for key, value in report.get("guardrails", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"
