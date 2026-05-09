#!/usr/bin/env python3
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


STAMP = "runtime_evidence_correlation_smoke_20990101-010203"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fixture_report(kind: str, **extra: Any) -> dict[str, Any]:
    data = {
        "schema_version": 1,
        "kind": kind,
        "stamp": STAMP,
        "passed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [],
        "warnings": [],
    }
    data.update(extra)
    return data


def seed_fixture(repo: Path) -> dict[str, Path]:
    paths = {
        "preflight": repo / f"output/validation/real_product_profile_preflight_{STAMP}.json",
        "heap_entry": repo / f"output/local_ai_runs/{STAMP}_unified/ai_packets/heap_exchange_runtime_entry.json",
        "heap_peer_runtime": repo / f"output/local_ai_runs/{STAMP}_unified/ai_packets/heap_peer_runtime_manifest.json",
        "gpu0_peer": repo / f"output/validation/openvino_gpu0_workload_{STAMP}.json",
        "npu_micro_peer": repo / f"output/validation/npu_micro_peer_{STAMP}.json",
        "shared_memory": repo / f"output/validation/shared_toolbox_ai_to_ai_bundle_{STAMP}.json",
        "tool_broker": repo / f"output/validation/full_toolbox_run_telemetry_summary_{STAMP}.json",
        "closure_audit": repo / f"output/validation/heap_exchange_closure_audit_{STAMP}.json",
        "product_readiness": repo / f"output/validation/review_pr_product_readiness_real_product_{STAMP}.json",
        "review_pr_prepare": repo / f"output/validation/review_pr_prepare_real_product_{STAMP}.json",
        "unified_chain_contract": repo / f"output/validation/unified_chain_contract_{STAMP}.json",
    }

    write_json(paths["preflight"], fixture_report("real_product_preflight_gate", steps=["full_product_pr_chain"], full_product_pr_chain=True))
    write_json(paths["heap_entry"], fixture_report("heap_exchange_runtime_entry", task_ingress=True, heap_exchange=True, runtime_entry=True))
    write_json(paths["heap_peer_runtime"], fixture_report("heap_peer_runtime_manifest", peers=["GPU1 primary advisory", "GPU0 OpenVINO peer", "NPU micro peer"]))
    write_json(paths["gpu0_peer"], fixture_report("openvino_gpu0_workload", gpu0=True, openvino=True, peer=True))
    write_json(paths["npu_micro_peer"], fixture_report("npu_micro_peer", npu=True, micro=True, peer=True))
    write_json(paths["shared_memory"], fixture_report("shared_toolbox_ai_to_ai_bundle", shared=True, memory=True, heap=True, ai_to_ai=True))
    write_json(paths["tool_broker"], fixture_report("full_toolbox_run_telemetry_summary", tool_usage_count=3, broker=True, telemetry=True, capability=True))
    write_json(paths["closure_audit"], fixture_report("heap_exchange_closure_audit", closure_state="ready_for_final_chain_contract", closure=True, audit=True, heap_exchange=True))
    write_json(paths["product_readiness"], fixture_report("review_pr_product_readiness", product=True, ready=True))
    write_json(paths["review_pr_prepare"], fixture_report("review_pr_prepare", product_commit=True, git_commit_performed=True))
    write_json(paths["unified_chain_contract"], fixture_report("unified_chain_contract", edges=[{"edge": "heap", "passed": True}]))

    return paths


def run_validator(source_repo: Path, fixture_repo: Path, output: Path, markdown: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(source_repo)
    return subprocess.run(
        [
            sys.executable,
            str(source_repo / "Tools/validation/check_runtime_evidence_correlation.py"),
            "--repo-root",
            str(fixture_repo),
            "--stamp",
            STAMP,
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ],
        cwd=fixture_repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/runtime_evidence_correlation_smoke.json")
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="runtime-evidence-correlation-smoke-") as tmp:
        fixture_repo = Path(tmp) / "repo"
        fixture_repo.mkdir(parents=True)
        seed_fixture(fixture_repo)
        validator_output = fixture_repo / "output/validation/runtime_evidence_correlation.json"
        validator_md = fixture_repo / "output/validation/runtime_evidence_correlation.md"
        result = run_validator(source_repo, fixture_repo, validator_output, validator_md)
        report = json.loads(validator_output.read_text(encoding="utf-8-sig")) if validator_output.exists() else {}

    require(result.returncode == 0, errors, "runtime evidence correlation validator failed")
    require(report.get("passed") is True, errors, "runtime evidence correlation report did not pass")
    require(not report.get("missing_surfaces"), errors, "runtime evidence correlation reported missing surfaces")
    require(not report.get("failed_surfaces"), errors, "runtime evidence correlation reported failed surfaces")
    require(len(report.get("surfaces") or []) == 11, errors, "runtime evidence correlation surface count mismatch")

    smoke = {
        "schema_version": 1,
        "kind": "runtime_evidence_correlation_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "validator_report": report,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(source_repo, args.output)
    print(write_json_report(smoke, output), end="")
    return 0 if smoke["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
