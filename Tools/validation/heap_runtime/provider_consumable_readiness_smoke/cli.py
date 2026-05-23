#!/usr/bin/env python3
"""Smoke provider-consumable broker evidence readiness semantics."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.runtime.heap_gate.matrix_lab import RuntimeGateMatrixLabMixin
from ia_carmine.runtime.heap_gate.runtime_common import (
    BASE_REQUIREMENTS,
    PROVIDER_START_REQUIREMENTS,
)
from ia_carmine.runtime.heap_gate.tool_plan_builder import (
    STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT,
)
from Tools.validation._shared.report_utils import write_json_report, write_text_report


class _Heap:
    def __init__(self, pending: list[dict[str, Any]] | None = None) -> None:
        self._pending = pending or []

    def pending_broker_requests(self) -> list[dict[str, Any]]:
        return self._pending


class _Gate(RuntimeGateMatrixLabMixin):
    def __init__(
        self,
        *,
        pending: list[dict[str, Any]] | None = None,
        unattempted: list[dict[str, Any]] | None = None,
    ) -> None:
        self.heap = _Heap(pending)
        self._unattempted = unattempted or []

    def broker_results(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            event.get("payload") or {}
            for event in events
            if event.get("event_type") == "broker_result"
        ]

    def requirement_for_tool(self, tool_name: str) -> str:
        return {
            "run_heap_code_execution_matrix": "code_execution_matrix",
            "agent_runtime_debug_lab": "runtime_debug_lab_execution",
            "runtime_file_refs": "runtime_file_refs",
            "runtime_sqlite_memory": STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT,
        }.get(tool_name, "unknown")

    def next_unattempted_plan_items(self, _events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return list(self._unattempted)


def _event(event_type: str, requirement: str, *, returncode: int = 0) -> dict[str, Any]:
    return {
        "event_type": event_type,
        "correlation_id": f"req:{requirement}",
        "payload": {
            "id": f"req:{requirement}",
            "tool": "run_heap_code_execution_matrix"
            if requirement == "code_execution_matrix"
            else "runtime_sqlite_memory",
            "requirement": requirement,
            "returncode": returncode,
            "outputs": {"json_report": f"output/validation/{requirement}.json"},
            "summary": {"passed": returncode == 0},
        },
    }


def run_smoke(repo_root: Path) -> dict[str, Any]:
    run_loop = _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop.py")
    arbiter = _read(repo_root, "ia_carmine/runtime/heap_gate/arbiter_step.py")
    broker = _read(repo_root, "ia_carmine/runtime/heap_gate/tool_broker.py")
    plan = _read(repo_root, "ia_carmine/runtime/heap_gate/tool_plan_builder.py")
    pending_request = _event("broker_request", "code_execution_matrix")
    pending_gate = _Gate(pending=[pending_request])
    failed_result_gate = _Gate()
    unattempted_gate = _Gate(
        unattempted=[{"requirement": "runtime_debug_lab_execution"}]
    )
    failed_result = _event("broker_result", "code_execution_matrix", returncode=2)
    checks = {
        "startup_batch_in_base_requirements": STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT
        in BASE_REQUIREMENTS,
        "startup_batch_in_provider_start": STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT
        in PROVIDER_START_REQUIREMENTS,
        "pending_provider_consumable_blocks_revision": pending_gate.provider_revision_evidence_ready(
            []
        )
        is False,
        "failed_result_is_consumable_feedback": failed_result_gate.provider_revision_evidence_ready(
            [failed_result]
        )
        is True,
        "unattempted_provider_input_blocks_revision": unattempted_gate.provider_revision_evidence_ready(
            []
        )
        is False,
        "feedback_mentions_broker_evidence": "PROVIDER_CONSUMABLE_BROKER_EVIDENCE"
        in failed_result_gate.provider_consumable_evidence_feedback([failed_result]),
        "run_loop_drains_provider_consumable": "drain_provider_consumable_evidence"
        in run_loop,
        "run_loop_defers_arbiter_on_pending": "pending_broker_request_unresolved_before_arbiter"
        in run_loop,
        "arbiter_treats_pending_as_live_progress": "pending_broker_requests" in arbiter
        and "return" in arbiter,
        "tool_broker_no_per_artifact_memory_flood": "need_operational_memory_index"
        not in broker
        and "broker_result_memory_index" not in broker,
        "tool_plan_has_single_startup_batch": plan.count(
            STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT
        )
        >= 2
        and "startup-memory-index-batch" in plan,
        "baseline_lab_can_be_pre_provider": "pre_provider_baseline" in plan,
    }
    return {
        "schema_version": 1,
        "kind": "provider_consumable_readiness_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": all(checks.values()),
        "checks": checks,
        "errors": [name for name, passed in checks.items() if not passed],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Consumable Readiness Smoke", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    for key, value in (report.get("checks") or {}).items():
        lines.append(f"- {key}: `{value}`")
    return "\n".join(lines) + "\n"


def _read(repo_root: Path, rel_path: str) -> str:
    return (repo_root / rel_path).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/provider_consumable_readiness_smoke.json",
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/provider_consumable_readiness_smoke.md",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke(repo_root)
    write_json_report(report, repo_root / args.output)
    write_text_report(render_markdown(report), repo_root / args.markdown_output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
