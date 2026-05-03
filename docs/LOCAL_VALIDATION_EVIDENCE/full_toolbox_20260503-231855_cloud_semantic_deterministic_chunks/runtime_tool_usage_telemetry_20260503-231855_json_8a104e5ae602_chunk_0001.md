# Evidence Chunk 0001/0001

- source: `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260503-231855.json`
- source_sha256: `8a104e5ae602928a01d3ef4bcf10b83c36576f73023ab8ea6108d23c61f7eb19`
- line_start: `2`
- line_end: `151`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; stamp; provider_execution_performed. Preview: "schema_version": 1, "kind": "runtime_tool_usage_telemetry", "generated_at": "2026-05-03T23:22:58", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "stamp": "20260503-231855", "passed": true, "errors": [], "warnings": [], "provider_execution_p...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "runtime_tool_usage_telemetry",
  "generated_at": "2026-05-03T23:22:58",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "stamp": "20260503-231855",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "sqlite_write_performed": false,
  "persistent_memory_write_performed": false,
  "manual_review_required": true,
  "inputs": {
    "orchestrator": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
    "gpu_report": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
    "gpu_npu_sync": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.json",
    "decision_loop": "output/ai_pipeline/full_toolbox_20260503-231855_agent_review_decision_loop.json"
  },
  "decision_loop_summary": {
    "passed": true,
    "recommendation_count": 20,
    "patch_plan_count": 20
  },
  "gpu_npu_sync_metrics": {
    "gpu_round_count": 4,
    "npu_audit_count": 1,
    "npu_audit_success_count": 1,
    "npu_audit_round_coverage": 0.25,
    "avg_gpu_round_seconds": 29.51,
    "p50_gpu_round_seconds": 29.51,
    "p90_gpu_round_seconds": 29.51,
    "avg_npu_audit_seconds": 104.0,
    "p50_npu_audit_seconds": 104.0,
    "p90_npu_audit_seconds": 104.0,
    "npu_to_gpu_avg_duration_ratio": 3.524,
    "gpu_elapsed_seconds": 118.039,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "summary": {
    "tool_call_entry_count": 1,
    "executed_count": 0,
    "failed_count": 0,
    "blocked_count": 0,
    "total_reported_tool_elapsed_seconds": 0.0,
    "by_caller_ai": {
      "gpu": {
        "count": 1,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "by_tool": {
      "declared_runtime_tool_request_summary": {
        "count": 1,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "by_phase": {
      "gpu_planner_declared_tool_request_counters": {
        "count": 1,
        "executed": 0,
        "failed": 0,
        "blocked": 0,
        "elapsed_seconds": 0.0
      }
    },
    "runtime_tool_request_count": 16,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_provider_request_count": 16,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_request_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "declared_not_executed_count": 16
  },
  "declared_runtime_tool_counters": {
    "runtime_tool_request_count": 16,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_provider_request_count": 16,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_request_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "declared_not_executed_count": 16
  },
  "tool_calls": [
    {
      "caller_ai": "gpu",
      "phase": "gpu_planner_declared_tool_request_counters",
      "round": null,
      "broker_source": "gpu_report_or_gpu_npu_sync_counters",
      "broker_report": "",
      "tool_request_id": "gpu_declared_runtime_tool_request_counter_summary",
      "tool": "declared_runtime_tool_request_summary",
      "reason": "GPU planner reported runtime tool request counters without broker-executed per-tool entries.",
      "requested_args": {},
      "status": "declared_counter_summary_not_broker_executed",
      "executed": false,
      "blocked": false,
      "failed": false,
      "elapsed_seconds": 0.0,
      "declared_counts": {
        "runtime_tool_request_count": 16,
        "runtime_tool_execution_count": 0,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 16,
        "runtime_tool_provider_request_execution_count": 0,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0,
        "declared_not_executed_count": 16
      },
      "result": {
        "summary": "Planner declared runtime tool requests; broker execution count is reported separately.",
        "runtime_tool_request_count": 16,
        "runtime_tool_execution_count": 0,
        "runtime_tool_failed_count": 0,
        "runtime_tool_blocked_count": 0,
        "runtime_tool_provider_request_count": 16,
        "runtime_tool_provider_request_execution_count": 0,
        "deterministic_runtime_tool_fallback_request_count": 0,
        "deterministic_runtime_tool_fallback_execution_count": 0,
        "declared_not_executed_count": 16
      }
    }
  ],
  "truncated_tool_call_count": 0,
  "guardrails": {
    "report_only": true,
    "committable_location": "docs/LOCAL_VALIDATION_EVIDENCE",
    "raw_output_commit_allowed": false,
    "provider_execution_performed": false,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false
  }
}
```
