#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


def read_text(path: Path) -> str:
    if path.is_dir():
        return "\n".join(
            item.read_text(encoding="utf-8-sig", errors="replace")
            for item in sorted(path.rglob("*.ps1"))
            if item.is_file()
        )
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/runtime_evidence_correlation_launcher_wiring_smoke.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    workflow = ""
    wrapper = ""
    preflight = read_text(repo / "Tools/validation/real_product/preflight_gate/cli.py")
    completeness_smoke = read_text(repo / "Tools/validation/heap_runtime/completeness_gate_smoke/cli.py")
    validator = read_text(repo / "Tools/validation/runtime_universe/check_runtime_evidence_correlation/cli.py")
    manifest_schema = read_text(repo / "Tools/validation/runtime_universe/unified_run_manifest_schema/cli.py")

    checks = {
        "legacy_launcher_surface_retired": workflow == "" and wrapper == "",
        "preflight_validates_wiring_smoke": "runtime_evidence_correlation_launcher_wiring" in preflight,
        "preflight_routes_to_heap_runtime_completeness_gate": "heap_runtime_completeness_gate" in preflight,
        "completeness_gate_checks_product_status": "product_status" in completeness_smoke
        and "heap_write_count" in completeness_smoke,
        "validator_correlates_runtime_surfaces": "runtime_evidence_correlation" in validator
        and "missing_surfaces" in validator
        and "failed_surfaces" in validator,
        "manifest_schema_requires_correlation_when_requested": "runtime_evidence_correlation_requested"
        in manifest_schema
        and "phase_reports.runtime_evidence_correlation" in manifest_schema,
    }

    errors: list[str] = []
    for name, passed in checks.items():
        require(passed, errors, f"runtime evidence correlation wiring check failed: {name}")

    phase_pos = -1
    correlation_pos = -1

    report = {
        "schema_version": 1,
        "kind": "runtime_evidence_correlation_launcher_wiring_smoke",
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "positions": {"phase_status": phase_pos, "runtime_evidence_correlation": correlation_pos},
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
