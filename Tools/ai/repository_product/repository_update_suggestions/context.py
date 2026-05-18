"""Context collection for repository update suggestions."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .common import (
    IGNORED_PLAN_FILENAMES,
    PROFILE_CONTEXT_FILES,
    PROFILE_REPORTS,
    compact_report_summary,
    read_json_if_exists,
    read_text_if_exists,
    unique_items,
)
from .routing import build_advisory_context_routing

def collect_context(
    repo_root: Path,
    *,
    profile: str,
    context_files: list[str],
    report_files: list[str],
    extra_context: list[str],
    extra_reports: list[str],
    max_chars: int,
) -> dict[str, Any]:
    requested_context_files = unique_items(
        list(PROFILE_CONTEXT_FILES.get(profile, ())) + context_files + extra_context
    )
    all_report_files = unique_items(
        list(PROFILE_REPORTS.get(profile, ())) + report_files + extra_reports
    )

    advisory_routing = build_advisory_context_routing(repo_root, requested_context_files)
    trusted_context_files = unique_items(
        [
            str(item.get("path"))
            for item in advisory_routing.get("trusted_context_files", [])
            if item.get("path")
        ]
    )

    docs = [
        read_text_if_exists(repo_root / rel, max_chars=max_chars) for rel in trusted_context_files
    ]
    reports_raw = [read_json_if_exists(repo_root / rel) for rel in all_report_files]

    active_dir = repo_root / "docs" / "EXECUTION_PLANS" / "active"
    completed_dir = repo_root / "docs" / "EXECUTION_PLANS" / "completed"
    active_plans = (
        [
            path
            for path in sorted(active_dir.glob("*.md"))
            if path.name not in IGNORED_PLAN_FILENAMES
        ]
        if active_dir.exists()
        else []
    )
    completed_plans = (
        [
            path
            for path in sorted(completed_dir.glob("*.md"))
            if path.name not in IGNORED_PLAN_FILENAMES
        ]
        if completed_dir.exists()
        else []
    )

    return {
        "schema_version": 1,
        "kind": "post_validation_ai_work_packet_context",
        "profile": profile,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "requested_context_files": requested_context_files,
        "context_files": trusted_context_files,
        "excluded_context_files": [
            item.get("path")
            for item in advisory_routing.get("excluded_context_files", [])
            if item.get("path")
        ],
        "advisory_context_routing": advisory_routing,
        "report_files": all_report_files,
        "docs": docs,
        "validation_reports": [compact_report_summary(report) for report in reports_raw],
        "execution_plans": {
            "active": [path.relative_to(repo_root).as_posix() for path in active_plans],
            "completed_tail": [
                path.relative_to(repo_root).as_posix() for path in completed_plans[-30:]
            ],
        },
    }
