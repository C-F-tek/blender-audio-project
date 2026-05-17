"""Artifact review and remediation aggregation for NPU guardrails."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import artifact_type, idea_scan, pattern_findings, read_json
from .config import BLOCKED_PATTERNS, REQUIRED_IDEAS, SMART_CONTEXT_IDEAS, WARNING_PATTERNS
from .remediation import remediation_requests

def review(path: Path, max_chars: int) -> dict[str, Any]:
    payload, read_warnings = read_json(path)
    text = json.dumps(payload, ensure_ascii=False)
    kind = artifact_type(path, payload)
    warnings: list[str] = list(read_warnings)
    blocking: list[str] = []
    positives: list[str] = []

    blocking.extend(pattern_findings(text, BLOCKED_PATTERNS, "blocked_pattern"))
    warnings.extend(pattern_findings(text, WARNING_PATTERNS, "warning_pattern"))

    if len(text) <= max_chars:
        positives.append("size_ok_for_npu_light_guardrail")
    else:
        warnings.append(f"artifact_large_for_npu_light_guardrail:{len(text)}>{max_chars}")

    base_warnings, base_positives = idea_scan(text, REQUIRED_IDEAS, "required_idea", required=False)
    warnings.extend(base_warnings)
    positives.extend(base_positives)

    if kind == "smart_context_packet":
        smart_warnings, smart_positives = idea_scan(
            text, SMART_CONTEXT_IDEAS, "smart_context_idea", required=True
        )
        warnings.extend(smart_warnings)
        positives.extend(smart_positives)

    if isinstance(payload, dict):
        if payload.get("schema_version"):
            positives.append("schema_version_present")
        else:
            warnings.append("schema_version_missing")
        selected = payload.get("selected_capsules")
        manifest = payload.get("capsule_manifest")
        assumptions = payload.get("assumptions")
        if isinstance(selected, list):
            positives.append(f"selected_capsules={len(selected)}")
            if len(selected) < 2:
                warnings.append("too_few_selected_capsules")
        if isinstance(manifest, list):
            positives.append(f"manifest_capsules={len(manifest)}")
        if kind in {"scene_brief", "smart_context_packet"} and not assumptions:
            warnings.append("explicit_assumptions_missing")

    score = max(
        0.0,
        min(
            1.0,
            round(
                1.0
                - len(blocking) * 0.35
                - len(warnings) * 0.045
                + min(0.22, len(positives) * 0.015),
                4,
            ),
        ),
    )
    severity = "blocking" if blocking else "warning" if warnings else "clean"
    requests = remediation_requests(path, payload, text, kind, blocking, warnings, score)
    return {
        "path": str(path),
        "artifact_type": kind,
        "size_chars": len(text),
        "score": score,
        "severity": severity,
        "passed": not blocking,
        "blocking": blocking,
        "warnings": warnings,
        "positives": positives,
        "remediation_requests": requests,
    }


def aggregate_remediation(reviews: list[dict[str, Any]]) -> dict[str, Any]:
    requests = [
        item for review_item in reviews for item in review_item.get("remediation_requests", [])
    ]
    by_stage: dict[str, list[dict[str, Any]]] = {}
    by_type: dict[str, int] = {}
    for item in requests:
        by_stage.setdefault(item["suggested_stage"], []).append(item)
        by_type[item["action_type"]] = by_type.get(item["action_type"], 0) + 1
    auto_safe = [item for item in requests if item.get("auto_safe")]
    manual = [item for item in requests if not item.get("auto_safe")]
    return {
        "request_count": len(requests),
        "auto_safe_count": len(auto_safe),
        "manual_review_count": len(manual),
        "by_type": by_type,
        "by_stage": {key: len(value) for key, value in by_stage.items()},
        "next_auto_safe_stages": sorted(by_stage.keys()),
        "requests": requests,
    }
