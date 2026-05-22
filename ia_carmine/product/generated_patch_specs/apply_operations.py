"""Operation extraction from generated patch specs."""

from __future__ import annotations

from typing import Any

from .apply_common import (
    CONCRETE_OPERATION_NAMES,
    MANUAL_OR_DRAFT_OPERATIONS,
    PatchOperation,
    normalize_operation,
)
from .apply_discovery import is_denied_target, normalize_repo_path

def replacement_to_operation(
    path: str, replacement: dict[str, Any], source_id: str
) -> PatchOperation | None:
    replacement_type = str(replacement.get("type") or "").strip().lower()
    if replacement_type == "exact":
        old = replacement.get("old")
        new = replacement.get("new")
        if isinstance(old, str) and isinstance(new, str):
            return PatchOperation(
                operation="replace_once",
                path=path,
                find=old,
                replace=new,
                source_id=source_id,
                family="generated_patch_spec",
                description="exact replacement from generated patch spec",
            )
    if replacement_type == "insert_after":
        anchor = replacement.get("anchor")
        insert = replacement.get("insert")
        if isinstance(anchor, str) and isinstance(insert, str):
            return PatchOperation(
                operation="insert_after_once",
                path=path,
                find=anchor,
                content=insert,
                source_id=source_id,
                family="generated_patch_spec",
                description="insert_after replacement from generated patch spec",
            )
    if replacement_type == "insert_before":
        anchor = replacement.get("anchor")
        insert = replacement.get("insert")
        if isinstance(anchor, str) and isinstance(insert, str):
            return PatchOperation(
                operation="insert_before_once",
                path=path,
                find=anchor,
                content=insert,
                source_id=source_id,
                family="generated_patch_spec",
                description="insert_before replacement from generated patch spec",
            )
    return None

def operations_from_spec(
    data: dict[str, Any], spec_path: str
) -> tuple[list[PatchOperation], list[dict[str, Any]]]:
    operations: list[PatchOperation] = []
    manual: list[dict[str, Any]] = []
    raw_operations = data.get("operations")
    if not isinstance(raw_operations, list):
        manual.append(
            {
                "id": spec_path,
                "reason": "spec operations is not a list",
                "target_files": [],
            }
        )
        return operations, manual

    for index, raw in enumerate(raw_operations):
        if not isinstance(raw, dict):
            manual.append(
                {
                    "id": f"{spec_path}#{index}",
                    "reason": "operation is not an object",
                    "target_files": [],
                }
            )
            continue

        source_id = str(raw.get("proposal_id") or raw.get("id") or f"{spec_path}#{index}")
        raw_operation = (
            str(raw.get("operation") or raw.get("op") or raw.get("action") or "")
            .strip()
            .lower()
            .replace("-", "_")
        )
        raw_path = normalize_repo_path(
            str(raw.get("path") or raw.get("target_file") or raw.get("file") or "")
        )
        denied = is_denied_target(raw_path)
        if denied:
            manual.append(
                {
                    "id": source_id,
                    "reason": denied,
                    "target_files": [raw_path] if raw_path else [],
                }
            )
            continue

        if (
            raw_operation in MANUAL_OR_DRAFT_OPERATIONS
            or raw.get("draft_status") == "needs_concrete_replacements"
        ):
            replacements = raw.get("replacements")
            if not replacements:
                manual.append(
                    {
                        "id": source_id,
                        "reason": "metadata-only draft operation has no concrete replacements",
                        "target_files": [raw_path] if raw_path else [],
                        "draft_status": raw.get("draft_status"),
                    }
                )
                continue

        normalized = normalize_operation(raw)
        if normalized and normalized.operation in CONCRETE_OPERATION_NAMES:
            operations.append(normalized)
            continue

        replacements = raw.get("replacements")
        if isinstance(replacements, list) and raw_path:
            converted = 0
            for repl_index, replacement in enumerate(replacements):
                if not isinstance(replacement, dict):
                    continue
                operation = replacement_to_operation(
                    raw_path, replacement, f"{source_id}:{repl_index}"
                )
                if operation:
                    operations.append(operation)
                    converted += 1
            if converted:
                continue

        manual.append(
            {
                "id": source_id,
                "reason": "no allowlisted concrete deterministic operation found",
                "target_files": [raw_path] if raw_path else [],
                "operation": raw_operation,
            }
        )

    return operations, manual
