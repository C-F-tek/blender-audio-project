#!/usr/bin/env python3
"""Static smoke for the canonical operator product run profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def has(text: str, token: str) -> bool:
    return token in text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/real_product_profile_smoke.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    dispatch_text = read_text(repo / "Tools/ai/dispatch.py")
    run_text = read_text(repo / "Tools/ai/run/cli.py")
    controller_text = read_text(repo / "Tools/ai/operator_product_core/controller.py")
    runner_text = read_text(repo / "Tools/ai/operator_product_core/runner.py")
    profiles_text = read_text(repo / "Tools/ai/operator_product_core/profiles.py")
    view_text = read_text(repo / "Tools/ai/operator_product_core/view/cli.py")
    profile_doc = read_json(repo / "Tools/ai/run/profiles/heap_runtime_launcher_profiles.json")
    deep_profile = (profile_doc.get("profiles") or {}).get("deep_external_heap", {})
    balanced_profile = (profile_doc.get("profiles") or {}).get("balanced_external_heap", {})

    checks = {
        "run_entrypoint_registered": '"run": "Tools.ai.run.cli:main"' in dispatch_text,
        "gui_entrypoint_registered": '"operator_product_gui": "Tools.ai.operator_product_core.view.cli:main"' in dispatch_text,
        "canonical_entrypoint_recorded": "python -m Tools.ai run" in run_text,
        "run_uses_shared_controller": "OperatorProductController" in run_text,
        "gui_uses_same_controller": "OperatorProductController" in view_text,
        "controller_shared_by_cli_and_gui": "run_operator_lab" in controller_text
        and "review_code_product" in controller_text,
        "task_markdown_required_for_execution": "Task markdown not found" in run_text
        and "not args.dry_run" in run_text,
        "preflight_compiles_product_modules": "py_compile" in run_text
        and "PREFLIGHT_FILES" in run_text,
        "preflight_runs_git_diff_check": 'git", "diff", "--check"' in run_text,
        "runner_invokes_heap_context_closure": "heap_context_closure" in profiles_text,
        "runner_packages_final_readable_product": "launcher_passed" in runner_text
        and "CODE_PRODUCT_FULL_PATCH.md" in runner_text,
        "runner_intakes_code_product": "Tools.ai.code_product.artifact_intake" in runner_text,
        "canonical_run_has_no_apply_safe_flag": "--apply-safe" not in run_text
        and "apply_safe=args.apply_safe" not in run_text,
        "run_does_not_expose_skip_preflight": "skip-preflight" not in run_text
        and "skip_preflight" not in profiles_text,
        "no_merge_or_force_push": "git merge" not in run_text
        and "git push --force" not in run_text
        and "--force-with-lease" not in run_text,
        "profiles_file_has_default": profile_doc.get("default_profile") == "deep_external_heap",
        "balanced_profile_provider_enabled": balanced_profile.get("allow_provider_generation") is True,
        "deep_profile_matches_manual_budget": deep_profile.get("budget_minutes") == 20
        and deep_profile.get("max_iterations") == 80
        and deep_profile.get("max_rounds") == 24
        and deep_profile.get("max_provider_revisions") == 12,
        "deep_profile_preserves_startup_context_depth": deep_profile.get("startup_max_memory_chars") == 1280000
        and deep_profile.get("startup_max_context_files") == 20800
        and deep_profile.get("startup_scan_context_files") == 20800
        and deep_profile.get("startup_max_chars_per_file") == 200000,
        "heap_universe_roles_present": set(deep_profile.get("universe_roles") or [])
        >= {"gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"},
        "block_pointer_protocol_present": deep_profile.get("block_pointer_protocol")
        == "external_heap_block_pointer_v1",
        "documents_output_enabled": deep_profile.get("no_documents") is False,
        "provider_generation_enabled": deep_profile.get("allow_provider_generation") is True,
        "gui_is_view_not_separate_runner": "self.controller().run()" in view_text
        and "controller().build_command()" in view_text,
    }

    errors = [f"real product profile check failed: {name}" for name, ok in checks.items() if not ok]
    report = {
        "schema_version": 1,
        "kind": "real_product_profile_smoke",
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "canonical_entrypoint": "python -m Tools.ai run",
        "gui_entrypoint": "python -m Tools.ai operator_product_gui",
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
