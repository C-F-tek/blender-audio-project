#!/usr/bin/env python3
"""Smoke-test prepare_review_pr.py argv construction."""
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
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_helper(source_repo: Path, repo: Path, context: dict[str, Any], name: str) -> dict[str, Any]:
    context_path = repo / f"output/validation/{name}_context.json"
    output_path = repo / f"output/validation/{name}_args.json"
    write_json(context_path, context)

    env = dict(os.environ)
    env["PYTHONPATH"] = str(source_repo)
    result = subprocess.run(
        [
            sys.executable,
            str(source_repo / "Tools/ai/build_review_pr_prepare_args.py"),
            "--context",
            str(context_path),
            "--output",
            str(output_path),
        ],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    report = json.loads(output_path.read_text(encoding="utf-8-sig")) if output_path.exists() else {}
    return {
        "name": name,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "report": report,
    }


def base_context(repo: Path) -> dict[str, Any]:
    apply_report = repo / "output/validation/patch_suggestion_bundle_apply.json"
    write_json(
        apply_report,
        {
            "schema_version": 1,
            "kind": "patch_suggestion_bundle_apply",
            "passed": True,
            "patch_application_performed": True,
            "source_writes_performed": True,
        },
    )
    return {
        "repo_root": str(repo),
        "stamp": "review_pr_args_smoke_20990101-010203",
        "task_file": "docs/LOCAL_AI_TASKS/smoke-task.md",
        "branch": "CARMINEai/review-pr-args-smoke",
        "base": "master",
        "remote": "origin",
        "title": "docs(ai): review PR args smoke",
        "commit_message": "docs(ai): review PR args smoke",
        "output": "output/validation/review_pr_prepare.json",
        "markdown_output": "output/validation/review_pr_prepare.md",
        "evidence_output": "docs/LOCAL_VALIDATION_EVIDENCE/review_pr_prepare.json",
        "evidence_markdown_output": "docs/LOCAL_VALIDATION_EVIDENCE/review_pr_prepare.md",
        "include_paths": ["docs/A.md, docs/B.md", "Tools/example.py"],
        "apply_report": str(apply_report),
        "auto_include_from_apply_report": True,
        "require_product_input": True,
        "allow_dirty_branch": True,
        "push": True,
        "create_pr": True,
        "draft_pr": True,
        "dry_run": True,
    }


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/review_pr_prepare_args_smoke.json")
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    cases: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="review-pr-args-smoke-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()

        full_context = base_context(repo)
        cases.append(run_helper(source_repo, repo, full_context, "full"))

        missing_apply_context = dict(full_context)
        missing_apply_context["apply_report"] = str(repo / "missing/apply.json")
        missing_apply_context["push"] = False
        missing_apply_context["create_pr"] = False
        missing_apply_context["draft_pr"] = False
        cases.append(run_helper(source_repo, repo, missing_apply_context, "missing_apply"))

        no_product_context = dict(full_context)
        no_product_context["include_paths"] = []
        no_product_context["apply_report"] = str(repo / "missing/apply.json")
        no_product_context["push"] = False
        no_product_context["create_pr"] = False
        no_product_context["draft_pr"] = False
        cases.append(run_helper(source_repo, repo, no_product_context, "no_product_input"))

        create_without_push_context = dict(full_context)
        create_without_push_context["push"] = False
        create_without_push_context["create_pr"] = True
        create_without_push_context["draft_pr"] = False
        cases.append(run_helper(source_repo, repo, create_without_push_context, "create_without_push"))

        draft_without_create_context = dict(full_context)
        draft_without_create_context["push"] = False
        draft_without_create_context["create_pr"] = False
        draft_without_create_context["draft_pr"] = True
        cases.append(run_helper(source_repo, repo, draft_without_create_context, "draft_without_create"))

    full = cases[0]["report"]
    full_argv = full.get("argv") or []
    require(cases[0]["returncode"] == 0, errors, "full case helper failed")
    require("--include-path" in full_argv, errors, "full case missing include paths")
    require("--apply-report" in full_argv, errors, "full case missing apply report")
    require("--auto-include-from-apply-report" in full_argv, errors, "full case missing auto include")
    require("--push" in full_argv, errors, "full case missing push")
    require("--create-pr" in full_argv, errors, "full case missing create-pr")
    require("--draft-pr" in full_argv, errors, "full case missing draft-pr")
    require("--dry-run" in full_argv, errors, "full case missing dry-run")

    missing = cases[1]["report"]
    missing_argv = missing.get("argv") or []
    require(cases[1]["returncode"] == 0, errors, "missing apply case helper failed")
    require("--apply-report" not in missing_argv, errors, "missing apply case should omit --apply-report")
    require("--auto-include-from-apply-report" not in missing_argv, errors, "missing apply case should omit auto include")
    require(bool(missing.get("warnings")), errors, "missing apply case should warn")

    no_product = cases[2]["report"]
    require(cases[2]["returncode"] == 2, errors, "no product input case should fail")
    require(not bool(no_product.get("passed")), errors, "no product input case should not pass")
    require(
        any("review PR product input missing" in str(item) for item in no_product.get("errors") or []),
        errors,
        "no product input case should explain missing product input",
    )

    by_name = {case["name"]: case for case in cases}
    create_without_push = by_name["create_without_push"]["report"]
    require(
        by_name["create_without_push"]["returncode"] == 2,
        errors,
        "create without push case should fail",
    )
    require(
        any("create_pr requires push" in str(item) for item in create_without_push.get("errors") or []),
        errors,
        "create without push case should explain create_pr requires push",
    )

    draft_without_create = by_name["draft_without_create"]["report"]
    require(
        by_name["draft_without_create"]["returncode"] == 2,
        errors,
        "draft without create case should fail",
    )
    require(
        any("draft_pr requires create_pr" in str(item) for item in draft_without_create.get("errors") or []),
        errors,
        "draft without create case should explain draft_pr requires create_pr",
    )

    report = {
        "schema_version": 1,
        "kind": "review_pr_prepare_args_smoke",
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
