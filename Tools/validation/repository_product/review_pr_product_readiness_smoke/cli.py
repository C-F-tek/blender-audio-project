#!/usr/bin/env python3
"""Smoke-test review PR product readiness gate."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_checker(
    source_repo: Path, repo: Path, payload: dict[str, Any], name: str
) -> dict[str, Any]:
    args_report = repo / f"output/validation/{name}_args.json"
    output = repo / f"output/validation/{name}_readiness.json"
    markdown = repo / f"output/validation/{name}_readiness.md"
    write_json(args_report, payload)

    env = dict(os.environ)
    env["PYTHONPATH"] = str(source_repo)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "Tools.validation",
            "check_review_pr_product_readiness",
            "--repo-root",
            str(repo),
            "--args-report",
            str(args_report),
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    report = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
    return {
        "name": name,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "report": report,
        "markdown_exists": markdown.exists(),
    }


def args_payload(
    *,
    include_count: int,
    apply_report: str,
    apply_product: bool,
    passed: bool = True,
    argv: list[str] | None = None,
) -> dict[str, Any]:
    if argv is None:
        argv = [
            "-m",
            "ia_carmine.cli",
            "agent_review_prepare_pr",
            "--repo-root",
            ".",
            "--branch",
            "CARMINEai/smoke",
            "--output",
            "output/validation/review_pr_prepare.json",
        ]
    return {
        "schema_version": 1,
        "kind": "review_pr_prepare_args",
        "passed": passed,
        "argv": argv,
        "derived": {
            "include_path_count": include_count,
            "apply_report": apply_report,
            "apply_report_product": apply_product,
            "require_product_input": True,
        },
        "errors": [] if passed else ["synthetic failure"],
        "warnings": [],
    }


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/review_pr_product_readiness_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="review-pr-readiness-smoke-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()

        cases = [
            run_checker(
                source_repo,
                repo,
                args_payload(include_count=2, apply_report="", apply_product=False),
                "include_paths",
            ),
            run_checker(
                source_repo,
                repo,
                args_payload(include_count=0, apply_report="output/apply.json", apply_product=True),
                "apply_product",
            ),
            run_checker(
                source_repo,
                repo,
                args_payload(include_count=0, apply_report="", apply_product=False),
                "missing_product",
            ),
            run_checker(
                source_repo,
                repo,
                args_payload(
                    include_count=0, apply_report="output/apply.json", apply_product=False
                ),
                "non_concrete_apply",
            ),
            run_checker(
                source_repo,
                repo,
                args_payload(
                    include_count=1,
                    apply_report="",
                    apply_product=False,
                    argv=[
                        "-m",
                        "ia_carmine.cli",
                        "agent_review_prepare_pr",
                        "-m",
                        "ia_carmine.cli",
                        "agent_review_prepare_pr",
                        "--repo-root",
                        ".",
                        "--branch",
                        "CARMINEai/smoke",
                        "--output",
                        "output/validation/review_pr_prepare.json",
                    ],
                ),
                "duplicate_prepare_script",
            ),
            run_checker(
                source_repo,
                repo,
                args_payload(
                    include_count=1,
                    apply_report="",
                    apply_product=False,
                    argv=[
                        "-m",
                        "ia_carmine.cli",
                        "agent_review_prepare_pr",
                        "--repo-root",
                        ".",
                        "--branch",
                        "CARMINEai/smoke",
                    ],
                ),
                "missing_prepare_output",
            ),
            run_checker(
                source_repo,
                repo,
                args_payload(include_count=1, apply_report="", apply_product=False, passed=False),
                "args_failed",
            ),
        ]

    by_name = {case["name"]: case for case in cases}
    require(by_name["include_paths"]["returncode"] == 0, errors, "include paths case should pass")
    require(
        by_name["include_paths"]["report"].get("prepare_review_pr_ready") is True,
        errors,
        "include paths should be ready",
    )
    require(by_name["apply_product"]["returncode"] == 0, errors, "apply product case should pass")
    require(
        by_name["apply_product"]["report"].get("prepare_review_pr_ready") is True,
        errors,
        "apply product should be ready",
    )
    require(
        by_name["missing_product"]["returncode"] == 2, errors, "missing product case should fail"
    )
    require(
        by_name["missing_product"]["report"].get("prepare_review_pr_ready") is False,
        errors,
        "missing product should not be ready",
    )
    require(
        by_name["non_concrete_apply"]["returncode"] == 2,
        errors,
        "non concrete apply case should fail",
    )
    require(
        by_name["duplicate_prepare_script"]["returncode"] == 2,
        errors,
        "duplicate prepare script case should fail",
    )
    require(
        by_name["duplicate_prepare_script"]["report"].get("prepare_script_reference_count") == 2,
        errors,
        "duplicate prepare script case should report reference count 2",
    )
    require(
        by_name["missing_prepare_output"]["returncode"] == 2,
        errors,
        "missing prepare output case should fail",
    )
    require(
        "--output"
        in (by_name["missing_prepare_output"]["report"].get("missing_prepare_flags") or []),
        errors,
        "missing prepare output case should report missing --output",
    )
    require(by_name["args_failed"]["returncode"] == 2, errors, "args failed case should fail")
    require(
        all(case.get("markdown_exists") for case in cases),
        errors,
        "all cases should write markdown",
    )

    report = {
        "schema_version": 1,
        "kind": "review_pr_product_readiness_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(source_repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
