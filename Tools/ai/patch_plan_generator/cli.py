#!/usr/bin/env python3
"""Create a deterministic dry-run patch-plan event from heap recommendations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.ai.provider_runtime_blackboard import ProviderRuntimeHeap, safe_dict
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.provider_runtime_blackboard import ProviderRuntimeHeap, safe_dict  # type: ignore

LANE_FILES = {
    "gpu0": ["Tools/ai/provider_mesh_runtime/gpu0_peer.py"],
    "npu": ["Tools/ai/provider_mesh_runtime/npu_micro.py"],
    "gpu1": ["Tools/ai/gpu_deep_planning_supervised/cli.py"],
    "orchestrator": ["Tools/ai/gpu_npu_parallel_orchestrator/cli.py"],
}
COMMON_FILES = [
    "Tools/ai/provider_runtime_blackboard/cli.py",
    "Tools/ai/gpu_npu_parallel_orchestrator/cli.py",
]


def latest_recommendation(snapshot: dict[str, Any]) -> dict[str, Any]:
    return safe_dict(safe_dict(snapshot.get("runtime_state")).get("latest_recommendation"))


def recommendation_summary(recommendation: dict[str, Any]) -> dict[str, Any]:
    source_pointers = safe_dict(recommendation.get("source_pointers"))
    return {
        "kind": recommendation.get("kind"),
        "status": recommendation.get("status"),
        "action": recommendation.get("action"),
        "target_lane": recommendation.get("target_lane"),
        "confidence": recommendation.get("confidence"),
        "reasons": recommendation.get("reasons") or [],
        "evidence": recommendation.get("evidence") or [],
        "deterministic_rule": recommendation.get("deterministic_rule"),
        "source_pointers": {
            "event_log": source_pointers.get("event_log"),
            "tool_pointer_protocol": source_pointers.get("tool_pointer_protocol"),
            "evidence_pointer_count": len(source_pointers.get("evidence_pointers") or []),
        },
    }


def build_patch_plan(snapshot: dict[str, Any]) -> dict[str, Any]:
    recommendation = latest_recommendation(snapshot)
    action = str(recommendation.get("action") or "collect_more_evidence")
    lane = str(recommendation.get("target_lane") or "orchestrator").lower()
    source_pointers = safe_dict(recommendation.get("source_pointers"))
    target_files = list(dict.fromkeys([*COMMON_FILES, *LANE_FILES.get(lane, [])]))
    if action == "repair_degraded_lane":
        command = [
            "python",
            "-m",
            "py_compile",
            *target_files,
        ]
        plan_action = "dry_run_repair_validation"
    elif action == "continue_to_patch_plan":
        command = ["python", "-m", "py_compile", *COMMON_FILES]
        plan_action = "dry_run_runtime_state_validation"
    else:
        command = ["python", "-m", "Tools.ai", "provider_runtime_blackboard", "--help"]
        plan_action = "dry_run_collect_more_evidence"
    return {
        "schema_version": 1,
        "kind": "runtime_heap_patch_plan",
        "status": "ready",
        "action": plan_action,
        "target_lane": lane,
        "target_files": target_files,
        "commands": [
            {
                "kind": "dry_run_command",
                "cwd": ".",
                "argv": command,
                "reason": "Validate the deterministic runtime heap/provider surface before any source write.",
            }
        ],
        "tool_pointer_inputs": {
            "event_log": source_pointers.get("event_log"),
            "tool_pointer_protocol": source_pointers.get("tool_pointer_protocol"),
            "evidence_pointers": source_pointers.get("evidence_pointers") or [],
        },
        "source_recommendation": recommendation_summary(recommendation),
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def write_patch_plan_event(heap: ProviderRuntimeHeap) -> dict[str, Any]:
    snapshot = heap.write_snapshot()
    plan = build_patch_plan(snapshot)
    event = heap.add_event("patch_plan", plan, lane="deterministic")
    heap.write_snapshot()
    return {"patch_plan": plan, "event": event}


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
    result = write_patch_plan_event(heap)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
