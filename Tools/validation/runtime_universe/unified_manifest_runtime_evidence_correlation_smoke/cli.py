#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_validator(repo_root: Path, manifest: Path, output: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "Tools/validation/runtime_universe/unified_run_manifest_schema/cli.py"),
            "--repo-root",
            str(repo_root),
            "--manifest",
            str(manifest),
            "--output",
            str(output),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    report = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
    return {
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-1500:],
        "stderr_tail": result.stderr[-1500:],
        "report": report,
    }


def base_manifest(stamp: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "unified_local_ai_refactor_manifest",
        "stamp": stamp,
        "mode_name": "all",
        "unified_run_operational_model": "single_dynamic_heap_exchange_run",
        "unified_run_source_of_knowledge": "heap_exchange",
        "unified_run_final_product": "reviewable_pr_with_concrete_changes",
        "phase_status": {
            "final_unified_chain_contract": True,
            "runtime_evidence_correlation": True,
        },
        "phase_reports": {},
        "report_files": [],
        "context_files": [],
    }


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/unified_manifest_runtime_evidence_correlation_smoke.json",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    work_dir = repo_root / "output/validation/manifest_runtime_correlation_smoke"
    stamp = "manifest_runtime_correlation_smoke_20990101-010203"

    good_manifest = base_manifest(stamp)
    good_manifest["runtime_evidence_correlation_requested"] = True
    good_manifest["phase_reports"]["runtime_evidence_correlation"] = (
        f"output/validation/runtime_evidence_correlation_all_{stamp}.json"
    )
    good_manifest["report_files"].append(
        f"output/validation/runtime_evidence_correlation_all_{stamp}.json"
    )
    good_manifest["context_files"].append(
        f"output/validation/runtime_evidence_correlation_all_{stamp}.md"
    )

    missing_manifest = base_manifest(stamp)
    missing_manifest["runtime_evidence_correlation_requested"] = True

    not_requested_manifest = base_manifest(stamp)
    not_requested_manifest["runtime_evidence_correlation_requested"] = False

    cases = []
    for name, manifest_payload in (
        ("good_requested", good_manifest),
        ("missing_requested", missing_manifest),
        ("not_requested", not_requested_manifest),
    ):
        manifest_path = work_dir / f"{name}.json"
        output_path = work_dir / f"{name}_report.json"
        write_json(manifest_path, manifest_payload)
        case = run_validator(repo_root, manifest_path, output_path)
        case["name"] = name
        cases.append(case)

    errors: list[str] = []
    by_name = {case["name"]: case for case in cases}

    require(
        by_name["good_requested"]["returncode"] == 0, errors, "good requested manifest should pass"
    )
    require(
        by_name["good_requested"]["report"].get("passed") is True,
        errors,
        "good requested report should pass",
    )

    missing_errors = by_name["missing_requested"]["report"].get("errors") or []
    require(
        by_name["missing_requested"]["returncode"] == 2,
        errors,
        "missing requested manifest should fail",
    )
    require(
        any("phase_reports.runtime_evidence_correlation" in item for item in missing_errors),
        errors,
        "missing requested manifest should report missing phase_reports.runtime_evidence_correlation",
    )
    require(
        any(
            "report_files" in item and "runtime_evidence_correlation" in item
            for item in missing_errors
        ),
        errors,
        "missing requested manifest should report missing runtime correlation report_files entry",
    )

    require(
        by_name["not_requested"]["returncode"] == 0, errors, "not requested manifest should pass"
    )
    require(
        by_name["not_requested"]["report"].get("passed") is True,
        errors,
        "not requested report should pass",
    )

    report = {
        "schema_version": 1,
        "kind": "unified_manifest_runtime_evidence_correlation_smoke",
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
