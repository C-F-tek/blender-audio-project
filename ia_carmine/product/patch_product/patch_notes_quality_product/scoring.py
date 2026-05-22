"""Compatibility API for patch-notes quality scoring."""

from __future__ import annotations

from .note_scoring import (
    _area_diverse_plans,
    _canonical_note_area,
    build_patch_notes,
    classify,
    patch_notes_applicability,
    score_product,
)
from .scoring_common import (
    _text,
    _unique_strings,
    patch_plan_summary,
    safe_dict,
    safe_list,
)
from .sufficiency import (
    ALL_ALL_REQUIRED_AREAS,
    PRODUCT_AREA_ALIASES,
    REPOSITORY_KIND_TO_PRODUCT_AREA,
    UNPATCHABLE_REPOSITORY_PREFIXES,
    _bump_area,
    _finding_patch_target,
    _is_unpatchable_generated_path,
    _merge_counts,
    _path_value,
    _proposal_area_counts,
    _repository_area_counts,
    _repository_patchable_area_counts,
    _subtract_counts,
    _task_text,
    _workflow_summary,
    build_product_sufficiency,
    canonical_product_area,
    detect_product_mode,
)

__all__ = [
    "ALL_ALL_REQUIRED_AREAS",
    "PRODUCT_AREA_ALIASES",
    "REPOSITORY_KIND_TO_PRODUCT_AREA",
    "UNPATCHABLE_REPOSITORY_PREFIXES",
    "build_patch_notes",
    "build_product_sufficiency",
    "canonical_product_area",
    "classify",
    "detect_product_mode",
    "patch_notes_applicability",
    "patch_plan_summary",
    "safe_dict",
    "safe_list",
    "score_product",
]
