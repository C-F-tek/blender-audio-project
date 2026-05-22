#!/usr/bin/env python3
"""Verify the canonical run has one CLI entry and one GUI view over the same core."""

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
    parser.add_argument("--output", default="output/validation/real_product_single_entry_exit_smoke.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    dispatch = read_text(repo / "ia_carmine/dispatch.py")
    run_cli = read_text(repo / "ia_carmine/runtime/run/cli.py")
    core_cli = read_text(repo / "ia_carmine/product/operator_product_core/cli.py")
    controller = read_text(repo / "ia_carmine/product/operator_product_core/controller.py")
    runner = read_text(repo / "ia_carmine/product/operator_product_core/runner.py")
    gui = read_text(repo / "ia_carmine/product/operator_product_core/view/cli.py")
    preflight = read_text(repo / "Tools/validation/real_product/preflight_gate/cli.py")

    checks = {
        "single_non_gui_entrypoint": '"run": "ia_carmine.runtime.run.cli:main"' in dispatch,
        "single_gui_view_entrypoint": '"operator_product_gui": "ia_carmine.product.operator_product_core.view.cli:main"'
        in dispatch,
        "run_mentions_canonical_command": "python -m ia_carmine.cli run" in run_cli,
        "run_builds_launcher_config": "LauncherConfig" in run_cli and "build_config" in run_cli,
        "run_calls_shared_controller": "OperatorProductController(config)" in run_cli,
        "gui_calls_shared_controller": "OperatorProductController(self.config())" in gui,
        "controller_owns_model_control": "run_operator_lab" in controller
        and "analyze_code_product" in controller,
        "runner_produces_exit_summary": "operator_product_lab_summary.json" in runner
        and "operator_product_lab_summary.md" in runner,
        "runner_requires_code_product": "CODE_PRODUCT_FULL_PATCH was not produced" in runner,
        "runner_validates_code_product": "code_product_review.json" in runner
        and "ia_carmine.product.code_product.artifact_intake" in runner,
        "safe_apply_separate_from_canonical_run": "--apply-safe" not in run_cli
        and "--apply-safe" in core_cli
        and "apply_safe_code_product" in controller,
        "preflight_contains_this_gate": "single_entry_exit" in preflight,
    }

    errors: list[str] = []
    for name, passed in checks.items():
        require(passed, errors, f"single entry/exit check failed: {name}")

    controller_pos = run_cli.find("OperatorProductController(config)")
    run_pos = run_cli.find("controller.run")
    require(controller_pos >= 0, errors, "controller construction missing in run entrypoint")
    require(run_pos > controller_pos, errors, "run must execute through shared controller")

    report = {
        "schema_version": 1,
        "kind": "real_product_single_entry_exit_smoke",
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "positions": {"controller": controller_pos, "run_call": run_pos},
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
