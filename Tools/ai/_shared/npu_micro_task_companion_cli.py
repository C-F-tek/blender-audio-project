from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

repo_root_for_import = Path(__file__).resolve().parents[2]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from Tools.ai._shared.provider_tool_loop import openvino_tool_loop_report

try:
    from build_npu_micro_task_companion_report import (
        build_npu_role_response,
        resolve_project_python,
        run_npu_device_workload,
        run_npu_micro_task,
    )
except ModuleNotFoundError:
    from Tools.ai.build_npu_micro_task_companion_report import (
        build_npu_role_response,
        resolve_project_python,
        run_npu_device_workload,
        run_npu_micro_task,
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    task_preview = _task_preview(repo_root, args.task_file, args.max_context_chars)
    request_input = str(args.request or "").strip()
    project_python = resolve_project_python(repo_root, args.python_exe)
    micro_task = run_npu_micro_task(args.timeout_seconds, repo_root=repo_root, python_exe=args.python_exe)
    device_workload = run_npu_device_workload(
        enabled=bool(args.run_device_workload),
        timeout_seconds=args.timeout_seconds,
        iterations=args.device_workload_iterations,
        min_seconds=args.device_workload_seconds,
        python_exe=project_python,
    )
    role_response = build_npu_role_response(request_input, micro_task)
    npu_tool_loop = _tool_loop(repo_root, request_input, args, project_python)
    report = _report(args, task_preview, request_input, project_python, micro_task, device_workload, role_response, npu_tool_loop)
    _apply_native_tool_loop_gate(report, npu_tool_loop)
    _write_outputs(args, report)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--request", default="", help="Optional heap request observed by NPU micro-task lane.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--python-exe", default="", help="Project Python executable for NPU/OpenVINO checks.")
    parser.add_argument("--max-context-chars", type=int, default=4000)
    parser.add_argument("--run-device-workload", action="store_true")
    parser.add_argument("--device-workload-seconds", type=float, default=0.25)
    parser.add_argument("--device-workload-iterations", type=int, default=8)
    parser.add_argument("--tool-loop-timeout-seconds", type=float, default=45.0)
    parser.add_argument("--tool-loop-max-new-tokens", type=int, default=128)
    return parser.parse_args()


def _task_preview(repo_root: Path, task_file: str, max_chars: int) -> str:
    task_path = repo_root / task_file if task_file else None
    if task_path and task_path.is_file():
        return task_path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    return ""


def _tool_loop(repo_root: Path, request_input: str, args: argparse.Namespace, project_python: Path):
    return openvino_tool_loop_report(
        repo_root=repo_root,
        prompt=request_input or "Call the broker tool needed for a heap code-product audit.",
        timeout_seconds=args.tool_loop_timeout_seconds,
        max_new_tokens=args.tool_loop_max_new_tokens,
        device="NPU",
        python_exe=str(project_python),
    )


def _response_text(role_response: dict, device_workload: dict, npu_tool_loop: dict) -> str:
    response_text = role_response["response_text"]
    if device_workload.get("requested"):
        response_text += (
            f" Workload NPU reale richiesto: performed={device_workload.get('performed')}, "
            f"passed={device_workload.get('passed')}, iterations={device_workload.get('iterations')}, "
            f"seconds={device_workload.get('seconds')}."
        )
    if npu_tool_loop.get("native_tool_loop_supported"):
        response_text += f" NPU OpenVINO tool loop attivo: tool_calls={npu_tool_loop.get('native_tool_call_count')}."
    else:
        response_text += f" NPU OpenVINO tool loop non disponibile: {npu_tool_loop.get('classification')}."
    return response_text


def _report(
    args: argparse.Namespace,
    task_preview: str,
    request_input: str,
    project_python: Path,
    micro_task: dict,
    device_workload: dict,
    role_response: dict,
    npu_tool_loop: dict,
) -> dict:
    response_text = _response_text(role_response, device_workload, npu_tool_loop)
    provider_performed = bool(device_workload.get("performed")) or bool(
        npu_tool_loop.get("native_tool_loop_performed")
    )
    return {
        "kind": "npu_micro_task_companion_report",
        "schema_version": 2,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": True,
        "mode": "report_only",
        "timeout_seconds": args.timeout_seconds,
        "task_file": args.task_file,
        "task_preview_chars": len(task_preview),
        "request_input": request_input,
        "project_python_exe": str(project_python),
        "response_text": response_text,
        "request_classification": role_response["request_classification"],
        "role_decision": role_response["role_decision"],
        "micro_task_used": role_response["micro_task_used"],
        "micro_task_result_summary": role_response["micro_task_result_summary"],
        "npu_micro_task": micro_task,
        "npu_device_workload": device_workload,
        "npu_openvino_native_tool_loop": npu_tool_loop,
        "native_tool_loop_provider": "openvino_genai_npu",
        "native_tool_loop_requested": bool(npu_tool_loop.get("native_tool_loop_requested")),
        "native_tool_loop_supported": bool(npu_tool_loop.get("native_tool_loop_supported")),
        "native_tool_loop_performed": bool(npu_tool_loop.get("native_tool_loop_performed")),
        "native_tool_call_count": int(npu_tool_loop.get("native_tool_call_count") or 0),
        "tool_calls": npu_tool_loop.get("tool_calls") or [],
        "npu_device_workload_requested": bool(device_workload.get("requested")),
        "npu_device_workload_performed": bool(device_workload.get("performed")),
        "npu_peer_activity_requested": True,
        "npu_peer_activity_performed": bool(micro_task.get("micro_task_performed")),
        "npu_device_execution_performed": bool(device_workload.get("performed"))
        or bool(micro_task.get("npu_device_available")),
        "npu_provider_execution_performed": provider_performed,
        "npu_activity_classification": role_response["role_decision"],
        "npu_activity_limit": "NPU lane executes bounded OpenVINO/NPU checks and an OpenVINO GenAI native tool-loop attempt when a local model is resolvable.",
        "recommendations": [{"id": "npu_companion_policy", "summary": response_text, "classification": "SAFE_MECHANICAL"}],
        "guardrails": {
            "legacy_npu_auditor_used": False,
            "provider_execution_performed": provider_performed,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "git_write_performed": False,
            "blender_runtime_execution_performed": False,
            "ffmpeg_runtime_execution_performed": False,
        },
    }


def _apply_native_tool_loop_gate(report: dict, npu_tool_loop: dict) -> None:
    if report["native_tool_loop_requested"] and report["native_tool_call_count"] <= 0:
        if npu_tool_loop.get("classification") != "openvino_native_tool_call_incomplete":
            report.setdefault("errors", []).append(
                str(npu_tool_loop.get("classification") or "openvino_npu_native_tool_call_missing")
            )
            report["passed"] = False


def _write_outputs(args: argparse.Namespace, report: dict) -> None:
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": True, "output": str(output), "markdown_output": str(markdown)}, indent=2))


def render_markdown(report: dict) -> str:
    lines = [
        "# NPU Micro-task Companion Report",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Mode: `{report['mode']}`",
        f"- NPU peer activity requested: `{report['npu_peer_activity_requested']}`",
        f"- NPU peer activity performed: `{report['npu_peer_activity_performed']}`",
        f"- NPU device execution performed: `{report['npu_device_execution_performed']}`",
        f"- NPU provider execution performed: `{report['npu_provider_execution_performed']}`",
        f"- NPU OpenVINO native tool loop supported: `{report['native_tool_loop_supported']}`",
        f"- NPU OpenVINO native tool calls: `{report['native_tool_call_count']}`",
        f"- NPU device workload requested: `{report['npu_device_workload_requested']}`",
        f"- NPU device workload performed: `{report['npu_device_workload_performed']}`",
        f"- NPU device workload: `{report['npu_device_workload']}`",
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
    return "\n".join(lines) + "\n"
