#!/usr/bin/env python3
"""Build an external heap block-pointer manifest from a run directory.

The manifest is external to the gate. It models the heap/universe product
contract as persistent blocks with navigation and refinement pointers:

- previous_block_id / next_block_id for forward continuation;
- refines_block_id for back-refinement;
- resume_from_block_id for continuing after a rewrite;
- role ownership for gpu1_planner, gpu0_reviewer_refiner and npu_auditor.

These pointers are not a side channel: they are the product graph used to recover
old decisions, backtrack, refine, resume, and compose the final long-form heap
answer beyond a single provider token window. Provider execution evidence remains
a separate guardrail flag and must not be inferred from block presence alone.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.runtime.heap_gate.pointer_soft_lock import pointer_closure_summary

from .provider_graph import provider_blocks, provider_rejections

DEFAULT_ROLES = ("gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor")
POINTER_PRODUCT_CONTRACT = {
    "product_contract": True,
    "decision_recovery": True,
    "supports_forward_navigation": True,
    "supports_backrefinement": True,
    "supports_resume": True,
    "provider_execution_is_separate_guardrail": True,
}
EXECUTION_TRUE_PATTERNS = (
    re.compile(
        r"\b(provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)\b\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"[\"'](provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)[\"']\s*:\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(NPU|GPU|provider|workload)[^\n]{0,120}\bperformed\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bperformed\s*=\s*true\b", re.IGNORECASE),
)
EXECUTION_BOOL_KEYS = {
    "provider_execution_performed",
    "gpu0_provider_execution_performed",
    "gpu1_provider_execution_performed",
    "npu_provider_execution_performed",
    "workload_performed",
}
WORKLOAD_CONTAINER_KEYS = {
    "npu_device_workload",
    "gpu_device_workload",
    "device_workload",
    "workload",
}
RESOURCE_MECHANICS_BOOL_KEYS = {
    "resource_mechanics_performed",
    "resource_probe_performed",
    "mechanical_not_static_read",
}


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_text(path: Path, limit: int) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if limit > 0 and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def compact_text(value: Any, limit: int) -> str:
    text = str(value or "")
    if limit > 0 and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def normalize_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def mapping_has_execution_evidence(value: Any, parent_key: str = "") -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            if key_lower in EXECUTION_BOOL_KEYS and normalize_bool(item):
                return True
            if (
                key_lower == "performed"
                and parent_key.lower() in WORKLOAD_CONTAINER_KEYS
                and normalize_bool(item)
            ):
                return True
            if mapping_has_execution_evidence(item, key_text):
                return True
    elif isinstance(value, list):
        return any(mapping_has_execution_evidence(item, parent_key) for item in value)
    return False


def text_has_execution_evidence(text: str) -> bool:
    return any(pattern.search(text) for pattern in EXECUTION_TRUE_PATTERNS)


def provider_execution_evidence(data: dict[str, Any], preview: str) -> bool:
    return mapping_has_execution_evidence(data) or text_has_execution_evidence(preview)


def mapping_has_resource_mechanics(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in RESOURCE_MECHANICS_BOOL_KEYS and normalize_bool(item):
                return True
            if mapping_has_resource_mechanics(item):
                return True
    elif isinstance(value, list):
        return any(mapping_has_resource_mechanics(item) for item in value)
    return False


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def append_block(blocks: list[dict[str, Any]], block: dict[str, Any]) -> None:
    if not any(existing.get("block_id") == block.get("block_id") for existing in blocks):
        blocks.append(block)


def proposal_blocks(repo_root: Path, run_dir: Path, max_block_chars: int) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    proposal_dir = run_dir / "team_context" / "proposal_iterations"
    proposal_files = (
        sorted(proposal_dir.glob("heap_proposal_revision_*.json")) if proposal_dir.exists() else []
    )
    previous_id = ""
    for index, path in enumerate(proposal_files, start=1):
        data = read_json(path)
        md_path = path.with_suffix(".md")
        diagnostic_preview = read_text(md_path if md_path.exists() else path, max_block_chars)
        candidate_preview = compact_text(
            data.get("response_text") or data.get("proposal_text") or "",
            max_block_chars,
        )
        preview = candidate_preview or diagnostic_preview
        block_id = str(data.get("block_id") or "").strip() or stable_id(
            "proposal", f"{repo_rel(repo_root, path)}:{data.get('revision')}:{index}"
        )
        block = {
            "block_id": block_id,
            "block_type": "proposal_chunk",
            "role": "gpu1_planner",
            "step_index": index,
            "revision": data.get("revision"),
            "source_path": repo_rel(repo_root, path),
            "markdown_path": repo_rel(repo_root, md_path) if md_path.exists() else "",
            "previous_block_id": str(data.get("previous_block_id") or previous_id),
            "next_block_id": str(data.get("next_block_id") or ""),
            "refines_block_id": str(
                data.get("refines_block_id")
                or (previous_id if data.get("quality_passed") is not True and previous_id else "")
            ),
            "resume_from_block_id": str(data.get("resume_from_block_id") or previous_id),
            "pointer_action": data.get("pointer_action"),
            "target_files": data.get("target_files") if isinstance(data.get("target_files"), list) else [],
            "exit_decision": data.get("exit_decision"),
            "reject_reason": data.get("reject_reason", ""),
            "gpu1_block_ref": data.get("gpu1_block_ref"),
            "gpu0_review_block_refs": data.get("gpu0_review_block_refs") if isinstance(data.get("gpu0_review_block_refs"), list) else [],
            "npu_audit_block_refs": data.get("npu_audit_block_refs") if isinstance(data.get("npu_audit_block_refs"), list) else [],
            "consumed_block_ids": data.get("consumed_block_ids") if isinstance(data.get("consumed_block_ids"), list) else [],
            "gpu1_closure_decision_packet": data.get("gpu1_closure_decision_packet"),
            "quality_passed": data.get("quality_passed"),
            "accepted": data.get("quality_passed") is True,
            "soft_lock_closure_owner_decision": data.get(
                "soft_lock_closure_owner_decision", ""
            ),
            "gpu0_closure_agreement": data.get("gpu0_closure_agreement", ""),
            "npu_closure_advisory": data.get("npu_closure_advisory", ""),
            "cpu_closure_validation": data.get("cpu_closure_validation", ""),
            "closure_quorum_status": data.get("closure_quorum_status", ""),
            "closure_quorum_reason": data.get("closure_quorum_reason", ""),
            "soft_lock_targeted_refine_used": data.get(
                "soft_lock_targeted_refine_used", False
            ),
            "sha256": (
                hashlib.sha256(preview.encode("utf-8", errors="replace")).hexdigest()
                if preview
                else ""
            ),
            "preview": preview,
            "candidate_response_preview": candidate_preview,
            "diagnostic_preview": diagnostic_preview,
            "preview_source": (
                "candidate_response" if candidate_preview else "diagnostic_markdown"
            ),
            "pointer_contract": {
                "product_contract": True,
                "decision_recovery": True,
                "navigation_role": "proposal_chain",
                "can_continue_to_next": True,
                "can_backrefine": bool(previous_id),
                "requires_review": data.get("quality_passed") is True,
            },
        }
        if previous_id:
            for existing in blocks:
                if existing.get("block_id") == previous_id:
                    existing["next_block_id"] = block_id
        append_block(blocks, block)
        previous_id = block_id
    return blocks


def block_provider_execution_performed(block: dict[str, Any]) -> bool:
    """Return true only for explicit provider/workload execution evidence.

    Pointer blocks are part of the heap product contract and decision-recovery
    graph. Their presence is required for the final product, but it must not be
    used as proof that a provider or hardware workload actually executed.
    """
    if normalize_bool(block.get("provider_execution_performed")):
        return True
    preview = str(block.get("preview") or "")
    return text_has_execution_evidence(preview)


def block_resource_mechanics_performed(block: dict[str, Any]) -> bool:
    """Return true for resource/provider preflight mechanics in pointer blocks."""
    return mapping_has_resource_mechanics(block)


def build_pointer_edges(blocks: list[dict[str, Any]]) -> list[dict[str, str]]:
    ids = {str(block.get("block_id")) for block in blocks}
    edges: list[dict[str, str]] = []
    seen_edges: set[tuple[str, str, str]] = set()
    for block in blocks:
        source = str(block.get("block_id") or "")
        for field, edge_type in (
            ("previous_block_id", "previous"),
            ("next_block_id", "next"),
            ("refines_block_id", "refines"),
            ("resume_from_block_id", "resume_from"),
        ):
            target = str(block.get(field) or "")
            key = (source, target, edge_type)
            if source and target and target in ids and target != source and key not in seen_edges:
                seen_edges.add(key)
                edges.append(
                    {
                        "source_block_id": source,
                        "target_block_id": target,
                        "edge_type": edge_type,
                    }
                )
    return edges


def build_report(
    repo_root: Path, run_dir: Path, max_block_chars: int, max_blocks: int
) -> dict[str, Any]:
    source_proposals = proposal_blocks(repo_root, run_dir, max_block_chars)
    source_providers = provider_blocks(repo_root, run_dir, max_block_chars)
    rejected_providers = provider_rejections(repo_root, run_dir)
    all_blocks = source_proposals + source_providers
    blocks = all_blocks[:max_blocks] if max_blocks > 0 else all_blocks
    edges = build_pointer_edges(blocks)
    pointer_closure = pointer_closure_summary(blocks)
    roles_present = sorted(
        {
            str(block.get("role"))
            for block in blocks
            if block.get("role") and normalize_bool(block.get("provider_role_counted"))
        }
    )
    all_roles_present = sorted(
        {
            str(block.get("role"))
            for block in all_blocks
            if block.get("role") and normalize_bool(block.get("provider_role_counted"))
        }
    )
    roles_verified = sorted(
        {
            str(block.get("role"))
            for block in source_providers
            if block.get("role") and normalize_bool(block.get("provider_role_counted"))
        }
    )
    invalid_roles = sorted(
        {
            str(item.get("provider_role"))
            for item in rejected_providers
            if item.get("provider_role") and normalize_bool(item.get("provider_role_observed"))
        }
    )
    roles_observed = sorted(set(roles_verified) | set(invalid_roles))
    roles_observed_invalid = invalid_roles
    accepted_blocks = [block for block in blocks if block.get("accepted") is True]
    rejected_blocks = [
        block
        for block in blocks
        if block.get("block_type") == "proposal_chunk" and block.get("accepted") is not True
    ]
    latest_proposal = source_proposals[-1] if source_proposals else {}
    all_accepted_blocks = [block for block in all_blocks if block.get("accepted") is True]
    all_rejected_blocks = [
        block
        for block in all_blocks
        if block.get("block_type") == "proposal_chunk" and block.get("accepted") is not True
    ]
    provider_mode_observed = bool(source_providers or rejected_providers)
    provider_roles = set(roles_verified)
    unlinked_peer_blocks = [
        block.get("block_id")
        for block in source_providers
        if block.get("role") in {"gpu0_reviewer_refiner", "npu_auditor"}
        and not block.get("refines_block_id")
    ]
    provider_execution_performed = any(
        normalize_bool(block.get("provider_work_verified")) for block in source_providers
    )
    resource_mechanics_performed = any(
        block_resource_mechanics_performed(block) for block in all_blocks
    )
    resource_mechanics_block_count = sum(
        1 for block in all_blocks if block_resource_mechanics_performed(block)
    )
    provider_missing_roles = sorted(set(DEFAULT_ROLES) - set(roles_observed))
    provider_unverified_roles = sorted((set(DEFAULT_ROLES) & set(roles_observed)) - provider_roles)
    provider_rejection_reasons = sorted(
        {
            str(item.get("provider_rejection_reason") or "")
            for item in rejected_providers
            if str(item.get("provider_rejection_reason") or "").strip()
        }
    )
    provider_graph_recoverable = bool(
        provider_mode_observed
        and not provider_missing_roles
        and not provider_unverified_roles
        and int(len(edges)) > 0
        and provider_execution_performed
        and not unlinked_peer_blocks
    )
    proposal_graph_product_passed = bool(source_proposals)
    errors: list[str] = []
    warnings: list[str] = []
    if not source_proposals and provider_graph_recoverable:
        warnings.append("provider graph recoverable but no proposal chunk")
    elif not source_proposals:
        errors.append("proposal_block_count is zero")
    if source_proposals and not edges:
        errors.append("edge_count is zero")
    if provider_mode_observed:
        if provider_missing_roles:
            errors.append(f"provider roles missing from graph: {provider_missing_roles}")
        if provider_unverified_roles:
            errors.append(f"provider roles observed but not verified: {provider_unverified_roles}")
        if provider_rejection_reasons:
            errors.append("provider work rejected: " + ",".join(provider_rejection_reasons))
        if unlinked_peer_blocks:
            errors.append(f"provider peer blocks lack refines edge: {unlinked_peer_blocks}")
    proposal_graph_product_passed = proposal_graph_product_passed and not errors
    final_product_passed = proposal_graph_product_passed and not provider_graph_recoverable
    return {
        "schema_version": 1,
        "kind": "external_heap_block_pointer_manifest",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "run_dir": repo_rel(repo_root, run_dir),
        "protocol": "external_heap_block_pointer_v1",
        "passed": not errors,
        "proposal_graph_product_passed": proposal_graph_product_passed,
        "provider_graph_recoverable": provider_graph_recoverable,
        "final_product_passed": final_product_passed,
        "pointer_product_contract": POINTER_PRODUCT_CONTRACT,
        "pointer_contract_role": "product_graph_decision_recovery_and_long_response_composition",
        "provider_execution_semantics": "separate_guardrail_true_only_with_explicit_provider_or_workload_evidence",
        "provider_work_semantics": (
            "provider role counts only when provider_work_verified=true; NPU peer evidence "
            "counts when npu_peer_evidence_verified=true, while native tool-loop timeout "
            "remains runtime feedback unless npu_native_tool_loop_required=true"
        ),
        "resource_mechanics_semantics": "separate_counter_true_for_resource_or_provider_preflight_mechanics",
        "roles_expected": list(DEFAULT_ROLES),
        "roles_present": roles_present,
        "all_roles_present": all_roles_present,
        "roles_observed": roles_observed,
        "roles_verified": roles_verified,
        "roles_observed_invalid": roles_observed_invalid,
        "invalid_roles": invalid_roles,
        "provider_missing_roles": provider_missing_roles,
        "provider_unverified_roles": provider_unverified_roles,
        "provider_verified_count": len(source_providers),
        "provider_rejected_count": len(rejected_providers),
        "provider_rejections": rejected_providers,
        "provider_rejection_reasons": provider_rejection_reasons,
        "block_count": len(blocks),
        "source_block_count": len(all_blocks),
        "max_blocks_applied": max_blocks > 0 and len(all_blocks) > len(blocks),
        "edge_count": len(edges),
        "accepted_block_count": len(accepted_blocks),
        "source_accepted_block_count": len(all_accepted_blocks),
        "rejected_proposal_block_count": len(rejected_blocks),
        "source_rejected_proposal_block_count": len(all_rejected_blocks),
        "has_forward_pointers": any(edge.get("edge_type") == "next" for edge in edges),
        "has_backrefinement_pointers": any(edge.get("edge_type") == "refines" for edge in edges),
        "has_resume_pointers": any(edge.get("edge_type") == "resume_from" for edge in edges),
        "blocks": blocks,
        "edges": edges,
        **pointer_closure,
        "soft_lock_closure_owner_decision": latest_proposal.get(
            "soft_lock_closure_owner_decision", ""
        ),
        "gpu0_closure_agreement": latest_proposal.get("gpu0_closure_agreement", ""),
        "npu_closure_advisory": latest_proposal.get("npu_closure_advisory", ""),
        "cpu_closure_validation": latest_proposal.get("cpu_closure_validation", ""),
        "closure_quorum_status": latest_proposal.get("closure_quorum_status", ""),
        "closure_quorum_reason": latest_proposal.get("closure_quorum_reason", ""),
        "soft_lock_targeted_refine_used": latest_proposal.get(
            "soft_lock_targeted_refine_used", False
        ),
        "provider_execution_performed": provider_execution_performed,
        "resource_mechanics_performed": resource_mechanics_performed,
        "resource_probe_performed": any(
            normalize_bool(block.get("resource_probe_performed")) for block in all_blocks
        ),
        "resource_mechanics_block_count": resource_mechanics_block_count,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "provider_mode_observed": provider_mode_observed,
        "unlinked_peer_blocks": unlinked_peer_blocks,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    try:
        from ia_carmine._shared.external_heap_block_pointer_manifest_cli import main as cli_main
    except ModuleNotFoundError:
        from ia_carmine._shared.external_heap_block_pointer_manifest_cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
