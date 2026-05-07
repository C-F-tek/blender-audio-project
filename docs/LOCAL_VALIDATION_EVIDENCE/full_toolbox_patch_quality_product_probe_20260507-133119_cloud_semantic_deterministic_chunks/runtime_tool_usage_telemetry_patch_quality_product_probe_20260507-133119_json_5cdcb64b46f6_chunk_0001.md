# Evidence Chunk 0001/0002

- source: `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `5cdcb64b46f6cc3065f72dde3b721c2d526248d2a776d9c8d828d7d7a03606eb`
- line_start: `2`
- line_end: `172`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/runtime_tool_usage_telemetry_patch_quality_product_probe_20260507-133119_json_5cdcb64b46f6_chunk_0002.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; stamp; provider_execution_performed. Preview: "schema_version": 1, "kind": "runtime_tool_usage_telemetry", "generated_at": "2026-05-07T13:33:46", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "stamp": "patch_quality_product_probe_20260507-133119", "passed": true, "errors": [], "warnings...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "runtime_tool_usage_telemetry",
  "generated_at": "2026-05-07T13:33:46",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "stamp": "patch_quality_product_probe_20260507-133119",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "provider_evidence": {
    "provider_execution_performed": true,
    "gpu_provider_execution_performed": true,
    "gpu_round_count": 4,
    "gpu_classification": null,
    "gpu_provider_empty_response": false,
    "npu_provider_execution_performed": false,
    "npu_audit_count": 0,
    "npu_audit_success_count": 0,
    "npu_micro_support_performed": false,
    "npu_micro_support_count": 0,
    "npu_micro_support_success_count": 0,
    "npu_micro_runtime_tool_execution_count": 0,
    "npu_micro_runtime_tool_live_execution_count": 0,
    "npu_lane_mode": "metadata_only",
    "provider_degraded_reasons": [
      "npu_auditor_not_confirmed:audit_count=0;success_count=0;lane_mode=metadata_only"
    ]
  },
  "provider_broker_loop": {},
  "patch_application_performed": false,
  "source_writes_performed": false,
  "sqlite_write_performed": false,
  "persistent_memory_write_performed": false,
  "manual_review_required": true,
  "inputs": {
    "orchestrator": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json",
    "gpu_report": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json",
    "gpu_npu_sync": "output/analysis/gpu_npu_run_sync_full_toolbox_patch_quality_product_probe_20260507-133119.json",
    "decision_loop": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_agent_review_decision_loop.json",
    "broker_reports": [
      "output/validation/runtime_tool_broker_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "output/validation/gpu0_peer_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json",
      "output/validation/npu_micro_runtime_tool_broker_patch_quality_product_probe_20260507-133119.json"
    ]
  },
  "decision_loop_summary": {
    "passed": true,
    "recommendation_count": 20,
    "patch_plan_count": 20
  },
  "gpu_npu_sync_metrics": {
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
  "summary": {
    "tool_call_entry_count": 6,
    "executed_count": 6,
    "failed_count": 0,
    "blocked_count": 0,
    "broker_entry_count": 6,
    "broker_executed_count": 6,
    "total_reported_tool_elapsed_seconds": 0.0,
    "by_caller_ai": {
      "orchestrator": {
        "count": 3,
        "executed": 3,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "gpu0": {
        "count": 3,
        "executed": 3,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "by_tool": {
      "check_python_syntax": {
        "count": 1,
        "executed": 1,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "build_python_line_count_csv": {
        "count": 1,
        "executed": 1,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "check_validation_report_contract": {
        "count": 2,
        "executed": 2,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "build_code_interpreter_report": {
        "count": 1,
        "executed": 1,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "build_refactor_duplication_audit": {
        "count": 1,
        "executed": 1,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "by_phase": {
      "explicit_runtime_tool_broker_bootstrap": {
        "count": 3,
        "executed": 3,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      },
      "gpu0_peer_runtime_tool_broker": {
        "count": 3,
        "executed": 3,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "runtime_tool_request_count": 15,
    "runtime_tool_execution_count": 7,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_provider_request_count": 8,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_request_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "declared_not_executed_count": 8
  },
  "declared_runtime_tool_counters": {
    "runtime_tool_request_count": 15,
    "runtime_tool_execution_count": 7,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_provider_request_count": 8,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_request_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "declared_not_executed_count": 8
  },
```

## Context after

  "tool_calls": [
    {
      "caller_ai": "orchestrator",
      "phase": "explicit_runtime_tool_broker_bootstrap",
      "round": 1,
      "broker_source": "runtime_tool_bootstrap_requests",
      "broker_report": "output/validation/runtime_tool_broker_full_toolbox_patch_quality_product_probe_20260507-133119.json",
      "tool_request_id": "full_toolbox_bootstrap_python_syntax",
      "tool": "check_python_syntax",
      "reason": "Brokered Python syntax validation.",
      "requested_args": {},
      "status": null,
