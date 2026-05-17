#!/usr/bin/env python3
"""Generate a provider-runtime heap GPU peer-exchange smoke event stream.

This script is source-only and report-only. It does not run providers, broker
tools, Blender, FFmpeg, Git writes or patch application.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap  # type: ignore


def append_gpu_peer_smoke(heap: ProviderRuntimeHeap, *, round_id: int) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    correlation_id = "gpu-peer-evidence-001"
    events.append(
        heap.append_event(
            source="gpu1",
            target="gpu0",
            event_type="evidence_request",
            round_id=round_id,
            correlation_id=correlation_id,
            payload={
                "objective": "GPU1 planner asks GPU0 coworker for OpenVINO-side code/tool evidence.",
                "requested_evidence": [
                    "runtime tool context",
                    "patch readiness",
                    "failed report triage",
                ],
                "direct_execution": False,
                "broker_required": True,
            },
        )
    )
    events.append(
        heap.append_event(
            source="gpu0",
            target="gpu1",
            event_type="evidence_response",
            round_id=round_id,
            correlation_id=correlation_id,
            payload={
                "summary": "GPU0 coworker responds with broker-mediated evidence requirements.",
                "recommended_broker_requests": [
                    {
                        "tool": "build_code_interpreter_report",
                        "args": {"input": "tools/ai,tools/validation,tools/workflow,tools/npu"},
                    },
                    {
                        "tool": "check_validation_report_contract",
                        "args": {"report_file": "output/validation/*.json"},
                    },
                ],
                "direct_execution": False,
                "broker_required": True,
            },
        )
    )
    return events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--round", type=int, default=1)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(
        repo_root, args.stamp, args.events, args.snapshot, args.markdown_output
    )
    events = append_gpu_peer_smoke(heap, round_id=args.round)
    snapshot = heap.write_snapshot()
    result = {
        "schema_version": 1,
        "kind": "provider_runtime_heap_gpu_peer_exchange_smoke",
        "stamp": args.stamp,
        "passed": True,
        "event_count": len(events),
        "events": events,
        "heap_snapshot": {
            "event_count": snapshot.get("event_count"),
            "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
            "event_log": snapshot.get("event_log"),
        },
        "guardrails": {
            "provider_execution_performed": False,
            "direct_tool_execution_allowed": False,
            "broker_required_for_tool_execution": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
