#!/usr/bin/env python3
"""Smoke-test external heap launcher command generation.

This smoke does not run providers and does not execute the heap runtime. It only
checks that profile-driven command generation exposes the expected external heap
operator commands and injects an explicitly supplied revision context into the
reviewable launcher request.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def env_for(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    return env


def run(command: list[str], repo_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=env_for(repo_root),
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def load_heap_closure_module(repo_root: Path) -> Any:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from Tools.ai.heap_context_closure import requesting

    return requesting


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Runtime Launcher Command Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Revision context fixture path: `{report.get('revision_context_fixture_path')}`",
        f"- Output artifact writes performed: `{report.get('output_artifact_writes_performed')}`",
        "",
        "## Checks",
        "",
    ]
    for check in report.get("checks") or []:
        lines.append(f"- `{check.get('name')}`: `{check.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors") or [])
    return "\n".join(lines) + "\n"


def write_revision_context_fixture(repo_root: Path) -> Path:
    run_dir = repo_root / "output" / "validation" / "heap_context_closure_smoke_revision_context"
    run_dir.mkdir(parents=True, exist_ok=True)
    fixture = run_dir / "external_heap_revision_context.json"
    fixture.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "external_heap_revision_context",
                "protocol": "external_heap_revision_context_v1",
                "product_acceptance_status": "blocked",
                "product_acceptance_passed": False,
                "requires_concrete_rewrite": True,
                "priority_next_action": "rewrite_non_concrete_candidates",
                "candidate_applicability_summary": {
                    "rewrite_task_count": 1,
                    "non_concrete_candidate_task_count": 1,
                    "concrete_candidate_task_count": 0,
                    "symbol_propagation_skipped_task_count": 1,
                    "flag_counts": {"generic_patch_sketch": 1},
                    "non_concrete_task_ids": ["gpu1_rewrite_rejected_proposal_smoke"],
                    "symbol_propagation_skipped_task_ids": ["gpu1_rewrite_rejected_proposal_smoke"],
                    "requires_concrete_rewrite": True,
                    "priority_next_action": "rewrite_non_concrete_candidates",
                },
                "resume_from_block_id": "proposal_smoke_previous",
                "latest_block_id": "proposal_smoke_latest",
                "tasks": [
                    {
                        "task_id": "gpu1_rewrite_rejected_proposal_smoke",
                        "role": "gpu1_planner",
                        "task_type": "rewrite_rejected_block",
                        "target_block_id": "proposal_smoke_latest",
                        "resume_from_block_id": "proposal_smoke_previous",
                        "candidate_applicability_flags": ["generic_patch_sketch"],
                        "candidate_concrete_enough": False,
                        "symbol_propagation_skipped": True,
                        "symbol_propagation_skip_reason": "candidate_not_concrete_enough",
                        "instruction": "Smoke fixture task.",
                    }
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return fixture


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_runtime_launcher_command_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_runtime_launcher_command_smoke.md"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    fixture_path = write_revision_context_fixture(repo_root)
    output_json = repo_root / "output" / "validation" / "heap_launcher_command_smoke.json"
    command = [
        sys.executable,
        "-m",
        "Tools.ai",
        "heap_runtime_launcher_command",
        "--repo-root",
        ".",
        "--profile",
        "balanced_external_heap",
        "--revision-context",
        str(fixture_path),
        "--include-postrun-package-command",
        "--output",
        str(output_json),
    ]
    result = run(command, repo_root)
    payload = read_json(output_json)
    generated_command = str(payload.get("command") or "")
    revision_fixture_payload = read_json(fixture_path)
    closure_module = load_heap_closure_module(repo_root)
    native_revision_prompt = closure_module.revision_context_prompt(
        revision_fixture_payload, fixture_path, 12
    )
    checks = [
        {"name": "command_builder_returncode_zero", "passed": result.get("passed") is True},
        {"name": "schema_version_6", "passed": payload.get("schema_version") == 6},
        {
            "name": "profile_balanced",
            "passed": payload.get("profile_name") == "balanced_external_heap",
        },
        {
            "name": "postrun_package_command_present",
            "passed": bool(payload.get("postrun_package_command")),
        },
        {
            "name": "revision_context_loaded",
            "passed": payload.get("revision_context_loaded") is True,
        },
        {
            "name": "revision_context_selection_explicit",
            "passed": payload.get("revision_context_selection_policy")
            == "explicit_revision_context",
        },
        {
            "name": "revision_context_injected_into_request",
            "passed": "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN" in generated_command,
        },
        {
            "name": "rewrite_priority_exposed_in_report",
            "passed": payload.get("revision_context_requires_concrete_rewrite") is True
            and payload.get("revision_context_priority_next_action")
            == "rewrite_non_concrete_candidates",
        },
        {
            "name": "rewrite_priority_injected_into_request",
            "passed": "requires_concrete_rewrite: True" in generated_command
            and "rewrite_non_concrete_candidates" in generated_command,
        },
        {
            "name": "symbol_propagation_skip_injected_into_request",
            "passed": "symbol_propagation_skipped=True" in generated_command
            and "candidate_not_concrete_enough" in generated_command,
        },
        {
            "name": "native_closure_revision_prompt_exposes_rewrite_priority",
            "passed": "requires_concrete_rewrite: True" in native_revision_prompt
            and "rewrite_non_concrete_candidates" in native_revision_prompt,
        },
        {
            "name": "native_closure_revision_prompt_preserves_symbol_skip",
            "passed": "symbol_propagation_skipped=True" in native_revision_prompt
            and "candidate_not_concrete_enough" in native_revision_prompt,
        },
        {
            "name": "main_command_targets_heap_closure",
            "passed": "-m Tools.ai heap_context_closure" in generated_command,
        },
        {
            "name": "postrun_command_targets_orchestrator",
            "passed": "-m Tools.ai external_heap_postrun_package"
            in str(payload.get("postrun_package_command") or ""),
        },
    ]
    errors = [check["name"] for check in checks if not check.get("passed")]
    report = {
        "schema_version": 2,
        "kind": "heap_runtime_launcher_command_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "output_artifact_writes_performed": True,
        "revision_context_fixture_used": True,
        "revision_context_fixture_path": str(fixture_path),
        "generated_command_json": str(output_json),
        "native_revision_prompt_preview": native_revision_prompt[-4000:],
        "checks": checks,
        "command_result": result,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(repo_root, args.output)), end="")
    write_text_report(render_markdown(report), resolve_output_path(repo_root, args.markdown_output))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
