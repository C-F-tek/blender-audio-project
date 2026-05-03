# Evidence Chunk 0001/0003

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_20260503-190820_recovered_220.json`
- source_sha256: `5fe73175e3f7654414e36fc39f0b48ea50b7660dc49c1a571474b02668874ab7`
- line_start: `2`
- line_end: `291`
- section_kinds: `['json_key_section']`
- previous_chunk_file: ``
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_run_telemetry_summary_20260503-190820_recovered_220_json_5fe73175e3f7_chunk_0002.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: schema_version; generated_at; repo_root; stamp; provider_execution_performed. Preview: "schema_version": 1, "kind": "full_toolbox_run_telemetry_summary", "generated_at": "2026-05-03T19:54:39", "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project", "stamp": "20260503-190820", "passed": true, "errors": [], "warnings": [], "provider_execu...

## Context before

{

## Chunk content

```json
  "schema_version": 1,
  "kind": "full_toolbox_run_telemetry_summary",
  "generated_at": "2026-05-03T19:54:39",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "stamp": "20260503-190820",
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
    "decision_loop": "output/ai_pipeline/full_toolbox_20260503-190820_agent_review_decision_loop_recovered_220.json",
    "recommendations": "output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json",
    "patch_plan": "output/patch_specs/full_toolbox_20260503-190820_agent_review_patch_plan_recovered_220.json",
    "repository_consistency": "output/analysis/repository_consistency_map_full_toolbox_20260503-190820.json",
    "repository_consistency_smoke": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-190820.json",
    "gpu_npu_sync": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.json",
    "orchestrator": "output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json",
    "gpu_report": "output/ai_pipeline/full_toolbox_20260503-190820_parallel_gpu.json"
  },
  "run_parameters": {
    "budget_minutes": 90,
    "max_rounds": 90,
    "files_per_round": 10,
    "max_context_files": 500,
    "max_chars_per_file": 8000,
    "max_new_tokens": 4800,
    "npu_auditor_every_rounds": 6,
    "repository_consistency_map_workers": 8
  },
  "workflow_summary": {
    "passed": true,
    "recommendation_count": 220,
    "patch_plan_count": 220,
    "deterministic_synthesizer_used": true,
    "patch_plan_fallback_used": null,
    "bundle_validation_passed": true,
    "evidence_to_commit": [
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\runtime_tool_usage_telemetry_20260503-190820.json",
      ".\\docs\\LOCAL_VALIDATION_EVIDENCE\\runtime_tool_usage_telemetry_20260503-190820.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/pr114_gpu_json_contract_replay_bundle_20260502-210324.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md"
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
        "docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_20260502-195523.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_python_command_script_missing",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_015",
      "area": "md_powershell",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_mentions_missing_powershell_path",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_016",
      "area": "md_powershell",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_mentions_missing_powershell_path",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_017",
      "area": "md_powershell",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/AUTO_PUSH_GENERATED_ARTIFACTS.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_mentions_missing_powershell_path",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_018",
      "area": "md_powershell",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_mentions_missing_powershell_path",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_019",
      "area": "md_powershell",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_mentions_missing_powershell_path",
      "repository_consistency_severity": "high"
    },
    {
      "id": "consistency_020",
      "area": "md_powershell",
      "risk": "medium",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-182047.md"
      ],
      "source": "repository_consistency_map",
      "repository_consistency_kind": "md_mentions_missing_powershell_path",
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
