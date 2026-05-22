"""Pointer-graph reconstruction contract for final heap products."""

from __future__ import annotations

from typing import Any


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def build_pointer_reconstruction(pointer: dict[str, Any], revision: dict[str, Any]) -> dict[str, Any]:
    blocks = [block for block in _list(pointer.get("blocks")) if isinstance(block, dict)]
    edges = [edge for edge in _list(pointer.get("edges")) if isinstance(edge, dict)]
    roles = {str(block.get("role") or "") for block in blocks}
    proposal_blocks = [
        block for block in blocks if str(block.get("block_type") or "") == "proposal_chunk"
    ]
    provider_blocks = [
        block for block in blocks if str(block.get("block_type") or "") != "proposal_chunk"
    ]
    latest = blocks[-1] if blocks else {}
    resume_block = str(revision.get("resume_from_block_id") or latest.get("resume_from_block_id") or "")
    errors: list[str] = []
    if not pointer:
        errors.append("pointer manifest missing")
    if not blocks:
        errors.append("pointer manifest has no blocks")
    if not edges:
        errors.append("pointer manifest has no graph edges")
    for role in ("gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"):
        if role not in roles:
            errors.append(f"pointer reconstruction missing role {role}")
    if not resume_block:
        errors.append("pointer reconstruction missing resume_from_block_id")
    if int(revision.get("linked_gpu0_block_count") or 0) <= 0:
        errors.append("pointer reconstruction has no linked GPU0 block")
    if int(revision.get("linked_npu_block_count") or 0) <= 0:
        errors.append("pointer reconstruction has no linked NPU block")
    return {
        "schema_version": 1,
        "kind": "heap_final_pointer_reconstruction",
        "passed": not errors,
        "performed": bool(blocks and edges),
        "source": "external_heap_block_pointer_manifest+external_heap_revision_context",
        "pointer_protocol": pointer.get("protocol"),
        "pointer_manifest_passed": pointer.get("passed"),
        "revision_context_passed": revision.get("passed"),
        "revision_context_operational": revision.get("operational_revision_context"),
        "block_count": len(blocks),
        "edge_count": len(edges),
        "proposal_block_count": len(proposal_blocks),
        "provider_block_count": len(provider_blocks),
        "roles_present": sorted(role for role in roles if role),
        "resume_from_block_id": resume_block,
        "latest_block_id": str(latest.get("block_id") or ""),
        "provider_execution_performed": _truthy(pointer.get("provider_execution_performed")),
        "contract": {
            "final_product_reconstructed_from_pointer_graph": True,
            "final_code_product_composed_from_pointer_graph": True,
            "composition_mode": "compose_refine_resume_pointer_graph",
            "provider_text_is_evidence_not_product": True,
            "resume_refines_previous_edges_required": True,
            "single_run_not_single_direction": True,
        },
        "errors": errors,
    }
