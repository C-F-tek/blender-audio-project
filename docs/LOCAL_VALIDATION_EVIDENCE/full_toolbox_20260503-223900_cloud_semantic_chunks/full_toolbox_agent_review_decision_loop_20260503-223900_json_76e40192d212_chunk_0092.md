# Evidence Chunk 0092/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `14982`
- line_end: `15131`
- section_kinds: `['json_key_section', 'json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0091.md`
- next_chunk_file: ``
- summary_source: `ollama`

## Local chunk summary

**Scopo**: definire la configurazione di discovery e

## Context before

          "has_next": false
        }
      ]
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md",
      "suffix": ".md",
      "line_count": 302,
      "chunk_size_lines": 200,
      "chunk_count": 2,
      "first_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md#L1-L200",
      "last_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md#L201-L302",

## Chunk content

```json
      "chunks": [
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md#L1-L200",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md#L201-L302",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md#L201-L302",
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md",
          "line_start": 201,
          "line_end": 302,
          "previous_chunk_id": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.md#L1-L200",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    },
    {
      "path": "output/validation/python_line_count_all_python_files_20260503-223900.md",
      "suffix": ".md",
      "line_count": 330,
      "chunk_size_lines": 200,
      "chunk_count": 2,
      "first_chunk_id": "output/validation/python_line_count_all_python_files_20260503-223900.md#L1-L200",
      "last_chunk_id": "output/validation/python_line_count_all_python_files_20260503-223900.md#L201-L330",
      "chunks": [
        {
          "chunk_id": "output/validation/python_line_count_all_python_files_20260503-223900.md#L1-L200",
          "path": "output/validation/python_line_count_all_python_files_20260503-223900.md",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/validation/python_line_count_all_python_files_20260503-223900.md#L201-L330",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/validation/python_line_count_all_python_files_20260503-223900.md#L201-L330",
          "path": "output/validation/python_line_count_all_python_files_20260503-223900.md",
          "line_start": 201,
          "line_end": 330,
          "previous_chunk_id": "output/validation/python_line_count_all_python_files_20260503-223900.md#L1-L200",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    },
    {
      "path": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md",
      "suffix": ".md",
      "line_count": 304,
      "chunk_size_lines": 200,
      "chunk_count": 2,
      "first_chunk_id": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md#L1-L200",
      "last_chunk_id": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md#L201-L304",
      "chunks": [
        {
          "chunk_id": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md#L1-L200",
          "path": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md#L201-L304",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md#L201-L304",
          "path": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md",
          "line_start": 201,
          "line_end": 304,
          "previous_chunk_id": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.md#L1-L200",
          "next_chunk_id": null,
          "has_previous": true,
          "has_next": false
        }
      ]
    }
  ],
  "recursive_default_discovery": {
    "enabled": false,
    "stamp": null,
    "include_unstamped": false,
    "max_files": 120,
    "report_roots": [],
    "artifact_roots": [],
    "discovered_reports": [],
    "discovered_artifacts": [],
    "skipped_reports": [],
    "skipped_artifacts": []
  },
  "included_artifact_policy": {
    "auto_include_related_artifacts": true,
    "max_included_artifact_chars": 16000,
    "max_included_artifacts": 24,
    "chunk_large_files_lines": 200,
    "content_extension_allowlist": [
      ".cfg",
      ".csv",
      ".ini",
      ".json",
      ".md",
      ".ps1",
      ".py",
      ".toml",
      ".txt",
      ".yaml",
      ".yml"
    ],
    "raw_artifact_deny_prefixes": [
      "output/ai_context_packs/",
      "output/ai_pipeline/gpu_deep_planning_parallel_checkpoints/",
      "output/ai_pipeline/gpu_planner_nonempty_diagnostics_checkpoints",
      "output/ai_pipeline/gpu_planner_fallback_verify_checkpoints",
      "output/ai_pipeline/gpu_planner_full_after_fallback_fix_checkpoints",
      "indexAI/code_chunks/",
      "indexAI/project_code_chunks/",
      "renders/"
    ],
    "raw_artifact_deny_fragments": [
      "full_analysis",
      "analysis_full",
      ".sqlite",
      ".db",
      "_npu_async_audit_context",
      "_npu_async_audit_npu",
      "_npu_async_audit_npu_notes"
    ]
  },
  "decision": {
    "ollama_gpu_primary_advisory": false,
    "npu_excluded_when_unusable": false,
    "provider_execution_seen": true,
    "npu_decode_smoke_passed": false,
    "selected_chunks_evidence_seen": true,
    "selected_chunks_built": true,
    "budget_respected": true,
    "artifact_manifest_built": true,
    "included_artifacts_built": true,
    "included_artifact_count": 24,
    "patch_plan_summary_seen": true
  }
}
```
