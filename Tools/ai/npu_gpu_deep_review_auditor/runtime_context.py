"""Runtime context preparation for NPU review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.ai.runtime_tool_guidance import build_provider_tool_guidance_payload

from .common import compact_json, read_json, repo_rel, resolve_path

def summarize_runtime_tool_context_report(
    path: Path, repo_root: Path, max_chars: int
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "path": repo_rel(path, repo_root),
        "exists": path.exists(),
        "json_ok": False,
    }
    if not path.exists() or not path.is_file():
        return item
    try:
        data = read_json(path)
    except Exception as exc:  # noqa: BLE001 - context summary must be non-blocking.
        item["read_error"] = f"{type(exc).__name__}: {exc}"
        return item
    item["json_ok"] = True
    tool_results = data.get("tool_results") if isinstance(data.get("tool_results"), list) else []
    item.update(
        {
            "kind": data.get("kind"),
            "passed": data.get("passed"),
            "tool_request_count": data.get("tool_request_count"),
            "tool_execution_count": data.get("tool_execution_count"),
            "blocked_tool_count": data.get("blocked_tool_count"),
            "failed_tool_count": data.get("failed_tool_count"),
            "provider_execution_performed": data.get("provider_execution_performed"),
            "patch_application_performed": data.get("patch_application_performed"),
            "sqlite_write_performed": data.get("sqlite_write_performed"),
            "persistent_memory_write_performed": data.get("persistent_memory_write_performed"),
            "operational_sqlite_write_performed": data.get("operational_sqlite_write_performed"),
            "guardrails": data.get("guardrails", {}),
            "tool_results": [
                {
                    "id": result.get("id"),
                    "tool": result.get("tool"),
                    "executed": result.get("executed"),
                    "blocked": result.get("blocked"),
                    "returncode": result.get("returncode"),
                    "outputs": result.get("outputs", {}),
                }
                for result in tool_results[:24]
                if isinstance(result, dict)
            ],
        }
    )
    rendered = json.dumps(item, ensure_ascii=False, default=str)
    if len(rendered) > max_chars:
        item["truncated"] = True
        item["tool_results"] = item.get("tool_results", [])[:8]
    return item

def load_runtime_tool_context_reports(
    repo_root: Path, values: list[str], max_chars: int
) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    seen: set[str] = set()
    for value in values:
        path = resolve_path(repo_root, value)
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        reports.append(summarize_runtime_tool_context_report(path, repo_root, max_chars))
    return reports

def build_context(
    gpu_review: dict[str, Any],
    runtime_tool_context_reports: list[dict[str, Any]] | None = None,
) -> str:
    runtime_tool_context_reports = runtime_tool_context_reports or []
    recommendations = gpu_review.get("recommendations", [])
    decision = gpu_review.get("decision", {})
    rounds = gpu_review.get("rounds", [])
    compact_rounds = []
    for item in rounds[:8]:
        compact_rounds.append(
            {
                "round": item.get("round"),
                "elapsed_seconds": item.get("elapsed_seconds"),
                "file_count": item.get("file_count"),
                "files": item.get("files", [])[:20],
                "parsed_response": item.get("parsed_response", {}),
            }
        )
    payload = {
        "role": "NPU audit guardrail for GPU/Ollama deep planning review",
        "instructions": [
            "Audit the GPU review for drift, over-broad patch plans, unsupported claims, missing evidence and guardrail violations.",
            "Do not create a patch.",
            "Do not act as primary advisory provider.",
            "Return concise Markdown with: Verdict, Drift Risks, Evidence Gaps, Guardrail Notes, Non-blocking Recommendation.",
            "If the audit needs more evidence, add a fenced JSON block containing tool_requests using the shared broker schema.",
        ],
        "gpu_review_summary": {
            "kind": gpu_review.get("kind"),
            "passed": gpu_review.get("passed"),
            "provider_execution_performed": gpu_review.get("provider_execution_performed"),
            "patch_application_performed": gpu_review.get("patch_application_performed"),
            "model_used": gpu_review.get("model_used"),
            "round_count": gpu_review.get("round_count"),
            "recommendation_count": gpu_review.get("recommendation_count"),
            "decision": decision,
            "guardrails": gpu_review.get("guardrails", {}),
        },
        "runtime_toolbox_context": {
            "seen": bool(runtime_tool_context_reports),
            "report_count": len(runtime_tool_context_reports),
            "reports": runtime_tool_context_reports,
            "instructions": [
                "Use this shared toolbox context as evidence for audit, not as authority to execute tools directly.",
                "The NPU auditor remains non-blocking and must not apply patches.",
                "Any further tool execution must be requested through the runtime broker/orchestrator layer.",
                "If additional evidence is needed, include optional JSON tool_requests using the shared broker schema; do not execute tools directly.",
                "When useful, include a fenced ```json object with top-level tool_requests so the broker can parse it.",
            ],
            "provider_tool_guidance": build_provider_tool_guidance_payload("npu_openvino"),
        },
        "recommendations": recommendations,
        "rounds": compact_rounds,
    }
    return "# NPU GPU Deep Review Audit Context\n\n" + compact_json(payload, 42000) + "\n"
