# Evidence Chunk 0007/0081

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.json`
- source_sha256: `df2ddd91f8e75a76d63e8a525113ba6bbaeb9c3f8942dc8efbcd0a0e343e96ef`
- line_start: `1110`
- line_end: `1234`
- section_kinds: `['json_key_section', 'json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0006.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_json_df2ddd91f8e7_chunk_0008.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports; selected_chunks_evidence. Preview: "reason": "not_a_tracked_workload_report", "classification": "" }, { "path": "Tools/validation/README.md", "lane": "", "trusted": true, "reason": "not_a_tracked_workload_report", "classification": "" }, { "path": "./docs/LOCAL_AI_TASKS/improve-gpu-planner-none...

## Context before

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

## Chunk content

```json
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
            "enforced": true,
            "policy": "quality-approved-workload-context-only",
            "provider_execution_performed": false
          }
        },
        "ollama": {
          "used": false,
          "model": null,
          "error": "",
          "text_preview": ""
        }
      }
    },
    {
      "path": "output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json",
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
      "path": "output/validation/full_memory_tool_regeneration_20260503-231855_workflow.json",
      "exists": true,
      "json_ok": true,
      "kind": "full_memory_tool_regeneration_workflow",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "full_memory_tool_regeneration_workflow",
        "passed": true,
        "provider_execution_performed": false,
        "patch_application_performed": false,
        "source_writes_performed": false,
        "errors": [],
        "warnings": []
      }
    }
  ],
  "selected_chunks_evidence": [
    {
      "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json",
      "exists": true,
      "json_ok": true,
      "kind": "selected_semantic_chunks_evidence",
      "passed": true,
      "summary": {
        "schema_version": 1,
        "kind": "selected_semantic_chunks_evidence",
        "passed": true,
        "provider_execution_performed": false,
        "source_writes_performed": false,
        "selected_count": 24,
        "total_selected_chars": 28649,
        "max_chunks": 24,
        "max_total_chars": 32000,
        "source_bundle": "output/ai_context_packs/full_context_golden_selected_chunks.json",
        "source_chunks": "indexAI/code_chunks/semantic_code_chunks.json",
        "decision": {
          "selected_chunks_built": true,
          "budget_respected": true,
          "provider_execution_seen": false,
          "source_writes_performed": false,
          "forbidden_paths_blocked": true
        },
        "errors": [],
        "warnings": []
      }
    }
  ],
```

## Context after

  "artifact_manifest": [
    {
      "path": "output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 14649,
      "sha256": "ef62b3de8ee9ef8af2594a4425551bd919b2ca5be18d958b5adf44ceb806bd32",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_npu_parallel_orchestrator\",\n  \"generated_at\": \"2026-05-03T23:22:54\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_parallel_gpu_planner_npu_auditor\",\n  \"elapsed_seconds\": 118.039,\n  \"gpu_returncode\": 0,\n  \"gpu_stdout_tail\": \"{\\n  \\\"passed\\\": true,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-231855_parallel_gpu.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-231855_parallel_gpu.md\\\",\\n  \\\"provider_execution_performed\\\": true,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"elapsed_seconds\\\": 50.391,\\n  \\\"round_count\\\": 4,\\n  \\\"npu_audit_count\\\": 0,\\n  \\\"npu_audit_success_count\\\": 0,\\n  \\\"npu_auditor_disabled_reason\\\": \\\"\\\",\\n  \\\"recommendation_count\\\": 0,\\n  \\\"raw_recommendation_candidate_count\\\": 0,\\n  \\\"filtered_recommendation_count\\\": 0,\\n  \\\"tool_request_count\\\": 0,\\n  \\\"valid_tool_request_count\\\": 0,\\n  \\\"invalid_tool_request_count\\\": 0,\\n  \\\"empty_recommendations_reason\\\": \\\"model_output_schema_mismatch\\\",\\n  \\\"runtime_tool_broker_enabled\\\": false,\\n  \\\"runtime_tool_bootstrap_executed\\\": false,\\n  \\\"runtime_tool_bootstrap_passed\\\": null,\\n  \\\"runtim",
      "preview_chars": 1500,
      "line_count": 274
