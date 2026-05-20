#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from Tools.ai._shared.process_tree import terminate_process_tree
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.ai._shared.process_tree import terminate_process_tree  # type: ignore
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/real_product_preflight_gate_smoke.json"
    )
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    preflight_json = (
        repo_root / "output/validation/real_product_preflight_gate_smoke_preflight.json"
    )
    preflight_md = repo_root / "output/validation/real_product_preflight_gate_smoke_preflight.md"

    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    command = [
        sys.executable,
        str(repo_root / "Tools/validation/real_product/preflight_gate/cli.py"),
        "--repo-root",
        str(repo_root),
        "--output",
        str(preflight_json),
        "--markdown-output",
        str(preflight_md),
        "--timeout-seconds",
        str(args.timeout_seconds),
    ]
    process = subprocess.Popen(
        command,
        cwd=repo_root,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        stdout, stderr = process.communicate(timeout=args.timeout_seconds + 30)
        result = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        terminate_process_tree(process)
        stdout, stderr = process.communicate()
        result = subprocess.CompletedProcess(
            command,
            124,
            stdout or "",
            (stderr or "") + "\npreflight gate smoke timeout",
        )

    report = (
        json.loads(preflight_json.read_text(encoding="utf-8-sig"))
        if preflight_json.exists()
        else {}
    )
    errors: list[str] = []

    require(result.returncode == 0, errors, "preflight gate failed")
    require(report.get("passed") is True, errors, "preflight report did not pass")
    require(
        report.get("provider_execution_performed") is False,
        errors,
        "preflight must not execute providers",
    )
    require(
        report.get("patch_application_performed") is False,
        errors,
        "preflight must not apply patches",
    )
    require(
        report.get("source_writes_performed") is False,
        errors,
        "preflight must not write source products",
    )
    require(preflight_md.exists(), errors, "preflight markdown missing")

    expected_steps = {
        "real_product_profile",
        "core_runtime_guard_suite",
        "real_product_single_entry_exit",
        "intrinsic_capability_contract",
        "runtime_mesh_contract",
        "provider_lane_activation",
        "openvino_peer_topology",
        "review_pr_prepare_args",
        "review_pr_product_readiness",
        "heap_provider_budget_governor",
        "heap_provider_invocation_contract",
        "heap_runtime_completeness_gate",
        "runtime_evidence_correlation",
        "runtime_evidence_correlation_launcher_wiring",
        "manifest_runtime_evidence_correlation_schema",
        "review_pr_final_product_contract",
    }
    observed_steps = {str(step.get("name")) for step in report.get("steps") or []}
    require(expected_steps.issubset(observed_steps), errors, "preflight missing expected steps")

    smoke = {
        "schema_version": 1,
        "kind": "real_product_preflight_gate_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "preflight_report": report,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(smoke, output), end="")
    return 0 if smoke["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
