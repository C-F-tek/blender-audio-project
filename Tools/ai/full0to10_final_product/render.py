"""Render final Full0To10 product package."""
from __future__ import annotations

from typing import Any


def render_product_markdown(request: str, evidence: dict[str, Any], readiness: dict[str, Any]) -> str:
    lines = [
        "# Full0To10 final tool product",
        "",
        "## Request",
        "",
        request,
        "",
        "## Deliverable scope",
        "",
        "This package is the final-tool-product staging output. It includes SQLite FTS5 evidence, accelerator control, provider governor, invocation dry-run plan, execution bridge, command plan, telemetry contracts, and quality evidence.",
        "",
        "## Evidence index",
        "",
    ]
    for role, record in evidence["artifacts"].items():
        lines.append(f"- `{role}` exists=`{record['exists']}` path=`{record['path']}`")
    lines.extend(
        [
            "",
            "## Provider execution bridge",
            "",
            "The execution bridge is the final non-executing gate before a future real provider run. It creates a command plan and workload output path contract, but performs no provider execution.",
            "",
            "## Real-run status",
            "",
            f"- Ready for product review: `{readiness['ready_for_tool_product_review']}`",
            f"- Ready for real provider run: `{readiness['ready_for_real_provider_run']}`",
            f"- Score: `{readiness['score']}`",
            "",
            "## Blockers",
            "",
        ]
    )
    for blocker in readiness["blockers"] or ["None"]:
        lines.append(f"- {blocker}")
    lines.extend(["", "## Next run", ""])
    lines.append("Next loop can attach the execution bridge to bundle promotion gates, then later add a real-run lane guarded by explicit flags.")
    lines.append("")
    return "\n".join(lines)


def render_readme(manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Full0To10 final tool product package",
            "",
            f"- Passed: `{manifest['passed']}`",
            f"- Product markdown: `{manifest['outputs']['product_markdown']}`",
            f"- Provider invocation plan: `{manifest['outputs'].get('provider_invocation_plan')}`",
            f"- Provider execution bridge: `{manifest['outputs'].get('provider_execution_bridge')}`",
            "",
            "This directory is generated output and should not be committed.",
            "",
        ]
    )
