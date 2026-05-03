# Evidence Chunk 0028/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `2289`
- line_end: `2512`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0027.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0029.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_chunk_index. Preview: "artifact_chunk_index": [ { "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json", "suffix": ".json", "line_count": 274, "chunk_size_lines": 200, "chunk_count": 2, "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchest...

## Context before

      "size_bytes": 2346,
      "sha256": "3724f8b4e286a02342227d202be228f1980b74ebd13cd03460c278cd7ecbca30",
      "role": "auto_related_artifact",
      "content_included": true,
      "content_truncated": false,
      "chunked_content": false,
      "line_count": 64,
      "raw_chars": 2282,
      "included_chars": 2282,
      "content": "# GPU/NPU Run Sync Analysis\n\n- Passed: `True`\n- Provider execution performed: `False`\n- Patch application performed: `False`\n- Source writes performed: `False`\n\n## Metrics\n\n- `gpu_round_count`: `4`\n- `npu_audit_count`: `1`\n- `npu_audit_success_count`: `1`\n- `npu_audit_round_coverage`: `0.25`\n- `avg_gpu_round_seconds`: `29.51`\n- `p50_gpu_round_seconds`: `29.51`\n- `p90_gpu_round_seconds`: `29.51`\n- `avg_npu_audit_seconds`: `104.0`\n- `p50_npu_audit_seconds`: `104.0`\n- `p90_npu_audit_seconds`: `104.0`\n- `npu_to_gpu_avg_duration_ratio`: `3.524`\n- `gpu_elapsed_seconds`: `118.039`\n- `provider_execution_performed`: `True`\n- `patch_application_performed`: `False`\n- `source_writes_performed`: `False`\n- `gpu_metrics_source`: `gpu_elapsed_divided_by_round_count`\n\n## Performance\n\n- Analyzer elapsed seconds: `0.0`\n- GPU elapsed seconds: `118.039`\n- GPU average round seconds: `29.51`\n- GPU timing source: `gpu_elapsed_divided_by_round_count`\n- NPU average audit seconds: `104.0`\n- NPU duration sample count: `1`\n\n## Operational opinions\n\n- NPU should remain an advisory sampled auditor, not a lockstep reviewer for every GPU round.\n- Audit coverage is intentionally sparse; this is acceptable only if findings are high-signal and evidence-backed.\n- GPU round timing is inferred; add direct per-round timing to the GPU runner for stronger diagnostics.\n\n## Refactoring suggestions\n\n- `high` `gpu_runner_timing`: Add per-round elapsed_seconds to each GPU planner round record. Evidence: gpu_metrics_source=gpu_elapsed_divided_by_round_count\n- `medium` `npu_cadence`: Increase npu_auditor_every_rounds or reduce NPU context/tokens before increasing GPU budget. Evidence: npu_to_gpu_avg_duration_ratio=3.524\n\n## Suggested balanced profile\n\n- `npu_auditor_every_rounds`: `4`\n- `max_concurrent_npu_audits`: `1`\n- `npu_auditor_timeout_seconds`: `420`\n- `npu_max_context_chars`: `8000`\n- `npu_max_prompt_chars`: `1200`\n- `npu_max_new_tokens`: `384`\n- `npu_final_wait_seconds`: `180`\n- `gpu_max_new_tokens`: `3600`\n- `gpu_files_per_round`: `8`\n- `gpu_max_chars_per_file`: `6000`\n\n## Reasoning\n\n- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.\n- NPU audits are usable; tune cadence rather than disabling the lane.\n\n"
    }
  ],

## Chunk content

```json
  "artifact_chunk_index": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
      "suffix": ".json",
      "line_count": 274,
      "chunk_size_lines": 200,
      "chunk_count": 2,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L201-L274",
      "chunks": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L1-L200",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L201-L274",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L201-L274",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
          "line_start": 201,
          "line_end": 274,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json#L1-L200",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
      "suffix": ".json",
      "line_count": 594,
      "chunk_size_lines": 200,
      "chunk_count": 3,
      "first_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L1-L200",
      "last_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L401-L594",
      "chunks": [
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L1-L200",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L201-L400",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L1-L200",
          "next_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L401-L594",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L401-L594",
          "path": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
          "line_start": 401,
          "line_end": 594,
          "previous_chunk_id": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json#L201-L400",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
      "suffix": ".json",
      "line_count": 144036,
      "chunk_size_lines": 200,
      "chunk_count": 721,
      "first_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1-L200",
      "last_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L144001-L144036",
      "chunks": [
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1-L200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L201-L400",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1-L200",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L401-L600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L401-L600",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 401,
          "line_end": 600,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L201-L400",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L601-L800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L601-L800",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 601,
          "line_end": 800,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L401-L600",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L801-L1000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L801-L1000",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 801,
          "line_end": 1000,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L601-L800",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1001-L1200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1001-L1200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 1001,
          "line_end": 1200,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L801-L1000",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1201-L1400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1201-L1400",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 1201,
          "line_end": 1400,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1001-L1200",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1401-L1600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1401-L1600",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 1401,
          "line_end": 1600,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1201-L1400",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1601-L1800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1601-L1800",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 1601,
          "line_end": 1800,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1401-L1600",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1801-L2000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1801-L2000",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 1801,
          "line_end": 2000,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1601-L1800",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2001-L2200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2001-L2200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 2001,
          "line_end": 2200,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L1801-L2000",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2201-L2400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2201-L2400",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 2201,
          "line_end": 2400,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2001-L2200",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2401-L2600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2401-L2600",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 2401,
          "line_end": 2600,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2201-L2400",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2601-L2800",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2601-L2800",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 2601,
          "line_end": 2800,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2401-L2600",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2801-L3000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2801-L3000",
```

## Context after

          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 2801,
          "line_end": 3000,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L2601-L2800",
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L3001-L3200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json#L3001-L3200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
          "line_start": 3001,
