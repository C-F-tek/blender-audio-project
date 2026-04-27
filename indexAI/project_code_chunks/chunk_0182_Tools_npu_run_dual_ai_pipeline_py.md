# Project Code Chunk 182/212

- File: `Tools/npu/run_dual_ai_pipeline.py`
- Part: `7`
- Lines: `1454-1664`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `from datetime import datetime`, `from typing import Any`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_ai_service_packet import build_ai_service_packet, slugify`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 53; `read_json(path)` line 57; `write_json(path, data)` line 63; `read_optional_json(path)` line 68; `update_track_paths(track_stem, analysis_ai_context)` line 81; `apply_default_input_paths(args)` line 93; `validate_input_files(args)` line 106; `looks_degraded_text(text)` line 126; `deterministic_technical_notes(music_context, project_manifest, reason)` line 142; `run_npu_technical_pass(args)` line 191; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 235; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 317; `build_implementation_prompt(plan, npu_notes, include_manual, gpu_packet, scene_brief, asset_inventory)` line 379; `build_implementation_retry_prompt(plan, invalid_draft, validation)` line 491; `safe_parse_json(text, fallback_key)` line 580; `extract_python_script(text)` line 588; `draft_from_raw_python_script(text, model, reason)` line 608; `get_indexed_project_files()` line 659; `validate_implementation_draft(draft)` line 664; `generated_scene_script_relpath()` line 761; `generated_scene_script_abspath()` line 765; `deterministic_scene_builder_script(track_stem, analysis_json, music_context_json, ai_context_json, blender_keyframes_json, asset_inventory_json, scene_brief)` line 769; `deterministic_support_files(track_stem, scene_brief)` line 1152; `build_fallback_implementation_draft(reason, model, args, scene_brief, asset_inventory)` line 1205; `normalize_implementation_draft(draft, model, args, scene_brief, asset_inventory)` line 1292; `generate_implementation_draft_with_retry(manager, model_name, implementation_prompt, plan, max_new_tokens, args, scene_brief, asset_inventory)` line 1313; `write_brief(plan, creative, technical, npu_notes)` line 1376; `write_implementation_draft(draft)` line 1399; `main()` line 1453
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `DEFAULT_TRACK_STEM`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`, `ALLOWED_NEW_PREFIXES`, `PREFERRED_IMPLEMENTATION_FILES`

