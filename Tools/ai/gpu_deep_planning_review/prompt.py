from __future__ import annotations

from .common import *  # noqa: F403

def build_prompt(
    *,
    objective: str,
    evidence: dict[str, Any],
    refined: dict[str, Any],
    context_reports: list[dict[str, Any]],
    batch: list[ContextFile],
    round_index: int,
    elapsed_seconds: float,
) -> str:
    files_block = []
    for item in batch:
        files_block.append(
            {
                "path": item.path,
                "exists": item.exists,
                "lines": item.lines,
                "chars": item.chars,
                "content_preview": item.preview,
            }
        )
    instruction = {
        "role": "IA-Carmine GPU deep planning reviewer",
        "objective": objective,
        "round_index": round_index,
        "elapsed_seconds": round(elapsed_seconds, 2),
        "rules": [
            "Do not propose automatic patch application.",
            "Use only evidence from supplied files and reports.",
            "Classify each recommendation as ready_for_patch_plan, needs_more_context, or advisory_only.",
            "Prefer small manual-review docs/code patch plans over broad rewrites.",
            "Call out missing evidence explicitly.",
            "Return valid JSON only.",
            "When schema_repair_provider_context is present, treat it as a hard repair contract for the next answer.",
            "Runtime tool evidence means you must convert evidence into recommendations or explicit missing_evidence; do not request the same evidence again.",
            "If evidence_ready_for_manual_patch_count is greater than zero, prefer at least one ready_for_patch_plan recommendation unless a specific blocker remains.",
            "When evidence is missing, request broker tools through tool_requests instead of guessing.",
            "If you cannot produce a schema-valid recommendation, emit at least one valid tool_request when an allowlisted tool can reduce uncertainty.",
            "Do not answer with prose summaries of repository files; return the JSON object only.",
            "Do not echo input file previews, execution plans, or documentation chunks.",
            "If recommendations is empty, tool_requests must be non-empty unless missing_evidence explicitly says no allowlisted tool can help.",
            "Never request shell, git write, provider execution, patch application, Blender runtime, or persistent memory writes.",
            "Operational memory may be requested only through runtime_sqlite_memory with scope=operational.",
            "Persistent memory may be searched/status-checked only through runtime_sqlite_memory with scope=persistent.",
        ],
        "available_runtime_tools": sorted(ALLOWED_RUNTIME_TOOLS),
        "tool_request_policy": {
            "execution_model": "planner emits tool_requests; orchestrator/broker executes later",
            "free_shell_allowed": False,
            "persistent_memory_write_allowed": False,
            "patch_application_allowed": False,
            "provider_execution_allowed": False,
            "operational_memory_scope": "scratch context under output/** only",
        },
        "tool_request_decision_guide": TOOL_REQUEST_DECISION_GUIDE,
        "provider_tool_guidance": build_provider_tool_guidance_payload("gpu_ollama"),
        "expected_json_schema": {
            "summary": "short technical summary",
            "confidence": "low|medium|high",
            "recommendations": [
                {
                    "id": "string",
                    "area": "doc_code|doc_doc|code_code|workflow|validation|other",
                    "status": "ready_for_patch_plan|needs_more_context|advisory_only",
                    "target_files": ["path"],
                    "rationale": "string",
                    "proposed_strategy": "string",
                    "risk": "low|medium|high",
                    "validation_commands": ["command"],
                    "stop_conditions": ["condition"],
                }
            ],
            "tool_requests": [
                {
                    "id": "string",
                    "tool": "one available_runtime_tools value",
                    "reason": "why the tool is needed before deciding",
                    "args": {},
                }
            ],
            "missing_evidence": ["string"],
            "next_best_action": "string",
        },
    }
    return "\n\n".join(
        [
            "You are reviewing a complex repository using explicit local GPU/Ollama reasoning.",
            "INSTRUCTIONS JSON:\n" + compact_json(instruction, 6000),
            "EVIDENCE SUFFICIENCY REPORT:\n" + compact_json(evidence, 18000),
            "REFINED MEGALITHIC REVIEW:\n" + compact_json(refined, 18000),
            "OPTIONAL CONTEXT REPORTS:\n" + compact_json(context_reports, 14000),
            "REPOSITORY FILE BATCH:\n" + compact_json(files_block, 36000),
        ]
    )
