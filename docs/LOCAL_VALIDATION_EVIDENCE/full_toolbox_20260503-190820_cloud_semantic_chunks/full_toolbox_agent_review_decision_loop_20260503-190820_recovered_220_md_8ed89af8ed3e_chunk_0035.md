# Evidence Chunk 0035/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `4275`
- line_end: `4359`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0034.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0036.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Valutare l’esecuzione parallela di GPU/NPU per un agente di patching, registrando metriche di successo, errori e raccomandazioni.  
**Segnali principali**: `passed=False`, `gpu_returncode=2`, `elapsed_seconds≈1687s`, 9 audit NPU riusciti, 200 richieste runtime tool ma nessuna esecuzione.  
**Guardrail/erori**: `gpu_empty_recommendations_reason=json_parse_failure`, `runtime_tool_broker_enabled=False`, `manual_review_required=True`.  
**Perché serve a una AI cloud**: Fornisce feedback dettagliato sullo stato di patching

## Context before

      "audit_output": "output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_024_npu_async_audit.json",
      "started_at": "2026-05-03T19:23:18",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_audit.json",

## Chunk content

````md
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_au
```

### `output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2896`
- SHA-256: `36a6ad829aa8a85ed3ce25a063ca6d22f3758f34bd66fdd33d1b7e23584163cb`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `False`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `2`
- `elapsed_seconds`: `1686.543`
- `npu_audit_count`: `9`
- `npu_audit_success_count`: `9`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `json_parse_failure`
- `gpu_evidence_ready_for_manual_patch_count`: `12`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `200`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `9`
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
- `gpu_empty_recommendations_reason`: `json_parse_failure`
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
- `npu_effective_auditor_every_rounds`: `6`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `6` status=`finished` class=`usable_audit_text` success=`True`
- round `12` status=`finished` class=`usable_audit_text` success=`True`
- round `18` status=`finished` class=`usable_audit_text` success=`True`
- round `24` status=`finished` class=`usable_audit_text` success=`True`
- round `30` status=`finished` class=`usable_audit_text` success=`True`
- round `36` status=`finished` class=`usable_audit_text` success=`True`
- round `42` status=`finished` class=`usable_audit_text` success=`True`
- round `48` status=`finished` class=`usable_audit_text` success=`True`

```

````

## Context after

### `output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `241760`
- SHA-256: `642c196f0c9e0d91757d8c155f674897336dffb9608d6c49b7e67e8341fc1fcf`
- Content included: `True`
- Content truncated: `True`

```text
{
