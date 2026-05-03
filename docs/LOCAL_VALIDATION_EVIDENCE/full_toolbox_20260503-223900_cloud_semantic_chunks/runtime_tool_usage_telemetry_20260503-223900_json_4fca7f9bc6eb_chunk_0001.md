# Evidence Chunk 0001/0001

- source: `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260503-223900.json`
- source_sha256: `4fca7f9bc6eb11f72c45b00d149677b00372ef44287dc14967c9628b12cfc1b8`
- line_start: `2`
- line_end: `67`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; stamp; provider_execution_performed. Preview: "schema_version": 1, "kind": "runtime_tool_usage_telemetry", "generated_at": "2026-05-03T22:45:35", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "stamp": "20260503-223900", "passed": true, "errors": [], "warnings": [], "provider_execution_p...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "runtime_tool_usage_telemetry",
  "generated_at": "2026-05-03T22:45:35",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "stamp": "20260503-223900",
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
    "orchestrator": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json",
    "gpu_report": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
    "gpu_npu_sync": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-223900.json",
    "decision_loop": "output/ai_pipeline/full_toolbox_20260503-223900_agent_review_decision_loop.json"
  },
  "decision_loop_summary": {
    "passed": true,
    "recommendation_count": 40,
    "patch_plan_count": 40
  },
  "gpu_npu_sync_metrics": {
    "gpu_round_count": 8,
    "npu_audit_count": 2,
    "npu_audit_success_count": 2,
    "npu_audit_round_coverage": 0.25,
    "avg_gpu_round_seconds": 34.761,
    "p50_gpu_round_seconds": 34.761,
    "p90_gpu_round_seconds": 34.761,
    "avg_npu_audit_seconds": 100.0,
    "p50_npu_audit_seconds": 98.0,
    "p90_npu_audit_seconds": 102.0,
    "npu_to_gpu_avg_duration_ratio": 2.877,
    "gpu_elapsed_seconds": 278.09,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "gpu_metrics_source": "gpu_elapsed_divided_by_round_count"
  },
  "summary": {
    "tool_call_entry_count": 0,
    "executed_count": 0,
    "failed_count": 0,
    "blocked_count": 0,
    "total_reported_tool_elapsed_seconds": 0.0,
    "by_caller_ai": {},
    "by_tool": {},
    "by_phase": {}
  },
  "tool_calls": [],
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
