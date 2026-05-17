#!/usr/bin/env python3
"""Report and selected-chunks summarizers for GitHub evidence bundles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.ai.github_evidence_bundle_io import (
    DEFAULT_SELECTED_CHUNKS_EVIDENCE,
    MAX_PATCH_PLAN_TEXT_CHARS,
    compact_value,
    read_json,
    repo_relative,
    resolve_repo_path,
    split_path_values,
)

CORE_SUMMARY_KEYS = (
    "usable_lanes",
    "unusable_lanes",
    "peer_mesh_operational_lanes",
    "peer_mesh_support_lanes",
    "peer_mesh_degraded_lanes",
    "peer_mesh_product_blockers",
    "provider_broker_loop_active",
    "provider_broker_loop_controlled_executor",
    "provider_broker_loop_broker_execution_count",
    "provider_broker_loop_gpu0_broker_execution_count",
    "provider_broker_loop_npu_broker_execution_count",
    "provider_broker_loop_product_blockers",
    "primary_advisory_provider",
    "policy",
    "mode",
    "provider",
    "python_exe",
    "device",
    "model_dir",
    "proposal_count",
    "patch_plan_count",
    "fallback_used",
    "manual_review_required",
    "recommendation_count",
    "round_count",
    "empty_recommendations_reason",
    "evidence_ready_for_manual_patch_count",
    "recommended_next_layer",
)
CHECK_SUMMARY_KEYS = (
    "classification",
    "usable_for_advisory",
    "npu_usable_for_advisory",
    "npu_classification",
    "metrics",
    "npu_metrics",
    "provider_envelope",
    "promotion_gate",
    "required_promotion_gate",
    "peer_mesh_visibility",
    "npu_support_lane",
    "collaboration_visibility",
    "peer_mesh_lane_state",
    "provider_broker_loop",
)
PATCH_NOTE_CORE_FIELDS = (
    "id",
    "area",
    "severity",
    "status",
    "target_files",
    "summary",
    "edit_strategy",
    "validation_commands",
    "stop_conditions",
    "manual_review_required",
)


def compact_patch_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Return compact patch-plan metadata for bundle summaries."""
    return {
        "id": plan.get("id"),
        "area": plan.get("area"),
        "source": plan.get("source"),
        "risk": plan.get("risk"),
        "status": plan.get("status"),
        "target_files": compact_value(plan.get("target_files") or [], max_string=300),
        "rationale": compact_value(
            plan.get("rationale") or "", max_string=MAX_PATCH_PLAN_TEXT_CHARS
        ),
        "edit_strategy": compact_value(
            plan.get("edit_strategy") or "", max_string=MAX_PATCH_PLAN_TEXT_CHARS
        ),
        "validation_commands": compact_value(plan.get("validation_commands") or [], max_string=500),
        "stop_conditions": compact_value(plan.get("stop_conditions") or [], max_string=500),
        "manual_review_required": plan.get("manual_review_required"),
    }


def compact_patch_note(note: dict[str, Any]) -> dict[str, Any]:
    """Return one compact patch-note proposal for AI-to-AI bundle handoff."""
    return {
        field: compact_value(note.get(field), max_string=1200)
        for field in PATCH_NOTE_CORE_FIELDS
        if field in note
    }


def patch_note_area_counts(patch_notes: list[dict[str, Any]]) -> dict[str, int]:
    """Return deterministic patch-note counts by area."""
    counts: dict[str, int] = {}
    for note in patch_notes:
        area = str(note.get("area") or "unknown")
        counts[area] = counts.get(area, 0) + 1
    return dict(sorted(counts.items()))


