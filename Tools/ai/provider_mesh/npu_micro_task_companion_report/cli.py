#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

try:
    from Tools.npu.provider_mesh._shared.npu_runtime import (
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
            "errors": ["Tools.npu.provider_mesh._shared.npu_runtime import unavailable"],
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
        hard_timeout = None if float(timeout_seconds or 0) <= 0 else float(timeout_seconds)
        completed = subprocess.run(
            [str(runner), "-c", child_code],
            cwd=str(Path.cwd()),
            text=True,
            capture_output=True,
            timeout=hard_timeout,
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
        "micro_task_used": "Tools.npu.provider_mesh._shared.npu_runtime.npu_preflight",
        "micro_task_result_summary": text,
        "response_text": text,
    }


def main() -> int:
    try:
        from Tools.ai._shared.npu_micro_task_companion_cli import main as cli_main
    except ModuleNotFoundError:
        from Tools.ai._shared.npu_micro_task_companion_cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
