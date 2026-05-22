"""Evidence sufficiency analysis routines."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .evidence_common import evidence_to_dict, inspect_file

def extract_doc_code_targets(refined: dict[str, Any]) -> list[dict[str, Any]]:
    targets = refined.get("refinement", {}).get("doc_code", {}).get("actionable_refs", []) or []
    return [item for item in targets if isinstance(item, dict)]

def extract_doc_doc_targets(refined: dict[str, Any]) -> list[dict[str, Any]]:
    targets = refined.get("refinement", {}).get("doc_doc", {}).get("actionable", []) or []
    return [item for item in targets if isinstance(item, dict)]

def normalize_candidate(candidate: Any) -> str:
    if candidate is None:
        return ""
    return str(candidate).replace("\\", "/").strip().strip('`.,:)];"').lstrip("/")

def candidate_exists(repo_root: Path, candidates: list[Any]) -> tuple[str | None, list[str]]:
    normalized = [normalize_candidate(item) for item in candidates]
    for item in normalized:
        if item and (repo_root / item).exists():
            return item, normalized
    return None, normalized

def analyze_doc_code(refined: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    items = []
    ready = 0
    needs_context = 0
    for target in extract_doc_code_targets(refined):
        doc = str(target.get("doc") or "")
        normalized_ref = normalize_candidate(
            target.get("normalized_reference") or target.get("reference")
        )
        candidates = target.get("candidate_references") or [normalized_ref]
        existing, normalized_candidates = candidate_exists(repo_root, candidates)
        doc_evidence = inspect_file(
            repo_root,
            doc,
            terms=[normalized_ref, *normalized_candidates],
            kind="source_markdown",
        )
        target_evidence = (
            inspect_file(repo_root, existing or normalized_ref, terms=[], kind="target_path")
            if existing
            else inspect_file(repo_root, normalized_ref, kind="target_path")
        )
        sufficient = doc_evidence.exists and normalized_ref and existing is None
        recommendation = (
            "manual_doc_reference_patch_candidate" if sufficient else "needs_more_context"
        )
        if sufficient:
            ready += 1
        else:
            needs_context += 1
        items.append(
            {
                "doc": doc,
                "reference": normalized_ref,
                "candidate_references": normalized_candidates,
                "existing_candidate": existing,
                "evidence_sufficient": sufficient,
                "recommendation": recommendation,
                "confidence": "medium" if sufficient else "low",
                "reason": (
                    "source doc exists and target path remains missing"
                    if sufficient
                    else "source doc missing or target resolved"
                ),
                "evidence_files": [
                    evidence_to_dict(doc_evidence),
                    evidence_to_dict(target_evidence),
                ],
            }
        )
    return {
        "area": "doc_code",
        "item_count": len(items),
        "ready_for_manual_patch_count": ready,
        "needs_more_context_count": needs_context,
        "items": items,
    }

def analyze_doc_doc(refined: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    items = []
    ready = 0
    for target in extract_doc_doc_targets(refined):
        path = str(target.get("path") or "")
        terms = [str(item) for item in target.get("missing_terms", [])]
        evidence = inspect_file(repo_root, path, terms=terms, kind="contract_doc")
        sufficient = evidence.exists and bool(terms)
        if sufficient:
            ready += 1
        items.append(
            {
                "path": path,
                "missing_terms": terms,
                "evidence_sufficient": sufficient,
                "recommendation": (
                    "manual_cross_reference_patch_candidate" if sufficient else "needs_more_context"
                ),
                "confidence": "medium" if sufficient else "low",
                "reason": (
                    "contract doc exists and missing terms are explicit"
                    if sufficient
                    else "contract doc missing or no explicit terms"
                ),
                "evidence_files": [evidence_to_dict(evidence)],
            }
        )
    return {
        "area": "doc_doc",
        "item_count": len(items),
        "ready_for_manual_patch_count": ready,
        "needs_more_context_count": len(items) - ready,
        "items": items,
    }

def analyze_code_code(refined: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    targets = refined.get("refinement", {}).get("code_code", {}).get("actionable", []) or []
    items = []
    for target in targets:
        symbol = str(target.get("symbol") or "")
        paths = [str(path) for path in target.get("paths", [])]
        evidence_files = [
            evidence_to_dict(inspect_file(repo_root, path, terms=[symbol], kind="symbol_file"))
            for path in paths[:8]
        ]
        items.append(
            {
                "symbol": symbol,
                "paths": paths,
                "evidence_sufficient": False,
                "recommendation": "advisory_only_until_semantic_equivalence_review",
                "confidence": "low",
                "reason": "duplicate symbol names alone are not enough to patch safely",
                "evidence_files": evidence_files,
            }
        )
    return {
        "area": "code_code",
        "item_count": len(items),
        "ready_for_manual_patch_count": 0,
        "needs_more_context_count": len(items),
        "items": items,
    }

def build_decision(
    doc_code: dict[str, Any], doc_doc: dict[str, Any], code_code: dict[str, Any]
) -> dict[str, Any]:
    ready = (
        doc_code["ready_for_manual_patch_count"]
        + doc_doc["ready_for_manual_patch_count"]
        + code_code["ready_for_manual_patch_count"]
    )
    needs_context = (
        doc_code["needs_more_context_count"]
        + doc_doc["needs_more_context_count"]
        + code_code["needs_more_context_count"]
    )
    next_steps = []
    if doc_code["ready_for_manual_patch_count"]:
        next_steps.append(
            "Review doc_code items and patch only source Markdown references with missing targets or intentional placeholders."
        )
    if doc_doc["ready_for_manual_patch_count"]:
        next_steps.append(
            "Add targeted cross-references to dedicated contract docs instead of duplicating full contracts everywhere."
        )
    if code_code["item_count"]:
        next_steps.append(
            "Keep code_code findings advisory-only until semantic equivalence is established."
        )
    return {
        "ready_for_manual_patch_count": ready,
        "needs_more_context_count": needs_context,
        "recommended_mode": (
            "manual_review_only_patch_candidates" if ready else "no_patch_recommended"
        ),
        "sufficient_for_real_pr": ready > 0,
        "next_steps": next_steps,
    }
