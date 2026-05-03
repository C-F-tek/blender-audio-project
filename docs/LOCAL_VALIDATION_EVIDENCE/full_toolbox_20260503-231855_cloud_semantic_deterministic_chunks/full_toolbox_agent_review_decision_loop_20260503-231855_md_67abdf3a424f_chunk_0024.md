# Evidence Chunk 0024/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `4190`
- line_end: `4406`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0023.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0025.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json`. Preview: ### `output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json` - Role: `auto_related_artifact` - Exists: `True` - Suffix: `.json` - Size bytes: `14649` - SHA-256: `ef62b3de8ee9ef8af2594a4425551bd919b2ca5be18d958b5adf44ceb806bd32` - Content included: `...

## Context before

- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_command_script_missing` at `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235` targeting `Tools/validation/check_markdown_command_hygiene.py`.
- Strategy: Build a focused patch plan for `md_python_command_script_missing` using mapper evidence `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md:1235`. Target `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md` and resolve `Tools/validation/check_markdown_command_hygiene.py` without formatting-only edits. Mapper recommendation: Update the command to a real script path or remove the obsolete command.

### consistency_017 — md_python
- Source: `repository_consistency_map`
- Status: `ready_for_patch_plan`
- Risk: `medium`
- Target files: `['docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md']`
- Rationale: Repository consistency mapper reported high `md_python_
```


## Chunk content

````md
### `output/ai_pipeline/full_toolbox_20260503-231855_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `14649`
- SHA-256: `ef62b3de8ee9ef8af2594a4425551bd919b2ca5be18d958b5adf44ceb806bd32`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-03T23:22:54",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 118.039,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 50.391,\n  \"round_count\": 4,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"empty_recommendations_reason\": \"model_output_schema_mismatch\",\n  \"runtime_tool_broker_enabled\": false,\n  \"runtime_tool_bootstrap_executed\": false,\n  \"runtime_tool_bootstrap_passed\": null,\n  \"runtime_tool_bootstrap_request_count\": 0,\n  \"runtime_tool_bootstrap_execution_count\": 0,\n  \"runtime_tool_bootstrap_failed_count\": 0,\n  \"runtime_tool_bootstrap_blocked_count\": 0,\n  \"runtime_tool_request_count\": 16,\n  \"runtime_tool_execution_count\": 0,\n  \"runtime_tool_failed_count\": 0,\n  \"runtime_tool_blocked_count\": 0,\n  \"runtime_tool_result_count\": 0,\n  \"provider_empty_response_count\": 0,\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/full_toolbox_20260503-231855_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "model_output_schema_mismatch",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "runtime_tool_broker_enabled": false,
  "runtime_tool_bootstrap_executed": false,
  "runtime_tool_bootstrap_passed": null,
  "runtime_tool_bootstrap_request_count": 0,
  "runtime_tool_bootstrap_execution_count": 0,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 16,
  "runtime_tool_execution_count": 0,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 0,
  "gpu_runtime_tool_broker_enabled": false,
  "gpu_runtime_tool_request_count": 16,
  "gpu_runtime_tool_execution_count": 0,
  "gpu_runtime_tool_failed_count": 0,
  "gpu_runtime_tool_blocked_count": 0,
  "gpu_runtime_tool_result_count": 0,
  "runtime_tool_provider_request_count": 16,
  "runtime_tool_provider_request_execution_count": 0,
  "runtime_tool_provider_request_failed_count": 0,
  "runtime_tool_provider_request_blocked_count": 0,
  "runtime_tool_provider_request_result_count": 0,
  "deterministic_runtime_tool_fallback_request_count": 0,
  "deterministic_runtime_tool_fallback_execution_count": 0,
  "deterministic_runtime_tool_fallback_failed_count": 0,
  "deterministic_runtime_tool_fallback_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap": {
    "enabled": false,
    "executed": false,
    "bootstrap": true,
    "requested_tool_count": 0,
    "tool_results": []
  },
  "orchestrator_runtime_tool_bootstrap_executed": false,
  "orchestrator_runtime_tool_bootstrap_passed": null,
  "orchestrator_runtime_tool_bootstrap_request_count": 0,
  "orchestrator_runtime_tool_bootstrap_execution_count": 0,
  "orchestrator_runtime_tool_bootstrap_failed_count": 0,
  "orchestrator_runtime_tool_bootstrap_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap_result_count": 0,
  "gpu_orchestrated_runtime_tool_brokers": [],
  "gpu_orchestrated_runtime_tool_request_count": 0,
  "gpu_orchestrated_runtime_tool_execution_count": 0,
  "gpu_orchestrated_runtime_tool_failed_count": 0,
  "gpu_orchestrated_runtime_tool_blocked_count": 0,
  "gpu_orchestrated_runtime_tool_result_count": 0,
  "gpu_runner_direct_runtime_tool_broker": false,
  "gpu_summary": {
    "passed": true,
    "round_count": 4,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 0,
    "repair_attempt_count": 0,
    "empty_recommendations_reason": "model_output_schema_mismatch",
    "evidence_ready_for_manual_patch_count": 12,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_request_count": 16,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_result_count": 0,
    "decision": {
      "ready_for_patch_plan": false,
      "ready_count": 0,
      "needs_more_context_count": 0,
      "fallback_patch_plan_recommended": true,
      "npu_auditor_non_blocking": true,
      "npu_unusable_or_failed_count": 0,
      "npu_audit_success_count": 0,
      "npu_auditor_disabled_reason": "",
      "recommended_next_layer": "build_agent_review_patch_plan.py",
      "manual_review_required": true
    },
    "gpu_direct_runtime_tool_request_count": 16,
    "gpu_direct_runtime_tool_execution_count": 0,
    "gpu_direct_runtime_tool_failed_count": 0,
    "gpu_direct_runtime_tool_blocked_count": 0,
    "gpu_direct_runtime_tool_provider_request_count": 16,
    "gpu_direct_runtime_tool_provider_request_execution_count": 0,
    "gpu_direct_runtime_tool_feedback_context_report_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_request_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_execution_count": 0,
    "gpu_lane": {
      "mode": "primary_fast_loop",
      "provider_execution_performed": true,
      "round_count": 4,
      "recommendation_count": 0,
      "empty_recommendations_reason": "model_output_schema_mismatch",
      "direct_runtime_tool_execution_count": 0,
      "direct_provider_request_execution_count": 0,
      "feedback_context_report_count": 0
    },
    "runtime_tool_feedback_context_report_count": 0
  },
  "checkpoint_dir": "output/ai_pipeline/full_toolbox_20260503-231855_checkpoints",
  "npu_audit_count": 1,
  "npu_audit_success_count": 1,
  "npu_tool_context_seen_count": 0,
  "npu_tool_request_count": 0,
  "npu_deterministic_tool_fallback_count": 0,
  "npu_runtime_tool_request_count": 0,
  "npu_runtime_tool_execution_count": 0,
  "npu_runtime_tool_failed_count": 0,
  "npu_runtime_tool_blocked_count": 0,
  "npu_runtime_tool_result_count": 0,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260503-231855_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260503-231855_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-03T23:21:08",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-231855_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "8000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "skipped",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T23:22:52",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-231855_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    }
  ],
  "decision": {
    "gpu_review_blocked_by_npu": false,
    "npu_auditor_mode": "parallel_best_effort",
    "npu_audit_success_count": 1,
    "npu_tool_context_seen_count": 0,
    "npu_tool_request_count": 0,
    "npu_deterministic_tool_fallback_count": 0,
    "npu_runtime_tool_request_count": 0,
    "npu_runtime_tool_execution_count": 0,
    "npu_runtime_tool_failed_count": 0,
    "npu_runtime_tool_blocked_count": 0,
    "npu_runtime_tool_result_count": 0,
    "ready_for_patch_plan": false,
    "fallback_patch_plan_recommended": true,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
````

## Context after

    "gpu_empty_recommendations_reason": "model_output_schema_mismatch",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_bootstrap_executed": false,
    "runtime_tool_bootstrap_execution_count": 0,
    "runtime_tool_provider_request_count": 0,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic_runtime_tool_fallback_execution_count": 0,
    "runtime_tool_execution_count": 0,
    "runtime_tool_result_count": 0,
    "manual_review_required": true,
    "gpu_lane_mode": "primary_fast_loop",
    "npu_lane_mode": "slow",
