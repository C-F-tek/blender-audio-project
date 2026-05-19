from __future__ import annotations

from Tools.ai._shared.evidence_item_planning import (
    doc_code_item_or_skip,
    doc_code_strategy_parts,
    doc_doc_item_or_skip,
    doc_doc_strategy_text,
    iter_sufficient_area_items,
)

from .common import *  # noqa: F403

def provider_recommendations(
    gpu_report: dict[str, Any], repo_root: Path
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    recommendations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    raw = gpu_report.get("recommendations")
    if not isinstance(raw, list):
        return recommendations, skipped
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            skipped.append(
                {
                    "id": f"provider_{index:03d}",
                    "reason": "recommendation is not an object",
                }
            )
            continue
        if item.get("status") != "ready_for_patch_plan":
            continue
        rec = dict(item)
        rec.setdefault("source", "gpu_provider")
        errors = recommendation_schema_errors(rec, len(recommendations), repo_root)
        if errors:
            skipped.append(
                {
                    "id": str(item.get("id") or f"provider_{index:03d}"),
                    "reason": "; ".join(errors),
                }
            )
            continue
        recommendations.append(rec)
    return recommendations, skipped

def doc_code_recommendation(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    npu_refs: list[dict[str, Any]],
    tool_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    evidence_item, skip = doc_code_item_or_skip(
        item=item,
        index=index,
        repo_root=repo_root,
        id_prefix="det_doc_code",
        target_path_error=target_path_error,
        missing_reason="doc_code item has no doc target",
    )
    if skip or evidence_item is None:
        return None, skip
    evidence_paths = compact_evidence_files(item)
    strategy_parts = doc_code_strategy_parts(
        reference=evidence_item.reference,
        doc=evidence_item.doc,
        existing_candidate=evidence_item.existing_candidate,
        candidates=evidence_item.candidates,
        opening="Create a narrow manual-review patch plan for the documentation/code reference mismatch.",
        inspect_template=(
            "Inspect `{reference}` and update `{doc}` only if the reference is stale "
            "or should point at an existing artifact."
        ),
        existing_template=(
            "Prefer existing candidate `{existing_candidate}` over inventing a new runtime artifact."
        ),
        candidate_limit=6,
    )

    return (
        {
            "id": f"det_doc_code_{index:03d}",
            "area": "doc_code",
            "status": "ready_for_patch_plan",
            "target_files": [evidence_item.doc],
            "rationale": item.get("reason")
            or "Evidence and runtime tool reports are sufficient to build a manual-review patch plan for this doc/code reference.",
            "proposed_strategy": " ".join(strategy_parts),
            "risk": "low",
            "validation_commands": DEFAULT_VALIDATION_COMMANDS,
            "stop_conditions": [
                "Stop if the referenced file exists after refreshing master.",
                "Stop if the fix requires creating runtime code instead of correcting documentation or references.",
                "Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.",
            ],
            "source": "deterministic_evidence_synthesizer",
            "evidence": evidence_paths,
            "tool_evidence": tool_refs,
            "npu_audit_refs": npu_refs,
            "guardrails": {
                "patch_application_performed": False,
                "manual_review_required": True,
            },
        },
        None,
    )

def doc_doc_recommendation(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    npu_refs: list[dict[str, Any]],
    tool_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    evidence_item, skip = doc_doc_item_or_skip(
        item=item,
        index=index,
        repo_root=repo_root,
        id_prefix="det_doc_doc",
        target_path_error=target_path_error,
        missing_reason="doc_doc item has no path target",
        term_limit=10,
        terms_fallback="the missing cross-reference terms",
    )
    if skip or evidence_item is None:
        return None, skip
    return (
        {
            "id": f"det_doc_doc_{index:03d}",
            "area": "doc_doc",
            "status": "ready_for_patch_plan",
            "target_files": [evidence_item.path],
            "rationale": item.get("reason")
            or "Evidence and runtime tool reports are sufficient to build a manual-review documentation cross-reference patch plan.",
            "proposed_strategy": doc_doc_strategy_text(
                evidence_item.terms_text,
                lead="Add a compact cross-reference for",
            ),
            "risk": "low",
            "validation_commands": DEFAULT_VALIDATION_COMMANDS,
            "stop_conditions": [
                "Stop if the missing terms are already present after refreshing master.",
                "Stop if the edit would duplicate large generated artifacts.",
                "Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.",
            ],
            "source": "deterministic_evidence_synthesizer",
            "evidence": compact_evidence_files(item),
            "tool_evidence": tool_refs,
            "npu_audit_refs": npu_refs,
            "guardrails": {
                "patch_application_performed": False,
                "manual_review_required": True,
            },
        },
        None,
    )

def synthesize_from_evidence(
    *,
    evidence: dict[str, Any],
    repo_root: Path,
    npu_refs: list[dict[str, Any]],
    tool_refs: list[dict[str, Any]],
    max_recommendations: int,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    recommendations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []

    for index, item in iter_sufficient_area_items(evidence, "doc_code"):
        if len(recommendations) >= max_recommendations:
            break
        rec, skip = doc_code_recommendation(
            item=item,
            index=index,
            repo_root=repo_root,
            npu_refs=npu_refs,
            tool_refs=tool_refs,
        )
        if rec:
            recommendations.append(rec)
        if skip:
            skipped.append(skip)

    for index, item in iter_sufficient_area_items(evidence, "doc_doc"):
        if len(recommendations) >= max_recommendations:
            break
        rec, skip = doc_doc_recommendation(
            item=item,
            index=index,
            repo_root=repo_root,
            npu_refs=npu_refs,
            tool_refs=tool_refs,
        )
        if rec:
            recommendations.append(rec)
        if skip:
            skipped.append(skip)

    validated: list[dict[str, Any]] = []
    for rec in recommendations:
        errors = recommendation_schema_errors(rec, len(validated), repo_root)
        if errors:
            skipped.append({"id": str(rec.get("id")), "reason": "; ".join(errors)})
            continue
        validated.append(rec)
    return validated, skipped
