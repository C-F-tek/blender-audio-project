"""Declarative report CLI specs for agent-review tools."""

from __future__ import annotations

import argparse
from typing import Any

from .cli_output import run_report_cli
from .evidence_common import (
    DEFAULT_MARKDOWN as EVIDENCE_DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT as EVIDENCE_DEFAULT_OUTPUT,
    DEFAULT_REFINED_PROPOSALS,
    DEFAULT_REFINED_REVIEW,
    resolve_path as resolve_evidence_path,
)
from .evidence_report import build_report as build_evidence_report
from .evidence_report import render_markdown as render_evidence_markdown
from .patch_bundle_builder import build_bundle, render_markdown as render_patch_bundle_markdown
from .patch_bundle_common import (
    DEFAULT_BASENAME,
    DEFAULT_MARKDOWN as PATCH_BUNDLE_DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT as PATCH_BUNDLE_DEFAULT_OUTPUT,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PATCH_PLAN,
    resolve_path as resolve_patch_bundle_path,
)


def _configure_evidence_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--refined-review", default=DEFAULT_REFINED_REVIEW)
    parser.add_argument("--refined-proposals", default=DEFAULT_REFINED_PROPOSALS)
    parser.add_argument("--report-file", action="append", default=[])


def _evidence_summary(report: dict[str, Any], output, markdown) -> dict[str, Any]:
    decision = report["decision"]
    return {
        "passed": report["passed"],
        "output": str(output),
        "markdown": str(markdown),
        "ready_for_manual_patch_count": decision["ready_for_manual_patch_count"],
        "needs_more_context_count": decision["needs_more_context_count"],
        "sufficient_for_real_pr": decision["sufficient_for_real_pr"],
        "provider_execution_performed": False,
        "patch_application_performed": False,
    }


def _configure_patch_bundle_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--patch-plan", default=DEFAULT_PATCH_PLAN)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    parser.add_argument("--stamp", default="")
    parser.add_argument("--write-bundle", action="store_true")


def _patch_bundle_summary(report: dict[str, Any], output, markdown) -> dict[str, Any]:
    return {
        "passed": report["passed"],
        "errors": report["errors"],
        "warnings": report["warnings"],
        "output": str(output),
        "markdown": str(markdown),
        "bundle_zip": report.get("bundle_zip"),
        "operation_count": report["operation_count"],
        "skipped_candidate_count": report["skipped_candidate_count"],
        "patch_application_performed": report["patch_application_performed"],
        "sqlite_write_performed": report["sqlite_write_performed"],
    }


def run_report_tool(tool_name: str) -> int:
    if tool_name == "evidence_sufficiency":
        return run_report_cli(
            configure_parser=_configure_evidence_parser,
            build_report=build_evidence_report,
            render_markdown=render_evidence_markdown,
            build_summary=_evidence_summary,
            resolve_path=resolve_evidence_path,
            default_output=EVIDENCE_DEFAULT_OUTPUT,
            default_markdown=EVIDENCE_DEFAULT_MARKDOWN,
            description="Build agent-review evidence sufficiency reports.",
        )
    if tool_name == "patch_bundle":
        return run_report_cli(
            configure_parser=_configure_patch_bundle_parser,
            build_report=build_bundle,
            render_markdown=render_patch_bundle_markdown,
            build_summary=_patch_bundle_summary,
            resolve_path=resolve_patch_bundle_path,
            default_output=PATCH_BUNDLE_DEFAULT_OUTPUT,
            default_markdown=PATCH_BUNDLE_DEFAULT_MARKDOWN,
            description="Build agent-review manual patch bundles.",
        )
    raise ValueError(f"unknown agent-review report tool: {tool_name}")
