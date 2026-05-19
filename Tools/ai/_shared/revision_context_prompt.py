"""Shared external heap revision-context prompt rendering."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_REVISION_CONTEXT_MARKER = "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN"
REVISION_CONTEXT_INSTRUCTIONS = [
    "- GPU1 must consume rewrite/propagation tasks before emitting new proposal blocks.",
    "- If requires_concrete_rewrite=true, GPU1 must first rewrite non-concrete candidates with real repo paths and concrete operations.",
    "- GPU1 must not propagate symbols from candidates marked non-concrete or from sketch/stub code.",
    "- GPU1 may move backward to propagate imports, variables, functions, classes and contracts, then resume forward.",
    "- GPU0 and NPU tasks are parallel recheck/audit work over old pointers.",
]
TASK_DETAIL_KEYS = (
    "candidate_applicability_flags",
    "discovered_symbols",
    "rejection_reasons",
)


def render_revision_context_prompt(
    payload: dict[str, Any],
    path: Path | None,
    max_tasks: int,
    *,
    marker: str = DEFAULT_REVISION_CONTEXT_MARKER,
) -> str:
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
        f"{marker}:",
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
        *REVISION_CONTEXT_INSTRUCTIONS,
        "TASKS:",
    ]
    for idx, task in enumerate(selected, start=1):
        if isinstance(task, dict):
            _append_task_lines(lines, idx, task)
    if len(tasks) > len(selected):
        lines.append(
            f"- omitted_tasks={len(tasks) - len(selected)}; read full revision context artifact for remaining tasks."
        )
    return "\n".join(lines)


def _append_task_lines(lines: list[str], idx: int, task: dict[str, Any]) -> None:
    lines.append(
        f"{idx}. {task.get('task_id')} role={task.get('role')} type={task.get('task_type')} "
        f"target={task.get('target_block_id')} resume={task.get('resume_from_block_id')}"
    )
    for key in TASK_DETAIL_KEYS:
        if task.get(key):
            lines.append(f"   {key}={json.dumps(task.get(key), ensure_ascii=False)}")
    if task.get("symbol_propagation_skipped"):
        lines.append(
            f"   symbol_propagation_skipped={task.get('symbol_propagation_skipped')} "
            f"reason={task.get('symbol_propagation_skip_reason')}"
        )
    if task.get("instruction"):
        lines.append(f"   instruction={task.get('instruction')}")
