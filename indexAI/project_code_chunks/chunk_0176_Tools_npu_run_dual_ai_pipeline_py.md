# Project Code Chunk 176/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `1`
- Lines: `1-245`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import argparse
00005: import json
00006: import subprocess
00007: from datetime import datetime
00008: from typing import Any
00009: 
00010: from build_music_context import build_music_context
00011: from build_npu_code_context import main as build_code_context
00012: from build_blender_manual_context import build_manual_context
00013: from build_ai_service_packet import build_ai_service_packet, slugify as packet_slugify
00014: from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index
00015: from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report
00016: from ollama_runtime import OllamaModelManager, parse_json_response
00017: from run_ollama_music_agent import build_prompt as build_music_prompt
00018: from run_ollama_music_agent import markdown_from_insights
00019: 
00020: 
00021: ROOT = Path(__file__).resolve().parents[2]
00022: TOOLS_DIR = ROOT / "Tools" / "npu"
00023: OUTPUT_DIR = ROOT / "output"
00024: 
00025: DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"
00026: TRACK_STEM = DEFAULT_TRACK_STEM
00027: 
00028: MUSIC_AI_CONTEXT = OUTPUT_DIR / f"{TRACK_STEM}_analysis_ai_context.json"
00029: DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
00030: DUAL_BRIEF_MD = TOOLS_DIR / "dual_ai_blender_agent_brief.md"
00031: OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
00032: OLLAMA_INSIGHTS_MD = TOOLS_DIR / "ollama_music_insights.md"
00033: NPU_TECH_MD = TOOLS_DIR / "npu_dual_ai_technical_notes.md"
00034: NPU_PREFLIGHT_JSON = TOOLS_DIR / "npu_preflight_report.json"
00035: IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"
00036: IMPLEMENTATION_SCRIPT = TOOLS_DIR / "generated_blender_script_candidate.py"
00037: IMPLEMENTATION_NOTES = TOOLS_DIR / "generated_implementation_notes.md"
00038: NPU_IMPLEMENTATION_NOTES = TOOLS_DIR / "npu_dual_ai_implementation_notes.md"
00039: 
00040: 
00041: ALLOWED_NEW_PREFIXES = ("indexAI/scene_scripts/", "indexAI/patch_library/")
00042: PREFERRED_IMPLEMENTATION_FILES = (
00043:     "Scripting/v61b/materials.py",
00044:     "Scripting/v61b/fog_dynamics.py",
00045:     "Scripting/v61b/physics_setup.py",
00046:     "Scripting/v61b/scene_tuning_panel.py",
00047:     "Scripting/v61b/config.py",
00048:     "Scripting/v61b/render_setup.py",
00049:     "Scripting/v61b/hot_update_scene_v61b.py",
00050: )
00051: 
00052: 
00053: def read_text(path: Path) -> str:
00054:     return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
00055: 
00056: 
00057: def read_json(path: Path) -> dict[str, Any]:
00058:     with open(path, "r", encoding="utf-8") as handle:
00059:         data = json.load(handle)
00060:     return data if isinstance(data, dict) else {}
00061: 
00062: 
00063: def write_json(path: Path, data: dict[str, Any]) -> None:
00064:     path.parent.mkdir(parents=True, exist_ok=True)
00065:     path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
00066: 
00067: 
00068: def read_optional_json(path: str | Path | None) -> dict[str, Any]:
00069:     if not path:
00070:         return {}
00071:     candidate = Path(path)
00072:     if not candidate.exists():
00073:         return {}
00074:     try:
00075:         data = json.loads(candidate.read_text(encoding="utf-8"))
00076:     except Exception:
00077:         return {}
00078:     return data if isinstance(data, dict) else {}
00079: 
00080: 
00081: def update_track_paths(track_stem: str, analysis_ai_context: str | None = None) -> None:
00082:     global TRACK_STEM
00083:     global MUSIC_AI_CONTEXT, DUAL_PLAN_JSON, OLLAMA_INSIGHTS_JSON
00084:     global IMPLEMENTATION_DRAFT_JSON
00085: 
00086:     TRACK_STEM = track_stem
00087:     MUSIC_AI_CONTEXT = Path(analysis_ai_context) if analysis_ai_context else OUTPUT_DIR / f"{TRACK_STEM}_analysis_ai_context.json"
00088:     DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
00089:     OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
00090:     IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"
00091: 
00092: 
00093: def apply_default_input_paths(args: argparse.Namespace) -> None:
00094:     if args.analysis is None:
00095:         args.analysis = str(OUTPUT_DIR / f"{args.track_stem}_analysis.json")
00096:     if args.track_summary is None:
00097:         args.track_summary = str(OUTPUT_DIR / f"{args.track_stem}_track_summary.json")
00098:     if args.compact_json is None:
00099:         args.compact_json = str(OUTPUT_DIR / f"{args.track_stem}_music_context.json")
00100:     if args.analysis_ai_context is None:
00101:         args.analysis_ai_context = str(OUTPUT_DIR / f"{args.track_stem}_analysis_ai_context.json")
00102:     if args.blender_keyframes_json is None:
00103:         args.blender_keyframes_json = str(OUTPUT_DIR / f"{args.track_stem}_analysis_blender_keyframes.json")
00104: 
00105: 
00106: def validate_input_files(args: argparse.Namespace) -> None:
00107:     required = [
00108:         ("analysis JSON", Path(args.analysis)),
00109:         ("track summary JSON", Path(args.track_summary)),
00110:         ("compact music context JSON", Path(args.compact_json)),
00111:         ("analysis AI context JSON", Path(args.analysis_ai_context)),
00112:         ("full Blender keyframes JSON", Path(args.blender_keyframes_json)),
00113:     ]
00114:     if args.phase == "implementation":
00115:         required.append(("dual AI scene plan JSON", DUAL_PLAN_JSON))
00116: 
00117:     missing = [f"{label}: {path}" for label, path in required if not path.exists()]
00118:     if missing:
00119:         raise FileNotFoundError(
00120:             "Prerequisiti mancanti per la pipeline AI:\n"
00121:             + "\n".join(f"- {item}" for item in missing)
00122:             + "\nEsegui/rigenera analysis, track summary, music context e piano prima del draft."
00123:         )
00124: 
00125: 
00126: def looks_degraded_text(text: str) -> bool:
00127:     stripped = text.strip()
00128:     if len(stripped) < 260:
00129:         return True
00130:     alnum = sum(ch.isalnum() for ch in stripped)
00131:     visible = sum(not ch.isspace() for ch in stripped)
00132:     if visible and alnum / visible < 0.45:
00133:         return True
00134:     markdown_heads = stripped.count("##")
00135:     useful_words = sum(
00136:         stripped.lower().count(word)
00137:         for word in ["audio", "blender", "segment", "material", "fog", "light", "mesh"]
00138:     )
00139:     return markdown_heads < 2 and useful_words < 5
00140: 
00141: 
00142: def deterministic_technical_notes(music_context: dict[str, Any], project_manifest: dict[str, Any], reason: str) -> str:
00143:     summary = music_context.get("analysis_summary") or {}
00144:     track_summary = music_context.get("track_summary") or {}
00145:     segments = music_context.get("segments") or []
00146:     files = project_manifest.get("files") or []
00147:     priority_files = [
00148:         item.get("file")
00149:         for item in files
00150:         if item.get("file", "").endswith((
00151:             "Scripting/v61b/config.py",
00152:             "Scripting/v61b/materials.py",
00153:             "Scripting/v61b/fog_dynamics.py",
00154:             "Scripting/v61b/physics_setup.py",
00155:             "Scripting/v61b/scene_tuning_panel.py",
00156:             "Tools/workflow/workflow_state.py",
00157:             "Tools/npu/run_dual_ai_pipeline.py",
00158:         ))
00159:     ]
00160: 
00161:     lines = [
00162:         "# Deterministic Technical Notes\n\n",
00163:         f"Reason: NPU output was not trusted (`{reason}`).\n\n",
00164:         "## Track Map\n",
00165:         f"- Duration: `{summary.get('duration_sec', track_summary.get('duration_sec', '?'))}` seconds.\n",
00166:         f"- FPS: `{summary.get('fps', track_summary.get('fps', '?'))}`.\n",
00167:         f"- BPM: `{summary.get('estimated_tempo_bpm', track_summary.get('estimated_tempo_bpm', '?'))}`.\n",
00168:         f"- Segment count: `{len(segments)}`.\n\n",
00169:         "## Project Primary Files\n",
00170:     ]
00171:     for file_name in priority_files[:20]:
00172:         lines.append(f"- `{file_name}`\n")
00173: 
00174:     lines.extend(
00175:         [
00176:             "\n## Safe Implementation Policy\n",
00177:             "- Use full frame-by-frame Blender keyframe JSON as data input only.\n",
00178:             "- Generate patch plans against existing project files, not monolithic replacement scripts.\n",
00179:             "- Prefer hotpatch/panel/update modules for materials, fog, lights and render changes.\n",
00180:             "- Require a reload only when primary object creation or scene topology changes.\n\n",
00181:             "## Audio Control Map\n",
00182:             "- Low band: hero mesh deformation scale, gravity/attractor strength, fog density body.\n",
00183:             "- Mid band: material roughness/emission mix, secondary object motion, fog filament drift.\n",
00184:             "- High band: small emission accents, glints, particle sparkle, sharp camera micro motion.\n",
00185:             "- Onset/beat: short impulses, never a constant global light flash.\n\n",
00186:         ]
00187:     )
00188:     return "".join(lines)
00189: 
00190: 
00191: def run_npu_technical_pass(args: argparse.Namespace) -> str:
00192:     script = TOOLS_DIR / "run_npu_review.py"
00193:     python_exe = Path(args.npu_python)
00194:     cmd = [
00195:         str(python_exe),
00196:         str(script),
00197:         "--engine",
00198:         "npu",
00199:         "--domain",
00200:         "music",
00201:         "--mode",
00202:         "chunked",
00203:         "--context",
00204:         str(TOOLS_DIR / "npu_music_context.md"),
00205:         "--chunk-dir",
00206:         str(TOOLS_DIR / "npu_music_chunks"),
00207:         "--out",
00208:         str(NPU_TECH_MD),
00209:         "--notes-out",
00210:         str(TOOLS_DIR / "npu_dual_ai_chunk_notes.md"),
00211:         "--max-context-chars",
00212:         "0",
00213:         "--chunk-chars",
00214:         "10500",
00215:         "--chunk-overlap-chars",
00216:         "700",
00217:         "--max-prompt-chars",
00218:         "15000",
00219:         "--max-chunk-tokens",
00220:         str(args.npu_chunk_tokens),
00221:         "--max-reduce-tokens",
00222:         str(args.npu_reduce_tokens),
00223:         "--max-new-tokens",
00224:         str(args.npu_final_tokens),
00225:         "--max-prompt-len",
00226:         "16384",
00227:         "--min-response-len",
00228:         "64",
00229:     ]
00230: 
00231:     subprocess.run(cmd, check=True)
00232:     return read_text(NPU_TECH_MD)
00233: 
00234: 
00235: def build_creative_scene_prompt(music_context: dict[str, Any], npu_notes: str, project_index: str) -> str:
00236:     compact = {
00237:         "analysis_summary": music_context.get("analysis_summary"),
00238:         "track_summary": music_context.get("track_summary"),
00239:         "scene_summaries": music_context.get("scene_summaries"),
00240:         "ai_operating_contract": {
00241:             "memory_first": "Use director memory and user corrections before generic defaults.",
00242:             "chunk_first": "Use compact chunks for reasoning and refs for exact data.",
00243:             "full_keyframes": "Never summarize or discard full Blender keyframes; scripts must read the full frames list.",
00244:             "answer_shape": "Return only the requested JSON schema during pipeline calls.",
00245:         },
```
