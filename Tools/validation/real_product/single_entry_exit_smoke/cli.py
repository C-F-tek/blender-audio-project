#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/real_product_single_entry_exit_smoke.json"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    wrapper = read_text(repo_root / "Tools/workflow/_powershell/run_unified_real_product_pr.ps1")
    preflight = read_text(repo_root / "Tools/validation/real_product/preflight_gate/cli.py")
    readme = read_text(repo_root / "Tools/workflow/README.md")

    checks = {
        "task_file_optional": '[string]$TaskFile = ""' in wrapper,
        "process_gate_task_switch": "[switch]$ProcessGateTask" in wrapper,
        "process_gate_task_generator": "function New-HeapExchangeProcessGateTask" in wrapper,
        "process_gate_task_under_output": "output/local_ai_task_inputs" in wrapper,
        "single_wrapper_launches_unified_launcher": "run_unified_local_ai_refactor.ps1" in wrapper,
        "final_product_validation_switch": "[switch]$ValidateFinalReviewPrProduct" in wrapper,
        "create_pr_implies_final_validation": "if ($CreatePr) { $ValidateFinalReviewPrProduct = $true }"
        in wrapper,
        "final_product_contract_invoked": "check_review_pr_final_product_contract.py" in wrapper,
        "remote_pr_contract_required_when_create_pr": "--require-remote-pr" in wrapper
        and "if ($CreatePr)" in wrapper,
        "single_exit_after_contract": "Review PR final product contract passed" in wrapper
        and "exit 0" in wrapper,
        "preflight_validates_single_entry_exit": "run_real_product_single_entry_exit_smoke.py"
        in preflight,
        "readme_documents_single_entry_exit": "REAL-PRODUCT-SINGLE-ENTRY-EXIT" in readme,
    }

    errors: list[str] = []
    for name, passed in checks.items():
        require(passed, errors, f"single entry/exit check failed: {name}")

    launcher_pos = wrapper.find("& powershell.exe @script:LauncherArgs")
    contract_pos = wrapper.find("check_review_pr_final_product_contract.py")
    require(launcher_pos >= 0, errors, "launcher invocation missing")
    require(
        contract_pos > launcher_pos,
        errors,
        "final product contract must run after unified launcher",
    )

    report = {
        "schema_version": 1,
        "kind": "real_product_single_entry_exit_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "positions": {
            "launcher_invocation": launcher_pos,
            "final_product_contract": contract_pos,
        },
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
