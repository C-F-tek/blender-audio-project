# Evidence Chunk 0006/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `835`
- line_end: `1109`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0005.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0007.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports. Preview: "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md" ], "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_revi...

## Context before

                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_019",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [

## Chunk content

```json
                "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1333` targeting `app.py`.",
              "edit_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1333`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_020",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1334` targeting `app.py`.",
              "edit_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1334`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `app.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
              "validation_commands": [
                "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
                "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
                "git diff --check",
                "git status --short"
              ],
              "stop_conditions": [
                "Stop if the edit is only whitespace, tag spacing or Markdown formatting without fixing the cited finding.",
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            }
          ]
        }
      }
    },
    {
      "path": "output/ai_pipeline/repository_change_proposals.json",
      "exists": true,
      "json_ok": true,
      "kind": "repository_change_proposals",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "repository_change_proposals",
        "passed": true,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": []
      }
    },
    {
      "path": "output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json",
      "exists": true,
      "json_ok": true,
      "kind": "post_validation_ai_work_packet",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "post_validation_ai_work_packet",
        "passed": true,
        "provider_execution_performed": null,
        "patch_application_performed": null,
        "source_writes_performed": null,
        "errors": [],
        "warnings": [],
        "context": {
          "context_files": [
            "AGENTS.md",
            "WORKFLOW.md",
            "docs/AI_DOCS_ENTRYPOINT.md",
            "docs/PROJECT_STATUS_POINT.md",
            "docs/TECH_DEBT_TRACKER.md",
            "docs/REFACTORING_AND_REUSE_PLAN.md",
            "docs/JSON_SCHEMAS.md",
            "docs/AI_ARTIFACT_SCHEMAS.md",
            "Tools/npu/pipeline/README.md",
            "Tools/validation/README.md",
            "./docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md",
            "./Tools/ai/run_agent_gpu_deep_planning_review.py",
            "./Tools/ai/run_agent_gpu_deep_planning_supervised.py",
            "./Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
            "./Tools/ai/build_agent_review_patch_plan.py"
          ],
          "excluded_context_files": [],
          "advisory_context_routing": {
            "quality_report_present": true,
            "advisory_lanes": [
              "ollama"
            ],
            "excluded_advisory_lanes": [
              "npu"
            ],
            "trusted_context_files": [
              {
                "path": "AGENTS.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "WORKFLOW.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/AI_DOCS_ENTRYPOINT.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/PROJECT_STATUS_POINT.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/TECH_DEBT_TRACKER.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/REFACTORING_AND_REUSE_PLAN.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/JSON_SCHEMAS.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/AI_ARTIFACT_SCHEMAS.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "Tools/npu/pipeline/README.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "Tools/validation/README.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "./docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "./Tools/ai/run_agent_gpu_deep_planning_review.py",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "./Tools/ai/run_agent_gpu_deep_planning_supervised.py",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "./Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "./Tools/ai/build_agent_review_patch_plan.py",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              }
            ],
            "excluded_context_files": [],
            "decisions": [
              {
                "path": "AGENTS.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "WORKFLOW.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/AI_DOCS_ENTRYPOINT.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/PROJECT_STATUS_POINT.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/TECH_DEBT_TRACKER.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/REFACTORING_AND_REUSE_PLAN.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/JSON_SCHEMAS.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "docs/AI_ARTIFACT_SCHEMAS.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "Tools/npu/pipeline/README.md",
                "lane": "",
                "trusted": true,
```

## Context after

                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "Tools/validation/README.md",
                "lane": "",
                "trusted": true,
                "reason": "not_a_tracked_workload_report",
                "classification": ""
              },
              {
                "path": "./docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md",
