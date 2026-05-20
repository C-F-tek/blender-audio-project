#!/usr/bin/env python3
"""Provider invocation contract for heap-driven IA-Carmine runtime loops.

This validator describes the provider invocation contract used by the real runtime owner.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.heap_provider.budget_governor import (
        build_heap_provider_budget_governor,
        config_from_namespace,
    )
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.heap_provider.budget_governor import (  # type: ignore
        build_heap_provider_budget_governor,
        config_from_namespace,
    )
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

PRIMARY_PROVIDER_LANE = "gpu1_planner"
AUDITOR_LANE = "npu_micro_task_auditor"
DIAGNOSTIC_LANE = "gpu0_peer"
EXPECTED_WORKLOAD_REPORTS = (
    "provider_lane",
    "model_name",
    "heap_event_refs",
    "tool_request_refs",
    "tool_execution_telemetry",
    "recommendations_or_blockers",
    "product_status_signal",
)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def requirement(name: str, passed: bool, reason: str) -> dict[str, Any]:
    return {"requirement": name, "passed": bool(passed), "reason": reason}


def build_workload_report_contract(governor: dict[str, Any]) -> dict[str, Any]:
    permit = safe_dict(governor.get("permit"))
    contract = {
        "kind": "heap_provider_workload_report_contract",
        "passed": True,
        "provider_lane": PRIMARY_PROVIDER_LANE,
        "permit_required": True,
        "permit_decision": permit.get("decision"),
        "permit_allowed": permit.get("permit_allowed"),
        "reports_required_after_real_run": list(EXPECTED_WORKLOAD_REPORTS),
        "minimum_content_requirements": [
            "heap stamp",
            "provider lane",
            "model name if provider is used",
            "input evidence references",
            "brokered tool usage telemetry",
            "recommendations or explicit blockers",
            "no patch applied flag",
            "product_status ready or blocked_with_reason",
        ],
        "failure_policy": {
            "missing_report": "block_product_ready",
            "unusable_report": "block_primary_advisory",
            "patch_application_detected": "hard_fail",
            "missing_heap_refs": "hard_fail",
        },
    }
    return contract


def build_expected_telemetry_contract(governor: dict[str, Any]) -> dict[str, Any]:
    loop_budget = safe_dict(governor.get("loop_budget"))
    contract = {
        "kind": "heap_provider_expected_telemetry_contract",
        "passed": True,
        "provider_lane": PRIMARY_PROVIDER_LANE,
        "budget": loop_budget,
        "events_required": [
            "task_state",
            "fact",
            "need",
            "broker_request",
            "broker_result",
            "claim",
            "validation_signal",
            "decision",
            "candidate_operation",
            "product_signal",
        ],
        "fields_required": [
            "timestamp",
            "provider_lane",
            "permit_decision",
            "generation_enabled",
            "duration_ms",
            "exit_code",
            "heap_event_refs",
            "output_paths",
        ],
        "forbidden_runtime_effects": [
            "provider_patch_apply",
            "blender_runtime",
            "ffmpeg_runtime",
        ],
    }
    return contract


def build_npu_audit_hooks(governor: dict[str, Any]) -> dict[str, Any]:
    npu_lane = safe_dict(safe_dict(governor.get("provider_lanes")).get(AUDITOR_LANE))
    hooks = {
        "kind": "heap_provider_npu_audit_hooks",
        "passed": True,
        "auditor_lane": AUDITOR_LANE,
        "diagnostic_lane": DIAGNOSTIC_LANE,
        "before_provider": [
            "verify permit decision",
            "verify heap has current task_state",
            "verify broker allowlist is the only tool execution path",
        ],
        "after_provider": [
            "compare recommendations to heap evidence",
            "verify no patch apply occurred",
            "verify GPU.0 did not become primary implicitly",
            "verify telemetry completeness",
            "verify product_signal was produced",
        ],
        "sample_count": npu_lane.get("max_samples", 3),
        "promotion_allowed": False,
        "model_load_required_for_contract": bool(npu_lane.get("model_load_required", False)),
    }
    return hooks


def apply_runtime_gate_status(sections: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    status = "ready_for_provider_runtime" if gate.get("passed") else "blocked_by_runtime_gate"
    reasons = list(gate.get("blocking_reasons") or [])
    for section in sections:
        section["status"] = status
        section["passed"] = bool(gate.get("passed"))
        if reasons:
            section["blocking_reasons"] = reasons


def build_real_run_gate(
    governor: dict[str, Any],
    workload_contract: dict[str, Any],
    telemetry_contract: dict[str, Any],
    npu_hooks: dict[str, Any],
    *,
    allow_provider_generation: bool,
    operator_intent: bool,
) -> dict[str, Any]:
    permit = safe_dict(governor.get("permit"))
    permit_allowed = bool(permit.get("permit_allowed"))
    requirements = [
        requirement(
            "operator_intent",
            bool(operator_intent),
            "explicit operator intent required for provider runtime",
        ),
        requirement(
            "allow_provider_generation",
            allow_provider_generation,
            "provider runtime selection is mandatory",
        ),
        requirement(
            "permit_allowed",
            permit_allowed,
            "provider run permit must allow generation",
        ),
        requirement(
            "workload_contract_ready",
            bool(workload_contract.get("passed")),
            "workload report contract must pass",
        ),
        requirement(
            "telemetry_contract_ready",
            bool(telemetry_contract.get("passed")),
            "telemetry contract must pass",
        ),
        requirement(
            "npu_audit_hooks_ready",
            bool(npu_hooks.get("passed")),
            "NPU audit hooks must pass",
        ),
        requirement(
            "heap_product_signal_required",
            True,
            "ready/blocked product signal is mandatory",
        ),
    ]
    allowed = all(item["passed"] for item in requirements)
    blocking_reasons = [str(item.get("requirement")) for item in requirements if not item["passed"]]
    gate = {
        "kind": "heap_provider_real_run_gate",
        "passed": bool(allowed),
        "real_run_allowed": bool(permit_allowed and allow_provider_generation),
        "real_run_requested": bool(allow_provider_generation),
        "requirements": requirements,
        "decision": "allow_provider_runtime_start" if allowed else "block_provider_runtime_start",
        "deny_is_failure_for_contract_only": False,
        "deny_requires_blocked_product_when_provider_selected": True,
        "product_status_if_selected": "ready_to_run" if allowed else "blocked_with_reason",
    }
    failed_requirements = [item for item in requirements if not item["passed"]]
    if failed_requirements:
        gate["failed_requirements"] = failed_requirements
    if blocking_reasons:
        gate["blocking_reasons"] = blocking_reasons
    return gate


def build_lane_activation_contract(
    governor: dict[str, Any],
    gate: dict[str, Any],
    workload_contract: dict[str, Any],
    telemetry_contract: dict[str, Any],
    npu_hooks: dict[str, Any],
) -> dict[str, Any]:
    blocking_reasons = list(gate.get("blocking_reasons") or [])
    activation_contract = {
        "kind": "heap_provider_required_lane_activation_plan",
        "passed": bool(gate.get("passed")),
        "real_run_gate_decision": gate.get("decision"),
        "execution_owner": "Tools.ai.heap_gate.provider_execution.run_provider_teamwork",
        "command_spec_source": "Tools/ai/heap_gate/provider_command_specs.py",
        "provider_selected_runtime_must_start_all_lanes": True,
        "start_failure_policy": "abort_universe",
        "active_lane_time_policy": "counter_not_hard_lane_timeout",
        "required_lanes": [
            {
                "provider_lane": PRIMARY_PROVIDER_LANE,
                "role": "primary_planner",
                "must_start_when_provider_selected": True,
                "budget": telemetry_contract.get("budget"),
                "expected_outputs": workload_contract.get("reports_required_after_real_run", []),
            },
            {
                "provider_lane": AUDITOR_LANE,
                "role": "micro_task_auditor",
                "must_start_when_provider_selected": True,
                "audit_hooks": npu_hooks.get("after_provider", []),
            },
            {
                "provider_lane": DIAGNOSTIC_LANE,
                "role": "peer_reviewer_refiner",
                "must_start_when_provider_selected": True,
            },
        ],
    }
    if blocking_reasons:
        activation_contract["blocking_reasons"] = blocking_reasons
    return activation_contract


def build_heap_provider_invocation_contract(
    governor: dict[str, Any],
    *,
    allow_provider_generation: bool = False,
    operator_intent: bool = False,
) -> dict[str, Any]:
    workload_contract = build_workload_report_contract(governor)
    telemetry_contract = build_expected_telemetry_contract(governor)
    npu_hooks = build_npu_audit_hooks(governor)
    gate = build_real_run_gate(
        governor,
        workload_contract,
        telemetry_contract,
        npu_hooks,
        allow_provider_generation=allow_provider_generation,
        operator_intent=operator_intent,
    )
    lane_activation_contract = build_lane_activation_contract(
        governor, gate, workload_contract, telemetry_contract, npu_hooks
    )
    apply_runtime_gate_status(
        [workload_contract, telemetry_contract, npu_hooks, lane_activation_contract],
        gate,
    )
    contract = {
        "schema_version": 1,
        "kind": "heap_provider_invocation_contract",
        "generated_at": now_iso(),
        "passed": bool(gate.get("passed")),
        "provider_runtime_owner": "Tools.ai.heap_gate.provider_execution.run_provider_teamwork",
        "provider_lane": PRIMARY_PROVIDER_LANE,
        "permit_decision": safe_dict(governor.get("permit")).get("decision"),
        "permit_allowed": safe_dict(governor.get("permit")).get("permit_allowed"),
        "workload_report_contract": workload_contract,
        "expected_telemetry_contract": telemetry_contract,
        "npu_audit_hooks": npu_hooks,
        "real_run_gate": gate,
        "lane_activation_contract": lane_activation_contract,
    }
    if gate.get("blocking_reasons"):
        contract["blocking_reasons"] = gate.get("blocking_reasons", [])
    return contract


def render_markdown(report: dict[str, Any]) -> str:
    gate = safe_dict(report.get("real_run_gate"))
    telemetry = safe_dict(report.get("expected_telemetry_contract"))
    workload = safe_dict(report.get("workload_report_contract"))
    lines = ["# Heap Provider Invocation Contract", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Provider lane: `{report.get('provider_lane')}`")
    lines.append(f"- Permit decision: `{report.get('permit_decision')}`")
    lines.append(f"- Real run decision: `{gate.get('decision')}`")
    lines.append(f"- Provider runtime owner: `{report.get('provider_runtime_owner')}`")
    lines.extend(["", "## Required heap events", ""])
    for item in telemetry.get("events_required", []):
        lines.append(f"- `{item}`")
    lines.extend(["", "## Workload report requirements", ""])
    for item in workload.get("minimum_content_requirements", []):
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--objective",
        default="prove heap-driven provider invocation contract before provider/LLM integration",
    )
    parser.add_argument("--budget-minutes", type=int, default=5)
    parser.add_argument("--max-rounds", type=int, default=4)
    parser.add_argument("--files-per-round", type=int, default=4)
    parser.add_argument("--max-context-files", type=int, default=40)
    parser.add_argument("--max-chars-per-file", type=int, default=4000)
    parser.add_argument("--max-new-tokens", type=int, default=1200)
    parser.add_argument("--keep-alive", default="10m")
    parser.add_argument("--npu-micro-start-mode", default="deferred")
    parser.add_argument("--npu-micro-timeout-seconds", type=int, default=60)
    parser.add_argument("--npu-final-wait-seconds", type=int, default=60)
    parser.add_argument("--npu-max-context-chars", type=int, default=8000)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=1200)
    parser.add_argument("--npu-max-new-tokens", type=int, default=384)
    parser.add_argument("--allow-provider-generation", action="store_true")
    parser.add_argument("--operator-intent", action="store_true")
    parser.add_argument("--requested-max-iterations", type=int, default=0)
    parser.add_argument(
        "--output", default="output/validation/heap_provider_invocation_contract.json"
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/heap_provider_invocation_contract.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    governor = build_heap_provider_budget_governor(
        config_from_namespace(args),
        requested_max_iterations=args.requested_max_iterations or None,
    )
    report = build_heap_provider_invocation_contract(
        governor,
        allow_provider_generation=args.allow_provider_generation,
        operator_intent=args.operator_intent,
    )
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
