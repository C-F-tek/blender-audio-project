# Evidence Chunk 0002/0004

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260503-223900.json`
- source_sha256: `46c583d95a8b37e1f4d0765c39ec8cd99b345dff25de727c4092572240261658`
- line_start: `54`
- line_end: `295`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_run_telemetry_summary_20260503-223900_json_46c583d95a8b_chunk_0001.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_run_telemetry_summary_20260503-223900_json_46c583d95a8b_chunk_0003.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: identificare e pianificare la correzione di script Python mancanti nei file Markdown del repository.  
**Segnali principali**: 13 avvisi “md_python_command_script_missing” con severità alta, tutti con stato “ready_for_patch_plan”.  
**Guardrail / errori**: la mancanza

## Context before

    "bundle_validation_passed": true,
    "evidence_to_commit": [
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_memory_tool_regeneration_bundle_20260503-223900.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_memory_tool_regeneration_bundle_20260503-223900.md",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_memory_tool_regeneration_python_line_count_20260503-223900.csv",
      "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-223919.csv",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_toolbox_agent_review_decision_loop_20260503-223900.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_toolbox_agent_review_decision_loop_20260503-223900.md",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\shared_toolbox_ai_to_ai_bundle_20260503-223900.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\shared_toolbox_ai_to_ai_bundle_20260503-223900.md"
    ]
  },

## Chunk content

```json
  "recommendations_first20": [
    {
      "id": "consistency_001",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_002",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_003",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_004",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_005",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_006",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_007",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_008",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_009",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0025.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_010",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0025.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_011",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0025.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_012",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0025.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_013",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0009.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_014",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0009.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_015",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0010.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_016",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0010.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_017",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0010.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_018",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0010.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_019",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0010.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_020",
      "area": "md_python",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0010.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    }
  ],
```

## Context after

  "patch_plans_first20": [
    {
      "id": "consistency_001",
      "area": "md_python",
      "target_files": [
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
      ],
      "manual_review_required": true,
      "cosmetic_patch_allowed": false,
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
