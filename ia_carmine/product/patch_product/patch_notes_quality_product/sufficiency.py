"""Availability-aware patch-note product sufficiency checks."""

from __future__ import annotations

from typing import Any

from .scoring_common import safe_dict, safe_list

PRODUCT_AREA_ALIASES = {
    "md_md": "doc_doc",
    "markdown_markdown": "doc_doc",
    "doc_code": "doc_python",
    "md_python": "doc_python",
    "md_powershell": "doc_python",
    "python_validation": "python_doc",
    "repository_consistency": "refactor_candidate",
}

ALL_ALL_REQUIRED_AREAS = [
    "doc_doc",
    "doc_python",
    "python_doc",
    "python_python",
    "policy_violation",
    "refactor_candidate",
    "evidence_gap",
]

REPOSITORY_KIND_TO_PRODUCT_AREA = {
    "md_mentions_missing_markdown_path": "doc_doc",
    "md_mentions_missing_python_path": "doc_python",
    "md_mentions_missing_powershell_path": "doc_python",
    "md_python_command_script_missing": "doc_python",
    "md_cli_arg_not_in_argparse": "doc_python",
    "documented_python_script_without_obvious_smoke": "python_doc",
    "python_import_missing": "python_python",
    "python_import_symbol_missing": "python_python",
}


def canonical_product_area(area: Any) -> str:
    value = str(area or "").strip()
    return PRODUCT_AREA_ALIASES.get(value, value)


