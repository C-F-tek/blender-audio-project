"""Step definitions for agnostic context stack smoke."""

from __future__ import annotations

import argparse
import sys
from typing import Any

def build_step_specs(args: argparse.Namespace) -> list[tuple[str, list[str], dict[str, dict[str, Any]]]]:
    py = sys.executable
    work_dir = args.work_dir.replace("\\", "/").rstrip("/")
    memory_json = f"{work_dir}/agent_memory_inventory.json"
    memory_md = f"{work_dir}/agent_memory_inventory.md"
    tool_json = f"{work_dir}/agent_agnostic_tool_inventory.json"
    tool_md = f"{work_dir}/agent_agnostic_tool_inventory.md"
    transient_json = f"{work_dir}/agent_transient_request_context.json"
    transient_md = f"{work_dir}/agent_transient_request_context.md"
    review_json = f"{work_dir}/megalithic_repo_review.json"
    review_md = f"{work_dir}/megalithic_repo_review.md"
    review_props = f"{work_dir}/megalithic_repo_review_proposals.json"
    refined_json = f"{work_dir}/megalithic_refined_review.json"
    refined_md = f"{work_dir}/megalithic_refined_review.md"
    refined_props = f"{work_dir}/megalithic_refined_proposals.json"
    pr_draft_json = f"{work_dir}/megalithic_review_pr_draft.json"
    pr_draft_md = f"{work_dir}/megalithic_review_pr_draft.md"

    step_specs = [
        (
            "agent_memory_inventory",
            [
                py,
                "-m",
                "ia_carmine",
                "build_agent_memory_inventory",
                "--repo-root",
                ".",
                "--memory-db",
                args.memory_db,
                "--objective",
                args.objective,
                "--output",
                memory_json,
                "--markdown-output",
                memory_md,
            ],
            {
                memory_json: {
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "guardrails.sqlite_read_only": True,
                }
            },
        ),
        (
            "agent_agnostic_tool_inventory",
            [
                py,
                "ia_carmine/context/agent_context/agnostic_tool_inventory/cli.py",
                "--repo-root",
                ".",
                "--output",
                tool_json,
                "--markdown-output",
                tool_md,
            ],
            {
                tool_json: {
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "guardrails.report_only": True,
                }
            },
        ),
        (
            "agent_transient_request_context",
            [
                py,
                "ia_carmine/context/agent_context/transient_request_context/cli.py",
                "--repo-root",
                ".",
                "--objective",
                args.objective,
                "--memory-note",
                args.objective,
                "--report-file",
                memory_json,
                "--report-file",
                tool_json,
                "--output",
                transient_json,
                "--markdown-output",
                transient_md,
            ],
            {
                transient_json: {
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "guardrails.request_scoped": True,
                    "persistence.sqlite_write_performed": False,
                }
            },
        ),
        (
            "megalithic_repo_review_with_agnostic_context",
            [
                py,
                "-m",
                "ia_carmine",
                "megalithic_repo_review",
                "--repo-root",
                ".",
                "--include-all-docs",
                "--include-all-code",
                "--include-raw",
                "--include-output",
                "--include-index",
                "--include-sqlite-memory",
                "--report-file",
                memory_json,
                "--report-file",
                tool_json,
                "--report-file",
                transient_json,
                "--output",
                review_json,
                "--markdown-output",
                review_md,
                "--proposal-output",
                review_props,
            ],
            {
                review_json: {
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "guardrails.sqlite_memory_read_only": True,
                },
                review_props: {
                    "patch_application_performed": False,
                    "apply_mode": "manual_review_only",
                },
            },
        ),
        (
            "megalithic_signal_refinement",
            [
                py,
                "-m",
                "ia_carmine",
                "megalithic_review_refinement",
                "--review",
                review_json,
                "--proposals",
                review_props,
                "--output",
                refined_json,
                "--proposal-output",
                refined_props,
                "--markdown-output",
                refined_md,
            ],
            {
                refined_json: {
                    "patch_application_performed": False,
                    "guardrails.real_github_pr_created": False,
                },
                refined_props: {
                    "patch_application_performed": False,
                    "apply_mode": "manual_review_only",
                },
            },
        ),
        (
            "megalithic_pr_draft",
            [
                py,
                "ia_carmine/product/repository_product/megalithic_review_pr_draft/cli.py",
                "--review",
                refined_json,
                "--proposals",
                refined_props,
                "--output",
                pr_draft_json,
                "--markdown-output",
                pr_draft_md,
                "--base-branch",
                "master",
                "--title-prefix",
                "review",
            ],
            {
                pr_draft_json: {
                    "patch_application_performed": False,
                    "guardrails.real_github_pr_created": False,
                    "guardrails.manual_review_required": True,
                }
            },
        ),
    ]
    return step_specs
