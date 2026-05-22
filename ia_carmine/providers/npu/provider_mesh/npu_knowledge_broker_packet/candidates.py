"""Candidate scoring for NPU knowledge broker packets."""

from __future__ import annotations

from typing import Any

from .common import normalize_path, path_allowed

def score_candidate(
    path: str, objective_terms: set[str], base_score: int = 0
) -> tuple[int, list[str]]:
    text = normalize_path(path).lower()
    matched = sorted(term for term in objective_terms if term and term in text)
    score = base_score + len(matched) * 4
    if text.startswith("Tools/workflow/"):
        score += 8
    if text.startswith("ia_carmine/"):
        score += 7
    if text.startswith("Tools/validation/"):
        score += 7
    if text.startswith("Tools/npu/"):
        score += 6
    if text.startswith("docs/"):
        score += 4
    if "selected" in text or "chunk" in text:
        score += 3
    if "adapter" in text or "manifest" in text:
        score += 3
    if "npu" in text or "knowledge" in text or "broker" in text:
        score += 5
    return score, matched


def add_candidate(
    candidates: dict[str, dict[str, Any]],
    path: str,
    source: str,
    objective_terms: set[str],
    reason: str,
    base_score: int = 0,
) -> None:
    normalized = normalize_path(path)
    if not path_allowed(normalized):
        return
    score, matched = score_candidate(normalized, objective_terms, base_score)
    existing = candidates.get(normalized)
    if existing:
        existing["score"] = max(existing["score"], score)
        if source not in existing["sources"]:
            existing["sources"].append(source)
        if reason not in existing["reasons"]:
            existing["reasons"].append(reason)
        existing["matched_terms"] = sorted(set(existing["matched_terms"]) | set(matched))
        return
    candidates[normalized] = {
        "path": normalized,
        "score": score,
        "sources": [source],
        "reasons": [reason],
        "matched_terms": matched,
        "content_role": "candidate_context",
        "provider_execution_required": False,
        "source_write_allowed": False,
    }
