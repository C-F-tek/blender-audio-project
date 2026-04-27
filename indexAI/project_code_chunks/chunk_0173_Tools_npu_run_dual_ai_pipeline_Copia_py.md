# Project Code Chunk 173/212

- File: `Tools/npu/run_dual_ai_pipeline - Copia.py`
- Part: `1`
- Lines: `1-264`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `sys`, `from datetime import datetime`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 38; `read_json(path)` line 42; `write_json(path, data)` line 47; `validate_input_files(args)` line 52; `looks_degraded_text(text)` line 72; `deterministic_technical_notes(music_context, project_manifest, reason)` line 85; `run_npu_technical_pass(args)` line 134; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 178; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 254; `build_implementation_prompt(plan, npu_notes, include_manual)` line 305; `safe_parse_json(text, fallback_key)` line 373; `write_brief(plan, creative, technical, npu_notes)` line 380; `validate_implementation_draft(draft)` line 403; `write_implementation_draft(draft)` line 450; `main()` line 478
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import argparse
00005: import json
00006: import subprocess
00007: import sys
00008: from datetime import datetime
00009: 
00010: from build_music_context import build_music_context
00011: from build_npu_code_context import main as build_code_context
00012: from build_blender_manual_context import build_manual_context
00013: from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index
00014: from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report
00015: from ollama_runtime import OllamaModelManager, parse_json_response
00016: from run_ollama_music_agent import build_prompt as build_music_prompt
00017: from run_ollama_music_agent import markdown_from_insights
00018: 
00019: 
00020: ROOT = Path(__file__).resolve().parents[2]
00021: TOOLS_DIR = ROOT / "Tools" / "npu"
00022: OUTPUT_DIR = ROOT / "output"
00023: 
00024: TRACK_STEM = "Feel The Light-Luca Vera_Master"
00025: MUSIC_AI_CONTEXT = OUTPUT_DIR / f"{TRACK_STEM}_analysis_ai_context.json"
00026: DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
00027: DUAL_BRIEF_MD = TOOLS_DIR / "dual_ai_blender_agent_brief.md"
00028: OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
00029: OLLAMA_INSIGHTS_MD = TOOLS_DIR / "ollama_music_insights.md"
00030: NPU_TECH_MD = TOOLS_DIR / "npu_dual_ai_technical_notes.md"
00031: NPU_PREFLIGHT_JSON = TOOLS_DIR / "npu_preflight_report.json"
00032: IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"
00033: IMPLEMENTATION_SCRIPT = TOOLS_DIR / "generated_blender_script_candidate.py"
00034: IMPLEMENTATION_NOTES = TOOLS_DIR / "generated_implementation_notes.md"
00035: NPU_IMPLEMENTATION_NOTES = TOOLS_DIR / "npu_dual_ai_implementation_notes.md"
00036: 
00037: 
00038: def read_text(path: Path) -> str:
00039:     return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
00040: 
00041: 
00042: def read_json(path: Path) -> dict:
00043:     with open(path, "r", encoding="utf-8") as handle:
00044:         return json.load(handle)
00045: 
00046: 
00047: def write_json(path: Path, data: dict) -> None:
00048:     path.parent.mkdir(parents=True, exist_ok=True)
00049:     path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
00050: 
00051: 
00052: def validate_input_files(args: argparse.Namespace) -> None:
00053:     required = [
00054:         ("analysis JSON", Path(args.analysis)),
00055:         ("track summary JSON", Path(args.track_summary)),
00056:         ("compact music context JSON", Path(args.compact_json)),
00057:         ("analysis AI context JSON", Path(args.analysis_ai_context)),
00058:         ("full Blender keyframes JSON", Path(args.blender_keyframes_json)),
00059:     ]
00060:     if args.phase == "implementation":
00061:         required.append(("dual AI scene plan JSON", DUAL_PLAN_JSON))
00062: 
00063:     missing = [f"{label}: {path}" for label, path in required if not path.exists()]
00064:     if missing:
00065:         raise FileNotFoundError(
00066:             "Prerequisiti mancanti per la pipeline AI:\n"
00067:             + "\n".join(f"- {item}" for item in missing)
00068:             + "\nEsegui/rigenera analysis, track summary, music context e piano prima del draft."
00069:         )
00070: 
00071: 
00072: def looks_degraded_text(text: str) -> bool:
00073:     stripped = text.strip()
00074:     if len(stripped) < 260:
00075:         return True
00076:     alnum = sum(ch.isalnum() for ch in stripped)
00077:     visible = sum(not ch.isspace() for ch in stripped)
00078:     if visible and alnum / visible < 0.45:
00079:         return True
00080:     markdown_heads = stripped.count("##")
00081:     useful_words = sum(stripped.lower().count(word) for word in ["audio", "blender", "segment", "material", "fog", "light", "mesh"])
00082:     return markdown_heads < 2 and useful_words < 5
00083: 
00084: 
00085: def deterministic_technical_notes(music_context: dict, project_manifest: dict, reason: str) -> str:
00086:     summary = music_context.get("analysis_summary") or {}
00087:     track_summary = music_context.get("track_summary") or {}
00088:     segments = music_context.get("segments") or []
00089:     files = project_manifest.get("files") or []
00090:     priority_files = [
00091:         item.get("file")
00092:         for item in files
00093:         if item.get("file", "").endswith((
00094:             "Scripting/v61b/config.py",
00095:             "Scripting/v61b/materials.py",
00096:             "Scripting/v61b/fog_dynamics.py",
00097:             "Scripting/v61b/physics_setup.py",
00098:             "Scripting/v61b/scene_tuning_panel.py",
00099:             "Tools/workflow/workflow_state.py",
00100:             "Tools/npu/run_dual_ai_pipeline.py",
00101:         ))
00102:     ]
00103: 
00104:     lines = [
00105:         "# Deterministic Technical Notes\n\n",
00106:         f"Reason: NPU output was not trusted (`{reason}`).\n\n",
00107:         "## Track Map\n",
00108:         f"- Duration: `{summary.get('duration_sec', track_summary.get('duration_sec', '?'))}` seconds.\n",
00109:         f"- FPS: `{summary.get('fps', track_summary.get('fps', '?'))}`.\n",
00110:         f"- BPM: `{summary.get('estimated_tempo_bpm', track_summary.get('estimated_tempo_bpm', '?'))}`.\n",
00111:         f"- Segment count: `{len(segments)}`.\n\n",
00112:         "## Project Primary Files\n",
00113:     ]
00114:     for file_name in priority_files[:20]:
00115:         lines.append(f"- `{file_name}`\n")
00116: 
00117:     lines.extend(
00118:         [
00119:             "\n## Safe Implementation Policy\n",
00120:             "- Use full frame-by-frame Blender keyframe JSON as data input only.\n",
00121:             "- Generate patch plans against existing project files, not monolithic replacement scripts.\n",
00122:             "- Prefer hotpatch/panel/update modules for materials, fog, lights and render changes.\n",
00123:             "- Require a reload only when primary object creation or scene topology changes.\n\n",
00124:             "## Audio Control Map\n",
00125:             "- Low band: hero mesh deformation scale, gravity/attractor strength, fog density body.\n",
00126:             "- Mid band: material roughness/emission mix, secondary object motion, fog filament drift.\n",
00127:             "- High band: small emission accents, glints, particle sparkle, sharp camera micro motion.\n",
00128:             "- Onset/beat: short impulses, never a constant global light flash.\n\n",
00129:         ]
00130:     )
00131:     return "".join(lines)
00132: 
00133: 
00134: def run_npu_technical_pass(args: argparse.Namespace) -> str:
00135:     script = TOOLS_DIR / "run_npu_review.py"
00136:     python_exe = Path(args.npu_python)
00137:     cmd = [
00138:         str(python_exe),
00139:         str(script),
00140:         "--engine",
00141:         "npu",
00142:         "--domain",
00143:         "music",
00144:         "--mode",
00145:         "chunked",
00146:         "--context",
00147:         str(TOOLS_DIR / "npu_music_context.md"),
00148:         "--chunk-dir",
00149:         str(TOOLS_DIR / "npu_music_chunks"),
00150:         "--out",
00151:         str(NPU_TECH_MD),
00152:         "--notes-out",
00153:         str(TOOLS_DIR / "npu_dual_ai_chunk_notes.md"),
00154:         "--max-context-chars",
00155:         "0",
00156:         "--chunk-chars",
00157:         "10500",
00158:         "--chunk-overlap-chars",
00159:         "700",
00160:         "--max-prompt-chars",
00161:         "15000",
00162:         "--max-chunk-tokens",
00163:         str(args.npu_chunk_tokens),
00164:         "--max-reduce-tokens",
00165:         str(args.npu_reduce_tokens),
00166:         "--max-new-tokens",
00167:         str(args.npu_final_tokens),
00168:         "--max-prompt-len",
00169:         "16384",
00170:         "--min-response-len",
00171:         "64",
00172:     ]
00173: 
00174:     subprocess.run(cmd, check=True)
00175:     return read_text(NPU_TECH_MD)
00176: 
00177: 
00178: def build_creative_scene_prompt(music_context: dict, npu_notes: str, project_index: str) -> str:
00179:     compact = {
00180:         "analysis_summary": music_context.get("analysis_summary"),
00181:         "track_summary": music_context.get("track_summary"),
00182:         "scene_summaries": music_context.get("scene_summaries"),
00183:         "segments": [
00184:             {
00185:                 "index": segment.get("index"),
00186:                 "start_sec": segment.get("start_sec"),
00187:                 "end_sec": segment.get("end_sec"),
00188:                 "dominant_band": segment.get("dominant_band"),
00189:                 "intensity": segment.get("intensity"),
00190:                 "intensity_score": segment.get("intensity_score"),
00191:                 "controls": segment.get("controls"),
00192:                 "top_events": segment.get("top_events", [])[:6],
00193:             }
00194:             for segment in music_context.get("segments", [])
00195:         ],
00196:         "npu_technical_notes": npu_notes[:18000],
00197:         "primary_project_index": project_index[:14000],
00198:     }
00199:     payload = json.dumps(compact, indent=2, ensure_ascii=False)
00200:     return f"""
00201: Sei il generatore creativo locale per una scena Blender audio-reactive.
00202: 
00203: Hai un contesto musicale compatto, scene JSON esistenti e note tecniche NPU.
00204: Devi proporre una scena piu ricca SENZA cambiare direttamente codice Blender.
00205: Il codice reale del progetto e' la fonte primaria: rispetta file, moduli e funzioni esistenti.
00206: Il JSON full frame per Blender deve restare completo e invariato.
00207: 
00208: Rispondi SOLO con JSON valido.
00209: 
00210: Schema richiesto:
00211: {{
00212:   "creative_intent": "...",
00213:   "visual_language": {{
00214:     "background": "...",
00215:     "hero": "...",
00216:     "fog": "...",
00217:     "materials": "...",
00218:     "lights": "...",
00219:     "physics": "..."
00220:   }},
00221:   "scene_layers": [
00222:     {{
00223:       "layer": "Hero",
00224:       "objects": ["..."],
00225:       "audio_drivers": ["low", "mid", "high", "onset", "beat"],
00226:       "implementation_hint": "..."
00227:     }}
00228:   ],
00229:   "segment_variations": [
00230:     {{
00231:       "segment": 1,
00232:       "time_range": "0.0-16.0",
00233:       "variation": "...",
00234:       "material_modulation": "...",
00235:       "fog_modulation": "...",
00236:       "light_modulation": "...",
00237:       "camera_modulation": "..."
00238:     }}
00239:   ],
00240:   "render_safety": {{
00241:     "heavy_features_to_avoid": ["..."],
00242:     "fast_preview_strategy": "...",
00243:     "final_strategy": "..."
00244:   }},
00245:   "json_outputs_to_create": ["..."],
00246:   "do_not_touch": ["full analysis frame JSON", "..."]
00247: }}
00248: 
00249: CONTESTO:
00250: {payload}
00251: """.strip()
00252: 
00253: 
00254: def build_merge_prompt(music_context: dict, npu_notes: str, creative: dict, technical: dict) -> str:
00255:     payload = {
00256:         "music_summary": music_context.get("analysis_summary"),
00257:         "npu_technical_notes": npu_notes[:14000],
00258:         "primary_project_index": read_text(PROJECT_INDEX_MD)[:12000],
00259:         "ollama_creative": creative,
00260:         "ollama_technical": technical,
00261:     }
00262:     return f"""
00263: Sei l'orchestratore finale NPU+Ollama per Blender.
00264: 
```
