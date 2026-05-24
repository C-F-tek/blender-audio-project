"""Doc/reference refinement for megalithic review signals."""

from __future__ import annotations

from typing import Any

from .common import (
    LOW_SIGNAL_DOCS,
    candidate_references,
    existing_candidate,
    has_path_intent,
    is_conceptual_slash_term,
    is_placeholder_reference,
    normalize_reference,
    repo_root_from_review,
)

def refine_doc_code(
    review: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    repo_root = repo_root_from_review(review)
    missing = review.get("doc_code_consistency", {}).get("missing_path_references", []) or []
    actionable_refs = []
    ignored_refs = []
    resolved_refs = []
    for item in missing:
        doc = str(item.get("doc") or "")
        reference = str(item.get("reference") or "")
        normalized = normalize_reference(reference)
        resolved = existing_candidate(reference, repo_root)
        if doc in LOW_SIGNAL_DOCS:
            ignored_refs.append(
                {
                    **item,
                    "normalized_reference": normalized,
                    "reason": "low_signal_generated_history",
                }
            )
        elif is_placeholder_reference(reference):
            ignored_refs.append(
                {
                    **item,
                    "normalized_reference": normalized,
                    "reason": "placeholder_generated_or_template_path",
                }
            )
        elif resolved:
            resolved_refs.append(
                {
                    **item,
                    "normalized_reference": normalized,
                    "resolved_reference": resolved,
                    "reason": "exists_after_normalization_or_alias",
                }
            )
        elif is_conceptual_slash_term(reference):
            ignored_refs.append(
                {
                    **item,
                    "normalized_reference": normalized,
                    "reason": "conceptual_slash_term",
                }
            )
        elif has_path_intent(reference):
            actionable_refs.append(
                {
                    **item,
                    "normalized_reference": normalized,
                    "candidate_references": candidate_references(reference),
                }
            )
        else:
            ignored_refs.append(
                {
                    **item,
                    "normalized_reference": normalized,
                    "reason": "no_clear_path_intent",
                }
            )
    findings = []
    if actionable_refs:
        findings.append(
            {
                "severity": "medium",
                "area": "doc_code",
                "title": "Markdown references likely repository paths that are missing",
                "details": [
                    f"{item.get('doc')} -> {item.get('normalized_reference')}"
                    for item in actionable_refs[:30]
                ],
            }
        )
    return findings, {
        "actionable_refs": actionable_refs[:200],
        "resolved_count": len(resolved_refs),
        "resolved_sample": resolved_refs[:80],
        "ignored_count": len(ignored_refs),
        "ignored_sample": ignored_refs[:80],
    }

def refine_doc_doc(
    review: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    canonical_docs = review.get("doc_doc_consistency", {}).get("canonical_docs", []) or []
    actionable = []
    informational = []
    for item in canonical_docs:
        missing = list(item.get("missing_terms") or [])
        if not missing:
            continue
        path = str(item.get("path"))
        if path in {
            "docs/JSON_SCHEMAS.md",
            "Tools/validation/CONTEXT_INDEX.md",
            "docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md",
        }:
            actionable.append({"path": path, "missing_terms": missing})
        else:
            informational.append(
                {
                    "path": path,
                    "missing_terms": missing,
                    "reason": "canonical_doc_not_required_to_repeat_all_contract_terms",
                }
            )
    findings = []
    if actionable:
        findings.append(
            {
                "severity": "medium",
                "area": "doc_doc",
                "title": "Dedicated contract docs may need targeted cross-references",
                "details": [f"{item['path']}: {item['missing_terms']}" for item in actionable],
            }
        )
    return findings, {"actionable": actionable, "informational": informational}
