"""Delta review helper for the GPU1 native tool-loop preflight."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import artifact_ref, write_text_artifact
from ia_carmine.runtime.runtime_tool.broker.executor import build_report
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
    operator_ref = write_text_artifact(
        repo_root,
        review_dir,
        name="delta_review_request",
        text=(
            "Review this GPU1 FINAL_PRODUCT_DELTA as a report-only follow-up artifact. "
            "Do not apply code and do not synthesize product in place of GPU1. "
            "Return refinement/review evidence for the next runtime turn."
        ),
        kind="gpu1_delta_review_request",
        producer="gpu1_native_tool_loop_preflight",
        suffix=".md",
    )
    review_request_id = f"{request_id}_delta_review_generic_write"
    request_file = review_dir / "delta_review_broker_request_packet.json"
    _json_write(
        {
            "schema_version": 1,
            "kind": "agent_runtime_tool_requests",
            "source": "gpu1_delta_review_preflight",
            "tool_requests": [
                {
                    "id": review_request_id,
                    "request_id": review_request_id,
                    "tool": "generic_write",
                    "args": {
                        "request_file": str(operator_ref["path"]),
                        "provider_report": str(provider_report),
                        "proposal_text_file": str(delta_ref["path"]),
                        "capture_mode": "native_call",
                        "evidence_report": str(evidence_report),
                        "source_lane": GPU1_LANE,
                        "source_revision": "0",
                        "gpu1_followup_required": "true",
                        "provider_role": "primary",
                        "reason": "preflight_delta_review_before_run_unica_launch",
                    },
                    "source": "gpu1_delta_review_preflight",
                    "lane": GPU1_LANE,
                    "provider_native_tool_call": False,
                    "delta_review_tool_call": True,
                    "revision": 0,
                    "gpu1_tool_loop_subturn": 1,
                }
            ],
        },
        request_file,
    )
    broker_output = review_dir / "delta_review_broker_report.json"
    review_report = build_report(
        argparse.Namespace(
            repo_root=str(repo_root),
            request_file=str(request_file),
            request_json="",
            payload_file="",
            job_id=f"{stamp}_delta_review",
            tool_output_dir=str(review_dir / "broker_tools"),
            stamp=f"{stamp}_delta_review",
            timeout_seconds=timeout_seconds,
            dry_run=False,
            output=str(broker_output),
            markdown_output=str(broker_output.with_suffix(".md")),
        )
    )
    write_json_report(review_report, broker_output)
    results = review_report.get("tool_results") if isinstance(review_report.get("tool_results"), list) else []
    result = dict(results[0]) if results and isinstance(results[0], dict) else {}
    return {
        "request_id": review_request_id,
        "passed": bool(review_report.get("passed") and result.get("executed") is True),
        "broker_report": review_report,
        "broker_report_ref": artifact_ref(broker_output, repo_root, kind="gpu1_delta_review_broker_report"),
        "delta_ref": delta_ref,
        "operator_request_ref": operator_ref,
        "tool_result": result,
    }


def _json_write(payload: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
