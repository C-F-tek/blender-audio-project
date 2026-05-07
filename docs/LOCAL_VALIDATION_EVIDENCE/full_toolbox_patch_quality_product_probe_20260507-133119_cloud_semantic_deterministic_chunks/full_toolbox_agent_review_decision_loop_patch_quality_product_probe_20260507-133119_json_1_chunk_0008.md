# Evidence Chunk 0008/0120

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119.json`
- source_sha256: `1df132b8718338e0ec5b905ec0ea9078464e7ea07b84f9506f685b5ac0618fac`
- line_start: `1554`
- line_end: `1628`
- section_kinds: `['json_key_section', 'json_key_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0007.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_patch_quality_product_probe_20260507-133119_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_patch_quality_product_probe_20260507-133119_json_1_chunk_0009.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: reports; selected_chunks_evidence. Preview: "validation_commands": [ "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json", "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contr...

## Context before

            },
            {
              "id": "consistency_050",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101` targeting `validate_after_patch.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md:101`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-001.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",

## Chunk content

```json
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
              "id": "consistency_051",
              "area": "md_powershell",
              "source": "gpu_recommendation",
              "risk": "medium",
              "status": "ready_for_manual_review",
              "target_files": [
                "docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md"
              ],
              "rationale": "Repository consistency mapper reported high `md_mentions_missing_powershell_path` at `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330` targeting `validate_after_patch.ps1`.",
              "edit_strategy": "Build a focused patch plan for `md_mentions_missing_powershell_path` using mapper evidence `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md:330`. Target `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure/part-003.md` and resolve `validate_after_patch.ps1` without formatting-only edits. Mapper recommendation: Correct the documentation reference or restore the missing target if it is still required.",
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
      "path": "output/ai_pipeline/full_toolbox_patch_quality_product_probe_20260507-133119_orchestrator.json",
      "exists": true,
      "suffix": ".json",
      "size_bytes": 72790,
      "sha256": "b652af93b70b46f7c9059d998c48b8bf641ca2617fe268c3b6b30ace0b64d52c",
      "role": "local_artifact_reference",
      "content_included": true,
      "preview": "{\n  \"schema_version\": 1,\n  \"kind\": \"agent_gpu_npu_parallel_orchestrator\",\n  \"generated_at\": \"2026-05-07T13:33:23\",\n  \"repo_root\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\",\n  \"passed\": true,\n  \"errors\": [],\n  \"warnings\": [],\n  \"provider_execution_performed\": true,\n  \"gpu_provider_execution_performed\": true,\n  \"gpu0_peer_support_provider_execution_performed\": true,\n  \"npu_provider_execution_performed\": false,\n  \"legacy_npu_provider_execution_performed\": false,\n  \"npu_micro_support_provider_execution_performed\": false,\n  \"npu_micro_support_provider_requested\": false,\n  \"legacy_npu_auditor_provider_requested\": false,\n  \"npu_auditor_provider_requested\": false,\n  \"npu_auditor_provider_performed\": false,\n  \"provider_degraded_reasons\": [],\n  \"patch_application_performed\": false,\n  \"source_writes_performed\": false,\n  \"apply_mode\": \"report_only_parallel_gpu_planner_npu_auditor\",\n  \"elapsed_seconds\": 61.694,\n  \"gpu_returncode\": 0,\n  \"gpu_stdout_tail\": \"{\\n  \\\"passed\\\": true,\\n  \\\"output\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.json\\\",\\n  \\\"markdown\\\": \\\"C:\\\\\\\\Users\\\\\\\\carmi\\\\\\\\blender\\\\\\\\blender-audio-project\\\\\\\\output\\\\\\\\ai_pipeline\\\\\\\\full_toolbox_patch_quality_product_probe_20260507-133119_parallel_gpu.md\\\",\\n  \\\"provider_execution_performed\\\": true,\\n  \\\"patch_application_performed\\\": false,\\n  \\\"elapsed_seconds\\\": 50.767,\\n  \\\"round_count\\\": 4,\\n  \\\"npu_a",
      "preview_chars": 1500,
      "line_count": 1067
