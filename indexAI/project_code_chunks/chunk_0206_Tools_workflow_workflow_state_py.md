# Project Code Chunk 206/212

- File: `Tools/workflow/workflow_state.py`
- Part: `1`
- Lines: `1-265`

## Symbol Map
- Imports: `from __future__ import annotations`, `from dataclasses import dataclass, asdict`, `from datetime import datetime`, `from pathlib import Path`, `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `time`
- Classes: `OperationResult` line 45; `WorkflowSession` line 125 methods: default, save
- Functions: `now_iso()` line 40; `write_json(path, payload)` line 59; `append_event(operation, event, payload)` line 64; `save_operation_result(result)` line 76; `slugify(value)` line 82; `track_stem_from_wav(wav_path)` line 89; `build_artifacts(wav_path)` line 93; `load_session(create)` line 159; `set_current_wav(wav_path)` line 191; `reset_to_default_wav()` line 218; `set_debug_enabled(enabled)` line 239; `available_ollama_models()` line 248; `set_ai_models()` line 266; `python_executable()` line 297; `audio_python_executable()` line 313; `run_command(command, operation, check, echo, debug, print_output, metadata, log)` line 346; `finish_session_operation(session, operation)` line 425; `path_within(path, parent)` line 431; `is_safe_intermediate_target(path)` line 439; `cleanup_intermediate_targets(session, include_all_tracks, include_logs)` line 450; `cleanup_render_frame_targets(session)` line 565; `delete_target_set(operation, targets, session)` line 582; `human_bytes(size)` line 632; `scan_path_stats(path)` line 641; `collect_matching_files(root, patterns)` line 683; `file_set_stats(name, paths)` line 692; `build_project_storage_stats(session)` line 714; `format_project_storage_stats(stats)` line 795; `cleanup_intermediates(session, include_all_tracks, include_logs)` line 841; `cleanup_render_frames(session)` line 854; `operation_status(session)` line 859; `run_analyze_wav(session, fps, skip_music_context)` line 877; `run_track_summary(session)` line 894; `run_music_context(session, include_ollama, ollama_model)` line 912; `run_code_context(session)` line 934; `run_project_ai_index(session, force)` line 941; `run_asset_inventory(session)` line 950; `run_scene_director_brief(session)` line 968; `run_manual_index(session, limit_files)` line 1001; `ensure_manual_library(session)` line 1011; `artifact_missing(session, key)` line 1017; `ensure_ai_prerequisites(session, phase, include_manual)` line 1022; `run_dual_ai(session, phase, include_manual, skip_npu, skip_ollama, creative_model, technical_model, max_new_tokens)` line 1053; `run_full_audio_prepare(session)` line 1123
- Assignments: `ROOT`, `PROJECT_DIR`, `AUDIO_DIR`, `RENDERS_DIR`, `OUTPUT_DIR`, `TOOLS_DIR`, `NPU_DIR`, `INDEX_AI_DIR`, `SESSION_PATH`, `LOG_DIR`, `EVENT_LOG_PATH`, `LAST_RESULT_PATH`, `DEFAULT_WAV`, `DEFAULT_TRACK_STEM`, `DEFAULT_RENDER_STEM`, `DEFAULT_FRAME_PREFIX`, `NPU_PYTHON`, `AUDIO_PYTHON`, `DEFAULT_CREATIVE_MODEL`, `DEFAULT_TECHNICAL_MODEL`, `DEFAULT_CHAT_MODEL`, `DEFAULT_SCRIPT_TOKENS`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from dataclasses import dataclass, asdict
00004: from datetime import datetime
00005: from pathlib import Path
00006: import json
00007: import os
00008: import re
00009: import shutil
00010: import subprocess
00011: import sys
00012: import time
00013: 
00014: 
00015: ROOT = Path.home() / "blender"
00016: PROJECT_DIR = ROOT / "blender-audio-project"
00017: AUDIO_DIR = ROOT / "audio"
00018: RENDERS_DIR = ROOT / "renders"
00019: OUTPUT_DIR = PROJECT_DIR / "output"
00020: TOOLS_DIR = PROJECT_DIR / "Tools"
00021: NPU_DIR = TOOLS_DIR / "npu"
00022: INDEX_AI_DIR = PROJECT_DIR / "indexAI"
00023: SESSION_PATH = OUTPUT_DIR / "spaziotempo_workflow_session.json"
00024: LOG_DIR = OUTPUT_DIR / "workflow_logs"
00025: EVENT_LOG_PATH = LOG_DIR / "workflow_events.jsonl"
00026: LAST_RESULT_PATH = LOG_DIR / "last_operation_result.json"
00027: 
00028: DEFAULT_WAV = AUDIO_DIR / "Feel The Light-Luca Vera_Master.wav"
00029: DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
00030: DEFAULT_RENDER_STEM = "spaziotempo_asset_visual_v61b"
00031: DEFAULT_FRAME_PREFIX = "spaziotempo_v61b_"
00032: NPU_PYTHON = ROOT / "venvs" / "blender-npu-ai" / "Scripts" / "python.exe"
00033: AUDIO_PYTHON = ROOT / "venvs" / "blender-audio-ai" / "Scripts" / "python.exe"
00034: DEFAULT_CREATIVE_MODEL = "gpt-oss:20b"
00035: DEFAULT_TECHNICAL_MODEL = "qwen2.5-coder:14b"
00036: DEFAULT_CHAT_MODEL = "qwen2.5-coder:14b"
00037: DEFAULT_SCRIPT_TOKENS = 7000
00038: 
00039: 
00040: def now_iso() -> str:
00041:     return datetime.now().isoformat(timespec="seconds")
00042: 
00043: 
00044: @dataclass
00045: class OperationResult:
00046:     operation: str
00047:     ok: bool
00048:     started_at: str
00049:     ended_at: str
00050:     elapsed_sec: float
00051:     command: list[str] | None = None
00052:     cwd: str | None = None
00053:     returncode: int | None = None
00054:     stdout_tail: str = ""
00055:     error: str | None = None
00056:     metadata: dict | None = None
00057: 
00058: 
00059: def write_json(path: Path, payload: dict) -> None:
00060:     path.parent.mkdir(parents=True, exist_ok=True)
00061:     path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
00062: 
00063: 
00064: def append_event(operation: str, event: str, payload: dict | None = None) -> None:
00065:     LOG_DIR.mkdir(parents=True, exist_ok=True)
00066:     line = {
00067:         "time": now_iso(),
00068:         "operation": operation,
00069:         "event": event,
00070:         "payload": payload or {},
00071:     }
00072:     with EVENT_LOG_PATH.open("a", encoding="utf-8") as handle:
00073:         handle.write(json.dumps(line, ensure_ascii=False) + "\n")
00074: 
00075: 
00076: def save_operation_result(result: OperationResult) -> OperationResult:
00077:     write_json(LAST_RESULT_PATH, asdict(result))
00078:     append_event(result.operation, "result", asdict(result))
00079:     return result
00080: 
00081: 
00082: def slugify(value: str) -> str:
00083:     value = value.strip().lower()
00084:     value = re.sub(r"[^a-z0-9]+", "_", value)
00085:     value = re.sub(r"_+", "_", value).strip("_")
00086:     return value or "track"
00087: 
00088: 
00089: def track_stem_from_wav(wav_path: Path) -> str:
00090:     return wav_path.stem or DEFAULT_TRACK_STEM
00091: 
00092: 
00093: def build_artifacts(wav_path: Path | str | None = None) -> dict:
00094:     wav = Path(wav_path or DEFAULT_WAV).expanduser()
00095:     track_stem = track_stem_from_wav(wav)
00096:     is_default = track_stem == DEFAULT_TRACK_STEM
00097:     render_stem = DEFAULT_RENDER_STEM if is_default else f"spaziotempo_{slugify(track_stem)}"
00098:     frame_prefix = DEFAULT_FRAME_PREFIX if is_default else f"{slugify(track_stem)}_"
00099: 
00100:     return {
00101:         "track_stem": track_stem,
00102:         "audio_path": str(wav),
00103:         "output_dir": str(OUTPUT_DIR),
00104:         "analysis_json": str(OUTPUT_DIR / f"{track_stem}_analysis.json"),
00105:         "analysis_plot_png": str(OUTPUT_DIR / f"{track_stem}_analysis.png"),
00106:         "blender_keyframes_json": str(OUTPUT_DIR / f"{track_stem}_analysis_blender_keyframes.json"),
00107:         "track_summary_json": str(OUTPUT_DIR / f"{track_stem}_track_summary.json"),
00108:         "music_context_json": str(OUTPUT_DIR / f"{track_stem}_music_context.json"),
00109:         "analysis_ai_context_json": str(OUTPUT_DIR / f"{track_stem}_analysis_ai_context.json"),
00110:         "dual_ai_plan_json": str(OUTPUT_DIR / f"{track_stem}_dual_ai_scene_plan.json"),
00111:         "ollama_music_insights_json": str(OUTPUT_DIR / f"{track_stem}_ollama_music_insights.json"),
00112:         "ai_implementation_draft_json": str(OUTPUT_DIR / f"{track_stem}_ai_implementation_draft.json"),
00113:         "gpu_task_packet_json": str(OUTPUT_DIR / f"{track_stem}_gpu_task_packet.json"),
00114:         "scene_brief_json": str(OUTPUT_DIR / f"{track_stem}_scene_brief.json"),
00115:         "asset_inventory_json": str(OUTPUT_DIR / "spaziotempo_asset_inventory.json"),
00116:         "generated_scene_script": str(INDEX_AI_DIR / "scene_scripts" / f"{slugify(track_stem)}_scene_builder_candidate.py"),
00117:         "render_mp4": str(RENDERS_DIR / f"{render_stem}.mp4"),
00118:         "render_ffmpeg_mp4": str(RENDERS_DIR / f"{render_stem}_ffmpeg.mp4"),
00119:         "render_frames_dir": str(RENDERS_DIR / f"{render_stem}_frames"),
00120:         "render_frame_prefix": frame_prefix,
00121:     }
00122: 
00123: 
00124: @dataclass
00125: class WorkflowSession:
00126:     version: int
00127:     updated_at: str
00128:     use_session_track: bool
00129:     debug_enabled: bool
00130:     current_wav: str
00131:     track_stem: str
00132:     artifacts: dict
00133:     creative_model: str = DEFAULT_CREATIVE_MODEL
00134:     technical_model: str = DEFAULT_TECHNICAL_MODEL
00135:     chat_model: str = DEFAULT_CHAT_MODEL
00136:     script_max_tokens: int = DEFAULT_SCRIPT_TOKENS
00137:     last_operation: str | None = None
00138:     last_result_path: str | None = None
00139: 
00140:     @classmethod
00141:     def default(cls) -> "WorkflowSession":
00142:         artifacts = build_artifacts(DEFAULT_WAV)
00143:         return cls(
00144:             version=1,
00145:             updated_at=now_iso(),
00146:             use_session_track=False,
00147:             debug_enabled=False,
00148:             current_wav=str(DEFAULT_WAV),
00149:             track_stem=artifacts["track_stem"],
00150:             artifacts=artifacts,
00151:         )
00152: 
00153:     def save(self) -> None:
00154:         OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
00155:         self.updated_at = now_iso()
00156:         SESSION_PATH.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8")
00157: 
00158: 
00159: def load_session(create: bool = True) -> WorkflowSession:
00160:     if SESSION_PATH.exists():
00161:         try:
00162:             data = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
00163:             base_artifacts = build_artifacts(data.get("current_wav") or DEFAULT_WAV)
00164:             stored_artifacts = data.get("artifacts") or {}
00165:             artifacts = dict(base_artifacts)
00166:             artifacts.update({key: value for key, value in stored_artifacts.items() if value is not None})
00167:             return WorkflowSession(
00168:                 version=int(data.get("version", 1)),
00169:                 updated_at=str(data.get("updated_at") or now_iso()),
00170:                 use_session_track=bool(data.get("use_session_track", False)),
00171:                 debug_enabled=bool(data.get("debug_enabled", False)),
00172:                 current_wav=str(data.get("current_wav") or DEFAULT_WAV),
00173:                 track_stem=str(data.get("track_stem") or artifacts["track_stem"]),
00174:                 artifacts=artifacts,
00175:                 creative_model=str(data.get("creative_model") or DEFAULT_CREATIVE_MODEL),
00176:                 technical_model=str(data.get("technical_model") or DEFAULT_TECHNICAL_MODEL),
00177:                 chat_model=str(data.get("chat_model") or DEFAULT_CHAT_MODEL),
00178:                 script_max_tokens=int(data.get("script_max_tokens") or DEFAULT_SCRIPT_TOKENS),
00179:                 last_operation=data.get("last_operation"),
00180:                 last_result_path=data.get("last_result_path"),
00181:             )
00182:         except Exception:
00183:             pass
00184: 
00185:     session = WorkflowSession.default()
00186:     if create:
00187:         session.save()
00188:     return session
00189: 
00190: 
00191: def set_current_wav(wav_path: Path | str) -> WorkflowSession:
00192:     wav = Path(wav_path).expanduser().resolve()
00193:     if not wav.exists():
00194:         raise FileNotFoundError(f"WAV non trovato: {wav}")
00195:     if wav.suffix.lower() != ".wav":
00196:         raise ValueError(f"Serve un file .wav, ricevuto: {wav}")
00197: 
00198:     previous = load_session(create=False)
00199:     artifacts = build_artifacts(wav)
00200:     session = WorkflowSession(
00201:         version=1,
00202:         updated_at=now_iso(),
00203:         use_session_track=True,
00204:         debug_enabled=previous.debug_enabled,
00205:         current_wav=str(wav),
00206:         track_stem=artifacts["track_stem"],
00207:         artifacts=artifacts,
00208:         creative_model=previous.creative_model,
00209:         technical_model=previous.technical_model,
00210:         chat_model=previous.chat_model,
00211:         script_max_tokens=previous.script_max_tokens,
00212:         last_operation="set_current_wav",
00213:     )
00214:     session.save()
00215:     return session
00216: 
00217: 
00218: def reset_to_default_wav() -> WorkflowSession:
00219:     previous = load_session(create=False)
00220:     artifacts = build_artifacts(DEFAULT_WAV)
00221:     session = WorkflowSession(
00222:         version=1,
00223:         updated_at=now_iso(),
00224:         use_session_track=False,
00225:         debug_enabled=previous.debug_enabled,
00226:         current_wav=str(DEFAULT_WAV),
00227:         track_stem=artifacts["track_stem"],
00228:         artifacts=artifacts,
00229:         creative_model=previous.creative_model,
00230:         technical_model=previous.technical_model,
00231:         chat_model=previous.chat_model,
00232:         script_max_tokens=previous.script_max_tokens,
00233:         last_operation="reset_to_default_wav",
00234:     )
00235:     session.save()
00236:     return session
00237: 
00238: 
00239: def set_debug_enabled(enabled: bool) -> WorkflowSession:
00240:     session = load_session()
00241:     session.debug_enabled = bool(enabled)
00242:     session.last_operation = "set_debug_enabled"
00243:     session.save()
00244:     append_event("set_debug_enabled", "updated", {"debug_enabled": session.debug_enabled})
00245:     return session
00246: 
00247: 
00248: def available_ollama_models() -> list[str]:
00249:     npu_path = str(NPU_DIR)
00250:     if npu_path not in sys.path:
00251:         sys.path.insert(0, npu_path)
00252:     try:
00253:         from ollama_runtime import list_models, list_models_from_disk, DEFAULT_BASE_URL
00254: 
00255:         models: list[str] = []
00256:         try:
00257:             models.extend(list_models(DEFAULT_BASE_URL))
00258:         except Exception:
00259:             pass
00260:         models.extend(list_models_from_disk())
00261:         return sorted(set(model for model in models if model))
00262:     except Exception:
00263:         return sorted({DEFAULT_CREATIVE_MODEL, DEFAULT_TECHNICAL_MODEL, DEFAULT_CHAT_MODEL})
00264: 
00265: 
```
