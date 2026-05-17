#!/usr/bin/env python3
"""Smoke-test the unified chain contract validator.

The contract intentionally validates the heap/exchange envelope rather than a
fixed internal reasoning path: the dynamic AI entities may collaborate freely,
but the run must leave observable exchange/evidence and concrete patch products
when review-PR generation is requested.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
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


MODE_NAME = "agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_smoke"


def run(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, check=False, timeout=120
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-6000:],
        "stderr_tail": result.stderr[-6000:],
        "ok": result.returncode == 0,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Unified Chain Contract Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        "",
        "## Cases",
        "",
    ]
    for case in report.get("cases") or []:
        lines.append(f"- `{case.get('name')}`: `{case.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def prepare_case(repo: Path, stamp: str, *, exchange: bool, concrete: bool, product: bool) -> None:
    write_json(
        repo / f"output/validation/{stamp}_phase_official.json",
        {
            "schema_version": 1,
            "kind": "unified_launcher_phase_status",
            "phase": "official",
            "passed": True,
            "status": "passed",
            "return_code": 0,
        },
    )
    write_json(
        repo / f"output/validation/openvino_gpu0_workload_{stamp}.json",
        {
            "schema_version": 1,
            "kind": "openvino_gpu0_workload",
            "passed": True,
            "openvino_gpu0_visible": True,
            "openvino_gpu0_workload_performed": True,
            "openvino_gpu0_workload_passed": True,
            "provider_execution_performed": True,
        },
    )
    write_json(
        repo
        / f"output/local_ai_runs/{stamp}_unified/pipeline/unified_local_ai_refactor_manifest.json",
        {"schema_version": 1, "kind": "unified_local_ai_refactor_manifest", "stamp": stamp},
    )
    observer = repo / f"output/local_ai_runs/{stamp}_observer"
    observer.mkdir(parents=True, exist_ok=True)
    if exchange:
        (observer / "ai_public_events.jsonl").write_text(
            json.dumps(
                {
                    "kind": "proposal",
                    "entity": "heap.exchange",
                    "summary": "concrete patch proposal published",
                }
            )
            + "\n",
            encoding="utf-8",
        )

    apply_report = {
        "schema_version": 1,
        "kind": "patch_suggestion_bundle_apply",
        "passed": True,
        "operation_count": 1 if concrete else 0,
        "changed_count": 1 if concrete else 0,
        "applied_count": 1 if concrete else 0,
        "manual_review_required": not concrete,
        "results": [
            {
                "operation": "append_once" if concrete else "metadata_only",
                "path": "docs/LOCAL_AI_TASKS/example.md",
                "changed": bool(concrete),
                "ok": True,
            }
        ]
        if concrete
        else [],
    }
    write_json(
        repo / f"output/validation/patch_suggestion_bundle_apply_{MODE_NAME}_{stamp}.json",
        apply_report,
    )

    product_report = {
        "schema_version": 1,
        "kind": "patch_suggestion_product_separation",
        "passed": bool(product),
        "patch_product_status": "deterministic_patch_operations_ready"
        if product
        else "no_applicable_patch_product",
        "ready_for_patch_suggestion_review": bool(product),
        "essential_patch_suggestion_items": [
            {"id": "example", "path": "docs/LOCAL_AI_TASKS/example.md"}
        ]
        if product
        else [],
        "supplemental_telemetry_debug_items": [],
    }
    write_json(
        repo / f"output/validation/patch_suggestion_product_separation_{MODE_NAME}_{stamp}.json",
        product_report,
    )


def run_contract(repo: Path, validator: Path, stamp: str, output: str) -> dict[str, Any]:
    command = [
        sys.executable,
        str(validator),
        "--repo-root",
        str(repo),
        "--stamp",
        stamp,
        "--mode-name",
        MODE_NAME,
        "--require-ai-exchange",
        "--require-concrete-patch-specs",
        "--require-review-pr-product",
        "--output",
        output,
    ]
    return run(command, repo)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/unified_chain_contract_smoke.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/unified_chain_contract_smoke.md"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    validator = source_repo / "Tools/validation/check_unified_chain_contract.py"
    errors: list[str] = []
    cases: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="unified-chain-contract-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        # The validator itself runs from the source repository but inspects temp evidence.
        missing_stamp = "missing_exchange_metadata_only"
        prepare_case(repo, missing_stamp, exchange=False, concrete=False, product=False)
        missing_result = run_contract(
            repo, validator, missing_stamp, "output/validation/missing_contract.json"
        )
        missing_combined = f"{missing_result['stdout_tail']}\n{missing_result['stderr_tail']}"
        missing_ok = (
            missing_result["returncode"] == 2
            and "provider_to_ai_exchange" in missing_combined
            and "patch_specs_to_review_bridge" in missing_combined
        )
        cases.append(
            {
                "name": "missing_exchange_metadata_only_fails",
                "passed": missing_ok,
                "command": missing_result,
            }
        )
        if not missing_ok:
            errors.append(
                "missing exchange / metadata-only case did not fail with expected broken edges"
            )

        passing_stamp = "heap_exchange_concrete_product"
        prepare_case(repo, passing_stamp, exchange=True, concrete=True, product=True)
        passing_result = run_contract(
            repo, validator, passing_stamp, "output/validation/passing_contract.json"
        )
        passing_ok = (
            passing_result["returncode"] == 0
            and '"passed": true' in passing_result["stdout_tail"].lower()
        )
        cases.append(
            {
                "name": "heap_exchange_concrete_product_passes",
                "passed": passing_ok,
                "command": passing_result,
            }
        )
        if not passing_ok:
            errors.append("heap exchange concrete product case did not pass")

    report = {
        "schema_version": 1,
        "kind": "unified_chain_contract_smoke",
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
    markdown = resolve_output_path(source_repo, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
