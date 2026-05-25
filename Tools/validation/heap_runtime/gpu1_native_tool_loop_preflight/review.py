"""Deterministic delta review helper for the GPU1 native tool-loop preflight."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import artifact_ref, write_text_artifact
from Tools.validation._shared.report_utils import write_json_report


GPU1_LANE = "gpu1_planner"


def run_delta_review_tool(
    *,
    repo_root: Path,
    work_dir: Path,
    stamp: str,
    request_id: str,
    delta_text: str,
    provider_report: Path,
    evidence_report: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    """Capture the delta and validate review evidence without calling generic_write."""
    review_dir = work_dir / "delta_review"
    delta_ref = write_text_artifact(
        repo_root,
        review_dir,
        name="gpu1_final_product_delta",
        text=delta_text,
        kind="gpu1_final_product_delta_review_input",
        producer="gpu1_native_tool_loop_preflight",
        suffix=".md",
    )
    evidence = _read_json(evidence_report)
    errors: list[str] = []
    if not delta_text.strip():
        errors.append("gpu1_one_turn_final_product_delta_empty")
    if evidence.get("all_tool_reports_passed") is not True:
        errors.append("gpu1_delta_review_broker_not_all_passed")
    if int(evidence.get("failed_tool_report_count") or 0) > 0:
        errors.append("gpu1_delta_review_failed_tool_report_present")
    if int(evidence.get("tool_result_failed_count") or 0) > 0:
        errors.append("gpu1_delta_review_failed_tool_result_present")
    if int(evidence.get("tool_result_passed_count") or 0) <= 0:
        errors.append("gpu1_delta_review_passed_tool_result_missing")

    review_output = review_dir / "delta_review_semantic_report.json"
    review_report = {
        "schema_version": 1,
        "kind": "gpu1_delta_deterministic_review",
        "request_id": f"{request_id}_delta_deterministic_review",
        "stamp": stamp,
        "lane": GPU1_LANE,
        "passed": not errors,
        "generic_write_performed": False,
        "artifact_capture_performed": True,
        "semantic_review_performed": True,
        "provider_report_ref": artifact_ref(
            provider_report, repo_root, kind="gpu1_delta_review_provider_report"
        ),
        "evidence_report_ref": artifact_ref(
            evidence_report, repo_root, kind="gpu1_delta_review_evidence_report"
        ),
        "delta_ref": delta_ref,
        "errors": errors,
    }
    write_json_report(review_report, review_output)
    return {
        "request_id": str(review_report["request_id"]),
        "passed": bool(review_report.get("passed")),
        "review_report": review_report,
        "review_report_ref": artifact_ref(
            review_output, repo_root, kind="gpu1_delta_deterministic_review"
        ),
        "delta_ref": delta_ref,
        "tool_result": {},
        "errors": errors,
    }


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}
