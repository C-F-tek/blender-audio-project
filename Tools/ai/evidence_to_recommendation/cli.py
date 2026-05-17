#!/usr/bin/env python3
"""Convert runtime heap evidence into a deterministic recommendation event."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from tools.ai.heap_event_pointers import source_pointer_bundle
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.heap_event_pointers import source_pointer_bundle  # type: ignore
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict  # type: ignore


def degraded_lanes(snapshot: dict[str, Any]) -> list[str]:
    state = safe_dict(snapshot.get("runtime_state"))
    lanes = state.get("degraded_lanes")
    return [str(item) for item in lanes] if isinstance(lanes, list) else []


def evidence_items(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    state = safe_dict(snapshot.get("runtime_state"))
    count = int(state.get("evidence_count") or 0)
    by_lane = safe_dict(snapshot.get("by_lane"))
    items: list[dict[str, Any]] = []
    for lane, lane_state in by_lane.items():
        if not isinstance(lane_state, dict):
            continue
        event_types = safe_dict(lane_state.get("event_types"))
        evidence_count = int(event_types.get("lane_evidence") or 0) + int(
            event_types.get("evidence_response") or 0
        )
        if evidence_count:
            items.append({"lane": lane, "evidence_count": evidence_count})
    if not items and count:
        items.append({"lane": "orchestrator", "evidence_count": count})
    return items


def build_recommendation(snapshot: dict[str, Any], repo_root: Path | None = None) -> dict[str, Any]:
    lanes = degraded_lanes(snapshot)
    evidence = evidence_items(snapshot)
    source_pointers = source_pointer_bundle(repo_root, snapshot)
    if lanes:
        return {
            "schema_version": 1,
            "kind": "runtime_heap_recommendation",
            "status": "ready",
            "action": "repair_degraded_lane",
            "target_lane": lanes[0],
            "confidence": 0.9,
            "reasons": [f"lane_status_degraded:{lane}" for lane in lanes],
            "evidence": evidence,
            "source_pointers": source_pointers,
            "deterministic_rule": "degraded lane takes priority over optimization",
        }
    if evidence:
        strongest = max(evidence, key=lambda item: int(item.get("evidence_count") or 0))
        return {
            "schema_version": 1,
            "kind": "runtime_heap_recommendation",
            "status": "ready",
            "action": "continue_to_patch_plan",
            "target_lane": str(strongest.get("lane") or "deterministic"),
            "confidence": 0.78,
            "reasons": ["runtime_lane_evidence_present"],
            "evidence": evidence,
            "source_pointers": source_pointers,
            "deterministic_rule": "all lanes healthy with evidence",
        }
    return {
        "schema_version": 1,
        "kind": "runtime_heap_recommendation",
        "status": "degraded",
        "action": "collect_more_evidence",
        "target_lane": "orchestrator",
        "confidence": 0.45,
        "reasons": ["no_runtime_lane_evidence"],
        "evidence": [],
        "source_pointers": source_pointers,
        "deterministic_rule": "no evidence means collect before planning",
    }


def write_recommendation_event(heap: ProviderRuntimeHeap) -> dict[str, Any]:
    snapshot = heap.write_snapshot()
    recommendation = build_recommendation(snapshot, heap.repo_root)
    event = heap.add_event("recommendation", recommendation, lane="deterministic")
    heap.write_snapshot()
    return {"recommendation": recommendation, "event": event}


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
    result = write_recommendation_event(heap)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
