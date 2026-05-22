#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


class FakeGate:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.provider_reports: list[dict[str, Any]] = []
        self.state: dict[str, Any] = {
            "provider_results": [],
            "claims": [],
            "decisions": [],
            "product": {"status": "not_ready"},
        }
        self.events: list[dict[str, Any]] = []
        self.exchange_events: list[dict[str, Any]] = []
        self.provider_leader_packet_path = ""
        self.provider_universe_blocked_reason = ""
        self.errors: list[str] = []
        self.decision_count = 0
        self.stamp = "smoke"
        self.heap = SimpleNamespace(paths=SimpleNamespace(events=repo_root / "events.jsonl"))

    def summarize_provider_report(
        self,
        spec: dict[str, Any],
        completed: subprocess.CompletedProcess[str],
        report_data: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "lane": spec["lane"],
            "role": spec.get("role"),
            "requirement": spec["requirement"],
            "output": str(spec["output"]),
            "returncode": completed.returncode,
            "passed": completed.returncode == 0 and report_data.get("passed") is True,
            "response_text": str(report_data.get("response_text") or ""),
            "semantic_provider_execution_performed": bool(
                report_data.get("semantic_provider_execution_performed")
            ),
            "native_tool_loop_performed": bool(report_data.get("native_tool_loop_performed")),
            "native_tool_call_count": int(report_data.get("native_tool_call_count") or 0),
            "tool_calls": report_data.get("tool_calls") or [],
            "target_files": report_data.get("target_files") or [],
        }

    def enrich_provider_report_with_operational_peer_review(
        self,
        provider_report: dict[str, Any],
        lane: str,
        work_dir: Path,
        revision: int,
        events: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return provider_report

    def provider_block_contract(
        self,
        lane: str,
        revision: int,
        provider_report: dict[str, Any],
    ) -> dict[str, Any]:
        from ia_carmine.runtime.heap_gate.provider_block_contract import provider_block_contract

        return provider_block_contract("smoke", lane, revision, provider_report)

    def publish(
        self,
        source: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        target: str = "",
        correlation_id: str = "",
        round_id: int | None = None,
    ) -> None:
        self.events.append(
            {
                "source": source,
                "event_type": event_type,
                "payload": payload,
                "target": target,
                "correlation_id": correlation_id,
                "round_id": round_id,
            }
        )

    def append_heap_exchange_event(self, payload: dict[str, Any]) -> None:
        self.exchange_events.append(payload)

    def request_text(self) -> str:
        return "smoke request"

    def response_text(self) -> str:
        return ""

    def build_final_response_text(self, events: list[dict[str, Any]]) -> str:
        return ""

    def response_source(self) -> str:
        return ""

    def provider_refs(self) -> list[str]:
        return []

    def provider_response_texts(self) -> list[str]:
        return []

    def provider_role_decisions(self) -> list[str]:
        return []

    def read_events(self) -> list[dict[str, Any]]:
        return list(self.events)


def provider_contract_checks() -> dict[str, bool]:
    from ia_carmine.runtime.heap_gate.provider_block_contract import operational_provider_activity

    gpu1_text, gpu1_text_class = operational_provider_activity(
        "gpu1_planner",
        {
            "selected_model": "qwen3-coder:latest",
            "response_text": "# HEAP_DELTA_PROPOSAL\nTARGET_FILES\nEXIT_DECISION=PATCHABLE_TARGET",
        },
    )
    gpu1_tool, gpu1_tool_class = operational_provider_activity(
        "gpu1_planner",
        {
            "selected_model": "qwen3-coder:latest",
            "native_tool_call_count": 1,
            "tool_calls": [{"tool": "run_heap_code_execution_matrix", "reason": "structured"}],
        },
    )
    gpu0_device_only, gpu0_device_class = operational_provider_activity(
        "gpu0_peer",
        {
            "semantic_provider_execution_performed": True,
            "response_text": "GPU.0 workload device available_devices",
        },
    )
    npu_timeout, npu_timeout_class = operational_provider_activity(
        "npu_micro_task_auditor",
        {
            "semantic_provider_execution_performed": True,
            "semantic_provider_classification": "openvino_native_tool_loop_timeout",
            "response_text": "audit evidence target validation",
        },
    )
    return {
        "gpu1_heap_delta_text_operational": gpu1_text
        and gpu1_text_class == "gpu1_heap_delta_proposal_present",
        "gpu1_native_tool_call_operational": gpu1_tool
        and gpu1_tool_class == "gpu1_structured_native_tool_call_present",
        "gpu0_device_only_not_operational": (not gpu0_device_only)
        and gpu0_device_class == "gpu0_peer_no_review_audit_or_native_tool_call",
        "npu_timeout_not_operational": (not npu_timeout)
        and npu_timeout_class.startswith("non_operational_classification:"),
    }


def provider_absorption_checks(repo: Path) -> dict[str, bool]:
    from ia_carmine.runtime.heap_gate.provider_report_absorption import absorb_completed_provider_item

    work_dir = repo / "output" / "validation" / "observable_peer_activity_absorption_smoke"
    work_dir.mkdir(parents=True, exist_ok=True)
    output = work_dir / "gpu0_peer.json"
    output.write_text(
        "{\n"
        '  "passed": true,\n'
        '  "semantic_provider_execution_performed": true,\n'
        '  "response_text": "GPU.0 workload device available_devices",\n'
        '  "native_tool_call_count": 0,\n'
        '  "tool_calls": []\n'
        "}\n",
        encoding="utf-8",
    )
    gate = FakeGate(repo)
    item: dict[str, Any] = {
        "spec": {
            "lane": "gpu0_peer",
            "requirement": "gpu0_provider_peer",
            "role": "gpu0_peer_reviewer_refiner",
            "output": output,
        },
        "lane": "gpu0_peer",
        "requirement": "gpu0_provider_peer",
        "correlation": "smoke:gpu0",
        "command": [],
        "completed": subprocess.CompletedProcess([], 0, "", ""),
        "started_at": "",
        "completed_at": "",
        "elapsed_seconds": 0.1,
        "pid": None,
    }
    absorbed = absorb_completed_provider_item(
        gate,
        item,
        launch_manifest=work_dir / "provider_launch_manifest.json",
        work_dir=work_dir,
        round_id=1,
        revision=0,
        timeout_seconds=60,
    )
    report = gate.provider_reports[0] if gate.provider_reports else {}
    event_types = [event.get("event_type") for event in gate.events]
    return {
        "diagnostic_report_absorbed": absorbed,
        "diagnostic_report_passed_kept": report.get("passed") is True
        and report.get("report_passed") is True,
        "diagnostic_only_true": report.get("diagnostic_only") is True,
        "diagnostic_not_operational": report.get("operational_provider_activity") is False,
        "diagnostic_status_ready": report.get("status") == "ready",
        "diagnostic_provider_evidence_published": "provider_evidence" in event_types,
        "diagnostic_peer_block_not_published": "provider_peer_block" not in event_types,
        "diagnostic_product_not_blocked": gate.state["product"].get("status") == "not_ready",
    }


def provider_requirement_checks() -> dict[str, bool]:
    from ia_carmine.runtime.heap_gate.matrix_lab import RuntimeGateMatrixLabMixin

    class FakeRequirements(RuntimeGateMatrixLabMixin):
        def __init__(self, allow_provider_generation: bool) -> None:
            self.args = SimpleNamespace(allow_provider_generation=allow_provider_generation)

        def virtual_dev_environment_required(self) -> bool:
            return False

        def code_execution_matrix_required(self) -> bool:
            return False

        def runtime_debug_lab_required(self) -> bool:
            return False

    required = FakeRequirements(True).required_requirements_order()
    no_provider = FakeRequirements(False).required_requirements_order()
    return {
        "gpu1_primary_is_hard_provider_requirement": "gpu1_provider_planner" in required,
        "gpu0_peer_is_hard_provider_requirement": "gpu0_provider_peer" in required,
        "npu_peer_is_hard_provider_requirement": "npu_micro_task_auditor" in required,
        "provider_requirements_absent_when_generation_disabled": not any(
            item.endswith("_provider_peer")
            or item in {"gpu1_provider_planner", "npu_micro_task_auditor"}
            for item in no_provider
        ),
    }


def provider_stall_checks() -> dict[str, bool]:
    from ia_carmine.runtime.heap_gate.provider_universe_abort import (
        block_provider_universe_run,
        provider_universe_abort_reason,
    )
    from ia_carmine.runtime.heap_gate.provider_process_collection import _provider_lane_start_abort_reason

    start_failed = [{"lane": "gpu1_planner", "prepare_error": "missing provider"}]
    diagnostic_ready = [
        {
            "lane": "gpu0_peer",
            "completed": subprocess.CompletedProcess([], 0, "", ""),
            "started_at": "2026-05-20T00:00:00",
            "provider_report": {
                "status": "ready",
                "diagnostic_only": True,
                "operational_provider_activity": False,
            },
        }
    ]
    failed_lane = [
        {
            "lane": "npu_micro_task_auditor",
            "completed": subprocess.CompletedProcess([], 1, "", ""),
            "started_at": "2026-05-20T00:00:00",
            "provider_report": {"status": "failed"},
        }
    ]
    abort_gate = FakeGate(Path.cwd())
    reason = provider_universe_abort_reason(failed_lane)
    block_provider_universe_run(abort_gate, reason, 1, 0)
    return {
        "provider_lane_start_failure_is_hard_block": _provider_lane_start_abort_reason(
            start_failed
        ).startswith("provider_universe_lane_not_started:gpu1_planner:"),
        "diagnostic_ready_peer_does_not_abort_universe": (
            provider_universe_abort_reason(diagnostic_ready) == ""
        ),
        "failed_lane_blocks_universe": (
            reason == "provider_universe_lane_not_active:npu_micro_task_auditor:failed"
        ),
        "inactive_provider_universe_blocks_run": (
            abort_gate.state["product"].get("status") == "blocked_with_reason"
            and abort_gate.provider_universe_blocked_reason == reason
            and bool(abort_gate.state["decisions"])
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/observable_peer_activity_contract_smoke.json"
    )
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    gpu0 = repo / "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py"
    npu = repo / "ia_carmine/providers/provider_mesh/npu_micro_task_companion_report/cli.py"
    npu_shared = repo / "ia_carmine/_shared/npu_micro_task_companion_cli.py"
    gpu0_text = read_text(gpu0)
    npu_text = read_text(npu) + "\n" + read_text(npu_shared)

    checks: dict[str, bool] = {
        "gpu0_default_iterations_observable": "run_ollama_probe" in gpu0_text,
        "gpu0_default_min_seconds_observable": "--max-new-tokens" in gpu0_text,
        "gpu0_requires_observable_workload": "ollama_gpu0_vulkan_required"
        in gpu0_text,
        "gpu0_fails_non_observable_when_required": "--require-ollama-gpu-residency"
        in gpu0_text
        and "provider_work_verified" in gpu0_text,
        "npu_declares_activity_requested": "npu_peer_activity_requested" in npu_text,
        "npu_declares_activity_performed": "npu_peer_activity_performed" in npu_text,
        "npu_declares_device_execution": "npu_device_execution_performed" in npu_text,
        "npu_declares_peer_micro_audit_mode": '"mode": "peer_micro_audit"' in npu_text,
    }
    checks.update(provider_contract_checks())
    checks.update(provider_absorption_checks(repo))
    checks.update(provider_requirement_checks())
    checks.update(provider_stall_checks())
    errors = [
        f"observable peer activity contract missing: {name}"
        for name, ok in checks.items()
        if not ok
    ]
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "observable_peer_activity_contract_smoke",
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(repo, args.output)), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
