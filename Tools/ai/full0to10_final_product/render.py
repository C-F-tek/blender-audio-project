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
        "This package is the final-tool-product staging output. It includes SQLite FTS5 evidence, accelerator control, provider governor, invocation dry-run plan, telemetry contracts, and quality evidence. It is not provider-generated text.",
        "",
        "## Evidence index",
        "",
    ]
    for role, record in evidence["artifacts"].items():
        lines.append(f"- `{role}` exists=`{record['exists']}` path=`{record['path']}`")

    lines.extend(
        [
            "",
            "## Provider invocation plan",
            "",
            "The package includes a dry-run invocation plan, workload report contract, expected telemetry contract, NPU audit hooks and non-executing steps.",
            "",
            "## GPU/Ollama",
            "",
            "Ollama/GPU can only run in a future explicit real-run lane after permit and workload contract are satisfied.",
            "",
            "## NPU/OpenVINO",
            "",
            "NPU is wired as auditor. GPU.0 stays diagnostic/secondary.",
            "",
            "## Readiness",
            "",
            f"- Score: `{readiness['score']}`",
            f"- Ready for product review: `{readiness['ready_for_tool_product_review']}`",
            f"- Ready for real provider run: `{readiness['ready_for_real_provider_run']}`",
            "",
            "## Blockers",
            "",
        ]
    )
    for blocker in readiness["blockers"] or ["None"]:
        lines.append(f"- {blocker}")
    lines.extend(["", "## Next run", ""])
    lines.append("Next loop can attach this dry-run plan to the unified bundle and later introduce a strictly gated real provider invocation.")
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
            f"- Workload contract: `{manifest['outputs'].get('provider_workload_report_contract')}`",
            "",
            "This directory is generated output and should not be committed.",
            "",
        ]
    )
