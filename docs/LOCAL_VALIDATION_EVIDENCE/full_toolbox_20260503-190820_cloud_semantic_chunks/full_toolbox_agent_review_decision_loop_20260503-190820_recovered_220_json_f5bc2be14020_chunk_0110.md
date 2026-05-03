# Evidence Chunk 0110/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `17469`
- line_end: `17580`
- section_kinds: `['json_key_section', 'json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0109.md`
- next_chunk_file: ``
- summary_source: `ollama`

## Local chunk summary

**Scopo**: definire la struttura di scoperta e inclusione di artefatti per la generazione di patch in un ambiente AI cloud.  
**Segnali principali**:  
- `recursive_default_discovery.enabled = false` → la ricerca ricorsiva di report/artifact è disabilitata.  
- Limiti di inclusione: massimo 120 file, 24 artefatti, 24 000 caratteri totali, 200 linee per file grande.  
- Lista di estensioni consentite (.cfg, .csv, .ini, .json, .md, .ps1, .py, .toml, .txt, .yaml, .yml).

## Context before

          "line_start": 601,
          "line_end": 800,
          "previous_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L401-L600",
          "next_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L801-L1000",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L801-L1000",
          "path": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md",
          "line_start": 801,
          "line_end": 1000,

## Chunk content

```json
          "previous_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L601-L800",
          "next_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1001-L1200",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1001-L1200",
          "path": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md",
          "line_start": 1001,
          "line_end": 1200,
          "previous_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L801-L1000",
          "next_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1201-L1400",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1201-L1400",
          "path": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md",
          "line_start": 1201,
          "line_end": 1400,
          "previous_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1001-L1200",
          "next_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1401-L1600",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1401-L1600",
          "path": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md",
          "line_start": 1401,
          "line_end": 1600,
          "previous_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1201-L1400",
          "next_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1601-L1692",
          "has_previous": true,
          "has_next": true
        },
        {
          "chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1601-L1692",
          "path": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md",
          "line_start": 1601,
          "line_end": 1692,
          "previous_chunk_id": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.md#L1401-L1600",
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
    "max_included_artifact_chars": 24000,
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
    "included_artifact_count": 14,
    "patch_plan_summary_seen": true
  }
}
```
