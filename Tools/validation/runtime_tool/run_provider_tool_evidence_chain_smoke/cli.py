#!/usr/bin/env python3
"""Smoke-test provider tool evidence in the unified chain contract."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


STAMP = "provider_tool_evidence_chain_smoke_20990101-010203"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, events: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/provider_tool_evidence_chain_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="provider-tool-evidence-chain-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()
        manifest = (
            repo / f"output/local_ai_runs/{STAMP}/pipeline/unified_local_ai_refactor_manifest.json"
        )
        official = repo / f"output/validation/{STAMP}_phase_official.json"
        gpu0 = repo / f"output/validation/openvino_gpu0_workload_{STAMP}.json"
        observer = repo / f"output/local_ai_runs/{STAMP}_observer"
        ai_events = observer / "ai_public_events.jsonl"
        capability = repo / f"output/validation/runtime_tool_capability_manifest_{STAMP}.json"
        usage = repo / f"output/validation/full_toolbox_run_telemetry_summary_{STAMP}.json"
        product = repo / f"output/validation/patch_suggestion_product_separation_{STAMP}.json"
        output = repo / "output/validation/unified_chain_contract.json"

        write_json(
            manifest,
            {"schema_version": 1, "kind": "unified_local_ai_refactor_manifest", "stamp": STAMP},
        )
        write_json(
            official,
            {
                "schema_version": 1,
                "kind": "official",
                "passed": True,
                "status": "passed",
                "return_code": 0,
            },
        )
        write_json(
            gpu0,
            {
                "schema_version": 1,
                "kind": "gpu0",
                "openvino_gpu0_visible": True,
                "openvino_gpu0_workload_performed": True,
                "openvino_gpu0_workload_passed": True,
            },
        )
        write_jsonl(
            ai_events,
            [
                {
                    "kind": "decision",
                    "summary": "provider selected tool_result for patch recommendation",
                }
            ],
        )
        write_json(
            capability,
            {
                "schema_version": 1,
                "kind": "runtime_tool_capability_manifest",
                "passed": True,
                "tool_count": 3,
                "tools": ["repo_search", "patchkit", "validator"],
            },
        )
        write_json(
            usage,
            {
                "schema_version": 1,
                "kind": "full_toolbox_run_telemetry_summary",
                "passed": True,
                "tool_usage_count": 2,
                "tool_usage": [{"tool": "repo_search"}, {"tool": "validator"}],
            },
        )
        write_json(
            product,
            {
                "schema_version": 1,
                "kind": "patch_suggestion_product_separation",
                "passed": True,
                "patch_product_status": "product_facing_patch_suggestions_ready",
                "ready_for_patch_suggestion_review": True,
            },
        )

        env = dict(os.environ)
        env["PYTHONPATH"] = str(source_repo)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "Tools.validation",
                "unified_chain_contract",
                "--repo-root",
                str(repo),
                "--stamp",
                STAMP,
                "--manifest",
                str(manifest),
                "--official-report",
                str(official),
                "--gpu0-report",
                str(gpu0),
                "--observer-dir",
                str(observer),
                "--tool-capability-manifest",
                str(capability),
                "--tool-usage-telemetry",
                str(usage),
                "--product-separation-report",
                str(product),
                "--require-ai-exchange",
                "--require-provider-tool-evidence",
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
        if result.returncode != 0:
            errors.append(f"chain contract command failed: {result.stderr[-500:]}")
        if report.get("passed") is not True:
            errors.append(f"chain contract did not pass: {report.get('errors')}")
        if not any(
            edge.get("edge") == "provider_to_tool_evidence" and edge.get("passed") is True
            for edge in report.get("edges") or []
        ):
            errors.append("provider_to_tool_evidence edge missing or failed")

    final = {
        "schema_version": 1,
        "kind": "provider_tool_evidence_chain_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": [],
    }
    output_path = resolve_output_path(source_repo, args.output)
    print(write_json_report(final, output_path), end="")
    return 0 if final["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