def summarize_patch_plan_report(data: dict[str, Any]) -> dict[str, Any] | None:
    """Return native patch-plan summary for legacy agent_review_patch_plan reports."""
    if data.get("kind") != "agent_review_patch_plan":
        return None

    decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
    patch_plans = data.get("patch_plans") if isinstance(data.get("patch_plans"), list) else []

    return {
        "patch_plan_count": data.get("patch_plan_count", len(patch_plans)),
        "fallback_used": decision.get("fallback_used"),
        "manual_review_required": decision.get("manual_review_required"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "patch_application_performed": data.get("patch_application_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "plans": [compact_patch_plan(plan) for plan in patch_plans if isinstance(plan, dict)],
    }


def summarize_patch_notes_quality_product_report(
    data: dict[str, Any],
) -> dict[str, Any] | None:
    """Return the complete compact proposal core for patch-notes quality products.

    This is intentionally not limited to the first 20 items: the patch-notes
    product is the durable handoff ledger used by the next AI/session to choose
    concrete patch waves. Each note is compacted field-by-field so the GitHub
    evidence bundle can carry all proposals without embedding full raw reports.
    """
    patch_notes = data.get("patch_notes") if isinstance(data.get("patch_notes"), list) else []
    if "patch_notes_quality_product" not in str(data.get("kind") or "") and not patch_notes:
        return None

    compact_notes = [compact_patch_note(note) for note in patch_notes if isinstance(note, dict)]
    product_sufficiency = (
        data.get("product_sufficiency") if isinstance(data.get("product_sufficiency"), dict) else {}
    )
    applicability = (
        data.get("patch_notes_applicability")
        if isinstance(data.get("patch_notes_applicability"), dict)
        else {}
    )

    return {
        "purpose": "durable_core_proposal_ledger_for_followup_patch_waves",
        "patch_note_count": len(compact_notes),
        "area_counts": patch_note_area_counts(
            [note for note in patch_notes if isinstance(note, dict)]
        ),
        "quality_gate_passed": data.get("quality_gate_passed"),
        "classification": data.get("classification"),
        "quality_score": data.get("quality_score"),
        "requested_areas": product_sufficiency.get("requested_areas"),
        "available_requested_areas": product_sufficiency.get("available_requested_areas"),
        "missing_available_areas": product_sufficiency.get("missing_available_areas"),
        "requested_min_patch_notes": product_sufficiency.get("requested_min_patch_notes"),
        "patch_note_limit": product_sufficiency.get("patch_note_limit"),
        "sufficient": product_sufficiency.get("sufficient"),
        "insufficiency_reasons": product_sufficiency.get("insufficiency_reasons"),
        "all_applicable": applicability.get("all_applicable"),
        "invalid_note_count": applicability.get("invalid_note_count"),
        "notes": compact_notes,
    }


def add_core_summary_fields(summary: dict[str, Any], data: dict[str, Any]) -> None:
    """Add common scalar/list report fields to a summary."""
    for key in CORE_SUMMARY_KEYS:
        if key in data:
            summary[key] = compact_value(data.get(key))


def add_nested_summary_fields(summary: dict[str, Any], data: dict[str, Any]) -> None:
    """Add compact nested report fields to a summary."""
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    if checks:
        summary["checks"] = compact_value(
            {key: checks.get(key) for key in CHECK_SUMMARY_KEYS if key in checks},
            max_string=350,
        )
    routing = data.get("routing") if isinstance(data.get("routing"), dict) else {}
    if routing:
        summary["routing"] = compact_value(
            {
                "advisory_lanes": routing.get("advisory_lanes"),
                "excluded_advisory_lanes": routing.get("excluded_advisory_lanes"),
                "primary_advisory_provider": routing.get("primary_advisory_provider"),
                "trusted_context_files": routing.get("trusted_context_files"),
                "excluded_context_files": routing.get("excluded_context_files"),
            },
            max_string=350,
        )
    context = data.get("context") if isinstance(data.get("context"), dict) else {}
    if context:
        summary["context"] = compact_value(
            {
                "context_files": context.get("context_files"),
                "excluded_context_files": context.get("excluded_context_files"),
                "advisory_context_routing": context.get("advisory_context_routing"),
            },
            max_string=350,
        )
    ollama = data.get("ollama") if isinstance(data.get("ollama"), dict) else {}
    if ollama:
        summary["ollama"] = compact_value(
            {
                "used": ollama.get("used"),
                "model": ollama.get("model"),
                "error": ollama.get("error"),
                "text_preview": (ollama.get("text") or "")[:500],
            },
            max_string=500,
        )

    for key in (
        "peer_mesh_visibility",
        "npu_support_lane",
        "collaboration_visibility",
        "peer_mesh_lane_state",
    ):
        value = data.get(key)
        if isinstance(value, dict):
            summary[key] = compact_value(value, max_string=900)


def promote_peer_mesh_lane_fields(summary: dict[str, Any], data: dict[str, Any]) -> None:
    """Promote peer-mesh lane fields from nested product reports into compact summaries."""

    lane_state = (
        data.get("peer_mesh_lane_state")
        if isinstance(data.get("peer_mesh_lane_state"), dict)
        else {}
    )
    if not lane_state:
        collaboration = (
            data.get("collaboration_round")
            if isinstance(data.get("collaboration_round"), dict)
            else {}
        )
        lane_state = (
            collaboration.get("peer_mesh_lane_state")
            if isinstance(collaboration.get("peer_mesh_lane_state"), dict)
            else {}
        )
    if lane_state:
        mapping = {
            "peer_mesh_operational_lanes": "operational_lanes",
            "peer_mesh_support_lanes": "support_lanes",
            "peer_mesh_degraded_lanes": "degraded_lanes",
            "peer_mesh_product_blockers": "product_blockers",
        }
        for summary_key, state_key in mapping.items():
            if summary.get(summary_key) is None and lane_state.get(state_key) is not None:
                summary[summary_key] = compact_value(lane_state.get(state_key))
        summary["peer_mesh_lane_state"] = compact_value(lane_state, max_string=900)


def base_report_summary(data: dict[str, Any]) -> dict[str, Any]:
    """Return common report summary fields."""
    return {
        "schema_version": data.get("schema_version"),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "patch_application_performed": data.get("patch_application_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "errors": compact_value(data.get("errors") or []),
        "warnings": compact_value(data.get("warnings") or []),
    }


def summarize_report(path: Path, repo_root: Path) -> dict[str, Any]:
    """Summarize one JSON validation/provider/report artifact."""
    rel = repo_relative(path, repo_root)
    data = read_json(path)
    if data is None:
        return {
            "path": rel,
            "exists": path.exists(),
            "json_ok": False,
            "kind": None,
            "passed": None,
            "summary": {},
        }

    summary = base_report_summary(data)
    add_core_summary_fields(summary, data)
    add_nested_summary_fields(summary, data)
    promote_peer_mesh_lane_fields(summary, data)

    patch_plan_summary = summarize_patch_plan_report(data)
    if patch_plan_summary:
        summary["patch_plan_summary"] = patch_plan_summary

    patch_notes_core = summarize_patch_notes_quality_product_report(data)
    if patch_notes_core:
        summary["proposal_core"] = patch_notes_core

    return {
        "path": rel,
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "summary": summary,
    }


def summarize_selected_chunks_evidence(path: Path, repo_root: Path) -> dict[str, Any]:
    """Return compact selected-chunks evidence without reading raw context packs."""
    rel = repo_relative(path, repo_root)
    data = read_json(path)
    if data is None:
        return {
            "path": rel,
            "exists": path.exists(),
            "json_ok": False,
            "kind": None,
            "passed": None,
            "summary": {},
        }

    summary: dict[str, Any] = {
        "schema_version": data.get("schema_version"),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "selected_count": data.get("selected_count"),
        "total_selected_chars": data.get("total_selected_chars"),
        "max_chunks": data.get("max_chunks"),
        "max_total_chars": data.get("max_total_chars"),
        "source_bundle": data.get("source_bundle"),
        "source_chunks": data.get("source_chunks"),
        "decision": compact_value(data.get("decision") or {}),
        "errors": compact_value(data.get("errors") or []),
        "warnings": compact_value(data.get("warnings") or []),
    }
    return {
        "path": rel,
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "summary": summary,
    }


def discover_selected_chunks_evidence(
    repo_root: Path, explicit_paths: list[str], *, auto_discover: bool = True
) -> list[Path]:
    """Discover compact selected-chunks evidence files under docs evidence."""
    candidates = split_path_values(explicit_paths)
    if auto_discover and not candidates:
        candidates = list(DEFAULT_SELECTED_CHUNKS_EVIDENCE)
        evidence_dir = repo_root / "docs" / "LOCAL_VALIDATION_EVIDENCE"
        if evidence_dir.exists():
            for path in sorted(evidence_dir.glob("*selected_chunks_evidence.json")):
                rel = repo_relative(path, repo_root)
                if rel not in candidates:
                    candidates.append(rel)
    resolved: list[Path] = []
    seen: set[str] = set()
    for raw in candidates:
        path = resolve_repo_path(repo_root, raw)
        key = path.resolve().as_posix() if path.exists() else path.as_posix()
        if key not in seen and path.exists():
            resolved.append(path)
            seen.add(key)
    return resolved


def report_summaries(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return summary dicts from report entries."""
    return [item.get("summary", {}) for item in reports if isinstance(item.get("summary"), dict)]
