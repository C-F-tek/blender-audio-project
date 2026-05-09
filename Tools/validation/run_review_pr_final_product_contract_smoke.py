#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_contract(repo_root: Path, report_path: Path, output: Path, require_remote: bool) -> dict[str, Any]:
    command = [
        sys.executable,
        str(repo_root / "Tools/validation/check_review_pr_final_product_contract.py"),
        "--repo-root",
        str(repo_root),
        "--review-pr-report",
        str(report_path),
        "--output",
        str(output),
    ]
    if require_remote:
        command.append("--require-remote-pr")
    result = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    report = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
    return {
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-1500:],
        "stderr_tail": result.stderr[-1500:],
        "report": report,
    }


def base_review_report() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "review_pr_prepare",
        "passed": True,
        "branch": "codex/review-pr-final-product-smoke",
        "base_branch": "master",
        "include_paths": ["Tools/example.py"],
        "git_commit_performed": True,
        "product_commit": "0123456789abcdef0123456789abcdef01234567",
        "git_push_performed": False,
        "github_pr_created": False,
        "github_pr_draft_requested": False,
        "github_pr_url": "",
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "commands": [],
        "errors": [],
        "warnings": [],
    }


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/review_pr_final_product_contract_smoke.json")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    work_dir = repo_root / "output/validation/review_pr_final_product_contract_smoke"

    local_report = base_review_report()
    remote_report = base_review_report()
    remote_report["git_push_performed"] = True
    remote_report["github_pr_created"] = True
    remote_report["github_pr_draft_requested"] = True
    remote_report["github_pr_url"] = "https://github.com/C-F-tek/blender-audio-project/pull/999"

    missing_remote_report = base_review_report()
    missing_remote_report["git_push_performed"] = True

    cases = []
    for name, payload, require_remote in (
        ("local_product", local_report, False),
        ("remote_product", remote_report, True),
        ("missing_remote_pr", missing_remote_report, True),
    ):
        report_path = work_dir / f"{name}_review_pr_prepare.json"
        output_path = work_dir / f"{name}_contract.json"
        write_json(report_path, payload)
        case = run_contract(repo_root, report_path, output_path, require_remote)
        case["name"] = name
        case["require_remote_pr"] = require_remote
        cases.append(case)

    errors: list[str] = []
    by_name = {case["name"]: case for case in cases}

    require(by_name["local_product"]["returncode"] == 0, errors, "local product case should pass")
    require(by_name["local_product"]["report"].get("passed") is True, errors, "local product report should pass")
    require(by_name["remote_product"]["returncode"] == 0, errors, "remote product case should pass")
    require(by_name["remote_product"]["report"].get("passed") is True, errors, "remote product report should pass")

    missing_errors = by_name["missing_remote_pr"]["report"].get("errors") or []
    require(by_name["missing_remote_pr"]["returncode"] == 2, errors, "missing remote PR case should fail")
    require(
        any("github_pr_created" in item or "github_pr_url_present" in item for item in missing_errors),
        errors,
        "missing remote PR case should report missing GitHub PR",
    )

    report = {
        "schema_version": 1,
        "kind": "review_pr_final_product_contract_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
