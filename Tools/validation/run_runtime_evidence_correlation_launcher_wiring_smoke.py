#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def position(text: str, token: str) -> int:
    return text.find(token)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/runtime_evidence_correlation_launcher_wiring_smoke.json")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    workflow = read_text(repo_root / "Tools/workflow/run_unified_local_ai_refactor.ps1")
    wrapper = read_text(repo_root / "Tools/workflow/run_unified_real_product_pr.ps1")
    preflight = read_text(repo_root / "Tools/validation/run_real_product_preflight_gate.py")
    heap_runtime_completeness_gate_smoke = read_text(repo_root / "Tools/validation/run_heap_runtime_completeness_gate_smoke.py")

    errors: list[str] = []

    checks: dict[str, bool] = {
        "launcher_exposes_switch": "[switch]$BuildRuntimeEvidenceCorrelation" in workflow,
        "launcher_has_final_marker": "IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-FINAL-BEGIN" in workflow,
        "launcher_invokes_validator": "check_runtime_evidence_correlation.py" in workflow,
        "launcher_records_phase_status": "runtime_evidence_correlation" in workflow and "Build runtime evidence correlation" in workflow,
        "launcher_adds_report_file": "$ReportFiles += $RuntimeEvidenceCorrelationJson" in workflow,
        "launcher_adds_context_file": "runtime_evidence_correlation" in workflow and "Add-ExistingContextFile" in workflow,
        "wrapper_requests_correlation": "-BuildRuntimeEvidenceCorrelation" in wrapper,
        "preflight_validates_wiring_smoke": "run_runtime_evidence_correlation_launcher_wiring_smoke.py" in preflight,
        "preflight_routes_to_heap_runtime_completeness_gate": "run_heap_runtime_completeness_gate_smoke.py" in preflight,
        "heap_runtime_completeness_gate_smoke_checks_product_status": "product_status" in heap_runtime_completeness_gate_smoke and "heap_write_count" in heap_runtime_completeness_gate_smoke,
    }

    for name, passed in checks.items():
        require(passed, errors, f"runtime evidence correlation launcher wiring check failed: {name}")

    final_chain_pos = position(workflow, "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-FINAL-GATE-BEGIN")
    correlation_pos = position(workflow, "IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-FINAL-BEGIN")
    require(final_chain_pos >= 0, errors, "final unified chain contract marker missing")
    require(correlation_pos >= 0, errors, "runtime evidence correlation final marker missing")
    require(
        final_chain_pos >= 0 and correlation_pos > final_chain_pos,
        errors,
        "runtime evidence correlation must run after final unified chain contract",
    )

    report = {
        "schema_version": 1,
        "kind": "runtime_evidence_correlation_launcher_wiring_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "positions": {
            "final_chain_contract": final_chain_pos,
            "runtime_evidence_correlation": correlation_pos,
        },
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
