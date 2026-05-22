"""Recommendation classification helpers."""

from __future__ import annotations

from typing import Any

from .common import COSMETIC_PATCH_KEYWORDS

def recommendation_text_blob(rec: dict[str, Any]) -> str:
    return " ".join(
        str(rec.get(key) or "")
        for key in ("area", "rationale", "proposed_strategy", "edit_strategy")
    ).lower()

def has_substantive_consistency_evidence(rec: dict[str, Any]) -> bool:
    if isinstance(rec.get("repository_consistency_finding"), dict):
        return True
    evidence = rec.get("source_evidence")
    return isinstance(evidence, dict) and isinstance(
        evidence.get("repository_consistency_finding"), dict
    )

def is_cosmetic_recommendation(rec: dict[str, Any]) -> bool:
    if has_substantive_consistency_evidence(rec):
        return False
    text = recommendation_text_blob(rec)
    return any(keyword in text for keyword in COSMETIC_PATCH_KEYWORDS)
