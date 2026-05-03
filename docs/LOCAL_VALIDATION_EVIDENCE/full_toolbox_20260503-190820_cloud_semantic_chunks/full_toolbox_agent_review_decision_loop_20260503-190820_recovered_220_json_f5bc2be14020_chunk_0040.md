# Evidence Chunk 0040/0110

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.json`
- source_sha256: `f5bc2be14020dc547c7f7a03b7b3f51eeb29490d4cc34a108fd427e6db624f4a`
- line_start: `5736`
- line_end: `5766`
- section_kinds: `['json_key_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0039.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_json_f5bc2be14020_chunk_0041.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: selected_chunks_evidence. Preview: "selected_chunks_evidence": [ { "path": "docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json", "exists": true, "json_ok": true, "kind": "selected_semantic_chunks_evidence", "passed": true, "summary": { "schema_version": 1, "kind": ...

## Context before

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
    }
  ],

## Chunk content

```json
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
      "path": "output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 46914,
      "sha256": "4d48c0a3aa8e35c16db123a614a511def22c3a1f63a9ebcd7427849fb5387afb",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_npu_parallel_orchestrator\",\n  \"generated_at\": \"2026-05-03T19:38:46\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": false,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_parallel_gpu_planner_npu_auditor\",\n  \"elapsed_seconds\": 1686.543,\n  \"gpu_returncode\": 2,\n  \"gpu_stdout_tail\": \"{\\n  \\\"passed\\\": false,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-190820_parallel_gpu.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_20260503-190820_parallel_gpu.md\\\",\\n  \\\"provider_execution_performed\\\": true,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"elapsed_seconds\\\": 1679.037,\\n  \\\"round_count\\\": 50,\\n  \\\"npu_audit_count\\\": 0,\\n  \\\"npu_audit_success_count\\\": 0,\\n  \\\"npu_auditor_disabled_reason\\\": \\\"\\\",\\n  \\\"recommendation_count\\\": 0,\\n  \\\"raw_recommendation_candidate_count\\\": 0,\\n  \\\"filtered_recommendation_count\\\": 0,\\n  \\\"tool_request_count\\\": 0,\\n  \\\"valid_tool_request_count\\\": 0,\\n  \\\"invalid_tool_request_count\\\": 0,\\n  \\\"empty_recommendations_reason\\\": \\\"json_parse_failure\\\",\\n  \\\"runtime_tool_broker_enabled\\\": false,\\n  \\\"runtime_tool_bootstrap_executed\\\": false,\\n  \\\"runtime_tool_bootstrap_passed\\\": null,\\n  \\\"runtime_to",
      "preview_chars": 1500,
      "line_count": 738
