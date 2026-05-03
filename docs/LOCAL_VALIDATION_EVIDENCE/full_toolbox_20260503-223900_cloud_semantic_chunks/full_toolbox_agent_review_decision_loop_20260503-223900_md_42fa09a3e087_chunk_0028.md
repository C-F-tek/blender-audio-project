# Evidence Chunk 0028/0031

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.md`
- source_sha256: `42fa09a3e087ebc6b51a8d9d2d501922dd8ed8c400791441877ab803557340fa`
- line_start: `4591`
- line_end: `4734`
- section_kinds: `['markdown_heading_section', 'markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0027.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0029.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: `output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.json`; `output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.md`; Agent GPU/NPU Parallel Orchestrator; Decision; NPU Audits. Preview: "--output", "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006_npu_async_audit.json", "--markdown-output", "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_too...

## Context before

      "round": 6,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260503-223900_checkpoints/round_006.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260503-223900_checkpoints/round_006_npu_async_audit.json",
      "started_at": "2026-05-03T22:43:50",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006.json",

## Chunk content

````md
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-223900_checkpoints\\round_006_npu_async_audit_metadata.json",
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
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 6,
      "finished_at": "2026-05-03T22:45:28",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-223900_checkpoints\\\\round_006_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-223900_checkpoints\\\\round_006_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
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
    "npu_audit_success_count": 2,
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
    "gpu_empty_recommendations_reason": "context_echo_detected",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_bootstrap_executed": false,
    "runtime_tool_bootstrap_execution_count": 0,
    "runtime_tool_provider_request_count": 0,
    "runtime_tool_provider_request_execution_count": 0,
    "deterministic
```

### `output/ai_pipeline/full_toolbox_20260503-223900_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2387`
- SHA-256: `2e0a8ed29c4616ab0a369c6b43499e2957c84ac7cfed4847aaf694a2e57f0f11`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `278.09`
- `npu_audit_count`: `2`
- `npu_audit_success_count`: `2`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `gpu_evidence_ready_for_manual_patch_count`: `12`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `28`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `2`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_deterministic_tool_fallback_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `True`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_bootstrap_executed`: `False`
- `runtime_tool_bootstrap_execution_count`: `0`
- `runtime_tool_provider_request_count`: `0`
- `runtime_tool_provider_request_execution_count`: `0`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_result_count`: `0`
- `manual_review_required`: `True`
- `gpu_lane_mode`: `primary_fast_loop`
- `npu_lane_mode`: `slow`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `6`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `6` status=`finished` class=`usable_audit_text` success=`True`

```

````

## Context after

### `output/ai_pipeline/full_toolbox_20260503-223900_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `68132`
- SHA-256: `c62431d23c5e6894a6e5413eff1074d8fdf62669d2b9a43563bae9bbc3bfbcbb`
- Content included: `True`
- Content truncated: `True`

```text
{
