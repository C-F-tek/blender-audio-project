from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from .apply import safe_apply_sections
from .report import render_markdown

from .common import (
    DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT,
    INTEGRATED_STATUSES,
    now_iso,
    read_text,
    write_json,
    write_text,
)
from .sections import analyze_section, declared_empty_code_product, split_sections, summarize_sections


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    code_product = Path(args.code_product).expanduser().resolve()
    output = _resolve_output(repo_root, args.output or DEFAULT_OUTPUT)
    markdown = _resolve_output(repo_root, args.markdown_output or DEFAULT_MARKDOWN)
    output_dir = output.parent
    errors: list[str] = []
    warnings: list[str] = []
    text = _read_code_product(code_product, errors)
    empty_code_product = declared_empty_code_product(text)
    raw_sections = split_sections(text)
    sections = [analyze_section(repo_root, output_dir, item) for item in raw_sections]
    initial_status_counts, initial_errors, initial_warnings = summarize_sections(sections)
    safe_apply_report = _safe_apply_report(args, repo_root, output_dir, raw_sections, sections)
    if safe_apply_report.get("performed"):
        sections = [analyze_section(repo_root, output_dir, item) for item in raw_sections]
    status_counts, section_errors, section_warnings = summarize_sections(sections)
    errors.extend(section_errors)
    warnings.extend(section_warnings)
    errors.extend(str(item) for item in safe_apply_report.get("errors", []))
    warnings.extend(str(item) for item in safe_apply_report.get("warnings", []))
    all_integrated = _all_integrated(sections, empty_code_product)
    forward_applicable = _forward_applicable_count(sections)
    needs_review = _needs_review_count(sections)
    _add_terminal_errors(args, sections, empty_code_product, all_integrated, errors, warnings)
    report = _build_report(
        args,
        repo_root,
        code_product,
        text,
        sections,
        empty_code_product,
        status_counts,
        initial_status_counts,
        safe_apply_report,
        all_integrated,
        forward_applicable,
        needs_review,
        errors,
        warnings,
        output,
        markdown,
    )
    write_json(output, report)
    write_text(markdown, render_markdown(report))
    print_report(report)
    return report


def _resolve_output(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _read_code_product(code_product: Path, errors: list[str]) -> str:
    if not code_product.exists():
        errors.append(f"missing code product: {code_product}")
        return ""
    return read_text(code_product)


def _safe_apply_report(
    args: argparse.Namespace,
    repo_root: Path,
    output_dir: Path,
    raw_sections: list[dict[str, str]],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "requested": bool(args.apply_safe),
        "performed": False,
        "applied_count": 0,
    }
    _, initial_errors, _ = summarize_sections(sections)
    if args.apply_safe and not initial_errors:
        report.update(safe_apply_sections(repo_root, output_dir, raw_sections, sections))
    return report


def _all_integrated(sections: list[dict[str, Any]], empty_code_product: bool) -> bool:
    return (not sections and empty_code_product) or bool(sections) and all(
        section.get("status") in INTEGRATED_STATUSES for section in sections
    )


def _forward_applicable_count(sections: list[dict[str, Any]]) -> int:
    return sum(
        1 for section in sections if str(section.get("status") or "").startswith("forward_applicable")
    )


def _needs_review_count(sections: list[dict[str, Any]]) -> int:
    accepted = {*INTEGRATED_STATUSES, "forward_applicable", "forward_applicable_new_file"}
    return sum(1 for section in sections if section.get("status") not in accepted)


def _add_terminal_errors(
    args: argparse.Namespace,
    sections: list[dict[str, Any]],
    empty_code_product: bool,
    all_integrated: bool,
    errors: list[str],
    warnings: list[str],
) -> None:
    if not sections and empty_code_product:
        warnings.append("code product declares zero effective code sections; nothing to apply")
    elif not sections:
        errors.append("no target sections found")
    if args.require_all_integrated and not all_integrated:
        errors.append("not all code product sections are already integrated")


def _build_report(
    args: argparse.Namespace,
    repo_root: Path,
    code_product: Path,
    text: str,
    sections: list[dict[str, Any]],
    empty_code_product: bool,
    status_counts: dict[str, int],
    initial_status_counts: dict[str, int],
    safe_apply_report: dict[str, Any],
    all_integrated: bool,
    forward_applicable: int,
    needs_review: int,
    errors: list[str],
    warnings: list[str],
    output: Path,
    markdown: Path,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "code_product_artifact_intake",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "code_product_path": str(code_product),
        "code_product_lines": len(text.splitlines()) if text else 0,
        "code_product_chars": len(text),
        "target_count": len(sections),
        "empty_code_product": not sections and empty_code_product,
        "status_counts": status_counts,
        "initial_status_counts": initial_status_counts,
        "already_integrated_count": sum(status_counts.get(status, 0) for status in INTEGRATED_STATUSES),
        "forward_applicable_count": forward_applicable,
        "needs_review_count": needs_review,
        "all_integrated": all_integrated,
        "passed": bool((sections or empty_code_product) and not errors),
        "require_all_integrated": bool(args.require_all_integrated),
        "apply_safe_requested": bool(args.apply_safe),
        "safe_apply": safe_apply_report,
        "provider_execution_performed": False,
        "patch_application_performed": bool(safe_apply_report.get("performed")),
        "source_writes_performed": bool(safe_apply_report.get("performed")),
        "git_write_performed": False,
        "errors": errors,
        "warnings": warnings,
        "sections": sections,
        "output": str(output),
        "markdown_output": str(markdown),
    }


def print_report(report: dict[str, Any]) -> None:
    import json

    print(json.dumps(report, indent=2, ensure_ascii=False))
