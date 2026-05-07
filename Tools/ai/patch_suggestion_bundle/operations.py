"""Patch operation normalization and deterministic application."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai.patch_suggestion_bundle.common import (
    DENY_FRAGMENTS,
    DENY_PREFIXES,
    PROPOSAL_ONLY_OPERATIONS,
    SUPPORTED_OPERATIONS,
    PatchOperation,
    as_string_list,
    first_string,
)


def is_safe_target(path: str) -> tuple[bool, str | None]:
    """Validate that a target path is safe for deterministic source edits."""
    normalized = path.replace("\\", "/").lstrip("/")
    lower = normalized.lower()
    if ".." in Path(normalized).parts:
        return False, "path traversal is not allowed"
    if any(lower.startswith(prefix.lower()) for prefix in DENY_PREFIXES):
        return False, "target is under a denied prefix"
    if any(fragment.lower() in lower for fragment in DENY_FRAGMENTS):
        return False, "target contains a denied database/runtime suffix"
    if not normalized:
        return False, "empty target path"
    return True, None


def resolve_target(repo_root: Path, rel_path: str) -> Path:
    """Resolve a safe target path inside repo_root."""
    target = (repo_root / rel_path).resolve()
    target.relative_to(repo_root.resolve())
    return target


def normalize_operation(raw: dict[str, Any]) -> PatchOperation | None:
    """Convert a raw suggestion dict into a supported PatchOperation."""
    op = first_string(raw, ("operation", "op", "action", "patch_operation", "edit_operation"))
    if not op:
        return None
    op = op.strip().lower().replace("-", "_")
    if op not in SUPPORTED_OPERATIONS:
        return None

    rel_path = first_string(raw, ("path", "target", "target_file", "file", "file_path"))
    if not rel_path:
        return None

    return PatchOperation(
        operation=op,
        path=rel_path,
        content=first_string(raw, ("content", "text", "block", "body", "new_content")),
        find=first_string(raw, ("find", "old", "search", "anchor", "needle")),
        replace=first_string(raw, ("replace", "new", "replacement")),
        marker=first_string(raw, ("marker", "idempotency_marker")),
        source_id=first_string(raw, ("id", "suggestion_id", "plan_id", "proposal_id")),
        family=first_string(raw, ("family", "suggestion_family", "area", "kind")),
        description=first_string(raw, ("description", "rationale", "title")),
    )


def iter_dicts(data: Any) -> list[dict[str, Any]]:
    """Flatten all dictionaries found in JSON-like data."""
    found: list[dict[str, Any]] = []
    if isinstance(data, dict):
        found.append(data)
        for value in data.values():
            found.extend(iter_dicts(value))
    elif isinstance(data, list):
        for value in data:
            found.extend(iter_dicts(value))
    return found


def is_report_container(raw: dict[str, Any]) -> bool:
    """Detect report-root/container dictionaries that should not become manual items."""
    if not isinstance(raw, dict) or "kind" not in raw:
        return False
    container_keys = {
        "schema_version",
        "repo_root",
        "generated_at",
        "passed",
        "errors",
        "warnings",
        "checks",
        "results",
        "reports_read",
        "loaded_reports",
        "workflow",
        "bundle",
    }
    return bool(container_keys.intersection(raw.keys()))


def is_manual_candidate(raw: dict[str, Any]) -> bool:
    """Return true for real suggestion/proposal nodes, not telemetry containers."""
    if not isinstance(raw, dict) or is_report_container(raw):
        return False

    operation = first_string(raw, ("operation", "op", "action", "patch_operation", "edit_operation"))
    if operation and operation.strip().lower().replace("-", "_") in PROPOSAL_ONLY_OPERATIONS:
        return True

    if raw.get("write_policy") == "manual_review_only" or raw.get("content_status") == "proposal_only":
        return True

    proposal_keys = {
        "proposal_id",
        "priority",
        "area",
        "title",
        "rationale",
        "target_files",
        "target_file",
        "patch_sketch",
        "suggestion_outputs",
        "validation_commands",
        "stop_conditions",
        "change_type",
        "apply_mode",
        "details",
    }
    if proposal_keys.intersection(raw.keys()):
        return bool(first_string(raw, ("title", "rationale", "description", "details", "proposal_id", "id")))
    return False


def manual_item(raw: dict[str, Any]) -> dict[str, Any]:
    """Build a compact manual-review item from a suggestion/proposal node."""
    operation = first_string(raw, ("operation", "op", "action", "patch_operation", "edit_operation"))
    target = first_string(raw, ("path", "target", "target_file", "file", "file_path"))
    target_files = as_string_list(raw.get("target_files"))
    if target and target not in target_files:
        target_files.append(target)
    return {
        "id": first_string(raw, ("proposal_id", "id", "suggestion_id", "plan_id")),
        "priority": first_string(raw, ("priority", "severity")),
        "family": first_string(raw, ("family", "suggestion_family", "area", "kind")),
        "title": first_string(raw, ("title", "description", "rationale", "details")),
        "operation": operation,
        "apply_mode": first_string(raw, ("apply_mode", "write_policy", "content_status")),
        "target": target,
        "target_files": target_files,
        "change_type": first_string(raw, ("change_type", "artifact_kind")),
        "patch_sketch": as_string_list(raw.get("patch_sketch")),
        "validation_commands": as_string_list(raw.get("validation_commands")),
        "stop_conditions": as_string_list(raw.get("stop_conditions")),
        "reason": "proposal-only or no supported deterministic operation found",
    }


def discover_operations(data: Any) -> tuple[list[PatchOperation], list[dict[str, Any]]]:
    """Discover supported deterministic operations and manual-review candidates."""
    operations: list[PatchOperation] = []
    manual: list[dict[str, Any]] = []
    seen_operations: set[tuple[str, str, str | None, str | None, str | None]] = set()
    seen_manual: set[str] = set()

    for raw in iter_dicts(data):
        operation = normalize_operation(raw)
        if operation:
            key = (operation.operation, operation.path, operation.find, operation.replace, operation.content)
            if key not in seen_operations:
                seen_operations.add(key)
                operations.append(operation)
            continue

        if is_manual_candidate(raw):
            item = manual_item(raw)
            item_key = repr(sorted(item.items()))
            if item_key not in seen_manual:
                seen_manual.add(item_key)
                manual.append(item)

    return operations, manual


def read_text(path: Path) -> str:
    """Read UTF-8 text with BOM tolerance."""
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    """Write UTF-8 text with final newline preservation controlled by caller."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def line_count(text: str) -> int:
    """Return physical line count."""
    return len(text.splitlines())


