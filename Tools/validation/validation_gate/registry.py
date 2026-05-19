"""Central registry for validation, smoke, and gate commands."""

from __future__ import annotations

import argparse
import sys

from .models import GateStep


def build_registered_steps(args: argparse.Namespace) -> list[GateStep]:
    """Return the known validation commands.

    The default registry is intentionally provider-free. Heavy or live-provider
    checks are selectable but not part of the quick gate.
    """
    py = sys.executable
    timeout = int(args.timeout_seconds)
    heavy_timeout = int(args.heavy_timeout_seconds)
    return [
        GateStep(
            name="python_syntax",
            suites=("quick", "refactor", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "check_python_syntax",
                "--repo-root",
                ".",
                "--output",
                "output/validation/python_syntax.json",
            ],
            outputs=("output/validation/python_syntax.json",),
            timeout_seconds=timeout,
            tags=("syntax", "gate"),
        ),
        GateStep(
            name="validation_report_contract",
            suites=("quick", "refactor", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "check_validation_report_contract",
                "--repo-root",
                ".",
                "--report-file",
                "output/validation/python_syntax.json",
                "--output",
                "output/validation/validation_report_contract.json",
            ],
            outputs=("output/validation/validation_report_contract.json",),
            timeout_seconds=timeout,
            tags=("contract", "gate"),
        ),
        GateStep(
            name="docs_links",
            suites=("quick", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "check_docs_links",
                "--repo-root",
                ".",
                "--output",
                "output/validation/docs_links.json",
            ],
            outputs=("output/validation/docs_links.json",),
            timeout_seconds=timeout,
            tags=("docs", "gate"),
        ),
        GateStep(
            name="npu_pipeline_modules",
            suites=("quick", "refactor", "smoke", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "npu_pipeline_modules_check",
                "--repo-root",
                ".",
                "--output",
                "output/validation/npu_pipeline_modules.json",
            ],
            outputs=("output/validation/npu_pipeline_modules.json",),
            timeout_seconds=timeout,
            tags=("npu", "contract", "smoke"),
        ),
        GateStep(
            name="patch_notes_quality_product_smoke",
            suites=("smoke", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "patch_notes_quality_product_smoke",
                "--repo-root",
                ".",
                "--output",
                "output/validation/patch_notes_quality_product_smoke.json",
                "--markdown-output",
                "output/validation/patch_notes_quality_product_smoke.md",
            ],
            outputs=(
                "output/validation/patch_notes_quality_product_smoke.json",
                "output/validation/patch_notes_quality_product_smoke.md",
            ),
            timeout_seconds=timeout,
            tags=("patch-notes", "smoke"),
        ),
        GateStep(
            name="agnostic_ai_tools_smoke_matrix_dry",
            suites=("smoke", "refactor", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "agnostic_ai_tools_smoke_matrix",
                "--repo-root",
                ".",
                "--dry-run",
                "--output",
                "output/validation/agnostic_ai_tools_smoke_matrix.json",
                "--markdown-output",
                "output/validation/agnostic_ai_tools_smoke_matrix.md",
            ],
            outputs=(
                "output/validation/agnostic_ai_tools_smoke_matrix.json",
                "output/validation/agnostic_ai_tools_smoke_matrix.md",
            ),
            timeout_seconds=timeout,
            tags=("ai-tools", "smoke", "dry-run"),
        ),
        GateStep(
            name="agnostic_context_stack_smoke_dry",
            suites=("smoke", "refactor", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "agnostic_context_stack_smoke",
                "--repo-root",
                ".",
                "--dry-run",
                "--output",
                "output/validation/agnostic_context_stack_smoke.json",
                "--markdown-output",
                "output/validation/agnostic_context_stack_smoke.md",
            ],
            outputs=(
                "output/validation/agnostic_context_stack_smoke.json",
                "output/validation/agnostic_context_stack_smoke.md",
            ),
            timeout_seconds=timeout,
            tags=("context-stack", "smoke", "dry-run"),
        ),
        GateStep(
            name="agent_review_patch_plan_full_validation",
            suites=("deep", "all"),
            command=[
                py,
                "-m",
                "Tools.validation",
                "agent_review_patch_plan_full_validation",
                "--repo-root",
                ".",
            ],
            outputs=(
                "output/validation/agent_review_patch_plan_full_validation.json",
                "output/validation/agent_review_patch_plan_full_validation.md",
            ),
            timeout_seconds=heavy_timeout,
            heavy=True,
            tags=("agent-review", "evidence-bundle", "deep"),
        ),
    ]


def select_steps(args: argparse.Namespace) -> list[GateStep]:
    steps = build_registered_steps(args)
    selected = [step for step in steps if args.suite in step.suites]
    if not args.include_heavy:
        selected = [step for step in selected if not step.heavy]
    if not args.include_provider_live:
        selected = [step for step in selected if not step.provider_live]
    if args.only:
        wanted = set(args.only)
        selected = [step for step in selected if step.name in wanted]
    return selected
