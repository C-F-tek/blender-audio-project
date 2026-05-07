#!/usr/bin/env python3
"""Apply deterministic patch suggestions as the final full-toolbox phase.

The tool is intentionally conservative. It consumes suggestion/proposal JSON,
applies only explicit file-edit operations, and writes a JSON report. Natural
language recommendations are preserved as manual-review items instead of being
converted into source edits.

Supported operations:
- replace_once
- append_once
- insert_after_once
- insert_before_once
- write_file

It never executes providers, Blender, FFmpeg, SQLite workflows, Git commits,
Git pushes, merges, force pushes, deletes, or output artifact promotion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation.report_utils import resolve_output_path, write_json_report
except ImportError:  # pragma: no cover - direct script execution fallback
    from report_utils import resolve_output_path, write_json_report  # type: ignore


DENY_PREFIXES = (
    ".git/",
    "output/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "renders/",
)

DENY_FRAGMENTS = (
    ".sqlite",
    ".sqlite-wal",
    ".sqlite-shm",
    ".db",
)

SUPPORTED_OPERATIONS = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}

DEFAULT_DISCOVER_SUGGESTION_ROOTS = (
    "docs/LOCAL_VALIDATION_EVIDENCE",
    "output/patch_specs",
    "output/validation",
    "output/ai_pipeline",
    "output/ai_packets",
)

DEFAULT_DISCOVER_SUGGESTION_TOKENS = (
    "patch_notes_quality_product",
    "patch_suggestion",
    "suggestion",
    "proposal",
    "recommendation",
    "patch_plan",
    "agent_review",
)


@dataclass
class PatchOperation:
    """Normalized deterministic patch operation."""

    operation: str
    path: str
    content: str | None = None
    find: str | None = None
    replace: str | None = None
    marker: str | None = None
    source_id: str | None = None
    family: str | None = None
    description: str | None = None


def compact_artifact_stamp(stamp: str, max_chars: int = 56) -> str:
    """Match the full-toolbox Python engine artifact-stamp normalization."""
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", stamp.strip() or "run").strip("._-")
    if len(safe) <= max_chars:
        return safe
    digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10]
    head = safe[: max(12, max_chars - len(digest) - 1)].rstrip("._-")
    return f"{head}-{digest}"


def run_git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def current_branch(repo_root: Path) -> str:
    """Return current branch name when available."""
    return run_git(repo_root, "branch", "--show-current") or "unknown"


def git_status_short(repo_root: Path) -> str:
    """Return git status --short output."""
    return run_git(repo_root, "status", "--short")


def split_values(values: list[str] | tuple[str, ...]) -> list[str]:
    """Split repeatable/comma-separated CLI values while preserving order."""
    out: list[str] = []
    for value in values:
        for part in str(value).split(","):
            cleaned = part.strip()
            if cleaned:
                out.append(cleaned)
    return out


def repo_relative(path: Path, repo_root: Path) -> str:
    """Return a normalized repository-relative path."""
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


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


def load_json(path: Path) -> tuple[Any | None, str | None]:
    """Read JSON, returning data or error."""
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")), None
    except Exception as exc:  # noqa: BLE001 - report exact failure
        return None, f"{type(exc).__name__}: {exc}"


def first_string(data: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    """Return the first non-empty string from any accepted key."""
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return None


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
        source_id=first_string(raw, ("id", "suggestion_id", "plan_id")),
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


def discover_operations(data: Any) -> tuple[list[PatchOperation], list[dict[str, Any]]]:
    """Discover supported deterministic operations and manual-review candidates."""
    operations: list[PatchOperation] = []
    manual: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str | None, str | None, str | None]] = set()

    for raw in iter_dicts(data):
        operation = normalize_operation(raw)
        if operation:
            key = (
                operation.operation,
                operation.path,
                operation.find,
                operation.replace,
                operation.content,
            )
            if key not in seen:
                seen.add(key)
                operations.append(operation)
            continue

        family = first_string(raw, ("family", "suggestion_family", "area", "kind"))
        title = first_string(raw, ("title", "description", "rationale", "id"))
        if family or title:
            manual.append(
                {
                    "family": family,
                    "title": title,
                    "reason": "no supported deterministic operation found",
                }
            )

    return operations, manual


def discover_suggestion_reports(
    repo_root: Path,
    stamp: str | None,
    roots: list[str],
    tokens: list[str],
    max_files: int,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Discover local suggestion/proposal JSON reports by compact artifact stamp.

    Discovery is read-only and accepts both Git-tracked evidence under docs and
    local runtime reports under output. Returned paths are repository-relative.
    """
    if not stamp:
        return [], []
    normalized_tokens = [token.lower() for token in tokens if token]
    discovered: list[tuple[float, str]] = []
    scanned: list[dict[str, Any]] = []

    for raw_root in roots:
        root = (repo_root / raw_root).resolve()
        scan_item = {
            "root": raw_root.replace("\\", "/"),
            "exists": root.exists(),
            "json_candidates": 0,
            "matched": 0,
            "error": None,
        }
        if not root.exists():
            scanned.append(scan_item)
            continue
        try:
            root.relative_to(repo_root.resolve())
        except ValueError:
            scan_item["error"] = "root is outside repository"
            scanned.append(scan_item)
            continue

        for path in root.rglob("*.json"):
            scan_item["json_candidates"] += 1
            rel = repo_relative(path, repo_root)
            lower_rel = rel.lower()
            if stamp.lower() not in lower_rel:
                continue
            if normalized_tokens and not any(token in lower_rel for token in normalized_tokens):
                continue
            discovered.append((path.stat().st_mtime, rel))
            scan_item["matched"] += 1
        scanned.append(scan_item)

    deduped: list[str] = []
    seen: set[str] = set()
    for _, rel in sorted(discovered, reverse=True):
        if rel in seen:
            continue
        seen.add(rel)
        deduped.append(rel)
        if len(deduped) >= max_files:
            break
    return deduped, scanned


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
                result["skipped"] = True
                result["ok"] = True
                result["line_count_after"] = line_count(old_text)
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
                result["skipped"] = True
                result["ok"] = True
                result["line_count_after"] = line_count(old_text)
                return result
            count = old_text.count(operation.find)
            if count == 0:
                raise ValueError(f"{operation.operation} anchor not found")
            if count > 1:
                raise ValueError(f"{operation.operation} expected 1 match, found {count}")
            if operation.operation == "insert_after_once":
                new_text = old_text.replace(operation.find, operation.find + operation.content, 1)
            else:
                new_text = old_text.replace(operation.find, operation.content + operation.find, 1)

        elif operation.operation == "write_file":
            if operation.content is None:
                raise ValueError("write_file requires content")
            if exists and old_text == operation.content:
                result["skipped"] = True
                result["ok"] = True
                result["line_count_after"] = line_count(old_text)
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


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--suggestion-report",
        action="append",
        default=[],
        help="Suggestion/proposal JSON path. Repeatable.",
    )
    parser.add_argument(
        "--Stamp",
        default="",
        help="Full-toolbox run stamp. This matches the Python workflow engine parameter.",
    )
    parser.add_argument(
        "--suggestion-stamp",
        default=None,
        help="Backward-compatible alias for --Stamp.",
    )
    parser.add_argument(
        "--discover-suggestion-root",
        action="append",
        default=[],
        help="Root used with --suggestion-stamp. Repeatable or comma-separated.",
    )
    parser.add_argument(
        "--discover-suggestion-token",
        action="append",
        default=[],
        help="Filename/path token used with --suggestion-stamp. Repeatable or comma-separated.",
    )
    parser.add_argument("--discover-max-files", type=int, default=50)
    parser.add_argument("--output", default="output/validation/patch_suggestion_bundle_apply.json")
    parser.add_argument("--apply", action="store_true", help="Actually write source/doc files.")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow applying with dirty git status.")
    parser.add_argument(
        "--allowed-branch-prefix",
        action="append",
        default=["codex/"],
        help="Allowed branch prefix for --apply. Repeatable.",
    )
    return parser.parse_args()


