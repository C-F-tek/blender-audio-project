# Evidence Chunk 0030/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `3307`
- line_end: `3381`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0029.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0031.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: included_artifacts. Preview: }, { "path": "output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.md", "exists": true, "suffix": ".md", "size_bytes": 606, "sha256": "ade444a4d7002868f8529cb9b2c5e7a8ebf09a6b78014fc2b3c7286211cd8b8e", "role": "auto...

## Context before

      "exists": true,
      "suffix": ".md",
      "size_bytes": 7129,
      "sha256": "5963bc8bf594dd3adf40c00079a3ec9d0179e69152e68522dc0cfe9da633db2e",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 84,
      "raw_chars": 7045,
      "included_chars": 7045,
      "content": "# Static Code Interpreter Report\n\n- Passed: `True`\n- File count: `601`\n- Parsed files: `601`\n- Total lines: `101948`\n- Total functions: `3667`\n- Total classes: `101`\n- Risk signals: `90`\n- TODO/FIXME markers: `21`\n- Recommendation count: `185`\n- Provider execution performed: `False`\n- Patch application performed: `False`\n- Source writes performed: `False`\n\n## Largest files\n\n- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` - `2263` lines, risk `high`\n- `Tools/npu/run_dual_ai_pipeline.py` - `1774` lines, risk `high`\n- `Scripting/v61b/scene_tuning_panel.py` - `1262` lines, risk `high`\n- `Tools/workflow/workflow_state.py` - `1230` lines, risk `high`\n- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` - `1180` lines, risk `high`\n- `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` - `1100` lines, risk `high`\n- `Scripting/v61b/animation.py` - `1079` lines, risk `high`\n- `Tools/ai/build_deterministic_recommendations.py` - `909` lines, risk `high`\n- `Tools/ai/run_agent_gpu_deep_planning_review.py` - `902` lines, risk `high`\n- `Tools/ai/build_runtime_tool_usage_telemetry.py` - `823` lines, risk `high`\n- `Tools/ai/agent_runtime_tool_broker.py` - `759` lines, risk `medium`\n- `Tools/workflow/gui/workflow_gui.py` - `738` lines, risk `medium`\n- `Scripting/v61b/physics_setup.py` - `737` lines, risk `medium`\n- `Scripting/v61b/asset_setup.py` - `725` lines, risk `medium`\n- `Tools/ai/build_refactor_duplication_audit.py` - `725` lines, risk `medium`\n- `Tools/npu/build_music_context.py` - `711` lines, risk `medium`\n- `Tools/ai/run_npu_gpu_deep_review_auditor.py` - `694` lines, risk `medium`\n- `Scripting/v61b/materials.py` - `657` lines, risk `medium`\n- `Tools/ai/build_ai_peer_exchange_packet.py` - `642` lines, risk `medium`\n- `Tools/npu/run_npu_review.py` - `631` lines, risk `medium`\n\n## Recommendations\n\n- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected\n- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected\n- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module\n- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected\n- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected\n- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_011` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected\n- `code_static_012` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_013` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_014` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected\n- `code_static_015` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_016` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected\n- `code_static_017` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected\n- `code_static_018` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected\n- `code_static_019` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected\n- `code_static_020` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected\n- `code_static_021` `Tools/ai/agent_memory_routing_policy.py` risk `medium`: medium-size Python module, large functions detected\n- `code_static_022` `Tools/ai/agent_review_warning_policy.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_023` `Tools/ai/agent_runtime_sqlite_memory.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_024` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected\n- `code_static_025` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module\n- `code_static_026` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module\n- `code_static_027` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected\n- `code_static_028` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected\n- `code_static_029` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module\n- `code_static_030` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module, large functions detected\n- `code_static_031` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_032` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_033` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected\n- `code_static_034` `Tools/ai/build_ai_peer_exchange_packet.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_035` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected\n- `code_static_036` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected\n- `code_static_037` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected\n- `code_static_038` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected\n- `code_static_039` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected\n- `code_static_040` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected\n\n## Guardrail\n\nThis is static interpretation only. It does not execute repository code or apply changes.\n"

## Chunk content

```json
    },
    {
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.md",
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
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 5238,
      "sha256": "60600cb5f05992f6f5bbb6b700a0312dd025899f469e59d7663ddb828c2c16c9",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 140,
      "raw_chars": 5098,
      "included_chars": 5098,
      "content": "{\n  \"schema_version\": 1,\n  \"kind\": \"gpu_npu_run_sync_analysis\",\n  \"generated_at\": \"2026-05-07T13:33:23\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": false,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"blender_runtime_execution_performed\": false,\n  \"sqlite_write_performed\": false,\n  \"manual_review_required\": true,\n  \"inputs\": {\n    \"orchestrator\": \"output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json\"\n  },\n  \"metrics\": {\n    \"gpu_round_count\": 4,\n    \"npu_audit_count\": 0,\n    \"legacy_npu_audit_count\": 0,\n    \"npu_micro_support_count\": 0,\n    \"npu_micro_support_overlap_count\": 0,\n    \"gpu0_peer_support_count\": 5,\n    \"gpu0_peer_support_overlap_count\": 4,\n    \"npu_audit_success_count\": 0,\n    \"npu_audit_round_coverage\": 0.0,\n    \"avg_gpu_round_seconds\": 15.424,\n    \"p50_gpu_round_seconds\": 15.424,\n    \"p90_gpu_round_seconds\": 15.424,\n    \"avg_npu_audit_seconds\": 0.0,\n    \"p50_npu_audit_seconds\": 0.0,\n    \"p90_npu_audit_seconds\": 0.0,\n    \"npu_to_gpu_avg_duration_ratio\": 0.0,\n    \"gpu_elapsed_seconds\": 61.694,\n    \"provider_execution_performed\": true,\n    \"patch_application_performed\": false,\n    \"source_writes_performed\": false,\n    \"gpu_metrics_source\": \"gpu_elapsed_divided_by_round_count\"\n  },\n  \"performance\": {\n    \"analyzer_elapsed_seconds\": 0.001,\n    \"gpu\": {\n      \"elapsed_seconds\": 61.694,\n      \"round_count\": 4,\n      \"round_duration_source\": \"gpu_elapsed_divided_by_round_count\",\n      \"round_duration_sample_count\": 1,\n      \"avg_round_seconds\": 15.424,\n      \"p50_round_seconds\": 15.424,\n      \"p90_round_seconds\": 15.424,\n      \"max_round_seconds\": 15.424,\n      \"round_durations_total_seconds\": 15.424,\n      \"provider_empty_response_count\": 0,\n      \"schema_repair_retry_attempt_count\": 0,\n      \"schema_repair_retry_accept_count\": 0,\n      \"runtime_tool_counters\": {\n        \"runtime_tool_request_count\": 15,\n        \"runtime_tool_execution_count\": 7,\n        \"runtime_tool_failed_count\": 0,\n        \"runtime_tool_blocked_count\": 0,\n        \"runtime_tool_provider_request_count\": 8,\n        \"runtime_tool_provider_request_execution_count\": 0,\n        \"deterministic_runtime_tool_fallback_request_count\": 0,\n        \"deterministic_runtime_tool_fallback_execution_count\": 0\n      },\n      \"embedded_performance\": {}\n    },\n    \"npu\": {\n      \"audit_count\": 0,\n      \"audit_requested_count\": 0,\n      \"audit_success_count\": 0,\n      \"duration_sample_count\": 0,\n      \"avg_audit_seconds\": 0.0,\n      \"p50_audit_seconds\": 0.0,\n      \"p90_audit_seconds\": 0.0,\n      \"max_audit_seconds\": 0.0,\n      \"audit_durations_total_seconds\": 0.0,\n      \"status_counts\": {},\n      \"classification_counts\": {},\n      \"lane_diagnostics\": {}\n    },\n    \"sync\": {\n      \"npu_to_gpu_avg_duration_ratio\": 0.0,\n      \"npu_audit_round_coverage\": 0.0,\n      \"gpu_metrics_source\": \"gpu_elapsed_divided_by_round_count\"\n    },\n    \"guardrails\": {\n      \"report_only\": true,\n      \"provider_execution_performed\": false,\n      \"patch_application_performed\": false,\n      \"source_writes_performed\": false,\n      \"blender_runtime_execution_performed\": false,\n      \"sqlite_write_performed\": false\n    }\n  },\n  \"suggestions\": {\n    \"recommended_profile\": \"gpu_npu_balanced_advisory\",\n    \"reasoning\": [\n      \"No NPU audits were observed; first verify provider availability before tuning cadence.\",\n      \"GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate.\"\n    ],\n    \"parameters\": {\n      \"npu_auditor_every_rounds\": 4,\n      \"max_concurrent_npu_audits\": 1,\n      \"npu_auditor_timeout_seconds\": 420,\n      \"npu_max_context_chars\": 8000,\n      \"npu_max_prompt_chars\": 1200,\n      \"npu_max_new_tokens\": 384,\n      \"npu_final_wait_seconds\": 180,\n      \"gpu_max_new_tokens\": 3600,\n      \"gpu_files_per_round\": 8,\n      \"gpu_max_chars_per_file\": 6000\n    },\n    \"guardrails\": {\n      \"do_not_change_provider_model_settings_first\": true,\n      \"keep_npu_auditor_non_blocking\": true,\n      \"keep_max_concurrent_npu_audits\": 1,\n      \"do_not_promote_npu_advisory\": true,\n      \"do_not_make_openvino_gpu_primary\": true\n    }\n  },\n  \"operational_opinions\": [\n    \"Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.\",\n    \"GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.\"\n  ],\n  \"refactoring_suggestions\": [\n    {\n      \"priority\": \"high\",\n      \"area\": \"gpu_runner_timing\",\n      \"recommendation\": \"Use rounds[*].elapsed_seconds as the primary GPU round timing source.\",\n      \"evidence\": \"gpu_metrics_source=gpu_elapsed_divided_by_round_count\",\n      \"guardrail\": \"report_only_no_provider_setting_change\"\n    }\n  ],\n  \"decision\": {\n    \"npu_too_slow_for_per_round_lockstep\": false,\n    \"recommended_next_layer\": \"feed timing-backed GPU/NPU suggestions into decision-loop patch planning\",\n    \"manual_review_required\": true\n  }\n}\n"
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 2367,
      "sha256": "11aef7aeee95ee274bd5f397bde63f698d765de29985a4b1d40911f2e4fb6e89",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 69,
      "raw_chars": 2298,
      "included_chars": 2298,
      "content": "# GPU/NPU Run Sync Analysis\n\n- Passed: `True`\n- Provider execution performed: `False`\n- Patch application performed: `False`\n- Source writes performed: `False`\n\n## Metrics\n\n- `gpu_round_count`: `4`\n- `npu_audit_count`: `0`\n- `legacy_npu_audit_count`: `0`\n- `npu_micro_support_count`: `0`\n- `npu_micro_support_overlap_count`: `0`\n- `gpu0_peer_support_count`: `5`\n- `gpu0_peer_support_overlap_count`: `4`\n- `npu_audit_success_count`: `0`\n- `npu_audit_round_coverage`: `0.0`\n- `avg_gpu_round_seconds`: `15.424`\n- `p50_gpu_round_seconds`: `15.424`\n- `p90_gpu_round_seconds`: `15.424`\n- `avg_npu_audit_seconds`: `0.0`\n- `p50_npu_audit_seconds`: `0.0`\n- `p90_npu_audit_seconds`: `0.0`\n- `npu_to_gpu_avg_duration_ratio`: `0.0`\n- `gpu_elapsed_seconds`: `61.694`\n- `provider_execution_performed`: `True`\n- `patch_application_performed`: `False`\n- `source_writes_performed`: `False`\n- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`\n\n## Performance\n\n- Analyzer elapsed seconds: `0.001`\n- GPU elapsed seconds: `61.694`\n- GPU average round seconds: `15.424`\n- GPU timing source: `gpu_elapsed_divided_by_round_count`\n- GPU timing sample count: `1`\n- GPU round durations total seconds: `15.424`\n- NPU average audit seconds: `0.0`\n- NPU duration sample count: `0`\n\n## Operational opinions\n\n- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.\n- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.\n\n## Refactoring suggestions\n\n- `high` `gpu_runner_timing`: Use rounds[*].elapsed_seconds as the primary GPU round timing source. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count\n\n## Suggested balanced profile\n\n- `npu_auditor_every_rounds`: `4`\n- `max_concurrent_npu_audits`: `1`\n- `npu_auditor_timeout_seconds`: `420`\n- `npu_max_context_chars`: `8000`\n- `npu_max_prompt_chars`: `1200`\n- `npu_max_new_tokens`: `384`\n- `npu_final_wait_seconds`: `180`\n- `gpu_max_new_tokens`: `3600`\n- `gpu_files_per_round`: `8`\n- `gpu_max_chars_per_file`: `6000`\n\n## Reasoning\n\n- No NPU audits were observed; first verify provider availability before tuning cadence.\n- GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate.\n\n"
    },
    {
      "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 212,
      "sha256": "ab8c829b5f099b245a1f6048441784a3a280a173d7787782e1288efabc3bec5e",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 8,
      "raw_chars": 204,
      "included_chars": 204,
      "content": "# Agent Review Decision Loop Smoke\n\n- Passed: `True`\n- Return code: `0`\n- Recommendation count: `1`\n- Patch plan count: `1`\n- Deterministic synthesizer used: `True`\n- Patch application performed: `False`\n"
    },
    {
      "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 1487,
      "sha256": "d0f044b80c6e1d6797bf9c34875a8ef1b4045cc6392587ff084a34a99d942566",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 33,
      "raw_chars": 1452,
      "included_chars": 1452,
      "content": "# Deterministic Recommendation Synthesizer Smoke\n\n- Passed: `True`\n- Recommendation count: `1`\n- Deterministic synthesizer used: `True`\n- Next best action: `build_agent_review_patch_plan.py`\n- Patch application performed: `False`\n\n## Synthesized report preview\n\n# Deterministic Recommendation Synthesizer\n\n- Passed: `True`\n- Recommendation count: `1`\n- Deterministic synthesizer used: `True`\n- GPU empty recommendations reason: `json_parse_failure`\n- Evidence ready for manual patch count: `1`\n- Next best action: `build_agent_review_patch_plan.py`\n- Patch application performed: `False`\n\n## Recommendations\n\n### det_doc_code_001 — doc_code\n- Source: `deterministic_evidence_synthesizer`\n- Status: `ready_for_patch_plan`\n- Risk: `low`\n- Target files: `['AGENTS.md']`\n- Rationale: The documentation points at a recommendation lane that must be normalized before patch-plan construction.\n- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Tools/ai/build_deterministic_recommendations.py` and update `AGENTS.md` only if the reference is stale or should point at an existing artifact. Prefer existing candidate `Tools/ai/build_agent_review_patch_plan.py` over inventing a new runtime artifact. Candidate references observed: `Tools/ai/build_agent_review_patch_plan.py`, `Tools/ai/gpu_planner_json_contract.py`.\n\n## Guardrails\n\nThis report is deterministic and report-only. It is not a patch queue.\n"
```

## Context after

    },
    {
      "path": "output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.md",
      "exists": true,
      "suffix": ".md",
      "size_bytes": 3684,
      "sha256": "0c0d7b5af72f9f70cc78f10bdab6871259a710e9f5bd872f2c3e87ba09ba6bf3",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 44,
