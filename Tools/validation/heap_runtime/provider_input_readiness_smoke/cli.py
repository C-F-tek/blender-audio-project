#!/usr/bin/env python3
"""Smoke-test pre-provider input readiness gates."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.runtime.heap_gate.runtime_common import BASE_REQUIREMENTS
from ia_carmine.runtime.heap_gate.tool_broker import RuntimeGateToolBrokerMixin
from ia_carmine.runtime.heap_gate.tool_plan_builder import (
    STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT,
)
from Tools.validation._shared.report_utils import write_json_report, write_text_report


class _Args:
    allow_provider_generation = True
    objective = "Implement runtime/provider readiness without provider diff."
    request_file = ""
    max_context_files = 8
    max_chars_per_file = 1200
    context_document_count = 8
    context_document_preview_chars = 1200
    semantic_code_chunk_limit = 4
    semantic_code_chunk_preview_chars = 1200
    semantic_evidence_chunk_limit = 8
    memory_search_limit = 4
    tool_inventory_roots = "Tools,ia_carmine"
    semantic_path_boosts = "ia_carmine/runtime/heap_gate,ia_carmine/runtime/run"
    code_interpreter_inputs = "ia_carmine,Tools"
    duplication_audit_roots = "ia_carmine,Tools"
    ai_context_pack_profile = "core_ai_backend"
    timeout_seconds = 120


class _Heap:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def append_event(
        self,
        *,
        source: str,
        target: str | None,
        event_type: str,
        correlation_id: str | None,
        round_id: int | None,
        payload: dict[str, Any],
    ) -> None:
        self.events.append(
            {
                "source": source,
                "target": target,
                "event_type": event_type,
                "correlation_id": correlation_id,
                "round_id": round_id,
                "payload": payload,
            }
        )

    def read_events(self) -> list[dict[str, Any]]:
        return list(self.events)


class _Owner(RuntimeGateToolBrokerMixin):
    def __init__(self, repo_root: Path) -> None:
        self.args = _Args()
        self.repo_root = repo_root
        self.stamp = "provider-input-smoke"
        self.heap = _Heap()
        self.heap_read_count = 0
        self.heap_write_count = 0
        self.tool_request_count = 0
        self.tool_execution_count = 0
        self.max_iterations = 4
        self.provider_reports: list[dict[str, Any]] = []
        self.state: dict[str, Any] = {
            "shared_evidence": [],
            "needs": [],
            "tool_requests": [],
        }

    def runtime_context_dir(self) -> Path:
        path = self.repo_root / "output" / "validation" / "provider_input_readiness_smoke"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def request_text(self) -> str:
        return "Implement provider input readiness for runtime and debug requests."

    def real_source_file_candidates(self, limit: int = 32) -> list[str]:
        return ["ia_carmine/runtime/heap_gate/tool_broker.py"][:limit]

    def startup_manifest_from_task_file(self) -> tuple[Path | None, dict[str, Any]]:
        return None, {}

    def implementation_output_required(self) -> bool:
        return True

    def historical_tool_context_files(self) -> list[str]:
        return []

    def virtual_dev_environment_plan_items(
        self, _context_dir: Path, _request: str
    ) -> list[dict[str, Any]]:
        return [
            {
                "stage": 4,
                "requirement": "virtual_dev_environment",
                "id": "baseline-virtual-dev",
                "tool": "run_heap_virtual_dev_environment",
                "args": {},
                "reason": "baseline virtual development environment evidence",
            }
        ]

    def runtime_debug_lab_plan_items(
        self, _context_dir: Path, _request: str
    ) -> list[dict[str, Any]]:
        return [
            {
                "stage": 4,
                "requirement": "runtime_debug_lab_execution",
                "id": "baseline-runtime-debug-lab",
                "tool": "agent_runtime_debug_lab",
                "args": {},
                "reason": "baseline runtime debug lab evidence",
            }
        ]

    def code_execution_matrix_plan_items(
        self, _context_dir: Path, _request: str
    ) -> list[dict[str, Any]]:
        return [
            {
                "stage": 4,
                "requirement": "code_execution_matrix",
                "id": "post-provider-code-matrix",
                "tool": "run_heap_code_execution_matrix",
                "args": {},
                "reason": "post-provider product validation",
            }
        ]

    def required_requirements_order(self) -> list[str]:
        return list(BASE_REQUIREMENTS)

    def provider_refs(self) -> list[str]:
        return []

    def proposal_iteration_artifacts(self) -> list[str]:
        return []


def _broker_event(requirement: str, tool: str | None = None) -> dict[str, Any]:
    tool_name = tool or requirement
    return {
        "event_type": "broker_result",
        "payload": {
            "tool": tool_name,
            "requirement": requirement,
            "returncode": 0,
            "outputs": {
                "json_report": f"output/validation/{requirement}.json",
                "markdown_report": f"output/validation/{requirement}.md",
            },
            "summary": {"passed": True, "requirement": requirement},
        },
    }


def _events_for(requirements: list[str]) -> list[dict[str, Any]]:
    return [
        _broker_event(
            requirement,
            "runtime_file_refs" if requirement == "runtime_file_refs" else requirement,
        )
        for requirement in requirements
    ]


def run_smoke(repo_root: Path) -> dict[str, Any]:
    owner = _Owner(repo_root)
    pre_provider_plan = owner.tool_plan()
    batch_requirement = STARTUP_MEMORY_INDEX_BATCH_REQUIREMENT
    batch_items = [
        item
        for item in pre_provider_plan
        if item.get("requirement") == batch_requirement
    ]
    runtime_refs = [
        item for item in pre_provider_plan if item.get("requirement") == "runtime_file_refs"
    ]
    baseline_requirements = {
        item.get("requirement")
        for item in pre_provider_plan
        if item.get("pre_provider_baseline")
    }
    pre_provider_post_validation_requirements = {
        item.get("requirement")
        for item in pre_provider_plan
        if item.get("requirement")
        in {"virtual_dev_environment", "runtime_debug_lab_execution", "code_execution_matrix"}
    }
    code_matrix_before_provider = [
        item for item in pre_provider_plan if item.get("requirement") == "code_execution_matrix"
    ]

    base_events = _events_for(
        [item for item in BASE_REQUIREMENTS if item != batch_requirement]
    )
    owner.publish_shared_evidence_facts(1, base_events)
    per_artifact_memory_requests = [
        request
        for request in owner.state["tool_requests"]
        if str(request.get("id") or "").startswith(f"{owner.stamp}:sqlite-index:")
    ]
    first_after_base = owner.next_unattempted_plan_items(base_events)

    batch_item = first_after_base[0] if first_after_base else {}
    batch_content = str((batch_item.get("args") or {}).get("content") or "{}")
    try:
        batch_payload = json.loads(batch_content)
    except json.JSONDecodeError:
        batch_payload = {}

    batch_events = [
        *base_events,
        _broker_event(
        batch_requirement,
        "runtime_sqlite_memory",
        ),
    ]
    owner.publish_shared_evidence_facts(2, batch_events)

    owner.provider_reports = [{"lane": "gpu1_planner"}]
    post_provider_plan = owner.tool_plan()
    code_matrix_after_provider = [
        item for item in post_provider_plan if item.get("requirement") == "code_execution_matrix"
    ]
    post_provider_feedback = [
        item
        for item in post_provider_plan
        if item.get("requirement") in {"virtual_dev_environment", "runtime_debug_lab_execution"}
    ]
    source_text = "\n".join(
        [
            (repo_root / "ia_carmine/runtime/heap_gate/tool_broker.py").read_text(
                encoding="utf-8", errors="replace"
            ),
            (repo_root / "ia_carmine/runtime/heap_gate/loop_steps.py").read_text(
                encoding="utf-8", errors="replace"
            ),
        ]
    )

    checks = {
        "single_batch_plan_item": len(batch_items) == 1
        and batch_items[0].get("tool") == "runtime_sqlite_memory",
        "runtime_file_refs_hard_gate": bool(runtime_refs)
        and runtime_refs[0].get("pre_provider_hard_gate") is True,
        "no_baseline_tools_pre_provider": baseline_requirements == set()
        and pre_provider_post_validation_requirements == set(),
        "code_matrix_not_pre_provider": not code_matrix_before_provider,
        "no_per_artifact_sqlite_requests": not per_artifact_memory_requests,
        "startup_batch_runs_after_base": {
            item.get("requirement") for item in first_after_base
        } == {batch_requirement},
        "batch_indexes_runtime_refs": {
            item.get("requirement") for item in batch_payload.get("artifact_refs", [])
        }.issuperset({"runtime_file_refs"}),
        "provider_gate_waits_for_batch": not owner.provider_start_requirements_complete(
            base_events
        ),
        "provider_gate_ready_after_batch": owner.provider_start_requirements_complete(
            batch_events
        ),
        "virtual_debug_post_provider_feedback": {
            item.get("requirement") for item in post_provider_feedback
        }
        == {"virtual_dev_environment", "runtime_debug_lab_execution"}
        and all(item.get("post_provider") for item in post_provider_feedback)
        and all(item.get("provider_feedback_evidence") for item in post_provider_feedback),
        "code_matrix_post_provider_final_validation": bool(code_matrix_after_provider)
        and code_matrix_after_provider[0].get("post_provider") is True
        and code_matrix_after_provider[0].get("final_product_validation") is True,
        "single_provider_start_requirements_complete_method": source_text.count(
            "def provider_start_requirements_complete"
        )
        == 1,
    }
    return {
        "schema_version": 1,
        "kind": "provider_input_readiness_smoke",
        "repo_root": repo_root.as_posix(),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": all(checks.values()),
        "checks": checks,
        "batch_payload": batch_payload,
        "errors": [name for name, passed in checks.items() if not passed],
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Input Readiness Smoke", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    for key, value in (report.get("checks") or {}).items():
        lines.append(f"- {key}: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/provider_input_readiness_smoke.json",
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/provider_input_readiness_smoke.md",
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
