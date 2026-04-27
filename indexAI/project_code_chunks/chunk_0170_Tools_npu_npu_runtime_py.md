# Project Code Chunk 170/212

- File: `Tools/npu/npu_runtime.py`
- Part: `1`
- Lines: `1-95`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `json`, `subprocess`
- Functions: `_run_python(python_exe, code, timeout)` line 13; `npu_preflight(python_exe, model_dir)` line 31; `write_npu_preflight_report(report, out_path)` line 93
- Assignments: `ROOT`, `DEFAULT_NPU_PYTHON`, `DEFAULT_MODEL_DIR`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import json
00005: import subprocess
00006: 
00007: 
00008: ROOT = Path(__file__).resolve().parents[2]
00009: DEFAULT_NPU_PYTHON = Path.home() / "blender" / "venvs" / "blender-npu-ai" / "Scripts" / "python.exe"
00010: DEFAULT_MODEL_DIR = Path.home() / "blender" / "npu-models" / "Phi-3.5-mini-instruct-int4-cw-ov"
00011: 
00012: 
00013: def _run_python(python_exe: Path, code: str, timeout: float = 30.0) -> tuple[bool, str]:
00014:     try:
00015:         result = subprocess.run(
00016:             [str(python_exe), "-c", code],
00017:             capture_output=True,
00018:             text=True,
00019:             timeout=timeout,
00020:             check=False,
00021:         )
00022:     except Exception as exc:
00023:         return False, str(exc)
00024: 
00025:     output = (result.stdout or "").strip()
00026:     error = (result.stderr or "").strip()
00027:     text = "\n".join(item for item in [output, error] if item)
00028:     return result.returncode == 0, text
00029: 
00030: 
00031: def npu_preflight(
00032:     python_exe: Path | str = DEFAULT_NPU_PYTHON,
00033:     model_dir: Path | str = DEFAULT_MODEL_DIR,
00034: ) -> dict:
00035:     python_exe = Path(python_exe)
00036:     model_dir = Path(model_dir)
00037: 
00038:     checks = {
00039:         "python_exe": str(python_exe),
00040:         "model_dir": str(model_dir),
00041:         "python_exists": python_exe.exists(),
00042:         "model_dir_exists": model_dir.exists(),
00043:         "python_starts": False,
00044:         "openvino_genai_import": False,
00045:         "openvino_available_devices": [],
00046:         "npu_device_available": False,
00047:         "ready": False,
00048:         "load_policy": "NPU is loaded when LLMPipeline is instantiated by run_npu_review.py.",
00049:         "errors": [],
00050:     }
00051: 
00052:     if not checks["python_exists"]:
00053:         checks["errors"].append(f"NPU Python not found: {python_exe}")
00054:         return checks
00055: 
00056:     ok, text = _run_python(python_exe, "print('ok')", timeout=15.0)
00057:     checks["python_starts"] = ok
00058:     if not ok:
00059:         checks["errors"].append(f"NPU Python does not start: {text}")
00060:         return checks
00061: 
00062:     ok, text = _run_python(python_exe, "import openvino_genai; print('openvino_genai ok')", timeout=30.0)
00063:     checks["openvino_genai_import"] = ok
00064:     if not ok:
00065:         checks["errors"].append(f"openvino_genai import failed: {text}")
00066: 
00067:     ok, text = _run_python(
00068:         python_exe,
00069:         "import json, openvino as ov; print(json.dumps(ov.Core().available_devices))",
00070:         timeout=30.0,
00071:     )
00072:     if ok:
00073:         try:
00074:             checks["openvino_available_devices"] = json.loads(text.splitlines()[-1])
00075:         except Exception:
00076:             checks["openvino_available_devices"] = [text]
00077:         checks["npu_device_available"] = "NPU" in checks["openvino_available_devices"]
00078:     else:
00079:         checks["errors"].append(f"OpenVINO device check failed: {text}")
00080: 
00081:     if not checks["model_dir_exists"]:
00082:         checks["errors"].append(f"NPU model dir not found: {model_dir}")
00083: 
00084:     checks["ready"] = (
00085:         checks["python_starts"]
00086:         and checks["openvino_genai_import"]
00087:         and checks["model_dir_exists"]
00088:         and checks["npu_device_available"]
00089:     )
00090:     return checks
00091: 
00092: 
00093: def write_npu_preflight_report(report: dict, out_path: Path) -> None:
00094:     out_path.parent.mkdir(parents=True, exist_ok=True)
00095:     out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
```
