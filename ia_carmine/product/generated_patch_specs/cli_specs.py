"""Shared CLI specs for generated patch-spec tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .proposal_common import (
    DEFAULT_BASENAME as PROPOSAL_DEFAULT_BASENAME,
    DEFAULT_OUTPUT_DIR as PROPOSAL_DEFAULT_OUTPUT_DIR,
    resolve_repo_path as resolve_proposal_path,
)
from .proposal_manifest import build_patch_specs
from .review_builder import build_reviewed_spec
from .review_common import (
    DEFAULT_BASENAME as REVIEW_DEFAULT_BASENAME,
    DEFAULT_OUTPUT_DIR as REVIEW_DEFAULT_OUTPUT_DIR,
    resolve_repo_path as resolve_review_path,
    sanitize_filename,
)


def _print_summary(summary: dict[str, Any]) -> None:
    print(json.dumps(summary, indent=2))


def run_proposal_cli() -> int:
    parser = argparse.ArgumentParser(description="Build proposal-derived patch specs.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--proposal",
        default="output/ai_pipeline/repository_change_proposals.json",
        help="Repository change proposal JSON report.",
    )
    parser.add_argument("--output-dir", default=PROPOSAL_DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=PROPOSAL_DEFAULT_BASENAME)
    parser.add_argument("--max-proposals", type=int)
    parser.add_argument(
        "--require-concrete",
        action="store_true",
        help="Fail when generated specs contain no concrete deterministic operations.",
    )
    parser.add_argument(
        "--require-provider-execution",
        action="store_true",
        help="Fail unless the proposal report proves provider_work_verified=true.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest = build_patch_specs(
        repo_root=repo_root,
        proposal_path=resolve_proposal_path(repo_root, args.proposal),
        output_dir=resolve_proposal_path(repo_root, args.output_dir),
        basename=args.basename,
        max_proposals=args.max_proposals,
        require_concrete=bool(args.require_concrete),
        require_provider_execution=bool(args.require_provider_execution),
    )
    _print_summary(
        {
            "passed": manifest["passed"],
            "manifest_json": manifest["manifest_json"],
            "manifest_markdown": manifest["manifest_markdown"],
            "patch_spec_count": manifest["patch_spec_count"],
            "concrete_spec_count": manifest["concrete_spec_count"],
            "skipped_target_count": manifest["skipped_target_count"],
        }
    )
    return 0 if manifest["passed"] else 2


def run_review_cli() -> int:
    parser = argparse.ArgumentParser(description="Promote a reviewed generated patch spec.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--draft", required=True, help="Draft proposal patch spec JSON.")
    parser.add_argument("--replacement-plan", required=True, help="Explicit replacement plan JSON.")
    parser.add_argument("--output-dir", default=REVIEW_DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=REVIEW_DEFAULT_BASENAME)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest = build_reviewed_spec(
        repo_root=repo_root,
        draft_path=resolve_review_path(repo_root, args.draft),
        plan_path=resolve_review_path(repo_root, args.replacement_plan),
        output_dir=resolve_review_path(repo_root, args.output_dir),
        basename=sanitize_filename(args.basename),
    )
    _print_summary(
        {
            "passed": manifest["passed"],
            "manifest_json": manifest["manifest_json"],
            "manifest_markdown": manifest["manifest_markdown"],
            "reviewed_spec": manifest["reviewed_spec"],
            "reviewed_spec_count": manifest["reviewed_spec_count"],
        }
    )
    return 0 if manifest["passed"] else 2
