# Evidence Chunk 0031/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `3594`
- line_end: `3875`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0030.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_md_8ed89af8ed3e_chunk_0032.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json`. Preview: "npu_runtime_tool_failed_count": null, "npu_runtime_tool_blocked_count": null }, { "round": 24, "status": "finished", "classification": "usable_audit_text", "runtime_tool_context_seen": false, "npu_tool_request_count": 0, "npu_runtime_tool_execution_count": nu...

## Context before

          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 18,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,

## Chunk content

```md
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 24,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 30,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 36,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 42,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        }
      ],
      "repository_consistency_finding": {
        "kind": "md_python_command_script_missing",
        "severity": "high",
        "source": "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md",
        "line": 368,
        "target": "Tools/validation/check_markdown_command_hygiene.py",
        "flag": "",
        "evidence": ""
      },
      "guardrails": {
        "patch_application_performed": false,
        "manual_review_required": true,
        "cosmetic_patch_allowed": false
      }
    },
    {
      "id": "consistency_003",
      "area": "md_python",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md"
      ],
      "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444` targeting `Tools/validation/check_markdown_command_hygiene.py`.",
      "proposed_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444`. Target `docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
      "risk": "medium",
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
      "source": "repository_consistency_map",
      "evidence": [
        "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md:444"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-190820.json",
          "kind": "repository_consistency_map",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-190820.json",
          "kind": "repository_consistency_map_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.json",
          "kind": "gpu_npu_run_sync_analysis",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        }
      ],
      "npu_audit_refs": [
        {
          "round": 1,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 6,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 12,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 18,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 24,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 30,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 36,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 42,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        }
      ],
      "repository_consistency_finding": {
        "kind": "md_python_command_script_missing",
        "severity": "high",
        "source": "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md",
        "line": 444,
        "target": "Tools/validation/check_markdown_command_hygiene.py",
        "flag": "",
        "evidence": ""
      },
      "guardrails": {
        "patch_application_performed": false,
        "manual_review_required": true,
        "cosmetic_patch_allowed": false
      }
    },
    {
      "id": "consistency_004",
      "area": "md_python",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md"
      ],
      "rationale": "Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77` targeting `Tools/validation/check_markdown_command_hygiene.py`.",
      "proposed_strategy": "Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77`. Target `docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.",
      "risk": "medium",
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
      "source": "repository_consistency_map",
      "evidence": [
        "docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md:77"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/repository_consistency_map_full_toolbox_20260503-190820.json",
          "kind": "repository_consistency_map",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/repository_consistency_map_smoke_full_toolbox_20260503-190820.json",
          "kind": "repository_consistency_map_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_npu_run_sync_full_toolbox_20260503-190820.json",
          "kind": "gpu_npu_run_sync_analysis",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        }
      ],
      "npu_audit_refs": [
        {
          "round": 1,
          "status": "finished",
```

## Context after

          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
     
```

### `output/ai_pipeline/full_toolbox_20260503-190820_orchestrator.json`

- Role: `auto_related_artifact`
