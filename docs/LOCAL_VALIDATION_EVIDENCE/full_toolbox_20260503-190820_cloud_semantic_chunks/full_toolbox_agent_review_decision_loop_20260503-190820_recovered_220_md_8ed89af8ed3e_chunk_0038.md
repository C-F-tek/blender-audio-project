# Evidence Chunk 0038/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `4867`
- line_end: `5045`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0037.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0039.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.json`; `output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.md`; Agent GPU Deep Planning Review; Decision; Recommendations. Preview: "invalid_tool_request_count": 0, "empty_recommendations_reason": "json_parse_failure", "evidence_ready_for_manual_patch_count": 12, "provider_tool_request_absence_reason": "", "recommended_next_layer": "" }, { ``` ### `output/ai_pipeline/full_toolbox_20260503-...

## Context before

      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "",
      "contract": {},
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,

## Chunk content

````md
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
 
```

### `output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1055`
- SHA-256: `9655c7328f767f14acea6c9d1bf250a0f96b20f39dc2bf54398fe6f2d4b1c2ed`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `False`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `1679.037`
- Round count: `50`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- Tool request count: `0`
- Valid tool request count: `0`
- Invalid tool request count: `0`
- JSON parse error count: `50`
- Context echo detected count: `0`
- Model output schema mismatch count: `0`
- Empty recommendations reason: `json_parse_failure`
- Evidence ready for manual patch count: `12`

## Decision

- `ready_for_patch_plan`: `False`
- `ready_count`: `0`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `True`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `manual_review_required`: `True`

## Recommendations


```

### `output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2468`
- SHA-256: `7fd8dd0297321f083c8f51019153375b2b661993ee9284bc7e69ff1bd0c21edf`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `50`
- `npu_audit_count`: `9`
- `npu_audit_success_count`: `9`
- `npu_audit_round_coverage`: `0.18`
- `avg_gpu_round_seconds`: `33.731`
- `p50_gpu_round_seconds`: `33.731`
- `p90_gpu_round_seconds`: `33.731`
- `avg_npu_audit_seconds`: `105.556`
- `p50_npu_audit_seconds`: `106.0`
- `p90_npu_audit_seconds`: `108.0`
- `npu_to_gpu_avg_duration_ratio`: `3.129`
- `gpu_elapsed_seconds`: `1686.543`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`

## Performance

- Analyzer elapsed seconds: `0.001`
- GPU elapsed seconds: `1686.543`
- GPU average round seconds: `33.731`
- GPU timing source: `gpu_elapsed_divided_by_round_count`
- NPU average audit seconds: `105.556`
- NPU duration sample count: `9`

## Operational opinions

- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.
- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.
- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.

## Refactoring suggestions

- `high` `gpu_runner_timing`: Add per-round elapsed_seconds to each GPU planner round record. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count
- `medium` `npu_cadence`: Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget. Evidence: npu_to_gpu_avg_duration_ratio=3.129

## Suggested balanced profile

- `npu_auditor_every_rounds`: `3`
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

- NPU audit coverage is low compared with GPU round count; keep checkpoint auditing sampled, not per-round.
- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.
- NPU audits are usable; tune cadence rather than disabling the lane.


```

### `output/analysis/repository_consistency_map_full_toolbox_20260503-190820.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `45267`
- SHA-256: `71010556ab897a2a1b73296ba5cff6ef7d26fc861751c45b9af60ced1c14611d`
- Content included: `True`
- Content truncated: `True`

```text
# Repository Consistency Map

- Passed: `True`
- Finding count: `2327`
- Markdown files: `1236`
- Python files: `316`
- Markdown references: `39844`
- Markdown Python commands: `1277`
- Provider execution performed: `False`
- Workers requested: `18`
- Total build seconds: `33.631`
- Markdown scan seconds: `23.693`
- Python inventory seconds: `3.231`
- Patch application performed: `False`

## Severity counts

- `high`: `816`
- `low`: `46`
- `medium`: `1465`

## Finding kind counts

- `documented_python_script_without_obvious_smoke`: `46`
- `md_cli_arg_not_in_argparse`: `2`
- `md_mentions_missing_markdown_path`: `1463`
- `md_mentions_missing_powershell_path`: `39`
- `md_mentions_missing_python_path`: `763`
- `md_python_command_script_missing`: `14`

````

## Context after

## Findings

| Severity | Kind | Source | Line | Target | Recommendation |
|---|---|---|---:|---|---|
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 91 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 93 | `animation.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 94 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 96 | `asset_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 97 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 99 | `atmosphere_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 100 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
| `high` | `md_mentions_missing_python_path` | `.aider.chat.history.md` | 102 | `camera_setup.cpython-313.py` | Correct the documentation reference or restore the missing target if it is still required. |
