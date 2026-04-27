# Project Code Chunk 183/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `8`
- Lines: `1665-1704`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
01665:             "model_switch_rule": "Unload/stop previous Ollama model before loading the next model.",
01666:             "phase": args.phase,
01667:             "manual_context_used": args.include_manual,
01668:             "scene_brief_json": str(Path(args.scene_brief)) if args.scene_brief else None,
01669:             "asset_inventory_json": str(Path(args.asset_inventory)) if args.asset_inventory else None,
01670:             "implementation_draft_json": str(IMPLEMENTATION_DRAFT_JSON) if args.phase in {"implementation", "full"} else None,
01671:             "implementation_script": str(IMPLEMENTATION_SCRIPT) if args.phase in {"implementation", "full"} else None,
01672:         },
01673:         "npu_preflight_json": str(NPU_PREFLIGHT_JSON),
01674:         "npu_technical_notes_md": str(NPU_TECH_MD),
01675:         "ai_service_packet": {
01676:             "capsule_json": service_packet_info.get("capsule_json"),
01677:             "gpu_packet_json": service_packet_info.get("gpu_packet_json"),
01678:             "output_gpu_packet_json": service_packet_info.get("output_gpu_packet_json"),
01679:             "capsule_md": service_packet_info.get("capsule_md"),
01680:         },
01681:         "creative_ollama": creative,
01682:         "technical_ollama": technical,
01683:         "final_plan": plan,
01684:     }
01685: 
01686:     write_json(DUAL_PLAN_JSON, output)
01687:     write_json(OLLAMA_INSIGHTS_JSON, technical)
01688:     OLLAMA_INSIGHTS_MD.write_text(
01689:         markdown_from_insights(technical, technical.get("model", args.technical_model)),
01690:         encoding="utf-8",
01691:     )
01692:     write_brief(plan, creative, technical, npu_notes)
01693: 
01694:     print(f"[OK] Wrote: {DUAL_PLAN_JSON}")
01695:     print(f"[OK] Wrote: {DUAL_BRIEF_MD}")
01696:     print(f"[OK] Wrote: {NPU_TECH_MD}")
01697:     if args.phase in {"implementation", "full"} and not args.skip_ollama:
01698:         print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
01699:         print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
01700:         print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")
01701: 
01702: 
01703: if __name__ == "__main__":
01704:     main()
```
