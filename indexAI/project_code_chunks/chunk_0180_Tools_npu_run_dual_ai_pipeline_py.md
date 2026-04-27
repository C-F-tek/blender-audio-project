# Project Code Chunk 180/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `5`
- Lines: `993-1212`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
00993:         keyframe_material_emission(hero_mat, frame, 0.28 + high * 0.55 + onset * 0.22 + beat * 0.18)
00994:         inserted += 1
00995:     return inserted
00996: 
00997: 
00998: def apply_full_audio_keyframes_inverted(hero: bpy.types.Object, disp: bpy.types.Modifier, hero_mat: bpy.types.Material, keyframes: dict, fps: float) -> int:
00999:     audio_frames = keyframes.get("frames") or []
01000:     inserted = 0
01001:     for audio in audio_frames:
01002:         time_sec = float(audio.get("time") or 0.0)
01003:         frame = int(round(time_sec * fps)) + 1
01004:         low = float(audio.get("low") or 0.0)
01005:         mid = float(audio.get("mid") or 0.0)
01006:         high = float(audio.get("high") or 0.0)
01007:         onset = float(audio.get("onset") or 0.0)
01008:         beat = float(audio.get("beat") or 0.0)
01009:         hero.scale = (
01010:             1.0 + high * 0.12 + onset * 0.018,
01011:             1.0 + low * 0.075 + beat * 0.025,
01012:             1.0 + mid * 0.055 + high * 0.035,
01013:         )
01014:         hero.keyframe_insert(data_path="scale", frame=frame)
01015:         disp.strength = 0.035 + high * 0.11 + low * 0.045 + onset * 0.02
01016:         disp.keyframe_insert(data_path="strength", frame=frame)
01017:         keyframe_material_emission(hero_mat, frame, 0.25 + low * 0.45 + mid * 0.20 + beat * 0.22)
01018:         inserted += 1
01019:     return inserted
01020: 
01021: 
01022: def build_scene() -> None:
01023:     analysis = load_json(ANALYSIS_JSON)
01024:     music = load_json(MUSIC_CONTEXT_JSON)
01025:     ai_context = load_json(AI_CONTEXT_JSON)
01026:     keyframes = load_json(BLENDER_KEYFRAMES_JSON)
01027:     asset_inventory = load_json(ASSET_INVENTORY_JSON) if ASSET_INVENTORY_JSON else {{}}
01028: 
01029:     meta = keyframes.get("meta") or analysis.get("meta") or (ai_context.get("analysis_summary") or {{}}).get("meta") or {{}}
01030:     fps = float(meta.get("fps") or 30.0)
01031:     duration = float(meta.get("duration_sec") or 180.0)
01032:     scene = bpy.context.scene
01033:     scene.frame_start = 1
01034:     scene.frame_end = max(1, int(duration * fps))
01035:     scene.render.fps = int(round(fps))
01036: 
01037:     clear_scene()
01038:     col_core = make_collection("AI Scene Core")
01039:     col_orbits = make_collection("AI Audio Orbits")
01040:     col_fog = make_collection("AI Volumetric Forms")
01041:     col_refs = make_collection("AI JSON References")
01042: 
01043:     hero_mat = create_material("AI_Hero_Material_MatterEmission", (0.70, 0.86, 0.88, 1.0), 0.45)
01044:     counter_mat = create_material("AI_Hero_CounterMaterial_Ball", (0.95, 0.72, 0.45, 1.0), 0.55)
01045:     accent_mat = create_material("AI_Accent_Emission_Material", (0.95, 0.72, 0.45, 1.0), 1.2)
01046:     cool_mat = create_material("AI_Cool_Background_Material", (0.13, 0.38, 0.44, 1.0), 0.08)
01047:     fog_mat = create_material("AI_Fog_Filament_Material", (0.48, 0.78, 0.84, 0.35), 0.12)
01048:     text_mat = create_material("AI_Title_Material", (0.82, 0.91, 0.88, 1.0), 0.35)
01049: 
01050:     ball_asset = preferred_ball_asset_path(asset_inventory)
01051:     hero_location = (-0.95, 0, 1.75) if USE_DUAL_FOCUS else (0, 0, 1.75)
01052:     hero = add_uv_sphere("AI_HeroAura_DeformableCore", 1.20 if USE_DUAL_FOCUS else 1.35, hero_location, hero_mat, segments=96)
01053:     link_to(col_core, hero)
01054:     disp = hero.modifiers.new("AI_Audio_Displace_LowMid", "DISPLACE")
01055:     tex = bpy.data.textures.new("AI_Audio_Deformation_Texture", "VORONOI")
01056:     tex.noise_scale = 1.15
01057:     tex.intensity = 0.42
01058:     disp.texture = tex
01059:     disp.strength = 0.08
01060: 
01061:     counter_hero = None
01062:     counter_disp = None
01063:     if USE_DUAL_FOCUS:
01064:         if ball_asset:
01065:             counter_hero = make_asset_focus("AI_BallAsset_CounterCore", ball_asset, (0.95, 0, 1.75), counter_mat, fallback_radius=1.12)
01066:         else:
01067:             counter_hero = add_uv_sphere("AI_CounterSphere_DeformableCore", 1.12, (0.95, 0, 1.75), counter_mat, segments=96)
01068:         link_to(col_core, counter_hero)
01069:         counter_disp = counter_hero.modifiers.new("AI_Audio_Displace_InvertedBall", "DISPLACE")
01070:         counter_tex = bpy.data.textures.new("AI_Audio_Deformation_Texture_InvertedBall", "VORONOI")
01071:         counter_tex.noise_scale = 1.35
01072:         counter_tex.intensity = 0.38
01073:         counter_disp.texture = counter_tex
01074:         counter_disp.strength = 0.07
01075: 
01076:     segments = music.get("segments") or []
01077:     sample_segments = segments[::max(1, len(segments) // 16)] or segments[:16]
01078:     for idx, segment in enumerate(sample_segments[:18]):
01079:         controls = segment.get("controls") or {{}}
01080:         angle = idx * (math.tau / max(1, len(sample_segments[:18])))
01081:         band = segment.get("dominant_band") or controls.get("primary_band") or "mid"
01082:         score = float(segment.get("intensity_score") or 0.2)
01083:         radius = 3.4 + score * 1.8
01084:         z = 1.45 + math.sin(angle * 2.0) * 0.55
01085:         mat = accent_mat if band == "high" else cool_mat if band == "mid" else hero_mat
01086:         sat = add_uv_sphere(f"AI_AudioSatellite_{{idx+1:02d}}_{{band}}", 0.12 + score * 0.18, (math.cos(angle) * radius, math.sin(angle) * radius, z), mat, segments=32)
01087:         link_to(col_orbits, sat)
01088:         sat["segment_index"] = int(segment.get("index") or idx + 1)
01089:         sat["audio_band"] = str(band)
01090:         sat["json_start_sec"] = float(segment.get("start_sec") or 0.0)
01091:         start_frame = int(float(segment.get("start_sec") or 0.0) * fps) + 1
01092:         end_frame = int(float(segment.get("end_sec") or 0.0) * fps) + 1
01093:         for frame, rot in [(start_frame, angle), (end_frame, angle + math.tau * (1.0 + score))]:
01094:             sat.rotation_euler[2] = rot
01095:             sat.keyframe_insert(data_path="rotation_euler", frame=frame, index=2)
01096:         scale = 1.0 + float(controls.get("accent_emission") or score) * 0.85
01097:         sat.scale = (scale, scale, scale)
01098:         sat.keyframe_insert(data_path="scale", frame=start_frame)
01099: 
01100:     # Procedural fog represented as visible soft filaments instead of heavy volume simulation.
01101:     for idx in range(24):
01102:         angle = idx * math.tau / 24
01103:         length = 0.9 + (idx % 5) * 0.24
01104:         bpy.ops.mesh.primitive_cube_add(size=1, location=(math.cos(angle) * 2.6, math.sin(angle) * 2.6, 1.0 + (idx % 6) * 0.22))
01105:         fog = bpy.context.object
01106:         fog.name = f"AI_FogFilament_{{idx+1:02d}}"
01107:         fog.scale = (0.035, length, 0.035)
01108:         fog.rotation_euler[2] = angle
01109:         fog.data.materials.append(fog_mat)
01110:         link_to(col_fog, fog)
01111:         for frame, mul in [(1, 0.65), (scene.frame_end // 2, 1.35), (scene.frame_end, 0.75)]:
01112:             fog.scale = (0.035 * mul, length * mul, 0.035 * mul)
01113:             fog.keyframe_insert(data_path="scale", frame=frame)
01114: 
01115:     title = add_text_label(TRACK_STEM.replace("_Master", ""), (0, -3.25, 0.72), 0.34, text_mat)
01116:     link_to(col_refs, title)
01117: 
01118:     inserted_full_keyframes = apply_full_audio_keyframes(hero, disp, hero_mat, keyframes, fps)
01119:     hero["full_audio_keyframes_inserted"] = inserted_full_keyframes
01120:     if counter_hero and counter_disp:
01121:         counter_inserted = apply_full_audio_keyframes_inverted(counter_hero, counter_disp, counter_mat, keyframes, fps)
01122:         counter_hero["full_audio_keyframes_inserted"] = counter_inserted
01123:         counter_hero["source_asset"] = str(ball_asset) if ball_asset else "procedural_fallback"
01124: 
01125:     bpy.ops.object.light_add(type="AREA", location=(0, -4.8, 4.8), rotation=(math.radians(60), 0, 0))
01126:     key = bpy.context.object
01127:     key.name = "AI_Soft_Key_Light"
01128:     key.data.energy = 450
01129:     key.data.size = 5.5
01130:     link_to(col_core, key)
01131: 
01132:     bpy.ops.object.camera_add(location=(0, -7.4, 3.2), rotation=(math.radians(65), 0, 0))
01133:     camera = bpy.context.object
01134:     camera.name = "AI_Album_Camera"
01135:     scene.camera = camera
01136:     camera.data.lens = 42
01137: 
01138:     world = scene.world or bpy.data.worlds.new("AI_World")
01139:     scene.world = world
01140:     world.color = (0.025, 0.095, 0.105)
01141: 
01142:     scene["ai_generated_from"] = str(MUSIC_CONTEXT_JSON)
01143:     scene["full_keyframes_reference"] = str(BLENDER_KEYFRAMES_JSON)
01144:     scene["note"] = "Standalone AI scene draft. Existing project files were used only as style reference."
01145: 
01146: 
01147: if __name__ == "__main__":
01148:     build_scene()
01149: '''
01150: 
01151: 
01152: def deterministic_support_files(track_stem: str, scene_brief: dict[str, Any] | None = None) -> list[dict[str, str]]:
01153:     slug = packet_slugify(track_stem)
01154:     bundle_dir = f"indexAI/scene_scripts/{slug}_scene_bundle"
01155:     manifest = {
01156:         "kind": "spaziotempo_generated_scene_bundle_manifest",
01157:         "track_stem": track_stem,
01158:         "main_script": f"indexAI/scene_scripts/{slug}_scene_builder_candidate.py",
01159:         "npu_service_role": [
01160:             "create split/module plan",
01161:             "maintain manifest of generated files",
01162:             "check naming consistency",
01163:             "summarize previous script for next GPU revision",
01164:             "avoid heavy code generation unless explicitly requested",
01165:         ],
01166:         "gpu_writer_role": [
01167:             "generate Blender Python scene logic",
01168:             "apply scene director changes",
01169:             "keep full audio keyframes as the animation source",
01170:         ],
01171:         "generated_files": [
01172:             f"{bundle_dir}/manifest.json",
01173:             f"{bundle_dir}/director_brief_snapshot.json",
01174:             f"{bundle_dir}/README.md",
01175:         ],
01176:     }
01177:     readme = f"""# {track_stem} Scene Bundle
01178: 
01179: This folder is generated support context for the standalone Blender scene script.
01180: 
01181: - Main Blender script: `../{slug}_scene_builder_candidate.py`
01182: - Existing project files are reference only.
01183: - Full audio keyframe JSON remains the source for animation.
01184: - NPU can safely maintain this manifest/split plan; GPU/Ollama should handle heavy Blender code generation.
01185: """
01186:     return [
01187:         {
01188:             "file": f"{bundle_dir}/manifest.json",
01189:             "kind": "manifest",
01190:             "content": json.dumps(manifest, indent=2, ensure_ascii=False),
01191:         },
01192:         {
01193:             "file": f"{bundle_dir}/director_brief_snapshot.json",
01194:             "kind": "brief_snapshot",
01195:             "content": json.dumps(scene_brief or {}, indent=2, ensure_ascii=False),
01196:         },
01197:         {
01198:             "file": f"{bundle_dir}/README.md",
01199:             "kind": "notes",
01200:             "content": readme,
01201:         },
01202:     ]
01203: 
01204: 
01205: def build_fallback_implementation_draft(
01206:     reason: str,
01207:     model: str | None = None,
01208:     args: argparse.Namespace | None = None,
01209:     scene_brief: dict[str, Any] | None = None,
01210:     asset_inventory: dict[str, Any] | None = None,
01211: ) -> dict[str, Any]:
01212:     indexed_files = get_indexed_project_files()
```
