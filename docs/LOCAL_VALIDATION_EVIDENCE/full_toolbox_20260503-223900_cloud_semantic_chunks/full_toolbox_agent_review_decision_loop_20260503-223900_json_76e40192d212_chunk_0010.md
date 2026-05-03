# Evidence Chunk 0010/0092

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.json`
- source_sha256: `76e40192d2124d0e85d076bdbcc3a2249446979db38750fe7199ee17d457a16a`
- line_start: `1322`
- line_end: `1591`
- section_kinds: `['json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0009.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_json_76e40192d212_chunk_0011.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports. Preview: "Stop if the target/source evidence no longer exists after refreshing master.", "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.", "Stop if resolving the finding requires inventing behavior not supported ...

## Context before

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

## Chunk content

```json
                "Stop if the target/source evidence no longer exists after refreshing master.",
                "Stop if the fix would touch output/**, generated indexes, SQLite, provider settings or Blender runtime.",
                "Stop if resolving the finding requires inventing behavior not supported by code evidence."
              ],
              "manual_review_required": true
            },
            {
              "id": "consistency_039",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md:495` targeting `run_agent.py`.",
              "edit_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md:495`. Target `docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md` and resolve `run_agent.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
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
              "id": "consistency_040",
              "area": "md_python",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md:500` targeting `run_agent.py`.",
              "edit_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md:500`. Target `docs/LOCAL_VALIDATION_EVIDENCE/pr111_gpu_repair_failure_recommendation_bundle_20260502-202906.md` and resolve `run_agent.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
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
```

## Context after

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
