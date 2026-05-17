"""Markdown and JSON helpers for RepoRuntimeUniverse."""

from __future__ import annotations

from .models import RepoRuntimeUniverse


def render_universe_markdown(universe: RepoRuntimeUniverse) -> str:
    summary = universe.summary()
    lines = ["# Repo Runtime Universe", ""]
    for key in (
        "file_count",
        "source_count",
        "docs_count",
        "validation_count",
        "asset_count",
        "output_artifact_count",
        "tool_catalog_count",
        "startup_artifact_ref_count",
    ):
        lines.append(f"- {key}: `{summary.get(key)}`")
    lines.extend(["", "## Top-Level Coverage", ""])
    counts = summary.get("top_level_counts")
    if isinstance(counts, dict):
        for key, value in list(counts.items())[:20]:
            lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Source Samples", ""])
    for item in universe.source_index[:40]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Asset Samples", ""])
    for item in universe.asset_index[:20]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Broker Tool Catalog", ""])
    for item in universe.tool_catalog[:40]:
        lines.append(f"- `{item.get('name')}` args=`{item.get('allowed_args')}`")
    lines.extend(["", "## Startup Artifact Samples", ""])
    for item in (
        universe.tool_catalog_refs
        + universe.memory_inventory_refs
        + universe.context_chunk_refs
        + universe.semantic_chunk_refs
        + universe.startup_manifest_refs
    )[:40]:
        lines.append(f"- `{item}`")
    return "\n".join(lines) + "\n"