## Content
```py
01454:     parser = argparse.ArgumentParser(description="Build code/music contexts, run NPU technical pass and Ollama creative passes.")
01455:     parser.add_argument("--phase", choices=["plan", "implementation", "full"], default="plan")
01456:     parser.add_argument("--track-stem", default=DEFAULT_TRACK_STEM)
01457:     parser.add_argument("--analysis", default=None)
01458:     parser.add_argument("--track-summary", default=None)
01459:     parser.add_argument("--compact-json", default=None)
01460:     parser.add_argument("--analysis-ai-context", default=None)
01461:     parser.add_argument("--blender-keyframes-json", default=None)
01462:     parser.add_argument("--skip-npu", action="store_true")
01463:     parser.add_argument("--skip-ollama", action="store_true")
01464:     parser.add_argument("--include-manual", action="store_true")
01465:     parser.add_argument("--creative-model", default="gpt-oss:20b")
01466:     parser.add_argument("--technical-model", default="qwen2.5-coder:14b")
01467:     parser.add_argument("--ollama-base-url", default=None)
01468:     parser.add_argument("--npu-python", default=str(DEFAULT_NPU_PYTHON))
01469:     parser.add_argument("--npu-model-dir", default=str(DEFAULT_MODEL_DIR))
01470:     parser.add_argument("--npu-chunk-tokens", type=int, default=520)
01471:     parser.add_argument("--npu-reduce-tokens", type=int, default=650)
01472:     parser.add_argument("--npu-final-tokens", type=int, default=900)
01473:     parser.add_argument("--max-new-tokens", type=int, default=1800)
01474:     parser.add_argument("--force-npu", action="store_true", help="Re-run NPU notes even when reusable notes exist.")
01475:     parser.add_argument("--scene-brief", default=None, help="Optional scene director brief JSON created by the workflow shell/GUI.")
01476:     parser.add_argument("--asset-inventory", default=None, help="Optional asset inventory JSON with known local Blender/FBX/GLTF assets.")
01477:     args = parser.parse_args()
01478: 
01479:     apply_default_input_paths(args)
01480:     update_track_paths(args.track_stem, args.analysis_ai_context)
01481: 
01482:     if not Path(args.analysis).exists():
01483:         raise FileNotFoundError(f"Analysis JSON missing: {args.analysis}")
01484:     if not Path(args.track_summary).exists():
01485:         raise FileNotFoundError(
01486:             f"Track summary missing: {args.track_summary}\n"
01487:             "Crea prima il track summary o usa la workflow shell che ora lo ripara automaticamente."
01488:         )
01489:     if args.phase == "implementation" and not DUAL_PLAN_JSON.exists():
01490:         raise FileNotFoundError(f"Dual AI scene plan missing, run phase plan first: {DUAL_PLAN_JSON}")
01491: 
01492:     build_code_context()
01493:     project_manifest = build_project_ai_index()
01494:     build_music_context(
01495:         analysis_path=Path(args.analysis),
01496:         track_summary_path=Path(args.track_summary),
01497:         compact_json_path=Path(args.compact_json),
01498:         analysis_ai_context_path=Path(args.analysis_ai_context),
01499:         blender_keyframes_path=Path(args.blender_keyframes_json),
01500:     )
01501:     if args.include_manual:
01502:         build_manual_context(limit_files=80)
01503:     validate_input_files(args)
01504:     music_context = read_json(MUSIC_AI_CONTEXT)
01505:     scene_brief = read_optional_json(args.scene_brief)
01506:     asset_inventory = read_optional_json(args.asset_inventory)
01507: 
01508:     npu_notes = ""
01509:     if not args.skip_npu:
01510:         if args.phase == "implementation" and not args.force_npu and NPU_TECH_MD.exists():
01511:             npu_notes = read_text(NPU_TECH_MD)
01512:             print(f"[NPU] Reusing plan technical notes: {NPU_TECH_MD}")
01513:         else:
01514:             report = npu_preflight(args.npu_python, args.npu_model_dir)
01515:             write_npu_preflight_report(report, NPU_PREFLIGHT_JSON)
01516:             if report.get("ready"):
01517:                 try:
01518:                     npu_notes = run_npu_technical_pass(args)
01519:                 except Exception as exc:
01520:                     npu_notes = f"NPU technical pass unavailable after ready preflight: {exc}"
01521:                     NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
01522:             else:
01523:                 npu_notes = "NPU not ready. Preflight:\n" + json.dumps(report, indent=2, ensure_ascii=False)
01524:                 NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
01525: 
01526:         if looks_degraded_text(npu_notes):
01527:             npu_notes = deterministic_technical_notes(
01528:                 music_context=music_context,
01529:                 project_manifest=project_manifest,
01530:                 reason="degraded_or_too_short_npu_output",
01531:             )
01532:             NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
01533:             if args.phase == "implementation":
01534:                 NPU_IMPLEMENTATION_NOTES.write_text(npu_notes, encoding="utf-8")
01535:             print("[WARN] NPU notes looked degraded; deterministic technical notes were used.")
01536:     else:
01537:         npu_notes = deterministic_technical_notes(
01538:             music_context=music_context,
01539:             project_manifest=project_manifest,
01540:             reason="npu_skipped_gpu_heavy_mode",
01541:         )
01542:         NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
01543: 
01544:     service_packet_info = build_ai_service_packet(
01545:         track_stem=TRACK_STEM,
01546:         analysis_path=Path(args.analysis),
01547:         track_summary_path=Path(args.track_summary),
01548:         music_context_path=Path(args.compact_json),
01549:         analysis_ai_context_path=Path(args.analysis_ai_context),
01550:         blender_keyframes_path=Path(args.blender_keyframes_json),
01551:         dual_plan_path=DUAL_PLAN_JSON if DUAL_PLAN_JSON.exists() else None,
01552:         npu_notes=npu_notes,
01553:         npu_status="skipped_gpu_heavy_mode" if args.skip_npu else "router_capsule_ready",
01554:         scene_brief=scene_brief,
01555:         asset_inventory=asset_inventory,
01556:     )
01557:     gpu_task_packet = service_packet_info["gpu_packet"]
01558: 
01559:     if args.phase == "implementation":
01560:         if args.skip_ollama:
01561:             draft = build_fallback_implementation_draft(
01562:                 reason="Ollama skipped; deterministic standalone scene script generated.",
01563:                 model=None,
01564:                 args=args,
01565:                 scene_brief=scene_brief,
01566:                 asset_inventory=asset_inventory,
01567:             )
01568:             write_implementation_draft(draft)
01569:         else:
01570:             plan_output = read_json(DUAL_PLAN_JSON)
01571:             plan = plan_output.get("final_plan", plan_output)
01572:             manager_kwargs = {}
01573:             if args.ollama_base_url:
01574:                 manager_kwargs["base_url"] = args.ollama_base_url
01575:             with OllamaModelManager(**manager_kwargs) as manager:
01576:                 implementation_prompt = build_implementation_prompt(plan, npu_notes, args.include_manual, gpu_task_packet, scene_brief, asset_inventory)
01577:                 draft = generate_implementation_draft_with_retry(
01578:                     manager=manager,
01579:                     model_name=args.technical_model,
01580:                     implementation_prompt=implementation_prompt,
01581:                     plan=plan,
01582:                     max_new_tokens=args.max_new_tokens,
01583:                     args=args,
01584:                     scene_brief=scene_brief,
01585:                     asset_inventory=asset_inventory,
01586:                 )
01587:                 write_implementation_draft(draft)
01588: 
01589:         print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
01590:         print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
01591:         print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")
01592:         return
01593: 
01594:     if args.skip_ollama:
01595:         creative = {"skipped": True}
01596:         technical = {"skipped": True}
01597:         plan = {
01598:             "pipeline_policy": {
01599:                 "use_full_blender_keyframes_json": True,
01600:                 "ai_context_is_analysis_only": True,
01601:                 "ollama_model_switch_policy": "unload previous model before loading next",
01602:             },
01603:             "recommended_scene_plan": {
01604:                 "summary": "Ollama skipped; use NPU notes only.",
01605:                 "priority_changes": [],
01606:                 "defer_changes": [],
01607:             },
01608:         }
01609:     else:
01610:         manager_kwargs = {}
01611:         if args.ollama_base_url:
01612:             manager_kwargs["base_url"] = args.ollama_base_url
01613: 
01614:         with OllamaModelManager(**manager_kwargs) as manager:
01615:             creative_prompt = build_creative_scene_prompt(music_context, npu_notes, read_text(PROJECT_INDEX_MD))
01616:             creative_text, creative_model = manager.generate(
01617:                 args.creative_model,
01618:                 creative_prompt,
01619:                 max_new_tokens=args.max_new_tokens,
01620:                 temperature=0.20,
01621:             )
01622:             creative = safe_parse_json(creative_text, "raw_creative_response")
01623:             creative["model"] = creative_model
01624: 
01625:             technical_prompt = build_music_prompt(music_context)
01626:             technical_text, technical_model = manager.generate(
01627:                 args.technical_model,
01628:                 technical_prompt,
01629:                 max_new_tokens=args.max_new_tokens,
01630:                 temperature=0.10,
01631:             )
01632:             technical = safe_parse_json(technical_text, "raw_technical_response")
01633:             technical["model"] = technical_model
01634: 
01635:             merge_prompt = build_merge_prompt(music_context, npu_notes, creative, technical)
01636:             merge_text, merge_model = manager.generate(
01637:                 args.technical_model,
01638:                 merge_prompt,
01639:                 max_new_tokens=args.max_new_tokens,
01640:                 temperature=0.08,
01641:             )
01642:             plan = safe_parse_json(merge_text, "raw_plan_response")
01643:             plan["merge_model"] = merge_model
01644: 
01645:             if args.phase == "full":
01646:                 implementation_prompt = build_implementation_prompt(plan, npu_notes, args.include_manual, gpu_task_packet, scene_brief, asset_inventory)
01647:                 draft = generate_implementation_draft_with_retry(
01648:                     manager=manager,
01649:                     model_name=args.technical_model,
01650:                     implementation_prompt=implementation_prompt,
01651:                     plan=plan,
01652:                     max_new_tokens=args.max_new_tokens,
01653:                     args=args,
01654:                     scene_brief=scene_brief,
01655:                     asset_inventory=asset_inventory,
01656:                 )
01657:                 write_implementation_draft(draft)
01658: 
01659:     output = {
01660:         "generated_at": datetime.now().isoformat(timespec="seconds"),
01661:         "track_stem": TRACK_STEM,
01662:         "policy": {
01663:             "full_blender_keyframes_json": str(Path(args.blender_keyframes_json)),
01664:             "ai_context_json": str(MUSIC_AI_CONTEXT),
```
