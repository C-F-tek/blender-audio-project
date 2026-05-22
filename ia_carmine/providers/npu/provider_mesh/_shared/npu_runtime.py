from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from ia_carmine.providers.npu.paths import find_repo_root
from typing import Any

ROOT = find_repo_root(__file__)
DEFAULT_NPU_PYTHON = (
    ROOT / ".venv" / "Scripts" / "python.exe"
    if os.name == "nt"
    else ROOT / ".venv" / "bin" / "python"
)
DEFAULT_MODEL_DIR = Path(
    os.environ.get(
        "SPAZIOTEMPO_NPU_MODEL_DIR",
        Path.home() / "blender" / "npu-models" / "Phi-3.5-mini-instruct-int4-cw-ov",
    )
)
DEFAULT_TIMEOUT_SEC = float(os.environ.get("SPAZIOTEMPO_NPU_PREFLIGHT_TIMEOUT", "30"))


def resolve_project_python(repo_root: Path | None = None) -> Path:
    # Resolve the project Python required by IA-Carmine runtime policy.
    # The NPU lane must not silently fall back to a system Python or a user-level
    # virtualenv. Runtime callers may pass an explicit Python executable;
    # otherwise the repository `.venv` is authoritative.
    root = Path(repo_root or ROOT).resolve()
    if os.name == "nt":
        candidate = root / ".venv" / "Scripts" / "python.exe"
    else:
        candidate = root / ".venv" / "bin" / "python"
    return candidate


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run_python(
    python_exe: Path, code: str, timeout: float = DEFAULT_TIMEOUT_SEC
) -> tuple[bool, str, int | None]:
    hard_timeout = None if float(timeout or 0) <= 0 else timeout
    try:
        result = subprocess.run(
            [str(python_exe), "-c", code],
            capture_output=True,
            text=True,
            timeout=hard_timeout,
            check=False,
        )
    except Exception as exc:
        return False, str(exc), None

    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    text = "\n".join(item for item in [output, error] if item)
    return result.returncode == 0, text, result.returncode


def _parse_last_json_line(text: str) -> Any:
    for line in reversed((text or "").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            return json.loads(line)
        except Exception:
            continue
    return None


def npu_preflight(
    python_exe: Path | str | None = None,
    model_dir: Path | str = DEFAULT_MODEL_DIR,
    timeout: float = DEFAULT_TIMEOUT_SEC,
) -> dict[str, Any]:
    """Return a defensive OpenVINO/NPU readiness report.

    The function never raises for normal workstation/runtime problems. If the
    NPU stack is not ready, callers can continue with deterministic guardrails.
    """
    python_exe = Path(python_exe) if python_exe else resolve_project_python(ROOT)
    model_dir = Path(model_dir)

    checks: dict[str, Any] = {
        "schema_version": 2,
        "generated_at": utc_now(),
        "python_exe": str(python_exe),
        "model_dir": str(model_dir),
        "python_exists": python_exe.exists(),
        "model_dir_exists": model_dir.exists(),
        "python_starts": False,
        "python_version": None,
        "openvino_import": False,
        "openvino_genai_import": False,
        "openvino_available_devices": [],
        "npu_device_available": False,
        "ready": False,
        "mode": "heuristic_fallback",
        "recommended_workers": 1,
        "load_policy": "NPU model loading is optional; guardrail checks remain deterministic when unavailable.",
        "errors": [],
        "warnings": [],
    }

    if not checks["python_exists"]:
        checks["errors"].append(f"NPU Python not found: {python_exe}")
        checks["warnings"].append("Using deterministic heuristic guardrail fallback.")
        return checks

    ok, text, _ = _run_python(
        python_exe,
        "import json, sys; print(json.dumps({'version': sys.version.split()[0], 'executable': sys.executable}))",
        timeout=(min(timeout, 15.0) if float(timeout or 0) > 0 else 0),
    )
    checks["python_starts"] = ok
    if ok:
        parsed = _parse_last_json_line(text) or {}
        checks["python_version"] = parsed.get("version")
    else:
        checks["errors"].append(f"NPU Python does not start: {text}")
        checks["warnings"].append("Using deterministic heuristic guardrail fallback.")
        return checks

    ok, text, _ = _run_python(python_exe, "import openvino; print('openvino ok')", timeout=timeout)
    checks["openvino_import"] = ok
    if not ok:
        checks["errors"].append(f"openvino import failed: {text}")

    ok, text, _ = _run_python(
        python_exe, "import openvino_genai; print('openvino_genai ok')", timeout=timeout
    )
    checks["openvino_genai_import"] = ok
    if not ok:
        checks["warnings"].append(f"openvino_genai import failed: {text}")

    ok, text, _ = _run_python(
        python_exe,
        "import json; from openvino import Core; print(json.dumps(Core().available_devices))",
        timeout=timeout,
    )
    if ok:
        parsed = _parse_last_json_line(text)
        checks["openvino_available_devices"] = parsed if isinstance(parsed, list) else [text]
        checks["npu_device_available"] = "NPU" in checks["openvino_available_devices"]
    else:
        checks["errors"].append(f"OpenVINO device check failed: {text}")

    if not checks["model_dir_exists"]:
        checks["warnings"].append(f"NPU model dir not found: {model_dir}")

    checks["ready"] = (
        checks["python_starts"]
        and checks["openvino_import"]
        and checks["openvino_genai_import"]
        and checks["model_dir_exists"]
        and checks["npu_device_available"]
    )
    if checks["ready"]:
        checks["mode"] = "npu_ready"
        checks["recommended_workers"] = 4
    elif checks["npu_device_available"]:
        checks["mode"] = "npu_device_available_runtime_incomplete"
        checks["recommended_workers"] = 2
    else:
        checks["warnings"].append(
            "NPU device not available; guardrail service will continue in heuristic mode."
        )
    return checks


def guardrail_runtime_summary(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "ready": bool(report.get("ready")),
        "mode": report.get("mode", "unknown"),
        "npu_device_available": bool(report.get("npu_device_available")),
        "recommended_workers": int(report.get("recommended_workers") or 1),
        "error_count": len(report.get("errors") or []),
        "warning_count": len(report.get("warnings") or []),
    }


def write_npu_preflight_report(report: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
