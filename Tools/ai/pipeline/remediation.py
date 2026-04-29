"""Guardrail remediation helpers for the AI artifact pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .artifact_contracts import (
    EXPECTED_MUSIC_ARTIFACTS,
    EXPECTED_SMART_CONTEXT_ARTIFACTS,
    EXPECTED_WAVE_REVIEW_ARTIFACTS,
)
from .compat import pipeline_step, run_pipeline_step
from .models import PipelineStep
from .steps import build_step_commands


def load_json_if_exists(path: Path) -> Any | None:
    """Load JSON when present; return None on parse or I/O failure."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def guardrail_queue(out: Path) -> dict[str, Any]:
    """Load guardrail action queue or return an empty compatible queue."""
    payload = load_json_if_exists(out / "npu_guardrail_action_queue.json")
    if isinstance(payload, dict):
        return payload
    return {"schema_version": 1, "queue": []}


def auto_safe_requests(out: Path) -> list[dict[str, Any]]:
    """Return auto-safe remediation requests from the guardrail queue."""
    queue = guardrail_queue(out).get("queue") or []
    return [item for item in queue if isinstance(item, dict) and item.get("auto_safe")]


def remediation_plan_from_requests(requests: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize guardrail remediation requests by stage and action type."""
    by_stage: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for item in requests:
        stage = str(item.get("suggested_stage") or "unknown")
        action = str(item.get("action_type") or "unknown")
        by_stage[stage] = by_stage.get(stage, 0) + 1
        by_type[action] = by_type.get(action, 0) + 1
    return {"request_count": len(requests), "by_stage": by_stage, "by_type": by_type, "requests": requests}


def remedial_steps(
    repo: Path,
    out: Path,
    args: Any,
    requests: list[dict[str, Any]],
    pass_index: int,
) -> list[PipelineStep]:
    """Build PipelineStep remediation commands requested by the guardrail."""
    commands = build_step_commands(repo, out, args)
    stages = {str(item.get("suggested_stage") or "") for item in requests}
    todo: list[PipelineStep] = []

    if "wave_entrypoint_review" in stages and "review_wave_entrypoints" in commands:
        todo.append(
            pipeline_step(
                "remediate_review_wave_entrypoints",
                "CPU",
                "Repeat first-wave script review requested by guardrail.",
                EXPECTED_WAVE_REVIEW_ARTIFACTS,
                commands["review_wave_entrypoints"],
                pass_index,
            )
        )
    if "enrich_intermediates" in stages and "build_music_intermediates" in commands:
        todo.append(
            pipeline_step(
                "remediate_build_music_intermediates",
                "CPU",
                "Auto-safe enrichment pass requested by NPU guardrail.",
                EXPECTED_MUSIC_ARTIFACTS,
                commands["build_music_intermediates"],
                pass_index,
            )
        )
    if "compact_context_generation" in stages and "build_smart_ai_context" in commands:
        todo.append(
            pipeline_step(
                "remediate_build_smart_ai_context_compact",
                "CPU",
                "Auto-safe compact context rebuild requested by NPU guardrail.",
                EXPECTED_SMART_CONTEXT_ARTIFACTS,
                commands["build_smart_ai_context"],
                pass_index,
            )
        )
    if "smart_context_generation" in stages and "build_smart_ai_context" in commands:
        todo.append(
            pipeline_step(
                "remediate_build_smart_ai_context",
                "CPU",
                "Auto-safe smart context rebuild requested by NPU guardrail.",
                EXPECTED_SMART_CONTEXT_ARTIFACTS,
                commands["build_smart_ai_context"],
                pass_index,
            )
        )
    if "guardrail_second_pass" in stages and "npu_guardrail" in commands:
        todo.append(
            pipeline_step(
                "remediate_npu_guardrail_second_pass",
                "NPU",
                "Second guardrail pass requested by NPU guardrail.",
                [str(out / "npu_guardrail_report.json")],
                commands["npu_guardrail"],
                pass_index,
            )
        )

    if todo and "npu_guardrail" in commands and all(step.name != "remediate_npu_guardrail_second_pass" for step in todo):
        todo.append(
            pipeline_step(
                "remediate_npu_guardrail_verify",
                "NPU",
                "Verify artifact state after auto-safe remediation passes.",
                [str(out / "npu_guardrail_report.json")],
                commands["npu_guardrail"],
                pass_index,
            )
        )

    return todo


def execute_remediation_loop(repo: Path, out: Path, args: Any, results: list[dict[str, Any]]) -> dict[str, Any]:
    """Execute auto-safe remediation passes requested by the NPU guardrail."""
    if not args.guardrail_auto_remediate or not args.npu_guardrail:
        return {"enabled": False, "reason": "disabled", "passes": []}

    passes: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()
    for pass_index in range(1, max(1, args.guardrail_max_passes) + 1):
        requests = auto_safe_requests(out)
        plan = remediation_plan_from_requests(requests)
        signature = json.dumps(plan.get("by_stage", {}), sort_keys=True)
        if not requests:
            passes.append({"pass_index": pass_index, "status": "no_auto_safe_requests", "plan": plan, "steps": []})
            break
        if signature in seen_signatures:
            passes.append({"pass_index": pass_index, "status": "repeated_plan_stopped", "plan": plan, "steps": []})
            break
        seen_signatures.add(signature)

        todo = remedial_steps(repo, out, args, requests, pass_index)
        if not todo:
            passes.append({"pass_index": pass_index, "status": "no_supported_remediation_commands", "plan": plan, "steps": []})
            break

        step_results = []
        for step in todo:
            res = run_pipeline_step(step, repo, args.dry_run)
            step_results.append(res)
            results.append(res)
            if res["returncode"] and not args.continue_on_error:
                break
        passes.append({"pass_index": pass_index, "status": "executed", "plan": plan, "steps": step_results})
        if any(item["returncode"] for item in step_results) and not args.continue_on_error:
            break
    return {"enabled": True, "max_passes": args.guardrail_max_passes, "passes": passes}
