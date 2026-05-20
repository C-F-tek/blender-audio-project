#!/usr/bin/env python3
"""Provider budget governor for heap-driven IA-Carmine runtime loops.

This module intentionally does not import any deleted legacy pipeline package. It
extracts the useful semantics from the old provider governor layer into a small,
provider-free contract that can be written to the heap before any GPU/NPU/LLM
execution is allowed.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

DEFAULT_LANES = {
    "gpu1_planner": {
        "role": "primary_planner",
        "provider_kind": "ollama_gpu",
        "generation_allowed": False,
        "requires_explicit_operator_intent": True,
        "requires_runtime_provider_permit": True,
    },
    "gpu0_peer": {
        "role": "peer_reviewer_refiner",
        "provider_kind": "openvino_gpu0",
        "generation_allowed": False,
        "peer_review_required_when_provider_selected": True,
        "primary_generation_role": False,
    },
    "npu_micro_task_auditor": {
        "role": "micro_task_auditor",
        "provider_kind": "openvino_npu",
        "generation_allowed": False,
        "audit_only": True,
        "model_load_required": False,
    },
    "broker": {
        "role": "tool_executor",
        "provider_kind": "local_tool_broker",
        "generation_allowed": False,
        "allowlisted_tools_only": True,
    },
}


@dataclass(frozen=True)
class ProviderBudgetConfig:
    objective: str
    budget_minutes: int
    max_rounds: int
    files_per_round: int
    max_context_files: int
    max_chars_per_file: int
    max_new_tokens: int
    keep_alive: str
    npu_micro_start_mode: str
    npu_micro_timeout_seconds: int
    npu_final_wait_seconds: int
    npu_max_context_chars: int
    npu_max_prompt_chars: int
    npu_max_new_tokens: int
    allow_provider_generation: bool = False
    operator_intent: bool = False


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def positive_int(value: Any, default: int, minimum: int = 1) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, parsed)


def normalized_npu_micro_start_mode(value: str) -> str:
    raw = str(value or "startup").strip().lower()
    aliases = {
        "peer": "startup",
        "post-gpu-provider": "final-provider",
        "post_gpu_provider": "final-provider",
        "off": "disabled",
        "none": "disabled",
    }
    return aliases.get(raw, raw)


def clamp_loop_iterations(config: ProviderBudgetConfig, requested_max_iterations: int) -> int:
    max_rounds = positive_int(config.max_rounds, 1)
    requested = positive_int(requested_max_iterations, max_rounds)
    budget_seconds = positive_int(config.budget_minutes, 1) * 60
    counter_cycles = max_rounds if budget_seconds <= 0 else max(max_rounds, budget_seconds // 5)
    return max(1, requested, max_rounds, counter_cycles)


def build_budget_plan(
    config: ProviderBudgetConfig, requested_max_iterations: int | None = None
) -> dict[str, Any]:
    max_iterations = clamp_loop_iterations(config, requested_max_iterations or config.max_rounds)
    return {
        "kind": "heap_provider_budget_plan",
        "objective": config.objective,
        "loop_budget": {
            "budget_minutes": positive_int(config.budget_minutes, 1),
            "max_rounds": positive_int(config.max_rounds, 1),
            "max_iterations": max_iterations,
            "loop_counter_semantics": "time_counter_cycle_capacity_not_hard_provider_cutoff",
            "files_per_round": positive_int(config.files_per_round, 1),
            "max_context_files": positive_int(config.max_context_files, 1),
            "max_chars_per_file": positive_int(config.max_chars_per_file, 1),
            "max_new_tokens": positive_int(config.max_new_tokens, 1),
            "keep_alive": config.keep_alive,
        },
        "provider_lanes": {
            **DEFAULT_LANES,
            "npu_micro_task_auditor": {
                **DEFAULT_LANES["npu_micro_task_auditor"],
                "start_mode": normalized_npu_micro_start_mode(config.npu_micro_start_mode),
                "requested_counter_seconds": positive_int(config.npu_micro_timeout_seconds, 1),
                "final_wait_counter_seconds": positive_int(config.npu_final_wait_seconds, 0, minimum=0),
                "max_context_chars": positive_int(config.npu_max_context_chars, 1),
                "max_prompt_chars": positive_int(config.npu_max_prompt_chars, 1),
                "max_new_tokens": positive_int(config.npu_max_new_tokens, 1),
                "time_input_semantics": "counter_not_hard_lane_timeout",
                "started_lane_hard_kill_allowed": False,
                "lane_start_failure_policy": "abort_universe",
            },
        },
        "global_limits": {
            "no_generation_without_permit": True,
            "no_patch_apply_from_provider": True,
            "no_blender_runtime": True,
            "no_ffmpeg_runtime": True,
            "output_only_under_output_or_docs_evidence": True,
            "product_status_required": True,
        },
        "budget_order": [
            "heap_state_first",
            "brokered_tool_evidence_second",
            "critic_claim_third",
            "arbiter_decision_fourth",
            "product_signal_required_before_exit",
            "provider_generation_only_after_runtime_permit",
        ],
    }


def build_requirements(
    config: ProviderBudgetConfig, budget: dict[str, Any]
) -> list[dict[str, Any]]:
    loop_budget = budget.get("loop_budget") if isinstance(budget.get("loop_budget"), dict) else {}
    return [
        {
            "requirement": "operator_intent_for_provider_generation",
            "passed": bool(config.operator_intent) or not bool(config.allow_provider_generation),
            "reason": "provider generation requires explicit operator intent when provider runtime is selected",
        },
        {
            "requirement": "budget_minutes_positive",
            "passed": positive_int(loop_budget.get("budget_minutes"), 0, minimum=0) > 0,
            "reason": "loop must have an explicit time budget",
        },
        {
            "requirement": "max_rounds_positive",
            "passed": positive_int(loop_budget.get("max_rounds"), 0, minimum=0) > 0,
            "reason": "loop must have an explicit round budget",
        },
        {
            "requirement": "provider_runtime_permit_required",
            "passed": all(
                not lane.get("generation_allowed")
                for lane in budget.get("provider_lanes", {}).values()
            ),
            "reason": "provider lanes require a valid runtime permit before generation",
        },
        {
            "requirement": "product_status_required",
            "passed": budget.get("global_limits", {}).get("product_status_required") is True,
            "reason": "heap loop must exit with ready or blocked_with_reason",
        },
    ]


def build_run_permit(
    config: ProviderBudgetConfig, requirements: list[dict[str, Any]]
) -> dict[str, Any]:
    failed = [item for item in requirements if item.get("passed") is not True]
    permit_allowed = bool(
        config.allow_provider_generation and config.operator_intent and not failed
    )
    raw_blocking_reasons = [
        "provider generation selected without a valid heap/provider permit"
    ] + [str(item.get("requirement")) for item in failed]
    blocking_reasons = (
        raw_blocking_reasons if config.allow_provider_generation and not permit_allowed else []
    )
    permit = {
        "kind": "heap_provider_run_permit",
        "passed": not blocking_reasons,
        "permit_allowed": permit_allowed,
        "decision": (
            "allow_provider_generation"
            if permit_allowed
            else (
                "provider_generation_blocked_missing_operator_intent"
                if config.allow_provider_generation
                else "provider_generation_not_selected"
            )
        ),
        "allow_provider_generation_requested": bool(config.allow_provider_generation),
        "operator_intent": bool(config.operator_intent),
        "blocked_product_required_if_provider_selected": bool(blocking_reasons),
        "execution_contract": {
            "provider_generation_runtime_owner": (
                "Tools.ai.heap_gate.provider_execution.run_provider_teamwork"
            ),
            "provider_runtime_requires_this_permit": True,
            "provider_generation_must_write_heap_events": True,
            "provider_generation_must_write_tool_telemetry": True,
        },
    }
    if failed:
        permit["failed_requirements"] = failed
    if blocking_reasons:
        permit["blocking_reasons"] = blocking_reasons
    return permit


def build_heap_provider_budget_governor(
    config: ProviderBudgetConfig, requested_max_iterations: int | None = None
) -> dict[str, Any]:
    budget = build_budget_plan(config, requested_max_iterations=requested_max_iterations)
    requirements = build_requirements(config, budget)
    permit = build_run_permit(config, requirements)
    errors = list(permit.get("blocking_reasons") or [])
    governor = {
        "schema_version": 1,
        "kind": "heap_provider_budget_governor",
        "generated_at": now_iso(),
        "passed": not errors,
        "objective": config.objective,
        "budget": budget,
        "requirements": requirements,
        "permit": permit,
        "decision": permit["decision"],
        "permit_allowed": permit["permit_allowed"],
        "loop_budget": budget["loop_budget"],
        "provider_lanes": budget["provider_lanes"],
    }
    if permit.get("blocking_reasons"):
        governor["blocking_reasons"] = permit["blocking_reasons"]
    if errors:
        governor["errors"] = errors
    return governor


def config_from_namespace(args: argparse.Namespace) -> ProviderBudgetConfig:
    return ProviderBudgetConfig(
        objective=args.objective,
        budget_minutes=args.budget_minutes,
        max_rounds=args.max_rounds,
        files_per_round=args.files_per_round,
        max_context_files=args.max_context_files,
        max_chars_per_file=args.max_chars_per_file,
        max_new_tokens=args.max_new_tokens,
        keep_alive=args.keep_alive,
        npu_micro_start_mode=args.npu_micro_start_mode,
        npu_micro_timeout_seconds=args.npu_micro_timeout_seconds,
        npu_final_wait_seconds=args.npu_final_wait_seconds,
        npu_max_context_chars=args.npu_max_context_chars,
        npu_max_prompt_chars=args.npu_max_prompt_chars,
        npu_max_new_tokens=args.npu_max_new_tokens,
        allow_provider_generation=args.allow_provider_generation,
        operator_intent=args.operator_intent,
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Provider Budget Governor", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Decision: `{report.get('decision')}`")
    lines.append(f"- Permit allowed: `{report.get('permit_allowed')}`")
    loop_budget = report.get("loop_budget") if isinstance(report.get("loop_budget"), dict) else {}
    lines.extend(["", "## Loop budget", ""])
    for key in (
        "budget_minutes",
        "max_rounds",
        "max_iterations",
        "files_per_round",
        "max_context_files",
        "max_chars_per_file",
        "max_new_tokens",
        "keep_alive",
    ):
        lines.append(f"- {key}: `{loop_budget.get(key)}`")
    lines.extend(["", "## Provider lanes", ""])
    lanes = report.get("provider_lanes") if isinstance(report.get("provider_lanes"), dict) else {}
    for lane, value in lanes.items():
        if isinstance(value, dict):
            lines.append(
                f"- `{lane}` role=`{value.get('role')}` provider=`{value.get('provider_kind')}` generation_allowed=`{value.get('generation_allowed')}`"
            )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--objective", default="prove heap-driven provider budget before runtime loop"
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
    parser.add_argument("--output", default="output/validation/heap_provider_budget_governor.json")
    parser.add_argument(
        "--markdown-output",
        default="output/validation/heap_provider_budget_governor.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_heap_provider_budget_governor(
        config_from_namespace(args),
        requested_max_iterations=args.requested_max_iterations or None,
    )
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
