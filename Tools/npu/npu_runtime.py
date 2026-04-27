from __future__ import annotations

from pathlib import Path
import json
import subprocess


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NPU_PYTHON = Path.home() / "blender" / "venvs" / "blender-npu-ai" / "Scripts" / "python.exe"
DEFAULT_MODEL_DIR = Path.home() / "blender" / "npu-models" / "Phi-3.5-mini-instruct-int4-cw-ov"


def _run_python(python_exe: Path, code: str, timeout: float = 30.0) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [str(python_exe), "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except Exception as exc:
        return False, str(exc)

    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    text = "\n".join(item for item in [output, error] if item)
    return result.returncode == 0, text


def npu_preflight(
    python_exe: Path | str = DEFAULT_NPU_PYTHON,
    model_dir: Path | str = DEFAULT_MODEL_DIR,
) -> dict:
    python_exe = Path(python_exe)
    model_dir = Path(model_dir)

    checks = {
        "python_exe": str(python_exe),
        "model_dir": str(model_dir),
        "python_exists": python_exe.exists(),
        "model_dir_exists": model_dir.exists(),
        "python_starts": False,
        "openvino_genai_import": False,
        "openvino_available_devices": [],
        "npu_device_available": False,
        "ready": False,
        "load_policy": "NPU is loaded when LLMPipeline is instantiated by run_npu_review.py.",
        "errors": [],
    }

    if not checks["python_exists"]:
        checks["errors"].append(f"NPU Python not found: {python_exe}")
        return checks

    ok, text = _run_python(python_exe, "print('ok')", timeout=15.0)
    checks["python_starts"] = ok
    if not ok:
        checks["errors"].append(f"NPU Python does not start: {text}")
        return checks

    ok, text = _run_python(python_exe, "import openvino_genai; print('openvino_genai ok')", timeout=30.0)
    checks["openvino_genai_import"] = ok
    if not ok:
        checks["errors"].append(f"openvino_genai import failed: {text}")

    ok, text = _run_python(
        python_exe,
        "import json, openvino as ov; print(json.dumps(ov.Core().available_devices))",
        timeout=30.0,
    )
    if ok:
        try:
            checks["openvino_available_devices"] = json.loads(text.splitlines()[-1])
        except Exception:
            checks["openvino_available_devices"] = [text]
        checks["npu_device_available"] = "NPU" in checks["openvino_available_devices"]
    else:
        checks["errors"].append(f"OpenVINO device check failed: {text}")

    if not checks["model_dir_exists"]:
        checks["errors"].append(f"NPU model dir not found: {model_dir}")

    checks["ready"] = (
        checks["python_starts"]
        and checks["openvino_genai_import"]
        and checks["model_dir_exists"]
        and checks["npu_device_available"]
    )
    return checks


def write_npu_preflight_report(report: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
