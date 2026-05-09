#!/usr/bin/env python3
"""Apply controlled patch bundles.

Bundle schema v1 intentionally supports a small deterministic operation set.
Future IA-Carmine patch bundles should carry only the core patch data; this
runner handles backup, encoding/newline preservation, idempotency, validation,
dry-run reporting and rollback on parser failure.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from Tools.ai.patchkit.anchors import append_once, insert_after_marker, insert_before_marker, replace_once
from Tools.ai.patchkit.filesystem import LoadedText, backup_file, load_text, rel, repo_path, write_text_preserved
from Tools.ai.patchkit.powershell import assert_no_naked_throw, insert_after_invoke_checked, run_parser
from Tools.ai.patchkit.reports import write_json, write_markdown


def load_bundle(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("bundle root must be a JSON object")
    if data.get("kind") != "codemod_patch_bundle":
        raise ValueError("bundle kind must be codemod_patch_bundle")
    if int(data.get("schema_version", 0)) != 1:
        raise ValueError("bundle schema_version must be 1")
    if not isinstance(data.get("operations"), list):
        raise ValueError("bundle operations must be a list")
    return data


def read_fragment(bundle_dir: Path, op: dict[str, Any]) -> str:
    if "content" in op:
        return str(op["content"])
    fragment = op.get("content_file")
    if not fragment:
        raise ValueError("operation requires content or content_file")
    path = repo_path(bundle_dir, str(fragment))
    return path.read_text(encoding="utf-8-sig")


def apply_operation(text: str, op: dict[str, Any], bundle_dir: Path) -> tuple[bool, str, str]:
    operation = str(op.get("operation") or "")
    marker = str(op.get("marker") or "")
    idempotency_marker = str(op.get("idempotency_marker") or marker or "")

    if operation == "insert_after_invoke_checked":
        return insert_after_invoke_checked(text, str(op["label"]), read_fragment(bundle_dir, op), idempotency_marker=idempotency_marker)
    if operation == "insert_before_marker":
        change = insert_before_marker(text, str(op["target_marker"]), read_fragment(bundle_dir, op), idempotency_marker=idempotency_marker)
        return change.changed, change.text, change.reason
    if operation == "insert_after_marker":
        change = insert_after_marker(text, str(op["target_marker"]), read_fragment(bundle_dir, op), idempotency_marker=idempotency_marker)
        return change.changed, change.text, change.reason
    if operation == "replace_once":
        change = replace_once(text, str(op["old"]), str(op["new"]))
        return change.changed, change.text, change.reason
    if operation == "append_once":
        change = append_once(text, read_fragment(bundle_dir, op), idempotency_marker=idempotency_marker)
        return change.changed, change.text, change.reason
    if operation == "assert_marker":
        required = str(op["required_marker"])
        if required not in text:
            raise ValueError(f"required marker missing: {required}")
        return False, text, "assert_marker passed"
    if operation == "assert_no_naked_throw":
        assert_no_naked_throw(text)
        return False, text, "assert_no_naked_throw passed"
    raise ValueError(f"unsupported operation: {operation}")


def run_python_compile(repo_root: Path, files: list[str]) -> tuple[bool, str]:
    if not files:
        return True, ""
    command = [sys.executable, "-m", "py_compile", *files]
    result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True, check=False)
    return result.returncode == 0, result.stdout + result.stderr


def run_git_diff_check(repo_root: Path) -> tuple[bool, str]:
    inside = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_root, capture_output=True, text=True, check=False)
    if inside.returncode != 0:
        return False, "repo-root is not a Git worktree; cannot run git diff --check\n" + inside.stdout + inside.stderr
    result = subprocess.run(["git", "diff", "--check"], cwd=repo_root, capture_output=True, text=True, check=False)
    return result.returncode == 0, result.stdout + result.stderr


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8-sig").splitlines())


def apply_bundle(repo_root: Path, bundle_path: Path, *, dry_run: bool) -> dict[str, Any]:
    bundle = load_bundle(bundle_path)
    bundle_dir = bundle_path.parent
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    changed_count = 0
    backups: list[str] = []
    touched: set[Path] = set()
    loaded_by_target: dict[Path, LoadedText] = {}
    text_by_target: dict[Path, str] = {}

    for index, op in enumerate(bundle["operations"], start=1):
        target_raw = str(op.get("target") or bundle.get("target") or "")
        if not target_raw:
            errors.append(f"operation {index}: missing target")
            continue
        target = repo_path(repo_root, target_raw)
        if not target.exists():
            errors.append(f"operation {index}: target missing: {target_raw}")
            continue
        try:
            if target not in loaded_by_target:
                loaded = load_text(target)
                loaded_by_target[target] = loaded
                text_by_target[target] = loaded.text_lf
            changed, patched, reason = apply_operation(text_by_target[target], op, bundle_dir)
            if changed:
                changed_count += 1
                touched.add(target)
                text_by_target[target] = patched
            results.append({"index": index, "operation": op.get("operation"), "target": target_raw, "changed": changed, "reason": reason})
        except Exception as exc:  # noqa: BLE001
            errors.append(f"operation {index} failed: {type(exc).__name__}: {exc}")

    if not dry_run and not errors:
        for target in sorted(touched):
            backup = backup_file(repo_root, target)
            backups.append(rel(repo_root, backup))
            write_text_preserved(loaded_by_target[target], text_by_target[target])

    validators = bundle.get("validators") or []
    validator_results: list[dict[str, Any]] = []
    if not dry_run and not errors:
        for validator in validators:
            if validator == "powershell_parser":
                for target in sorted(touched):
                    if target.suffix.lower() == ".ps1":
                        ok, output = run_parser(target)
                        validator_results.append({"validator": validator, "target": rel(repo_root, target), "passed": ok, "output_tail": output[-4000:]})
                        if not ok:
                            errors.append(f"PowerShell parser failed for {rel(repo_root, target)}")
            elif validator == "python_compile":
                files = [rel(repo_root, path) for path in sorted(touched) if path.suffix.lower() == ".py"]
                ok, output = run_python_compile(repo_root, files)
                validator_results.append({"validator": validator, "passed": ok, "files": files, "output_tail": output[-4000:]})
                if not ok:
                    errors.append("python compile failed")
            elif validator == "git_diff_check":
                ok, output = run_git_diff_check(repo_root)
                validator_results.append({"validator": validator, "passed": ok, "output_tail": output[-4000:]})
                if not ok:
                    errors.append("git diff --check failed")
            else:
                warnings.append(f"unknown validator ignored: {validator}")

    line_counts = {rel(repo_root, path): line_count(path) for path in sorted(touched) if path.exists() and not dry_run}
    report = {
        "schema_version": 1,
        "kind": "patchkit_apply_report",
        "bundle": rel(repo_root, bundle_path),
        "dry_run": dry_run,
        "operation_count": len(bundle["operations"]),
        "changed_count": changed_count,
        "backups": backups,
        "results": results,
        "validators": validator_results,
        "line_counts": line_counts,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": bool(changed_count and not dry_run),
        "source_writes_performed": bool(changed_count and not dry_run),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--output", default="output/validation/patchkit_apply_report.json")
    parser.add_argument("--markdown-output", default="output/validation/patchkit_apply_report.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    bundle_path = repo_path(repo_root, args.bundle)
    report = apply_bundle(repo_root, bundle_path, dry_run=args.dry_run)
    write_json(repo_path(repo_root, args.output), report)
    write_markdown(repo_path(repo_root, args.markdown_output), report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
