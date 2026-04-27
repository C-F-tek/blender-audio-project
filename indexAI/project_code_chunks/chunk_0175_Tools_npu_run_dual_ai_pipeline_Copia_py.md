# Project Code Chunk 175/212

- File: `Tools/npu/run_dual_ai_pipeline - Copia.py`
- Part: `3`
- Lines: `507-705`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `argparse`, `json`, `subprocess`, `sys`, `from datetime import datetime`, `from build_music_context import build_music_context`, `from build_npu_code_context import main`, `from build_blender_manual_context import build_manual_context`, `from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index`, `from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report`, `from ollama_runtime import OllamaModelManager, parse_json_response`, `from run_ollama_music_agent import build_prompt`, `from run_ollama_music_agent import markdown_from_insights`
- Functions: `read_text(path)` line 38; `read_json(path)` line 42; `write_json(path, data)` line 47; `validate_input_files(args)` line 52; `looks_degraded_text(text)` line 72; `deterministic_technical_notes(music_context, project_manifest, reason)` line 85; `run_npu_technical_pass(args)` line 134; `build_creative_scene_prompt(music_context, npu_notes, project_index)` line 178; `build_merge_prompt(music_context, npu_notes, creative, technical)` line 254; `build_implementation_prompt(plan, npu_notes, include_manual)` line 305; `safe_parse_json(text, fallback_key)` line 373; `write_brief(plan, creative, technical, npu_notes)` line 380; `validate_implementation_draft(draft)` line 403; `write_implementation_draft(draft)` line 450; `main()` line 478
- Assignments: `ROOT`, `TOOLS_DIR`, `OUTPUT_DIR`, `TRACK_STEM`, `MUSIC_AI_CONTEXT`, `DUAL_PLAN_JSON`, `DUAL_BRIEF_MD`, `OLLAMA_INSIGHTS_JSON`, `OLLAMA_INSIGHTS_MD`, `NPU_TECH_MD`, `NPU_PREFLIGHT_JSON`, `IMPLEMENTATION_DRAFT_JSON`, `IMPLEMENTATION_SCRIPT`, `IMPLEMENTATION_NOTES`, `NPU_IMPLEMENTATION_NOTES`

