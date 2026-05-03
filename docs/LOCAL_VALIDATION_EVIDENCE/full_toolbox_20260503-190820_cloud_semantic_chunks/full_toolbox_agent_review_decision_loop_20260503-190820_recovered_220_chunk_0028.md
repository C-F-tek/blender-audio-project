# Evidence Chunk 0028/0041

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220.md`
- source_sha256: `8ed89af8ed3e4fa6f8a1a3a56da19fd97a274354793464078ec9f92deaf33e83`
- line_start: `3132`
- line_end: `3307`
- section_kinds: `['markdown_heading_section_split']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0027.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-190820_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-190820_recovered_220_chunk_0029.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Eseguire audit NPU/GPU deep‑review per i checkpoint delle iterazioni 18 e 24 del pipeline AI.  
**Segnali principali**: audit termin

## Context before

        "3000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 6,
      "finished_at": "2026-05-03T19:18:32",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_012_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_012_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",

## Chunk content

```md
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
    },
    {
      "round": 18,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_018.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_018_npu_async_audit.json",
      "started_at": "2026-05-03T19:19:46",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_018.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_018_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_018_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_018_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_018_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_018_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_018_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "3000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 6,
      "finished_at": "2026-05-03T19:21:30",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_018_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_018_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
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
    },
    {
      "round": 24,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_024.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_024_npu_async_audit.json",
      "started_at": "2026-05-03T19:23:18",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_024_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "3000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 6,
      "finished_at": "2026-05-03T19:25:04",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_024_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_024_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
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
    },
    {
      "round": 30,
      "checkpoint": "output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_030.json",
      "audit_output": "output/ai_pipeline/full_toolbox_20260503-190820_checkpoints/round_030_npu_async_audit.json",
      "started_at": "2026-05-03T19:26:20",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_030.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_030_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_030_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_030_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_030_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_030_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\full_toolbox_20260503-190820_checkpoints\\round_030_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "420",
        "--max-context-chars",
        "3000",
        "--max-prompt-chars",
        "1200",
        "--max-new-tokens",
        "384",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 6,
      "finished_at": "2026-05-03T19:28:04",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_030_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\full_toolbox_20260503-190820_checkpoints\\\\round_030_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
```

## Context after

      "provider_execution_requested": true,
      "provider_load_attempted"
```

### `output/ai_pipeline/full_toolbox_20260503-190820_deterministic_recommendations_recovered_220.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `1563444`
- SHA-256: `5e47daa32352033f202ac54e5c6a798dac09a8689cceb30fd033108e1e72f821`
- Content included: `True`
