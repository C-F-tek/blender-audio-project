# Project Code Chunk 114/212

- File: `Tools/npu/build_ai_service_packet.py`
- Part: `1`
- Lines: `1-235`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `argparse`, `hashlib`, `json`, `re`, `from typing import Any`
- Functions: `slugify(value, max_len)` line 20; `read_json(path)` line 25; `sha256_file(path)` line 33; `safe_float(value, default)` line 43; `top_project_files(manifest)` line 50; `role_for_file(file_name)` line 83; `compact_segments(music_context, limit)` line 102; `build_ai_service_packet(track_stem, analysis_path, track_summary_path, music_context_path, analysis_ai_context_path, blender_keyframes_path, dual_plan_path, npu_notes, npu_status, scene_brief, asset_inventory)` line 138; `format_capsule_md(capsule)` line 305; `main()` line 325
- Assignments: `ROOT`, `OUTPUT_DIR`, `INDEX_AI_DIR`, `PATCH_LIBRARY_DIR`, `SCENE_SCRIPTS_DIR`, `PROJECT_MANIFEST_JSON`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from datetime import datetime
00004: from pathlib import Path
00005: import argparse
00006: import hashlib
00007: import json
00008: import re
00009: from typing import Any
00010: 
00011: 
00012: ROOT = Path(__file__).resolve().parents[2]
00013: OUTPUT_DIR = ROOT / "output"
00014: INDEX_AI_DIR = ROOT / "indexAI"
00015: PATCH_LIBRARY_DIR = INDEX_AI_DIR / "patch_library"
00016: SCENE_SCRIPTS_DIR = INDEX_AI_DIR / "scene_scripts"
00017: PROJECT_MANIFEST_JSON = INDEX_AI_DIR / "project_code_manifest.json"
00018: 
00019: 
00020: def slugify(value: str, max_len: int = 72) -> str:
00021:     slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
00022:     return slug[:max_len] or "track"
00023: 
00024: 
00025: def read_json(path: Path) -> dict[str, Any]:
00026:     if not path.exists():
00027:         return {}
00028:     with path.open("r", encoding="utf-8") as handle:
00029:         data = json.load(handle)
00030:     return data if isinstance(data, dict) else {}
00031: 
00032: 
00033: def sha256_file(path: Path) -> str:
00034:     if not path.exists() or not path.is_file():
00035:         return ""
00036:     digest = hashlib.sha256()
00037:     with path.open("rb") as handle:
00038:         for chunk in iter(lambda: handle.read(1024 * 1024), b""):
00039:             digest.update(chunk)
00040:     return digest.hexdigest()
00041: 
00042: 
00043: def safe_float(value: Any, default: float = 0.0) -> float:
00044:     try:
00045:         return round(float(value), 4)
00046:     except Exception:
00047:         return default
00048: 
00049: 
00050: def top_project_files(manifest: dict[str, Any]) -> list[dict[str, Any]]:
00051:     priority = (
00052:         "Scripting/v61b/config.py",
00053:         "Scripting/v61b/main_v61b.py",
00054:         "Scripting/v61b/animation.py",
00055:         "Scripting/v61b/materials.py",
00056:         "Scripting/v61b/fog_dynamics.py",
00057:         "Scripting/v61b/fog_filaments.py",
00058:         "Scripting/v61b/physics_setup.py",
00059:         "Scripting/v61b/render_setup.py",
00060:         "Scripting/v61b/scene_tuning_panel.py",
00061:         "Scripting/v61b/hot_update_scene_v61b.py",
00062:         "Tools/workflow/workflow_state.py",
00063:         "Tools/npu/run_dual_ai_pipeline.py",
00064:     )
00065:     files = {item.get("file"): item for item in manifest.get("files", []) if item.get("file")}
00066:     selected = []
00067:     for index, file_name in enumerate(priority, 1):
00068:         item = files.get(file_name)
00069:         if not item:
00070:             continue
00071:         selected.append(
00072:             {
00073:                 "id": f"F{index:03d}",
00074:                 "file": file_name,
00075:                 "lines": item.get("lines"),
00076:                 "sha": str(item.get("sha256", ""))[:12],
00077:                 "role": role_for_file(file_name),
00078:             }
00079:         )
00080:     return selected
00081: 
00082: 
00083: def role_for_file(file_name: str) -> str:
00084:     name = Path(file_name).name
00085:     roles = {
00086:         "config.py": "CFG profile/path/render/audio constants",
00087:         "main_v61b.py": "MAIN build orchestration",
00088:         "animation.py": "ANIM keyframes/audio driven transforms",
00089:         "materials.py": "MAT shader/node/material setup",
00090:         "fog_dynamics.py": "FOG audio reactive volume controls",
00091:         "fog_filaments.py": "FOG_FILAMENT procedural fog strands",
00092:         "physics_setup.py": "PHYS orbit/force/particle setup",
00093:         "render_setup.py": "RENDER compositor/quality profiles",
00094:         "scene_tuning_panel.py": "PANEL Blender UI/operators",
00095:         "hot_update_scene_v61b.py": "HOT_UPDATE partial scene refresh",
00096:         "workflow_state.py": "WF shell/GUI operation orchestration",
00097:         "run_dual_ai_pipeline.py": "AI_PIPELINE NPU/GPU routing",
00098:     }
00099:     return roles.get(name, "PROJECT source")
00100: 
00101: 
00102: def compact_segments(music_context: dict[str, Any], limit: int = 32) -> list[dict[str, Any]]:
00103:     segments = music_context.get("segments") or []
00104:     compact = []
00105:     for segment in segments[:limit]:
00106:         controls = segment.get("controls") or {}
00107:         compact.append(
00108:             {
00109:                 "id": f"S{int(segment.get('index', len(compact) + 1)):03d}",
00110:                 "t": [safe_float(segment.get("start_sec")), safe_float(segment.get("end_sec"))],
00111:                 "b": segment.get("dominant_band"),
00112:                 "i": segment.get("intensity"),
00113:                 "score": safe_float(segment.get("intensity_score")),
00114:                 "beats": int(segment.get("beat_count") or 0),
00115:                 "ctl": {
00116:                     "hero": safe_float(controls.get("hero_deformation")),
00117:                     "mat": safe_float(controls.get("material_shimmer")),
00118:                     "fog": safe_float(controls.get("fog_motion")),
00119:                     "emit": safe_float(controls.get("accent_emission")),
00120:                     "cam": safe_float(controls.get("camera_pressure")),
00121:                 },
00122:                 "evt": [
00123:                     {
00124:                         "t": safe_float(event.get("time")),
00125:                         "lo": safe_float(event.get("low")),
00126:                         "mi": safe_float(event.get("mid")),
00127:                         "hi": safe_float(event.get("high")),
00128:                         "on": safe_float(event.get("onset")),
00129:                         "bt": safe_float(event.get("beat")),
00130:                     }
00131:                     for event in (segment.get("top_events") or [])[:3]
00132:                 ],
00133:             }
00134:         )
00135:     return compact
00136: 
00137: 
00138: def build_ai_service_packet(
00139:     track_stem: str,
00140:     analysis_path: Path,
00141:     track_summary_path: Path,
00142:     music_context_path: Path,
00143:     analysis_ai_context_path: Path,
00144:     blender_keyframes_path: Path,
00145:     dual_plan_path: Path | None = None,
00146:     npu_notes: str = "",
00147:     npu_status: str = "service_packet",
00148:     scene_brief: dict[str, Any] | None = None,
00149:     asset_inventory: dict[str, Any] | None = None,
00150: ) -> dict[str, Any]:
00151:     PATCH_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
00152:     slug = slugify(track_stem)
00153: 
00154:     music_context = read_json(music_context_path)
00155:     ai_context = read_json(analysis_ai_context_path)
00156:     track_summary = read_json(track_summary_path)
00157:     project_manifest = read_json(PROJECT_MANIFEST_JSON)
00158:     dual_plan = read_json(dual_plan_path) if dual_plan_path else {}
00159:     scene_brief = scene_brief or {}
00160:     asset_inventory = asset_inventory or {}
00161: 
00162:     meta = (ai_context.get("analysis_summary") or {}).get("meta") or {}
00163:     overall = (ai_context.get("analysis_summary") or {}).get("overall_stats") or {}
00164:     ai_memory_context = music_context.get("ai_memory_context") or ai_context.get("ai_memory_context") or {}
00165:     project_awareness = ai_memory_context.get("project_awareness") or {}
00166: 
00167:     capsule = {
00168:         "format": "SPAZIOTEMPO_AI_SERVICE_CAPSULE_V1",
00169:         "generated_at": datetime.now().isoformat(timespec="seconds"),
00170:         "routing_policy": {
00171:             "heavy_reasoning": "GPU_OLLAMA",
00172:             "code_generation": "GPU_OLLAMA_SCENE_SCRIPT_WRITER",
00173:             "npu_role": "service_data_router_compact_capsule",
00174:             "npu_heavy_generation": False,
00175:             "full_keyframes_policy": "reference_only_never_compact_for_blender",
00176:             "memory_policy": "Every AI call receives compact user memory, scene brief, asset inventory and project/audio chunk references.",
00177:         },
00178:         "track": {
00179:             "stem": track_stem,
00180:             "duration": safe_float(meta.get("duration_sec", track_summary.get("duration_sec"))),
00181:             "fps": safe_float(meta.get("fps", track_summary.get("fps"))),
00182:             "bpm": safe_float(meta.get("estimated_tempo_bpm", track_summary.get("estimated_tempo_bpm"))),
00183:             "frames": (ai_context.get("analysis_summary") or {}).get("frame_count"),
00184:             "segments": len(music_context.get("segments") or []),
00185:         },
00186:         "refs": {
00187:             "analysis_json": str(analysis_path),
00188:             "track_summary_json": str(track_summary_path),
00189:             "music_context_json": str(music_context_path),
00190:             "analysis_ai_context_json": str(analysis_ai_context_path),
00191:             "full_blender_keyframes_json": str(blender_keyframes_path),
00192:             "full_blender_keyframes_sha": sha256_file(blender_keyframes_path),
00193:             "dual_plan_json": str(dual_plan_path) if dual_plan_path else "",
00194:             "project_manifest_json": str(PROJECT_MANIFEST_JSON),
00195:         },
00196:         "audio_language": {
00197:             "legend": "S{id}: t=[sec0,sec1], b=band, i=intensity, ctl={hero,mat,fog,emit,cam}, evt=top events.",
00198:             "overall": {
00199:                 "low": safe_float((overall.get("low") or {}).get("avg")),
00200:                 "mid": safe_float((overall.get("mid") or {}).get("avg")),
00201:                 "high": safe_float((overall.get("high") or {}).get("avg")),
00202:                 "onset": safe_float((overall.get("onset") or {}).get("avg")),
00203:                 "beat": safe_float((overall.get("beat") or {}).get("avg")),
00204:             },
00205:             "segments": compact_segments(music_context),
00206:         },
00207:         "director_memory": {
00208:             "scene_preferences": scene_brief.get("scene_preferences", {}),
00209:             "conversation_memory": scene_brief.get("conversation_memory", {}),
00210:             "ai_memory_context": ai_memory_context,
00211:             "project_awareness": project_awareness,
00212:             "verified_answers": project_awareness.get("verified_answers", []),
00213:             "recent_conversation": (scene_brief.get("conversation_transcript") or [])[-8:],
00214:             "must_apply": [
00215:                 "Respect user corrections from scene brief over generic defaults.",
00216:                 "Do not echo the whole brief as an answer.",
00217:                 "Use primary_ball_asset when the user says ball.",
00218:                 "For dual central ball objects, animate/deform them in counterphase using the full keyframe JSON.",
00219:             ],
00220:         },
00221:         "asset_language": {
00222:             "asset_count": asset_inventory.get("asset_count", 0),
00223:             "known_primary_assets": [
00224:                 asset
00225:                 for asset in asset_inventory.get("assets", [])
00226:                 if asset.get("role") in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}
00227:             ][:20],
00228:             "notes": asset_inventory.get("notes", []),
00229:         },
00230:         "project_language": {
00231:             "legend": "F{id}: existing source file reference; GPU may propose new draft files but must not modify these directly.",
00232:             "files": top_project_files(project_manifest),
00233:             "source_fingerprint": project_manifest.get("source_fingerprint"),
00234:         },
00235:         "style_contract": {
```
