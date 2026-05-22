"""Evidence fallback plan builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine._shared.evidence_item_planning import (
    doc_code_item_or_skip,
    doc_code_strategy_parts,
    doc_doc_item_or_skip,
    doc_doc_strategy_text,
    iter_sufficient_area_items,
)

from .common import DEFAULT_VALIDATION_COMMANDS, compact_evidence_files, target_path_error

def plan_from_doc_code_item(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    audit_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    evidence_item, skip = doc_code_item_or_skip(
        item=item,
        index=index,
        repo_root=repo_root,
        id_prefix="fallback_doc_code",
        target_path_error=target_path_error,
        missing_reason="doc_code item has no source doc",
    )
    if skip or evidence_item is None:
        return None, skip
    strategy_bits = doc_code_strategy_parts(
        reference=evidence_item.reference,
        doc=evidence_item.doc,
        existing_candidate=evidence_item.existing_candidate,
        candidates=evidence_item.candidates,
        opening="Patch the source Markdown only; do not create missing code/runtime files from this fallback.",
        inspect_template=(
            "Review the referenced path `{reference}` and decide whether it is stale, "
            "intentionally future-facing, or should point to an existing artifact."
        ),
        existing_template=(
            "Existing candidate `{existing_candidate}` was detected; prefer link normalization over new content."
        ),
        candidate_limit=8,
    )
    return (
        {
            "id": f"fallback_doc_code_{index:03d}",
            "source": "evidence_sufficiency_fallback",
            "area": "doc_code",
            "status": "ready_for_manual_review",
            "target_files": [evidence_item.doc],
            "rationale": item.get("reason")
            or "Evidence report marks this doc/code reference as sufficient for manual patch planning.",
            "edit_strategy": " ".join(strategy_bits),
            "risk": "low",
            "validation_commands": DEFAULT_VALIDATION_COMMANDS,
            "stop_conditions": [
                "Stop if the reference actually exists after refreshing the branch.",
                "Stop if the fix requires creating runtime code instead of correcting documentation.",
                "Stop if the edit would touch output/**, generated indexes, full analysis JSON, or Blender runtime behavior.",
            ],
            "source_evidence": {
                "evidence_area": "doc_code",
                "reference": evidence_item.reference,
                "candidate_references": evidence_item.candidates,
                "existing_candidate": evidence_item.existing_candidate or None,
                "confidence": item.get("confidence"),
                "evidence_files": compact_evidence_files(item),
                "npu_audit_refs": audit_refs,
            },
            "manual_review_required": True,
        },
        None,
    )

def plan_from_doc_doc_item(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    audit_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    evidence_item, skip = doc_doc_item_or_skip(
        item=item,
        index=index,
        repo_root=repo_root,
        id_prefix="fallback_doc_doc",
        target_path_error=target_path_error,
        missing_reason="doc_doc item has no target path",
        term_limit=12,
        terms_fallback="the missing explicit terms",
    )
    if skip or evidence_item is None:
        return None, skip
    return (
        {
            "id": f"fallback_doc_doc_{index:03d}",
            "source": "evidence_sufficiency_fallback",
            "area": "doc_doc",
            "status": "ready_for_manual_review",
            "target_files": [evidence_item.path],
            "rationale": item.get("reason")
            or "Evidence report marks this documentation cross-reference as sufficient.",
            "edit_strategy": doc_doc_strategy_text(
                evidence_item.terms_text,
                lead="Add a small targeted cross-reference for",
            ),
            "risk": "low",
            "validation_commands": DEFAULT_VALIDATION_COMMANDS,
            "stop_conditions": [
                "Stop if the missing terms are already present after refreshing the branch.",
                "Stop if the change duplicates entire contract documents instead of adding a narrow cross-reference.",
                "Stop if the edit would touch generated output or runtime files.",
            ],
            "source_evidence": {
                "evidence_area": "doc_doc",
                "missing_terms": evidence_item.missing_terms,
                "confidence": item.get("confidence"),
                "evidence_files": compact_evidence_files(item),
                "npu_audit_refs": audit_refs,
            },
            "manual_review_required": True,
        },
        None,
    )

def fallback_plans_from_evidence(
    *,
    evidence: dict[str, Any],
    repo_root: Path,
    audit_refs: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []

    for index, item in iter_sufficient_area_items(evidence, "doc_code"):
        plan, skip = plan_from_doc_code_item(
            item=item, index=index, repo_root=repo_root, audit_refs=audit_refs
        )
        if plan:
            plans.append(plan)
        if skip:
            skipped.append(skip)

    for index, item in iter_sufficient_area_items(evidence, "doc_doc"):
        plan, skip = plan_from_doc_doc_item(
            item=item, index=index, repo_root=repo_root, audit_refs=audit_refs
        )
        if plan:
            plans.append(plan)
        if skip:
            skipped.append(skip)

    return plans, skipped
