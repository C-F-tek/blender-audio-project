"""Remediation request generation for NPU guardrails."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import is_pythonish
from .config import INTERMEDIATE_ENRICHMENT_FIELDS

def remediation(
    action_type: str,
    priority: str,
    target: Path,
    reason: str,
    instruction: str,
    suggested_stage: str,
    auto_safe: bool,
    source_finding: str,
) -> dict[str, Any]:
    return {
        "action_type": action_type,
        "priority": priority,
        "target": str(target),
        "reason": reason,
        "instruction": instruction,
        "suggested_stage": suggested_stage,
        "auto_safe": auto_safe,
        "source_finding": source_finding,
    }


def missing_fields(payload: Any, kind: str) -> list[str]:
    if not isinstance(payload, dict):
        return []
    wanted = INTERMEDIATE_ENRICHMENT_FIELDS.get(kind, [])
    missing: list[str] = []
    for field in wanted:
        if field not in payload and not any(field in str(value) for value in payload.values()):
            missing.append(field)
    return missing


def remediation_requests(
    path: Path,
    payload: Any,
    text: str,
    kind: str,
    blocking: list[str],
    warnings: list[str],
    score: float,
) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    pythonish = is_pythonish(path, payload, text)

    for finding in blocking:
        if "ShaderNodeTexMusgrave" in finding:
            requests.append(
                remediation(
                    "fix_python_code",
                    "high",
                    path,
                    "Generated or indexed code references a Blender node that is blocked for the target Blender 5.x environment.",
                    "Replace ShaderNodeTexMusgrave with a Blender 5.x compatible procedural material strategy such as ShaderNodeTexNoise, ShaderNodeTexVoronoi and ColorRamp. Keep the change local and configurable.",
                    "python_patch_or_regenerate_code",
                    False,
                    finding,
                )
            )
        elif pythonish:
            requests.append(
                remediation(
                    "fix_python_code",
                    "high",
                    path,
                    "Blocking pattern detected in a Python-like artifact.",
                    "Request a focused Python correction patch. Do not rewrite the whole package; remove the blocked construct and preserve configurable paths and entry points.",
                    "python_patch_or_regenerate_code",
                    False,
                    finding,
                )
            )
        else:
            requests.append(
                remediation(
                    "review_generated_artifact",
                    "high",
                    path,
                    "Blocking pattern detected in an AI artifact.",
                    "Request a revised artifact from the planner/generator with the blocked pattern removed and the assumption documented.",
                    "regenerate_ai_artifact",
                    False,
                    finding,
                )
            )

    for finding in warnings:
        if "schema_version_missing" in finding or "explicit_assumptions_missing" in finding:
            requests.append(
                remediation(
                    "enrich_intermediate_data",
                    "medium",
                    path,
                    "Intermediate artifact is missing metadata required for reliable downstream AI planning.",
                    "Rerun or enrich the intermediate builder so the artifact includes schema_version, explicit assumptions and planner-ready metadata.",
                    "enrich_intermediates",
                    True,
                    finding,
                )
            )
        elif "artifact_large_for_npu_light_guardrail" in finding:
            requests.append(
                remediation(
                    "create_compact_summary",
                    "medium",
                    path,
                    "Artifact is too large for NPU-light review.",
                    "Create a compact summary artifact and use the full JSON only as a read-only source of truth.",
                    "compact_context_generation",
                    True,
                    finding,
                )
            )
        elif "local_windows_paths_present" in finding or "C:\\Users" in finding:
            requests.append(
                remediation(
                    "parameterize_path",
                    "medium",
                    path,
                    "Local workstation path detected.",
                    "Move the path into config or mark the artifact as local-only. Do not hardcode private paths in reusable generated packages.",
                    "python_patch_or_config_enrichment",
                    False,
                    finding,
                )
            )
        elif "too_few_selected_capsules" in finding or "smart_context_idea_missing" in finding:
            requests.append(
                remediation(
                    "rerun_context_selection",
                    "medium",
                    path,
                    "Smart context packet is under-specified for the requested task.",
                    "Rerun smart context generation with a more specific task and include additional task capsules, code chunks and artifact references.",
                    "smart_context_generation",
                    True,
                    finding,
                )
            )

    miss = missing_fields(payload, kind)
    if miss:
        requests.append(
            remediation(
                "enrich_intermediate_data",
                "medium" if score >= 0.5 else "high",
                path,
                f"{kind} artifact is missing planner-useful fields: {', '.join(miss)}.",
                "Add the missing fields through the relevant deterministic builder or a small AI enrichment pass. Preserve the original source analysis JSON as read-only.",
                "enrich_intermediates",
                True,
                "missing_fields:" + ",".join(miss),
            )
        )

    if score < 0.55 and not blocking:
        requests.append(
            remediation(
                "multi_pass_review",
                "medium",
                path,
                "Guardrail score is low but no blocking pattern was found.",
                "Run an additional review/enrichment pass before using this artifact as central AI context.",
                "guardrail_second_pass",
                True,
                f"low_score:{score}",
            )
        )

    return requests
