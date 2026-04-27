# Project Code Chunk 208/212

- File: `Tools/workflow/workflow_state.py`
- Part: `3`
- Lines: `574-855`

## Symbol Map
- Imports: `from __future__ import annotations`, `from dataclasses import dataclass, asdict`, `from datetime import datetime`, `from pathlib import Path`, `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `time`
- Classes: `OperationResult` line 45; `WorkflowSession` line 125 methods: default, save
- Functions: `now_iso()` line 40; `write_json(path, payload)` line 59; `append_event(operation, event, payload)` line 64; `save_operation_result(result)` line 76; `slugify(value)` line 82; `track_stem_from_wav(wav_path)` line 89; `build_artifacts(wav_path)` line 93; `load_session(create)` line 159; `set_current_wav(wav_path)` line 191; `reset_to_default_wav()` line 218; `set_debug_enabled(enabled)` line 239; `available_ollama_models()` line 248; `set_ai_models()` line 266; `python_executable()` line 297; `audio_python_executable()` line 313; `run_command(command, operation, check, echo, debug, print_output, metadata, log)` line 346; `finish_session_operation(session, operation)` line 425; `path_within(path, parent)` line 431; `is_safe_intermediate_target(path)` line 439; `cleanup_intermediate_targets(session, include_all_tracks, include_logs)` line 450; `cleanup_render_frame_targets(session)` line 565; `delete_target_set(operation, targets, session)` line 582; `human_bytes(size)` line 632; `scan_path_stats(path)` line 641; `collect_matching_files(root, patterns)` line 683; `file_set_stats(name, paths)` line 692; `build_project_storage_stats(session)` line 714; `format_project_storage_stats(stats)` line 795; `cleanup_intermediates(session, include_all_tracks, include_logs)` line 841; `cleanup_render_frames(session)` line 854; `operation_status(session)` line 859; `run_analyze_wav(session, fps, skip_music_context)` line 877; `run_track_summary(session)` line 894; `run_music_context(session, include_ollama, ollama_model)` line 912; `run_code_context(session)` line 934; `run_project_ai_index(session, force)` line 941; `run_asset_inventory(session)` line 950; `run_scene_director_brief(session)` line 968; `run_manual_index(session, limit_files)` line 1001; `ensure_manual_library(session)` line 1011; `artifact_missing(session, key)` line 1017; `ensure_ai_prerequisites(session, phase, include_manual)` line 1022; `run_dual_ai(session, phase, include_manual, skip_npu, skip_ollama, creative_model, technical_model, max_new_tokens)` line 1053; `run_full_audio_prepare(session)` line 1123
- Assignments: `ROOT`, `PROJECT_DIR`, `AUDIO_DIR`, `RENDERS_DIR`, `OUTPUT_DIR`, `TOOLS_DIR`, `NPU_DIR`, `INDEX_AI_DIR`, `SESSION_PATH`, `LOG_DIR`, `EVENT_LOG_PATH`, `LAST_RESULT_PATH`, `DEFAULT_WAV`, `DEFAULT_TRACK_STEM`, `DEFAULT_RENDER_STEM`, `DEFAULT_FRAME_PREFIX`, `NPU_PYTHON`, `AUDIO_PYTHON`, `DEFAULT_CREATIVE_MODEL`, `DEFAULT_TECHNICAL_MODEL`, `DEFAULT_CHAT_MODEL`, `DEFAULT_SCRIPT_TOKENS`

## Content
```py
00574:         "protected_roots": [str(AUDIO_DIR)],
00575:         "preserved_video_outputs": [
00576:             session.artifacts.get("render_mp4"),
00577:             session.artifacts.get("render_ffmpeg_mp4"),
00578:         ],
00579:     }
00580: 
00581: 
00582: def delete_target_set(operation: str, targets: dict, session: WorkflowSession) -> OperationResult:
00583:     started_at = now_iso()
00584:     start = time.perf_counter()
00585:     deleted: list[str] = []
00586:     errors: list[str] = []
00587: 
00588:     append_event(operation, "start", {"targets": targets})
00589: 
00590:     for file_name in targets.get("files", []):
00591:         path = Path(file_name)
00592:         try:
00593:             if path.exists() and is_safe_intermediate_target(path):
00594:                 path.unlink()
00595:                 deleted.append(str(path))
00596:         except Exception as exc:
00597:             errors.append(f"{path}: {exc}")
00598: 
00599:     for dir_name in targets.get("dirs", []):
00600:         path = Path(dir_name)
00601:         try:
00602:             allowed = is_safe_intermediate_target(path) or path_within(path, RENDERS_DIR)
00603:             if path.exists() and allowed and not path_within(path, AUDIO_DIR):
00604:                 shutil.rmtree(path)
00605:                 deleted.append(str(path))
00606:         except Exception as exc:
00607:             errors.append(f"{path}: {exc}")
00608: 
00609:     result = OperationResult(
00610:         operation=operation,
00611:         ok=not errors,
00612:         started_at=started_at,
00613:         ended_at=now_iso(),
00614:         elapsed_sec=round(time.perf_counter() - start, 4),
00615:         command=None,
00616:         cwd=str(PROJECT_DIR),
00617:         returncode=0 if not errors else 1,
00618:         stdout_tail="\n".join(deleted[-200:]),
00619:         error="\n".join(errors) if errors else None,
00620:         metadata={
00621:             "deleted_count": len(deleted),
00622:             "deleted": deleted,
00623:             "errors": errors,
00624:             "targets": targets,
00625:         },
00626:     )
00627:     save_operation_result(result)
00628:     finish_session_operation(session, operation)
00629:     return result
00630: 
00631: 
00632: def human_bytes(size: int | float) -> str:
00633:     value = float(size or 0)
00634:     for unit in ["B", "KB", "MB", "GB", "TB"]:
00635:         if value < 1024.0 or unit == "TB":
00636:             return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
00637:         value /= 1024.0
00638:     return f"{value:.1f} TB"
00639: 
00640: 
00641: def scan_path_stats(path: Path) -> dict:
00642:     path = Path(path)
00643:     stats = {
00644:         "path": str(path),
00645:         "exists": path.exists(),
00646:         "bytes": 0,
00647:         "files": 0,
00648:         "dirs": 0,
00649:         "errors": [],
00650:     }
00651:     if not stats["exists"]:
00652:         return stats
00653: 
00654:     try:
00655:         if path.is_file():
00656:             stats["bytes"] = path.stat().st_size
00657:             stats["files"] = 1
00658:             return stats
00659:     except OSError as exc:
00660:         stats["errors"].append(f"{path}: {exc}")
00661:         return stats
00662: 
00663:     stack = [path]
00664:     while stack:
00665:         current = stack.pop()
00666:         try:
00667:             with os.scandir(current) as entries:
00668:                 for entry in entries:
00669:                     try:
00670:                         if entry.is_dir(follow_symlinks=False):
00671:                             stats["dirs"] += 1
00672:                             stack.append(Path(entry.path))
00673:                         elif entry.is_file(follow_symlinks=False):
00674:                             stats["files"] += 1
00675:                             stats["bytes"] += entry.stat(follow_symlinks=False).st_size
00676:                     except OSError as exc:
00677:                         stats["errors"].append(f"{entry.path}: {exc}")
00678:         except OSError as exc:
00679:             stats["errors"].append(f"{current}: {exc}")
00680:     return stats
00681: 
00682: 
00683: def collect_matching_files(root: Path, patterns: list[str]) -> list[Path]:
00684:     if not root.exists():
00685:         return []
00686:     found: set[Path] = set()
00687:     for pattern in patterns:
00688:         found.update(path for path in root.glob(pattern) if path.is_file())
00689:     return sorted(found, key=lambda item: str(item).lower())
00690: 
00691: 
00692: def file_set_stats(name: str, paths: list[Path]) -> dict:
00693:     total = 0
00694:     existing: list[str] = []
00695:     for path in paths:
00696:         try:
00697:             if path.exists() and path.is_file():
00698:                 total += path.stat().st_size
00699:                 existing.append(str(path))
00700:         except OSError:
00701:             pass
00702:     return {
00703:         "name": name,
00704:         "path": "<file set>",
00705:         "exists": bool(existing),
00706:         "bytes": total,
00707:         "files": len(existing),
00708:         "dirs": 0,
00709:         "errors": [],
00710:         "sample_files": existing[:12],
00711:     }
00712: 
00713: 
00714: def build_project_storage_stats(session: WorkflowSession) -> dict:
00715:     scene_scripts_dir = INDEX_AI_DIR / "scene_scripts"
00716:     patch_library_dir = INDEX_AI_DIR / "patch_library"
00717:     manual_dir = ROOT / "manual"
00718:     frame_dir = Path(session.artifacts.get("render_frames_dir", ""))
00719:     venvs_dir = ROOT / "venvs"
00720: 
00721:     sections = [
00722:         ("Workspace root", ROOT),
00723:         ("Project total", PROJECT_DIR),
00724:         ("Output/intermedi", OUTPUT_DIR),
00725:         ("Workflow logs", LOG_DIR),
00726:         ("indexAI total", INDEX_AI_DIR),
00727:         ("Generated scene scripts", scene_scripts_dir),
00728:         ("AI patch/service library", patch_library_dir),
00729:         ("Manual library", manual_dir),
00730:         ("Tools NPU/workflow", TOOLS_DIR),
00731:         ("Renders total", RENDERS_DIR),
00732:         ("Current frame render dir", frame_dir),
00733:         ("Audio library", AUDIO_DIR),
00734:         ("Python venvs", venvs_dir),
00735:     ]
00736: 
00737:     section_stats = []
00738:     for name, path in sections:
00739:         item = scan_path_stats(path)
00740:         item["name"] = name
00741:         section_stats.append(item)
00742: 
00743:     ai_chat_files = collect_matching_files(
00744:         OUTPUT_DIR,
00745:         [
00746:             "*_scene_brief.json",
00747:             "*_dual_ai_scene_plan.json",
00748:             "*_ai_implementation_draft.json",
00749:             "*_gpu_task_packet.json",
00750:             "workflow_logs/*.json",
00751:             "workflow_logs/*.jsonl",
00752:         ],
00753:     )
00754:     generated_ai_files = collect_matching_files(
00755:         INDEX_AI_DIR,
00756:         [
00757:             "scene_scripts/*_scene_builder_candidate.py",
00758:             "scene_scripts/**/*",
00759:             "patch_library/*_npu_service_capsule.json",
00760:             "patch_library/*_npu_service_capsule.md",
00761:             "patch_library/*_gpu_task_packet.json",
00762:         ],
00763:     )
00764: 
00765:     artifact_stats = [
00766:         file_set_stats("AI chats/briefs/logs", ai_chat_files),
00767:         file_set_stats("Generated AI scripts/bundles", generated_ai_files),
00768:     ]
00769: 
00770:     current_artifacts = []
00771:     for key, value in session.artifacts.items():
00772:         path = Path(value) if isinstance(value, str) else None
00773:         if path and path.suffix:
00774:             current_artifacts.append({
00775:                 "key": key,
00776:                 "path": str(path),
00777:                 "exists": path.exists(),
00778:                 "bytes": path.stat().st_size if path.exists() and path.is_file() else 0,
00779:             })
00780: 
00781:     return {
00782:         "generated_at": now_iso(),
00783:         "track_stem": session.track_stem,
00784:         "audio_path": session.artifacts.get("audio_path"),
00785:         "sections": section_stats,
00786:         "artifact_sets": artifact_stats,
00787:         "current_artifacts": current_artifacts,
00788:         "notes": [
00789:             "GPU 0 / iGPU can be considered for Intel/OpenVINO service tasks when supported by drivers/runtime.",
00790:             "NVIDIA GPU should stay reserved for Blender/Ollama/render-heavy work when possible.",
00791:         ],
00792:     }
00793: 
00794: 
00795: def format_project_storage_stats(stats: dict) -> str:
00796:     lines = [
00797:         "=" * 78,
00798:         "SPAZIOTEMPO PROJECT STORAGE STATS",
00799:         "=" * 78,
00800:         f"Generated: {stats.get('generated_at')}",
00801:         f"Track:     {stats.get('track_stem')}",
00802:         f"Audio:     {stats.get('audio_path')}",
00803:         "",
00804:         "Main Areas:",
00805:     ]
00806:     for item in stats.get("sections", []):
00807:         mark = "OK" if item.get("exists") else "MISSING"
00808:         lines.append(
00809:             f"  [{mark}] {item.get('name')}: {human_bytes(item.get('bytes', 0))} | "
00810:             f"files={item.get('files', 0)} dirs={item.get('dirs', 0)}"
00811:         )
00812:         lines.append(f"       {item.get('path')}")
00813:         if item.get("errors"):
00814:             lines.append(f"       errors={len(item.get('errors', []))}")
00815: 
00816:     lines.append("")
00817:     lines.append("AI / Chat / Generated Artifacts:")
00818:     for item in stats.get("artifact_sets", []):
00819:         lines.append(
00820:             f"  {item.get('name')}: {human_bytes(item.get('bytes', 0))} | files={item.get('files', 0)}"
00821:         )
00822:         for sample in item.get("sample_files", [])[:8]:
00823:             lines.append(f"       {sample}")
00824:         if item.get("files", 0) > 8:
00825:             lines.append(f"       ... altri {item.get('files', 0) - 8} file")
00826: 
00827:     lines.append("")
00828:     lines.append("Current Track Artifacts:")
00829:     for item in stats.get("current_artifacts", []):
00830:         mark = "OK" if item.get("exists") else "--"
00831:         lines.append(f"  [{mark}] {item.get('key')}: {human_bytes(item.get('bytes', 0))}")
00832:         lines.append(f"       {item.get('path')}")
00833: 
00834:     lines.append("")
00835:     lines.append("Notes:")
00836:     for note in stats.get("notes", []):
00837:         lines.append(f"  - {note}")
00838:     return "\n".join(lines)
00839: 
00840: 
00841: def cleanup_intermediates(session: WorkflowSession, include_all_tracks: bool = True, include_logs: bool = True) -> OperationResult:
00842:     targets = cleanup_intermediate_targets(session, include_all_tracks=include_all_tracks, include_logs=include_logs)
00843:     targets["preserved"] = {
00844:         "audio_dir": str(AUDIO_DIR),
00845:         "renders_dir": str(RENDERS_DIR),
00846:         "current_audio": session.artifacts.get("audio_path"),
00847:         "render_mp4": session.artifacts.get("render_mp4"),
00848:         "render_ffmpeg_mp4": session.artifacts.get("render_ffmpeg_mp4"),
00849:         "render_frames_dir": session.artifacts.get("render_frames_dir"),
00850:     }
00851:     return delete_target_set("cleanup_intermediates", targets, session)
00852: 
00853: 
00854: def cleanup_render_frames(session: WorkflowSession) -> OperationResult:
00855:     targets = cleanup_render_frame_targets(session)
```
