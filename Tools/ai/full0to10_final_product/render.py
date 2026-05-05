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
        "This package is the final-tool-product staging output. It is built from local tools, SQLite FTS5 memory, provider contracts, accelerator control, provider governor, telemetry, and quality evidence. It is not provider-generated text.",
        "",
        "## Evidence index",
        "",
    ]
    for role, record in evidence["artifacts"].items():
        lines.append(f"- `{role}` exists=`{record['exists']}` path=`{record['path']}`")

    lines.extend(
        [
            "",
            "## SQLite memory",
            "",
            "SQLite FTS5 is the deterministic local context layer.",
            "",
            "## Runtime tools",
            "",
            "Runtime tool usage must be represented by JSON telemetry before any real run.",
            "",
            "## GPU/Ollama",
            "",
            "Ollama/GPU is explicit primary advisory only after quality gates and provider governor permit.",
            "",
            "## NPU/OpenVINO",
            "",
            "NPU/OpenVINO remains sampled-auditor/diagnostic. GPU.0 remains secondary unless promoted.",
            "",
            "## Accelerator control",
            "",
            "The package includes GPU body, GPU mind, NPU auditor, GPU.0 contract and scheduler evidence.",
            "",
            "## Provider governor",
            "",
            "The governor produces a run permit decision and budget. This package never executes providers.",
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
    lines.append("Next run should include accelerator control and provider governor evidence, then decide whether generation is allowed.")
    lines.append("")
    return "\n".join(lines)


def render_readme(manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Full0To10 final tool product package",
            "",
            f"- Passed: `{manifest['passed']}`",
            f"- Product markdown: `{manifest['outputs']['product_markdown']}`",
            f"- Evidence index: `{manifest['outputs']['evidence_index']}`",
            f"- Readiness: `{manifest['outputs']['readiness']}`",
            f"- Accelerator control: `{manifest['outputs'].get('accelerator_control')}`",
            f"- Provider governor: `{manifest['outputs'].get('provider_governor')}`",
            "",
            "This directory is generated output and should not be committed.",
            "",
        ]
    )
