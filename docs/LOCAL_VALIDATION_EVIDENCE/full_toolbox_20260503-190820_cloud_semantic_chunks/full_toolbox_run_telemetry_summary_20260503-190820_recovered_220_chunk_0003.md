# Evidence Chunk 0003/0003

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260503-190820_recovered_220.json`
- source_sha256: `5fe73175e3f7654414e36fc39f0b48ea50b7660dc49c1a571474b02668874ab7`
- line_start: `628`
- line_end: `655`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_run_telemetry_summary_20260503-190820_recovered_220_chunk_0002.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: refactoring_suggestions; guardrails; report_only; committable_location; raw_output_commit_allowed. Preview: "refactoring_suggestions": [ { "priority": "high", "area": "gpu_runner_timing", "recommendation": "Add per-round elapsed_seconds to each GPU planner round record.", "evidence": "gpu_metrics_source=gpu_elapsed_divided_by_round_count", "guardrail": "report_only_...

## Context before

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

## Chunk content

```json
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
        "evidence": "npu_to_gpu_avg_duration_ratio=3.129",
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
