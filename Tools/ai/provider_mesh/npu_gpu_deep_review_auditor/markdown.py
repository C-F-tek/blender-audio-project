"""Markdown renderer for NPU/GPU deep review audit reports."""

from __future__ import annotations

from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# NPU GPU Deep Review Audit", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Non-blocking: `{report['non_blocking']}`")
    lines.append(f"- NPU Python: `{report['npu_python']}`")
    lines.append(f"- NPU Python exists: `{report['npu_python_exists']}`")
    lines.append(f"- Provider execution requested: `{report['provider_execution_requested']}`")
    lines.append(f"- Provider load attempted: `{report['provider_load_attempted']}`")
    lines.append(f"- Provider execution succeeded: `{report['provider_execution_succeeded']}`")
    lines.append(f"- Provider empty response: `{report.get('provider_empty_response')}`")
    lines.append(f"- Dependency missing: `{report['dependency_missing']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Classification: `{report['npu_auditor']['classification']}`")
    lines.append(f"- Runtime tool context seen: `{report.get('runtime_tool_context_seen')}`")
    lines.append(
        f"- Runtime tool context report count: `{report.get('runtime_tool_context_report_count')}`"
    )
    lines.append(f"- Tool request count: `{report.get('tool_request_count')}`")
    lines.append(f"- GPU review blocked: `{report['decision']['gpu_review_blocked']}`")
    lines.append("")
    if report["warnings"]:
        lines.append("## Warnings")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")
    lines.append("## Decision")
    for key, value in report["decision"].items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"
