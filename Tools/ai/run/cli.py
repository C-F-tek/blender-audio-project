"""Canonical non-GUI heap/universe operator run.

This command is the Python twin of the operator GUI. It turns the long manual
PowerShell recipe into one profile-driven runtime command:

``python -m Tools.ai run --request-file <task.md>``
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from Tools.ai.operator_product_core import LauncherConfig
from Tools.ai.operator_product_core.io_utils import now_stamp
from Tools.ai.operator_product_core.profiles import (
    build_heap_command,
    profile_names,
    resolve_config,
    resolve_project_python,
    run_dir_for,
)
from Tools.ai.operator_product_core.controller import OperatorProductController

DEFAULT_TASK_FILE = "IA-Carmine_GUI_launcher_final_code_product_task.md"
DEFAULT_INTERMEDIATE_ROOT = "output/validation/operator_product_launcher_lab"
DEFAULT_PROFILE = "deep_external_heap"
DEFAULT_BRANCH = "codex/code-product-intake"

PREFLIGHT_FILES = [
    "Tools/ai/operator_product_view/cli.py",
    "Tools/ai/operator_product_core/controller.py",
    "Tools/ai/operator_product_core/cli.py",
    "Tools/ai/operator_product_core/runner.py",
    "Tools/ai/operator_product_core/profiles.py",
    "Tools/ai/run_heap_runtime_context_closure/cli.py",
    "Tools/ai/assemble_heap_final_readable_product/cli.py",
    "Tools/ai/code_product_artifact_intake/cli.py",
    "Tools/ai/code_product_artifact_intake/analyzer.py",
]


def default_task_md() -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / "Downloads" / DEFAULT_TASK_FILE


def default_final_root(stamp: str) -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / "Documents" / f"aicarmine_gui_launcher_lab_{stamp}"


def run_checked(command: list[str], *, cwd: Path) -> None:
    completed = subprocess.run(command, cwd=cwd, text=True, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"command failed with exit code {completed.returncode}: {command}")


def git_sync(repo_root: Path, branch: str) -> None:
    run_checked(["git", "fetch", "origin"], cwd=repo_root)
    run_checked(["git", "checkout", branch], cwd=repo_root)
    run_checked(["git", "pull", "--ff-only", "origin", branch], cwd=repo_root)
    run_checked(["git", "status", "--short"], cwd=repo_root)


def preflight(repo_root: Path, python_exe: str) -> None:
    run_checked([python_exe, "-m", "py_compile", *PREFLIGHT_FILES], cwd=repo_root)
    run_checked(["git", "diff", "--check"], cwd=repo_root)


def parse_set_overrides(raw_values: list[str]) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    for raw in raw_values:
        if "=" not in raw:
            raise SystemExit(f"--set expects key=value, got: {raw}")
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise SystemExit(f"--set key is empty: {raw}")
        if value.isdigit():
            overrides[key] = int(value)
        else:
            try:
                overrides[key] = float(value)
            except ValueError:
                overrides[key] = value
    return overrides


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", "--task-md", default="")
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--intermediate-root", default=DEFAULT_INTERMEDIATE_ROOT)
    parser.add_argument("--final-root", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--revision-context", default="auto_latest")
    parser.add_argument("--timeout-seconds", type=int, default=24000)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--git-sync", action="store_true")
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list-profiles", action="store_true")
    parser.add_argument("--apply-safe", action="store_true")
    parser.add_argument("--confirm", default="")
    parser.add_argument("--require-all-integrated", action="store_true")
    return parser


def build_config(args: argparse.Namespace, repo_root: Path, stamp: str) -> LauncherConfig:
    request_file = Path(args.request_file) if args.request_file else default_task_md()
    final_root = Path(args.final_root) if args.final_root else default_final_root(stamp)
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=Path(args.intermediate_root),
        final_root=final_root,
        profile_name=args.profile,
        python_exe=args.python_exe,
        stamp=stamp,
        revision_context=args.revision_context,
        profile_overrides=parse_set_overrides(args.set),
    )


def dry_run_report(config: LauncherConfig) -> dict[str, Any]:
    cfg = resolve_config(config)
    return {
        "schema_version": 1,
        "kind": "operator_universe_run_plan",
        "execution_performed": False,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "profile_name": cfg.profile_name,
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir_for(cfg)),
        "final_root": str(cfg.final_root),
        "command": build_heap_command(cfg),
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    if args.list_profiles:
        print(json.dumps({"profiles": profile_names(repo_root)}, indent=2))
        return 0

    stamp = args.stamp or now_stamp()
    config = build_config(args, repo_root, stamp)
    cfg = resolve_config(config)
    python_exe = resolve_project_python(repo_root, args.python_exe)

    if args.apply_safe and args.confirm != "safe_apply":
        raise SystemExit("--apply-safe requires --confirm safe_apply")
    if not cfg.request_file.exists() and not args.dry_run:
        raise SystemExit(f"Task markdown not found: {cfg.request_file}")

    if args.git_sync:
        if args.dry_run:
            print(f"[dry-run] would sync origin/{args.branch}")
        else:
            git_sync(repo_root, args.branch)
    if not args.skip_preflight and not args.dry_run:
        preflight(repo_root, python_exe)

    if args.dry_run:
        print(json.dumps(dry_run_report(config), indent=2, ensure_ascii=False))
        return 0

    controller = OperatorProductController(config)
    report = controller.run(
        timeout=args.timeout_seconds,
        apply_safe=args.apply_safe,
        require_all_integrated=args.require_all_integrated,
    )
    report["canonical_entrypoint"] = "python -m Tools.ai run"
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
