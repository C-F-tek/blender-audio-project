"""Step definitions for agnostic AI tools smoke matrix."""

from __future__ import annotations

import argparse
import sys

from .models import SmokeStep

def build_steps(args: argparse.Namespace) -> list[SmokeStep]:
    py = sys.executable
    work_dir = args.work_dir.replace("\\", "/").rstrip("/")
    memory_inventory_json = f"{work_dir}/agent_memory_inventory.json"
    memory_inventory_md = f"{work_dir}/agent_memory_inventory.md"
    megalithic_json = f"{work_dir}/megalithic_repo_review.json"
    megalithic_md = f"{work_dir}/megalithic_repo_review.md"
    megalithic_proposals = f"{work_dir}/megalithic_repo_review_proposals.json"
    refined_json = f"{work_dir}/megalithic_refined_review.json"
    refined_md = f"{work_dir}/megalithic_refined_review.md"
    refined_proposals = f"{work_dir}/megalithic_refined_proposals.json"
    pr_draft_json = f"{work_dir}/megalithic_review_pr_draft.json"
    pr_draft_md = f"{work_dir}/megalithic_review_pr_draft.md"

    steps = [
        SmokeStep(
            name="agent_memory_inventory",
            command=[
                py,
                "-m",
                "Tools.ai",
                "build_agent_memory_inventory",
                "--repo-root",
                ".",
                "--memory-db",
                args.memory_db,
                "--objective",
                "Smoke-test generic agent memory inventory for IA-Carmine orchestration.",
                "--output",
                memory_inventory_json,
                "--markdown-output",
                memory_inventory_md,
            ],
            expected_outputs=[memory_inventory_json, memory_inventory_md],
            expected_values_by_output={
                memory_inventory_json: {
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "guardrails.sqlite_read_only": True,
                }
            },
        ),
        SmokeStep(
            name="megalithic_repo_review_cpu",
            command=[
                py,
                "-m",
                "Tools.ai",
                "run_megalithic_repo_review",
                "--repo-root",
                ".",
                "--include-all-docs",
                "--include-all-code",
                "--include-raw",
                "--include-output",
                "--include-index",
                "--include-sqlite-memory",
                "--output",
                megalithic_json,
                "--markdown-output",
                megalithic_md,
                "--proposal-output",
                megalithic_proposals,
            ],
            expected_outputs=[megalithic_json, megalithic_md, megalithic_proposals],
            expected_values_by_output={
                megalithic_json: {
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "guardrails.sqlite_memory_read_only": True,
                },
                megalithic_proposals: {
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "apply_mode": "manual_review_only",
                },
            },
            heavy=True,
        ),
        SmokeStep(
            name="megalithic_signal_refinement",
            command=[
                py,
                "-m",
                "Tools.ai",
                "refine_megalithic_review_signals",
                "--review",
                megalithic_json,
                "--proposals",
                megalithic_proposals,
                "--output",
                refined_json,
                "--proposal-output",
                refined_proposals,
                "--markdown-output",
                refined_md,
            ],
            expected_outputs=[refined_json, refined_md, refined_proposals],
            expected_values_by_output={
                refined_json: {
                    "patch_application_performed": False,
                    "guardrails.real_github_pr_created": False,
                },
                refined_proposals: {
                    "patch_application_performed": False,
                    "apply_mode": "manual_review_only",
                },
            },
        ),
        SmokeStep(
            name="megalithic_pr_draft",
            command=[
                py,
                "Tools/ai/build_megalithic_review_pr_draft/cli.py",
                "--review",
                refined_json,
                "--proposals",
                refined_proposals,
                "--output",
                pr_draft_json,
                "--markdown-output",
                pr_draft_md,
                "--base-branch",
                "master",
                "--title-prefix",
                "review",
            ],
            expected_outputs=[pr_draft_json, pr_draft_md],
            expected_values_by_output={
                pr_draft_json: {
                    "patch_application_performed": False,
                    "guardrails.real_github_pr_created": False,
                    "guardrails.manual_review_required": True,
                }
            },
        ),
    ]

    if args.include_ollama_live:
        live_json = f"{work_dir}/megalithic_repo_review_ollama_live.json"
        live_md = f"{work_dir}/megalithic_repo_review_ollama_live.md"
        live_proposals = f"{work_dir}/megalithic_repo_review_ollama_live_proposals.json"
        steps.append(
            SmokeStep(
                name="megalithic_repo_review_ollama_live",
                command=[
                    py,
                    "-m",
                    "Tools.ai",
                    "run_megalithic_repo_review",
                    "--repo-root",
                    ".",
                    "--include-all-docs",
                    "--include-all-code",
                    "--include-raw",
                    "--include-output",
                    "--include-index",
                    "--include-sqlite-memory",
                    "--use-ollama",
                    "--ollama-max-new-tokens",
                    str(args.ollama_max_new_tokens),
                    "--output",
                    live_json,
                    "--markdown-output",
                    live_md,
                    "--proposal-output",
                    live_proposals,
                ],
                expected_outputs=[live_json, live_md, live_proposals],
                expected_values_by_output={
                    live_json: {
                        "provider_execution_performed": True,
                        "patch_application_performed": False,
                    },
                    live_proposals: {
                        "provider_execution_performed": True,
                        "patch_application_performed": False,
                        "apply_mode": "manual_review_only",
                    },
                },
                heavy=True,
                provider_live=True,
            )
        )

    if args.include_workflow:
        workflow_summary = "output/ai_pipeline/local_ai_core_tool_activation_summary.json"
        steps.append(
            SmokeStep(
                name="local_ai_core_tool_activation_workflow",
                command=[
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    ".\\Tools\\workflow\\run_local_ai_core_tool_activation.ps1",
                    "-RunMegalithicReview",
                ],
                expected_outputs=[workflow_summary],
                expected_values_by_output={
                    workflow_summary: {
                        "patch_application_performed": False,
                        "run_megalithic_review": True,
                    }
                },
                heavy=True,
                workflow=True,
            )
        )
    return steps
