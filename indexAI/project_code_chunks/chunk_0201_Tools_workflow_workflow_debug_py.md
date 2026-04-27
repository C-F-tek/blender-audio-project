# Project Code Chunk 201/212

- File: `Tools/workflow/workflow_debug.py`
- Part: `1`
- Lines: `1-271`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `argparse`, `json`, `os`, `shutil`, `subprocess`, `time`, `workflow_state`
- Functions: `_iso_to_dt(value)` line 15; `_format_age(seconds)` line 24; `_format_size(size)` line 37; `_read_json(path)` line 48; `read_events(max_events)` line 57; `detect_active_operation(events)` line 75; `_tail_non_empty(path, max_lines)` line 116; `_write_probe(directory)` line 126; `path_check(label, path, required, expect)` line 145; `expected_paths_for_operation(session, operation)` line 189; `collect_processes()` line 304; `collect_write_checks(probe_write)` line 338; `active_compute_processes(processes, operation)` line 361; `build_debug_report(probe_write)` line 390; `_format_check(item)` line 467; `_format_process(item)` line 475; `format_debug_report(report)` line 485; `main()` line 578

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from datetime import datetime
00004: from pathlib import Path
00005: import argparse
00006: import json
00007: import os
00008: import shutil
00009: import subprocess
00010: import time
00011: 
00012: import workflow_state as wf
00013: 
00014: 
00015: def _iso_to_dt(value: str | None) -> datetime | None:
00016:     if not value:
00017:         return None
00018:     try:
00019:         return datetime.fromisoformat(value)
00020:     except ValueError:
00021:         return None
00022: 
00023: 
00024: def _format_age(seconds: float | None) -> str:
00025:     if seconds is None:
00026:         return "-"
00027:     seconds = max(0, int(seconds))
00028:     minutes, sec = divmod(seconds, 60)
00029:     hours, minutes = divmod(minutes, 60)
00030:     if hours:
00031:         return f"{hours}h {minutes}m {sec}s"
00032:     if minutes:
00033:         return f"{minutes}m {sec}s"
00034:     return f"{sec}s"
00035: 
00036: 
00037: def _format_size(size: int | None) -> str:
00038:     if size is None:
00039:         return "-"
00040:     value = float(size)
00041:     for suffix in ["B", "KB", "MB", "GB"]:
00042:         if value < 1024 or suffix == "GB":
00043:             return f"{value:.1f} {suffix}" if suffix != "B" else f"{int(value)} B"
00044:         value /= 1024
00045:     return f"{value:.1f} GB"
00046: 
00047: 
00048: def _read_json(path: Path) -> dict | list | None:
00049:     if not path.exists():
00050:         return None
00051:     try:
00052:         return json.loads(path.read_text(encoding="utf-8"))
00053:     except Exception:
00054:         return None
00055: 
00056: 
00057: def read_events(max_events: int = 600) -> list[dict]:
00058:     if not wf.EVENT_LOG_PATH.exists():
00059:         return []
00060:     events: list[dict] = []
00061:     try:
00062:         lines = wf.EVENT_LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
00063:     except Exception:
00064:         return []
00065:     for line in lines[-max_events:]:
00066:         if not line.strip():
00067:             continue
00068:         try:
00069:             events.append(json.loads(line))
00070:         except json.JSONDecodeError:
00071:             events.append({"time": "", "operation": "log_parse", "event": "bad_json", "payload": {"raw": line[:500]}})
00072:     return events
00073: 
00074: 
00075: def detect_active_operation(events: list[dict]) -> dict:
00076:     for index in range(len(events) - 1, -1, -1):
00077:         event = events[index]
00078:         if event.get("event") != "start":
00079:             continue
00080: 
00081:         operation = str(event.get("operation") or "")
00082:         start_time = str(event.get("time") or "")
00083:         has_result = False
00084:         for later in events[index + 1 :]:
00085:             if later.get("operation") == operation and later.get("event") == "result":
00086:                 has_result = True
00087:                 break
00088:         if has_result:
00089:             continue
00090: 
00091:         start_dt = _iso_to_dt(start_time)
00092:         elapsed = (datetime.now() - start_dt).total_seconds() if start_dt else None
00093:         return {
00094:             "active": True,
00095:             "operation": operation,
00096:             "started_at": start_time,
00097:             "elapsed_sec": elapsed,
00098:             "payload": event.get("payload") or {},
00099:         }
00100: 
00101:     last_result = None
00102:     for event in reversed(events):
00103:         if event.get("event") == "result":
00104:             last_result = event
00105:             break
00106: 
00107:     return {
00108:         "active": False,
00109:         "operation": str(last_result.get("operation") if last_result else ""),
00110:         "started_at": "",
00111:         "elapsed_sec": None,
00112:         "payload": last_result.get("payload") if last_result else {},
00113:     }
00114: 
00115: 
00116: def _tail_non_empty(path: Path, max_lines: int = 8) -> list[str]:
00117:     if not path.exists() or not path.is_file():
00118:         return []
00119:     try:
00120:         lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
00121:     except Exception as exc:
00122:         return [f"<read failed: {exc}>"]
00123:     return [line.strip() for line in lines if line.strip()][-max_lines:]
00124: 
00125: 
00126: def _write_probe(directory: Path) -> tuple[bool, str]:
00127:     if not directory.exists():
00128:         return False, "directory missing"
00129:     if not directory.is_dir():
00130:         return False, "not a directory"
00131:     probe = directory / f".workflow_debug_probe_{os.getpid()}.tmp"
00132:     try:
00133:         probe.write_text("ok", encoding="utf-8")
00134:         probe.unlink(missing_ok=True)
00135:         return True, "temp write ok"
00136:     except Exception as exc:
00137:         try:
00138:             if probe.exists():
00139:                 probe.unlink()
00140:         except Exception:
00141:             pass
00142:         return False, str(exc)
00143: 
00144: 
00145: def path_check(label: str, path: Path | str, required: bool = True, expect: str = "any") -> dict:
00146:     target = Path(path)
00147:     exists = target.exists()
00148:     is_file = target.is_file()
00149:     is_dir = target.is_dir()
00150:     info: dict = {
00151:         "label": label,
00152:         "path": str(target),
00153:         "required": required,
00154:         "expect": expect,
00155:         "exists": exists,
00156:         "readable": os.access(str(target), os.R_OK) if exists else False,
00157:         "writable": os.access(str(target), os.W_OK) if exists else False,
00158:         "size": None,
00159:         "mtime": "",
00160:         "status": "OK",
00161:         "message": "",
00162:     }
00163: 
00164:     if exists:
00165:         try:
00166:             stat = target.stat()
00167:             info["size"] = int(stat.st_size) if is_file else None
00168:             info["mtime"] = datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")
00169:         except Exception as exc:
00170:             info["status"] = "WARN"
00171:             info["message"] = f"stat failed: {exc}"
00172: 
00173:     if required and not exists:
00174:         info["status"] = "MISSING"
00175:         info["message"] = "required path missing"
00176:     elif exists and expect == "file" and not is_file:
00177:         info["status"] = "WARN"
00178:         info["message"] = "expected file"
00179:     elif exists and expect == "dir" and not is_dir:
00180:         info["status"] = "WARN"
00181:         info["message"] = "expected directory"
00182:     elif not required and not exists:
00183:         info["status"] = "PENDING"
00184:         info["message"] = "not created yet"
00185: 
00186:     return info
00187: 
00188: 
00189: def expected_paths_for_operation(session: wf.WorkflowSession, operation: str) -> dict:
00190:     artifacts = session.artifacts
00191:     script = lambda name: wf.PROJECT_DIR / name
00192:     npu = lambda name: wf.NPU_DIR / name
00193: 
00194:     common_inputs = [
00195:         ("Session JSON", wf.SESSION_PATH, "file"),
00196:         ("Project root", wf.PROJECT_DIR, "dir"),
00197:         ("indexAI dir", wf.INDEX_AI_DIR, "dir"),
00198:         ("indexAI project index", wf.INDEX_AI_DIR / "project_code_index.md", "file"),
00199:         ("Output dir", wf.OUTPUT_DIR, "dir"),
00200:         ("Workflow log dir", wf.LOG_DIR, "dir"),
00201:     ]
00202: 
00203:     operation_inputs: list[tuple[str, Path | str, str]] = []
00204:     operation_outputs: list[tuple[str, Path | str, str]] = []
00205:     progress_files: list[tuple[str, Path | str, str]] = []
00206: 
00207:     if operation == "analyze_wav":
00208:         operation_inputs = [
00209:             ("Current WAV", artifacts["audio_path"], "file"),
00210:             ("analyze_wav.py", script("analyze_wav.py"), "file"),
00211:             ("Audio Python", wf.AUDIO_PYTHON, "file"),
00212:         ]
00213:         operation_outputs = [
00214:             ("Analysis JSON", artifacts["analysis_json"], "file"),
00215:             ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
00216:             ("Analysis plot PNG", artifacts["analysis_plot_png"], "file"),
00217:         ]
00218:     elif operation == "build_track_summary":
00219:         operation_inputs = [
00220:             ("Analysis JSON", artifacts["analysis_json"], "file"),
00221:             ("build_track_summary.py", script("build_track_summary.py"), "file"),
00222:         ]
00223:         operation_outputs = [("Track summary JSON", artifacts["track_summary_json"], "file")]
00224:     elif operation == "build_music_context":
00225:         operation_inputs = [
00226:             ("Analysis JSON", artifacts["analysis_json"], "file"),
00227:             ("Track summary JSON", artifacts["track_summary_json"], "file"),
00228:             ("build_music_context.py", npu("build_music_context.py"), "file"),
00229:         ]
00230:         operation_outputs = [
00231:             ("Music context JSON", artifacts["music_context_json"], "file"),
00232:             ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
00233:             ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
00234:             ("NPU music chunks", npu("npu_music_chunks"), "dir"),
00235:         ]
00236:     elif operation == "build_code_context":
00237:         operation_inputs = [
00238:             ("Project root", wf.PROJECT_DIR, "dir"),
00239:             ("build_npu_code_context.py", npu("build_npu_code_context.py"), "file"),
00240:         ]
00241:         operation_outputs = [
00242:             ("NPU code context", npu("npu_code_context.md"), "file"),
00243:             ("NPU code index", npu("npu_code_index.md"), "file"),
00244:             ("NPU code manifest", npu("npu_code_manifest.json"), "file"),
00245:             ("NPU code chunks", npu("npu_code_chunks"), "dir"),
00246:         ]
00247:     elif operation in {"build_manual_context", "ensure_manual_library"}:
00248:         operation_inputs = [
00249:             ("Manual root", wf.ROOT / "manual", "dir"),
00250:             ("build_blender_manual_context.py", npu("build_blender_manual_context.py"), "file"),
00251:         ]
00252:         operation_outputs = [
00253:             ("Manual index", npu("npu_blender_manual_index.md"), "file"),
00254:             ("Manual manifest", npu("npu_blender_manual_manifest.json"), "file"),
00255:             ("Manual chunks", npu("npu_blender_manual_chunks"), "dir"),
00256:         ]
00257:     elif operation == "dual_ai_plan":
00258:         operation_inputs = [
00259:             ("Analysis JSON", artifacts["analysis_json"], "file"),
00260:             ("Track summary JSON", artifacts["track_summary_json"], "file"),
00261:             ("Music context JSON", artifacts["music_context_json"], "file"),
00262:             ("Analysis AI context JSON", artifacts["analysis_ai_context_json"], "file"),
00263:             ("Blender keyframes JSON", artifacts["blender_keyframes_json"], "file"),
00264:             ("run_dual_ai_pipeline.py", npu("run_dual_ai_pipeline.py"), "file"),
00265:             ("NPU Python", wf.NPU_PYTHON, "file"),
00266:         ]
00267:         operation_outputs = [
00268:             ("Dual AI scene plan JSON", artifacts["dual_ai_plan_json"], "file"),
00269:             ("Dual AI Blender brief", npu("dual_ai_blender_agent_brief.md"), "file"),
00270:             ("NPU technical notes", npu("npu_dual_ai_technical_notes.md"), "file"),
00271:         ]
```
