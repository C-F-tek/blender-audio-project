# Evidence Chunk 0002/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `58`
- line_end: `397`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0001.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0003.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports. Preview: "reports": [ { "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json", "exists": true, "json_ok": true, "kind": "agent_gpu_npu_parallel_orchestrator", "passed": true, "summary": { "schema_version": 1, "kind": "agent_gpu_npu_parallel_orches...

## Context before

    "output/ai_pipeline/full_toolbox_20260503-231855_bridge_orchestrator.json",
    "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
    "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.md",
    "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
    "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.md",
    "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
    "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.md",
    "output/ai_pipeline/repository_change_proposals.md",
    "output/analysis/code_interpreter_full_toolbox_20260503-231855.md",
    "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.md",
    "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.md"
  ],

## Chunk content

```json
  "reports": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_npu_parallel_orchestrator",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_gpu_npu_parallel_orchestrator",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_gpu_deep_planning_supervised",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_gpu_deep_planning_supervised",
        "passed": true,
        "provider_execution_performed": true,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "recommendation_count": 0,
        "round_count": 4,
        "empty_recommendations_reason": "model_output_schema_mismatch",
        "evidence_ready_for_manual_patch_count": 12,
        "recommended_next_layer": "build_agent_review_patch_plan.py"
      }
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "repository_consistency_map",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_consistency_map_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "repository_consistency_map_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/analysis/code_interpreter_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "code_interpreter_report",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "code_interpreter_report",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true,
        "recommendation_count": 155
      }
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_line_count_csv",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "python_line_count_csv",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/validation/python_syntax_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "python_syntax",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "python_syntax",
        "passed": true,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_planner_json_contract_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu_planner_json_contract_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "deterministic_recommendation_synthesizer_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true,
        "recommendation_count": 1
      }
    },
    {
      "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop_smoke",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_review_decision_loop_smoke",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "patch_plan_count": 1,
        "manual_review_required": true,
        "recommendation_count": 1
      }
    },
    {
      "path": "output/validation/npu_provider_environment_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "npu_provider_environment",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "npu_provider_environment",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "checks": {}
      }
    },
    {
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_planner_json_contract_replay",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu_planner_json_contract_replay",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-231855.json",
      "exists": true,
      "json_ok": true,
      "kind": "gpu_npu_run_sync_analysis",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "gpu_npu_run_sync_analysis",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true
      }
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_deterministic_recommendations.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_synthesizer",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "deterministic_recommendation_synthesizer",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "manual_review_required": true,
        "recommendation_count": 20
      }
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_bridge_orchestrator.json",
      "exists": true,
      "json_ok": true,
      "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_agent_review_decision_loop.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_decision_loop",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_review_decision_loop",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "patch_plan_count": 20,
        "manual_review_required": true,
        "recommendation_count": 20
      }
    },
    {
      "path": "output/patch_specs/full_toolbox_20260503-231855_agent_review_patch_plan.json",
      "exists": true,
      "json_ok": true,
      "kind": "agent_review_patch_plan",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "agent_review_patch_plan",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": [],
        "patch_plan_count": 20,
        "patch_plan_summary": {
          "patch_plan_count": 20,
          "fallback_used": false,
          "manual_review_required": true,
          "provider_execution_performed": false,
          "patch_application_performed": false,
          "source_writes_performed": false,
          "plans": [
            {
              "id": "consistency_001",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163` targeting `Tools/validation/check_markdown_command_hygiene.py`.",
              "edit_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:163`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
```

## Context after

                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_002",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
