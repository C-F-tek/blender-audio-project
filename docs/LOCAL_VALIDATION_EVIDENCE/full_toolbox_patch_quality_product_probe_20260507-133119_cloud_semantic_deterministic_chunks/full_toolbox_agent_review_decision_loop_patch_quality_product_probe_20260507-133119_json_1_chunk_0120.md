# Evidence Chunk 0120/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `18633`
- line_end: `18739`
- section_kinds: `['json_key_section', 'json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0119.md`
- next_chunk_file: ``
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: artifact_chunk_index; recursive_default_discovery; enabled; stamp; include_unstamped. Preview: { "chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L1-L200", "path": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md", "line_start": 1, "line_e...

## Context before

        }
      ]
    },
    {
      "path": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md",
      "suffix": ".md",
      "line_count": 660,
      "chunk_size_lines": 200,
      "chunk_count": 4,
      "first_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L1-L200",
      "last_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L601-L660",
      "chunks": [

## Chunk content

```json
        {
          "chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L1-L200",
          "path": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md",
          "line_start": 1,
          "line_end": 200,
          "previous_chunk_id": null,
          "next_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L201-L400",
          "has_previous": false,
          "has_next": true
        },
        {
          "chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L201-L400",
          "path": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md",
          "line_start": 201,
          "line_end": 400,
          "previous_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L1-L200",
          "next_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L401-L600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L401-L600",
          "path": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md",
          "line_start": 401,
          "line_end": 600,
          "previous_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L201-L400",
          "next_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L601-L660",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L601-L660",
          "path": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md",
          "line_start": 601,
          "line_end": 660,
          "previous_chunk_id": "output/validation/python_line_count_all_python_files_patch_quality_product_probe_20260507-133119.md#L401-L600",
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
    "max_included_artifacts": 42,
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
    "included_artifact_count": 42,
    "patch_plan_summary_seen": true
  }
}
```
