#!/usr/bin/env python3
"""Operator launcher core for heap final-product runs and safe apply."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

PROFILE_FILE = "Tools/ai/heap_runtime_launcher_profiles.json"
DEFAULT_PROFILE = "balanced_external_heap"
CLI_VALUE_KEYS = {
    "budget_minutes": "--budget-minutes",
    "max_iterations": "--max-iterations",
    "min_runtime_rounds": "--min-runtime-rounds",
    "min_proposal_iterations": "--min-proposal-iterations",
    "max_rounds": "--max-rounds",
    "max_provider_revisions": "--max-provider-revisions",
    "timeout_seconds": "--timeout-seconds",
    "preflight_timeout_seconds": "--preflight-timeout-seconds",
    "npu_device_workload_seconds": "--npu-device-workload-seconds",
    "npu_device_workload_iterations": "--npu-device-workload-iterations",
    "startup_max_memory_chars": "--startup-max-memory-chars",
    "startup_max_context_files": "--startup-max-context-files",
    "startup_scan_context_files": "--startup-scan-context-files",
    "startup_max_chars_per_file": "--startup-max-chars-per-file",
}
CLI_FLAG_KEYS = {
    "allow_provider_generation": "--allow-provider-generation",
    "skip_preflight": "--skip-preflight",
    "skip_startup_reload": "--skip-startup-reload",
    "strict_startup_reload": "--strict-startup-reload",
    "no_documents": "--no-documents",
}


@dataclass
class LauncherConfig:
    repo_root: Path
    request_file: Path
    intermediate_root: Path
    final_root: Path
    profile_name: str = DEFAULT_PROFILE
    python_exe: str = ""
    stamp: str = ""
    revision_context: str = ""
    profiles_file: Path | None = None
    profile_overrides: dict[str, Any] | None = None


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def read_json_quiet(path: Path) -> dict[str, Any]:
    try:
        return read_json(path)
    except Exception:
        return {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def load_profiles(repo_root: Path, profiles_file: Path | None = None) -> dict[str, Any]:
    path = profiles_file or repo_root / PROFILE_FILE
    if not path.is_absolute():
        path = repo_root / path
    return read_json(path)


def profile_names(repo_root: Path) -> list[str]:
    profiles = load_profiles(repo_root).get("profiles", {})
    return sorted(profiles) if isinstance(profiles, dict) else []


def select_profile(repo_root: Path, name: str, profiles_file: Path | None = None) -> dict[str, Any]:
    doc = load_profiles(repo_root, profiles_file)
    profiles = doc.get("profiles") if isinstance(doc.get("profiles"), dict) else {}
    selected = name or str(doc.get("default_profile") or DEFAULT_PROFILE)
    profile = profiles.get(selected)
    if not isinstance(profile, dict):
        raise SystemExit(f"unknown profile '{selected}'. Available: {', '.join(sorted(profiles))}")
    result = dict(profile)
    result["profile_name"] = selected
    return result


def resolve_config(config: LauncherConfig) -> LauncherConfig:
    repo_root = config.repo_root.resolve()
    request_file = config.request_file
    if not request_file.is_absolute():
        request_file = repo_root / request_file
    intermediate_root = config.intermediate_root
    if not intermediate_root.is_absolute():
        intermediate_root = repo_root / intermediate_root
    final_root = config.final_root
    if not final_root.is_absolute():
        final_root = repo_root / final_root
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file.resolve(strict=False),
        intermediate_root=intermediate_root.resolve(strict=False),
        final_root=final_root.resolve(strict=False),
        profile_name=config.profile_name,
        python_exe=resolve_project_python(repo_root, config.python_exe),
        stamp=config.stamp or now_stamp(),
        revision_context=config.revision_context,
        profiles_file=config.profiles_file,
        profile_overrides=dict(config.profile_overrides or {}),
    )


def run_dir_for(config: LauncherConfig) -> Path:
    return config.intermediate_root / f"heap_context_closure_{config.stamp}"


def build_heap_command(config: LauncherConfig) -> list[str]:
    cfg = resolve_config(config)
    profile = select_profile(cfg.repo_root, cfg.profile_name, cfg.profiles_file)
    for key, value in (cfg.profile_overrides or {}).items():
        if value not in ("", None):
            profile[key] = value
    revision_context = cfg.revision_context or str(
        profile.get("revision_context_mode") or "auto_latest"
    )
    command = [
        cfg.python_exe,
        "Tools/ai/run_heap_runtime_context_closure.py",
        "--repo-root",
        ".",
        "--python-exe",
        cfg.python_exe,
        "--request-file",
        str(cfg.request_file),
        "--stamp",
        cfg.stamp,
        "--output-dir",
        str(run_dir_for(cfg)),
        "--documents-root",
        str(cfg.final_root),
        "--revision-context",
        revision_context,
    ]
    for key, flag in CLI_VALUE_KEYS.items():
        if key in profile and profile[key] not in ("", None):
            command.extend([flag, str(profile[key])])
    for key, flag in CLI_FLAG_KEYS.items():
        if bool(profile.get(key)):
            command.append(flag)
    return command


def command_env(repo_root: Path, python_exe: str) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    env["IA_CARMINE_PYTHON"] = python_exe
    return env


def run_command(command: list[str], cwd: Path, timeout: int = 3600) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=command_env(cwd, command[0]),
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-6000:],
        "stderr_tail": (completed.stderr or "")[-6000:],
    }


def discover_code_product(run_dir: Path, summary: dict[str, Any]) -> str:
    outputs = summary.get("final_readable_product_documents_outputs")
    if isinstance(outputs, dict) and outputs.get("documents_code_product"):
        return str(outputs["documents_code_product"])
    for key in ("composer_documents_dir", "run_dir"):
        value = str(summary.get(key) or "")
        if value:
            candidate = Path(value) / "CODE_PRODUCT_FULL_PATCH.md"
            if candidate.exists():
                return str(candidate)
    candidate = run_dir / "CODE_PRODUCT_FULL_PATCH.md"
    return str(candidate) if candidate.exists() else ""


def run_heap(config: LauncherConfig, timeout: int = 3600) -> dict[str, Any]:
    cfg = resolve_config(config)
    command = build_heap_command(cfg)
    result = run_command(command, cfg.repo_root, timeout=timeout)
    run_dir = run_dir_for(cfg)
    summary_path = run_dir / "heap_runtime_context_closure_launcher.json"
    summary = read_json_quiet(summary_path)
    report = {
        "schema_version": 1,
        "kind": "operator_product_launcher_run",
        "repo_root": str(cfg.repo_root),
        "profile_name": cfg.profile_name,
        "stamp": cfg.stamp,
        "request_file": str(cfg.request_file),
        "intermediate_run_dir": str(run_dir),
        "final_root": str(cfg.final_root),
        "launcher_summary": str(summary_path) if summary_path.exists() else "",
        "code_product": discover_code_product(run_dir, summary),
        "run_result": result,
        "launcher_summary_payload": summary,
        "passed": bool(result.get("passed")) and bool(summary.get("launcher_packaging_succeeded")),
    }
    write_json(run_dir / "operator_product_launcher_run.json", report)
    write_text(run_dir / "operator_product_launcher_run.md", render_run_markdown(report))
    return report


def analyze_code_product(
    repo_root: Path,
    code_product: Path,
    output_dir: Path,
    apply_safe: bool = False,
    require_all_integrated: bool = False,
) -> dict[str, Any]:
    tool_root = Path(__file__).resolve().parents[2]
    output = output_dir / (
        "code_product_apply_safe.json" if apply_safe else "code_product_review.json"
    )
    markdown = output.with_suffix(".md")
    command = [
        resolve_project_python(repo_root),
        str(tool_root / "Tools" / "ai" / "analyze_code_product_artifact.py"),
        "--repo-root",
        str(repo_root),
        "--code-product",
        str(code_product),
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
    ]
    if apply_safe:
        command.append("--apply-safe")
    if require_all_integrated:
        command.append("--require-all-integrated")
    result = run_command(command, tool_root, timeout=600)
    payload = read_json_quiet(output)
    payload["operator_launcher_command_result"] = result
    write_json(output, payload)
    return payload


def render_run_markdown(report: dict[str, Any]) -> str:
    summary = (
        report.get("launcher_summary_payload")
        if isinstance(report.get("launcher_summary_payload"), dict)
        else {}
    )
    lines = [
        "# Operator Product Launcher Run",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Profile: `{report.get('profile_name')}`",
        f"- Request file: `{report.get('request_file')}`",
        f"- Run dir: `{report.get('intermediate_run_dir')}`",
        f"- Code product: `{report.get('code_product')}`",
        f"- Final readable passed: `{summary.get('final_readable_product_passed')}`",
        f"- Packaging succeeded: `{summary.get('launcher_packaging_succeeded')}`",
    ]
    result = report.get("run_result") if isinstance(report.get("run_result"), dict) else {}
    if result.get("returncode") not in (0, None):
        lines.extend(
            ["", "## Stderr Tail", "", "```text", str(result.get("stderr_tail") or ""), "```"]
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument(
        "--intermediate-root", default="output/validation/operator_product_launcher"
    )
    parser.add_argument("--final-root", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--revision-context", default="auto_latest")
    parser.add_argument("--code-product", default="")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--review-code-product", action="store_true")
    parser.add_argument("--apply-safe", action="store_true")
    parser.add_argument("--require-all-integrated", action="store_true")
    parser.add_argument("--list-profiles", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--startup-max-memory-chars", type=int, default=0)
    parser.add_argument("--startup-max-context-files", type=int, default=0)
    parser.add_argument("--startup-scan-context-files", type=int, default=0)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    if args.list_profiles:
        print(json.dumps({"profiles": profile_names(repo_root)}, indent=2))
        return 0
    stamp = args.stamp or now_stamp()
    final_root = args.final_root or str(
        Path.home() / "Documents" / f"aicarmine_operator_launcher_{stamp}"
    )
    request_file = (
        Path(args.request_file) if args.request_file else repo_root / "docs" / "README.md"
    )
    config = LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=Path(args.intermediate_root),
        final_root=Path(final_root),
        profile_name=args.profile,
        python_exe=args.python_exe,
        stamp=stamp,
        revision_context=args.revision_context,
        profile_overrides={
            key: value
            for key, value in {
                "startup_max_memory_chars": args.startup_max_memory_chars,
                "startup_max_context_files": args.startup_max_context_files,
                "startup_scan_context_files": args.startup_scan_context_files,
                "startup_max_chars_per_file": args.startup_max_chars_per_file,
            }.items()
            if value
        },
    )
    if args.run:
        report = run_heap(config, timeout=args.timeout_seconds)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("passed") else 2
    code_product = Path(args.code_product)
    if not args.code_product and args.request_file:
        code_product = Path(args.request_file)
    if args.review_code_product or args.apply_safe:
        output_dir = run_dir_for(resolve_config(config))
        report = analyze_code_product(
            repo_root,
            code_product,
            output_dir,
            apply_safe=args.apply_safe,
            require_all_integrated=args.require_all_integrated,
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report.get("passed") else 2
    command = build_heap_command(config)
    print(
        json.dumps(
            {"command": command, "profiles": profile_names(repo_root)}, indent=2, ensure_ascii=False
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
