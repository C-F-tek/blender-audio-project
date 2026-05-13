#!/usr/bin/env python3
"""Build a PowerShell command for run_heap_runtime_context_closure.py from JSON profiles.

This tool does not execute the heap runtime. It externalizes launcher variables,
prints/writes a command that an operator can review, and preserves non-CLI
profile metadata for external heap-universe adapters such as block pointer
manifests and revision-context propagation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_PROFILE_FILE = "Tools/ai/heap_runtime_launcher_profiles.json"
REQUIRED_COMPOSER_JSON = "heap_final_proposal_composer.json"
PROFILE_TO_CLI: dict[str, tuple[str, str]] = {
    "budget_minutes": ("--budget-minutes", "value"),
    "max_iterations": ("--max-iterations", "value"),
    "max_rounds": ("--max-rounds", "value"),
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
    "revision_context_mode",
    "revision_context_max_tasks",
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


def read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


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
    return '"' + text.replace("`", "``").replace('"', '`"') + '"'


def choose_profile(profile_doc: dict[str, Any], profile_name: str) -> dict[str, Any]:
    profiles = (
        profile_doc.get("profiles")
        if isinstance(profile_doc.get("profiles"), dict)
        else {}
    )
    selected = profile_name or str(profile_doc.get("default_profile") or "")
    profile = profiles.get(selected)
    if not isinstance(profile, dict):
        raise SystemExit(
            f"unknown profile '{selected}'. Available: {', '.join(sorted(profiles))}"
        )
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


def is_complete_heap_run_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and path.name.startswith("heap_context_closure_")
        and (path / REQUIRED_COMPOSER_JSON).exists()
    )


def latest_revision_context(repo_root: Path) -> tuple[Path | None, dict[str, Any]]:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return None, {}
    candidates = sorted(
        [
            path / "external_heap_revision_context.json"
            for path in validation_dir.iterdir()
            if is_complete_heap_run_dir(path)
            and (path / "external_heap_revision_context.json").exists()
        ],
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )
    if not candidates:
        return None, {}
    path = candidates[0].resolve()
    return path, read_optional_json(path)


def revision_context_from_profile(
    repo_root: Path, profile: dict[str, Any], explicit_path: str
) -> tuple[Path | None, dict[str, Any]]:
    mode = str(profile.get("revision_context_mode") or "off")
    if mode == "off":
        return None, {}
    if explicit_path.strip():
        path = Path(explicit_path)
        if not path.is_absolute():
            path = repo_root / path
        path = path.resolve()
        return path, read_optional_json(path)
    if mode == "auto_latest":
        return latest_revision_context(repo_root)
    return None, {}


def revision_context_prompt(
    payload: dict[str, Any], path: Path | None, max_tasks: int
) -> str:
    if not payload:
        return ""
    tasks = payload.get("tasks") if isinstance(payload.get("tasks"), list) else []
    limit = max(0, max_tasks)
    selected = tasks[:limit]
    candidate_summary = (
        payload.get("candidate_applicability_summary")
        if isinstance(payload.get("candidate_applicability_summary"), dict)
        else {}
    )
    lines = [
        "",
        "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN:",
        f"- path: {path if path else ''}",
        f"- protocol: {payload.get('protocol')}",
        f"- product_acceptance_status: {payload.get('product_acceptance_status')}",
        f"- product_acceptance_passed: {payload.get('product_acceptance_passed')}",
        f"- requires_concrete_rewrite: {payload.get('requires_concrete_rewrite')}",
        f"- priority_next_action: {payload.get('priority_next_action')}",
        f"- candidate_applicability_summary: {json.dumps(candidate_summary, ensure_ascii=False)}",
        f"- resume_from_block_id: {payload.get('resume_from_block_id')}",
        f"- latest_block_id: {payload.get('latest_block_id')}",
        f"- task_count: {len(tasks)}",
        "- GPU1 must consume rewrite/propagation tasks before emitting new proposal blocks.",
        "- If requires_concrete_rewrite=true, GPU1 must first rewrite non-concrete candidates with real repo paths and concrete operations.",
        "- GPU1 must not propagate symbols from candidates marked non-concrete or from sketch/stub code.",
        "- GPU1 may move backward to propagate imports, variables, functions, classes and contracts, then resume forward.",
        "- GPU0 and NPU tasks are parallel recheck/audit work over old pointers.",
        "TASKS:",
    ]
    for idx, task in enumerate(selected, start=1):
        if not isinstance(task, dict):
            continue
        lines.append(
            f"{idx}. {task.get('task_id')} role={task.get('role')} type={task.get('task_type')} target={task.get('target_block_id')} resume={task.get('resume_from_block_id')}"
        )
        if task.get("candidate_applicability_flags"):
            lines.append(
                f"   candidate_applicability_flags={json.dumps(task.get('candidate_applicability_flags'), ensure_ascii=False)}"
            )
        if task.get("symbol_propagation_skipped"):
            lines.append(
                f"   symbol_propagation_skipped={task.get('symbol_propagation_skipped')} reason={task.get('symbol_propagation_skip_reason')}"
            )
        if task.get("discovered_symbols"):
            lines.append(
                f"   discovered_symbols={json.dumps(task.get('discovered_symbols'), ensure_ascii=False)}"
            )
        if task.get("rejection_reasons"):
            lines.append(
                f"   rejection_reasons={json.dumps(task.get('rejection_reasons'), ensure_ascii=False)}"
            )
        if task.get("instruction"):
            lines.append(f"   instruction={task.get('instruction')}")
    if len(tasks) > len(selected):
        lines.append(
            f"- omitted_tasks={len(tasks) - len(selected)}; read full revision context artifact for remaining tasks."
        )
    return "\n".join(lines)


def render_command(
    repo_root: Path,
    project_python: str,
    profile: dict[str, Any],
    request_override: str,
    revision_context_path: Path | None,
    revision_context_payload: dict[str, Any],
) -> str:
    parts = [
        "& " + ps_quote(project_python),
        ps_quote(".\\Tools\\ai\\run_heap_runtime_context_closure.py"),
        "`\n  --repo-root .",
        "`\n  --python-exe " + ps_quote(project_python),
    ]
    request = request_override.strip() or str(profile.get("request") or "")
    request += revision_context_prompt(
        revision_context_payload,
        revision_context_path,
        int(profile.get("revision_context_max_tasks") or 12),
    )
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


def latest_run_dir_snippet() -> str:
    return (
        "$RunDir = Get-ChildItem .\\output\\validation -Directory | `\n"
        '  Where-Object { $_.Name -like "heap_context_closure_*" -and (Test-Path (Join-Path $_.FullName "heap_final_proposal_composer.json")) } | `\n'
        "  Sort-Object LastWriteTime -Descending | `\n"
        "  Select-Object -First 1\n"
    )


def render_block_pointer_command(
    repo_root: Path, project_python: str, profile: dict[str, Any]
) -> str:
    max_block_chars = profile.get("max_block_chars", 9000)
    max_blocks = int(profile.get("max_blocks_per_step", 0) or 0) * int(
        profile.get("universe_max_steps", 0) or 0
    )
    return (
        latest_run_dir_snippet()
        + "\n& "
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


def render_revision_context_command(repo_root: Path, project_python: str) -> str:
    return (
        latest_run_dir_snippet()
        + '\n$PointerPath = Join-Path $RunDir.FullName "external_heap_block_pointer_manifest.json"\n'
        + '$ComposerPath = Join-Path $RunDir.FullName "heap_final_proposal_composer.json"\n'
        + '$CausalityPath = Join-Path $RunDir.FullName "heap_final_causality_normalized.json"\n\n'
        + "& "
        + ps_quote(project_python)
        + " "
        + ps_quote(".\\Tools\\ai\\build_external_heap_revision_context.py")
        + " `\n  --pointer-manifest $PointerPath"
        + " `\n  --composer-json $ComposerPath"
        + " `\n  --causality-json $CausalityPath"
        + ' `\n  --output (Join-Path $RunDir.FullName "external_heap_revision_context.json")\n'
    )


def render_postrun_package_command(repo_root: Path, project_python: str) -> str:
    return (
        "& "
        + ps_quote(project_python)
        + " "
        + ps_quote(".\\Tools\\ai\\run_external_heap_postrun_package.py")
        + " `\n  --repo-root ."
        + " `\n  --include-rejected-history"
        + " `\n  --include-peer-blocks\n"
    )


def list_profiles(profile_doc: dict[str, Any]) -> dict[str, Any]:
    profiles = (
        profile_doc.get("profiles")
        if isinstance(profile_doc.get("profiles"), dict)
        else {}
    )
    return {
        "schema_version": 1,
        "kind": "heap_runtime_launcher_profile_list",
        "default_profile": profile_doc.get("default_profile"),
        "profile_control_groups": profile_doc.get("profile_control_groups", {}),
        "profiles": [
            {
                "name": name,
                "description": (
                    value.get("description", "") if isinstance(value, dict) else ""
                ),
                "universe_enabled": (
                    value.get("universe_enabled") if isinstance(value, dict) else None
                ),
                "revision_context_mode": (
                    value.get("revision_context_mode")
                    if isinstance(value, dict)
                    else None
                ),
                "context_document_count": (
                    value.get("context_document_count")
                    if isinstance(value, dict)
                    else None
                ),
                "semantic_code_chunk_limit": (
                    value.get("semantic_code_chunk_limit")
                    if isinstance(value, dict)
                    else None
                ),
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
    parser.add_argument("--revision-context", default="")
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--list-profiles", action="store_true")
    parser.add_argument("--include-block-pointer-command", action="store_true")
    parser.add_argument("--include-revision-context-command", action="store_true")
    parser.add_argument("--include-postrun-package-command", action="store_true")
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
    revision_context_path, revision_context_payload = revision_context_from_profile(
        repo_root, profile, args.revision_context
    )
    command = render_command(
        repo_root,
        project_python,
        profile,
        args.request,
        revision_context_path,
        revision_context_payload,
    )
    block_pointer_command = render_block_pointer_command(
        repo_root, project_python, profile
    )
    revision_context_command = render_revision_context_command(
        repo_root, project_python
    )
    postrun_package_command = render_postrun_package_command(repo_root, project_python)
    candidate_summary = (
        revision_context_payload.get("candidate_applicability_summary")
        if isinstance(
            revision_context_payload.get("candidate_applicability_summary"), dict
        )
        else {}
    )
    report = {
        "schema_version": 6,
        "kind": "heap_runtime_launcher_command",
        "repo_root": repo_root.as_posix(),
        "profiles_file": str(profiles_path),
        "profile_name": profile.get("profile_name"),
        "profile": profile,
        "revision_context_selection_policy": (
            "latest_complete_heap_context_closure_with_composer_json"
            if profile.get("revision_context_mode") == "auto_latest"
            and not args.revision_context
            else ("explicit_revision_context" if args.revision_context else "off")
        ),
        "revision_context_path": (
            str(revision_context_path) if revision_context_path else ""
        ),
        "revision_context_loaded": bool(revision_context_payload),
        "revision_context_task_count": (
            len(revision_context_payload.get("tasks", []))
            if isinstance(revision_context_payload.get("tasks"), list)
            else 0
        ),
        "revision_context_requires_concrete_rewrite": revision_context_payload.get(
            "requires_concrete_rewrite"
        ),
        "revision_context_priority_next_action": revision_context_payload.get(
            "priority_next_action"
        ),
        "revision_context_candidate_applicability_summary": candidate_summary,
        "cli_bound_profile_keys": profile_cli_keys(profile),
        "external_metadata": profile_external_metadata(profile),
        "command": command,
        "block_pointer_command": block_pointer_command,
        "revision_context_command": revision_context_command,
        "postrun_package_command": postrun_package_command,
        "execution_performed": False,
        "notes": [
            "command targets run_heap_runtime_context_closure.py",
            "revision context is injected into --request text, not into the gate",
            "auto_latest revision context ignores smoke fixtures and requires a complete heap run with composer json",
            "postrun_package_command runs the external post-run adapter chain after the heap run",
            "block_pointer_command and revision_context_command remain available for manual step-by-step debugging",
        ],
    }
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(command)
    if args.include_block_pointer_command:
        print("\n# External heap block-pointer manifest command")
        print(block_pointer_command)
    if args.include_revision_context_command:
        print("\n# External heap revision context command")
        print(revision_context_command)
    if args.include_postrun_package_command:
        print("\n# External heap post-run package command")
        print(postrun_package_command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
