# Evidence Chunk 0025/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `4407`
- line_end: `4550`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0024.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0026.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json`; `output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.md`; Agent GPU/NPU Parallel Orchestrator; Decision; NPU Audits. Preview: "gpu_empty_recommendations_reason": "model_output_schema_mismatch", "runtime_tool_broker_enabled": false, "runtime_tool_bootstrap_executed": false, "runtime_tool_bootstrap_execution_count": 0, "runtime_tool_provider_request_count": 0, "runtime_tool_provider_re...

## Context before

    "npu_audit_success_count": 1,
    "npu_tool_context_seen_count": 0,
    "npu_tool_request_count": 0,
    "npu_deterministic_tool_fallback_count": 0,
    "npu_runtime_tool_request_count": 0,
    "npu_runtime_tool_execution_count": 0,
    "npu_runtime_tool_failed_count": 0,
    "npu_runtime_tool_blocked_count": 0,
    "npu_runtime_tool_result_count": 0,
    "ready_for_patch_plan": false,
    "fallback_patch_plan_recommended": true,
    "recommended_next_layer": "build_agent_review_patch_plan.py",

## Chunk content

````md
    "gpu_empty_recommendations_reason": "model_output_schema_mismatch",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_bootstrap_executed": false,
    "runtime_tool_bootstrap_execution_count": 0,
    "runtime_tool_provider_request_count": 0,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "runtime_tool_execution_count": 0,
    "runtime_tool_result_count": 0,
    "manual_review_required": true,
    "gpu_lane_mode": "primary_fast_loop",
    "npu_lane_mode": "slow",
    "gpu_direct_runtime_tool_provider_request_execution_count": 0,
    "runtime_tool_feedback_context_report_count": 0,
    "npu_effective_auditor_every_rounds": 4
  },
  "guardrails": {
    "gpu_continues_without_waiting_for_npu": true,
    "npu_auditor_non_blocking": true,
    "npu_primary_advisory": false,
    "patch_application_performed": false,
    "real_github_pr_created": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false,
    "runtime_tool_broker_report_only": true,
    "orchestrator_controls_gpu_runtime_tools": true,
    "gpu_runner_direct_runtime_tool_broker": false,
    "npu_runtime_tools_execute_via_broker": true
  },
  "gpu_direct_runtime_tool_request_count": 16,
  "gpu_direct_runtime_tool_execution_count": 0,
  "gpu_direct_runtime_tool_failed_count": 0,
  "gpu_direct_runtime_tool_blocked_count": 0,
  "gpu_direct_runtime_tool_provider_request_count": 16,
  "gpu_direct_runtime_tool_provider_request_execution_count": 0,
  "gpu_direct_runtime_tool_feedback_context_report_count": 0,
  "gpu_direct_deterministic_runtime_tool_fallback_request_count": 0,
  "gpu_direct_deterministic_runtime_tool_fallback_execution_count": 0,
  "gpu_lane_mode": "primary_fast_loop",
  "gpu_lane": {
    "mode": "primary_fast_loop",
    "provider_execution_performed": true,
    "round_count": 4,
    "recommendation_count": 0,
    "empty_recommendations_reason": "model_output_schema_mismatch",
    "direct_runtime_tool_execution_count": 0,
    "direct_provider_request_execution_count": 0,
    "feedback_context_report_count": 0
  },
  "npu_lane_mode": "slow",
  "npu_lane": {
    "mode": "slow",
    "provider_requested": true,
    "audit_count": 1,
    "finished_count": 1,
    "running_count": 0,
    "success_count": 1,
    "failed_count": 0,
    "avg_elapsed_seconds": 104.0,
    "max_elapsed_seconds": 104.0,
    "slow_threshold_seconds": 60.0,
    "base_auditor_every_rounds": 4,
    "slow_auditor_every_rounds": 4,
    "effective_auditor_every_rounds": 4,
    "non_blocking": true
  },
  "runtime_tool_feedback_context_report_count": 0
}

```

### `output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2330`
- SHA-256: `70e721efd80745de3995b3717723c26ce92f40ef44416b44c184ca0099ec0e49`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `118.039`
- `npu_audit_count`: `1`
- `npu_audit_success_count`: `1`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `model_output_schema_mismatch`
- `gpu_evidence_ready_for_manual_patch_count`: `12`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `16`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `1`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_deterministic_tool_fallback_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `True`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: `model_output_schema_mismatch`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_bootstrap_executed`: `False`
- `runtime_tool_bootstrap_execution_count`: `0`
- `runtime_tool_provider_request_count`: `0`
- `runtime_tool_provider_request_execution_count`: `0`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_result_count`: `0`
- `manual_review_required`: `True`
- `gpu_lane_mode`: `primary_fast_loop`
- `npu_lane_mode`: `slow`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `4`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`

```

````

## Context after

### `output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `22883`
- SHA-256: `18e66de8b74293075877dfbd2e09c7abb17aba63d545f2e9bbd6b2ab0ebd7aca`
- Content included: `True`
- Content truncated: `True`

```text
{
