from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    """Render a compact Markdown hardware manifest."""
    lines = [
        "# Runtime hardware capability manifest",
        "",
        f"- Kind: `{report.get('kind')}`",
        f"- Passed: `{report.get('passed')}`",
        f"- Mode: `{report.get('mode')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Patch application performed: `{report.get('patch_application_performed')}`",
        "",
        "## Capabilities",
        "",
        "| Resource | Name | Role | Provider | Status |",
        "|---|---|---|---|---|",
    ]
    for item in report.get("capabilities", []):
        lines.append(
            f"| `{item.get('resource')}` | `{item.get('name')}` | `{item.get('role')}` | "
            f"`{item.get('provider')}` | `{item.get('status')}` |"
        )
    lines.extend(["", "## Warnings", ""])
    warnings = report.get("warnings") or []
    lines.extend([f"- {warning}" for warning in warnings] or ["- none"])
    lines.append("")
    return "\n".join(lines)
