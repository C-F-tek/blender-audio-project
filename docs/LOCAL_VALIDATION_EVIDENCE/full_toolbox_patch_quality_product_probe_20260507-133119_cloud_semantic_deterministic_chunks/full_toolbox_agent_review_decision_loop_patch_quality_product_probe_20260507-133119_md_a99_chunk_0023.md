# Evidence Chunk 0023/0024

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `a996111fa318d87d97d3b80eb2d1e49442622645214c899236220d62065e9ccb`
- line_start: `4129`
- line_end: `4378`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0022.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0024.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Recommendations; Guardrail; `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.md`; GPU Planner JSON Contract Replay; Contract reason counts. Preview: ## Recommendations - `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected - `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected - `co...

## Context before

- `Tools/ai/build_runtime_tool_usage_telemetry.py` - `823` lines, risk `high`
- `Tools/ai/agent_runtime_tool_broker.py` - `759` lines, risk `medium`
- `Tools/workflow/gui/workflow_gui.py` - `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` - `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` - `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` - `725` lines, risk `medium`
- `Tools/npu/build_music_context.py` - `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` - `694` lines, risk `medium`
- `Scripting/v61b/materials.py` - `657` lines, risk `medium`
- `Tools/ai/build_ai_peer_exchange_packet.py` - `642` lines, risk `medium`
- `Tools/npu/run_npu_review.py` - `631` lines, risk `medium`


## Chunk content

````md
## Recommendations

- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected
- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module
- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected
- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_011` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected
- `code_static_012` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_013` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_014` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected
- `code_static_015` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_017` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected
- `code_static_018` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_019` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected
- `code_static_020` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_021` `Tools/ai/agent_memory_routing_policy.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_022` `Tools/ai/agent_review_warning_policy.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_023` `Tools/ai/agent_runtime_sqlite_memory.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_024` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_025` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_026` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module
- `code_static_027` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_028` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_029` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_030` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_031` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_033` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_034` `Tools/ai/build_ai_peer_exchange_packet.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_035` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_036` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_038` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_039` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_040` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/analysis/gpu_json_contract_replay_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `606`
- SHA-256: `ade444a4d7002868f8529cb9b2c5e7a8ebf09a6b78014fc2b3c7286211cd8b8e`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `4`
- Context echo detected: `0`
- JSON parse failures: `0`
- Schema mismatches: `4`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `model_output_schema_mismatch`: `4`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `5238`
- SHA-256: `60600cb5f05992f6f5bbb6b700a0312dd025899f469e59d7663ddb828c2c16c9`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "gpu_npu_run_sync_analysis",
  "generated_at": "2026-05-07T13:33:23",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "blender_runtime_execution_performed": false,
  "sqlite_write_performed": false,
  "manual_review_required": true,
  "inputs": {
    "orchestrator": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json"
  },
  "metrics": {
    "gpu_round_count": 4,
    "npu_audit_count": 0,
    "legacy_npu_audit_count": 0,
    "npu_micro_support_count": 0,
    "npu_micro_support_overlap_count": 0,
    "gpu0_peer_support_count": 5,
    "gpu0_peer_support_overlap_count": 4,
    "npu_audit_success_count": 0,
    "npu_audit_round_coverage": 0.0,
    "avg_gpu_round_seconds": 15.424,
    "p50_gpu_round_seconds": 15.424,
    "p90_gpu_round_seconds": 15.424,
    "avg_npu_audit_seconds": 0.0,
    "p50_npu_audit_seconds": 0.0,
    "p90_npu_audit_seconds": 0.0,
    "npu_to_gpu_avg_duration_ratio": 0.0,
    "gpu_elapsed_seconds": 61.694,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "performance": {
    "analyzer_elapsed_seconds": 0.001,
    "gpu": {
      "elapsed_seconds": 61.694,
      "round_count": 4,
      "round_duration_source": "gpu_elapsed_divided_by_round_count",
      "round_duration_sample_count": 1,
      "avg_round_seconds": 15.424,
      "p50_round_seconds": 15.424,
      "p90_round_seconds": 15.424,
      "max_round_seconds": 15.424,
      "round_durations_total_seconds": 15.424,
      "provider_empty_response_count": 0,
      "schema_repair_retry_attempt_count": 0,
      "schema_repair_retry_accept_count": 0,
      "runtime_tool_counters": {
        "runtime_tool_request_count": 15,
        "runtime_tool_execution_count": 7,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 8,
        "runtime_tool_provider_request_execution_count": 0,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0
      },
      "embedded_performance": {}
    },
    "npu": {
      "audit_count": 0,
      "audit_requested_count": 0,
      "audit_success_count": 0,
      "duration_sample_count": 0,
      "avg_audit_seconds": 0.0,
      "p50_audit_seconds": 0.0,
      "p90_audit_seconds": 0.0,
      "max_audit_seconds": 0.0,
      "audit_durations_total_seconds": 0.0,
      "status_counts": {},
      "classification_counts": {},
      "lane_diagnostics": {}
    },
    "sync": {
      "npu_to_gpu_avg_duration_ratio": 0.0,
      "npu_audit_round_coverage": 0.0,
      "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
    },
    "guardrails": {
      "report_only": true,
      "provider_execution_performed": false,
      "patch_application_performed": false,
      "source_writes_performed": false,
      "blender_runtime_execution_performed": false,
      "sqlite_write_performed": false
    }
  },
  "suggestions": {
    "recommended_profile": "gpu_npu_balanced_advisory",
    "reasoning": [
      "No NPU audits were observed; first verify provider availability before tuning cadence.",
      "GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate."
    ],
    "parameters": {
      "npu_auditor_every_rounds": 4,
      "max_concurrent_npu_audits": 1,
      "npu_auditor_timeout_seconds": 420,
      "npu_max_context_chars": 8000,
      "npu_max_prompt_chars": 1200,
      "npu_max_new_tokens": 384,
      "npu_final_wait_seconds": 180,
      "gpu_max_new_tokens": 3600,
      "gpu_files_per_round": 8,
      "gpu_max_chars_per_file": 6000
    },
    "guardrails": {
      "do_not_change_provider_model_settings_first": true,
      "keep_npu_auditor_non_blocking": true,
      "keep_max_concurrent_npu_audits": 1,
      "do_not_promote_npu_advisory": true,
      "do_not_make_openvino_gpu_primary": true
    }
  },
  "operational_opinions": [
    "Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.",
    "GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present."
  ],
  "refactoring_suggestions": [
    {
      "priority": "high",
      "area": "gpu_runner_timing",
      "recommendation": "Use rounds[*].elapsed_seconds as the primary GPU round timing source.",
      "evidence": "gpu_metrics_source=gpu_elapsed_divided_by_round_count",
      "guardrail": "report_only_no_provider_setting_change"
    }
  ],
  "decision": {
    "npu_too_slow_for_per_round_lockstep": false,
    "recommended_next_layer": "feed timing-backed GPU/NPU suggestions into decision-loop patch planning",
    "manual_review_required": true
  }
}

```

### `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2367`
- SHA-256: `11aef7aeee95ee274bd5f397bde63f698d765de29985a4b1d40911f2e4fb6e89`
- Content included: `True`
- Content truncated: `False`

```text
````

## Context after

# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `4`
- `npu_audit_count`: `0`
- `legacy_npu_audit_count`: `0`
