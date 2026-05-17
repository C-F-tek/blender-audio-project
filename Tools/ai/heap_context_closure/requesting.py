"""Request augmentation and startup-continuation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import DEFAULT_REQUEST, REVISION_CONTEXT_MARKER


def revision_context_prompt(payload: dict[str, Any], path: Path | None, max_tasks: int) -> str:
    if not payload:
        return ""
    tasks = payload.get("tasks") if isinstance(payload.get("tasks"), list) else []
    selected = tasks[: max(0, int(max_tasks))]
    candidate_summary = (
        payload.get("candidate_applicability_summary")
        if isinstance(payload.get("candidate_applicability_summary"), dict)
        else {}
    )
    lines = [
        "",
        REVISION_CONTEXT_MARKER + ":",
        f"- path: {path if path else ''}",
        f"- protocol: {payload.get('protocol')}",
        f"- product_acceptance_status: {payload.get('product_acceptance_status')}",
        f"- product_acceptance_passed: {payload.get('product_acceptance_passed')}",
        f"- requires_concrete_rewrite: {payload.get('requires_concrete_rewrite')}",
        f"- priority_next_action: {payload.get('priority_next_action')}",
        f"- candidate_applicability_summary: {json.dumps(candidate_summary, ensure_ascii=False)}",
        f"- resume_from_block_id: {payload.get('resume_from_block_id')}",
        f"- latest_block_id: {payload.get('latest_block_id')}",
        f"- task_count: {len(tasks)}",
        "- GPU1 must consume rewrite/propagation tasks before emitting new proposal blocks.",
        "- If requires_concrete_rewrite=true, GPU1 must first rewrite non-concrete candidates with real repo paths and concrete operations.",
        "- GPU1 must not propagate symbols from candidates marked non-concrete or from sketch/stub code.",
        "- GPU1 may move backward to propagate imports, variables, functions, classes and contracts, then resume forward.",
        "- GPU0 and NPU tasks are parallel recheck/audit work over old pointers.",
        "TASKS:",
    ]
    for idx, task in enumerate(selected, start=1):
        if not isinstance(task, dict):
            continue
        lines.append(
            f"{idx}. {task.get('task_id')} role={task.get('role')} type={task.get('task_type')} "
            f"target={task.get('target_block_id')} resume={task.get('resume_from_block_id')}"
        )
        for key in (
            "candidate_applicability_flags",
            "discovered_symbols",
            "rejection_reasons",
        ):
            if task.get(key):
                lines.append(f"   {key}={json.dumps(task.get(key), ensure_ascii=False)}")
        if task.get("symbol_propagation_skipped"):
            lines.append(
                f"   symbol_propagation_skipped={task.get('symbol_propagation_skipped')} "
                f"reason={task.get('symbol_propagation_skip_reason')}"
            )
        if task.get("instruction"):
            lines.append(f"   instruction={task.get('instruction')}")
    if len(tasks) > len(selected):
        lines.append(
            f"- omitted_tasks={len(tasks) - len(selected)}; read full revision context artifact for remaining tasks."
        )
    return "\n".join(lines)


def augmented_request(
    base_request: str,
    revision_context_path: Path | None = None,
    revision_context_payload: dict[str, Any] | None = None,
    revision_context_max_tasks: int = 12,
) -> str:
    operator = base_request.strip() or DEFAULT_REQUEST
    revision_payload = revision_context_payload or {}
    revision_text = ""
    if REVISION_CONTEXT_MARKER not in operator:
        revision_text = revision_context_prompt(
            revision_payload,
            revision_context_path,
            revision_context_max_tasks,
        )
    return (
        operator
        + revision_text
        + "\n\nHEAP CHUNK/COMPOSER CONTRACT:\n"
        + "- Treat context as persistent chunks, not as a single response window.\n"
        + "- Startup context/memory/tool/docs reload has prepared a task-file artifact; consume it as current heap input.\n"
        + "- If startup_reload_degraded=true, carry it as an explicit heap fact and continue with degraded context.\n"
        + "- Write proposal iteration artifacts for every useful partial block.\n"
        + "- GPU1 may re-open, extend and enrich previously written proposal chunks; a richer final document can be a composed refinement of prior chunks, not only a brand-new answer.\n"
        + "- When prior chunks are thin but valid, iterate on them by adding concrete targets, acceptance criteria, validation commands, risks and package boundaries.\n"
        + "- Do not restart from scratch just because the final document needs more depth; cite previous chunk/revision ids when enriching them.\n"
        + "- GPU0 must review/refine/reject proposal chunks using source anchors, quality errors and prior iteration context.\n"
        + "- NPU must produce bounded audit/workload evidence when enabled and that evidence must enter proposal chunks.\n"
        + "- Exit product may be blocked when placeholders/stubs remain.\n"
        + "- Final operator package is composed from proposal_iterations, provider reports and context artifacts."
    )


def startup_artifact_refs(startup_payload: dict[str, Any]) -> list[str]:
    artifacts = (
        startup_payload.get("artifacts")
        if isinstance(startup_payload.get("artifacts"), dict)
        else {}
    )
    refs: list[str] = []
    for value in artifacts.values():
        if isinstance(value, str) and value and value not in refs:
            refs.append(value)
    for execution in startup_payload.get("tool_executions") or []:
        if not isinstance(execution, dict):
            continue
        for key in ("useful_artifact_paths", "existing_artifact_paths", "artifact_paths"):
            for value in execution.get(key) or []:
                if isinstance(value, str) and value and value not in refs:
                    refs.append(value)
        for summary in execution.get("artifact_summaries") or []:
            if isinstance(summary, dict):
                value = summary.get("path")
                if isinstance(value, str) and value and value not in refs:
                    refs.append(value)
    return refs


def startup_can_continue(
    *,
    startup_result: dict[str, Any],
    startup_payload: dict[str, Any],
    startup_task_file: Path,
    strict_startup_reload: bool,
    skipped: bool,
) -> bool:
    if skipped or startup_result.get("passed") is True:
        return True
    if strict_startup_reload:
        return False
    if startup_payload.get("input_ready_before_heap") is True and startup_task_file.exists():
        return True
    return bool(startup_task_file.exists() and startup_artifact_refs(startup_payload))
