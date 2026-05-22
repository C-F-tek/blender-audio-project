"""Report rendering for local AI resource lane checks."""

from __future__ import annotations

from typing import Any

RESOURCE_MECHANICS_SEMANTICS = (
    "resource_provider_preflight_can_touch_runtime_services_or_device_enumeration"
)


def unavailable_lane(
    name: str, kind: str, message: str, *, elapsed_sec: float = 0.0
) -> dict[str, Any]:
    return {
        "lane": name,
        "kind": kind,
        "passed": False,
        "ready": False,
        "available": False,
        "provider_execution_performed": False,
        "resource_probe_performed": False,
        "resource_mechanics_semantics": RESOURCE_MECHANICS_SEMANTICS,
        "elapsed_sec": round(elapsed_sec, 4),
        "report": {"errors": [], "warnings": [message]},
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Local AI Resource Lanes", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Parallel: `{report['parallel']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Resource mechanics performed: `{report['resource_mechanics_performed']}`")
    lines.append(f"- Resource probe performed: `{report['resource_probe_performed']}`")
    lines.append(f"- Mechanical static read: `{not report['mechanical_not_static_read']}`")
    lines.append(f"- Ready lanes: `{', '.join(report['ready_lanes'])}`")
    lines.append(f"- Available lanes: `{', '.join(report['available_lanes'])}`")
    lines.append("")
    lines.append(
        "| Lane | Ready | Available | Elapsed sec | Provider execution | Resource probe |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|")
    for lane in report["lanes"]:
        lines.append(
            f"| {lane['lane']} | {lane['ready']} | {lane['available']} | "
            f"{lane['elapsed_sec']} | {lane['provider_execution_performed']} | "
            f"{lane.get('resource_probe_performed')} |"
        )
    if report["warnings"]:
        lines.append("\n## Warnings")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    if report["errors"]:
        lines.append("\n## Errors")
        for error in report["errors"]:
            lines.append(f"- {error}")
    lines.append("")
    lines.append("This report is observability-only and app-agnostic.")
    return "\n".join(lines) + "\n"