def main() -> int:
    """CLI entrypoint."""
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    branch = current_branch(repo_root)
    status_before = git_status_short(repo_root)
    errors: list[str] = []
    warnings: list[str] = []

    if args.apply and not any(branch.startswith(prefix) for prefix in args.allowed_branch_prefix):
        errors.append(f"refusing --apply on branch {branch!r}; expected allowed prefix")
    if args.apply and status_before and not args.allow_dirty:
        errors.append("refusing --apply with dirty working tree; use --allow-dirty only for reviewed incremental fixes")

    raw_stamp = args.Stamp or args.suggestion_stamp or ""
    artifact_stamp = compact_artifact_stamp(raw_stamp) if raw_stamp else ""

    discover_roots = split_values(args.discover_suggestion_root) or list(DEFAULT_DISCOVER_SUGGESTION_ROOTS)
    discover_tokens = split_values(args.discover_suggestion_token) or list(DEFAULT_DISCOVER_SUGGESTION_TOKENS)
    discovered_reports, discovery_scan = discover_suggestion_reports(
        repo_root,
        artifact_stamp,
        discover_roots,
        discover_tokens,
        int(args.discover_max_files),
    )

    report_paths = split_values(args.suggestion_report)
    for rel in discovered_reports:
        if rel not in report_paths:
            report_paths.append(rel)

    if raw_stamp and not report_paths:
        errors.append(
            "no suggestion/proposal JSON reports found for "
            f"Stamp {raw_stamp!r} (artifact stamp {artifact_stamp!r})"
        )

    loaded_reports: list[dict[str, Any]] = []
    operations: list[PatchOperation] = []
    manual_review: list[dict[str, Any]] = []

    for raw_path in report_paths:
        path = (repo_root / raw_path).resolve()
        data, error = load_json(path)
        report_item = {
            "path": raw_path.replace("\\", "/"),
            "exists": path.exists(),
            "json_ok": error is None,
            "error": error,
        }
        loaded_reports.append(report_item)
        if error:
            errors.append(f"{raw_path}: {error}")
            continue
        discovered, manual = discover_operations(data)
        operations.extend(discovered)
        manual_review.extend(manual)

    if not report_paths:
        warnings.append("no suggestion reports supplied or discovered")

    results = []
    if not errors:
        for operation in operations:
            results.append(apply_operation(repo_root, operation, bool(args.apply)))

    failed = [item for item in results if not item.get("ok")]
    changed = [item for item in results if item.get("changed")]
    applied = [item for item in results if item.get("applied")]

    report = {
        "schema_version": 1,
        "kind": "patch_suggestion_bundle_apply",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "branch": branch,
        "apply_requested": bool(args.apply),
        "Stamp": raw_stamp,
        "artifact_stamp": artifact_stamp,
        "suggestion_stamp": artifact_stamp,
        "discovered_report_count": len(discovered_reports),
        "discovered_reports": discovered_reports,
        "discovery_scan": discovery_scan,
        "provider_execution_performed": False,
        "blender_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "sqlite_writes_performed": False,
        "git_commit_performed": False,
        "git_push_performed": False,
        "patch_application_performed": bool(applied),
        "source_writes_performed": bool(applied),
        "loaded_reports": loaded_reports,
        "operation_count": len(operations),
        "changed_count": len(changed),
        "applied_count": len(applied),
        "failed_count": len(failed),
        "manual_review_required": bool(manual_review or failed),
        "manual_review_items": manual_review[:200],
        "results": results,
        "git_status_before": status_before,
        "git_status_after": git_status_short(repo_root),
        "passed": not errors and not failed,
        "errors": errors + [f"{item['path']}: {item['error']}" for item in failed],
        "warnings": warnings,
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