## Content
```py
00507:     MUSIC_AI_CONTEXT = Path(args.analysis_ai_context)
00508:     DUAL_PLAN_JSON = OUTPUT_DIR / f"{TRACK_STEM}_dual_ai_scene_plan.json"
00509:     OLLAMA_INSIGHTS_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ollama_music_insights.json"
00510:     IMPLEMENTATION_DRAFT_JSON = OUTPUT_DIR / f"{TRACK_STEM}_ai_implementation_draft.json"
00511: 
00512:     if not Path(args.analysis).exists():
00513:         raise FileNotFoundError(f"Analysis JSON missing: {args.analysis}")
00514:     if not Path(args.track_summary).exists():
00515:         raise FileNotFoundError(
00516:             f"Track summary missing: {args.track_summary}\n"
00517:             "Crea prima il track summary o usa la workflow shell che ora lo ripara automaticamente."
00518:         )
00519:     if args.phase == "implementation" and not DUAL_PLAN_JSON.exists():
00520:         raise FileNotFoundError(f"Dual AI scene plan missing, run phase plan first: {DUAL_PLAN_JSON}")
00521: 
00522:     build_code_context()
00523:     project_manifest = build_project_ai_index()
00524:     build_music_context(
00525:         analysis_path=Path(args.analysis),
00526:         track_summary_path=Path(args.track_summary),
00527:         compact_json_path=Path(args.compact_json),
00528:         analysis_ai_context_path=Path(args.analysis_ai_context),
00529:         blender_keyframes_path=Path(args.blender_keyframes_json),
00530:     )
00531:     if args.include_manual:
00532:         build_manual_context(limit_files=80)
00533:     validate_input_files(args)
00534:     music_context = read_json(MUSIC_AI_CONTEXT)
00535: 
00536:     npu_notes = ""
00537:     if not args.skip_npu:
00538:         if args.phase == "implementation" and not args.force_npu and NPU_TECH_MD.exists():
00539:             npu_notes = read_text(NPU_TECH_MD)
00540:             print(f"[NPU] Reusing plan technical notes: {NPU_TECH_MD}")
00541:         else:
00542:             report = npu_preflight(args.npu_python, args.npu_model_dir)
00543:             write_npu_preflight_report(report, NPU_PREFLIGHT_JSON)
00544:             if report.get("ready"):
00545:                 try:
00546:                     npu_notes = run_npu_technical_pass(args)
00547:                 except Exception as exc:
00548:                     npu_notes = f"NPU technical pass unavailable after ready preflight: {exc}"
00549:                     NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
00550:             else:
00551:                 npu_notes = "NPU not ready. Preflight:\n" + json.dumps(report, indent=2, ensure_ascii=False)
00552:                 NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
00553: 
00554:         if looks_degraded_text(npu_notes):
00555:             npu_notes = deterministic_technical_notes(
00556:                 music_context=music_context,
00557:                 project_manifest=project_manifest,
00558:                 reason="degraded_or_too_short_npu_output",
00559:             )
00560:             NPU_TECH_MD.write_text(npu_notes, encoding="utf-8")
00561:             if args.phase == "implementation":
00562:                 NPU_IMPLEMENTATION_NOTES.write_text(npu_notes, encoding="utf-8")
00563:             print("[WARN] NPU notes looked degraded; deterministic technical notes were used.")
00564: 
00565:     if args.phase == "implementation":
00566:         if args.skip_ollama:
00567:             draft = {
00568:                 "implementation_kind": "existing_project_patch_plan",
00569:                 "safety": {
00570:                     "does_not_modify_full_analysis_json": True,
00571:                     "requires_manual_review": True,
00572:                     "needs_blender_run": True,
00573:                 },
00574:                 "target_files": [],
00575:                 "patch_plan": [],
00576:                 "hotpatch_candidate_script": "",
00577:                 "notes": ["Ollama skipped; implementation draft intentionally contains no generated patch."],
00578:                 "files_to_review_before_applying": [],
00579:                 "expected_panel_or_operator": "",
00580:             }
00581:             write_implementation_draft(draft)
00582:         else:
00583:             plan_output = read_json(DUAL_PLAN_JSON)
00584:             plan = plan_output.get("final_plan", plan_output)
00585:             manager_kwargs = {}
00586:             if args.ollama_base_url:
00587:                 manager_kwargs["base_url"] = args.ollama_base_url
00588:             try:
00589:                 with OllamaModelManager(**manager_kwargs) as manager:
00590:                     implementation_prompt = build_implementation_prompt(plan, npu_notes, args.include_manual)
00591:                     implementation_text, implementation_model = manager.generate(
00592:                         args.technical_model,
00593:                         implementation_prompt,
00594:                         max_new_tokens=max(args.max_new_tokens, 2400),
00595:                         temperature=0.05,
00596:                     )
00597:                     draft = safe_parse_json(implementation_text, "raw_implementation_response")
00598:                     draft["model"] = implementation_model
00599:                     write_implementation_draft(draft)
00600:             finally:
00601:                 pass
00602: 
00603:         print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
00604:         print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
00605:         print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")
00606:         return
00607: 
00608:     if args.skip_ollama:
00609:         creative = {"skipped": True}
00610:         technical = {"skipped": True}
00611:         plan = {
00612:             "pipeline_policy": {
00613:                 "use_full_blender_keyframes_json": True,
00614:                 "ai_context_is_analysis_only": True,
00615:                 "ollama_model_switch_policy": "unload previous model before loading next",
00616:             },
00617:             "recommended_scene_plan": {
00618:                 "summary": "Ollama skipped; use NPU notes only.",
00619:                 "priority_changes": [],
00620:                 "defer_changes": [],
00621:             },
00622:         }
00623:     else:
00624:         manager_kwargs = {}
00625:         if args.ollama_base_url:
00626:             manager_kwargs["base_url"] = args.ollama_base_url
00627: 
00628:         with OllamaModelManager(**manager_kwargs) as manager:
00629:             creative_prompt = build_creative_scene_prompt(music_context, npu_notes, read_text(PROJECT_INDEX_MD))
00630:             creative_text, creative_model = manager.generate(
00631:                 args.creative_model,
00632:                 creative_prompt,
00633:                 max_new_tokens=args.max_new_tokens,
00634:                 temperature=0.20,
00635:             )
00636:             creative = safe_parse_json(creative_text, "raw_creative_response")
00637:             creative["model"] = creative_model
00638: 
00639:             technical_prompt = build_music_prompt(music_context)
00640:             technical_text, technical_model = manager.generate(
00641:                 args.technical_model,
00642:                 technical_prompt,
00643:                 max_new_tokens=args.max_new_tokens,
00644:                 temperature=0.10,
00645:             )
00646:             technical = safe_parse_json(technical_text, "raw_technical_response")
00647:             technical["model"] = technical_model
00648: 
00649:             merge_prompt = build_merge_prompt(music_context, npu_notes, creative, technical)
00650:             merge_text, merge_model = manager.generate(
00651:                 args.technical_model,
00652:                 merge_prompt,
00653:                 max_new_tokens=args.max_new_tokens,
00654:                 temperature=0.08,
00655:             )
00656:             plan = safe_parse_json(merge_text, "raw_plan_response")
00657:             plan["merge_model"] = merge_model
00658: 
00659:             if args.phase in {"implementation", "full"}:
00660:                 implementation_prompt = build_implementation_prompt(plan, npu_notes, args.include_manual)
00661:                 implementation_text, implementation_model = manager.generate(
00662:                     args.technical_model,
00663:                     implementation_prompt,
00664:                     max_new_tokens=max(args.max_new_tokens, 2400),
00665:                     temperature=0.06,
00666:                 )
00667:                 draft = safe_parse_json(implementation_text, "raw_implementation_response")
00668:                 draft["model"] = implementation_model
00669:                 write_implementation_draft(draft)
00670: 
00671:     output = {
00672:         "generated_at": datetime.now().isoformat(timespec="seconds"),
00673:         "track_stem": TRACK_STEM,
00674:         "policy": {
00675:             "full_blender_keyframes_json": str(Path(args.blender_keyframes_json)),
00676:             "ai_context_json": str(MUSIC_AI_CONTEXT),
00677:             "model_switch_rule": "Unload/stop previous Ollama model before loading the next model.",
00678:             "phase": args.phase,
00679:             "manual_context_used": args.include_manual,
00680:             "implementation_draft_json": str(IMPLEMENTATION_DRAFT_JSON) if args.phase in {"implementation", "full"} else None,
00681:             "implementation_script": str(IMPLEMENTATION_SCRIPT) if args.phase in {"implementation", "full"} else None,
00682:         },
00683:         "npu_preflight_json": str(NPU_PREFLIGHT_JSON),
00684:         "npu_technical_notes_md": str(NPU_TECH_MD),
00685:         "creative_ollama": creative,
00686:         "technical_ollama": technical,
00687:         "final_plan": plan,
00688:     }
00689: 
00690:     write_json(DUAL_PLAN_JSON, output)
00691:     write_json(OLLAMA_INSIGHTS_JSON, technical)
00692:     OLLAMA_INSIGHTS_MD.write_text(markdown_from_insights(technical, technical.get("model", args.technical_model)), encoding="utf-8")
00693:     write_brief(plan, creative, technical, npu_notes)
00694: 
00695:     print(f"[OK] Wrote: {DUAL_PLAN_JSON}")
00696:     print(f"[OK] Wrote: {DUAL_BRIEF_MD}")
00697:     print(f"[OK] Wrote: {NPU_TECH_MD}")
00698:     if args.phase in {"implementation", "full"} and not args.skip_ollama:
00699:         print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
00700:         print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
00701:         print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")
00702: 
00703: 
00704: if __name__ == "__main__":
00705:     main()
```
