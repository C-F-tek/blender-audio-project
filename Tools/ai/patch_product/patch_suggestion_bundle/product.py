"""Product-facing vs supplemental suggestion classification."""

from __future__ import annotations

from typing import Any

from Tools.ai.patch_product.patch_suggestion_bundle.operations import is_safe_target

AUXILIARY_FAMILIES = {
    "validation",
    "telemetry",
    "debug",
    "evidence",
    "execution_plans",
    "workload_quality",
    "provider_diagnostic",
}


def normalized_targets(item: dict[str, Any]) -> list[str]:
    """Return unique normalized targets from one manual-review item."""
    raw_targets = list(item.get("target_files") or [])
    if item.get("target"):
        raw_targets.append(str(item["target"]))
    out: list[str] = []
    seen: set[str] = set()
    for target in raw_targets:
        normalized = str(target).replace("\\", "/").strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            out.append(normalized)
    return out


def target_quality(targets: list[str]) -> dict[str, Any]:
    """Classify target-path quality for manual suggestions."""
    safe: list[str] = []
    unsafe: list[dict[str, str]] = []
    output_like: list[str] = []
    for target in targets:
        ok, reason = is_safe_target(target)
        if ok:
            safe.append(target)
        else:
            unsafe.append({"target": target, "reason": str(reason)})
        if target.lower().startswith(("output/", "docs/local_validation_evidence/")):
            output_like.append(target)
    return {
        "safe_targets": safe,
        "unsafe_targets": unsafe,
        "output_or_evidence_targets": output_like,
        "has_safe_source_target": bool(safe and len(output_like) < len(safe)),
    }


def classify_manual_item(item: dict[str, Any]) -> dict[str, Any]:
    """Classify one manual-review item for final-product usefulness."""
    targets = normalized_targets(item)
    quality = target_quality(targets)
    family = str(item.get("family") or "").lower()
    has_patch_sketch = bool(item.get("patch_sketch"))
    has_validation = bool(item.get("validation_commands"))
    has_stop_conditions = bool(item.get("stop_conditions"))
    has_title = bool(item.get("title"))
    product_ready = (
        quality["has_safe_source_target"]
        and has_title
        and (has_patch_sketch or item.get("operation"))
        and (has_validation or has_stop_conditions)
        and family not in AUXILIARY_FAMILIES
    )
    auxiliary = not product_ready
    if product_ready:
        reason = "concrete target files plus patch sketch and validation/stop conditions"
    elif family in AUXILIARY_FAMILIES:
        reason = "auxiliary validation/telemetry/debug signal"
    elif not quality["has_safe_source_target"]:
        reason = "no safe concrete source/doc target"
    elif not has_title:
        reason = "missing review title/rationale"
    elif not (has_patch_sketch or item.get("operation")):
        reason = "missing patch sketch or deterministic operation"
    else:
        reason = "missing validation commands or stop conditions"

    classified = dict(item)
    classified.update(
        {
            "product_facing": product_ready,
            "supplemental": auxiliary,
            "classification_reason": reason,
            "target_quality": quality,
        }
    )
    return classified


def build_manual_review_product(
    manual_items: list[dict[str, Any]],
    *,
    operation_count: int,
    failed_count: int,
) -> dict[str, Any]:
    """Build final-product readiness classification for suggestion reports."""
    classified = [classify_manual_item(item) for item in manual_items]
    product = [item for item in classified if item["product_facing"]]
    supplemental = [item for item in classified if item["supplemental"]]
    product_items = product[:100]
    supplemental_items = supplemental[:100]
    deterministic_ready = operation_count > 0 and failed_count == 0
    product_review_ready = bool(product)

    if deterministic_ready:
        status = "deterministic_patch_operations_ready"
        ready_for_close = True
    elif product_review_ready:
        status = "manual_review_product_suggestions_ready"
        ready_for_close = True
    else:
        status = "no_applicable_patch_product"
        ready_for_close = False

    return {
        "patch_product_status": status,
        "ready_for_patch_suggestion_review": ready_for_close,
        "deterministic_operation_count": operation_count,
        "deterministic_apply_ready": deterministic_ready,
        "product_facing_manual_review_count": len(product),
        "product_facing_manual_review_published_count": len(product_items),
        "product_facing_manual_review_total_count": len(product),
        "supplemental_manual_review_count": len(supplemental),
        "supplemental_manual_review_published_count": len(supplemental_items),
        "supplemental_manual_review_total_count": len(supplemental),
        "manual_review_count": len(classified),
        "product_facing_manual_review_items": product_items,
        "supplemental_manual_review_items": supplemental_items,
        "classification_policy": (
            "Product-facing suggestions need safe concrete source/doc targets, "
            "a title/rationale, patch sketch or operation, and validation commands "
            "or stop conditions. Telemetry/debug/evidence-only items stay supplemental."
        ),
    }
