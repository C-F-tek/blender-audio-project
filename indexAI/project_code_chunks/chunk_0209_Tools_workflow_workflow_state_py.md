# Project Code Chunk 209/212

- File: `Tools/workflow/workflow_state.py`
- Part: `4`
- Lines: `856-1102`

## Symbol Map
- Imports: `from __future__ import annotations`, `from dataclasses import dataclass, asdict`, `from datetime import datetime`, `from pathlib import Path`, `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `time`
- Classes: `OperationResult` line 45; `WorkflowSession` line 125 methods: default, save
- Functions: `now_iso()` line 40; `write_json(path, payload)` line 59; `append_event(operation, event, payload)` line 64; `save_operation_result(result)` line 76; `slugify(value)` line 82; `track_stem_from_wav(wav_path)` line 89; `build_artifacts(wav_path)` line 93; `load_session(create)` line 159; `set_current_wav(wav_path)` line 191; `reset_to_default_wav()` line 218; `set_debug_enabled(enabled)` line 239; `available_ollama_models()` line 248; `set_ai_models()` line 266; `python_executable()` line 297; `audio_python_executable()` line 313; `run_command(command, operation, check, echo, debug, print_output, metadata, log)` line 346; `finish_session_operation(session, operation)` line 425; `path_within(path, parent)` line 431; `is_safe_intermediate_target(path)` line 439; `cleanup_intermediate_targets(session, include_all_tracks, include_logs)` line 450; `cleanup_render_frame_targets(session)` line 565; `delete_target_set(operation, targets, session)` line 582; `human_bytes(size)` line 632; `scan_path_stats(path)` line 641; `collect_matching_files(root, patterns)` line 683; `file_set_stats(name, paths)` line 692; `build_project_storage_stats(session)` line 714; `format_project_storage_stats(stats)` line 795; `cleanup_intermediates(session, include_all_tracks, include_logs)` line 841; `cleanup_render_frames(session)` line 854; `operation_status(session)` line 859; `run_analyze_wav(session, fps, skip_music_context)` line 877; `run_track_summary(session)` line 894; `run_music_context(session, include_ollama, ollama_model)` line 912; `run_code_context(session)` line 934; `run_project_ai_index(session, force)` line 941; `run_asset_inventory(session)` line 950; `run_scene_director_brief(session)` line 968; `run_manual_index(session, limit_files)` line 1001; `ensure_manual_library(session)` line 1011; `artifact_missing(session, key)` line 1017; `ensure_ai_prerequisites(session, phase, include_manual)` line 1022; `run_dual_ai(session, phase, include_manual, skip_npu, skip_ollama, creative_model, technical_model, max_new_tokens)` line 1053; `run_full_audio_prepare(session)` line 1123
- Assignments: `ROOT`, `PROJECT_DIR`, `AUDIO_DIR`, `RENDERS_DIR`, `OUTPUT_DIR`, `TOOLS_DIR`, `NPU_DIR`, `INDEX_AI_DIR`, `SESSION_PATH`, `LOG_DIR`, `EVENT_LOG_PATH`, `LAST_RESULT_PATH`, `DEFAULT_WAV`, `DEFAULT_TRACK_STEM`, `DEFAULT_RENDER_STEM`, `DEFAULT_FRAME_PREFIX`, `NPU_PYTHON`, `AUDIO_PYTHON`, `DEFAULT_CREATIVE_MODEL`, `DEFAULT_TECHNICAL_MODEL`, `DEFAULT_CHAT_MODEL`, `DEFAULT_SCRIPT_TOKENS`

## Content
```py
00856:     return delete_target_set("cleanup_render_frames", targets, session)
00857: 
00858: 
00859: def operation_status(session: WorkflowSession) -> dict:
00860:     artifacts = session.artifacts
00861:     checks = {
00862:         "audio_path": bool(artifacts.get("audio_path")) and Path(artifacts["audio_path"]).exists(),
00863:         "analysis_json": bool(artifacts.get("analysis_json")) and Path(artifacts["analysis_json"]).exists(),
00864:         "track_summary_json": bool(artifacts.get("track_summary_json")) and Path(artifacts["track_summary_json"]).exists(),
00865:         "music_context_json": bool(artifacts.get("music_context_json")) and Path(artifacts["music_context_json"]).exists(),
00866:         "analysis_ai_context_json": bool(artifacts.get("analysis_ai_context_json")) and Path(artifacts["analysis_ai_context_json"]).exists(),
00867:         "blender_keyframes_json": bool(artifacts.get("blender_keyframes_json")) and Path(artifacts["blender_keyframes_json"]).exists(),
00868:         "dual_ai_plan_json": bool(artifacts.get("dual_ai_plan_json")) and Path(artifacts["dual_ai_plan_json"]).exists(),
00869:         "scene_brief_json": bool(artifacts.get("scene_brief_json")) and Path(artifacts["scene_brief_json"]).exists(),
00870:         "asset_inventory_json": bool(artifacts.get("asset_inventory_json")) and Path(artifacts["asset_inventory_json"]).exists(),
00871:         "ai_implementation_draft_json": bool(artifacts.get("ai_implementation_draft_json")) and Path(artifacts["ai_implementation_draft_json"]).exists(),
00872:         "generated_scene_script": bool(artifacts.get("generated_scene_script")) and Path(artifacts["generated_scene_script"]).exists(),
00873:     }
00874:     return checks
00875: 
00876: 
00877: def run_analyze_wav(session: WorkflowSession, fps: float = 30.0, skip_music_context: bool = False) -> None:
00878:     py = audio_python_executable()
00879:     args = [
00880:         str(py),
00881:         str(PROJECT_DIR / "analyze_wav.py"),
00882:         session.artifacts["audio_path"],
00883:         "--output-dir",
00884:         session.artifacts["output_dir"],
00885:         "--fps",
00886:         str(fps),
00887:     ]
00888:     if skip_music_context:
00889:         args.append("--skip-music-context")
00890:     run_command(args, operation="analyze_wav", metadata={"track_stem": session.track_stem, "fps": fps})
00891:     finish_session_operation(session, "analyze_wav")
00892: 
00893: 
00894: def run_track_summary(session: WorkflowSession) -> None:
00895:     py = python_executable()
00896:     run_command(
00897:         [
00898:             str(py),
00899:             str(PROJECT_DIR / "build_track_summary.py"),
00900:             "--analysis-json",
00901:             session.artifacts["analysis_json"],
00902:             "--out-json",
00903:             session.artifacts["track_summary_json"],
00904:             "--skip-music-context",
00905:         ],
00906:         operation="build_track_summary",
00907:         metadata={"track_stem": session.track_stem},
00908:     )
00909:     finish_session_operation(session, "build_track_summary")
00910: 
00911: 
00912: def run_music_context(session: WorkflowSession, include_ollama: bool = False, ollama_model: str = "qwen2.5-coder:14b") -> None:
00913:     py = python_executable()
00914:     args = [
00915:         str(py),
00916:         str(NPU_DIR / "build_music_context.py"),
00917:         "--analysis",
00918:         session.artifacts["analysis_json"],
00919:         "--track-summary",
00920:         session.artifacts["track_summary_json"],
00921:         "--compact-json",
00922:         session.artifacts["music_context_json"],
00923:         "--analysis-ai-context",
00924:         session.artifacts["analysis_ai_context_json"],
00925:         "--blender-keyframes-json",
00926:         session.artifacts["blender_keyframes_json"],
00927:     ]
00928:     if include_ollama:
00929:         args.extend(["--run-ollama", "--ollama-model", ollama_model])
00930:     run_command(args, operation="build_music_context", metadata={"track_stem": session.track_stem})
00931:     finish_session_operation(session, "build_music_context")
00932: 
00933: 
00934: def run_code_context(session: WorkflowSession) -> None:
00935:     py = python_executable()
00936:     run_command([str(py), str(NPU_DIR / "build_npu_code_context.py")], operation="build_code_context")
00937:     run_project_ai_index(session)
00938:     finish_session_operation(session, "build_code_context")
00939: 
00940: 
00941: def run_project_ai_index(session: WorkflowSession, force: bool = False) -> None:
00942:     py = python_executable()
00943:     args = [str(py), str(NPU_DIR / "build_project_ai_index.py")]
00944:     if force:
00945:         args.append("--force")
00946:     run_command(args, operation="build_project_ai_index", metadata={"force": force})
00947:     finish_session_operation(session, "build_project_ai_index")
00948: 
00949: 
00950: def run_asset_inventory(session: WorkflowSession) -> dict:
00951:     from asset_inventory import build_asset_inventory
00952: 
00953:     output_json = Path(session.artifacts["asset_inventory_json"])
00954:     output_md = INDEX_AI_DIR / "asset_inventory.md"
00955:     inventory = build_asset_inventory(ROOT, PROJECT_DIR, output_json, output_md)
00956:     append_event(
00957:         "build_asset_inventory",
00958:         "result",
00959:         {
00960:             "asset_count": inventory.get("asset_count"),
00961:             "output_json": str(output_json),
00962:             "output_md": str(output_md),
00963:         },
00964:     )
00965:     return inventory
00966: 
00967: 
00968: def run_scene_director_brief(session: WorkflowSession) -> OperationResult:
00969:     from scene_brief import run_interactive_scene_brief
00970: 
00971:     started_at = now_iso()
00972:     start = time.perf_counter()
00973:     append_event("scene_director_brief", "start", {"track_stem": session.track_stem})
00974:     output_path = Path(session.artifacts["scene_brief_json"])
00975:     brief = run_interactive_scene_brief(
00976:         track_stem=session.track_stem,
00977:         audio_path=session.artifacts["audio_path"],
00978:         output_path=output_path,
00979:     )
00980:     result = OperationResult(
00981:         operation="scene_director_brief",
00982:         ok=True,
00983:         started_at=started_at,
00984:         ended_at=now_iso(),
00985:         elapsed_sec=round(time.perf_counter() - start, 4),
00986:         command=None,
00987:         cwd=str(PROJECT_DIR),
00988:         returncode=0,
00989:         stdout_tail=f"Wrote {output_path}",
00990:         metadata={
00991:             "track_stem": session.track_stem,
00992:             "scene_brief_json": str(output_path),
00993:             "field_count": len(brief.get("scene_preferences", {})),
00994:         },
00995:     )
00996:     save_operation_result(result)
00997:     finish_session_operation(session, "scene_director_brief")
00998:     return result
00999: 
01000: 
01001: def run_manual_index(session: WorkflowSession, limit_files: int = 80) -> None:
01002:     py = python_executable()
01003:     run_command(
01004:         [str(py), str(NPU_DIR / "build_blender_manual_context.py"), "--limit-files", str(limit_files)],
01005:         operation="build_manual_context",
01006:         metadata={"limit_files": limit_files},
01007:     )
01008:     finish_session_operation(session, "build_manual_context")
01009: 
01010: 
01011: def ensure_manual_library(session: WorkflowSession) -> None:
01012:     py = python_executable()
01013:     run_command([str(py), str(NPU_DIR / "build_blender_manual_context.py"), "--ensure-only"], operation="ensure_manual_library")
01014:     finish_session_operation(session, "ensure_manual_library")
01015: 
01016: 
01017: def artifact_missing(session: WorkflowSession, key: str) -> bool:
01018:     value = session.artifacts.get(key)
01019:     return not value or not Path(value).exists()
01020: 
01021: 
01022: def ensure_ai_prerequisites(session: WorkflowSession, phase: str, include_manual: bool = False) -> None:
01023:     if artifact_missing(session, "analysis_json") or artifact_missing(session, "blender_keyframes_json"):
01024:         raise RuntimeError("Manca l'analisi WAV completa: esegui prima 3 Analizza WAV.")
01025: 
01026:     if artifact_missing(session, "track_summary_json"):
01027:         print("[AUTO] Track summary mancante: lo genero ora.")
01028:         run_track_summary(session)
01029: 
01030:     if (
01031:         artifact_missing(session, "music_context_json")
01032:         or artifact_missing(session, "analysis_ai_context_json")
01033:         or artifact_missing(session, "blender_keyframes_json")
01034:     ):
01035:         print("[AUTO] Music context mancante o incompleto: lo genero ora.")
01036:         run_music_context(session)
01037: 
01038:     project_index = INDEX_AI_DIR / "project_code_index.md"
01039:     project_manifest = INDEX_AI_DIR / "project_code_manifest.json"
01040:     if not project_index.exists() or not project_manifest.exists():
01041:         print("[AUTO] indexAI project index mancante: lo genero ora.")
01042:         run_project_ai_index(session)
01043: 
01044:     if include_manual:
01045:         ensure_manual_library(session)
01046: 
01047:     run_asset_inventory(session)
01048: 
01049:     if phase == "implementation" and artifact_missing(session, "dual_ai_plan_json"):
01050:         raise RuntimeError("Manca il piano Dual AI: esegui prima 9 Dual AI plan.")
01051: 
01052: 
01053: def run_dual_ai(
01054:     session: WorkflowSession,
01055:     phase: str = "plan",
01056:     include_manual: bool = False,
01057:     skip_npu: bool = True,
01058:     skip_ollama: bool = False,
01059:     creative_model: str | None = None,
01060:     technical_model: str | None = None,
01061:     max_new_tokens: int | None = None,
01062: ) -> None:
01063:     ensure_ai_prerequisites(session, phase=phase, include_manual=include_manual)
01064:     creative_model = creative_model or session.creative_model or DEFAULT_CREATIVE_MODEL
01065:     technical_model = technical_model or session.technical_model or DEFAULT_TECHNICAL_MODEL
01066:     max_new_tokens = max_new_tokens or session.script_max_tokens or DEFAULT_SCRIPT_TOKENS
01067:     py = python_executable()
01068:     args = [
01069:         str(py),
01070:         str(NPU_DIR / "run_dual_ai_pipeline.py"),
01071:         "--phase",
01072:         phase,
01073:         "--track-stem",
01074:         session.track_stem,
01075:         "--analysis",
01076:         session.artifacts["analysis_json"],
01077:         "--track-summary",
01078:         session.artifacts["track_summary_json"],
01079:         "--compact-json",
01080:         session.artifacts["music_context_json"],
01081:         "--analysis-ai-context",
01082:         session.artifacts["analysis_ai_context_json"],
01083:         "--blender-keyframes-json",
01084:         session.artifacts["blender_keyframes_json"],
01085:         "--creative-model",
01086:         creative_model,
01087:         "--technical-model",
01088:         technical_model,
01089:         "--npu-python",
01090:         str(NPU_PYTHON),
01091:         "--max-new-tokens",
01092:         str(max_new_tokens),
01093:     ]
01094:     if include_manual:
01095:         args.append("--include-manual")
01096:     if skip_npu:
01097:         args.append("--skip-npu")
01098:     if skip_ollama:
01099:         args.append("--skip-ollama")
01100:     scene_brief = Path(session.artifacts.get("scene_brief_json", ""))
01101:     if scene_brief.exists():
01102:         args.extend(["--scene-brief", str(scene_brief)])
```