def _task_text(task: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("title", "objective_hint"):
        value = task.get(key)
        if value:
            parts.append(str(value))
    for key in ("headings", "excerpt"):
        values = task.get(key)
        if isinstance(values, list):
            parts.extend(str(item) for item in values)
    return "\n".join(parts)


def detect_product_mode(task: dict[str, Any]) -> dict[str, Any]:
    text = _task_text(task)
    lowered = text.lower()
    all_all = "all_all" in lowered or "all-all" in lowered or "whole repository" in lowered
    requested = [area for area in ALL_ALL_REQUIRED_AREAS if area.lower() in lowered]
    if all_all and not requested:
        requested = list(ALL_ALL_REQUIRED_AREAS)
    return {
        "mode": "ALL_ALL" if all_all or requested else "standard",
        "requested_areas": requested,
    }


def _workflow_summary(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    decision = safe_dict(loaded.get("decision_loop"))
    return {
        "passed": decision.get("passed"),
        "recommendation_count": decision.get("recommendation_count"),
        "patch_plan_count": decision.get("patch_plan_count"),
    }


def _bump_area(counts: dict[str, int], area: Any, amount: int = 1) -> None:
    canonical = canonical_product_area(area)
    if canonical:
        counts[canonical] = counts.get(canonical, 0) + amount


def _repository_area_counts(repository_consistency: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for kind, count in safe_dict(repository_consistency.get("finding_kind_counts")).items():
        area = REPOSITORY_KIND_TO_PRODUCT_AREA.get(str(kind))
        if area:
            counts[area] = counts.get(area, 0) + int(count or 0)
    return counts


UNPATCHABLE_REPOSITORY_PREFIXES = (
    "output/",
    "renders/",
    ".git/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)


def _path_value(value: Any) -> str:
    text = str(value or "").strip().replace("\\\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text


def _is_unpatchable_generated_path(path: str) -> bool:
    normalized = _path_value(path)
    if not normalized:
        return True
    if "*" in normalized or normalized.endswith("/"):
        return True
    lowered = normalized.lower()
    if lowered.endswith((".db", ".sqlite")):
        return True
    return any(normalized.startswith(prefix) for prefix in UNPATCHABLE_REPOSITORY_PREFIXES)


def _finding_patch_target(finding: dict[str, Any]) -> str:
    kind = str(finding.get("kind") or "")
    area = REPOSITORY_KIND_TO_PRODUCT_AREA.get(kind)
    source = _path_value(finding.get("source") or finding.get("source_path"))
    target = _path_value(finding.get("target") or finding.get("target_path"))
    # For documentation consistency findings, the patch target is the document
    # that contains the stale reference, not the missing referenced artifact.
    if area in {"doc_doc", "doc_python"}:
        return source
    return source or target


def _repository_patchable_area_counts(
    repository_consistency: dict[str, Any],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    raw_findings = safe_list(repository_consistency.get("findings"))
    for item in raw_findings:
        if not isinstance(item, dict):
            continue
        area = REPOSITORY_KIND_TO_PRODUCT_AREA.get(str(item.get("kind") or ""))
        if not area:
            continue
        patch_target = _finding_patch_target(item)
        if _is_unpatchable_generated_path(patch_target):
            continue
        counts[area] = counts.get(area, 0) + 1
    # Older repository maps may expose counts but not full findings. Keep those
    # counts only as a fallback when no detailed finding list is available.
    if not raw_findings:
        return _repository_area_counts(repository_consistency)
    return counts


def _subtract_counts(
    raw_counts: dict[str, int], patchable_counts: dict[str, int]
) -> dict[str, int]:
    result: dict[str, int] = {}
    for area, raw_count in raw_counts.items():
        filtered = int(raw_count or 0) - int(patchable_counts.get(area, 0) or 0)
        if filtered > 0:
            result[area] = filtered
    return result


def _proposal_area_counts(loaded: dict[str, dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    patch_plan = safe_dict(loaded.get("patch_plan"))
    for key in ("patch_plans", "plans"):
        for item in safe_list(patch_plan.get(key)):
            if isinstance(item, dict):
                _bump_area(counts, item.get("area"))
    return counts


def _merge_counts(*items: dict[str, int]) -> dict[str, int]:
    merged: dict[str, int] = {}
    for item in items:
        for key, value in item.items():
            merged[key] = merged.get(key, 0) + int(value or 0)
    return merged


def build_product_sufficiency(
    report: dict[str, Any],
    loaded: dict[str, dict[str, Any]],
    task: dict[str, Any],
    *,
    patch_note_limit: int = 20,
    requested_min_patch_notes: int = 0,
) -> dict[str, Any]:
    mode = detect_product_mode(task)
    notes = [item for item in safe_list(report.get("patch_notes")) if isinstance(item, dict)]
    actual_area_counts: dict[str, int] = {}
    for note in notes:
        _bump_area(actual_area_counts, note.get("area"))
    actual_areas = sorted(actual_area_counts)
    raw_repository_area_counts = _repository_area_counts(
        safe_dict(loaded.get("repository_consistency"))
    )
    repository_area_counts = _repository_patchable_area_counts(
        safe_dict(loaded.get("repository_consistency"))
    )
    unpatchable_repository_area_counts = _subtract_counts(
        raw_repository_area_counts, repository_area_counts
    )
    proposal_area_counts = _proposal_area_counts(loaded)
    available_area_counts = _merge_counts(
        repository_area_counts, proposal_area_counts, actual_area_counts
    )
    requested_areas = list(mode["requested_areas"])
    available_requested_areas = [
        area for area in requested_areas if available_area_counts.get(area, 0) > 0
    ]
    unavailable_requested_areas = [
        area for area in requested_areas if area not in available_requested_areas
    ]
    missing_available_areas = [
        area for area in available_requested_areas if area not in actual_areas
    ]
    requested_min_patch_notes = int(requested_min_patch_notes or 0)
    if requested_min_patch_notes <= 0:
        requested_min_patch_notes = 1
        if mode["mode"] == "ALL_ALL":
            requested_min_patch_notes = max(5, min(40, max(1, len(available_requested_areas)) * 5))
    patch_note_limit = max(1, int(patch_note_limit or 20))
    workflow = _workflow_summary(loaded)
    recommendation_count = int(workflow.get("recommendation_count") or 0)
    patch_plan_count = int(
        workflow.get("patch_plan_count")
        or safe_dict(report.get("patch_plan_summary")).get("patch_plan_count")
        or 0
    )
    reasons: list[str] = []
    if len(notes) < requested_min_patch_notes:
        reasons.append("patch_note_count_below_requested_minimum")
    if patch_note_limit < requested_min_patch_notes:
        reasons.append("patch_note_limit_below_requested_minimum")
    if missing_available_areas:
        reasons.append("available_requested_area_coverage_missing")
    if workflow.get("passed") is False:
        reasons.append("workflow_summary_not_passed")
    if mode["mode"] == "ALL_ALL" and patch_plan_count < requested_min_patch_notes:
        reasons.append("patch_plan_count_below_availability_aware_minimum")
    if (
        mode["mode"] == "ALL_ALL"
        and recommendation_count
        and recommendation_count < requested_min_patch_notes
    ):
        reasons.append("recommendation_count_below_availability_aware_minimum")
    return {
        "mode": mode["mode"],
        "requested_areas": requested_areas,
        "available_requested_areas": available_requested_areas,
        "unavailable_requested_areas": unavailable_requested_areas,
        "missing_available_areas": missing_available_areas,
        "requested_min_patch_notes": requested_min_patch_notes,
        "patch_note_limit": patch_note_limit,
        "actual_patch_note_count": len(notes),
        "actual_areas": actual_areas,
        "actual_area_counts": actual_area_counts,
        "repository_area_counts": repository_area_counts,
        "raw_repository_area_counts": raw_repository_area_counts,
        "unpatchable_repository_area_counts": unpatchable_repository_area_counts,
        "proposal_area_counts": proposal_area_counts,
        "available_area_counts": available_area_counts,
        "workflow_summary_passed": workflow.get("passed"),
        "recommendation_count": recommendation_count,
        "patch_plan_count": patch_plan_count,
        "sufficient": not reasons,
        "insufficiency_reasons": reasons,
    }
