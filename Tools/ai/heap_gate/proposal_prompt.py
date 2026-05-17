"""Prompt helpers for heap proposal refinement."""

from __future__ import annotations


def build_refinement_prompt(
    *,
    revision: int,
    reasons: list[str],
    source_candidates: list[str],
) -> str:
    refinement_lines = [
        "HEAP REFINEMENT TASK FROM SAME-HEAP CROSS-LANE VETO",
        f"Rejected revision: {revision}",
        "The previous proposal is not accepted inside the heap universe.",
        "",
        "Output/context policy:",
        "- output may exceed a single model context;",
        "- persist long material as proposal/refinement artifacts;",
        "- pass only compact summaries and artifact paths to the next revision;",
        "- never require GPU1 to hold the whole final product in one context window.",
        "",
        "Rejection reasons:",
        *[f"- {reason}" for reason in reasons],
        "",
        "Next provider revision must:",
        "- return concrete patch-plan JSON or explicit reject_with_reason;",
        "- include repo-relative target_files with exact existing paths;",
        "- include concrete operations or patch-spec fragments, not prose-only status;",
        "- avoid TODO/FIXME/pass/stub/placeholder markers;",
        "- consume GPU0 review, NPU audit and heap_parallel_cycle artifact as hard constraints;",
        "- keep patch_application_performed=false and source_writes_performed=false.",
        "",
        "Allowed source anchors:",
        *[f"- {item}" for item in source_candidates[:24]],
    ]
    return "\n".join(refinement_lines)
