# Local Validation Evidence Bundle

- Generated at: `2026-05-02T20:29:11`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `False`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `4`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/analysis/gpu_repair_failure_recommendation_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_repair_failure_recommendation`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

## Artifact manifest

- `output/analysis/gpu_repair_failure_recommendation_20260502-195523.json` exists=`True` size=`4158` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/gpu_repair_failure_recommendation_20260502-195523.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1685`
- SHA-256: `3c781126b689383a8366b931ac8258b39aa826f623a9ebd33699d4255c6d19b8`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Repair Failure Recommendation

- Passed: `True`
- Recommendation count: `1`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## GPU failure summary

- `gpu_recommendation_count`: `0`
- `raw_recommendation_candidate_count`: `0`
- `filtered_recommendation_count`: `0`
- `json_parse_error_count`: `16`
- `repair_attempt_count`: `18`
- `empty_recommendations_reason`: `repair_attempt_failed`
- `evidence_ready_for_manual_patch_count`: `12`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`

## Recommendations

### `gpu_repair_failure_001` — provider_orchestration

- Status: `ready_for_manual_review`
- Risk: `medium`
- Target files: `Tools/ai/run_agent_gpu_deep_planning_review.py, Tools/ai/run_agent_gpu_deep_planning_supervised.py, Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py, docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md`
- Rationale: GPU/Ollama provider execution completed but produced zero usable recommendations because `repair_attempt_failed` was reported while 12 manual-review evidence candidates were ready.
- Strategy: Make the repair-failure path explicit in reports and review flow: preserve parse diagnostics, surface fallback plan readiness, and route reviewers to the deterministic manual-review patch-plan layer instead of leaving the result as an unexplained empty recommendation set.
- Static/provider agreement: `provider_failure_mode_detected_with_static_evidence_ready`


```

### `docs/LOCAL_AI_TASKS/gpu-repair-failure-recommendation.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3692`
- SHA-256: `152a7a28619f30a29ee452ae74af8a56ba81d1aa35a10805011614ad2c0ca621`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Repair Failure Recommendation Layer

## Purpose

Document the report-only diagnostic layer for this observed failure mode:

```text
GPU/Ollama provider execution completed
recommendation_count == 0
empty_recommendations_reason == repair_attempt_failed
evidence_ready_for_manual_patch_count > 0
```

The goal is not to force the GPU planner to invent recommendations. The goal is to make this state explicit, auditable and actionable by emitting one deterministic manual-review recommendation that routes reviewers to the fallback patch-plan layer.

## Tool

```text
Tools/ai/build_gpu_repair_failure_recommendation.py
```

## Inputs

```text
orchestrator report JSON
GPU planner report JSON
```

Typical project-complete run inputs:

```text
output/ai_pipeline/project_complete_<STAMP>_orchestrator.json
output/ai_pipeline/project_complete_<STAMP>_parallel_gpu.json
```

## Command

```powershell
python .\Tools\ai\build_gpu_repair_failure_recommendation.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_<STAMP>_orchestrator.json" `
  --gpu-report ".\output\ai_pipeline\project_complete_<STAMP>_parallel_gpu.json" `
  --output ".\output\analysis\gpu_repair_failure_recommendation_<STAMP>.json" `
  --markdown-output ".\output\analysis\gpu_repair_failure_recommendation_<STAMP>.md"
```

## Output behavior

When the repair-failure state is detected, the report emits:

```text
kind: gpu_repair_failure_recommendation
recommendation_count: 1
recommendations[0].id: gpu_repair_failure_001
recommendations[0].status: ready_for_manual_review
recommended_next_layer: build_agent_review_patch_plan.py
```

Guardrails stay report-only:

```text
provider_execution_performed=false
patch_application_performed=false
source_writes_performed=false
blender_runtime_execution_performed=false
sqlite_write_performed=false
manual_review_required=true
```

## Why the JSON broke in the reference run

The reference run showed:

```text
GPU/Ollama provider execution: true
round_count: 24
recommendation_count: 0
raw_recommendation_candidate_count: 0
filtered_recommendation_count: 0
json_parse_error_count: 16
empty_recommendations_reason: repair_attempt_failed
evidence_ready_for_manual_patch_count: 12
```

Operational interpretation:

```text
The local provider ran and returned text, but enough rounds failed the strict JSON contract that the repair layer could not recover valid recommendation objects.
The model did not produce parseable recommendation candidates, even though the deterministic evidence layer had ready manual-review candidates.
The correct next layer is therefore the fallback manual-review patch-plan builder, not a forced or hallucinated GPU recommendation.
```

Likely contributing causes to inspect in future work:

```text
prompt too large or too mixed between instructions, evidence and file previews
model returning prose or partially fenced JSON instead of one strict JSON object
model output truncation or malformed escaping in long recommendation fields
local parser not reusing the shared Tools.ai.model_json helper everywhere
post-validation packet currently reporting Ollama used=false in the included evidence, which may hide provider-path expectations for that stage
```

## Future fix direction

Small safe follow-ups:

```text
reuse Tools.ai.model_json.parse_model_json_object in GPU planner parsing paths
add explicit JSON-only prompt footer with a minimal schema example
record first parse error, repair attempt count and raw response preview hash per failed round
emit gpu_repair_failure_recommendation as an input to the compact evidence bundle
```

Do not change provider/model settings until the diagnostic path is validated.

```

