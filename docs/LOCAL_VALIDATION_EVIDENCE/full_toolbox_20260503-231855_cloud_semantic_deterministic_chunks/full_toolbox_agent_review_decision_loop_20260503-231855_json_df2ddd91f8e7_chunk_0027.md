# Evidence Chunk 0027/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `2257`
- line_end: `2288`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0026.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0028.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: included_artifacts. Preview: }, { "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.md", "exists": true, "suffix": ".md", "size_bytes": 606, "sha256": "ade444a4d7002868f8529cb9b2c5e7a8ebf09a6b78014fc2b3c7286211cd8b8e", "role": "auto_related_artifact", "content...

## Context before

      "exists": true,
      "suffix": ".md",
      "size_bytes": 7088,
      "sha256": "f2e1fadd2a0afa2180d5b0dbd6c71c8b89ed66ed73cab468842cdb417ae2a416",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 84,
      "raw_chars": 6964,
      "included_chars": 6964,
      "content": "# Static Code Interpreter Report\n\n- Passed: `True`\n- File count: `275`\n- Parsed files: `275`\n- Total lines: `77725`\n- Total functions: `2751`\n- Total classes: `93`\n- Risk signals: `56`\n- TODO/FIXME markers: `21`\n- Recommendation count: `155`\n- Provider execution performed: `False`\n- Patch application performed: `False`\n- Source writes performed: `False`\n\n## Largest files\n\n- `Tools/npu/run_dual_ai_pipeline.py` — `1774` lines, risk `high`\n- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines, risk `high`\n- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`\n- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines, risk `high`\n- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1129` lines, risk `high`\n- `Scripting/v61b/animation.py` — `1079` lines, risk `high`\n- `Tools/ai/build_deterministic_recommendations.py` — `908` lines, risk `high`\n- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines, risk `high`\n- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`\n- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`\n- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`\n- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`\n- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`\n- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`\n- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`\n- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`\n- `Scripting/v61b/materials.py` — `657` lines, risk `medium`\n- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`\n- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`\n- `Tools/ai/build_agent_review_patch_plan.py` — `626` lines, risk `medium`\n\n## Recommendations\n\n- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected\n- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected\n- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module\n- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected\n- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected\n- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_011` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected\n- `code_static_012` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_013` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_014` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected\n- `code_static_015` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_016` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected\n- `code_static_017` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_018` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected\n- `code_static_019` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected\n- `code_static_020` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected\n- `code_static_021` `Tools/ai/agent_memory_routing_policy.py` risk `medium`: medium-size Python module, large functions detected\n- `code_static_022` `Tools/ai/agent_review_warning_policy.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_023` `Tools/ai/agent_runtime_sqlite_memory.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_024` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected\n- `code_static_025` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module\n- `code_static_026` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module, complex functions detected\n- `code_static_027` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected\n- `code_static_028` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected\n- `code_static_029` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module\n- `code_static_030` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module\n- `code_static_031` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_032` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_033` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected\n- `code_static_034` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected\n- `code_static_035` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected\n- `code_static_036` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected\n- `code_static_037` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected\n- `code_static_038` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: large functions detected\n- `code_static_039` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected\n- `code_static_040` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected\n\n## Guardrail\n\nThis is static interpretation only. It does not execute repository code or apply changes.\n"

## Chunk content

```json
    },
    {
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 606,
      "sha256": "ade444a4d7002868f8529cb9b2c5e7a8ebf09a6b78014fc2b3c7286211cd8b8e",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 22,
      "raw_chars": 584,
      "included_chars": 584,
      "content": "# GPU Planner JSON Contract Replay\n\n- Passed: `True`\n- Replayed rounds: `4`\n- Context echo detected: `0`\n- JSON parse failures: `0`\n- Schema mismatches: `4`\n- Valid recommendation outputs: `0`\n- Patch application performed: `False`\n- Source writes performed: `False`\n\n## Contract reason counts\n\n- `model_output_schema_mismatch`: `4`\n\n## Decision\n\n- `contract_helper_replay_available`: `True`\n- `safe_to_wire_runner_after_replay`: `True`\n- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`\n- `manual_review_required`: `True`\n\n"
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 2346,
      "sha256": "3724f8b4e286a02342227d202be228f1980b74ebd13cd03460c278cd7ecbca30",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 64,
      "raw_chars": 2282,
      "included_chars": 2282,
      "content": "# GPU/NPU Run Sync Analysis\n\n- Passed: `True`\n- Provider execution performed: `False`\n- Patch application performed: `False`\n- Source writes performed: `False`\n\n## Metrics\n\n- `gpu_round_count`: `4`\n- `npu_audit_count`: `1`\n- `npu_audit_success_count`: `1`\n- `npu_audit_round_coverage`: `0.25`\n- `avg_gpu_round_seconds`: `29.51`\n- `p50_gpu_round_seconds`: `29.51`\n- `p90_gpu_round_seconds`: `29.51`\n- `avg_npu_audit_seconds`: `104.0`\n- `p50_npu_audit_seconds`: `104.0`\n- `p90_npu_audit_seconds`: `104.0`\n- `npu_to_gpu_avg_duration_ratio`: `3.524`\n- `gpu_elapsed_seconds`: `118.039`\n- `provider_execution_performed`: `True`\n- `patch_application_performed`: `False`\n- `source_writes_performed`: `False`\n- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`\n\n## Performance\n\n- Analyzer elapsed seconds: `0.0`\n- GPU elapsed seconds: `118.039`\n- GPU average round seconds: `29.51`\n- GPU timing source: `gpu_elapsed_divided_by_round_count`\n- NPU average audit seconds: `104.0`\n- NPU duration sample count: `1`\n\n## Operational opinions\n\n- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.\n- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.\n- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.\n\n## Refactoring suggestions\n\n- `high` `gpu_runner_timing`: Add per-round elapsed_seconds to each GPU planner round record. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count\n- `medium` `npu_cadence`: Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget. Evidence: npu_to_gpu_avg_duration_ratio=3.524\n\n## Suggested balanced profile\n\n- `npu_auditor_every_rounds`: `4`\n- `max_concurrent_npu_audits`: `1`\n- `npu_auditor_timeout_seconds`: `420`\n- `npu_max_context_chars`: `8000`\n- `npu_max_prompt_chars`: `1200`\n- `npu_max_new_tokens`: `384`\n- `npu_final_wait_seconds`: `180`\n- `gpu_max_new_tokens`: `3600`\n- `gpu_files_per_round`: `8`\n- `gpu_max_chars_per_file`: `6000`\n\n## Reasoning\n\n- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.\n- NPU audits are usable; tune cadence rather than disabling the lane.\n\n"
    }
  ],
```

## Context after

  "artifact_chunk_index": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
      "suffix": ".json",
      "line_count": 274,
      "chunk_size_lines": 200,
      "chunk_count": 2,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L201-L274",
      "chunks": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L1-L200",
