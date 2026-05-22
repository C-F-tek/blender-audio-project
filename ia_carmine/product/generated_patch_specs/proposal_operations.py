"""Operation construction for proposal-derived patch specs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .proposal_common import (
    CONCRETE_OPERATION_NAMES,
    DEFAULT_GUARDRAILS,
    EXPECTED_APPLY_MODE,
    SKIPPED_OUTPUT_KINDS,
    SPEC_KIND,
    SUPPORTED_OUTPUT_KINDS,
    normalize_repo_path,
    proposal_outputs,
    repo_relative,
    target_path_error,
)

def build_metadata_operation(*, proposal_id: str, output: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": normalize_repo_path(output.get("path")),
        "replacements": [],
        "proposal_id": proposal_id,
        "artifact_kind": output.get("artifact_kind"),
        "operation": output.get("operation") or "manual_patch_suggestion",
        "content_status": "draft_metadata_only",
        "draft_status": "needs_concrete_replacements",
        "draft_notes": [
            "Add exact, regex or insert replacements only after reviewing the target file.",
            "Keep replacements small enough for deterministic dry-run validation.",
            "Leave this draft under output/ until it has been intentionally reviewed.",
        ],
        "require_contains_after": [],
        "forbid_contains_after": [],
    }

def build_concrete_operation(
    *, proposal_id: str, raw: dict[str, Any], repo_root: Path
) -> tuple[dict[str, Any] | None, str]:
    operation = str(raw.get("operation") or "").strip().lower().replace("-", "_")
    path = normalize_repo_path(raw.get("path"))
    if operation not in CONCRETE_OPERATION_NAMES:
        return None, f"unsupported concrete operation: {operation or '(missing)'}"
    error = target_path_error(path, repo_root)
    if error:
        return None, error

    item: dict[str, Any] = {
        "proposal_id": raw.get("proposal_id") or proposal_id,
        "id": raw.get("id") or raw.get("source_id") or proposal_id,
        "path": path,
        "operation": operation,
        "content_status": "concrete_review_ready",
        "draft_status": "concrete_review_ready",
        "source_id": raw.get("source_id") or proposal_id,
        "family": raw.get("family") or "repository_change_proposals",
        "description": raw.get("description") or "concrete operation from repository proposal",
        "require_contains_after": raw.get("require_contains_after") or [],
        "forbid_contains_after": raw.get("forbid_contains_after") or [],
    }

    for key in ("find", "replace", "content"):
        value = raw.get(key)
        if isinstance(value, str):
            item[key] = value
    if operation == "replace_once" and not ("find" in item and "replace" in item):
        return None, "replace_once requires find and replace"
    if operation in {"append_once", "write_file"} and "content" not in item:
        return None, f"{operation} requires content"
    if operation in {"insert_after_once", "insert_before_once"} and not (
        "find" in item and "content" in item
    ):
        return None, f"{operation} requires find and content"
    return item, ""

def concrete_operations_from_proposal(
    proposal: dict[str, Any],
    *,
    proposal_id: str,
    repo_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    operations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    raw_operations = proposal.get("concrete_operations")
    if not isinstance(raw_operations, list):
        return operations, skipped
    for raw in raw_operations:
        if not isinstance(raw, dict):
            skipped.append({"path": "", "reason": "concrete operation is not an object"})
            continue
        operation, error = build_concrete_operation(
            proposal_id=proposal_id, raw=raw, repo_root=repo_root
        )
        if error:
            skipped.append({"path": normalize_repo_path(raw.get("path")), "reason": error})
            continue
        if operation:
            operations.append(operation)
    return operations, skipped

def build_spec_for_proposal(
    *,
    proposal: dict[str, Any],
    proposal_report_path: Path,
    repo_root: Path,
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    proposal_id = str(proposal.get("id") or "proposal")
    operations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    seen_paths: set[str] = set()

    if proposal.get("apply_mode") != EXPECTED_APPLY_MODE:
        skipped.append({"path": "", "reason": "proposal apply_mode is not manual_review_only"})
        return None, skipped

    concrete_ops, concrete_skipped = concrete_operations_from_proposal(
        proposal,
        proposal_id=proposal_id,
        repo_root=repo_root,
    )
    operations.extend(concrete_ops)
    skipped.extend(concrete_skipped)

    concrete_paths = {str(item.get("path") or "") for item in concrete_ops}
    suppress_metadata_outputs = bool(concrete_ops)
    for output in proposal_outputs(proposal):
        path = normalize_repo_path(output.get("path"))
        if path in concrete_paths:
            continue
        if suppress_metadata_outputs:
            skipped.append(
                {
                    "path": path,
                    "reason": "metadata-only companion suppressed because concrete_operations are present",
                }
            )
            continue
        artifact_kind = str(output.get("artifact_kind") or "")
        write_policy = output.get("write_policy")
        if write_policy != EXPECTED_APPLY_MODE:
            skipped.append(
                {
                    "path": path,
                    "reason": "suggestion output write_policy is not manual_review_only",
                }
            )
            continue
        if artifact_kind in SKIPPED_OUTPUT_KINDS:
            skipped.append(
                {
                    "path": path,
                    "reason": f"artifact kind {artifact_kind} is not a concrete file",
                }
            )
            continue
        if artifact_kind not in SUPPORTED_OUTPUT_KINDS:
            skipped.append({"path": path, "reason": f"unsupported artifact kind: {artifact_kind}"})
            continue
        error = target_path_error(path, repo_root)
        if error:
            skipped.append({"path": path, "reason": error})
            continue
        if path in seen_paths:
            skipped.append({"path": path, "reason": "duplicate target path in proposal"})
            continue
        seen_paths.add(path)
        operations.append(build_metadata_operation(proposal_id=proposal_id, output=output))

    if not operations:
        return None, skipped

    draft_status = "concrete_review_ready" if concrete_ops else "needs_concrete_replacements"
    spec = {
        "version": 1,
        "schema_version": 1,
        "kind": SPEC_KIND,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "source_proposal_report": repo_relative(proposal_report_path, repo_root),
        "proposal_id": proposal_id,
        "proposal_title": proposal.get("title") or "",
        "proposal_area": proposal.get("area") or "",
        "proposal_priority": proposal.get("priority") or "",
        "apply_mode": EXPECTED_APPLY_MODE,
        "draft_status": draft_status,
        "provider_execution_performed": False,
        "description": f"Patch spec for {proposal_id}: {proposal.get('title') or 'repository proposal'}",
        "operations": operations,
        "validation_commands": proposal.get("validation_commands") or [],
        "stop_conditions": proposal.get("stop_conditions") or [],
        "do_not_touch": proposal.get("do_not_touch") or [],
        "guardrails": DEFAULT_GUARDRAILS,
        "skipped_targets": skipped,
    }
    return spec, skipped
