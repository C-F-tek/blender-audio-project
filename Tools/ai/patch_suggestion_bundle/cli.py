"""CLI for deterministic patch suggestion final-phase application."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from tools.ai.patch_suggestion_bundle.common import (
    DEFAULT_DISCOVER_SUGGESTION_ROOTS,
    DEFAULT_DISCOVER_SUGGESTION_TOKENS,
    ReportPathNormalizer,
    compact_artifact_stamp,
    current_branch,
    git_status_short,
    load_json,
    split_values,
    unique_in_order,
)
from tools.ai.patch_suggestion_bundle.discovery import (
    discover_current_suggestion_reports,
    discover_suggestion_reports,
)
from tools.ai.patch_suggestion_bundle.git_branch import (
    create_review_branch,
    push_review_branch,
)
from tools.ai.patch_suggestion_bundle.operations import (
    apply_operation,
    discover_operations,
)
from tools.ai.patch_suggestion_bundle.product import build_manual_review_product
from tools.validation.report_utils import resolve_output_path, write_json_report


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--suggestion-report", action="append", default=[])
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
    parser.add_argument("--discover-suggestion-root", action="append", default=[])
    parser.add_argument("--discover-suggestion-token", action="append", default=[])
    parser.add_argument("--discover-max-files", type=int, default=50)
    parser.add_argument(
        "--no-current-suggestions",
        action="store_true",
        help="Do not include current non-stamped repository suggestion/proposal reports.",
    )
    parser.add_argument(
        "--output", default="output/validation/patch_suggestion_bundle_apply.json"
    )
    parser.add_argument(
        "--apply", action="store_true", help="Actually write source/doc files."
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow applying with dirty git status.",
    )
    parser.add_argument(
        "--create-review-branch",
        default="",
        help="Create and switch to this review branch before processing. No commit is created.",
    )
    parser.add_argument(
        "--allow-dirty-branch",
        action="store_true",
        help="Allow --create-review-branch with local uncommitted changes.",
    )
    parser.add_argument(
        "--push-review-branch",
        action="store_true",
        help="Push the current review branch after processing. No commit or force-push is performed.",
    )
    parser.add_argument("--push-remote", default="origin")
    parser.add_argument(
        "--allowed-branch-prefix",
        action="append",
        default=["CARMINEai/", "codex/"],
        help="Allowed branch prefix for --apply. Repeatable.",
    )
    return parser.parse_args()


def load_reports(
    repo_root: Path, report_paths: list[str], current_reports: list[str]
) -> tuple[
    list[dict[str, object]],
    list[object],
    list[dict[str, object]],
    list[str],
]:
    """Load reports and collect operations/manual-review suggestions."""
    loaded: list[dict[str, object]] = []
    operations: list[object] = []
    manual_review: list[dict[str, object]] = []
    errors: list[str] = []

    for raw_path in report_paths:
        path = (repo_root / raw_path).resolve()
        data, error = load_json(path)
        normalized = raw_path.replace("\\", "/")
        loaded.append(
            {
                "path": normalized,
                "exists": path.exists(),
                "json_ok": error is None,
                "error": error,
                "current_suggestion_report": normalized in current_reports,
            }
        )
        if error:
            errors.append(f"{raw_path}: {error}")
            continue
        discovered, manual = discover_operations(data)
        operations.extend(discovered)
        manual_review.extend(manual)
    return loaded, operations, manual_review, errors


def main() -> int:
    """CLI entrypoint."""
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    branch_prepare = create_review_branch(
        repo_root,
        args.create_review_branch.strip(),
        allowed_prefixes=list(args.allowed_branch_prefix),
        allow_dirty=bool(args.allow_dirty_branch),
    )
    branch = current_branch(repo_root)
    status_before = git_status_short(repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(branch_prepare.get("errors") or [])
    warnings.extend(branch_prepare.get("warnings") or [])

    if args.apply and not any(
        branch.startswith(prefix) for prefix in args.allowed_branch_prefix
    ):
        errors.append(f"refusing --apply on branch {branch!r}; expected allowed prefix")
    if args.apply and status_before and not args.allow_dirty:
        errors.append(
            "refusing --apply with dirty working tree; use --allow-dirty only for reviewed incremental fixes"
        )

    raw_stamp = args.Stamp or args.suggestion_stamp or ""
    artifact_stamp = compact_artifact_stamp(raw_stamp) if raw_stamp else ""
    discover_roots = split_values(args.discover_suggestion_root) or list(
        DEFAULT_DISCOVER_SUGGESTION_ROOTS
    )
    discover_tokens = split_values(args.discover_suggestion_token) or list(
        DEFAULT_DISCOVER_SUGGESTION_TOKENS
    )
    discovered_reports, discovery_scan = discover_suggestion_reports(
        repo_root,
        artifact_stamp,
        discover_roots,
        discover_tokens,
        int(args.discover_max_files),
    )
    current_suggestion_reports = discover_current_suggestion_reports(
        repo_root,
        enabled=not bool(args.no_current_suggestions),
    )
    report_paths = ReportPathNormalizer(repo_root).unique(
        unique_in_order(
            split_values(args.suggestion_report)
            + discovered_reports
            + current_suggestion_reports
        )
    )

    if raw_stamp and not report_paths:
        errors.append(
            "no suggestion/proposal JSON reports found for "
            f"Stamp {raw_stamp!r} (artifact stamp {artifact_stamp!r})"
        )

    loaded_reports, operations, manual_review, load_errors = load_reports(
        repo_root,
        report_paths,
        current_suggestion_reports,
    )
    errors.extend(load_errors)
    if not report_paths:
        warnings.append("no suggestion reports supplied or discovered")

    results = []
    if not errors:
        for operation in operations:
            results.append(apply_operation(repo_root, operation, bool(args.apply)))

    failed = [item for item in results if not item.get("ok")]
    changed = [item for item in results if item.get("changed")]
    applied = [item for item in results if item.get("applied")]
    product = build_manual_review_product(
        manual_review,
        operation_count=len(operations),
        failed_count=len(failed),
    )
    if not product["ready_for_patch_suggestion_review"] and not failed:
        warnings.append(
            "no deterministic operations or product-facing manual patch suggestions found"
        )

    push_result = {"requested": False, "pushed": False, "errors": [], "warnings": []}
    if args.push_review_branch:
        push_result = push_review_branch(
            repo_root,
            branch,
            remote=args.push_remote,
            allowed_prefixes=list(args.allowed_branch_prefix),
        )
        errors.extend(push_result.get("errors") or [])
        warnings.extend(push_result.get("warnings") or [])

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
        "current_suggestion_report_count": len(current_suggestion_reports),
        "current_suggestion_reports": current_suggestion_reports,
        "discovery_scan": discovery_scan,
        "provider_execution_performed": False,
        "blender_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "sqlite_writes_performed": False,
        "git_commit_performed": False,
        "git_push_performed": bool(push_result.get("pushed")),
        "git_review_branch_prepare": branch_prepare,
        "git_review_branch_push": push_result,
        "patch_application_performed": bool(applied),
        "source_writes_performed": bool(applied),
        "loaded_reports": loaded_reports,
        "operation_count": len(operations),
        "changed_count": len(changed),
        "applied_count": len(applied),
        "failed_count": len(failed),
        "manual_review_required": bool(manual_review or failed),
        "manual_review_items": manual_review[:200],
        "manual_review_product": product,
        "patch_product_status": product["patch_product_status"],
        "ready_for_patch_suggestion_review": product[
            "ready_for_patch_suggestion_review"
        ],
        "essential_patch_suggestion_items": product[
            "product_facing_manual_review_items"
        ],
        "supplemental_telemetry_debug_items": product[
            "supplemental_manual_review_items"
        ],
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
