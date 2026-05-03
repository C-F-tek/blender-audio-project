# Evidence Chunk 0034/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `3081`
- line_end: `3306`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0033.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0035.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_chunk_index. Preview: "artifact_chunk_index": [ { "path": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json", "suffix": ".json", "line_count": 332, "chunk_size_lines": 200, "chunk_count": 2, "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_orchest...

## Context before

      "size_bytes": 2349,
      "sha256": "97214ebc5ced9b137a07a16fcadf0bafca7d06559d4b96b91af57457a2cbdb96",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 64,
      "raw_chars": 2285,
      "included_chars": 2285,
      "content": "# GPU/NPU Run Sync Analysis\n\n- Passed: `True`\n- Provider execution performed: `False`\n- Patch application performed: `False`\n- Source writes performed: `False`\n\n## Metrics\n\n- `gpu_round_count`: `8`\n- `npu_audit_count`: `2`\n- `npu_audit_success_count`: `2`\n- `npu_audit_round_coverage`: `0.25`\n- `avg_gpu_round_seconds`: `34.761`\n- `p50_gpu_round_seconds`: `34.761`\n- `p90_gpu_round_seconds`: `34.761`\n- `avg_npu_audit_seconds`: `100.0`\n- `p50_npu_audit_seconds`: `98.0`\n- `p90_npu_audit_seconds`: `102.0`\n- `npu_to_gpu_avg_duration_ratio`: `2.877`\n- `gpu_elapsed_seconds`: `278.09`\n- `provider_execution_performed`: `True`\n- `patch_application_performed`: `False`\n- `source_writes_performed`: `False`\n- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`\n\n## Performance\n\n- Analyzer elapsed seconds: `0.001`\n- GPU elapsed seconds: `278.09`\n- GPU average round seconds: `34.761`\n- GPU timing source: `gpu_elapsed_divided_by_round_count`\n- NPU average audit seconds: `100.0`\n- NPU duration sample count: `2`\n\n## Operational opinions\n\n- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.\n- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.\n- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.\n\n## Refactoring suggestions\n\n- `high` `gpu_runner_timing`: Add per-round elapsed_seconds to each GPU planner round record. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count\n- `medium` `npu_cadence`: Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget. Evidence: npu_to_gpu_avg_duration_ratio=2.877\n\n## Suggested balanced profile\n\n- `npu_auditor_every_rounds`: `3`\n- `max_concurrent_npu_audits`: `1`\n- `npu_auditor_timeout_seconds`: `420`\n- `npu_max_context_chars`: `8000`\n- `npu_max_prompt_chars`: `1200`\n- `npu_max_new_tokens`: `384`\n- `npu_final_wait_seconds`: `180`\n- `gpu_max_new_tokens`: `3600`\n- `gpu_files_per_round`: `8`\n- `gpu_max_chars_per_file`: `6000`\n\n## Reasoning\n\n- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.\n- NPU audits are usable; tune cadence rather than disabling the lane.\n\n"
    }
  ],

## Chunk content

```json
  "artifact_chunk_index": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json",
      "suffix": ".json",
      "line_count": 332,
      "chunk_size_lines": 200,
      "chunk_count": 2,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json#L201-L332",
      "chunks": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json#L1-L200",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json#L201-L332",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json#L201-L332",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json",
          "line_start": 201,
          "line_end": 332,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json#L1-L200",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
      "suffix": ".json",
      "line_count": 1071,
      "chunk_size_lines": 200,
      "chunk_count": 6,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L1001-L1071",
      "chunks": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L1-L200",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L201-L400",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L1-L200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L401-L600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L401-L600",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
          "line_start": 401,
          "line_end": 600,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L201-L400",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L601-L800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L601-L800",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
          "line_start": 601,
          "line_end": 800,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L401-L600",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L801-L1000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L801-L1000",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
          "line_start": 801,
          "line_end": 1000,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L601-L800",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L1001-L1071",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L1001-L1071",
          "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
          "line_start": 1001,
          "line_end": 1071,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json#L801-L1000",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
      "suffix": ".json",
      "line_count": 153712,
      "chunk_size_lines": 200,
      "chunk_count": 769,
      "first_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1-L200",
      "last_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L153601-L153712",
      "chunks": [
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1-L200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L201-L400",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1-L200",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L401-L600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L401-L600",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 401,
          "line_end": 600,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L201-L400",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L601-L800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L601-L800",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 601,
          "line_end": 800,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L401-L600",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L801-L1000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L801-L1000",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 801,
          "line_end": 1000,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L601-L800",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1001-L1200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1001-L1200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 1001,
          "line_end": 1200,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L801-L1000",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1201-L1400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1201-L1400",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 1201,
          "line_end": 1400,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1001-L1200",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1401-L1600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1401-L1600",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 1401,
          "line_end": 1600,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1201-L1400",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1601-L1800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1601-L1800",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 1601,
          "line_end": 1800,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1401-L1600",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1801-L2000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1801-L2000",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 1801,
          "line_end": 2000,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1601-L1800",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2001-L2200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2001-L2200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 2001,
          "line_end": 2200,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L1801-L2000",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2201-L2400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2201-L2400",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 2201,
```

## Context after

          "line_end": 2400,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2001-L2200",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2401-L2600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2401-L2600",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
          "line_start": 2401,
          "line_end": 2600,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json#L2201-L2400",
