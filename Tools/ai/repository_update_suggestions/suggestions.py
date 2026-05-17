"""Deterministic suggestion and prompt builders."""

from __future__ import annotations

import json
from typing import Any

def deterministic_suggestions(context: dict[str, Any]) -> list[dict[str, str]]:
    suggestions: list[dict[str, str]] = []
    reports = context.get("validation_reports", [])
    failed_reports = [r for r in reports if r.get("passed") is False]
    missing_reports = [r for r in reports if not r.get("exists")]
    active_plans = context.get("execution_plans", {}).get("active", [])
    routing = context.get("advisory_context_routing", {})
    excluded_context = (
        routing.get("excluded_context_files", []) if isinstance(routing, dict) else []
    )

    if excluded_context:
        suggestions.append(
            {
                "priority": "P1",
                "area": "advisory_context",
                "title": "Use only quality-approved AI workload context files",
                "details": "; ".join(
                    f"excluded {item.get('path')} ({item.get('lane')}: {item.get('reason')})"
                    for item in excluded_context[:8]
                    if isinstance(item, dict)
                ),
            }
        )
    if failed_reports:
        suggestions.append(
            {
                "priority": "P1",
                "area": "validation",
                "title": "Fix failing validation reports before new runtime work",
                "details": "; ".join(
                    f"{r.get('path')}: {r.get('errors')}" for r in failed_reports[:5]
                ),
            }
        )
    if missing_reports:
        suggestions.append(
            {
                "priority": "P2",
                "area": "validation",
                "title": "Run or review missing validation reports before strict follow-up work",
                "details": "; ".join(str(r.get("path")) for r in missing_reports[:8]),
            }
        )
    if active_plans:
        suggestions.append(
            {
                "priority": "P2",
                "area": "execution_plans",
                "title": "Review active execution plans before opening the next milestone",
                "details": "; ".join(active_plans[:10]),
            }
        )
    suggestions.append(
        {
            "priority": "P2",
            "area": "agnostic_core",
            "title": "Prefer additive observability before provider or Blender runtime changes",
            "details": "Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.",
        }
    )
    return suggestions

def build_ollama_prompt(context: dict[str, Any], deterministic: list[dict[str, str]]) -> str:
    routing = context.get("advisory_context_routing", {})
    compact_routing = {
        "enforced": routing.get("enforced") if isinstance(routing, dict) else None,
        "advisory_lanes": (routing.get("advisory_lanes") if isinstance(routing, dict) else []),
        "excluded_advisory_lanes": (
            routing.get("excluded_advisory_lanes") if isinstance(routing, dict) else []
        ),
        "excluded_context_files": (
            routing.get("excluded_context_files") if isinstance(routing, dict) else []
        ),
        "provider_execution_performed": (
            routing.get("provider_execution_performed") if isinstance(routing, dict) else False
        ),
    }
    compact = {
        "profile": context.get("profile"),
        "repo_root": context.get("repo_root"),
        "advisory_context_routing": compact_routing,
        "validation_reports": context.get("validation_reports"),
        "execution_plans": context.get("execution_plans"),
        "deterministic_suggestions": deterministic,
    }
    return (
        "You are a local repository maintenance assistant for blender-audio-project.\n"
        "Return concise Markdown only. Do not propose Blender runtime, Ready To Jazz, "
        "provider execution, full analysis JSON edits, or generated index hand edits.\n"
        "Use only quality-approved AI workload context files.\n"
        "Prioritize app-agnostic core/backend/AI/NPU/multistep/guardrail/memory.\n\n"
        "Context JSON:\n"
        + json.dumps(compact, indent=2, ensure_ascii=False)
        + "\n\nProduce: 1) next safe milestone, 2) files to inspect, 3) validation commands, 4) stop conditions."
    )
