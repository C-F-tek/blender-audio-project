#!/usr/bin/env python3
"""Dry-run validation for runtime heap patch-plan events."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from tools.ai.provider_mesh_runtime.python_runtime import command_env, resolve_child_python
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict, safe_list
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.provider_mesh_runtime.python_runtime import (  # type: ignore
        command_env,
        resolve_child_python,
    )
    from tools.ai.provider_runtime_heap import (  # type: ignore
        ProviderRuntimeHeap,
        safe_dict,
        safe_list,
    )


def latest_patch_plan(snapshot: dict[str, Any]) -> dict[str, Any]:
    return safe_dict(safe_dict(snapshot.get("runtime_state")).get("latest_patch_plan"))


def normalize_command(repo_root: Path, argv: list[Any]) -> list[str]:
    command = [str(item) for item in argv if str(item)]
    if command and command[0] == "python":
        command[0] = resolve_child_python(repo_root)
    return command


def run_dry_commands(repo_root: Path, plan: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in safe_list(plan.get("commands")):
        command_item = safe_dict(item)
        command = normalize_command(repo_root, safe_list(command_item.get("argv")))
        if not command:
            results.append({"passed": False, "error": "empty command"})
            continue
        completed = subprocess.run(
            command,
            cwd=repo_root,
            env=command_env(repo_root),
            text=True,
            capture_output=True,
            check=False,
            timeout=120,
        )
        results.append(
            {
                "passed": completed.returncode == 0,
                "returncode": completed.returncode,
                "argv": command,
                "stdout_tail": (completed.stdout or "")[-1000:],
                "stderr_tail": (completed.stderr or "")[-1000:],
            }
        )
    return results


def build_validation_result(repo_root: Path, snapshot: dict[str, Any]) -> dict[str, Any]:
    plan = latest_patch_plan(snapshot)
    if not plan:
        return {
            "schema_version": 1,
            "kind": "runtime_heap_patch_plan_validation",
            "status": "failed",
            "passed": False,
            "errors": ["missing patch_plan event"],
            "command_results": [],
        }
    if not safe_list(plan.get("commands")):
        return {
            "schema_version": 1,
            "kind": "runtime_heap_patch_plan_validation",
            "status": "failed",
            "passed": False,
            "source_plan_action": plan.get("action"),
            "target_lane": plan.get("target_lane"),
            "tool_pointer_inputs": plan.get("tool_pointer_inputs") or {},
            "errors": ["patch_plan contains no dry-run commands"],
            "command_results": [],
            "patch_application_performed": False,
            "source_writes_performed": False,
        }
    command_results = run_dry_commands(repo_root, plan)
    errors = [
        f"command failed: {item.get('argv')}: rc={item.get('returncode')}"
        for item in command_results
        if item.get("passed") is not True
    ]
    return {
        "schema_version": 1,
        "kind": "runtime_heap_patch_plan_validation",
        "status": "ready" if not errors else "failed",
        "passed": not errors,
        "source_plan_action": plan.get("action"),
        "target_lane": plan.get("target_lane"),
        "tool_pointer_inputs": plan.get("tool_pointer_inputs") or {},
        "command_results": command_results,
        "errors": errors,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def write_validation_event(heap: ProviderRuntimeHeap) -> dict[str, Any]:
    snapshot = heap.write_snapshot()
    result = build_validation_result(heap.repo_root, snapshot)
    event = heap.add_event("validation", result, lane="deterministic")
    heap.write_snapshot()
    return {"validation": result, "event": event}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()
    heap = ProviderRuntimeHeap.from_args(
        Path(args.repo_root).resolve(),
        args.stamp,
        args.events,
        args.snapshot,
        args.markdown_output,
    )
    result = write_validation_event(heap)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if safe_dict(result.get("validation")).get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
