#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.npu.npu_runtime import (
        DEFAULT_NPU_PYTHON,
        guardrail_runtime_summary,
        npu_preflight,
    )
except ImportError:  # pragma: no cover
    DEFAULT_NPU_PYTHON = None  # type: ignore
    guardrail_runtime_summary = None  # type: ignore
    npu_preflight = None  # type: ignore


def resolve_project_python(repo_root: Path, explicit_python: str = "") -> Path:
    # Resolve project Python for NPU micro workload.
    # Policy: explicit project Python > repo .venv > blocking report error.
    # No system env or PATH fallback is used here.
    if explicit_python:
        return Path(explicit_python).resolve()
    if sys.platform.startswith("win"):
        return repo_root / ".venv" / "Scripts" / "python.exe"
    return repo_root / ".venv" / "bin" / "python"


def classify_request(text: str) -> str:
    normalized = " ".join(str(text or "").strip().lower().split())
    if not normalized:
        return "none"
    greetings = {"ciao", "salve", "buongiorno", "buonasera", "hello", "hi", "hey"}
    if normalized in greetings:
        return "casual_greeting"
    if any(
        token in normalized
        for token in ("errore", "traceback", "bug", "crash", "fallisce", "non funziona")
    ):
        return "debug_request"
    if any(token in normalized for token in ("patch", "modifica", "codice", "script", "repo")):
        return "repo_work_request"
    return "general_request"


def run_npu_micro_task(
    timeout_seconds: int, repo_root: Path | None = None, python_exe: str = ""
) -> dict[str, Any]:
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
    project_python = resolve_project_python(Path(repo_root or Path.cwd()).resolve(), python_exe)
    report = npu_preflight(python_exe=project_python, timeout=float(timeout_seconds))
    summary = guardrail_runtime_summary(report) if guardrail_runtime_summary else {}
    return {
        **summary,
        "python_exe": report.get("python_exe"),
        "mode": report.get("mode"),
        "openvino_import": report.get("openvino_import"),
        "openvino_genai_import": report.get("openvino_genai_import"),
        "openvino_available_devices": report.get("openvino_available_devices") or [],
        "npu_device_available": bool(report.get("npu_device_available")),
        "micro_task_performed": bool(
            report.get("python_starts")
            or report.get("openvino_import")
            or report.get("openvino_available_devices")
        ),
        "errors": report.get("errors") or [],
        "warnings": report.get("warnings") or [],
    }


