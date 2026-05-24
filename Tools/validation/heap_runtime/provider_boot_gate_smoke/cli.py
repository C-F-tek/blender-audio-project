from __future__ import annotations

import argparse
import inspect
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    checks = [
        _check_profiles(repo_root),
        _check_replight_lanes(),
        _check_boot_reason_mapping(),
        _check_failure_tails(),
        _check_execution_order(),
        _check_dry_run_policy(),
    ]
    errors = [error for check in checks for error in check.get("errors", [])]
    report = {
        "schema_version": 1,
        "kind": "provider_boot_gate_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "checks": checks,
        "errors": errors,
    }
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def _check_profiles(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "ia_carmine" / "runtime" / "run" / "profiles" / "heap_runtime_launcher_profiles.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    profiles = data.get("profiles") if isinstance(data.get("profiles"), dict) else {}
    for name, profile in profiles.items():
        if not isinstance(profile, dict):
            continue
        if bool(profile.get("allow_provider_generation")) and str(profile.get("keep_alive")) != "120s":
            errors.append(f"profile {name} keep_alive is not 120s")
    return {"name": "profiles_keep_alive", "errors": errors}


def _check_replight_lanes() -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_replight_gate import REQUIRED_REPLIGHT_LANES

    errors = []
    if tuple(REQUIRED_REPLIGHT_LANES) != ("gpu1_planner",):
        errors.append(f"unexpected replight lanes: {REQUIRED_REPLIGHT_LANES}")
    return {"name": "gpu1_only_replight", "errors": errors}


def _check_boot_reason_mapping() -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_coexistence_preflight import (
        provider_role_coexistence_block_reason,
    )

    reason = provider_role_coexistence_block_reason(
        {"passed": False, "errors": ["gpu0_not_alive_during_triple_coexistence"]}
    )
    errors = []
    if not reason.startswith("provider_boot_gate_failed:gpu0_peer:"):
        errors.append(f"unexpected boot reason: {reason}")
    return {"name": "boot_reason_mapping", "reason": reason, "errors": errors}


def _check_failure_tails() -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_replight_gate import _report_for_completed

    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "missing_report.json"
        spec = {
            "lane": "gpu0_peer",
            "role": "gpu0_peer_reviewer_refiner",
            "provider_backend": "ollama",
            "provider_compute_device": "ollama/gpu0-vulkan",
            "output": output,
            "command": ["python", "-m", "x", "--base-url", "http://127.0.0.1:11435"],
        }
        report = _report_for_completed(
            spec,
            subprocess.CompletedProcess(spec["command"], 2, "stdout marker", "stderr marker"),
        )
    errors = []
    if "stdout marker" not in str(report.get("stdout_tail")):
        errors.append("stdout tail missing from synthetic replight failure")
    if "stderr marker" not in str(report.get("stderr_tail")):
        errors.append("stderr tail missing from synthetic replight failure")
    if report.get("ollama_base_url") != "http://127.0.0.1:11435":
        errors.append("base URL missing from synthetic replight failure")
    return {"name": "failure_tail_preservation", "errors": errors}


def _check_execution_order() -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_execution import RuntimeGateProviderExecutionMixin

    source = inspect.getsource(RuntimeGateProviderExecutionMixin.run_provider_teamwork)
    boot_index = source.find("provider_boot_gate_started")
    replight_index = source.find("run_provider_replight_gate")
    errors = []
    if boot_index < 0:
        errors.append("provider_boot_gate_started stage missing")
    if replight_index < 0:
        errors.append("run_provider_replight_gate call missing")
    if boot_index >= 0 and replight_index >= 0 and boot_index > replight_index:
        errors.append("provider boot gate is still after replight")
    return {"name": "provider_boot_before_replight", "errors": errors}


def _check_dry_run_policy() -> dict[str, Any]:
    from ia_carmine.runtime.run.dry_run_policy import dry_run_contract_policy

    policy = dry_run_contract_policy(
        gpu1_base_url="http://127.0.0.1:11434",
        gpu0_base_url="http://127.0.0.1:11435",
        keep_alive="120s",
        field_sources={
            "gpu1_base_url": "smoke_fixture",
            "gpu0_base_url": "smoke_fixture",
            "keep_alive": "smoke_fixture",
            "gpu0_model": "smoke_fixture",
            "npu_model_dir": "smoke_fixture",
            "npu_micro_start_mode": "smoke_fixture",
            "allow_npu_device_workload": "smoke_fixture",
        },
    )
    errors = []
    boot = policy.get("provider_boot_gate_policy") if isinstance(policy.get("provider_boot_gate_policy"), dict) else {}
    replight = policy.get("provider_replight_policy") if isinstance(policy.get("provider_replight_policy"), dict) else {}
    if boot.get("required_lanes") != ["gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"]:
        errors.append("dry-run boot gate lanes missing")
    if replight.get("required_lanes") != ["gpu1_planner"]:
        errors.append("dry-run replight should require only GPU1")
    if boot.get("workload_verified_at_boot") is not False:
        errors.append("boot gate must not claim provider workload verification")
    return {"name": "dry_run_policy", "errors": errors}


if __name__ == "__main__":
    raise SystemExit(main())
