"""Markdown rendering for runtime file reference reports."""

from __future__ import annotations

from .models import RuntimeFileRef


def render_refs_markdown(title: str, refs: list[RuntimeFileRef]) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Ref count: `{len(refs)}`",
        f"- Patchable verified: `{sum(1 for item in refs if item.patchable)}`",
        f"- Validation only: `{sum(1 for item in refs if item.validation_only)}`",
        f"- Output only: `{sum(1 for item in refs if item.output_only)}`",
        "",
        "## References",
        "",
    ]
    for ref in refs:
        lines.append(
            f"- `{ref.repo_relative or ref.raw}` kind=`{ref.kind}` status=`{ref.status}` provenance=`{ref.provenance}` reason=`{ref.reason}`"
        )
    return "\n".join(lines) + "\n"
