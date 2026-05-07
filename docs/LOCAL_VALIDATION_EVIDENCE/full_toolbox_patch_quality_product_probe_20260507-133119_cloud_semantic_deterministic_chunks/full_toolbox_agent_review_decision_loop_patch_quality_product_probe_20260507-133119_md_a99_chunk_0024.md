# Evidence Chunk 0024/0024

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.md`
- source_sha256: `a996111fa318d87d97d3b80eb2d1e49442622645214c899236220d62065e9ccb`
- line_start: `4379`
- line_end: `4623`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_md_a99_chunk_0023.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: GPU/NPU Run Sync Analysis; Metrics; Performance; Operational opinions; Refactoring suggestions. Preview: # GPU/NPU Run Sync Analysis - Passed: `True` - Provider execution performed: `False` - Patch application performed: `False` - Source writes performed: `False` ## Metrics - `gpu_round_count`: `4` - `npu_audit_count`: `0` - `legacy_npu_audit_count`: `0` - `npu_m...

## Context before


### `output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2367`
- SHA-256: `11aef7aeee95ee274bd5f397bde63f698d765de29985a4b1d40911f2e4fb6e89`
- Content included: `True`
- Content truncated: `False`

```text

## Chunk content

````md
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `4`
- `npu_audit_count`: `0`
- `legacy_npu_audit_count`: `0`
- `npu_micro_support_count`: `0`
- `npu_micro_support_overlap_count`: `0`
- `gpu0_peer_support_count`: `5`
- `gpu0_peer_support_overlap_count`: `4`
- `npu_audit_success_count`: `0`
- `npu_audit_round_coverage`: `0.0`
- `avg_gpu_round_seconds`: `15.424`
- `p50_gpu_round_seconds`: `15.424`
- `p90_gpu_round_seconds`: `15.424`
- `avg_npu_audit_seconds`: `0.0`
- `p50_npu_audit_seconds`: `0.0`
- `p90_npu_audit_seconds`: `0.0`
- `npu_to_gpu_avg_duration_ratio`: `0.0`
- `gpu_elapsed_seconds`: `61.694`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.001`
- GPU elapsed seconds: `61.694`
- GPU average round seconds: `15.424`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- GPU timing sample count: `1`
- GPU round durations total seconds: `15.424`
- NPU average audit seconds: `0.0`
- NPU duration sample count: `0`

## Operational opinions

- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is not sourced from rounds[*].elapsed_seconds; keep diagnostics degraded until real samples are present.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Use rounds[*].elapsed_seconds as the primary GPU round timing source. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count

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

- No NPU audits were observed; first verify provider availability before tuning cadence.
- GPU per-round elapsed_seconds was unavailable; using total GPU elapsed divided by round count as estimate.


```

### `output/validation/agent_review_decision_loop_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `212`
- SHA-256: `ab8c829b5f099b245a1f6048441784a3a280a173d7787782e1288efabc3bec5e`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Decision Loop Smoke

- Passed: `True`
- Return code: `0`
- Recommendation count: `1`
- Patch plan count: `1`
- Deterministic synthesizer used: `True`
- Patch application performed: `False`

```

### `output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1487`
- SHA-256: `d0f044b80c6e1d6797bf9c34875a8ef1b4045cc6392587ff084a34a99d942566`
- Content included: `True`
- Content truncated: `False`

```text
# Deterministic Recommendation Synthesizer Smoke

- Passed: `True`
- Recommendation count: `1`
- Deterministic synthesizer used: `True`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Synthesized report preview

# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `1`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `json_parse_failure`
- Evidence ready for manual patch count: `1`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### det_doc_code_001 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['AGENTS.md']`
- Rationale: The documentation points at a recommendation lane that must be normalized before patch-plan construction.
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Tools/ai/build_deterministic_recommendations.py` and update `AGENTS.md` only if the reference is stale or should point at an existing artifact. Prefer existing candidate `Tools/ai/build_agent_review_patch_plan.py` over inventing a new runtime artifact. Candidate references observed: `Tools/ai/build_agent_review_patch_plan.py`, `Tools/ai/gpu_planner_json_contract.py`.

## Guardrails

This report is deterministic and report-only. It is not a patch queue.

```

### `output/validation/full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_workflow.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3684`
- SHA-256: `0c0d7b5af72f9f70cc78f10bdab6871259a710e9f5bd872f2c3e87ba09ba6bf3`
- Content included: `True`
- Content truncated: `False`

```text
# Full Memory / Tool Regeneration Workflow

- Passed: `True`
- Stamp: `patch_quality_product_probe_20260507-133119`
- Profile: `full_refactor`
- Report count: `13`
- Artifact count: `14`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`
- Persistent memory write performed: `False`

## Reports

- `.\output\ai_pipeline\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agent_memory_inventory.json`
- `.\output\ai_pipeline\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agnostic_tool_inventory.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_persistent_memory_status.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_operational_memory_status.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker.json`
- `.\output\ai_pipeline\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_transient_request_context.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_python_line_count.json`
- `.\output\analysis\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_code_interpreter.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_python_syntax.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_validation_report_contract.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker_smoke.json`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy_smoke.json`

## Artifacts

- `.\docs\LOCAL_AI_TASKS\full-memory-tool-regeneration-procedure.md`
- `.\Tools\workflow\run_full_memory_tool_regeneration.ps1`
- `.\output\ai_pipeline\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agent_memory_inventory.md`
- `.\output\ai_pipeline\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_agnostic_tool_inventory.md`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_persistent_memory_status.md`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_operational_memory_status.md`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy.md`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker.md`
- `.\output\ai_pipeline\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_transient_request_context.md`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_python_line_count.md`
- `.\docs/LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_patch_quality_product_probe_20260507-133119.csv`
- `.\output\analysis\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_code_interpreter.md`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_runtime_tool_broker_smoke.md`
- `.\output\validation\full_memory_tool_regeneration_patch_quality_product_probe_20260507-133119_memory_routing_policy_smoke.md`

```

### `output/validation/gpu0_companion_contract_patch_quality_product_probe_20260507-133119.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `231`
- SHA-256: `ace1eeebc553a5acee8dc4f851cf9ec75c49977b2aa4db80cf3b4868a5c53b29`
- Content included: `True`
- Content truncated: `False`

```text
# GPU0 Companion Contract

- Passed: `True`
- Selected report: `C:\Users\carmi\blender\blender-audio-project\output\validation\gpu0_companion_task_lane_patch_quality_product_probe_20260507-133119.json`
- Classifications: `[]`

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
git status --short
# Replace <bundle_basename> with the generated evidence bundle basename.
git add -- `
  .\docs\LOCAL_VALIDATION_EVIDENCE\<bundle_basename>.json `
  .\docs\LOCAL_VALIDATION_EVIDENCE\<bundle_basename>.md
git commit -m "test: add local ai workflow evidence bundle"
git push
# Never use: git add docs/LOCAL_VALIDATION_EVIDENCE/
```
````
