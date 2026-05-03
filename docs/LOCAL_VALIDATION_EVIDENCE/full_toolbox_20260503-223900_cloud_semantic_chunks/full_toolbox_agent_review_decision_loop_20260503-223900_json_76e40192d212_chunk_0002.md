# Evidence Chunk 0002/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `58`
- line_end: `397`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0001.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0003.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: generare e validare report di pipeline AI per orchestrazione GPU/NPU, pianificazione, analisi repository, interpretazione codice e sintassi Python.  
**Segnali principali**: tutti i report hanno `passed:true`; nessun errore o warning; patch_application e source_writes non eseguiti; 154

## Context before

    "output/ai_pipeline/full_toolbox_20260503-223900_bridge_orchestrator.json",
    "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
    "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.md",
    "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json",
    "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.md",
    "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
    "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.md",
    "output/ai_pipeline/repository_change_proposals.md",
    "output/analysis/code_interpreter_full_toolbox_20260503-223900.md",
    "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-223900.md",
    "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-223900.md"
  ],

## Chunk content

```json
  "reports": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json",
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
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json",
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
        "round_count": 8,
        "empty_recommendations_reason": "context_echo_detected",
        "evidence_ready_for_manual_patch_count": 12,
        "recommended_next_layer": "build_agent_review_patch_plan.py"
      }
    },
    {
      "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-223900.json",
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
      "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-223900.json",
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
      "path": "output/analysis/code_interpreter_full_toolbox_20260503-223900.json",
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
        "recommendation_count": 154
      }
    },
    {
      "path": "output/validation/python_line_count_full_toolbox_20260503-223900.json",
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
      "path": "output/validation/python_syntax_full_toolbox_20260503-223900.json",
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
      "path": "output/validation/gpu_planner_json_contract_smoke_full_toolbox_20260503-223900.json",
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
      "path": "output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_20260503-223900.json",
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
      "path": "output/validation/agent_review_decision_loop_smoke_full_toolbox_20260503-223900.json",
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
      "path": "output/validation/npu_provider_environment_full_toolbox_20260503-223900.json",
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
      "path": "output/analysis/gpu_json_contract_replay_full_toolbox_20260503-223900.json",
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
      "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-223900.json",
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
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_deterministic_recommendations.json",
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
        "recommendation_count": 40
      }
    },
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_bridge_orchestrator.json",
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
      "path": "output/ai_pipeline/full_toolbox_20260503-223900_agent_review_decision_loop.json",
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
        "patch_plan_count": 40,
        "manual_review_required": true,
        "recommendation_count": 40
      }
    },
    {
      "path": "output/patch_specs/full_toolbox_20260503-223900_agent_review_patch_plan.json",
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
        "patch_plan_count": 40,
        "patch_plan_summary": {
          "patch_plan_count": 40,
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
