"""Evidence fallback plan builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import DEFAULT_VALIDATION_COMMANDS, compact_evidence_files, normalize_repo_path, target_path_error, unique_strings

def plan_from_doc_code_item(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    audit_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    doc = normalize_repo_path(item.get("doc"))
    if not doc:
        return None, {
            "id": f"fallback_doc_code_{index:03d}",
            "reason": "doc_code item has no source doc",
        }
    error = target_path_error(doc, repo_root)
    if error:
        return None, {
            "id": f"fallback_doc_code_{index:03d}",
            "reason": f"{doc}: {error}",
        }
    reference = normalize_repo_path(item.get("reference"))
    existing_candidate = normalize_repo_path(item.get("existing_candidate"))
    candidates = unique_strings(
        item.get("candidate_references", [])
        if isinstance(item.get("candidate_references"), list)
        else []
    )
    strategy_bits = [
        "Patch the source Markdown only; do not create missing code/runtime files from this fallback.",
        f"Review the referenced path `{reference}` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact.",
    ]
    if existing_candidate:
        strategy_bits.append(
            f"Existing candidate `{existing_candidate}` was detected; prefer link normalization over new content."
        )
    if candidates:
        strategy_bits.append(
            f"Candidate references observed: {', '.join(f'`{candidate}`' for candidate in candidates[:8])}."
        )
    return (
        {
            "id": f"fallback_doc_code_{index:03d}",
            "source": "evidence_sufficiency_fallback",
            "area": "doc_code",
            "status": "ready_for_manual_review",
            "target_files": [doc],
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
                "reference": reference,
                "candidate_references": candidates,
                "existing_candidate": existing_candidate or None,
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
    path = normalize_repo_path(item.get("path"))
    if not path:
        return None, {
            "id": f"fallback_doc_doc_{index:03d}",
            "reason": "doc_doc item has no target path",
        }
    error = target_path_error(path, repo_root)
    if error:
        return None, {
            "id": f"fallback_doc_doc_{index:03d}",
            "reason": f"{path}: {error}",
        }
    missing_terms = (
        [str(term) for term in item.get("missing_terms", []) if str(term).strip()]
        if isinstance(item.get("missing_terms"), list)
        else []
    )
    terms_text = (
        ", ".join(f"`{term}`" for term in missing_terms[:12]) or "the missing explicit terms"
    )
    return (
        {
            "id": f"fallback_doc_doc_{index:03d}",
            "source": "evidence_sufficiency_fallback",
            "area": "doc_doc",
            "status": "ready_for_manual_review",
            "target_files": [path],
            "rationale": item.get("reason")
            or "Evidence report marks this documentation cross-reference as sufficient.",
            "edit_strategy": (
                f"Add a small targeted cross-reference for {terms_text}. "
                "Do not duplicate large contract sections; link or summarize the canonical location instead."
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
                "missing_terms": missing_terms,
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
    areas = evidence.get("areas", {}) if isinstance(evidence.get("areas"), dict) else {}

    doc_code = areas.get("doc_code", {}) if isinstance(areas.get("doc_code"), dict) else {}
    for index, item in enumerate(
        doc_code.get("items", []) if isinstance(doc_code.get("items"), list) else [],
        start=1,
    ):
        if not isinstance(item, dict) or not item.get("evidence_sufficient"):
            continue
        plan, skip = plan_from_doc_code_item(
            item=item, index=index, repo_root=repo_root, audit_refs=audit_refs
        )
        if plan:
            plans.append(plan)
        if skip:
            skipped.append(skip)

    doc_doc = areas.get("doc_doc", {}) if isinstance(areas.get("doc_doc"), dict) else {}
    for index, item in enumerate(
        doc_doc.get("items", []) if isinstance(doc_doc.get("items"), list) else [],
        start=1,
    ):
        if not isinstance(item, dict) or not item.get("evidence_sufficient"):
            continue
        plan, skip = plan_from_doc_doc_item(
            item=item, index=index, repo_root=repo_root, audit_refs=audit_refs
        )
        if plan:
            plans.append(plan)
        if skip:
            skipped.append(skip)

    return plans, skipped