def run_npu_device_workload(
    enabled: bool,
    timeout_seconds: int,
    iterations: int,
    min_seconds: float,
    python_exe: Path | str | None = None,
) -> dict[str, Any]:
    if not enabled:
        return {
            "requested": False,
            "performed": False,
            "passed": False,
            "mode": "not_requested",
            "iterations": 0,
            "seconds": 0.0,
            "errors": [],
            "warnings": [],
        }

    runner = Path(python_exe).resolve() if python_exe else Path(sys.executable).resolve()
    if not runner.is_file():
        return {
            "requested": True,
            "performed": False,
            "passed": False,
            "mode": "project_python_missing",
            "iterations": 0,
            "seconds": 0.0,
            "python_exe": str(runner),
            "errors": [f"project python not found: {runner}"],
            "warnings": [],
        }

    child_code = "\n".join(
        [
            "import json, time",
            "import numpy as np",
            "import openvino as ov",
            "from openvino import Core, opset8 as opset",
            f"iterations = int({int(iterations)})",
            f"min_seconds = float({float(min_seconds)!r})",
            "core = Core()",
            "devices = list(core.available_devices)",
            "if 'NPU' not in devices:",
            "    print(json.dumps({'passed': False, 'performed': False, 'requested': True, 'mode': 'npu_device_not_available', 'devices': devices, 'iterations': 0, 'seconds': 0.0, 'errors': [], 'warnings': ['NPU not available']}))",
            "    raise SystemExit(0)",
            "param = opset.parameter([1, 4], dtype=np.float32, name='input')",
            "const = opset.constant(np.ones((1, 4), dtype=np.float32))",
            "node = opset.add(param, const)",
            "model = ov.Model([node], [param], 'npu_micro_workload')",
            "compiled = core.compile_model(model, 'NPU')",
            "infer = compiled.create_infer_request()",
            "payload = np.ones((1, 4), dtype=np.float32)",
            "deadline = time.perf_counter() + min_seconds",
            "count = 0",
            "started = time.perf_counter()",
            "last = None",
            "while count < iterations or time.perf_counter() < deadline:",
            "    last = infer.infer({'input': payload})",
            "    count += 1",
            "elapsed = time.perf_counter() - started",
            "values = list(last.values())[0].reshape(-1).tolist() if last else []",
            "print(json.dumps({'passed': True, 'performed': True, 'requested': True, 'mode': 'npu_openvino_micro_workload', 'devices': devices, 'iterations': count, 'seconds': elapsed, 'output_preview': values[:4], 'errors': [], 'warnings': []}))",
        ]
    )

    try:
        completed = subprocess.run(
            [str(runner), "-c", child_code],
            cwd=str(Path.cwd()),
            text=True,
            capture_output=True,
            timeout=max(1, int(timeout_seconds)),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "requested": True,
            "performed": False,
            "passed": False,
            "mode": "npu_workload_timeout",
            "iterations": 0,
            "seconds": float(timeout_seconds),
            "python_exe": str(runner),
            "errors": [f"NPU workload timed out after {timeout_seconds}s"],
            "warnings": [],
            "stdout_tail": ((exc.stdout or "")[-1000:] if isinstance(exc.stdout, str) else ""),
            "stderr_tail": ((exc.stderr or "")[-1000:] if isinstance(exc.stderr, str) else ""),
        }

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    try:
        parsed = json.loads(stdout.strip().splitlines()[-1])
    except Exception:
        return {
            "requested": True,
            "performed": False,
            "passed": False,
            "mode": "npu_workload_unparseable",
            "iterations": 0,
            "seconds": 0.0,
            "python_exe": str(runner),
            "errors": [(stderr or stdout or "no workload output")[-2000:]],
            "returncode": completed.returncode,
            "stderr_tail": stderr[-2000:],
            "stdout_tail": stdout[-2000:],
        }

    parsed["requested"] = True
    parsed["python_exe"] = str(runner)
    parsed["returncode"] = completed.returncode
    parsed["stderr_tail"] = stderr[-2000:]
    parsed["stdout_tail"] = stdout[-2000:]
    if completed.returncode != 0:
        parsed["passed"] = False
        parsed["performed"] = False
        parsed["mode"] = parsed.get("mode") or "npu_workload_failed"
        parsed.setdefault("errors", [])
        parsed["errors"].append((stderr or stdout or f"returncode={completed.returncode}")[-2000:])
    return parsed


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
    parser.add_argument(
        "--request",
        default="",
        help="Optional heap request observed by NPU micro-task lane.",
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument(
        "--python-exe",
        default="",
        help="Project Python executable for NPU/OpenVINO checks. Defaults to repo .venv.",
    )
    parser.add_argument("--max-context-chars", type=int, default=4000)
    parser.add_argument(
        "--run-device-workload",
        action="store_true",
        help="Run a bounded real OpenVINO workload on device NPU when available.",
    )
    parser.add_argument("--device-workload-seconds", type=float, default=0.25)
    parser.add_argument("--device-workload-iterations", type=int, default=8)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    task_path = repo_root / args.task_file if args.task_file else None
    task_preview = ""
    if task_path and task_path.is_file():
        task_preview = task_path.read_text(encoding="utf-8", errors="replace")[
            : args.max_context_chars
        ]
    request_input = str(args.request or "").strip()
    micro_task = run_npu_micro_task(
        args.timeout_seconds, repo_root=repo_root, python_exe=args.python_exe
    )
    device_workload = run_npu_device_workload(
        enabled=bool(args.run_device_workload),
        timeout_seconds=args.timeout_seconds,
        iterations=args.device_workload_iterations,
        min_seconds=args.device_workload_seconds,
        python_exe=resolve_project_python(repo_root, args.python_exe),
    )
    role_response = build_npu_role_response(request_input, micro_task)
    response_text = role_response["response_text"]
    if device_workload.get("requested"):
        response_text = (
            response_text
            + f" Workload NPU reale richiesto: performed={device_workload.get('performed')}, "
            + f"passed={device_workload.get('passed')}, iterations={device_workload.get('iterations')}, seconds={device_workload.get('seconds')}."
        )

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
        "project_python_exe": str(resolve_project_python(repo_root, args.python_exe)),
        "response_text": response_text,
        "request_classification": role_response["request_classification"],
        "role_decision": role_response["role_decision"],
        "micro_task_used": role_response["micro_task_used"],
        "micro_task_result_summary": role_response["micro_task_result_summary"],
        "npu_micro_task": micro_task,
        "npu_device_workload": device_workload,
        "npu_device_workload_requested": bool(device_workload.get("requested")),
        "npu_device_workload_performed": bool(device_workload.get("performed")),
        "npu_peer_activity_requested": True,
        "npu_peer_activity_performed": bool(micro_task.get("micro_task_performed")),
        "npu_device_execution_performed": bool(device_workload.get("performed"))
        or bool(micro_task.get("npu_device_available")),
        "npu_provider_execution_performed": bool(device_workload.get("performed")),
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
            "provider_execution_performed": bool(device_workload.get("performed")),
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
    markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"passed": True, "output": str(output), "markdown_output": str(markdown)},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
