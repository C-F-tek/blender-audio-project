# Project Code Chunk 181/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `6`
- Lines: `1213-1453`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
01213:     selected_files = [path for path in PREFERRED_IMPLEMENTATION_FILES if path in indexed_files]
01214:     new_file = generated_scene_script_relpath()
01215:     scene_script = deterministic_scene_builder_script(
01216:         track_stem=TRACK_STEM,
01217:         analysis_json=str(Path(args.analysis)) if args else "",
01218:         music_context_json=str(Path(args.compact_json)) if args else "",
01219:         ai_context_json=str(Path(args.analysis_ai_context)) if args else "",
01220:         blender_keyframes_json=str(Path(args.blender_keyframes_json)) if args else "",
01221:         asset_inventory_json=str(Path(args.asset_inventory)) if args and getattr(args, "asset_inventory", None) else "",
01222:         scene_brief=scene_brief,
01223:     )
01224: 
01225:     reference_files = [
01226:         {
01227:             "file": path,
01228:             "exists_in_project_index": True,
01229:             "reason": "Style/source reference only; not modified by this generated scene script.",
01230:         }
01231:         for path in selected_files
01232:     ]
01233: 
01234:     implementation_plan = [
01235:         {
01236:             "reference_file": path,
01237:             "new_file": new_file,
01238:             "change": "Use this file as structure/style reference for the standalone scene builder.",
01239:             "why": "The generated product is a new Blender scene script, not a patch to the existing project.",
01240:             "risk": "medium",
01241:             "manual_check": "Open the generated script in Blender Text Editor and run on an empty scene.",
01242:         }
01243:         for path in selected_files
01244:     ]
01245: 
01246:     draft: dict[str, Any] = {
01247:         "implementation_kind": "new_blender_scene_script_from_json",
01248:         "safety": {
01249:             "does_not_modify_full_analysis_json": True,
01250:             "does_not_modify_project_source_files": True,
01251:             "requires_manual_review": True,
01252:             "needs_blender_run": True,
01253:         },
01254:         "reference_files": reference_files,
01255:         "proposed_files": [
01256:             {
01257:                 "file": new_file,
01258:                 "kind": "standalone_blender_scene_builder",
01259:                 "why": "Creates a new scene from JSON context while preserving the original project as reference only.",
01260:             }
01261:         ],
01262:         "implementation_plan": implementation_plan,
01263:         "new_files_allowed": [
01264:             "indexAI/scene_scripts/...",
01265:             "indexAI/patch_library/...",
01266:         ],
01267:         "scene_script": scene_script,
01268:         "support_files": deterministic_support_files(TRACK_STEM, scene_brief),
01269:         "notes": [
01270:             f"Deterministic fallback generated because implementation draft was invalid: {reason}",
01271:             "This is a standalone scene builder; it does not patch the existing project files.",
01272:             "NPU service work is represented as manifest/split-plan support files.",
01273:         ],
01274:         "files_to_review_before_applying": [item["file"] for item in reference_files],
01275:         "expected_panel_or_operator": "Run as standalone Blender Text script on a new/empty scene.",
01276:     }
01277: 
01278:     if model:
01279:         draft["model"] = model
01280:     if asset_inventory:
01281:         draft["asset_inventory_used"] = {
01282:             "asset_count": asset_inventory.get("asset_count"),
01283:             "primary_assets": [
01284:                 asset for asset in asset_inventory.get("assets", [])
01285:                 if asset.get("role") in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}
01286:             ][:10],
01287:         }
01288: 
01289:     return draft
01290: 
01291: 
01292: def normalize_implementation_draft(
01293:     draft: dict[str, Any],
01294:     model: str | None = None,
01295:     args: argparse.Namespace | None = None,
01296:     scene_brief: dict[str, Any] | None = None,
01297:     asset_inventory: dict[str, Any] | None = None,
01298: ) -> dict[str, Any]:
01299:     if not isinstance(draft, dict):
01300:         return build_fallback_implementation_draft("draft is not a dictionary", model=model, args=args, scene_brief=scene_brief, asset_inventory=asset_inventory)
01301: 
01302:     validation = validate_implementation_draft(draft)
01303:     if validation.get("ok"):
01304:         return draft
01305: 
01306:     reason = "; ".join(validation.get("issues", [])) or "unknown validation failure"
01307:     fallback = build_fallback_implementation_draft(reason, model=model, args=args, scene_brief=scene_brief, asset_inventory=asset_inventory)
01308:     fallback["raw_invalid_draft"] = draft
01309:     fallback["original_validation"] = validation
01310:     return fallback
01311: 
01312: 
01313: def generate_implementation_draft_with_retry(
01314:     manager: OllamaModelManager,
01315:     model_name: str,
01316:     implementation_prompt: str,
01317:     plan: dict[str, Any],
01318:     max_new_tokens: int,
01319:     args: argparse.Namespace | None = None,
01320:     scene_brief: dict[str, Any] | None = None,
01321:     asset_inventory: dict[str, Any] | None = None,
01322: ) -> dict[str, Any]:
01323:     implementation_text, implementation_model = manager.generate(
01324:         model_name,
01325:         implementation_prompt,
01326:         max_new_tokens=max(max_new_tokens, 6000),
01327:         temperature=0.01,
01328:     )
01329: 
01330:     draft = safe_parse_json(implementation_text, "raw_implementation_response")
01331:     draft["model"] = implementation_model
01332:     if draft.get("parse_error"):
01333:         raw_python = draft_from_raw_python_script(
01334:             implementation_text,
01335:             implementation_model,
01336:             "Model returned raw Python instead of JSON on first implementation pass.",
01337:         )
01338:         if raw_python and validate_implementation_draft(raw_python).get("ok"):
01339:             return raw_python
01340: 
01341:     validation = validate_implementation_draft(draft)
01342:     if validation.get("ok"):
01343:         return draft
01344: 
01345:     retry_prompt = build_implementation_retry_prompt(
01346:         plan=plan,
01347:         invalid_draft=draft,
01348:         validation=validation,
01349:     )
01350: 
01351:     retry_text, retry_model = manager.generate(
01352:         model_name,
01353:         retry_prompt,
01354:         max_new_tokens=max(max_new_tokens, 7000),
01355:         temperature=0.01,
01356:     )
01357: 
01358:     retry_draft = safe_parse_json(retry_text, "raw_implementation_retry_response")
01359:     retry_draft["model"] = retry_model
01360:     if retry_draft.get("parse_error"):
01361:         raw_python = draft_from_raw_python_script(
01362:             retry_text,
01363:             retry_model,
01364:             "Model returned raw Python instead of JSON on retry pass.",
01365:         )
01366:         if raw_python and validate_implementation_draft(raw_python).get("ok"):
01367:             raw_python["retry_of_invalid_draft"] = draft
01368:             raw_python["first_validation"] = validation
01369:             return raw_python
01370:     retry_draft["retry_of_invalid_draft"] = draft
01371:     retry_draft["first_validation"] = validation
01372: 
01373:     return normalize_implementation_draft(retry_draft, model=retry_model, args=args, scene_brief=scene_brief, asset_inventory=asset_inventory)
01374: 
01375: 
01376: def write_brief(plan: dict[str, Any], creative: dict[str, Any], technical: dict[str, Any], npu_notes: str) -> None:
01377:     lines = [
01378:         "# Dual AI Blender Agent Brief\n\n",
01379:         f"Generated: `{datetime.now().isoformat(timespec='seconds')}`\n\n",
01380:         "## Policy\n",
01381:         "- Full Blender keyframe JSON remains untouched.\n",
01382:         "- AI compact context is analysis only.\n",
01383:         "- Ollama model switch unloads the previous model before loading the next.\n\n",
01384:         "## Recommended Plan\n",
01385:         json.dumps(plan.get("recommended_scene_plan", plan), indent=2, ensure_ascii=False),
01386:         "\n\n## Audio Mapping\n",
01387:         json.dumps(plan.get("audio_mapping_plan", {}), indent=2, ensure_ascii=False),
01388:         "\n\n## Creative Source\n",
01389:         json.dumps(creative, indent=2, ensure_ascii=False)[:12000],
01390:         "\n\n## Technical Source\n",
01391:         json.dumps(technical, indent=2, ensure_ascii=False)[:12000],
01392:         "\n\n## NPU Notes\n",
01393:         npu_notes[:12000],
01394:         "\n",
01395:     ]
01396:     DUAL_BRIEF_MD.write_text("".join(lines), encoding="utf-8")
01397: 
01398: 
01399: def write_implementation_draft(draft: dict[str, Any]) -> None:
01400:     draft["validation"] = validate_implementation_draft(draft)
01401:     write_json(IMPLEMENTATION_DRAFT_JSON, draft)
01402: 
01403:     script = draft.get("scene_script", draft.get("hotpatch_candidate_script", draft.get("script", "")))
01404:     if not script:
01405:         script = (
01406:             "# AI implementation draft did not contain a scene script.\n"
01407:             "# Review the JSON draft for reference_files, proposed_files, validation and notes.\n"
01408:         )
01409:     IMPLEMENTATION_SCRIPT.write_text(str(script).rstrip() + "\n", encoding="utf-8")
01410:     scene_path = generated_scene_script_abspath()
01411:     scene_path.parent.mkdir(parents=True, exist_ok=True)
01412:     scene_path.write_text(str(script).rstrip() + "\n", encoding="utf-8")
01413: 
01414:     written_support_files: list[str] = []
01415:     for item in draft.get("support_files", []) or []:
01416:         if not isinstance(item, dict):
01417:             continue
01418:         relpath = str(item.get("file") or "").replace("\\", "/")
01419:         if not relpath.startswith(ALLOWED_NEW_PREFIXES):
01420:             continue
01421:         support_path = ROOT / relpath
01422:         support_path.parent.mkdir(parents=True, exist_ok=True)
01423:         support_path.write_text(str(item.get("content", "")).rstrip() + "\n", encoding="utf-8")
01424:         written_support_files.append(str(support_path))
01425:     if written_support_files:
01426:         draft["written_support_files"] = written_support_files
01427:         write_json(IMPLEMENTATION_DRAFT_JSON, draft)
01428: 
01429:     notes = [
01430:         "# Generated Implementation Notes\n\n",
01431:         "This file is an AI draft. Review before loading in Blender.\n\n",
01432:         "## Validation\n",
01433:         json.dumps(draft.get("validation", {}), indent=2, ensure_ascii=False),
01434:         "\n\n",
01435:         "## Safety\n",
01436:         json.dumps(draft.get("safety", {}), indent=2, ensure_ascii=False),
01437:         "\n\n## Notes\n",
01438:     ]
01439:     for note in draft.get("notes", []):
01440:         notes.append(f"- {note}\n")
01441:     notes.append("\n## Files To Review\n")
01442:     for path in draft.get("files_to_review_before_applying", []):
01443:         notes.append(f"- `{path}`\n")
01444:     notes.append("\n## Generated Scene Script\n")
01445:     notes.append(f"- `{scene_path}`\n")
01446:     if written_support_files:
01447:         notes.append("\n## Generated Support Files\n")
01448:         for path in written_support_files:
01449:             notes.append(f"- `{path}`\n")
01450:     IMPLEMENTATION_NOTES.write_text("".join(notes), encoding="utf-8")
01451: 
01452: 
01453: def main() -> None:
```
