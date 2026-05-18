#!/usr/bin/env python3
"""Validate that review PR preparation has concrete product inputs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def load_json(path: Path) -> tuple[dict[str, Any] | None, str]:
    if not path.exists() or not path.is_file():
        return None, f"missing file: {path.as_posix()}"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "JSON root must be an object"
    return data, ""


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# Review PR Product Readiness",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Args report passed: `{report.get('args_report_passed')}`",
        f"- Has explicit product paths: `{report.get('has_product_paths')}`",
        f"- Has apply report: `{report.get('has_apply_report')}`",
        f"- Apply report product: `{report.get('apply_report_product')}`",
        f"- Require product input: `{report.get('require_product_input')}`",
        f"- Prepare entrypoint referenced: `{report.get('prepare_entrypoint_referenced')}`",
        f"- Prepare entrypoint reference count: `{report.get('prepare_entrypoint_reference_count')}`",
        f"- Required prepare flags present: `{report.get('required_prepare_flags_present')}`",
        f"- Review PR args ready: `{report.get('review_pr_args_ready')}`",
        f"- Prepare review PR ready: `{report.get('prepare_review_pr_ready')}`",
        "",
        "## Derived",
        "",
    ]
    for key, value in sorted((report.get("derived") or {}).items()):
        lines.append(f"- `{key}`: `{value}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(repo_root: Path, args_report_path: Path) -> dict[str, Any]:
    data, error = load_json(args_report_path)
    errors: list[str] = []
    warnings: list[str] = []
    if error:
        errors.append(error)
        data = {}

    derived = data.get("derived") if isinstance(data, dict) else {}
    if not isinstance(derived, dict):
        derived = {}
        errors.append("args report missing derived object")

    argv = data.get("argv") if isinstance(data, dict) else []
    include_path_count = int(derived.get("include_path_count") or 0)
    apply_report = str(derived.get("apply_report") or "")
    apply_report_product = bool(derived.get("apply_report_product"))
    require_product_input = bool(derived.get("require_product_input"))
    args_report_passed = bool(data.get("passed")) if isinstance(data, dict) else False

    has_product_paths = include_path_count > 0
    has_apply_report = bool(apply_report)
    has_product_input = has_product_paths or has_apply_report
    has_concrete_product = has_product_paths or (has_apply_report and apply_report_product)

    argv_items = [str(item) for item in argv] if isinstance(argv, list) else []
    normalized_argv = [item.replace("\\", "/") for item in argv_items]
    prepare_reference_count = sum(
        1
        for index, item in enumerate(normalized_argv)
        if item.endswith("Tools/ai/agent_review/review_pr_cli.py")
        or (
            item == "agent_review_prepare_pr"
            and index >= 2
            and normalized_argv[index - 2 : index] == ["-m", "Tools.ai"]
        )
    )
    prepare_referenced = prepare_reference_count == 1
    required_prepare_flags = ["--repo-root", "--branch", "--output"]
    missing_prepare_flags = [flag for flag in required_prepare_flags if flag not in argv_items]
    required_prepare_flags_present = not missing_prepare_flags

    if not args_report_passed:
        errors.append("review PR args report did not pass")
    if require_product_input and not has_product_input:
        errors.append("review PR product input missing: no include paths and no apply report")
    if (
        require_product_input
        and has_apply_report
        and not has_product_paths
        and not apply_report_product
    ):
        errors.append("review PR apply report is present but not concrete")
    if prepare_reference_count == 0:
        errors.append("agent_review_prepare_pr entrypoint is not referenced by argv")
    elif prepare_reference_count > 1:
        errors.append("agent_review_prepare_pr entrypoint is referenced more than once by argv")
    if missing_prepare_flags:
        errors.append(
            "agent_review_prepare_pr argv missing required flags: " + ", ".join(missing_prepare_flags)
        )

    review_pr_args_ready = args_report_passed and prepare_referenced
    prepare_review_pr_ready = review_pr_args_ready and (
        not require_product_input or has_concrete_product
    )

    return {
        "schema_version": 1,
        "kind": "review_pr_product_readiness",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "args_report": args_report_path.as_posix(),
        "args_report_passed": args_report_passed,
        "has_product_paths": has_product_paths,
        "has_apply_report": has_apply_report,
        "apply_report_product": apply_report_product,
        "require_product_input": require_product_input,
        "prepare_entrypoint_referenced": prepare_referenced,
        "prepare_entrypoint_reference_count": prepare_reference_count,
        "prepare_script_referenced": prepare_referenced,
        "prepare_script_reference_count": prepare_reference_count,
        "required_prepare_flags_present": required_prepare_flags_present,
        "missing_prepare_flags": missing_prepare_flags,
        "review_pr_args_ready": review_pr_args_ready,
        "prepare_review_pr_ready": prepare_review_pr_ready,
        "derived": {
            "include_path_count": include_path_count,
            "apply_report": apply_report,
            "has_product_input": has_product_input,
            "has_concrete_product": has_concrete_product,
            "argv_count": len(argv) if isinstance(argv, list) else 0,
            "required_prepare_flags": required_prepare_flags,
        },
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors and prepare_review_pr_ready,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--args-report", required=True)
    parser.add_argument("--output", default="output/validation/review_pr_product_readiness.json")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    args_report = Path(args.args_report)
    if not args_report.is_absolute():
        args_report = repo_root / args_report

    report = build_report(repo_root, args_report)
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