### `output/ai_pipeline/project_complete_20260502-195523_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `20138`
- SHA-256: `fdf74c5801328d125e3d5d7bbb422b25f0ebb4327d487b85648685e7fc59a3e9`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-02T20:09:33",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 706.195,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 668.685,\n  \"round_count\": 24,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"empty_recommendations_reason\": \"repair_attempt_failed\",\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "repair_attempt_failed",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "gpu_summary": {
    "passed": true,
    "round_count": 24,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 16,
    "repair_attempt_count": 18,
    "empty_recommendations_reason": "repair_attempt_failed",
    "evidence_ready_for_manual_patch_count": 12,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
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
    }
  },
  "checkpoint_dir": "output/ai_pipeline/project_complete_20260502-195523_checkpoints",
  "npu_audit_count": 5,
  "npu_audit_success_count": 5,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-02T19:58:59",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:01:07",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "gpu_review_blocked": false
    },
    {
      "round": 4,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_004.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_004_npu_async_audit.json",
      "started_at": "2026-05-02T20:01:09",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:03:19",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_004_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_004_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "gpu_review_blocked": false
    },
    {
      "round": 8,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_008.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_008_npu_async_audit.json",
      "started_at": "2026-05-02T20:03:21",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:05:23",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_008_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_008_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": tru
```

### `output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `168570`
- SHA-256: `de0459178f46139aed0082527cee52e879b86d459684b84c0addb822396109c8`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-02T20:08:56",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
  "model_used": "qwen2.5-coder:14b",
  "ollama_base_url": "http://127.0.0.1:11434",
  "budget_minutes": 30,
  "elapsed_seconds": 668.685,
  "context_file_count": 240,
  "round_count": 24,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 70.87,
      "file_count": 10,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md",
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md"
      ],
      "response_chars": 21255,
      "raw_response_preview": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"AGENTS.md\",\n      \"exists\": true,\n      \"lines\": 123,\n      \"chars\": 4567,\n      \"content_preview\": \"# AGENTS.md\\n\\n## Purpose\\n\\nThis file is the main machine-readable entry point for any AI agent, coding assistant or automated reviewer that starts inside this repository.\\n\\nIt should contain practical instructions for AI systems:\\n\\n- repository identity;\\n- important folders;\\n- safe commands;\\n- validation commands;\\n- permission boundaries;\\n- refactoring rules;\\n- expected reporting format.\"\n    },\n    {\n      \"path\": \"WORKFLOW.md\",\n      \"exists\": true,\n      \"lines\": 150,\n      \"chars\": 6789,\n      \"content_preview\": \"# WORKFLOW.md\\n\\n## Purpose\\n\\nThis document outlines the general workflow for contributing to this repository, including guidelines for code submission, validation, and review.\\n\\n## Key Steps\\n\\n1. **Fork the Repository**: Create a fork of the main repository on GitHub.\\n2. **Clone Your Fork**: Clone your forked repository to your local machine.\\n3. **Create a New Branch**: For each new feature or bug fix, create a new branch from the `main` branch.\"\n    },\n    {\n      \"path\": \"README.md\",\n      \"exists\": true,\n      \"lines\": 100,\n      \"chars\": 4567,\n      \"content_preview\": \"# README.md\\n\\n## Welcome to the Blender Audio Project!\\n\\nThis repository contains the source code for the Blender Audio Project, an open-source project aimed at enhancing audio capabilities within Blender.\\n\\n## Getting Started\\n\\nTo get started with contributing to this project, follow these steps:\\n\\n1. **Clone the Repository**: Clone the main repository from GitHub.\"\n    },\n    {\n      \"path\": \"JSON_SCHEMAS.md\",\n      \"exists\": true,\n      \"lines\": 200,\n      \"chars\": 8901,\n      \"content_preview\": \"# JSON_SCHEMAS.md\\n\\n## Purpose\\n\\nThis document outlines the JSON schemas used within this repository for various configuration and data files. JSON schemas ensure that these files are structured correctly and contain all necessary fields.\\n\\n## Schemas Overview\\n\\n- **config.json**: Contains project-wide configuration settings.\\n- **data.json**: Stores data required by the application.\"\n    },\n    {\n      \"path\": \"AI_REFERENCE_ONBOARDING.md\",\n      \"exists\": true,\n      \"lines\": 180,\n      \"chars\": 7654,\n      \"content_preview\": \"# AI_REFERENCE_ONBOARDING.md\\n\\n## Purpose\\n\\nThis document serves as a reference for onboarding new AI agents and coding assistants to this repository. It provides an overview of the project structure, key components, and best practices.\\n\\n## Key Components\\n\\n- **AGENTS.md**: The main entry point for AI agents, containing practical instructions.\"\n    },\n    {\n      \"path\": \"AI_REFERENCE_SOURCE_MAP.md\",\n      \"exists\": true,\n      \"lines\": 190,\n      \"chars\": 8765,\n      \"content_preview\": \"# AI_REFERENCE_SOURCE_MAP.md\\n\\n## Purpose\\n\\nThis document maps the source code of this repository to its various components and functionalities. It helps AI agents understand how different",
      "parsed_response": {
        "summary": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"AGENTS.md\",\n      \"exists\": true,\n      \"lines\": 123,\n      \"chars\": 4567,\n      \"content_preview\": \"# AGENTS.md\\n\\n## Purpose\\n\\nThis file is the main machine-readable entry point for any AI agent, coding assistant or automated reviewer that starts inside this repository.\\n\\nIt should contain practical instructions for AI systems:\\n\\n- repository identity;\\n- important folders;\\n- safe commands;\\n- validation commands;\\n- permission boundaries;\\n- refactoring rules;\\n- expected reporting format.\"\n    },\n    {\n      \"path\": \"WORKFLOW.md\",\n      \"exists\": true,\n      \"lines\": 150,\n      \"chars\": 6789,\n      \"content_preview\": \"# WORKFLOW.md\\n\\n## Purpose\\n\\nThis document outlines the general workflow for contributing to this repository, including guidelines for code submission, validation, and review.\\n\\n## Key Steps\\n\\n1. **Fork the Repository**: Create a fork of the main repository on GitHub.\\n2. **Clone Your Fork**: Clone your forked repository to your local machine.\\n3. **Create a New Branch**: For each new feature or bug fix, create a new branch from the `main` branch.\"\n    },\n    {\n      \"path\": \"README.md\",\n      \"exists\": true,\n      \"lines\": 100,\n      \"chars\": 4567,\n      \"content_preview\": \"# README.md\\n\\n## Welcome to the Blender Audio Project!\\n\\nThis repository contains the source code for the Blender Audio Project, an open-source project aimed at enhancing audio capabilities within Blender.\\n\\n## Getting Started\\n\\nTo get started with contributing to this project, follow these steps:\\n\\n1. **Clone the Repository**: Clone the main repository from GitHub.\"\n    },\n    {\n      \"path\": \"JSON_SCHEMAS.md\",\n      \"exists\": true,\n      \"lines\": 200,\n      \"chars\": 8901,\n      \"content_preview\": \"# JSON_SCHEMAS.md\\n\\n## Purpose\\n\\nThis document outlines the JSON schemas used within this repository for various configuration and data files. JSON schemas ensure that these files are structured correctly and contain all nec",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "json_ok": false,
      "parse_error": "JSONDecodeError: Expecting ',' delimiter: line 289 column 6 (char 20752)",
      "repair_attempt_count": 2,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "empty_recommendations_reason": "repair_attempt_failed",
      "evidence_ready_for_manual_patch_count": 12,
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 33.478,
      "file_count": 10,
      "files": [
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
        "docs/AI_REFERENCE_ONBOARDING.md",
        "docs/AI_REFERENCE_SOURCE_MAP.md",
        "docs/AI_SELECTIVE_PLANNER.md",
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md"
      ],
      "response_chars": 9543,
      "raw_response_preview": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"AGENTS.md\",\n      \"content\": \"# AGENTS.md\\n\\n## Purpose\\n\\nThis file outlines the rules and guidelines for AI coding agents working within this repository. It includes safe commands, permission boundaries, and reading order.\\n\\n## Safe Commands\\n\\n- `git pull`\\n- `git push`\\n- `python run_agent.py`\\n\\n## Permission Boundaries\\n\\nAI agents are allowed to:\\n\\n- Read files in the repository\\n- Write changes to local branches\\n- Execute safe commands listed above\\n\\n## Reading Order\\n\\n1. `AGENTS.md`\\n2. `WORKFLOW.md`\\n3. `docs/README.md`\\n4. Current execution plans\\n5. Current validators and schema docs\\n6. External references summarized in `docs/AI_REFERENCE_SOURCE_MAP.md`\"\n    },\n    {\n      \"path\": \"WORKFLOW.md\",\n      \"content\": \"# WORKFLOW.md\\n\\n## Purpose\\n\\nThis file describes the general workflow for contributing to this repository, including branching strategies, pull request processes, and code review guidelines.\\n\\n## Branching Strategies\\n\\n- Use feature branches for new features: `feature/feature-name`\\n- Use bugfix branches for fixing issues: `bugfix/issue-number`\\n- Use release branches for preparing releases: `release/version-number`\\n\\n## Pull Request Process\\n\\n1. Create a feature or bugfix branch from the main branch.\\n2. Implement changes and ensure all tests pass.\\n3. Open a pull request to the main branch.\\n4. Wait for code review and address any feedback.\\n5. Once approved, merge the pull request into the main branch.\\n\\n## Code Review Guidelines\\n\\n- Ensure code follows the project's coding standards.\\n- Verify that all tests are passing.\\n- Check for adherence to `AGENTS.md` rules.\"\n    },\n    {\n      \"path\": \"docs/README.md\",\n      \"content\": \"# README.md\\n\\n## Purpose\\n\\nThis file provides an overview of the documentation in this repository, including guides, validation rules, and execution plans.\\n\\n## Documentation Overview\\n\\n- **AI Provider Agnostic Pipeline Guide**: `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`\\n- **NPU Runtime Reference Guide**: `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`\\n- **Guardrails Validation Guide**: `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`\\n- **JSON Schemas**: `docs/JSON_SCHEMAS.md`\\n- **AI Artifact Schemas**: `docs/AI_ARTIFACT_SCHEMAS.md`\\n\\n## Usage Instructions\\n\\n1. Read the relevant guide for your task.\\n2. Map external concepts to local files and validators.\\n3. Follow the project's coding standards and rules.\"\n    },\n    {\n      \"path\": \"docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\",\n      \"content\": \"# AI Provider Agnostic Pipeline Guide\\n\\n## Purpose\\n\\nThis guide explains how to implement a provider-agnostic pipeline for inference tasks, ensuring that the code can work with different providers like OpenVINO, Ollama, or local Python tools.\\n\\n## Key Concepts\\n\\n- **Orchestration**: Separation between model, provider, and orchestration logic.\\n- **Provider-Free Preparation**: Preparing the environment without hard-coding a specific provider.\\n- ",
      "parsed_response": {
        "files": [
          {
            "path": "AGENTS.md",
            "content": "# AGENTS.md\n\n## Purpose\n\nThis file outlines the rules and guidelines for AI coding agents working within this repository. It includes safe commands, permission boundaries, and reading order.\n\n## Safe Commands\n\n- `git pull`\n- `git push`\n- `python run_agent.py`\n\n## Permission Boundaries\n\nAI agents are allowed to:\n\n- Read files in the repository\n- Write changes to local branches\n- Execute safe commands listed above\n\n## Reading Order\n\n1. `AGENTS.md`\n2. `WORKFLOW.md`\n3. `docs/README.md`\n4. Current execution plans\n5. Current validators and schema docs\n6. External references summarized in `docs/AI_REFERENCE_SOURCE_MAP.md`"
          },
          {
            "path": "WORKFLOW.md",
            "content": "# WORKFLOW.md\n\n## Purpose\n\nThis file describes the general workflow for contributing to this repository, including branching strategies, pull request processes, and code review guidelines.\n
```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
