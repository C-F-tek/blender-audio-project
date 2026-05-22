"""Request augmentation and startup-continuation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine._shared.revision_context_prompt import render_revision_context_prompt

from .common import DEFAULT_REQUEST, REVISION_CONTEXT_MARKER


def revision_context_prompt(payload: dict[str, Any], path: Path | None, max_tasks: int) -> str:
    return render_revision_context_prompt(
        payload,
        path,
        max_tasks,
        marker=REVISION_CONTEXT_MARKER,
    )


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
        + "- Startup context/memory/tool/docs reload has prepared a structured manifest, artifact refs and heap inputs; do not use the readable MD artifact as the runtime data plane.\n"
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
    artifact_ready = bool(startup_artifact_refs(startup_payload))
    if strict_startup_reload:
        return False
    if startup_payload.get("input_ready_before_heap") is True and artifact_ready:
        return True
    return bool(artifact_ready or startup_task_file.exists())
