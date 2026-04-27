# Project Code Chunk 197/212

- File: `Tools/workflow/startup_check.py`
- Part: `1`
- Lines: `1-264`

## Symbol Map
- Imports: `from __future__ import annotations`, `argparse`, `from dataclasses import asdict, dataclass`, `from datetime import datetime`, `from pathlib import Path`, `json`, `os`, `shutil`, `subprocess`, `sys`, `tempfile`, `time`
- Classes: `Check` line 31
- Functions: `now_iso()` line 38; `add(checks, name, status, detail, path)` line 42; `probe_write(path)` line 46; `run_probe(command, timeout, cwd)` line 57; `powershell_test_path(path)` line 74; `powershell_get_command(name)` line 88; `visible_path_exists(path)` line 101; `fallback_ollama_exe()` line 105; `check_python_runtime(checks, label, python_path, code, timeout)` line 129; `check_ollama(checks)` line 137; `build_report(project, root)` line 178; `format_report(report)` line 242; `save_report(report)` line 261; `main()` line 267
- Assignments: `THIS_DIR`, `PROJECT_DIR`, `ROOT`, `NPU_DIR`, `LOG_DIR`, `REPORT_JSON`, `REPORT_TXT`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: import argparse
00004: from dataclasses import asdict, dataclass
00005: from datetime import datetime
00006: from pathlib import Path
00007: import json
00008: import os
00009: import shutil
00010: import subprocess
00011: import sys
00012: import tempfile
00013: import time
00014: 
00015: 
00016: THIS_DIR = Path(__file__).resolve().parent
00017: PROJECT_DIR = THIS_DIR.parents[1]
00018: ROOT = PROJECT_DIR.parent
00019: NPU_DIR = PROJECT_DIR / "Tools" / "npu"
00020: LOG_DIR = PROJECT_DIR / "output" / "workflow_logs"
00021: REPORT_JSON = LOG_DIR / "startup_check.json"
00022: REPORT_TXT = LOG_DIR / "startup_check.txt"
00023: 
00024: if str(THIS_DIR) not in sys.path:
00025:     sys.path.insert(0, str(THIS_DIR))
00026: if str(NPU_DIR) not in sys.path:
00027:     sys.path.insert(0, str(NPU_DIR))
00028: 
00029: 
00030: @dataclass
00031: class Check:
00032:     name: str
00033:     status: str
00034:     detail: str
00035:     path: str | None = None
00036: 
00037: 
00038: def now_iso() -> str:
00039:     return datetime.now().isoformat(timespec="seconds")
00040: 
00041: 
00042: def add(checks: list[Check], name: str, status: str, detail: str, path: Path | str | None = None) -> None:
00043:     checks.append(Check(name=name, status=status, detail=detail, path=str(path) if path else None))
00044: 
00045: 
00046: def probe_write(path: Path) -> tuple[bool, str]:
00047:     try:
00048:         path.mkdir(parents=True, exist_ok=True)
00049:         fd, temp_name = tempfile.mkstemp(prefix=".spaziotempo_probe_", suffix=".tmp", dir=str(path))
00050:         os.close(fd)
00051:         Path(temp_name).unlink(missing_ok=True)
00052:         return True, "temp write ok"
00053:     except Exception as exc:
00054:         return False, str(exc)
00055: 
00056: 
00057: def run_probe(command: list[str], timeout: float = 12.0, cwd: Path | None = None) -> tuple[bool, str]:
00058:     try:
00059:         result = subprocess.run(
00060:             command,
00061:             cwd=str(cwd or PROJECT_DIR),
00062:             text=True,
00063:             stdout=subprocess.PIPE,
00064:             stderr=subprocess.STDOUT,
00065:             timeout=timeout,
00066:             check=False,
00067:         )
00068:     except Exception as exc:
00069:         return False, str(exc)
00070:     output = (result.stdout or "").strip()
00071:     return result.returncode == 0, output[-1200:] if output else f"exit={result.returncode}"
00072: 
00073: 
00074: def powershell_test_path(path: Path) -> bool:
00075:     escaped = str(path).replace("'", "''")
00076:     ok, output = run_probe(
00077:         [
00078:             "powershell",
00079:             "-NoProfile",
00080:             "-Command",
00081:             f"if (Test-Path -LiteralPath '{escaped}') {{ 'YES' }} else {{ 'NO' }}",
00082:         ],
00083:         timeout=6.0,
00084:     )
00085:     return ok and output.strip().endswith("YES")
00086: 
00087: 
00088: def powershell_get_command(name: str) -> str | None:
00089:     ok, output = run_probe(
00090:         [
00091:             "powershell",
00092:             "-NoProfile",
00093:             "-Command",
00094:             f"$cmd = Get-Command {name} -ErrorAction SilentlyContinue; if ($cmd) {{ $cmd.Source }}",
00095:         ],
00096:         timeout=6.0,
00097:     )
00098:     return output.strip() if ok and output.strip() else None
00099: 
00100: 
00101: def visible_path_exists(path: Path) -> bool:
00102:     return path.exists() or powershell_test_path(path)
00103: 
00104: 
00105: def fallback_ollama_exe() -> Path | None:
00106:     candidates = []
00107:     for env_name in ("OLLAMA_EXE",):
00108:         value = os.environ.get(env_name)
00109:         if value:
00110:             candidates.append(Path(value))
00111:     local_app = os.environ.get("LOCALAPPDATA")
00112:     user_profile = os.environ.get("USERPROFILE")
00113:     program_files = os.environ.get("ProgramFiles")
00114:     if local_app:
00115:         candidates.extend([Path(local_app) / "Programs" / "Ollama" / "ollama.exe", Path(local_app) / "Ollama" / "ollama.exe"])
00116:     if user_profile:
00117:         candidates.append(Path(user_profile) / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe")
00118:     if program_files:
00119:         candidates.append(Path(program_files) / "Ollama" / "ollama.exe")
00120:     command_path = powershell_get_command("ollama")
00121:     if command_path:
00122:         candidates.append(Path(command_path))
00123:     for candidate in candidates:
00124:         if visible_path_exists(candidate):
00125:             return candidate
00126:     return None
00127: 
00128: 
00129: def check_python_runtime(checks: list[Check], label: str, python_path: Path, code: str, timeout: float = 20.0) -> None:
00130:     if not python_path.exists():
00131:         add(checks, label, "MISS", "python.exe missing", python_path)
00132:         return
00133:     ok, output = run_probe([str(python_path), "-c", code], timeout=timeout)
00134:     add(checks, label, "OK" if ok else "WARN", output or "ok", python_path)
00135: 
00136: 
00137: def check_ollama(checks: list[Check]) -> None:
00138:     try:
00139:         from ollama_runtime import DEFAULT_BASE_URL, find_ollama_exe, is_server_ready, list_models, list_models_from_disk, start_server
00140: 
00141:         exe = find_ollama_exe() or fallback_ollama_exe()
00142:         if exe:
00143:             add(checks, "Ollama executable", "OK", str(exe), exe)
00144:         else:
00145:             add(checks, "Ollama executable", "MISS", "ollama.exe not found; set OLLAMA_EXE or restart PATH")
00146: 
00147:         ready = is_server_ready(DEFAULT_BASE_URL, timeout=2.0)
00148:         started = False
00149:         if not ready and exe:
00150:             try:
00151:                 start_server(exe, DEFAULT_BASE_URL, startup_timeout=10.0)
00152:                 ready = is_server_ready(DEFAULT_BASE_URL, timeout=2.0)
00153:                 started = ready
00154:             except Exception as exc:
00155:                 add(checks, "Ollama API autostart", "WARN", str(exc), exe)
00156: 
00157:         if ready:
00158:             models = []
00159:             try:
00160:                 models = list_models(DEFAULT_BASE_URL)
00161:             except Exception:
00162:                 models = list_models_from_disk()
00163:             detail = f"{DEFAULT_BASE_URL} UP"
00164:             if started:
00165:                 detail += " (started now)"
00166:             detail += f"; models={', '.join(models[:8]) if models else 'none'}"
00167:             add(checks, "Ollama API", "OK", detail)
00168:         else:
00169:             disk_models = list_models_from_disk()
00170:             detail = f"{DEFAULT_BASE_URL} DOWN"
00171:             if disk_models:
00172:                 detail += f"; disk models={', '.join(disk_models[:8])}"
00173:             add(checks, "Ollama API", "DOWN", detail)
00174:     except Exception as exc:
00175:         add(checks, "Ollama runtime", "WARN", str(exc))
00176: 
00177: 
00178: def build_report(project: Path = PROJECT_DIR, root: Path = ROOT) -> dict:
00179:     checks: list[Check] = []
00180: 
00181:     add(checks, "Project root", "OK" if project.exists() else "MISS", str(project), project)
00182:     add(checks, "Workflow state", "OK" if (project / "Tools" / "workflow" / "workflow_state.py").exists() else "MISS", "workflow_state.py", project / "Tools" / "workflow" / "workflow_state.py")
00183:     add(checks, "Scene brief", "OK" if (project / "Tools" / "workflow" / "scene_brief.py").exists() else "MISS", "scene_brief.py", project / "Tools" / "workflow" / "scene_brief.py")
00184: 
00185:     for name, path in [
00186:         ("Output dir", project / "output"),
00187:         ("Workflow logs", project / "output" / "workflow_logs"),
00188:         ("indexAI", project / "indexAI"),
00189:         ("Manual library", root / "manual"),
00190:         ("Renders dir", root / "renders"),
00191:     ]:
00192:         ok, detail = probe_write(path) if name != "Manual library" else (path.exists(), "read-only library present" if path.exists() else "missing")
00193:         add(checks, name, "OK" if ok else "WARN", detail, path)
00194: 
00195:     check_ollama(checks)
00196: 
00197:     npu_python = root / "venvs" / "blender-npu-ai" / "Scripts" / "python.exe"
00198:     audio_python = root / "venvs" / "blender-audio-ai" / "Scripts" / "python.exe"
00199:     check_python_runtime(
00200:         checks,
00201:         "NPU/OpenVINO runtime",
00202:         npu_python,
00203:         "import json; import openvino as ov; print(json.dumps({'devices': list(ov.Core().available_devices)}))",
00204:         timeout=25.0,
00205:     )
00206:     check_python_runtime(
00207:         checks,
00208:         "Audio analysis runtime",
00209:         audio_python,
00210:         "import librosa, numpy, matplotlib; print('audio deps ok')",
00211:         timeout=25.0,
00212:     )
00213: 
00214:     ffmpeg = shutil.which("ffmpeg") or powershell_get_command("ffmpeg")
00215:     ffprobe = shutil.which("ffprobe") or powershell_get_command("ffprobe")
00216:     add(checks, "ffmpeg", "OK" if ffmpeg else "MISS", ffmpeg or "ffmpeg not in PATH", ffmpeg)
00217:     add(checks, "ffprobe", "OK" if ffprobe else "MISS", ffprobe or "ffprobe not in PATH", ffprobe)
00218: 
00219:     try:
00220:         from workflow_state import load_session, operation_status
00221: 
00222:         session = load_session(create=True)
00223:         status = operation_status(session)
00224:         add(checks, "Workflow session", "OK", f"track={session.track_stem}; chat={session.chat_model}; script_tokens={session.script_max_tokens}")
00225:         missing = [key for key, value in status.items() if key in {"analysis_json", "music_context_json", "blender_keyframes_json"} and not value]
00226:         add(checks, "Current track inputs", "OK" if not missing else "WARN", "ready" if not missing else "missing: " + ", ".join(missing))
00227:     except Exception as exc:
00228:         add(checks, "Workflow session", "WARN", str(exc))
00229: 
00230:     statuses = [item.status for item in checks]
00231:     report = {
00232:         "generated_at": now_iso(),
00233:         "project": str(project),
00234:         "root": str(root),
00235:         "ok": not any(status in {"DOWN", "MISS"} for status in statuses),
00236:         "warning_count": sum(1 for status in statuses if status in {"WARN", "DOWN", "MISS"}),
00237:         "checks": [asdict(item) for item in checks],
00238:     }
00239:     return report
00240: 
00241: 
00242: def format_report(report: dict) -> str:
00243:     lines = [
00244:         "=" * 78,
00245:         "SPAZIOTEMPO STARTUP SERVICE CHECK",
00246:         "=" * 78,
00247:         f"Generated: {report.get('generated_at')}",
00248:         f"Project:   {report.get('project')}",
00249:         f"Root:      {report.get('root')}",
00250:         "",
00251:     ]
00252:     for item in report.get("checks", []):
00253:         path = f" | {item.get('path')}" if item.get("path") else ""
00254:         lines.append(f"[{item.get('status')}] {item.get('name')}: {item.get('detail')}{path}")
00255:     lines.append("")
00256:     lines.append(f"Warnings: {report.get('warning_count', 0)}")
00257:     lines.append(f"Report:   {REPORT_JSON}")
00258:     return "\n".join(lines)
00259: 
00260: 
00261: def save_report(report: dict) -> None:
00262:     LOG_DIR.mkdir(parents=True, exist_ok=True)
00263:     REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
00264:     REPORT_TXT.write_text(format_report(report), encoding="utf-8")
```
