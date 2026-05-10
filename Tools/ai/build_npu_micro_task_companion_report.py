#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.npu.npu_runtime import guardrail_runtime_summary, npu_preflight
except ImportError:  # pragma: no cover
    guardrail_runtime_summary = None  # type: ignore
    npu_preflight = None  # type: ignore


def classify_request(text: str) -> str:
    normalized = " ".join(str(text or "").strip().lower().split())
    if not normalized:
        return "none"
    greetings = {"ciao", "salve", "buongiorno", "buonasera", "hello", "hi", "hey"}
    if normalized in greetings:
        return "casual_greeting"
    if any(token in normalized for token in ("errore", "traceback", "bug", "crash", "fallisce", "non funziona")):
        return "debug_request"
    if any(token in normalized for token in ("patch", "modifica", "codice", "script", "repo")):
        return "repo_work_request"
    return "general_request"


def run_npu_micro_task(timeout_seconds: int) -> dict[str, Any]:
    if npu_preflight is None:
        return {
            "ready": False,
            "mode": "npu_runtime_import_unavailable",
            "npu_device_available": False,
            "recommended_workers": 1,
            "error_count": 1,
            "warning_count": 0,
            "errors": ["Tools.npu.npu_runtime import unavailable"],
            "warnings": [],
            "micro_task_performed": False,
        }
    report = npu_preflight(timeout=float(timeout_seconds))
    summary = guardrail_runtime_summary(report) if guardrail_runtime_summary else {}
    return {
        **summary,
        "python_exe": report.get("python_exe"),
        "mode": report.get("mode"),
        "openvino_import": report.get("openvino_import"),
        "openvino_genai_import": report.get("openvino_genai_import"),
        "openvino_available_devices": report.get("openvino_available_devices") or [],
        "npu_device_available": bool(report.get("npu_device_available")),
        "micro_task_performed": bool(report.get("python_starts") or report.get("openvino_import") or report.get("openvino_available_devices")),
        "errors": report.get("errors") or [],
        "warnings": report.get("warnings") or [],
    }


def build_npu_role_response(request_input: str, micro: dict[str, Any]) -> dict[str, Any]:
    classification = classify_request(request_input)
    performed = bool(micro.get("micro_task_performed"))
    devices = micro.get("openvino_available_devices") or []
    npu_available = bool(micro.get("npu_device_available"))
    mode = str(micro.get("mode") or "unknown")
    errors = micro.get("errors") if isinstance(micro.get("errors"), list) else []
    warnings = micro.get("warnings") if isinstance(micro.get("warnings"), list) else []

    if not performed:
        decision = "blocked_micro_task"
        text = f"NPU micro-task non eseguita: mode={mode}, errors={len(errors)}, warnings={len(warnings)}."
    elif classification == "casual_greeting":
        decision = "no_micro_action_for_greeting"
        text = (
            f"NPU micro-task eseguita: mode={mode}, devices={devices}, npu_available={npu_available}. "
            "Ruolo: audit leggero; per un saluto casuale non serve azione NPU aggiuntiva."
        )
    elif classification in {"debug_request", "repo_work_request"}:
        decision = "micro_audit_available"
        text = (
            f"NPU micro-task eseguita: mode={mode}, devices={devices}, npu_available={npu_available}. "
            "Ruolo: companion lane disponibile per audit leggero del contesto e dei guardrail."
        )
    else:
        decision = "micro_observation_available"
        text = (
            f"NPU micro-task eseguita: mode={mode}, devices={devices}, npu_available={npu_available}. "
            "Ruolo: contributo di audit leggero disponibile per la sintesi GPU1."
        )

    return {
        "request_classification": classification,
        "role_decision": decision,
        "micro_task_used": "Tools.npu.npu_runtime.npu_preflight",
        "micro_task_result_summary": text,
        "response_text": text,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--request", default="", help="Optional heap request observed by NPU micro-task lane.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--max-context-chars", type=int, default=4000)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    task_path = repo_root / args.task_file if args.task_file else None
    task_preview = ""
    if task_path and task_path.is_file():
        task_preview = task_path.read_text(encoding="utf-8", errors="replace")[: args.max_context_chars]
    request_input = str(args.request or "").strip()
    micro_task = run_npu_micro_task(args.timeout_seconds)
    role_response = build_npu_role_response(request_input, micro_task)
    response_text = role_response["response_text"]

    report = {
        "kind": "npu_micro_task_companion_report",
        "schema_version": 2,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": True,
        "mode": "report_only",
        "timeout_seconds": args.timeout_seconds,
        "task_file": args.task_file,
        "task_preview_chars": len(task_preview),
        "request_input": request_input,
        "response_text": response_text,
        "request_classification": role_response["request_classification"],
        "role_decision": role_response["role_decision"],
        "micro_task_used": role_response["micro_task_used"],
        "micro_task_result_summary": role_response["micro_task_result_summary"],
        "npu_micro_task": micro_task,
        "npu_peer_activity_requested": True,
        "npu_peer_activity_performed": bool(micro_task.get("micro_task_performed")),
        "npu_device_execution_performed": bool(micro_task.get("npu_device_available")),
        "npu_provider_execution_performed": False,
        "npu_activity_classification": role_response["role_decision"],
        "npu_activity_limit": "NPU lane executes a bounded OpenVINO/NPU preflight micro-task; model generation remains disabled unless explicitly introduced by a future provider contract.",
        "recommendations": [
            {
                "id": "npu_companion_policy",
                "summary": response_text,
                "classification": "SAFE_MECHANICAL",
            }
        ],
        "guardrails": {
            "legacy_npu_auditor_used": False,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "git_write_performed": False,
            "blender_runtime_execution_performed": False,
            "ffmpeg_runtime_execution_performed": False,
        },
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# NPU Micro-task Companion Report",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Mode: `{report['mode']}`",
        f"- NPU peer activity requested: `{report['npu_peer_activity_requested']}`",
        f"- NPU peer activity performed: `{report['npu_peer_activity_performed']}`",
        f"- NPU device execution performed: `{report['npu_device_execution_performed']}`",
        f"- NPU provider execution performed: `{report['npu_provider_execution_performed']}`",
        f"- NPU activity classification: `{report['npu_activity_classification']}`",
        f"- Request input: `{report['request_input']}`",
        f"- Response text: {report['response_text']}",
        f"- NPU activity limit: {report['npu_activity_limit']}",
        f"- Legacy NPU auditor used: `{report['guardrails']['legacy_npu_auditor_used']}`",
        f"- Provider execution performed: `{report['guardrails']['provider_execution_performed']}`",
        "",
        "## Recommendation",
        "",
        report["recommendations"][0]["summary"],
    ]
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": True, "output": str(output), "markdown_output": str(markdown)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
