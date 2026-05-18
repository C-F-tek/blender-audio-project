"""CLI for heap runtime launcher command generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import (
    DEFAULT_PROFILE_FILE,
    apply_overrides,
    choose_profile,
    profile_cli_keys,
    profile_external_metadata,
    read_json,
    resolve_project_python,
)
from .render import (
    list_profiles,
    render_block_pointer_command,
    render_command,
    render_postrun_package_command,
    render_revision_context_command,
)
from .revision_context import revision_context_from_profile

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
    block_pointer_command = render_block_pointer_command(repo_root, project_python, profile)
    revision_context_command = render_revision_context_command(repo_root, project_python)
    postrun_package_command = render_postrun_package_command(repo_root, project_python)
    candidate_summary = (
        revision_context_payload.get("candidate_applicability_summary")
        if isinstance(revision_context_payload.get("candidate_applicability_summary"), dict)
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
            if profile.get("revision_context_mode") == "auto_latest" and not args.revision_context
            else ("explicit_revision_context" if args.revision_context else "off")
        ),
        "revision_context_path": (str(revision_context_path) if revision_context_path else ""),
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
            "command targets python -m Tools.ai heap_context_closure",
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
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
