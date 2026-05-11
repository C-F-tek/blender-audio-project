#!/usr/bin/env python3
"""Build a PowerShell command for run_heap_runtime_context_closure.py from JSON profiles.

This tool does not execute the heap runtime. It externalizes launcher variables,
prints/writes a command that an operator can review, and preserves non-CLI
profile metadata for external heap-universe adapters such as block pointer
manifests.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_PROFILE_FILE = "Tools/ai/heap_runtime_launcher_profiles.json"
PROFILE_TO_CLI: dict[str, tuple[str, str]] = {
    "budget_minutes": ("--budget-minutes", "value"),
    "max_iterations": ("--max-iterations", "value"),
    "max_provider_revisions": ("--max-provider-revisions", "value"),
    "timeout_seconds": ("--timeout-seconds", "value"),
    "preflight_timeout_seconds": ("--preflight-timeout-seconds", "value"),
    "npu_device_workload_seconds": ("--npu-device-workload-seconds", "value"),
    "npu_device_workload_iterations": ("--npu-device-workload-iterations", "value"),
    "startup_max_memory_chars": ("--startup-max-memory-chars", "value"),
    "startup_max_context_files": ("--startup-max-context-files", "value"),
    "startup_max_chars_per_file": ("--startup-max-chars-per-file", "value"),
    "documents_root": ("--documents-root", "value"),
    "output_dir": ("--output-dir", "value"),
    "stamp": ("--stamp", "value"),
    "allow_provider_generation": ("--allow-provider-generation", "flag"),
    "skip_preflight": ("--skip-preflight", "flag"),
    "skip_startup_reload": ("--skip-startup-reload", "flag"),
    "strict_startup_reload": ("--strict-startup-reload", "flag"),
    "no_documents": ("--no-documents", "flag"),
}

EXTERNAL_METADATA_KEYS = (
    "context_document_count",
    "context_document_preview_chars",
    "semantic_code_chunk_limit",
    "semantic_code_chunk_preview_chars",
    "semantic_evidence_chunk_limit",
    "memory_search_limit",
    "tool_catalog_limit",
    "universe_enabled",
    "universe_roles",
    "universe_max_steps",
    "universe_stop_condition",
    "block_pointer_protocol",
    "max_blocks_per_step",
    "max_block_chars",
    "max_revision_depth",
    "allow_backrefinement",
    "allow_forward_pointers",
    "require_resume_pointer",
    "require_refines_pointer",
)


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit(f"JSON profile file must contain an object: {path}")
    return data


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


def ps_quote(value: Any) -> str:
    text = str(value)
    return '"' + text.replace('`', '``').replace('"', '`"') + '"'


def choose_profile(profile_doc: dict[str, Any], profile_name: str) -> dict[str, Any]:
    profiles = profile_doc.get("profiles") if isinstance(profile_doc.get("profiles"), dict) else {}
    selected = profile_name or str(profile_doc.get("default_profile") or "")
    profile = profiles.get(selected)
    if not isinstance(profile, dict):
        raise SystemExit(f"unknown profile '{selected}'. Available: {', '.join(sorted(profiles))}")
    result = dict(profile)
    result["profile_name"] = selected
    return result


def apply_overrides(profile: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    result = dict(profile)
    for override in overrides:
        if "=" not in override:
            raise SystemExit(f"invalid override: {override}; expected key=value")
        key, value = override.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.lower() in {"true", "false"}:
            result[key] = value.lower() == "true"
        else:
            try:
                result[key] = int(value)
            except ValueError:
                try:
                    result[key] = float(value)
                except ValueError:
                    if value.startswith("[") or value.startswith("{"):
                        try:
                            result[key] = json.loads(value)
                            continue
                        except json.JSONDecodeError:
                            pass
                    result[key] = value
    return result


def profile_cli_keys(profile: dict[str, Any]) -> list[str]:
    return [key for key in profile if key in PROFILE_TO_CLI]


def profile_external_metadata(profile: dict[str, Any]) -> dict[str, Any]:
    return {key: profile[key] for key in EXTERNAL_METADATA_KEYS if key in profile}


def render_command(repo_root: Path, project_python: str, profile: dict[str, Any], request_override: str) -> str:
    parts = [
        "& " + ps_quote(project_python),
        ps_quote(".\\Tools\\ai\\run_heap_runtime_context_closure.py"),
        "`\n  --repo-root .",
        "`\n  --python-exe " + ps_quote(project_python),
    ]
    request = request_override.strip() or str(profile.get("request") or "")
    if request:
        parts.append("`\n  --request " + ps_quote(request))
    for key, (cli_arg, mode) in PROFILE_TO_CLI.items():
        if key not in profile:
            continue
        value = profile.get(key)
        if mode == "flag":
            if bool(value):
                parts.append("`\n  " + cli_arg)
        elif value is not None and value != "":
            parts.append("`\n  " + cli_arg + " " + ps_quote(value))
    return " ".join(parts) + "\n"


def render_block_pointer_command(repo_root: Path, project_python: str, profile: dict[str, Any]) -> str:
    max_block_chars = profile.get("max_block_chars", 9000)
    max_blocks = int(profile.get("max_blocks_per_step", 0) or 0) * int(profile.get("universe_max_steps", 0) or 0)
    return (
        "$RunDir = Get-ChildItem .\\output\\validation -Directory | `\n"
        "  Where-Object Name -like \"heap_context_closure_*\" | `\n"
        "  Sort-Object LastWriteTime -Descending | `\n"
        "  Select-Object -First 1\n\n"
        "& "
        + ps_quote(project_python)
        + " "
        + ps_quote(".\\Tools\\ai\\build_external_heap_block_pointer_manifest.py")
        + " `\n  --repo-root ."
        + " `\n  --run-dir $RunDir.FullName"
        + " `\n  --max-block-chars "
        + ps_quote(max_block_chars)
        + (" `\n  --max-blocks " + ps_quote(max_blocks) if max_blocks > 0 else "")
        + "\n"
    )


def list_profiles(profile_doc: dict[str, Any]) -> dict[str, Any]:
    profiles = profile_doc.get("profiles") if isinstance(profile_doc.get("profiles"), dict) else {}
    return {
        "schema_version": 1,
        "kind": "heap_runtime_launcher_profile_list",
        "default_profile": profile_doc.get("default_profile"),
        "profile_control_groups": profile_doc.get("profile_control_groups", {}),
        "profiles": [
            {
                "name": name,
                "description": value.get("description", "") if isinstance(value, dict) else "",
                "universe_enabled": value.get("universe_enabled") if isinstance(value, dict) else None,
                "context_document_count": value.get("context_document_count") if isinstance(value, dict) else None,
                "semantic_code_chunk_limit": value.get("semantic_code_chunk_limit") if isinstance(value, dict) else None,
            }
            for name, value in sorted(profiles.items())
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--profiles", default=DEFAULT_PROFILE_FILE)
    parser.add_argument("--profile", default="")
    parser.add_argument("--request", default="")
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--list-profiles", action="store_true")
    parser.add_argument("--include-block-pointer-command", action="store_true")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    project_python = resolve_project_python(repo_root, args.python_exe)
    profiles_path = Path(args.profiles)
    if not profiles_path.is_absolute():
        profiles_path = repo_root / profiles_path
    profile_doc = read_json(profiles_path)

    if args.list_profiles:
        print(json.dumps(list_profiles(profile_doc), indent=2, ensure_ascii=False))
        return 0

    profile = apply_overrides(choose_profile(profile_doc, args.profile), args.set)
    command = render_command(repo_root, project_python, profile, args.request)
    block_pointer_command = render_block_pointer_command(repo_root, project_python, profile)
    report = {
        "schema_version": 2,
        "kind": "heap_runtime_launcher_command",
        "repo_root": repo_root.as_posix(),
        "profiles_file": str(profiles_path),
        "profile_name": profile.get("profile_name"),
        "profile": profile,
        "cli_bound_profile_keys": profile_cli_keys(profile),
        "external_metadata": profile_external_metadata(profile),
        "command": command,
        "block_pointer_command": block_pointer_command,
        "execution_performed": False,
        "notes": [
            "command targets run_heap_runtime_context_closure.py",
            "block_pointer_command targets the external heap block-pointer manifest adapter",
            "non-CLI metadata is preserved for external adapters and future launcher wiring",
        ],
    }
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(command)
    if args.include_block_pointer_command:
        print("\n# External heap block-pointer manifest command")
        print(block_pointer_command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
