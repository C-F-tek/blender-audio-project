#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/observable_peer_activity_contract_smoke.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    gpu0 = repo / "Tools/ai/build_openvino_gpu0_workload_report.py"
    npu = repo / "Tools/ai/build_npu_micro_task_companion_report.py"
    gpu0_text = read_text(gpu0)
    npu_text = read_text(npu)

    checks: dict[str, bool] = {
        "gpu0_default_iterations_observable": "default=180" in gpu0_text,
        "gpu0_default_min_seconds_observable": "default=6.0" in gpu0_text,
        "gpu0_requires_observable_workload": "openvino_gpu0_observable_workload_required" in gpu0_text,
        "gpu0_fails_non_observable_when_required": "GPU.0 workload was not observable enough" in gpu0_text and "report[\"passed\"] = False" in gpu0_text,
        "npu_declares_activity_requested": "npu_peer_activity_requested" in npu_text,
        "npu_declares_activity_not_performed": "\"npu_peer_activity_performed\": False" in npu_text,
        "npu_declares_no_device_execution": "\"npu_device_execution_performed\": False" in npu_text,
        "npu_declares_diagnostic_only": "diagnostic_report_only" in npu_text,
    }
    errors = [f"observable peer activity contract missing: {name}" for name, ok in checks.items() if not ok]
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "observable_peer_activity_contract_smoke",
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(repo, args.output)), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
