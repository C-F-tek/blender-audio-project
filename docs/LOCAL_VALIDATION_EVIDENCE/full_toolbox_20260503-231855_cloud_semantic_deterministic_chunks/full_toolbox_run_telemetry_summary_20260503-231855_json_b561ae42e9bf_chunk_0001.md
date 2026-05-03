# Evidence Chunk 0001/0003

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260503-231855.json`
- source_sha256: `b561ae42e9bfddc6c9da4bccc7995e3e0a4aee729120a9177c2e517d9ff3c65e`
- line_start: `2`
- line_end: `295`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_run_telemetry_summary_20260503-231855_json_b561ae42e9bf_chunk_0002.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; stamp; provider_execution_performed. Preview: "schema_version": 1, "kind": "full_toolbox_run_telemetry_summary", "generated_at": "2026-05-03T23:22:58", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "stamp": "20260503-231855", "passed": true, "errors": [], "warnings": [], "provider_execu...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "full_toolbox_run_telemetry_summary",
  "generated_at": "2026-05-03T23:22:58",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "stamp": "20260503-231855",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "sqlite_write_performed": false,
  "persistent_memory_write_performed": false,
  "manual_review_required": true,
  "inputs": {
    "decision_loop": "output/ai_pipeline/full_toolbox_20260503-231855_agent_review_decision_loop.json",
    "recommendations": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
    "patch_plan": "output/patch_specs/full_toolbox_20260503-231855_agent_review_patch_plan.json",
    "repository_consistency": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
    "repository_consistency_smoke": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-231855.json",
    "gpu_npu_sync": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.json",
    "orchestrator": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
    "gpu_report": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json"
  },
  "run_parameters": {
    "budget_minutes": 8,
    "max_rounds": 4,
    "files_per_round": 6,
    "max_context_files": 80,
    "max_chars_per_file": 5000,
    "max_new_tokens": 2400,
    "npu_auditor_every_rounds": 4,
    "repository_consistency_map_workers": 8
  },
  "workflow_summary": {
    "passed": true,
    "recommendation_count": 20,
    "patch_plan_count": 20,
    "deterministic_synthesizer_used": true,
    "patch_plan_fallback_used": null,
    "bundle_validation_passed": true,
    "evidence_to_commit": [
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_memory_tool_regeneration_bundle_20260503-231855.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_memory_tool_regeneration_bundle_20260503-231855.md",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_memory_tool_regeneration_python_line_count_20260503-231855.csv",
      "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-231930.csv",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_toolbox_agent_review_decision_loop_20260503-231855.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_toolbox_agent_review_decision_loop_20260503-231855.md",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\shared_toolbox_ai_to_ai_bundle_20260503-231855.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\shared_toolbox_ai_to_ai_bundle_20260503-231855.md"
    ]
  },
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
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
