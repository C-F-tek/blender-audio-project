# Evidence Chunk 0028/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `5141`
- line_end: `5325`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0027.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: Recommendations; Guardrail; `output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.md`; GPU Planner JSON Contract Replay; Contract reason counts. Preview: ## Recommendations - `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected - `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected - `co...

## Context before

- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_repository_consistency_map.py` — `687` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `626` lines, risk `medium`


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
- `code_static_026` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_027` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_028` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_029` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_030` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module
- `code_static_031` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_033` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_034` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_035` `Tools/ai/build_deterministic_recommendations.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_036` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_038` `Tools/ai/build_full_toolbox_run_telemetry_summary.py` risk `medium`: large functions detected
- `code_static_039` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_040` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.md`

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

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2346`
- SHA-256: `3724f8b4e286a02342227d202be228f1980b74ebd13cd03460c278cd7ecbca30`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `4`
- `npu_audit_count`: `1`
- `npu_audit_success_count`: `1`
- `npu_audit_round_coverage`: `0.25`
- `avg_gpu_round_seconds`: `29.51`
- `p50_gpu_round_seconds`: `29.51`
- `p90_gpu_round_seconds`: `29.51`
- `avg_npu_audit_seconds`: `104.0`
- `p50_npu_audit_seconds`: `104.0`
- `p90_npu_audit_seconds`: `104.0`
- `npu_to_gpu_avg_duration_ratio`: `3.524`
- `gpu_elapsed_seconds`: `118.039`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.0`
- GPU elapsed seconds: `118.039`
- GPU average round seconds: `29.51`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- NPU average audit seconds: `104.0`
- NPU duration sample count: `1`

## Operational opinions

- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.
- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Add per-round elapsed_seconds to each GPU planner round record. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count
- `medium` `npu_cadence`: Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget. Evidence: npu_to_gpu_avg_duration_ratio=3.524

## Suggested balanced profile

- `npu_auditor_every_rounds`: `4`
- `max_concurrent_npu_audits`: `1`
- `npu_auditor_timeout_seconds`: `420`
- `npu_max_context_chars`: `8000`
- `npu_max_prompt_chars`: `1200`
- `npu_max_new_tokens`: `384`
- `npu_final_wait_seconds`: `180`
- `gpu_max_new_tokens`: `3600`
- `gpu_files_per_round`: `8`
- `gpu_max_chars_per_file`: `6000`

## Reasoning

- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.
- NPU audits are usable; tune cadence rather than disabling the lane.


```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
````
