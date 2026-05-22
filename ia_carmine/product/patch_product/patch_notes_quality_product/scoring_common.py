"""Shared helpers for patch-notes quality scoring."""

from __future__ import annotations

from typing import Any

from ia_carmine.product.patch_product.patch_plan_quality_product.scoring import list_plans

def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any, limit: int = 500) -> str:
    text = str(value or "").strip()
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def _unique_strings(items: list[Any], limit: int = 16) -> list[str]:
    out: list[str] = []
    for item in items:
        value = str(item or "").strip()
        if value and value not in out:
            out.append(value)
        if len(out) >= limit:
            break
    return out


def patch_plan_summary(patch_plan: dict[str, Any], patch_quality: dict[str, Any]) -> dict[str, Any]:
    plans = list_plans(patch_plan)
    targets: list[Any] = []
    validations: list[Any] = []
    stops: list[Any] = []
    for plan in plans:
        targets.extend(safe_list(plan.get("target_files")))
        validations.extend(safe_list(plan.get("validation_commands")))
        stops.extend(safe_list(plan.get("stop_conditions")))
    quality = safe_dict(patch_quality.get("quality"))
    return {
        "patch_plan_count": len(plans),
        "patch_quality_seen": bool(patch_quality),
        "patch_quality_gate_passed": patch_quality.get("quality_gate_passed"),
        "patch_quality_classification": patch_quality.get("classification"),
        "average_plan_score": quality.get("average_plan_score"),
        "target_files": _unique_strings(targets, limit=24),
        "validation_commands": _unique_strings(validations, limit=24),
        "stop_conditions": _unique_strings(stops, limit=24),
    }
