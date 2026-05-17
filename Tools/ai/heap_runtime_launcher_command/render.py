"""Command rendering for heap runtime launcher."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import PROFILE_TO_CLI, ps_quote
from .revision_context import revision_context_prompt

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
        "-m Tools.ai run_heap_runtime_context_closure",
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
        + " -m Tools.ai build_external_heap_block_pointer_manifest"
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
        + " -m Tools.ai build_external_heap_revision_context"
        + " `\n  --pointer-manifest $PointerPath"
        + " `\n  --composer-json $ComposerPath"
        + " `\n  --causality-json $CausalityPath"
        + ' `\n  --output (Join-Path $RunDir.FullName "external_heap_revision_context.json")\n'
    )

def render_postrun_package_command(repo_root: Path, project_python: str) -> str:
    return (
        "& "
        + ps_quote(project_python)
        + " -m Tools.ai run_external_heap_postrun_package"
        + " `\n  --repo-root ."
        + " `\n  --include-rejected-history"
        + " `\n  --include-peer-blocks\n"
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
                "description": (value.get("description", "") if isinstance(value, dict) else ""),
                "universe_enabled": (
                    value.get("universe_enabled") if isinstance(value, dict) else None
                ),
                "revision_context_mode": (
                    value.get("revision_context_mode") if isinstance(value, dict) else None
                ),
                "context_document_count": (
                    value.get("context_document_count") if isinstance(value, dict) else None
                ),
                "semantic_code_chunk_limit": (
                    value.get("semantic_code_chunk_limit") if isinstance(value, dict) else None
                ),
            }
            for name, value in sorted(profiles.items())
        ],
    }
