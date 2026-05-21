"""Canonical non-GUI heap/universe operator run.

This command is the single operator product entry for the current
contractor-universe runtime:

``python -m Tools.ai run --request-file <task.md>``
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from Tools.ai._shared.live_flow_monitor import CRLF_WARNING_RE
from Tools.ai.contractor_universe.runtime import ContractorUniverseRuntime
from Tools.ai.operator_product_core import LauncherConfig
from Tools.ai.operator_product_core.io_utils import now_stamp
from Tools.ai.operator_product_core.profiles import (
    profile_names,
    resolve_config,
    resolve_project_python,
    run_dir_for,
    select_profile,
)

DEFAULT_TASK_FILE = "IA-Carmine_GUI_launcher_final_code_product_task.md"
DEFAULT_INTERMEDIATE_ROOT = "output/validation/operator_product_launcher_lab"
DEFAULT_PROFILE = "deep_external_heap"
DEFAULT_BRANCH = "codex/code-product-intake"

CONTRACTOR_PREFLIGHT_FILES = [
    "Tools/ai/_shared/report_io.py",
    "Tools/ai/contractor_universe/__init__.py",
    "Tools/ai/contractor_universe/agents.py",
    "Tools/ai/contractor_universe/clock.py",
    "Tools/ai/contractor_universe/heap.py",
    "Tools/ai/contractor_universe/models.py",
    "Tools/ai/contractor_universe/runtime.py",
    "Tools/ai/provider_runtime_blackboard/common.py",
    "Tools/ai/provider_runtime_blackboard/heap.py",
    "Tools/ai/runtime_universe/builder.py",
]

INTENSITY_PROFILES = {
    "quick": "fast_external_heap",
    "balanced": "balanced_external_heap",
    "deep": "deep_external_heap",
}


def default_task_md() -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / "Downloads" / DEFAULT_TASK_FILE


def default_final_root(stamp: str) -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / "Documents" / f"aicarmine_gui_launcher_lab_{stamp}"


def process_gate_task_path(repo_root: Path, stamp: str) -> Path:
    return repo_root / "output" / "local_ai_task_inputs" / f"heap-exchange-process-gate-{stamp}.md"


def write_process_gate_task(repo_root: Path, stamp: str) -> Path:
    task_path = process_gate_task_path(repo_root, stamp)
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        "\n".join(
            [
                f"# Heap Exchange Process Gate - {stamp}",
                "",
                "## Objective",
                "",
                "Execute the IA-Carmine product path through the canonical entrypoint.",
                "",
                "## Input Contract",
                "",
                "- Entrypoint: `python -m Tools.ai run`.",
                "- Route: Tools.ai.run -> contractor_universe runtime -> blackboard/pointer artifacts.",
                "- Use existing repo modules only; do not create a parallel runner, mode switch or storage layer.",
                "- Treat this Markdown as controlled task input only, not runtime memory.",
                "",
                "## Required Runtime Evidence",
                "",
                "- Local request enters the contractor universe heap.",
                "- ProviderRuntimeHeap event log and snapshot are written as compact evidence.",
                "- GPU1/GPU0/NPU contractor roles publish pointer-linked blocks.",
                "- Product exit is either reviewable product evidence or `blocked_with_reason`.",
                "",
                "## Failure Policy",
                "",
                "A smoke, static report, package write or provider-only proposal is not product success.",
                "Smoke/full-run wrappers are downstream verification, not entry commands.",
                "`patch_application_performed` remains false unless an explicit apply boundary is requested.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return task_path


def run_checked(command: list[str], *, cwd: Path) -> None:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        check=False,
        capture_output=True,
    )
    suppressed = _print_filtered_output(completed.stdout or "", stream_name="stdout")
    suppressed += _print_filtered_output(completed.stderr or "", stream_name="stderr")
    if suppressed:
        print(f"[preflight] compressed {suppressed} git CRLF line-ending warnings")
    if completed.returncode != 0:
        raise SystemExit(f"command failed with exit code {completed.returncode}: {command}")


def _print_filtered_output(text: str, *, stream_name: str) -> int:
    suppressed = 0
    kept: list[str] = []
    for line in text.splitlines():
        if CRLF_WARNING_RE.match(line.strip()):
            suppressed += 1
        else:
            kept.append(line)
    if kept:
        print("\n".join(kept))
    return suppressed


def git_sync(repo_root: Path, branch: str) -> None:
    run_checked(["git", "fetch", "origin"], cwd=repo_root)
    run_checked(["git", "checkout", branch], cwd=repo_root)
    run_checked(["git", "pull", "--ff-only", "origin", branch], cwd=repo_root)
    run_checked(["git", "status", "--short"], cwd=repo_root)


def preflight(repo_root: Path, python_exe: str) -> None:
    run_checked([python_exe, "-m", "py_compile", *CONTRACTOR_PREFLIGHT_FILES], cwd=repo_root)
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
        elif value.lower() in {"true", "false"}:
            overrides[key] = value.lower() == "true"
        else:
            try:
                overrides[key] = float(value)
            except ValueError:
                overrides[key] = value
    return overrides


def profile_from_args(args: argparse.Namespace) -> str:
    if args.profile:
        return args.profile
    return INTENSITY_PROFILES.get(args.run_intensity, DEFAULT_PROFILE)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-RepoRoot", "--repo-root", dest="repo_root", default=".")
    parser.add_argument(
        "-TaskFile",
        "--request-file",
        "--task-md",
        dest="request_file",
        default="",
    )
    parser.add_argument("-ProcessGateTask", dest="process_gate_task", action="store_true")
    parser.add_argument("--profile", default="")
    parser.add_argument(
        "-RunIntensity",
        "--run-intensity",
        dest="run_intensity",
        default="deep",
        choices=("quick", "balanced", "deep", "custom"),
    )
    parser.add_argument("--intermediate-root", default=DEFAULT_INTERMEDIATE_ROOT)
    parser.add_argument("--final-root", default="")
    parser.add_argument("-PythonExe", "--python-exe", dest="python_exe", default="")
    parser.add_argument("-Stamp", "--stamp", dest="stamp", default="")
    parser.add_argument(
        "-Model",
        "--model",
        "--provider-model",
        dest="provider_model",
        default="",
        help="Explicit GPU1/Ollama model for the heap provider lane.",
    )
    parser.add_argument("-MaxNewTokens", "--max-new-tokens", dest="max_new_tokens", type=int)
    parser.add_argument("--ollama-num-ctx", dest="ollama_num_ctx", type=int)
    parser.add_argument("-KeepAlive", "--keep-alive", dest="keep_alive", default="")
    parser.add_argument("--gpu0-iterations", dest="gpu0_iterations", type=int)
    parser.add_argument("--gpu0-min-seconds", dest="gpu0_min_seconds", type=float)
    parser.add_argument("--npu-micro-timeout-seconds", dest="npu_micro_timeout_seconds", type=int)
    parser.add_argument("--npu-max-context-chars", dest="npu_max_context_chars", type=int)
    parser.add_argument("--npu-max-prompt-chars", dest="npu_max_prompt_chars", type=int)
    parser.add_argument("--npu-max-new-tokens", dest="npu_max_new_tokens", type=int)
    parser.add_argument("--context-document-count", dest="context_document_count", type=int)
    parser.add_argument(
        "--context-document-preview-chars",
        dest="context_document_preview_chars",
        type=int,
    )
    parser.add_argument("--semantic-code-chunk-limit", dest="semantic_code_chunk_limit", type=int)
    parser.add_argument(
        "--semantic-code-chunk-preview-chars",
        dest="semantic_code_chunk_preview_chars",
        type=int,
    )
    parser.add_argument(
        "--semantic-evidence-chunk-limit",
        dest="semantic_evidence_chunk_limit",
        type=int,
    )
    parser.add_argument("--memory-search-limit", dest="memory_search_limit", type=int)
    parser.add_argument("--tool-catalog-limit", dest="tool_catalog_limit", type=int)
    parser.add_argument(
        "--allow-npu-device-workload",
        dest="allow_npu_device_workload",
        action="store_true",
        help="Opt in to bounded NPU device workload; semantic NPU audit still runs without it.",
    )
    parser.add_argument("--revision-context", default="auto_latest")
    parser.add_argument("--timeout-seconds", type=int, default=None)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--git-sync", action="store_true")
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("-DryRun", "--dry-run", dest="dry_run", action="store_true")
    parser.add_argument("--list-profiles", action="store_true")
    return parser


def resolve_request_file(args: argparse.Namespace, repo_root: Path, stamp: str) -> Path:
    if args.request_file:
        return Path(args.request_file)
    if args.process_gate_task:
        if args.dry_run:
            return process_gate_task_path(repo_root, stamp)
        return write_process_gate_task(repo_root, stamp)
    return default_task_md()


def build_config(args: argparse.Namespace, repo_root: Path, stamp: str) -> LauncherConfig:
    request_file = resolve_request_file(args, repo_root, stamp)
    final_root = Path(args.final_root) if args.final_root else default_final_root(stamp)
    overrides = parse_set_overrides(args.set)
    for key in (
        "provider_model",
        "ollama_num_ctx",
        "max_new_tokens",
        "keep_alive",
        "gpu0_iterations",
        "gpu0_min_seconds",
        "npu_micro_timeout_seconds",
        "npu_max_context_chars",
        "npu_max_prompt_chars",
        "npu_max_new_tokens",
        "context_document_count",
        "context_document_preview_chars",
        "semantic_code_chunk_limit",
        "semantic_code_chunk_preview_chars",
        "semantic_evidence_chunk_limit",
        "memory_search_limit",
        "tool_catalog_limit",
        "timeout_seconds",
    ):
        value = getattr(args, key, None)
        if key == "timeout_seconds" and not value:
            continue
        if value not in ("", None):
            overrides[key] = value
    if args.allow_npu_device_workload:
        overrides["allow_npu_device_workload"] = True
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=Path(args.intermediate_root),
        final_root=final_root,
        profile_name=profile_from_args(args),
        python_exe=args.python_exe,
        stamp=stamp,
        revision_context=args.revision_context,
        profile_overrides=overrides,
    )


def contractor_runtime_args(cfg: LauncherConfig) -> argparse.Namespace:
    profile = select_profile(cfg.repo_root, cfg.profile_name, cfg.profiles_file)
    for key, value in (cfg.profile_overrides or {}).items():
        if value not in ("", None):
            profile[key] = value
    return argparse.Namespace(
        budget_minutes=int(profile.get("budget_minutes") or 10),
        timeout_seconds=int(profile.get("timeout_seconds") or 600),
    )


def dry_run_report(config: LauncherConfig) -> dict[str, Any]:
    cfg = resolve_config(config)
    return {
        "schema_version": 1,
        "kind": "operator_universe_run_plan",
        "canonical_entrypoint": "python -m Tools.ai run",
        "runtime": "contractor_universe",
        "single_product_entry": True,
        "parallel_product_entry": False,
        "smoke_product_entry": False,
        "execution_performed": False,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "profile_name": cfg.profile_name,
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir_for(cfg)),
        "final_root": str(cfg.final_root),
        "internal_runtime": "Tools.ai.contractor_universe.runtime.ContractorUniverseRuntime",
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

    if not cfg.request_file.exists() and not args.dry_run:
        raise SystemExit(f"Task markdown not found: {cfg.request_file}")

    if args.git_sync:
        if args.dry_run:
            print(f"[dry-run] would sync origin/{args.branch}")
        else:
            git_sync(repo_root, args.branch)
    if not args.dry_run:
        preflight(repo_root, python_exe)

    if args.dry_run:
        print(json.dumps(dry_run_report(config), indent=2, ensure_ascii=False))
        return 0

    runtime = ContractorUniverseRuntime(
        repo_root=repo_root,
        output_dir=run_dir_for(cfg),
        stamp=cfg.stamp,
        request_text=cfg.request_file.read_text(encoding="utf-8-sig", errors="replace"),
        args=contractor_runtime_args(cfg),
    )
    report = runtime.run()
    report.update(
        {
            "canonical_entrypoint": "python -m Tools.ai run",
            "single_product_entry": True,
            "parallel_product_entry": False,
            "smoke_product_entry": False,
            "python_exe": python_exe,
        }
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("product_status") == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
