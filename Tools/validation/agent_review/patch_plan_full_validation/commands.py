"""Command plan for agent review patch-plan full validation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .common import bundle_paths

def build_commands(
    args: argparse.Namespace, repo_root: Path
) -> tuple[list[tuple[str, list[str], int]], Path, Path]:
    bundle_json, bundle_md = bundle_paths(repo_root, args.evidence_output_dir, args.bundle_basename)
    commands: list[tuple[str, list[str], int]] = [
        (
            "agent_review_patch_plan_smoke",
            [
                sys.executable,
                "Tools/validation/agent_review/patch_plan_smoke/cli.py",
                "--repo-root",
                ".",
                "--orchestrator",
                args.orchestrator,
                "--evidence",
                args.evidence,
                "--min-patch-plans",
                str(args.min_patch_plans),
                "--tool-output",
                args.patch_plan,
                "--tool-markdown-output",
                args.patch_plan_markdown,
                "--output",
                args.smoke_output,
                "--markdown-output",
                args.smoke_markdown_output,
            ]
            + (["--expect-fallback"] if args.expect_fallback else []),
            args.timeout_seconds,
        ),
        (
            "docs_links",
            [
                sys.executable,
                "Tools/validation/check_docs_links/cli.py",
                "--repo-root",
                ".",
                "--output",
                args.docs_links_output,
            ],
            args.timeout_seconds,
        ),
        (
            "python_syntax",
            [
                sys.executable,
                "Tools/validation/check_python_syntax/cli.py",
                "--repo-root",
                ".",
                "--output",
                args.python_syntax_output,
            ],
            args.timeout_seconds,
        ),
        (
            "validation_report_contract",
            [
                sys.executable,
                "Tools/validation/check_validation_report_contract/cli.py",
                "--repo-root",
                ".",
                "--output",
                args.validation_report_contract_output,
            ],
            args.timeout_seconds,
        ),
        (
            "build_github_evidence_bundle",
            [
                sys.executable,
                "Tools/ai/build_github_evidence_bundle/cli.py",
                "--repo-root",
                ".",
                "--basename",
                args.bundle_basename,
                "--output-dir",
                args.evidence_output_dir,
                "--report",
                args.patch_plan,
                "--report",
                args.smoke_output,
                "--report",
                args.docs_links_output,
                "--report",
                args.python_syntax_output,
                "--report",
                args.validation_report_contract_output,
                "--selected-chunks-evidence",
                "__agent_review_patch_plan_no_selected_chunks__",
            ],
            args.timeout_seconds,
        ),
        (
            "check_github_evidence_bundle",
            [
                sys.executable,
                "Tools/validation/check_github_evidence_bundle/cli.py",
                "--repo-root",
                ".",
                "--bundle",
                str(bundle_json),
                "--output",
                args.bundle_validation_output,
            ],
            args.timeout_seconds,
        ),
        (
            "git_diff_check",
            ["git", "diff", "--check"],
            args.git_timeout_seconds,
        ),
        (
            "git_status_short",
            ["git", "status", "--short"],
            args.git_timeout_seconds,
        ),
    ]
    return commands, bundle_json, bundle_md
