#!/usr/bin/env python3
"""Validate PatchKit bundle contracts before local apply.

The validator is report-only: it does not execute providers, apply patches,
write source files, delete files, or run bundle validators. It checks that a
PatchKit bundle is syntactically usable and that operations remain explicit,
guarded and inside the repository safety perimeter.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

ALLOWED_OPERATIONS = {
    "insert_after_invoke_checked",
    "insert_before_marker",
    "insert_after_marker",
    "replace_once",
    "append_once",
    "assert_marker",
    "assert_no_naked_throw",
    "delete_file",
}
DESTRUCTIVE_OPERATIONS = {"delete_file"}
ALLOWED_VALIDATORS = {"powershell_parser", "python_compile", "git_diff_check"}
DENIED_TARGET_PREFIXES = (
    "output/",
    "renders/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)
DENIED_TARGET_SUFFIXES = (".db", ".sqlite", ".sqlite3")
CONTENT_OPERATIONS = {
    "insert_after_invoke_checked",
    "insert_before_marker",
    "insert_after_marker",
    "append_once",
}


def repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix().replace("\\", "/")


def normalize_target(raw: Any) -> str:
    return str(raw or "").replace("\\", "/").lstrip("./")


def load_bundle(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "bundle missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "bundle root must be a JSON object"
    return data, None


def target_is_denied(target: str) -> str:
    if any(target.startswith(prefix) for prefix in DENIED_TARGET_PREFIXES):
        return f"denied target prefix: {target}"
    if target.endswith(DENIED_TARGET_SUFFIXES):
        return f"denied target suffix: {target}"
    if not target or target.startswith("../") or "/../" in target:
        return f"target escapes repository or is empty: {target}"
    return ""


def validate_fragment(repo_root: Path, bundle_dir: Path, op: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if "content" in op:
        return errors
    content_file = str(op.get("content_file") or "")
    if not content_file:
        errors.append("content operation requires content or content_file")
        return errors
    normalized = normalize_target(content_file)
    if normalized.startswith("../") or "/../" in normalized:
        errors.append(f"content_file escapes bundle directory: {content_file}")
        return errors
    fragment_path = repo_path(bundle_dir, content_file)
    if not fragment_path.exists() or not fragment_path.is_file():
        errors.append(f"content_file missing: {rel(repo_root, fragment_path)}")
    return errors


def validate_operation(
    repo_root: Path, bundle_dir: Path, bundle: dict[str, Any], index: int, op: Any
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(op, dict):
        return {
            "index": index,
            "passed": False,
            "operation": "",
            "target": "",
            "errors": ["operation must be a JSON object"],
            "warnings": [],
        }

    operation = str(op.get("operation") or "")
    target = normalize_target(op.get("target") or bundle.get("target"))
    if operation not in ALLOWED_OPERATIONS:
        errors.append(f"unsupported operation: {operation}")
    denied = target_is_denied(target)
    if denied:
        errors.append(denied)

    if operation in CONTENT_OPERATIONS:
        errors.extend(validate_fragment(repo_root, bundle_dir, op))
        marker = str(op.get("idempotency_marker") or op.get("marker") or "")
        if not marker:
            warnings.append("content operation has no marker/idempotency_marker")

    if operation == "insert_after_invoke_checked" and not str(op.get("label") or ""):
        errors.append("insert_after_invoke_checked requires label")
    if operation in {"insert_before_marker", "insert_after_marker"} and not str(
        op.get("target_marker") or ""
    ):
        errors.append(f"{operation} requires target_marker")
    if operation == "replace_once" and ("old" not in op or "new" not in op):
        errors.append("replace_once requires old and new")
    if operation == "assert_marker" and not str(op.get("required_marker") or ""):
        errors.append("assert_marker requires required_marker")
    if operation == "delete_file":
        if op.get("allow_delete") is not True:
            errors.append("delete_file requires allow_delete=true")
        if not str(op.get("required_marker") or "") and not bool(op.get("missing_ok")):
            errors.append("delete_file requires required_marker unless missing_ok=true")

    return {
        "index": index,
        "operation": operation,
        "target": target,
        "destructive": operation in DESTRUCTIVE_OPERATIONS,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PatchKit Bundle Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Bundle: `{report.get('bundle')}`",
        f"- Operation count: `{report.get('operation_count')}`",
        f"- Destructive operation count: `{report.get('destructive_operation_count')}`",
        "",
        "## Operations",
        "",
        "| # | Operation | Target | Destructive | Passed |",
        "|---:|---|---|---:|---:|",
    ]
    for item in report.get("operations", []):
        lines.append(
            f"| {item.get('index')} | `{item.get('operation')}` | `{item.get('target')}` | `{item.get('destructive')}` | `{item.get('passed')}` |"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def validate_bundle(repo_root: Path, bundle_path: Path) -> dict[str, Any]:
    bundle, load_error = load_bundle(bundle_path)
    operations: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    if load_error:
        errors.append(load_error)
        bundle = {}

    if bundle.get("kind") != "codemod_patch_bundle":
        errors.append("bundle kind must be codemod_patch_bundle")
    if int(bundle.get("schema_version") or 0) != 1:
        errors.append("bundle schema_version must be 1")

    raw_operations = bundle.get("operations")
    if not isinstance(raw_operations, list):
        errors.append("bundle operations must be a list")
        raw_operations = []
    if len(raw_operations) == 0:
        warnings.append("bundle has zero operations")

    validators = bundle.get("validators") or []
    if not isinstance(validators, list):
        errors.append("bundle validators must be a list when present")
        validators = []
    for validator in validators:
        if str(validator) not in ALLOWED_VALIDATORS:
            warnings.append(f"unknown validator will be ignored by current runner: {validator}")

    bundle_dir = bundle_path.parent
    for index, op in enumerate(raw_operations, start=1):
        result = validate_operation(repo_root, bundle_dir, bundle, index, op)
        operations.append(result)
        errors.extend(f"operation {index}: {error}" for error in result["errors"])
        warnings.extend(f"operation {index}: {warning}" for warning in result["warnings"])

    destructive_count = sum(1 for item in operations if item.get("destructive"))
    return {
        "schema_version": 1,
        "kind": "patchkit_bundle_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "bundle": rel(repo_root, bundle_path),
        "operation_count": len(raw_operations),
        "destructive_operation_count": destructive_count,
        "validators": [str(item) for item in validators],
        "operations": operations,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a PatchKit bundle contract without applying it."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--output", default="output/validation/patchkit_bundle_contract.json")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    bundle_path = repo_path(repo_root, args.bundle)
    report = validate_bundle(repo_root, bundle_path)
    print(write_json_report(report, resolve_output_path(repo_root, args.output)), end="")
    if args.markdown_output:
        write_text_report(
            render_markdown(report), resolve_output_path(repo_root, args.markdown_output)
        )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
