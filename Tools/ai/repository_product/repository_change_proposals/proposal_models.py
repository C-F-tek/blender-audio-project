from __future__ import annotations

from .common import *  # noqa: F403

def proposal_concrete_operation_count(item: dict[str, Any]) -> int:
    operations = item.get("concrete_operations")
    if not isinstance(operations, list):
        return 0
    return sum(1 for operation in operations if isinstance(operation, dict))

def proposals_concrete_operation_count(proposals: list[dict[str, Any]]) -> int:
    return sum(proposal_concrete_operation_count(item) for item in proposals)

def proposal(
    *,
    proposal_id: str,
    priority: str,
    area: str,
    title: str,
    rationale: str,
    target_files: list[str],
    change_type: str,
    sketch: list[str],
    validation: list[str],
    stop_conditions: list[str],
    suggestion_outputs: list[dict[str, str]] | None = None,
    do_not_touch: list[str] | None = None,
    evidence_summary: dict[str, Any] | None = None,
    concrete_operations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": proposal_id,
        "priority": priority,
        "area": area,
        "title": title,
        "rationale": rationale,
        "target_files": target_files,
        "change_type": change_type,
        "apply_mode": "manual_review_only",
        "patch_sketch": sketch,
        "evidence_summary": evidence_summary or {},
        "suggestion_outputs": (
            suggestion_outputs
            if suggestion_outputs is not None
            else build_suggestion_outputs(target_files)
        ),
        "validation_commands": validation,
        "stop_conditions": stop_conditions,
        "do_not_touch": do_not_touch
        or [
            "runtime Blender files",
            "Ready To Jazz migration",
            "full analysis JSON",
            "generated indexes by hand",
            "provider execution behavior unless explicitly scoped",
        ],
    }
    if concrete_operations:
        item["concrete_operations"] = concrete_operations
    return item
