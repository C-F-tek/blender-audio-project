#!/usr/bin/env python3
"""Smoke-test unified chain contract argv construction."""

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
            str(source_repo / "Tools/ai/build_unified_chain_contract_args.py"),
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
    manifest = repo / "output/local_ai_runs/stamp/pipeline/unified_local_ai_refactor_manifest.json"
    apply_report = repo / "output/validation/apply.json"
    product_report = repo / "output/validation/product.json"
    review_report = repo / "output/validation/review.json"
    for path in (manifest, apply_report, product_report, review_report):
        write_json(path, {"kind": path.stem, "passed": True})
    return {
        "repo_root": str(repo),
        "stamp": "chain_args_smoke_20990101-010203",
        "mode_name": "smoke",
        "manifest": str(manifest),
        "apply_report": str(apply_report),
        "product_separation_report": str(product_report),
        "review_pr_report": str(review_report),
        "output_report": str(repo / "output/validation/unified_chain_contract.json"),
        "markdown_report": str(repo / "output/validation/unified_chain_contract.md"),
        "use_primary_advisory_provider": True,
        "run_multistep_provider_workflow": False,
        "use_ollama_advisory": False,
        "run_ollama_probe": False,
        "open_extended_observer_consoles": False,
        "review_pr_from_generated_patch_specs": True,
        "prepare_review_pr": True,
        "review_pr_apply_deterministic_suggestions": False,
    }


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/unified_chain_contract_args_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    cases: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="unified-chain-args-smoke-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()
        full_context = base_context(repo)
        cases.append(run_helper(source_repo, repo, full_context, "full"))

        minimal_context = dict(full_context)
        minimal_context.update(
            {
                "use_primary_advisory_provider": False,
                "review_pr_from_generated_patch_specs": False,
                "prepare_review_pr": False,
                "review_pr_apply_deterministic_suggestions": False,
                "apply_report": str(repo / "missing/apply.json"),
            }
        )
        cases.append(run_helper(source_repo, repo, minimal_context, "minimal"))

    full = cases[0]["report"]
    full_argv = full.get("argv") or []
    require(cases[0]["returncode"] == 0, errors, "full case helper failed")
    require("--apply-report" in full_argv, errors, "full case missing --apply-report")
    require(
        "--product-separation-report" in full_argv,
        errors,
        "full case missing --product-separation-report",
    )
    require("--review-pr-report" in full_argv, errors, "full case missing --review-pr-report")
    require("--require-ai-exchange" in full_argv, errors, "full case missing --require-ai-exchange")
    require(
        "--require-concrete-patch-specs" in full_argv,
        errors,
        "full case missing --require-concrete-patch-specs",
    )
    require(
        "--require-review-pr-product" in full_argv,
        errors,
        "full case missing --require-review-pr-product",
    )

    minimal = cases[1]["report"]
    minimal_argv = minimal.get("argv") or []
    require(cases[1]["returncode"] == 0, errors, "minimal case helper failed")
    require(
        "--apply-report" not in minimal_argv,
        errors,
        "minimal case should omit missing --apply-report",
    )
    require(
        "--require-ai-exchange" not in minimal_argv,
        errors,
        "minimal case should not require AI exchange",
    )
    require(
        "--require-concrete-patch-specs" not in minimal_argv,
        errors,
        "minimal case should not require concrete patch specs",
    )
    require(
        "--require-review-pr-product" not in minimal_argv,
        errors,
        "minimal case should not require review PR product",
    )

    report = {
        "schema_version": 1,
        "kind": "unified_chain_contract_args_smoke",
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
