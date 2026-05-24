"""Render the final heap plan product artifact."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine._shared.heap_final_readable_synthesis import (
    as_dict,
    gpu1_raw_evidence_summary,
    matrix_has_applicable_code_product,
    pointer_graph_chain_summary,
    pointer_summary,
    render_pointer_closure_markdown_lines,
    soft_lock_state_from_reports,
)


def render_plan_product_full_patch(
    *,
    run_dir: Path,
    gate: dict[str, Any],
    revision: dict[str, Any],
    pointer: dict[str, Any],
    matrix: dict[str, Any],
    matrix_path: str,
) -> str:
    metrics = as_dict(gate.get("metrics"))
    soft_lock_state = soft_lock_state_from_reports(gate, pointer, revision)
    has_applicable_code_product = matrix_has_applicable_code_product(matrix)
    status = (
        "PATCH_PRODUCT_AVAILABLE"
        if has_applicable_code_product
        else "PLAN_PRODUCT_FULL_PATCH_ONLY"
    )
    lines = [
        "# PLAN_PRODUCT_FULL_PATCH",
        "",
        "Artifact finale della run per piano, pointer graph e prompt/evidenza GPU1 ricostruiti.",
        "Non e' una patch applicata e non sostituisce `CODE_PRODUCT_FULL_PATCH.md` quando esiste un diff verificato.",
        "",
        "## Stato",
        "",
        f"- Plan product status: `{status}`.",
        "- Code product sibling: `CODE_PRODUCT_FULL_PATCH.md`.",
        f"- Matrix target count: `{matrix.get('target_count')}`.",
        f"- Verified target count: `{matrix.get('verified_target_count')}`.",
        f"- Matrix report: `{matrix_path}`.",
        f"- Resume from block: `{revision.get('resume_from_block_id') or ''}`.",
        f"- Latest block id: `{revision.get('latest_block_id') or ''}`.",
        f"- GPU1 block count: `{revision.get('gpu1_block_count') or 0}`.",
        f"- Proposal block count: `{revision.get('proposal_block_count') or 0}`.",
        "",
        "## Catena GPU1 Ricostruita",
        "",
        *[f"- {line}" for line in gpu1_raw_evidence_summary(run_dir)],
        "",
        "## Pointer Graph",
        "",
        *[f"- {line}" for line in pointer_summary(run_dir, revision)],
        "",
        *render_pointer_closure_markdown_lines(soft_lock_state),
        "",
        "## Quorum E Recovery",
        "",
        *[f"- {line}" for line in pointer_graph_chain_summary(metrics, pointer, soft_lock_state)],
        "",
        "## Uso Operativo",
        "",
        "- Questo file e' un prodotto finale di piano/evidenza della run.",
        "- Usarlo per riprendere il pointer graph, ricostruire il prompt GPU1 e guidare recovery/congruence.",
        "- Non applicarlo come diff; applicare solo sezioni patch verificate da `CODE_PRODUCT_FULL_PATCH.md`.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"
