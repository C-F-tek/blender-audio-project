#!/usr/bin/env python3
"""Smoke-test final unified run manifest schema validator."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/unified_run_manifest_schema_smoke.json")
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    cases = []

    with tempfile.TemporaryDirectory(prefix="unified-manifest-schema-smoke-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()
        manifest = repo / "output/local_ai_runs/stamp/pipeline/unified_local_ai_refactor_manifest.json"
        output = repo / "output/validation/manifest_validation.json"
        write_json(
            manifest,
            {
                "schema_version": 1,
                "kind": "unified_local_ai_refactor_manifest",
                "stamp": "manifest_schema_smoke_20990101-010203",
                "mode_name": "smoke",
                "full0to10_legacy_alias_requested": False,
                "full0to10_standalone_pipeline": False,
                "unified_run_operational_model": "single_dynamic_heap_exchange_run",
                "unified_run_source_of_knowledge": "heap_exchange",
                "unified_run_final_product": "reviewable_pr_with_concrete_changes",
                "phase_status": {"smoke": True, "unified_chain_contract_final": True},
                "phase_reports": {
                    "smoke": "output/validation/smoke.json",
                    "unified_chain_contract": "output/validation/unified_chain_contract.json",
                },
                "report_files": [
                    "output/validation/smoke.json",
                    "output/validation/unified_chain_contract.json",
                ],
                "context_files": [
                    "output/validation/unified_chain_contract.md",
                ],
            },
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(source_repo)
        result = subprocess.run(
            [
                sys.executable,
                str(source_repo / "Tools/validation/check_unified_run_manifest_schema.py"),
                "--repo-root",
                str(repo),
                "--manifest",
                str(manifest),
                "--output",
                str(output),
            ],
            cwd=repo,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        report = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
        cases.append({"returncode": result.returncode, "report": report, "stderr_tail": result.stderr[-2000:]})
        if result.returncode != 0 or report.get("passed") is not True:
            errors.append("valid manifest fixture failed schema validation")

    final = {
        "schema_version": 1,
        "kind": "unified_run_manifest_schema_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }
    output_path = resolve_output_path(source_repo, args.output)
    print(write_json_report(final, output_path), end="")
    return 0 if final["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
