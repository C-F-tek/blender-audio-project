# Project Code Chunk 178/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `3`
- Lines: `509-743`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
00509:         "allowed_new_prefixes": list(ALLOWED_NEW_PREFIXES),
00510:         "previous_validation_errors": validation.get("issues", []),
00511:         "previous_response_was_invalid": True,
00512:     }
00513: 
00514:     return f"""
00515: Rispondi esclusivamente con un singolo oggetto JSON valido.
00516: 
00517: REGOLE OBBLIGATORIE:
00518: - Il primo carattere della risposta deve essere {{.
00519: - L'ultimo carattere della risposta deve essere }}.
00520: - Non usare Markdown.
00521: - Non usare blocchi ```json.
00522: - Non scrivere documentazione.
00523: - Non spiegare il progetto.
00524: - Non includere testo prima o dopo il JSON.
00525: - Usa preferred_existing_files solo come reference/style.
00526: - Scrivi nuovi file solo sotto i prefissi consentiti.
00527: - Non modificare il full analysis JSON frame-by-frame.
00528: - scene_script deve contenere codice Python Blender completo, con lettura JSON, keyframe_insert, materiali e modifier.
00529: - scene_script deve usare tutti i frame del full Blender keyframes JSON, non solo i segmenti compatti.
00530: - Non usare placeholder, TODO, pass, o scene minime con solo camera/luce/piano.
00531: 
00532: Schema obbligatorio:
00533: {{
00534:   "implementation_kind": "new_blender_scene_script_from_json",
00535:   "safety": {{
00536:     "does_not_modify_full_analysis_json": true,
00537:     "does_not_modify_project_source_files": true,
00538:     "requires_manual_review": true,
00539:     "needs_blender_run": true
00540:   }},
00541:   "reference_files": [
00542:     {{
00543:       "file": "Scripting/v61b/materials.py",
00544:       "exists_in_project_index": true,
00545:       "reason": "style/source reference only"
00546:     }}
00547:   ],
00548:   "proposed_files": [
00549:     {{
00550:       "file": "indexAI/scene_scripts/generated_scene_builder_candidate.py",
00551:       "kind": "standalone_blender_scene_builder",
00552:       "why": "new scene script, not a project patch"
00553:     }}
00554:   ],
00555:   "implementation_plan": [
00556:     {{
00557:       "reference_file": "Scripting/v61b/materials.py",
00558:       "new_file": "indexAI/scene_scripts/generated_scene_builder_candidate.py",
00559:       "change": "...",
00560:       "why": "...",
00561:       "risk": "low",
00562:       "manual_check": "..."
00563:     }}
00564:   ],
00565:   "new_files_allowed": [
00566:     "indexAI/scene_scripts/...",
00567:     "indexAI/patch_library/..."
00568:   ],
00569:   "scene_script": "import bpy\\n...",
00570:   "notes": ["..."],
00571:   "files_to_review_before_applying": ["..."],
00572:   "expected_panel_or_operator": "..."
00573: }}
00574: 
00575: DATI:
00576: {json.dumps(payload, indent=2, ensure_ascii=False)}
00577: """.strip()
00578: 
00579: 
00580: def safe_parse_json(text: str, fallback_key: str) -> dict[str, Any]:
00581:     try:
00582:         parsed = parse_json_response(text)
00583:         return parsed if isinstance(parsed, dict) else {fallback_key: text, "parse_error": True}
00584:     except Exception:
00585:         return {fallback_key: text, "parse_error": True}
00586: 
00587: 
00588: def extract_python_script(text: str) -> str:
00589:     stripped = text.strip()
00590:     if "```" in stripped:
00591:         parts = stripped.split("```")
00592:         for index, part in enumerate(parts):
00593:             body = part
00594:             if index % 2 == 1:
00595:                 lines = body.splitlines()
00596:                 if lines and lines[0].strip().lower() in {"python", "py"}:
00597:                     body = "\n".join(lines[1:])
00598:                 if "import bpy" in body:
00599:                     return body.strip()
00600:     if "import bpy" in stripped:
00601:         start = stripped.find("from __future__")
00602:         if start < 0:
00603:             start = stripped.find("import bpy")
00604:         return stripped[start:].strip()
00605:     return ""
00606: 
00607: 
00608: def draft_from_raw_python_script(text: str, model: str | None, reason: str) -> dict[str, Any] | None:
00609:     script = extract_python_script(text)
00610:     if not script:
00611:         return None
00612:     new_file = generated_scene_script_relpath()
00613:     reference_files = [
00614:         {
00615:             "file": path,
00616:             "exists_in_project_index": True,
00617:             "reason": "Style/source reference only; not modified by this generated scene script.",
00618:         }
00619:         for path in PREFERRED_IMPLEMENTATION_FILES
00620:         if path in get_indexed_project_files()
00621:     ]
00622:     return {
00623:         "implementation_kind": "new_blender_scene_script_from_json",
00624:         "safety": {
00625:             "does_not_modify_full_analysis_json": True,
00626:             "does_not_modify_project_source_files": True,
00627:             "requires_manual_review": True,
00628:             "needs_blender_run": True,
00629:         },
00630:         "reference_files": reference_files,
00631:         "proposed_files": [
00632:             {
00633:                 "file": new_file,
00634:                 "kind": "standalone_blender_scene_builder",
00635:                 "why": "The model returned raw Python; the pipeline wrapped it into the required review JSON.",
00636:             }
00637:         ],
00638:         "implementation_plan": [
00639:             {
00640:                 "reference_file": item["file"],
00641:                 "new_file": new_file,
00642:                 "change": "Use this source as reference style while reviewing the raw generated Blender script.",
00643:                 "why": "Preserve project structure while creating a separate candidate script.",
00644:                 "risk": "medium",
00645:                 "manual_check": "Run only inside Blender on a disposable scene.",
00646:             }
00647:             for item in reference_files[:6]
00648:         ],
00649:         "new_files_allowed": ["indexAI/scene_scripts/...", "indexAI/patch_library/..."],
00650:         "scene_script": script,
00651:         "support_files": [],
00652:         "notes": [reason, "Raw Python was accepted only after wrapping and normal validation."],
00653:         "files_to_review_before_applying": [item["file"] for item in reference_files],
00654:         "expected_panel_or_operator": "Run as standalone Blender Text script on a new/empty scene.",
00655:         "model": model,
00656:     }
00657: 
00658: 
00659: def get_indexed_project_files() -> set[str]:
00660:     manifest = read_json(PROJECT_MANIFEST_JSON) if PROJECT_MANIFEST_JSON.exists() else {}
00661:     return {item.get("file") for item in manifest.get("files", []) if item.get("file")}
00662: 
00663: 
00664: def validate_implementation_draft(draft: dict[str, Any]) -> dict[str, Any]:
00665:     indexed_files = get_indexed_project_files()
00666: 
00667:     issues: list[str] = []
00668:     reference_files = draft.get("reference_files") or []
00669:     proposed_files = draft.get("proposed_files") or []
00670:     implementation_plan = draft.get("implementation_plan") or []
00671: 
00672:     if draft.get("implementation_kind") != "new_blender_scene_script_from_json":
00673:         issues.append("implementation_kind should be new_blender_scene_script_from_json.")
00674: 
00675:     if not isinstance(reference_files, list) or not reference_files:
00676:         issues.append("No reference_files entries were provided.")
00677:     if not isinstance(proposed_files, list) or not proposed_files:
00678:         issues.append("No proposed_files entries were provided.")
00679:     if not isinstance(implementation_plan, list) or not implementation_plan:
00680:         issues.append("No implementation_plan entries were provided.")
00681: 
00682:     if isinstance(reference_files, list):
00683:         for item in reference_files:
00684:             if not isinstance(item, dict):
00685:                 issues.append("A reference_files entry is not an object.")
00686:                 continue
00687:             file_name = str(item.get("file") or "").replace("\\", "/")
00688:             if not file_name:
00689:                 issues.append("A reference_files entry has no file.")
00690:                 continue
00691:             if file_name not in indexed_files:
00692:                 issues.append(f"Reference file is not in project index: {file_name}")
00693: 
00694:     if isinstance(proposed_files, list):
00695:         for item in proposed_files:
00696:             if not isinstance(item, dict):
00697:                 issues.append("A proposed_files entry is not an object.")
00698:                 continue
00699:             file_name = str(item.get("file") or "").replace("\\", "/")
00700:             if not file_name:
00701:                 issues.append("A proposed_files entry has no file.")
00702:                 continue
00703:             if file_name in indexed_files:
00704:                 issues.append(f"Proposed file must not be an existing source file: {file_name}")
00705:             if not file_name.startswith(ALLOWED_NEW_PREFIXES):
00706:                 issues.append(f"Proposed file is not under an allowed generated-output prefix: {file_name}")
00707: 
00708:     support_files = draft.get("support_files") or []
00709:     if support_files and not isinstance(support_files, list):
00710:         issues.append("support_files must be a list when provided.")
00711:     if isinstance(support_files, list):
00712:         for item in support_files:
00713:             if not isinstance(item, dict):
00714:                 issues.append("A support_files entry is not an object.")
00715:                 continue
00716:             file_name = str(item.get("file") or "").replace("\\", "/")
00717:             if not file_name:
00718:                 issues.append("A support_files entry has no file.")
00719:                 continue
00720:             if file_name in indexed_files:
00721:                 issues.append(f"Support file must not be an existing source file: {file_name}")
00722:             if not file_name.startswith(ALLOWED_NEW_PREFIXES):
00723:                 issues.append(f"Support file is not under an allowed generated-output prefix: {file_name}")
00724:             if "content" not in item:
00725:                 issues.append(f"Support file has no content: {file_name}")
00726: 
00727:     script = str(draft.get("scene_script") or draft.get("hotpatch_candidate_script") or draft.get("script") or "")
00728:     script_lower = script.lower()
00729:     stripped_script = script.strip()
00730:     if len(stripped_script) < 2500:
00731:         issues.append("scene_script is missing or too short.")
00732:     if "import bpy" not in script:
00733:         issues.append("scene_script does not appear to be a Blender Python script.")
00734:     if "json" not in script_lower or "load_json" not in script:
00735:         issues.append("scene_script must load and use the JSON context files.")
00736:     if 'keyframes.get("frames"' not in script and "keyframes.get('frames'" not in script:
00737:         issues.append("scene_script must use the full Blender keyframes JSON frames.")
00738:     if "keyframe_insert" not in script:
00739:         issues.append("scene_script must create Blender keyframes from the audio context.")
00740:     if "modifiers.new" not in script and ".modifiers" not in script:
00741:         issues.append("scene_script must include at least one mesh/modifier-driven visual system.")
00742:     if "materials.new" not in script and ".data.materials" not in script:
00743:         issues.append("scene_script must create or assign materials.")
```
