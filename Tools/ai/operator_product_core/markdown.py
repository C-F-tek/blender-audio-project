"""Markdown renderers for operator product reports."""

from __future__ import annotations

from typing import Any


def render_run_markdown(report: dict[str, Any]) -> str:
    summary = (
        report.get("launcher_summary_payload")
        if isinstance(report.get("launcher_summary_payload"), dict)
        else {}
    )
    lines = [
        "# Operator Product Launcher Run",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Profile: `{report.get('profile_name')}`",
        f"- Request file: `{report.get('request_file')}`",
        f"- Run dir: `{report.get('intermediate_run_dir')}`",
        f"- Code product: `{report.get('code_product')}`",
        f"- Final readable passed: `{summary.get('final_readable_product_passed')}`",
        f"- Packaging succeeded: `{summary.get('launcher_packaging_succeeded')}`",
    ]
    result = report.get("run_result") if isinstance(report.get("run_result"), dict) else {}
    lines.extend(
        [
            f"- Live flow status: `{result.get('flow_status_markdown') or ''}`",
            f"- CRLF warnings compressed: `{result.get('crlf_warning_count') or 0}`",
            f"- Interrupted by operator: `{result.get('keyboard_interrupt') or False}`",
        ]
    )
    if result.get("returncode") not in (0, None):
        lines.extend(
            ["", "## Stderr Tail", "", "```text", str(result.get("stderr_tail") or ""), "```"]
        )
    return "\n".join(lines) + "\n"


def render_lab_markdown(report: dict[str, Any]) -> str:
    metrics = report.get("code_product_metrics")
    if not isinstance(metrics, dict):
        metrics = {}
    review = report.get("review_report")
    if not isinstance(review, dict):
        review = {}
    lines = [
        "# Operator Product Lab Summary",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Profile: `{report.get('profile_name')}`",
        f"- Run dir: `{report.get('intermediate_run_dir')}`",
        f"- Code product: `{report.get('code_product')}`",
        f"- Code product exists: `{metrics.get('exists')}`",
        f"- Diff git blocks: `{metrics.get('diff_git_blocks')}`",
        f"- Empty marker: `{metrics.get('empty_code_product_marker')}`",
        f"- No applicable marker: `{metrics.get('no_applicable_marker')}`",
        f"- Review passed: `{review.get('passed')}`",
        f"- Forward-applicable count: `{review.get('forward_applicable_count')}`",
        f"- Patch application performed: `{review.get('patch_application_performed')}`",
        f"- Source writes performed: `{review.get('source_writes_performed')}`",
    ]
    apply_report = report.get("safe_apply_report")
    if isinstance(apply_report, dict):
        lines.extend(
            [
                "",
                "## Safe Apply",
                "",
                f"- Passed: `{apply_report.get('passed')}`",
                f"- Patch application performed: `{apply_report.get('patch_application_performed')}`",
                f"- Source writes performed: `{apply_report.get('source_writes_performed')}`",
            ]
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"
