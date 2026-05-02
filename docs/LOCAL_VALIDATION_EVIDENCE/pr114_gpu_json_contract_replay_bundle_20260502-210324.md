# Local Validation Evidence Bundle

- Generated at: `2026-05-02T21:03:24`
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
- `included_artifact_count`: `3`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/analysis/gpu_json_contract_replay_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Artifact manifest

- `output/analysis/gpu_json_contract_replay_20260502-195523.json` exists=`True` size=`23063` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `output/analysis/gpu_json_contract_replay_20260502-195523.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `638`
- SHA-256: `62fae4b5076a81ce8798422e102020ed46d7ff908badb236613c9307e160c4f5`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `24`
- Context echo detected: `0`
- JSON parse failures: `22`
- Schema mismatches: `2`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `json_parse_failure`: `22`
- `model_output_schema_mismatch`: `2`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `docs/LOCAL_AI_TASKS/gpu-json-contract-runner-integration.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2371`
- SHA-256: `7d5848ea67eaa571425df6d1a9268643b7d9d8fcf1b24728bcff2bfc1da54cff`
- Content included: `True`
- Content truncated: `False`

```text
# GPU JSON Contract Runner Integration

## Purpose

Plan and validation notes for integrating `Tools.ai.gpu_planner_json_contract.validate_model_response_contract()` into the real GPU planning runners.

Target runners:

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
```

## Current safe bridge

Before changing the long-running provider path, use:

```text
Tools/ai/replay_gpu_planner_json_contract.py
```

This replays already captured GPU planner raw responses through the contract helper.

It does not run providers and does not write source files.

## Command

```powershell
python .\Tools\ai\replay_gpu_planner_json_contract.py `
  --repo-root . `
  --gpu-report ".\output\ai_pipeline\project_complete_20260502-195523_parallel_gpu.json" `
  --output ".\output\analysis\gpu_json_contract_replay_20260502-195523.json" `
  --markdown-output ".\output\analysis\gpu_json_contract_replay_20260502-195523.md"
```

## Expected report fields

```text
replayed_round_count
contract_reason_counts
context_echo_detected_count
json_parse_failure_count
model_output_schema_mismatch_count
valid_recommendation_output_count
```

## Integration target

Once replay confirms useful classifications, update the runner parsing flow:

```text
model response
-> validate_model_response_contract(response, evidence_ready_for_manual_patch_count)
-> parsed response from contract result when valid
-> round diagnostics include contract fields
-> aggregate diagnostics use classified reasons
```

## New reason precedence

Prefer this ordering when no valid recommendations survive:

```text
context_echo_detected
json_parse_failure
model_output_schema_mismatch
recommendations_filtered_out
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

`repair_attempt_failed` should remain only as a legacy/compatibility signal when older reports are inspected.

## Guardrails

```text
no provider/model settings change in the runner integration PR
no automatic patch application
no source writes through patch runner
no Blender runtime execution
no SQLite/database writes
manual review required
```

## Bundle rule

Include only compact evidence:

```text
GPU JSON contract replay report
this integration note
small smoke/compile evidence
```

Do not include raw GPU output directly unless truncated by the bundle builder.

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
