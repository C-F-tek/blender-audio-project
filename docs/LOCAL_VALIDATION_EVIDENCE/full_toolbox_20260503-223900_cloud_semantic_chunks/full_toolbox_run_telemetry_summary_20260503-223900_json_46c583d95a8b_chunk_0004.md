# Evidence Chunk 0004/0004

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260503-223900.json`
- source_sha256: `46c583d95a8b37e1f4d0765c39ec8cd99b345dff25de727c4092572240261658`
- line_start: `568`
- line_end: `659`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_run_telemetry_summary_20260503-223900_json_46c583d95a8b_chunk_0003.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: performance; operational_opinions; refactoring_suggestions; guardrails; report_only. Preview: "performance": { "analyzer_elapsed_seconds": 0.001, "gpu": { "elapsed_seconds": 278.09, "round_count": 8, "round_duration_source": "gpu_elapsed_divided_by_round_count", "round_duration_sample_count": 1, "avg_round_seconds": 34.761, "p50_round_seconds": 34.761,...

## Context before

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

## Chunk content

```json
    "performance": {
      "analyzer_elapsed_seconds": 0.001,
      "gpu": {
        "elapsed_seconds": 278.09,
        "round_count": 8,
        "round_duration_source": "gpu_elapsed_divided_by_round_count",
        "round_duration_sample_count": 1,
        "avg_round_seconds": 34.761,
        "p50_round_seconds": 34.761,
        "p90_round_seconds": 34.761,
        "max_round_seconds": 34.761,
        "round_durations_total_seconds": 34.761,
        "provider_empty_response_count": 0,
        "schema_repair_retry_attempt_count": 0,
        "schema_repair_retry_accept_count": 0,
        "runtime_tool_counters": {
          "runtime_tool_request_count": 28,
          "runtime_tool_execution_count": 0,
          "runtime_tool_failed_count": 0,
          "runtime_tool_blocked_count": 0,
          "runtime_tool_provider_request_count": 28,
          "runtime_tool_provider_request_execution_count": 0,
          "deterministic_runtime_tool_fallback_request_count": 0,
          "deterministic_runtime_tool_fallback_execution_count": 0
        },
        "embedded_performance": {}
      },
      "npu": {
        "audit_count": 2,
        "audit_requested_count": 0,
        "audit_success_count": 2,
        "duration_sample_count": 2,
        "avg_audit_seconds": 100.0,
        "p50_audit_seconds": 98.0,
        "p90_audit_seconds": 102.0,
        "max_audit_seconds": 102.0,
        "audit_durations_total_seconds": 200.0,
        "status_counts": {
          "finished": 2
        },
        "classification_counts": {
          "usable_audit_text": 2
        },
        "lane_diagnostics": {}
      },
      "sync": {
        "npu_to_gpu_avg_duration_ratio": 2.877,
        "npu_audit_round_coverage": 0.25,
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
    "operational_opinions": [
      "NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.",
      "Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.",
      "GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics."
    ],
    "refactoring_suggestions": [
      {
        "priority": "high",
        "area": "gpu_runner_timing",
        "recommendation": "Add per-round elapsed_seconds to each GPU planner round record.",
        "evidence": "gpu_metrics_source=gpu_elapsed_divided_by_round_count",
        "guardrail": "report_only_no_provider_setting_change"
      },
      {
        "priority": "medium",
        "area": "npu_cadence",
        "recommendation": "Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget.",
        "evidence": "npu_to_gpu_avg_duration_ratio=2.877",
        "guardrail": "keep_max_concurrent_npu_audits_1"
      }
    ]
  },
  "guardrails": {
    "report_only": true,
    "committable_location": "docs/LOCAL_VALIDATION_EVIDENCE",
    "raw_output_commit_allowed": false,
    "provider_execution_performed": true,
    "patch_application_performed": false,
    "source_writes_performed": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false
  }
}
```