def apply_operation(repo_root: Path, operation: PatchOperation, apply: bool) -> dict[str, Any]:
    """Apply or dry-run a single deterministic operation."""
    safe, reason = is_safe_target(operation.path)
    result: dict[str, Any] = {
        "operation": operation.operation,
        "path": operation.path.replace("\\", "/"),
        "source_id": operation.source_id,
        "family": operation.family,
        "description": operation.description,
        "applied": False,
        "changed": False,
        "skipped": False,
        "ok": False,
        "error": None,
        "line_count_after": None,
    }
    if not safe:
        result["error"] = reason
        return result

    try:
        target = resolve_target(repo_root, result["path"])
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"target resolution failed: {type(exc).__name__}: {exc}"
        return result

    exists = target.exists()
    old_text = read_text(target) if exists else ""

    try:
        new_text = old_text
        if operation.operation == "replace_once":
            if operation.find is None or operation.replace is None:
                raise ValueError("replace_once requires find and replace")
            count = old_text.count(operation.find)
            if count == 0:
                raise ValueError("replace_once anchor not found")
            if count > 1:
                raise ValueError(f"replace_once expected 1 match, found {count}")
            new_text = old_text.replace(operation.find, operation.replace, 1)
        elif operation.operation == "append_once":
            if operation.content is None:
                raise ValueError("append_once requires content")
            marker = operation.marker or operation.content
            if marker in old_text:
                result.update({"skipped": True, "ok": True, "line_count_after": line_count(old_text)})
                return result
            separator = "" if not old_text or old_text.endswith("\n") else "\n"
            new_text = old_text + separator + operation.content
            if not new_text.endswith("\n"):
                new_text += "\n"
        elif operation.operation in {"insert_after_once", "insert_before_once"}:
            if operation.find is None or operation.content is None:
                raise ValueError(f"{operation.operation} requires find and content")
            marker = operation.marker or operation.content
            if marker in old_text:
                result.update({"skipped": True, "ok": True, "line_count_after": line_count(old_text)})
                return result
            count = old_text.count(operation.find)
            if count == 0:
                raise ValueError(f"{operation.operation} anchor not found")
            if count > 1:
                raise ValueError(f"{operation.operation} expected 1 match, found {count}")
            insert = operation.find + operation.content
            if operation.operation == "insert_before_once":
                insert = operation.content + operation.find
            new_text = old_text.replace(operation.find, insert, 1)
        elif operation.operation == "write_file":
            if operation.content is None:
                raise ValueError("write_file requires content")
            if exists and old_text == operation.content:
                result.update({"skipped": True, "ok": True, "line_count_after": line_count(old_text)})
                return result
            new_text = operation.content
        else:  # pragma: no cover - guarded by normalize_operation
            raise ValueError(f"unsupported operation: {operation.operation}")

        result["changed"] = new_text != old_text
        result["line_count_after"] = line_count(new_text)
        if apply and result["changed"]:
            write_text(target, new_text)
            result["applied"] = True
        result["ok"] = True
        return result
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result
