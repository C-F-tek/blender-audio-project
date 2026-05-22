from __future__ import annotations

from .common import *  # noqa: F403
from .implementation import *  # noqa: F403
from .prompts import build_creative_scene_prompt, build_merge_prompt
from .technical import run_npu_technical_pass
from .writers import write_brief, write_implementation_draft

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build code/music contexts, run NPU technical pass and Ollama creative passes."
    )
    parser.add_argument("--phase", choices=["plan", "implementation", "full"], default="plan")
    parser.add_argument("--track-stem", default=DEFAULT_TRACK_STEM)
    parser.add_argument("--analysis", default=None)
    parser.add_argument("--track-summary", default=None)
    parser.add_argument("--compact-json", default=None)
    parser.add_argument("--analysis-ai-context", default=None)
    parser.add_argument("--blender-keyframes-json", default=None)
    parser.add_argument("--skip-npu", action="store_true")
    parser.add_argument("--skip-ollama", action="store_true")
    parser.add_argument("--include-manual", action="store_true")
    parser.add_argument("--creative-model", default="qwen2.5-coder:14b")
    parser.add_argument("--technical-model", default="qwen2.5-coder:14b")
    parser.add_argument("--ollama-base-url", default=None)
    parser.add_argument("--npu-python", default=str(DEFAULT_NPU_PYTHON))
    parser.add_argument("--npu-model-dir", default=str(DEFAULT_MODEL_DIR))
    parser.add_argument("--npu-chunk-tokens", type=int, default=520)
    parser.add_argument("--npu-reduce-tokens", type=int, default=650)
    parser.add_argument("--npu-final-tokens", type=int, default=900)
    parser.add_argument("--max-new-tokens", type=int, default=1800)
    parser.add_argument(
        "--force-npu", action="store_true", help="Re-run NPU notes even when reusable notes exist."
    )
    parser.add_argument(
        "--scene-brief",
        default=None,
        help="Optional scene director brief JSON created by the workflow shell/GUI.",
    )
    parser.add_argument(
        "--asset-inventory",
        default=None,
        help="Optional asset inventory JSON with known local Blender/FBX/GLTF assets.",
    )
    args = parser.parse_args()

    apply_default_input_paths(args)
    update_track_paths(args.track_stem, args.analysis_ai_context)

    if not Path(args.analysis).exists():
        raise FileNotFoundError(f"Analysis JSON missing: {args.analysis}")
    if not Path(args.track_summary).exists():
        raise FileNotFoundError(
            f"Track summary missing: {args.track_summary}\n"
            "Crea prima il track summary o usa la workflow shell che ora lo ripara automaticamente."
        )
    if args.phase == "implementation" and not DUAL_PLAN_JSON.exists():
        raise FileNotFoundError(
            f"Dual AI scene plan missing, run phase plan first: {DUAL_PLAN_JSON}"
        )

    build_code_context()
    project_manifest = build_project_ai_index()
    build_music_context(
        analysis_path=Path(args.analysis),
        track_summary_path=Path(args.track_summary),
        compact_json_path=Path(args.compact_json),
        analysis_ai_context_path=Path(args.analysis_ai_context),
        blender_keyframes_path=Path(args.blender_keyframes_json),
    )
    if args.include_manual:
        build_manual_context(limit_files=80)
    validate_input_files(args)
    music_context = read_json(MUSIC_AI_CONTEXT)
    scene_brief = read_optional_json(args.scene_brief)
    asset_inventory = read_optional_json(args.asset_inventory)

    npu_notes = ""
    if not args.skip_npu:
        if args.phase == "implementation" and not args.force_npu and NPU_TECH_MD.exists():
            npu_notes = read_text(NPU_TECH_MD)
            print(f"[NPU] Reusing plan technical notes: {NPU_TECH_MD}")
        else:
            raw_report = npu_preflight(args.npu_python, args.npu_model_dir)
            report = normalize_npu_preflight_report(
                raw_report,
                npu_python=args.npu_python,
                npu_model_dir=args.npu_model_dir,
            )
            write_legacy_npu_preflight_report(report, NPU_PREFLIGHT_JSON)
            if report.get("ready"):
                try:
                    npu_notes = run_npu_technical_pass(args)
                except Exception as exc:
                    npu_notes = f"NPU technical pass unavailable after ready preflight: {exc}"
                    write_legacy_text_output(NPU_TECH_MD, npu_notes)
            else:
                npu_notes = "NPU not ready. Preflight:\n" + json.dumps(
                    report, indent=2, ensure_ascii=False
                )
                write_legacy_text_output(NPU_TECH_MD, npu_notes)

        if looks_degraded_text(npu_notes):
            npu_notes = deterministic_technical_notes(
                music_context=music_context,
                project_manifest=project_manifest,
                reason="degraded_or_too_short_npu_output",
            )
            write_legacy_text_output(NPU_TECH_MD, npu_notes)
            if args.phase == "implementation":
                write_legacy_text_output(NPU_IMPLEMENTATION_NOTES, npu_notes)
            print("[WARN] NPU notes looked degraded; deterministic technical notes were used.")
    else:
        npu_notes = deterministic_technical_notes(
            music_context=music_context,
            project_manifest=project_manifest,
            reason="npu_skipped_gpu_heavy_mode",
        )
        write_legacy_text_output(NPU_TECH_MD, npu_notes)

    service_packet_info = build_ai_service_packet(
        track_stem=TRACK_STEM,
        analysis_path=Path(args.analysis),
        track_summary_path=Path(args.track_summary),
        music_context_path=Path(args.compact_json),
        analysis_ai_context_path=Path(args.analysis_ai_context),
        blender_keyframes_path=Path(args.blender_keyframes_json),
        dual_plan_path=DUAL_PLAN_JSON if DUAL_PLAN_JSON.exists() else None,
        npu_notes=npu_notes,
        npu_status="skipped_gpu_heavy_mode" if args.skip_npu else "router_capsule_ready",
        scene_brief=scene_brief,
        asset_inventory=asset_inventory,
    )
    gpu_task_packet = service_packet_info["gpu_packet"]

    if args.phase == "implementation":
        if args.skip_ollama:
            draft = build_fallback_implementation_draft(
                reason="Ollama skipped; deterministic standalone scene script generated.",
                model=None,
                args=args,
                scene_brief=scene_brief,
                asset_inventory=asset_inventory,
            )
            write_implementation_draft(draft)
        else:
            plan_output = read_json(DUAL_PLAN_JSON)
            plan = plan_output.get("final_plan", plan_output)
            manager_kwargs = {}
            if args.ollama_base_url:
                manager_kwargs["base_url"] = args.ollama_base_url
            with OllamaModelManager(**manager_kwargs) as manager:
                implementation_prompt = build_implementation_prompt(
                    plan,
                    npu_notes,
                    args.include_manual,
                    gpu_task_packet,
                    scene_brief,
                    asset_inventory,
                )
                draft = generate_implementation_draft_with_retry(
                    manager=manager,
                    model_name=args.technical_model,
                    implementation_prompt=implementation_prompt,
                    plan=plan,
                    max_new_tokens=args.max_new_tokens,
                    args=args,
                    scene_brief=scene_brief,
                    asset_inventory=asset_inventory,
                )
                write_implementation_draft(draft)

        print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
        print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
        print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")
        return

    if args.skip_ollama:
        creative = {"skipped": True}
        technical = {"skipped": True}
        plan = {
            "pipeline_policy": {
                "use_full_blender_keyframes_json": True,
                "ai_context_is_analysis_only": True,
                "ollama_model_switch_policy": "unload previous model before loading next",
            },
            "recommended_scene_plan": {
                "summary": "Ollama skipped; use NPU notes only.",
                "priority_changes": [],
                "defer_changes": [],
            },
        }
    else:
        manager_kwargs = {}
        if args.ollama_base_url:
            manager_kwargs["base_url"] = args.ollama_base_url

        with OllamaModelManager(**manager_kwargs) as manager:
            creative_prompt = build_creative_scene_prompt(
                music_context, npu_notes, read_text(PROJECT_INDEX_MD)
            )
            creative_text, creative_model = manager.generate(
                args.creative_model,
                creative_prompt,
                max_new_tokens=args.max_new_tokens,
                temperature=0.20,
            )
            creative = safe_parse_json(creative_text, "raw_creative_response")
            creative["model"] = creative_model

            technical_prompt = build_music_prompt(music_context)
            technical_text, technical_model = manager.generate(
                args.technical_model,
                technical_prompt,
                max_new_tokens=args.max_new_tokens,
                temperature=0.10,
            )
            technical = safe_parse_json(technical_text, "raw_technical_response")
            technical["model"] = technical_model

            merge_prompt = build_merge_prompt(music_context, npu_notes, creative, technical)
            merge_text, merge_model = manager.generate(
                args.technical_model,
                merge_prompt,
                max_new_tokens=args.max_new_tokens,
                temperature=0.08,
            )
            plan = safe_parse_json(merge_text, "raw_plan_response")
            plan["merge_model"] = merge_model

            if args.phase == "full":
                implementation_prompt = build_implementation_prompt(
                    plan,
                    npu_notes,
                    args.include_manual,
                    gpu_task_packet,
                    scene_brief,
                    asset_inventory,
                )
                draft = generate_implementation_draft_with_retry(
                    manager=manager,
                    model_name=args.technical_model,
                    implementation_prompt=implementation_prompt,
                    plan=plan,
                    max_new_tokens=args.max_new_tokens,
                    args=args,
                    scene_brief=scene_brief,
                    asset_inventory=asset_inventory,
                )
                write_implementation_draft(draft)

    output = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "track_stem": TRACK_STEM,
        "policy": {
            "full_blender_keyframes_json": str(Path(args.blender_keyframes_json)),
            "ai_context_json": str(MUSIC_AI_CONTEXT),
            "model_switch_rule": "Unload/stop previous Ollama model before loading the next model.",
            "phase": args.phase,
            "manual_context_used": args.include_manual,
            "scene_brief_json": str(Path(args.scene_brief)) if args.scene_brief else None,
            "asset_inventory_json": str(Path(args.asset_inventory))
            if args.asset_inventory
            else None,
            "implementation_draft_json": str(IMPLEMENTATION_DRAFT_JSON)
            if args.phase in {"implementation", "full"}
            else None,
            "implementation_script": str(IMPLEMENTATION_SCRIPT)
            if args.phase in {"implementation", "full"}
            else None,
            "legacy_runtime_output_policy": legacy_runtime_output_policy_report(),
        },
        "npu_preflight_json": str(NPU_PREFLIGHT_JSON),
        "npu_technical_notes_md": str(NPU_TECH_MD),
        "ai_service_packet": {
            "capsule_json": service_packet_info.get("capsule_json"),
            "gpu_packet_json": service_packet_info.get("gpu_packet_json"),
            "output_gpu_packet_json": service_packet_info.get("output_gpu_packet_json"),
            "capsule_md": service_packet_info.get("capsule_md"),
        },
        "creative_ollama": creative,
        "technical_ollama": technical,
        "final_plan": plan,
    }

    write_legacy_json_output(DUAL_PLAN_JSON, output)
    write_legacy_json_output(OLLAMA_INSIGHTS_JSON, technical)
    write_legacy_text_output(
        OLLAMA_INSIGHTS_MD,
        markdown_from_insights(technical, technical.get("model", args.technical_model)),
    )
    write_brief(plan, creative, technical, npu_notes)

    print(f"[OK] Wrote: {DUAL_PLAN_JSON}")
    print(f"[OK] Wrote: {DUAL_BRIEF_MD}")
    print(f"[OK] Wrote: {NPU_TECH_MD}")
    if args.phase in {"implementation", "full"} and not args.skip_ollama:
        print(f"[OK] Wrote: {IMPLEMENTATION_DRAFT_JSON}")
        print(f"[OK] Wrote: {IMPLEMENTATION_SCRIPT}")
        print(f"[OK] Wrote: {IMPLEMENTATION_NOTES}")
