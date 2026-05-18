"""Report writers for NPU guardrails."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import now_iso

def write_md(report: dict[str, Any], path: Path) -> None:
    pre = report.get("npu_preflight") or {}
    runtime = report.get("runtime_summary") or {}
    remediation_plan = report.get("remediation_plan") or {}
    lines = [
        "# NPU Guardrail Report",
        "",
        f"Generated: `{report.get('generated_at')}`",
        f"Passed: `{report.get('passed')}`",
        f"Soft fail: `{report.get('soft_fail')}`",
        f"Average score: `{report.get('average_score')}`",
        "",
        "## Runtime",
        f"- Mode: `{runtime.get('mode')}`",
        f"- Ready: `{runtime.get('ready')}`",
        f"- NPU available: `{runtime.get('npu_device_available')}`",
        f"- Recommended workers: `{runtime.get('recommended_workers')}`",
        f"- Devices: `{pre.get('openvino_available_devices')}`",
        "",
        "## Remediation Plan",
        f"- Requests: `{remediation_plan.get('request_count', 0)}`",
        f"- Auto-safe requests: `{remediation_plan.get('auto_safe_count', 0)}`",
        f"- Manual review requests: `{remediation_plan.get('manual_review_count', 0)}`",
    ]
    for action_type, count in (remediation_plan.get("by_type") or {}).items():
        lines.append(f"- {action_type}: `{count}`")
    lines += ["", "## Reviews"]
    for item in report.get("reviews", []):
        lines += [
            "",
            f"### {item.get('path')}",
            f"- Type: `{item.get('artifact_type')}`",
            f"- Score: `{item.get('score')}`",
            f"- Severity: `{item.get('severity')}`",
            f"- Passed: `{item.get('passed')}`",
        ]
        for block in item.get("blocking", []):
            lines.append(f"- BLOCKING: {block}")
        for warning in item.get("warnings", [])[:24]:
            lines.append(f"- Warning: {warning}")
        for request in item.get("remediation_requests", [])[:12]:
            lines.append(
                f"- Request `{request.get('action_type')}` / `{request.get('priority')}`: {request.get('instruction')}"
            )
        for positive in item.get("positives", [])[:16]:
            lines.append(f"- OK: {positive}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_action_queue(remediation_plan: dict[str, Any], report_path: Path) -> Path:
    queue_path = report_path.with_name("npu_guardrail_action_queue.json")
    payload = {
        "schema_version": 1,
        "generated_at": now_iso(),
        "source_report": str(report_path),
        "queue": remediation_plan.get("requests", []),
    }
    queue_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return queue_path
