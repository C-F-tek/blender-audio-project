"""Markdown renderer for NPU knowledge broker packets."""

from __future__ import annotations

from typing import Any

def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# NPU Knowledge Broker Packet",
        "",
        f"- Objective: {packet['objective']}",
        f"- NPU role: `{packet['npu_role']}`",
        f"- Apply mode: `{packet['apply_mode']}`",
        f"- Provider execution performed: `{packet['provider_execution_performed']}`",
        f"- NPU promoted to advisory: `{packet['npu_promoted_to_advisory']}`",
        f"- Candidate count: `{packet['candidate_count']}`",
        "",
        "## Candidate context",
        "",
    ]
    for item in packet["candidate_context"]:
        lines.append(f"### {item['path']}")
        lines.append(f"- Score: `{item['score']}`")
        lines.append(f"- Sources: `{', '.join(item['sources'])}`")
        if item.get("matched_terms"):
            lines.append(f"- Matched terms: `{', '.join(item['matched_terms'])}`")
        lines.append("- Reasons:")
        for reason in item.get("reasons", []):
            lines.append(f"  - {reason}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
