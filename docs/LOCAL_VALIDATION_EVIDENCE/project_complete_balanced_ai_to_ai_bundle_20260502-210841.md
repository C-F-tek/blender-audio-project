# Local Validation Evidence Bundle

- Generated at: `2026-05-02T21:20:05`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `20`
- `patch_plan_summary_seen`: `True`

## Reports

### `output/validation/python_syntax_project_complete_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/npu_provider_environment_project_complete_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/gpu_planner_json_contract_smoke_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_project_complete_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `115`

### `output/ai_pipeline/project_complete_balanced_20260502-210841_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/project_complete_balanced_20260502-210841_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `build_agent_review_patch_plan.py`

### `output/analysis/gpu_json_contract_replay_balanced_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_balanced_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet`
- Passed: `True`
- Ollama: `{'used': False, 'model': None, 'error': '', 'text_preview': ''}`

### `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/ai_pipeline/repository_change_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/patch_specs/agent_review_patch_plan_project_complete_balanced_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`
- Patch plan summary count: `12`
- Fallback used: `True`
- Manual review required: `True`

### `output/validation/agent_review_patch_plan_smoke_project_complete_balanced_20260502-210841.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`
- Warnings: `['fallback_used is true; GPU planner produced no usable ready recommendation']`

## Patch plan summary

### `output/patch_specs/agent_review_patch_plan_project_complete_balanced_20260502-210841.json`

- Patch plan count: `12`
- Fallback used: `True`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### fallback_doc_code_001 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/config_model.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

#### fallback_doc_code_002 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/diagnostics.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

#### fallback_doc_code_003 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

#### fallback_doc_code_004 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

#### fallback_doc_code_005 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_SOURCE_MAP.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

#### fallback_doc_code_006 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_SOURCE_MAP.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

#### fallback_doc_code_007 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code-quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

#### fallback_doc_code_008 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code_quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

#### fallback_doc_code_009 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/ci.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

#### fallback_doc_doc_001 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

#### fallback_doc_doc_002 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/JSON_SCHEMAS.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

#### fallback_doc_doc_003 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/README.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.


## Artifact manifest

- `output/validation/python_syntax_project_complete_20260502-210841.json` exists=`True` size=`32226` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_provider_environment_project_complete_20260502-210841.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_20260502-210841.json` exists=`True` size=`3635` suffix=`.json` preview_chars=`1500`
- `output/analysis/code_interpreter_project_complete_20260502-210841.json` exists=`True` size=`1168294` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/project_complete_balanced_20260502-210841_orchestrator.json` exists=`True` size=`20674` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/project_complete_balanced_20260502-210841_parallel_gpu.json` exists=`True` size=`116642` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_balanced_20260502-210841.json` exists=`True` size=`19905` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_balanced_20260502-210841.json` exists=`True` size=`2644` suffix=`.json` preview_chars=`1500`
- `output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json` exists=`True` size=`190374` suffix=`.json` preview_chars=`1500`
- `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json` exists=`True` size=`7530` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/repository_change_proposals.json` exists=`True` size=`8219` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/agent_review_patch_plan_project_complete_balanced_20260502-210841.json` exists=`True` size=`61025` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_patch_plan_smoke_project_complete_balanced_20260502-210841.json` exists=`True` size=`1313` suffix=`.json` preview_chars=`1287`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-review-request.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `5012`
- SHA-256: `4820d57bccde654d2b88fd31d1932fb757dc5c93ed4abb7a1f00b4c66fc3384d`
- Content included: `True`
- Content truncated: `False`

```text
# Project Complete AI-to-AI Review Request

## Purpose

Canonical Markdown request for a project-only complete local AI run.

This file is the first task document to provide to the local AI workflow. The run must not start from ad-hoc chat instructions only.

## Core flow

```text
read this Markdown request
read the official local AI runbook
run the local project analysis tools
run the local GPU planner
run the local NPU checkpoint auditor when available
run the post-validation packet step
run the manual-review fallback plan step when needed
build a compact evidence bundle
validate the bundle
commit and push only the compact bundle and small notes
review results from GitHub evidence
```

## Required reading order

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md
docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md
docs/PROJECT_STATUS_POINT.md
docs/AGENT_REVIEW_CODE_PATCH_PLAN.md
docs/TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/build_agent_review_patch_plan.py
Tools/ai/build_github_evidence_bundle.py
Tools/validation/run_agent_review_patch_plan_smoke.py
Tools/validation/check_github_evidence_bundle.py
```

If instructions conflict, stop and report the conflict instead of continuing.

## Run type

```text
run_type: complete
scope: project-only
local_ai_lanes: enabled
```

A complete run means all applicable local tools and local AI lanes are active for the selected scope.

Enabled lanes:

```text
static code interpreter
validation tools
artifact and bundle tools
GPU planner
NPU checkpoint auditor when available
post-validation packet
manual-review fallback plan builder
bundle validation
```

## Project-only scope

Include:

```text
Tools/ai
Tools/validation
Tools/npu
Tools/workflow
Scripting/v61b
Scripting/shared
docs
```

Exclude as analysis targets:

```text
old script legacy/**
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/**
Scripting/v61b_backgood/**
renders/**
```

Local output reports may be used as inputs, but raw local output files are not the Git review artifact. The Git review artifact is the compact bundle under `docs/LOCAL_VALIDATION_EVIDENCE/`.

## Main request

Review the current project AI and tooling pipeline after PR #109 was merged.

Focus on:

```text
static analysis versus provider recommendation agreement
whether GPU planning produces actionable recommendations from ready evidence
whether NPU checkpoint auditing is useful and non-blocking
whether fallback manual-review plan generation is still needed
which one or two project-only targets should become the next small review PR
```

Produce advisory outputs and manual-review candidates only.

## AI improvement impressions

In addition to evidence-backed recommendations, provide a separate section named `AI improvement impressions`.

This section should contain operational impressions that emerged while reading the repository, running the local tools, comparing reports and observing provider behavior.

Each impression must be clearly marked as one of:

```text
evidence-backed
inferred from multiple signals
speculative but potentially useful
```

For each impression include:

```text
short title
why it may improve the project
evidence or signals that triggered it
risk if ignored
minimal next action
whether it should become a task, issue, doc update or future PR
```

Useful impression categories include:

```text
architecture simplification
pipeline reuse in other projects
tooling ergonomics
evidence quality
provider orchestration
GPU/NPU workload split
manual-review friction
bundle/audit readability
validator coverage
future refactor candidates
```

Do not present impressions as facts unless the evidence supports them. Do not propose automatic edits from impressions. Convert them into reviewable task candidates only.

## Required final artifact

```text
docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_<timestamp>.json
docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_<timestamp>.md
```

The bundle must include this Markdown request as an included artifact so the reviewer can see the exact task given to the local AI system.

## Recommendation format

Each useful recommendation should include:

```text
target file or module
reason from evidence
risk level
minimal review strategy
validation commands
stop conditions
static/provider agreement status
```

Prefer small project infrastructure or tooling targets over large visual legacy scripts.

## Stop conditions

Stop and report if:

```text
required evidence is missing and cannot be regenerated safely
the GPU planner is unavailable for a complete run
NPU auditing would block GPU planning instead of acting as support
any tool attempts automatic patching
raw local output files would become the committed review artifact
```

```

### `docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-procedure.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `11184`
- SHA-256: `ae4e096aa0a71906070f06b50af3567e8500f3b36f4a32c4cf1537e94288d07f`
- Content included: `True`
- Content truncated: `False`

```text
# Project Complete AI-to-AI Procedure

## Purpose

Canonical procedure for a project-only complete local AI run.

This procedure preserves the current repository workflow:

```text
Markdown request
-> local static analysis
-> GPU planner
-> NPU checkpoint auditor when available
-> post-validation AI packet
-> fallback manual-review patch-plan when needed
-> compact evidence bundle
-> bundle validation
-> commit/push
-> GitHub audit
```

Use this document together with:

```text
docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-review-request.md
docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md
```

## 0. Sync master and prepare the shell

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

"STAMP=$Stamp"
$env:PYTHONPATH
```

## 1. Read the official request and runbooks

```powershell
Get-Content .\AGENTS.md -TotalCount 220
Get-Content .\docs\LOCAL_AI_RUN_BOOTSTRAP.md -TotalCount 220
Get-Content .\docs\LOCAL_AI_TASKS\README.md -TotalCount 220
Get-Content .\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md -TotalCount 260
Get-Content .\docs\LOCAL_AI_TASKS\gpu-npu-parallel-evidence-runbook.md -TotalCount 320
```

The local AI run must use the Markdown request as the task input. Do not rely only on ad-hoc chat instructions.

## 2. Run NPU/provider preflight

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output ".\output\validation\npu_provider_environment_project_complete_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_project_complete_$Stamp.md"

Get-Content ".\output\validation\npu_provider_environment_project_complete_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, provider_execution_performed, patch_application_performed
```

## 3. Run project-only static gates

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_project_complete_$Stamp.json"

python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/npu `
  --input Tools/workflow `
  --input Scripting/v61b `
  --input Scripting/shared `
  --output ".\output\analysis\code_interpreter_project_complete_$Stamp.json" `
  --markdown-output ".\output\analysis\code_interpreter_project_complete_$Stamp.md"
```

Project-only exclusions:

```text
old script legacy/**
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/**
Scripting/v61b_backgood/**
renders/**
```

## 4. Run the official GPU/NPU AI-to-AI orchestrator

```powershell
python .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py `
  --repo-root . `
  --budget-minutes 30 `
  --max-rounds 24 `
  --files-per-round 10 `
  --max-context-files 240 `
  --max-chars-per-file 8000 `
  --max-new-tokens 4800 `
  --keep-alive 35m `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --refined-review .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review_v3.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agent_memory_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agnostic_tool_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_transient_request_context.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --report-file ".\output\analysis\code_interpreter_project_complete_$Stamp.json" `
  --context-root docs `
  --context-root Tools\ai `
  --context-root Tools\validation `
  --context-root Tools\workflow `
  --context-root Tools\npu `
  --context-root Scripting\v61b `
  --context-root Scripting\shared `
  --run-npu-auditor-provider `
  --npu-auditor-every-rounds 4 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 600 `
  --npu-max-context-chars 12000 `
  --npu-max-prompt-chars 1500 `
  --npu-max-new-tokens 512 `
  --npu-final-wait-seconds 120 `
  --checkpoint-dir ".\output\ai_pipeline\project_complete_${Stamp}_checkpoints" `
  --gpu-output ".\output\ai_pipeline\project_complete_${Stamp}_parallel_gpu.json" `
  --gpu-markdown-output ".\output\ai_pipeline\project_complete_${Stamp}_parallel_gpu.md" `
  --output ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.json" `
  --markdown-output ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.md"
```

## 5. Inspect the orchestrator summary

```powershell
$orch = Get-Content ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.json" -Raw | ConvertFrom-Json

$orch |
  Select-Object kind, passed, provider_execution_performed, patch_application_performed, elapsed_seconds, gpu_returncode, npu_audit_count, npu_audit_success_count

$orch.gpu_summary
$orch.decision
```

If the orchestrator fails, continue only far enough to bundle the failure evidence. Do not treat proposals as valid.

## 6. Run post-validation AI packet with the Markdown request included

```powershell
$GpuReport = $orch.gpu_output
$GpuReport

$ContextFiles = @(
  ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md",
  ".\docs\LOCAL_AI_TASKS\gpu-npu-parallel-evidence-runbook.md",
  ".\docs\LOCAL_AI_TASKS\improve-gpu-planner-nonempty-recommendations.md",
  ".\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py",
  ".\Tools\ai\run_agent_gpu_deep_planning_review.py",
  ".\Tools\ai\run_agent_gpu_deep_planning_supervised.py",
  ".\Tools\ai\build_agent_review_patch_plan.py",
  ".\output\analysis\code_interpreter_project_complete_$Stamp.md"
)

$ReportFiles = @(
  ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.json",
  $GpuReport,
  ".\output\analysis\code_interpreter_project_complete_$Stamp.json",
  ".\output\validation\npu_provider_environment_project_complete_$Stamp.json"
)

$params = @{
  Profile     = "core"
  ContextFile = $ContextFiles
  ReportFile  = $ReportFiles
}

& .\Tools\workflow\run_post_validation_ai_packet.ps1 @params
```

## 7. Run fallback manual-review patch-plan and smoke validation

```powershell
python .\Tools\ai\build_agent_review_patch_plan.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.json" `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output ".\output\patch_specs\agent_review_patch_plan_project_complete_$Stamp.json" `
  --markdown-output ".\output\patch_specs\agent_review_patch_plan_project_complete_$Stamp.md"

python .\Tools\validation\run_agent_review_patch_plan_smoke.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.json" `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output ".\output\validation\agent_review_patch_plan_smoke_project_complete_$Stamp.json" `
  --markdown-output ".\output\validation\agent_review_patch_plan_smoke_project_complete_$Stamp.md"
```

## 8. Build the compact GitHub evidence bundle

```powershell
$Reports = @(
  ".\output\validation\python_syntax_project_complete_$Stamp.json",
  ".\output\validation\npu_provider_environment_project_complete_$Stamp.json",
  ".\output\analysis\code_interpreter_project_complete_$Stamp.json",
  ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.json",
  ".\output\ai_pipeline\project_complete_${Stamp}_parallel_gpu.json",
  ".\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json",
  ".\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json",
  ".\output\ai_pipeline\repository_change_proposals.json",
  ".\output\patch_specs\agent_review_patch_plan_project_complete_$Stamp.json",
  ".\output\validation\agent_review_patch_plan_smoke_project_complete_$Stamp.json"
) | Where-Object { Test-Path $_ }

"REPORTS:"
$Reports

python -m Tools.ai.build_github_evidence_bundle `
  --repo-root . `
  --basename project_complete_ai_to_ai_bundle_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md" `
  --artifact ".\output\analysis\code_interpreter_project_complete_$Stamp.md" `
  --artifact ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.md" `
  --artifact ".\output\ai_pipeline\project_complete_${Stamp}_parallel_gpu.md" `
  --artifact ".\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.md" `
  --artifact ".\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.md" `
  --artifact ".\output\ai_pipeline\repository_change_proposals.md" `
  --artifact ".\output\patch_specs\agent_review_patch_plan_project_complete_$Stamp.md" `
  --max-included-artifact-chars 12000 `
  --max-included-artifacts 80
```

The bundle must include `project-complete-ai-to-ai-review-request.md`, so the task given to the local AI is visible in GitHub review.

## 9. Validate the compact bundle

```powershell
python -m Tools.validation.check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_ai_to_ai_bundle_$Stamp.json" `
  --output ".\output\validation\project_complete_ai_to_ai_bundle_${Stamp}_validation.json"

Get-Content ".\output\validation\project_complete_ai_to_ai_bundle_${Stamp}_validation.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```

## 10. Commit and push only compact evidence

```powershell
git status --short
git diff --check

git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_ai_to_ai_bundle_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_ai_to_ai_bundle_$Stamp.md"

git diff --cached --name-only
git commit -m "test(ai): add project complete AI-to-AI evidence bundle"
git push origin master

git status --short
git log --oneline -5
```

Do not commit raw `output/**` files.

## Current successful reference run

A successful project complete AI-to-AI run was pushed in:

```text
e133698 test(ai): add project complete AI-to-AI evidence bundle
```

Local state reported after push:

```text
git status --short: clean
HEAD: e133698
origin/master: e133698
```

Observed from the committed evidence bundle:

```text
provider_execution_seen=true
patch_plan_summary_seen=true
artifact_manifest_built=true
included_artifacts_built=true
included_artifact_count=13
python_syntax passed=true
npu_provider_environment passed=true
code_interpreter_report passed=true
orchestrator passed=true
GPU provider execution performed=true
NPU audits succeeded=5
fallback patch plan count=12
patch application performed=false
source writes performed=false
manual review required=true
```

## Guardrails

```text
no automatic patch application
no source writes through patch runner
no Blender runtime execution
no raw output/** commit
no full analysis JSON commit
no SQLite/database commit
no NPU advisory promotion
no OpenVINO GPU primary advisory lane
review from committed GitHub evidence only
```

```

### `docs/LOCAL_AI_TASKS/post-pr114-next-task-handoff.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `8179`
- SHA-256: `7b87e2bcdebc4ff70973979d527a338e513ec9cdd1f02b4482ae46432175d813`
- Content included: `True`
- Content truncated: `False`

```text
# Post-PR114 Next Task Handoff

## Purpose

Operational handoff for the next AI/tooling tasks after PR #109, PR #111, PR #112, PR #113 and PR #114.

This document exists to prevent the next task from restarting architecture analysis from scratch.

Use it as the first local/context document before touching the next GPU planner integration PR.

## Current merged baseline

```text
master includes PR #109: manual-review code patch plan lane and GitHub evidence bundle refactor
master includes PR #111: GPU repair-failure recommendation report
master includes PR #112: GPU planner JSON contract helper and smoke
master includes PR #113: GPU/NPU sync analyzer, balanced profile, bundle retention policy
master includes PR #114: GPU planner JSON contract replay on historical outputs
```

Latest relevant merge:

```text
28c600a6fecb2ab56be6b9951a9de72adf2ffbab
Merge PR #114: feat(ai): replay GPU planner JSON contract on real outputs
```

## Critical evidence from the reference complete run

Reference run:

```text
project_complete_20260502-195523
```

Original GPU/NPU behavior:

```text
GPU round count: 24
NPU audit count: 5
NPU audit success count: 5
GPU recommendation count: 0
GPU raw recommendation candidate count: 0
GPU filtered recommendation count: 0
legacy empty reason: repair_attempt_failed
evidence ready for manual patch count: 12
fallback patch plan count: 12
```

PR #114 replay evidence refined the failure diagnosis:

```text
replayed_round_count=24
json_parse_failure=22
model_output_schema_mismatch=2
context_echo_detected=0
valid_recommendation_output=0
```

Interpretation:

```text
The historical GPU output mostly failed as malformed/truncated JSON, with two rounds producing parseable but schema-invalid output. The old repair_attempt_failed aggregate was too coarse.
```

## Current helper/tool inventory relevant to next work

```text
Tools/ai/gpu_planner_json_contract.py
Tools/validation/run_gpu_planner_json_contract_smoke.py
Tools/ai/replay_gpu_planner_json_contract.py
Tools/ai/build_gpu_repair_failure_recommendation.py
Tools/ai/analyze_gpu_npu_run_sync.py
Tools/ai/build_agent_review_patch_plan.py
Tools/ai/build_github_evidence_bundle.py
Tools/validation/check_github_evidence_bundle.py
```

Important docs:

```text
docs/LOCAL_AI_TASKS/gpu-planner-json-contract-hardening.md
docs/LOCAL_AI_TASKS/gpu-json-contract-runner-integration.md
docs/LOCAL_AI_TASKS/gpu-npu-balanced-run-profile.md
docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap.md
docs/LOCAL_VALIDATION_EVIDENCE/README.md
```

## Next recommended PR

Title:

```text
feat(ai): wire GPU planner JSON contract into runner diagnostics
```

Primary target:

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
```

Secondary target only if needed:

```text
Tools/ai/run_agent_gpu_deep_planning_supervised.py
```

Reason:

```text
The supervised runner currently depends on the base GPU planning behavior. Start with the base runner and only touch supervised wiring if the code path requires explicit propagation.
```

## Required behavior change

Current legacy path:

```text
model response
-> parse_model_json_with_diagnostics()
-> recommendation_diagnostics_for_round()
-> aggregate_recommendation_diagnostics()
-> empty_recommendations_reason often collapses to repair_attempt_failed
```

Target path:

```text
model response
-> validate_model_response_contract(response, evidence_ready_for_manual_patch_count)
-> parsed response from contract result when schema is usable
-> round diagnostics include contract_* fields
-> aggregate diagnostics prefers explicit contract reasons
```

## Required output fields to add or preserve

Add where practical:

```text
contract_json_ok
contract_schema_ok
contract_context_echo_detected
contract_empty_recommendations_reason
contract_parse_error
contract_schema_errors
contract_raw_response_sha256
contract_top_level_keys
contract_valid_recommendation_count
contract_invalid_recommendation_count
```

Preserve existing compatibility fields:

```text
json_ok
parse_error
repair_attempt_count
raw_recommendation_candidate_count
filtered_recommendation_count
recommendation_count
empty_recommendations_reason
evidence_ready_for_manual_patch_count
recommended_next_layer
```

## Reason precedence for aggregate empty output

Prefer this order when no valid recommendations survive:

```text
context_echo_detected
json_parse_failure
model_output_schema_mismatch
recommendations_filtered_out
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

Use `repair_attempt_failed` only as legacy compatibility when reading older reports, not as the primary new classifier.

## Prompt hardening is a separate PR

Do not mix runner diagnostic wiring with prompt rewriting.

The next PR should focus on diagnostics/classification only.

A later PR can change prompt shape, for example:

```text
JSON-only footer
explicit no files/content_preview top-level output
compact retry lane
schema-only response example
```

## GPU/NPU balance baseline

PR #113 established the measured skew:

```text
gpu_round_count=24
npu_audit_count=5
npu_audit_success_count=5
npu_audit_round_coverage=0.208
avg_gpu_round_seconds=29.425
avg_npu_audit_seconds=124.8
npu_to_gpu_avg_duration_ratio=4.241
```

Balanced profile candidate for future complete run:

```text
--max-rounds 20
--files-per-round 8
--max-context-files 220
--max-chars-per-file 6000
--max-new-tokens 3600
--npu-auditor-every-rounds 3
--npu-auditor-timeout-seconds 420
--npu-max-context-chars 8000
--npu-max-prompt-chars 1200
--npu-max-new-tokens 384
--npu-final-wait-seconds 180
```

Do not change provider/model settings in the diagnostic wiring PR.

## Bundle retention law

Follow:

```text
docs/LOCAL_VALIDATION_EVIDENCE/README.md
```

Main rule:

```text
commit the smallest bundle that proves the decision
```

For the next PR, commit only one final compact evidence bundle unless an after-fix bundle is required.

## Local validation sequence for the next PR

Minimum local validation after wiring:

```powershell
python -m py_compile .\Tools\ai\run_agent_gpu_deep_planning_review.py .\Tools\ai\gpu_planner_json_contract.py
python -m py_compile .\Tools\ai\replay_gpu_planner_json_contract.py
python .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  --repo-root . `
  --output .\output\validation\gpu_planner_json_contract_smoke_<STAMP>.json `
  --markdown-output .\output\validation\gpu_planner_json_contract_smoke_<STAMP>.md
python .\Tools\ai\replay_gpu_planner_json_contract.py `
  --repo-root . `
  --gpu-report .\output\ai_pipeline\project_complete_20260502-195523_parallel_gpu.json `
  --output .\output\analysis\gpu_json_contract_replay_after_wiring_<STAMP>.json `
  --markdown-output .\output\analysis\gpu_json_contract_replay_after_wiring_<STAMP>.md
```

If a provider run is needed, use the complete-run procedure only after the wiring PR merges.

## Evidence bundle for the next PR

Recommended compact bundle inputs:

```text
output/validation/gpu_planner_json_contract_smoke_<STAMP>.json
output/analysis/gpu_json_contract_replay_after_wiring_<STAMP>.json
docs/LOCAL_AI_TASKS/post-pr114-next-task-handoff.md
docs/LOCAL_AI_TASKS/gpu-json-contract-runner-integration.md
```

Do not include raw `output/**` files directly outside the bundle.

## Stop conditions

Stop if:

```text
runner wiring requires a large rewrite of run_agent_gpu_deep_planning_review.py
contract helper changes break the existing smoke
supervised runner requires unclear behavior changes
bundle exceeds retention policy limits
any step suggests automatic patch application
any step suggests provider/model setting changes in this diagnostic PR
```

## Next tasks after runner diagnostic wiring

Recommended order:

```text
1. Prompt hardening: JSON-only footer and no context echo output
2. Compact prompt retry lane for failed full-context GPU rounds
3. Recommendation schema validator integration into merge/filter logic
4. Provider agreement matrix
5. AI improvement impressions extractor
6. Issue/task candidate pack
7. Reusable project-agnostic AI pipeline profiles
8. Complete-run manifest
9. Bundle quality score
10. Evidence bundle retention inventory report-only tool
```

```

### `docs/LOCAL_AI_TASKS/gpu-npu-balanced-run-profile.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3594`
- SHA-256: `f50b4a7456e6d48a7a3512b79c3cf1ad0664dfbc01f187119d4fc57ed9f16247`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Balanced Run Profile

## Purpose

Balanced profile proposal for complete local AI-to-AI runs when the GPU planner advances much faster than the NPU checkpoint auditor.

The goal is not perfect lockstep. The goal is useful NPU checkpoint coverage without blocking GPU progress or leaving NPU audits too stale.

## Reference run observation

Reference run:

```text
project_complete_20260502-195523
```

Observed behavior:

```text
GPU planner completed 24 rounds
NPU checkpoint auditor completed 5 audits
NPU audits succeeded
GPU output still ended with repair_attempt_failed
```

Interpretation:

```text
NPU is useful as a sampled checkpoint auditor, not as a per-round synchronous reviewer.
```

## Baseline complete-run parameters

Previous project-complete run used:

```text
--budget-minutes 30
--max-rounds 24
--files-per-round 10
--max-context-files 240
--max-chars-per-file 8000
--max-new-tokens 4800
--npu-auditor-every-rounds 4
--max-concurrent-npu-audits 1
--npu-auditor-timeout-seconds 600
--npu-max-context-chars 12000
--npu-max-prompt-chars 1500
--npu-max-new-tokens 512
--npu-final-wait-seconds 120
```

## Balanced profile candidate

Use this profile for the next comparative complete run after JSON-contract integration is available:

```text
--budget-minutes 30
--max-rounds 20
--files-per-round 8
--max-context-files 220
--max-chars-per-file 6000
--max-new-tokens 3600
--npu-auditor-every-rounds 3
--max-concurrent-npu-audits 1
--npu-auditor-timeout-seconds 420
--npu-max-context-chars 8000
--npu-max-prompt-chars 1200
--npu-max-new-tokens 384
--npu-final-wait-seconds 180
```

## Rationale

GPU-side changes:

```text
slightly smaller file batches
slightly smaller per-file context
lower max-new-tokens than 4800
fewer max rounds
```

Expected effect:

```text
less prompt echo pressure
less malformed long JSON
more compact GPU responses
less runaway round count
```

NPU-side changes:

```text
smaller context budget
smaller prompt budget
smaller decode budget
shorter per-audit timeout
longer final wait
```

Expected effect:

```text
faster NPU checkpoint completion
less chance that final NPU audits are still draining after GPU completion
better end-of-run audit inclusion
```

Cadence:

```text
npu-auditor-every-rounds 3
```

Expected effect:

```text
more frequent checkpoint coverage than every 4 rounds, while still avoiding per-round lockstep.
```

## Guardrails

```text
NPU remains non-blocking
NPU remains checkpoint/audit/support lane
NPU is not promoted to primary advisory
OpenVINO GPU is not used as primary lane
no provider/model setting changes first
no patch auto-apply
no source writes through patch runner
no Blender runtime execution
raw output/** remains local only
compact bundle remains required
```

## Required analysis tool

Use:

```powershell
python .\Tools\ai\analyze_gpu_npu_run_sync.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_<STAMP>_orchestrator.json" `
  --output ".\output\analysis\gpu_npu_run_sync_<STAMP>.json" `
  --markdown-output ".\output\analysis\gpu_npu_run_sync_<STAMP>.md"
```

The sync analysis report must be included in the evidence bundle for any future complete run that changes GPU/NPU cadence parameters.

## Success criteria

A balanced run is better if:

```text
GPU JSON contract failures decrease
context_echo_detected is separated from raw parse failure
NPU audit success remains true
NPU audit coverage improves or remains useful
final bundle includes NPU audit evidence and sync analysis
fallback patch-plan remains available when GPU recommendations are empty
```

```

### `docs/LOCAL_VALIDATION_EVIDENCE/README.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `4338`
- SHA-256: `702b263e403a2d70fd23034afca1355544a70b3a59916e72ff3701796cad7b7d`
- Content included: `True`
- Content truncated: `False`

```text
# Local Validation Evidence Bundle Policy

## Purpose

This directory stores compact Git-trackable validation evidence for manual review.

It must not become a raw output archive.

The repository source of truth is:

```text
raw local run outputs -> output/** only, ignored/local
compact review evidence -> docs/LOCAL_VALIDATION_EVIDENCE/
GitHub audit -> from committed compact bundles only
```

## Bundle law

Use this rule for every run:

```text
commit the smallest bundle that proves the decision
```

Do not commit every generated intermediate artifact.

Do not commit raw provider output directories.

Do not commit full analysis JSON unless it is a compact bounded evidence bundle.

## Allowed committed files

Allowed here:

```text
small compact bundle JSON
small compact bundle Markdown
selected golden evidence files that are intentionally reused across many runs
README/policy files
```

Typical accepted names:

```text
pr<NUMBER>_<topic>_bundle_<timestamp>.json
pr<NUMBER>_<topic>_bundle_<timestamp>.md
project_complete_ai_to_ai_bundle_<timestamp>.json
project_complete_ai_to_ai_bundle_<timestamp>.md
full_context_golden_selected_chunks_evidence.json
```

## Forbidden committed files

Do not commit:

```text
raw output/** directories
full provider transcripts unless bounded/truncated by the bundle builder
full analysis JSON dumps copied by hand
checkpoint directories
raw NPU audit context dumps
raw GPU planner responses
SQLite/database files
render outputs
large binary artifacts
```

## Size guidance

Soft limits:

```text
single bundle JSON: prefer under 250 KB
single bundle Markdown: prefer under 250 KB
single PR evidence addition: prefer under 1 MB total
included_artifact_count: prefer <= 10 for normal PRs
included_artifact_count: prefer <= 20 for complete-run PRs
max included chars per artifact: prefer <= 12000
```

If a bundle exceeds these limits, reduce included artifacts or include summaries instead of raw content.

## Retention guidance

Keep:

```text
one final evidence bundle per PR
one final evidence bundle per complete run
one after-fix bundle when an earlier bundle had a validation defect
stable golden evidence used by many tools
```

Avoid keeping:

```text
multiple failed bundles for the same PR
superseded pre-fix bundles when an after-fix bundle exists
large duplicate bundles that prove the same state
```

Current non-destructive policy:

```text
new work should avoid adding redundant bundles
existing bundles are not deleted automatically
cleanup/removal requires explicit human approval
```

## Bundle replacement rule

When a validation defect is found in a bundle:

```text
1. create an after-fix bundle
2. make the after-fix bundle the reviewed artifact
3. reference the superseded bundle only as historical context
4. do not add more bundles unless the reviewed evidence changes materially
```

For example:

```text
pr113_gpu_npu_sync_bundle_*.json        -> initial bundle
pr113_gpu_npu_sync_bundle_after_fix_*.json -> reviewed bundle after analyzer fix
```

The after-fix bundle is the authoritative one for review.

## Required metadata in future bundles

Future bundle builders or bundle quality checks should prefer including:

```text
run_id or PR number
source commit SHA
branch name
request Markdown path, when applicable
procedure Markdown path, when applicable
primary reports included
explicit guardrail flags
included_artifact_count
budget/truncation status
recommended_next_layer
whether this bundle supersedes another bundle
```

## Review rule

Reviewers should reject evidence if:

```text
raw output/** was committed directly
bundle does not include the task/request when the run was AI-to-AI
bundle is too large because it includes raw transcripts instead of summaries
bundle lacks guardrail flags
bundle hides which earlier bundle it supersedes
```

## Future cleanup tool candidate

A future report-only tool may inventory this directory and propose cleanup candidates:

```text
Tools/ai/analyze_evidence_bundle_retention.py
```

It should only report candidates. It must not delete files automatically.

Potential outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_retention_inventory_<timestamp>.json
docs/LOCAL_VALIDATION_EVIDENCE/evidence_bundle_retention_inventory_<timestamp>.md
```

Deletion or archival remains explicit/manual only.

```

### `output/analysis/code_interpreter_project_complete_20260502-210841.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6915`
- SHA-256: `1c88231195266d7617a8b34ab821b4cbb6a5d66bbb2bed4f42e6e2b0e5d76caf`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `231`
- Parsed files: `231`
- Total lines: `61323`
- Total functions: `2232`
- Total classes: `91`
- Risk signals: `43`
- TODO/FIXME markers: `21`
- Recommendation count: `115`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Scripting/v61b/animation.py` — `1079` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `714` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `628` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/workflow/workflow_debug.py` — `607` lines, risk `medium`
- `Tools/ai/build_repository_change_proposals.py` — `582` lines, risk `medium`
- `Tools/ai/build_ai_context_pack.py` — `575` lines, risk `medium`
- `Tools/ai/run_pipeline_dry_run_matrix.py` — `573` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `562` lines, risk `medium`
- `Scripting/v61b/atmosphere_setup.py` — `554` lines, risk `medium`
- `Tools/ai/suggest_repository_updates.py` — `551` lines, risk `medium`

## Recommendations

- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected
- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module
- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected
- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_011` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected
- `code_static_012` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_013` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_014` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected
- `code_static_015` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_017` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected
- `code_static_018` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_019` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected
- `code_static_020` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_021` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_022` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: complex functions detected
- `code_static_023` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_024` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_025` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_026` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_027` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_028` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_029` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_030` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_031` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_032` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected
- `code_static_033` `Tools/ai/build_patch_specs_from_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_034` `Tools/ai/build_repository_change_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_035` `Tools/ai/build_selective_execution_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_036` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_038` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_039` `Tools/ai/gpu_planner_json_contract.py` risk `medium`: complex functions detected
- `code_static_040` `Tools/ai/model_json.py` risk `medium`: complex functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/ai_pipeline/project_complete_balanced_20260502-210841_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1168`
- SHA-256: `95ed05bacaf8abdda737a0c2b8a804f0f7b2def733e178b4e786ef0f922457c1`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `524.16`
- `npu_audit_count`: `5`
- `npu_audit_success_count`: `5`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `repair_attempt_failed`
- `gpu_evidence_ready_for_manual_patch_count`: `12`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `5`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `True`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: `repair_attempt_failed`
- `manual_review_required`: `True`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `3` status=`finished` class=`usable_audit_text` success=`True`
- round `6` status=`finished` class=`usable_audit_text` success=`True`
- round `9` status=`finished` class=`usable_audit_text` success=`True`
- round `12` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/project_complete_balanced_20260502-210841_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `881`
- SHA-256: `cc8d5c2ec652b78f035e20b626ecfcd71350a35aa0c4cb82cdf7fc3a71faa459`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `460.77`
- Round count: `20`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- JSON parse error count: `17`
- Empty recommendations reason: `repair_attempt_failed`
- Evidence ready for manual patch count: `12`

## Decision

- `ready_for_patch_plan`: `False`
- `ready_count`: `0`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `True`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `manual_review_required`: `True`

## Recommendations


```

### `output/analysis/gpu_json_contract_replay_balanced_20260502-210841.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `670`
- SHA-256: `743e3bf3ce28b943d814d4deacef80c37388b6f441935f2d904f6e35d056943a`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `20`
- Context echo detected: `1`
- JSON parse failures: `18`
- Schema mismatches: `1`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `context_echo_detected`: `1`
- `json_parse_failure`: `18`
- `model_output_schema_mismatch`: `1`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_balanced_20260502-210841.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1587`
- SHA-256: `2172766b32bc2a0de3780ee9bc411b05d8fa9181d8fd103689ffc58353d7ae86`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `20`
- `npu_audit_count`: `5`
- `npu_audit_success_count`: `5`
- `npu_audit_round_coverage`: `0.25`
- `avg_gpu_round_seconds`: `26.208`
- `p50_gpu_round_seconds`: `26.208`
- `p90_gpu_round_seconds`: `26.208`
- `avg_npu_audit_seconds`: `101.6`
- `p50_npu_audit_seconds`: `102.0`
- `p90_npu_audit_seconds`: `104.0`
- `npu_to_gpu_avg_duration_ratio`: `3.877`
- `gpu_elapsed_seconds`: `524.16`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_summary_or_elapsed_estimate`

## Suggested balanced profile

- `npu_auditor_every_rounds`: `4`
- `max_concurrent_npu_audits`: `1`
- `npu_auditor_timeout_seconds`: `420`
- `npu_max_context_chars`: `8000`
- `npu_max_prompt_chars`: `1200`
- `npu_max_new_tokens`: `384`
- `npu_final_wait_seconds`: `180`
- `gpu_max_new_tokens`: `3600`
- `gpu_files_per_round`: `8`
- `gpu_max_chars_per_file`: `6000`

## Reasoning

- NPU audit coverage is low compared with GPU round count; keep checkpoint auditing sampled, not per-round.
- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.
- NPU audits are usable; tune cadence rather than disabling the lane.
- GPU JSON contract hardening should be tested before increasing GPU token budget further.


```

### `output/patch_specs/agent_review_patch_plan_project_complete_balanced_20260502-210841.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7039`
- SHA-256: `0b8d630de857a586ce99ab42bf36efd8101ca1f9b5f71b1f5c8e47630e9a35b1`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Patch Plan

- Passed: `True`
- Apply mode: `report_only_manual_review_patch_plan`
- Provider execution performed: `False`
- Patch application performed: `False`
- Patch plan count: `12`
- Fallback used: `True`
- Manual review required: `True`

## Inputs

- `orchestrator`: `output/ai_pipeline/project_complete_balanced_20260502-210841_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/project_complete_balanced_20260502-210841_parallel_gpu.json`
- `orchestrator_kind`: `agent_gpu_npu_parallel_orchestrator`
- `evidence_kind`: `agent_review_evidence_sufficiency`
- `gpu_kind`: `agent_gpu_deep_planning_supervised`

## Patch plans

### fallback_doc_code_001 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/config_model.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

### fallback_doc_code_002 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/diagnostics.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

### fallback_doc_code_003 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

### fallback_doc_code_004 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

### fallback_doc_code_005 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

### fallback_doc_code_006 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

### fallback_doc_code_007 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code-quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

### fallback_doc_code_008 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code_quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

### fallback_doc_code_009 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/ci.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

### fallback_doc_doc_001 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

### fallback_doc_doc_002 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/JSON_SCHEMAS.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

### fallback_doc_doc_003 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['Tools/validation/README.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

## Guardrail

This artifact is a plan only. It contains no replacements and must not be treated as an apply queue.

```

### `output/ai_packets/gpu_planner_nonempty_recommendations_advisory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3973`
- SHA-256: `df251fad3c39f4fa7f0e4950bf17aa3bc643465640a98a87aca0b997e9804110`
- Content included: `True`
- Content truncated: `False`

```text
# Post-Validation AI Work Packet

- Generated at: `2026-05-01T20:50:40`
- Repo: `C:\Users\carmi\blender\blender-audio-project`
- Profile: `core`
- Ollama used: `False`
- Packet manifest: `C:\Users\carmi\blender\blender-audio-project\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json`

## Advisory context routing

- Enforced: `True`
- Provider execution performed: `False`
- Advisory lanes: `ollama`
- Excluded advisory lanes: `npu`

## Deterministic suggestions

### P1 — Fix failing validation reports before new runtime work

- Area: `validation`
- Details: C:\Users\carmi\blender\blender-audio-project\output\validation\ai_workload_report_quality.json: ['npu: alphabetic character ratio is too low', 'npu: word count is too low', 'npu: report appears numeric/hex-like rather than natural language']

### P2 — Review active execution plans before opening the next milestone

- Area: `execution_plans`
- Details: docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md; docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md; docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md; docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_ai_pipeline_report_contracts.md; docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_output_policy_provider_preflight.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md; docs/EXECUTION_PLANS/active/2026-04-30_runtime_safe_provider_report_adoption.md; docs/EXECUTION_PLANS/active/2026-04-30_validator_report_consistency_review.md

### P2 — Prefer additive observability before provider or Blender runtime changes

- Area: `agnostic_core`
- Details: Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.

## Inputs

### Trusted context files
- `AGENTS.md`
- `WORKFLOW.md`
- `docs/AI_DOCS_ENTRYPOINT.md`
- `docs/PROJECT_STATUS_POINT.md`
- `docs/TECH_DEBT_TRACKER.md`
- `docs/REFACTORING_AND_REUSE_PLAN.md`
- `docs/JSON_SCHEMAS.md`
- `docs/AI_ARTIFACT_SCHEMAS.md`
- `Tools/npu/pipeline/README.md`
- `Tools/validation/README.md`
- `./docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md`
- `./Tools/ai/run_agent_gpu_deep_planning_review.py`
- `./Tools/ai/run_agent_gpu_deep_planning_supervised.py`
- `./Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`
- `./Tools/ai/build_agent_review_patch_plan.py`

### Report files
- `output/validation/python_syntax.json`
- `output/validation/ai_pipeline_modules.json`
- `output/validation/npu_pipeline_modules.json`
- `output/validation/npu_pipeline_helper_tests.json`
- `output/validation/npu_pipeline_docs.json`
- `output/validation/provider_result_parsing.json`
- `output/validation/provider_result_report.json`
- `output/validation/ai_workload_report_quality.json`
- `output/validation/ai_workload_quality_lane_routing.json`
- `output/validation/npu_decode_quality_remediation.json`
- `output/validation/npu_decode_smoke_diagnostic.json`
- `output/validation/npu_runtime_output_manifest.json`
- `output/validation/local_ai_resource_lanes.json`
- `output/validation/local_provider_probe.json`
- `output/validation/execution_plan_status.json`
- `output/validation/validation_report_contract.json`
- `output/validation/docs_links.json`
- `./output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json`
- `output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.json`

## Guardrails

- Advisory only: do not auto-apply edits from this packet.
- Output/input paths are configurable; defaults are not part of the architecture boundary.
- Validate locally before committing generated indexes.
- Keep provider execution changes in a separate explicitly scoped milestone.

```

### `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3476`
- SHA-256: `c13cf9413bd6e464df8b12b81138ae78a1dec8b8a06d76f8b31c5f6215410c9f`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-01T20:50:40`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-AI-WORKLOAD-REPORT-QUALITY-GATE — Gate AI workload reports before using them as advisory context

- Priority: `P1`
- Area: `local_ai_workloads`
- Change type: `workload_quality_gate`
- Apply mode: `manual_review_only`
- Rationale: AI workload report quality found usable lanes: ollama; unusable lanes: npu. Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed.

### Evidence summary

```json
{
  "workload_quality_decision": {
    "quality_report_present": true,
    "usable_lanes": [
      "ollama"
    ],
    "unusable_lanes": [
      "npu"
    ],
    "ollama_gpu_primary_advisory_allowed": true,
    "npu_excluded_from_primary_advisory": true,
    "routing_policy": "usable_text_lanes_only_for_advisory_context"
  }
}
```

### Target files
- `Tools/validation/check_ai_workload_report_quality.py`
- `Tools/npu/run_npu_review.py`
- `Tools/ai/suggest_repository_updates.py`
- `Tools/ai/build_repository_change_proposals.py`
- `Tools/validation/README.md`
- `docs/JSON_SCHEMAS.md`

### Patch sketch
- Keep Ollama/GPU workload reports as primary advisory context when classified usable.
- Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.
- Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.
- Add report metadata that distinguishes availability, execution and output usability.

### Suggestion outputs
- `python_code` `Tools/validation/check_ai_workload_report_quality.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/npu/run_npu_review.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/build_repository_change_proposals.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change would execute providers implicitly or by default.
- Any change would hide a failing/unusable AI workload report instead of reporting it.
- Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `35905`
- SHA-256: `a2216b89a69fc267b8015cfcbf775591b4c8b05abd127aef322936947f80683c`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_review_evidence_sufficiency",
  "generated_at": "2026-05-01T17:46:48",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_evidence_sufficiency",
  "inputs": {
    "refined_review": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json",
    "refined_proposals": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_proposals_v3.json",
    "refined_proposal_count": 2,
    "context_reports": [
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agent_memory_inventory.json",
        "exists": true,
        "kind": "agent_memory_inventory",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agnostic_tool_inventory.json",
        "exists": true,
        "kind": "agent_agnostic_tool_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "tool_count": 166,
          "category_counts": {
            "validator": 50,
            "provider_probe_or_adapter": 41,
            "orchestrator_pipeline": 30,
            "support_tool": 28,
            "agent_context_builder": 6,
            "proposal_or_review_builder": 5,
            "git_helper": 3,
            "review_helper": 3
          },
          "owner_lane_counts": {
            "npu_explicit_provider_tool": 65,
            "cpu_validation": 29,
            "gpu_cuda_explicit_provider_tool": 27,
            "cpu_support": 22,
            "cpu_orchestration": 18,
            "cpu_context_builder": 3,
            "cpu_proposal_builder": 2
          },
          "consumed_lane_counts": {
            "cpu": 166,
            "npu": 123,
            "gpu_cuda": 89
          },
          "apply_mode_counts": {
            "not_declared": 121,
            "manual_review_only": 20,
            "report_only": 16,
            "explicit_git_operation": 9
          },
          "provider_execution_default_counts": {
            "none_or_reported": 151,
            "explicit_only": 15
          }
        }
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_transient_request_context.json",
        "exists": true,
        "kind": "agent_transient_request_context",
        "passed": true,
        "error": "",
        "summary": {}
      }
    ]
  },
  "areas": {
    "doc_code": {
      "area": "doc_code",
      "item_count": 9,
      "ready_for_manual_patch_count": 9,
      "needs_more_context_count": 0,
      "items": [
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/config_model.py",
          "candidate_references": [
            "Scripting/shared/config_model.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/config_model.py",
                "Scripting/shared/config_model.py"
              ],
              "snippet": " still needing staged decomposition. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do"
            },
            {
              "path": "Scripting/shared/config_model.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/diagnostics.py",
          "candidate_references": [
            "Scripting/shared/diagnostics.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/diagnostics.py",
                "Scripting/shared/diagnostics.py"
              ],
              "snippet": "on. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do not assume every status document"
            },
            {
              "path": "Scripting/shared/diagnostics.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/external_references",
          "candidate_references": [
            "docs/external_references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/external_references",
                "docs/external_references"
              ],
              "snippet": "rnal repositories.\n\n## What this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;\n- a replacement for local validation;\n- a runtime dependency;\n- a permission to perform destructive changes;\n- a reason to bypass `AGENTS.md`, execution plans or validators.\n\n## Repository policy\n\nFull external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nThe committed repository should contain only:\n\n```text\ndocs/AI_REFERENCE_ONBOARDING.md\ndocs/AI_REFERENCE_SOURCE_MAP.md\ndocs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\ndocs/AI_GUARDRAILS_VALIDATION_GUIDE.md\ndocs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md\n```\n\nThis keeps remote AI agents effective without bloating the repository.\n\n## Recommended agent behavior\n\nWhen an AI agent uses this reference layer, it should:\n\n1. identify the target work area;\n2. read the related guide;\n3. map external concepts to existing project files;\n4. avoid introducing new dependencies unless explicitly approved;\n5. prefer additive documentation, validators and helper modules;\n6. preserve current Blender package behavior;\n7. keep NPU helper work provider-free unless a validated phase says otherwise;\n8. update `docs/README.md` when adding stable documentation;\n9. report uncertainty rather than inventing unsupported repository state.\n\n## Task routing\n\n| Task | Read first |\n|---|---|\n| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_"
            },
            {
              "path": "docs/external_references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/references",
          "candidate_references": [
            "docs/references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/references",
                "docs/references"
           
```

### `output/ai_pipeline/project_complete_balanced_20260502-210841_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `20674`
- SHA-256: `1ac41147368703524d45de6b48c41fd02011e29ff0e847a9da0f83b9044f37dd`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-02T21:18:48",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 524.16,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_balanced_20260502-210841_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_balanced_20260502-210841_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 460.77,\n  \"round_count\": 20,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"empty_recommendations_reason\": \"repair_attempt_failed\",\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/project_complete_balanced_20260502-210841_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/project_complete_balanced_20260502-210841_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "repair_attempt_failed",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "gpu_summary": {
    "passed": true,
    "round_count": 20,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 17,
    "repair_attempt_count": 6,
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
  "checkpoint_dir": "output/ai_pipeline/project_complete_balanced_20260502-210841_checkpoints",
  "npu_audit_count": 5,
  "npu_audit_success_count": 5,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/project_complete_balanced_20260502-210841_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/project_complete_balanced_20260502-210841_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-02T21:10:10",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_001_npu_async_audit_metadata.json",
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
      "finished_at": "2026-05-02T21:11:52",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_balanced_20260502-210841_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_balanced_20260502-210841_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
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
      "round": 3,
      "checkpoint": "output/ai_pipeline/project_complete_balanced_20260502-210841_checkpoints/round_003.json",
      "audit_output": "output/ai_pipeline/project_complete_balanced_20260502-210841_checkpoints/round_003_npu_async_audit.json",
      "started_at": "2026-05-02T21:11:54",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_003.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_003_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_003_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_003_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_003_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_003_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_003_npu_async_audit_metadata.json",
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
      "finished_at": "2026-05-02T21:13:36",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_balanced_20260502-210841_checkpoints\\\\round_003_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_balanced_20260502-210841_checkpoints\\\\round_003_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
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
      "round": 6,
      "checkpoint": "output/ai_pipeline/project_complete_balanced_20260502-210841_checkpoints/round_006.json",
      "audit_output": "output/ai_pipeline/project_complete_balanced_20260502-210841_checkpoints/round_006_npu_async_audit.json",
      "started_at": "2026-05-02T21:13:38",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_006.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_006_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_006_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_006_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_006_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_006_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_balanced_20260502-210841_checkpoints\\round_006_npu_async_audit_metadata.json",
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
      "finished_at": "2026-05-02T21:15:18",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_balanced_20260502-210841_checkpoints\\\\round_006_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\
```

### `output/ai_pipeline/project_complete_balanced_20260502-210841_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `116642`
- SHA-256: `4e5d9ec05a65a34503d7a418e88f4d85db4cf585454a77b9a8d5bfe1e4eb8866`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-02T21:17:44",
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
  "elapsed_seconds": 460.77,
  "context_file_count": 220,
  "round_count": 20,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 5.446,
      "file_count": 8,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md"
      ],
      "response_chars": 432,
      "raw_response_preview": "It seems like you have provided a detailed preview of several markdown files related to AI-generated content and validation processes within a Blender repository. These documents outline standards, guidelines, and procedures for handling AI-generated artifacts, ensuring they meet specific quality and compatibility criteria.\n\nIf you need further assistance or have specific questions about any of these documents, feel free to ask!",
      "parsed_response": {
        "summary": "It seems like you have provided a detailed preview of several markdown files related to AI-generated content and validation processes within a Blender repository. These documents outline standards, guidelines, and procedures for handling AI-generated artifacts, ensuring they meet specific quality and compatibility criteria.\n\nIf you need further assistance or have specific questions about any of these documents, feel free to ask!",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "json_ok": false,
      "parse_error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 9.931,
      "file_count": 8,
      "files": [
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md",
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
        "docs/AI_REFERENCE_ONBOARDING.md"
      ],
      "response_chars": 1818,
      "raw_response_preview": "It seems like you have provided a detailed set of documentation files related to an AI pipeline project. These files cover various aspects such as the architecture, refactoring status, provider-agnostic guidelines, and optimization strategies. Here's a summary of the key points from each file:\n\n1. **AI_PIPELINE_ARCHITECTURE.md**:\n   - Describes the modular architecture of the AI artifact pipeline.\n   - Lists the main components like `defaults.py`, `models.py`, `runner.py`, etc., which are part of the pipeline.\n   - Explains the data flow and interactions between different modules.\n\n2. **AI_PIPELINE_REFACTOR_STATUS.md**:\n   - Provides a status marker for the current state of the AI pipeline refactor.\n   - Indicates that the modular split is complete but local validation is pending.\n   - Lists the required steps for local validation, including running specific Python scripts and regenerating indexes.\n\n3. **AI_PIPELINE_OPTIMIZATION.md**:\n   - Outlines the optimization priorities for the AI pipeline.\n   - Provides a checklist of tasks to be completed after changes to the pipeline.\n   - Emphasizes the importance of local dry-run validation before making further optimizations.\n\n4. **AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md**:\n   - Explains how the AI pipeline should remain reusable across different providers and runtimes.\n   - Defines the boundaries between the orchestration layer, provider layer, and artifact layer.\n   - Provides a recommended sequence of stages for generating artifacts and handling failures.\n\nThese documents are essential for maintaining and extending the AI pipeline project. They ensure that changes are made in a structured manner, with proper validation and testing at each step. If you have any specific questions or need further assistance with these files, feel free to ask!",
      "parsed_response": {
        "summary": "It seems like you have provided a detailed set of documentation files related to an AI pipeline project. These files cover various aspects such as the architecture, refactoring status, provider-agnostic guidelines, and optimization strategies. Here's a summary of the key points from each file:\n\n1. **AI_PIPELINE_ARCHITECTURE.md**:\n   - Describes the modular architecture of the AI artifact pipeline.\n   - Lists the main components like `defaults.py`, `models.py`, `runner.py`, etc., which are part of the pipeline.\n   - Explains the data flow and interactions between different modules.\n\n2. **AI_PIPELINE_REFACTOR_STATUS.md**:\n   - Provides a status marker for the current state of the AI pipeline refactor.\n   - Indicates that the modular split is complete but local validation is pending.\n   - Lists the required steps for local validation, including running specific Python scripts and regenerating indexes.\n\n3. **AI_PIPELINE_OPTIMIZATION.md**:\n   - Outlines the optimization priorities for the AI pipeline.\n   - Provides a checklist of tasks to be completed after changes to the pipeline.\n   - Emphasizes the importance of local dry-run validation before making further optimizations.\n\n4. **AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md**:\n   - Explains how the AI pipeline should remain reusable across different providers and runtimes.\n   - Defines the boundaries between the orchestration layer, provider layer, and artifact layer.\n   - Provides a recommended sequence of stages for generating artifacts and handling failures.\n\nThese documents are essential for maintaining and extending the AI pipeline project. They ensure that changes are made in a structured manner, with proper validation and testing at each step. If you have any specific questions or need further assistance with these files, feel free to ask!",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "json_ok": false,
      "parse_error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "recommended_next_layer": ""
    },
    {
      "round": 3,
      "elapsed_seconds": 26.976,
      "file_count": 8,
      "files": [
        "docs/AI_REFERENCE_SOURCE_MAP.md",
        "docs/AI_SELECTIVE_PLANNER.md",
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md",
        "docs/AUDIO_ANALYSIS_PIPELINE.md",
        "docs/AUTO_PUSH_GENERATED_ARTIFACTS.md",
        "docs/BLENDER_SCRIPT_ENTRYPOINTS.md",
        "docs/CODE_CONSULTATION_REPORT.md"
      ],
      "response_chars": 5369,
      "raw_response_preview": "```json\n{\n  \"path\": \"docs/CODE_CONSULTATION_REPORT.md\",\n  \"exists\": true,\n  \"lines\": 151,\n  \"chars\": 6000,\n  \"content_preview\": \"# Code Consultation Report\\n\\n## Scope\\n\\nThis report summarizes a broad code consultation of `blender-audio-project` after the GitHub code-quality check was launched.\\n\\nThe review is non-destructive. No working Blender script was refactored or modified.\\n\\n## Repository status\\n\\n- Repository: `C-F-tek/blender-audio-project`\\n- Default branch: `master`\\n- Visibility: private\\n- GitHub App permissions observed: admin, maintain, pull, push, triage\\n- Repository size observed: about 2564 KB\\n\\n## Code quality workflow visibility\\n\\nNo workflow run was visible through the available GitHub connector for the checked commits.\\n\\nThe following common workflow paths were not found:\\n\\n```text\\n.github/workflows/code-quality.yml\\n.github/workflows/code_quality.yml\\n.github/workflows/ci.yml\\n```\\n\\nThis means that the code-quality action may be external, not indexed through the available API endpoint, manually launched in a way not returned by commit workflow lookup, or not yet committed as a workflow file.\\n\\n## Source index consulted\\n\\nThe main source index consulted was:\\n\\n```text\\nindexAI/project_code_index.md\\nindexAI/project_code_manifest.json\\n```\\n\\nThe index reports:\\n\\n- 98 indexed files\\n- 212 code chunks\\n- generated timestamp: `2026-04-27T14:41:27`\\n\\nImportant: this index predates the latest documentation and template additions. It should be regenerated.\\n\\n## Main code areas\\n\\n### Root tools\\n\\n| File | Role | Assessment |\\n|---|---|---|\\n| `analyze_wav.py` | WAV analysis, low/mid/high/onset/beat extraction, Blender JSON generation | Good functional core. Needs dependency documentation and optional validation. |\\n| `build_track_summary.py` | Compact summary builder from analysis JSON | Useful, but default paths are track-specific. Should be made more generic or documented as local defaults. |\\n| `normalize_scene_spec.py` | Scene-spec normalization | Useful, but contains duplicated helper function definitions that should be reviewed. |\\n\\n### Blender package area\\n\\n| Area | Role | Assessment |\\n|---|---|---|\\n| `Scripting/v61b/` | Main complex reference package | Strong reference model. Do not refactor broadly without Blender tests. |\\n| `Scripting/v61b_backgood/` | Backup or previous-good version | Useful safety copy, but should be documented as backup/reference. |\\n| `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/` | Additional generated package | Should be compared with v61b standards and documented per package. |\\n| `Scripting/_template_audio_reactive_package/` | New package template | Good structure. Not part of old index yet. |\\n| `Scripting/shared/` | Shared utility target area | Policy exists; code extraction is intentionally pending. |\\n\\n### AI and NPU tooling\\n\\n| Area | Role | Assessment |\\n|---|---|---|\\n| `Tools/npu/` | Local AI, NPU, context generation, dual AI pipeline | Rich but compl",
      "parsed_response": {
        "summary": "```json\n{\n  \"path\": \"docs/CODE_CONSULTATION_REPORT.md\",\n  \"exists\": true,\n  \"lines\": 151,\n  \"chars\": 6000,\n  \"content_preview\": \"# Code Consultation Report\\n\\n## Scope\\n\\nThis report summarizes a broad code consultation of `blender-audio-project` after the GitHub code-quality check was launched.\\n\\nThe review is non-destructive. No working Blender script was refactored or modified.\\n\\n## Repository status\\n\\n- Repository: `C-F-tek/blender-audio-project`\\n- Default branch: `master`\\n- Visibility: private\\n- GitHub App permissions observed: admin, maintain, pull, push, triage\\n- Repository size observed: about 2564 KB\\n\\n## Code quality workflow visibility\\n\\nNo workflow run was visible through the available GitHub connector for the checked commits.
```

### `output/ai_pipeline/repository_change_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3476`
- SHA-256: `6057ede2ac6aad96e450dc2513f20278713fb1b9d247d649950c4ec5a9cfa2c6`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-02T21:19:52`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-AI-WORKLOAD-REPORT-QUALITY-GATE — Gate AI workload reports before using them as advisory context

- Priority: `P1`
- Area: `local_ai_workloads`
- Change type: `workload_quality_gate`
- Apply mode: `manual_review_only`
- Rationale: AI workload report quality found usable lanes: ollama; unusable lanes: npu. Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed.

### Evidence summary

```json
{
  "workload_quality_decision": {
    "quality_report_present": true,
    "usable_lanes": [
      "ollama"
    ],
    "unusable_lanes": [
      "npu"
    ],
    "ollama_gpu_primary_advisory_allowed": true,
    "npu_excluded_from_primary_advisory": true,
    "routing_policy": "usable_text_lanes_only_for_advisory_context"
  }
}
```

### Target files
- `Tools/validation/check_ai_workload_report_quality.py`
- `Tools/npu/run_npu_review.py`
- `Tools/ai/suggest_repository_updates.py`
- `Tools/ai/build_repository_change_proposals.py`
- `Tools/validation/README.md`
- `docs/JSON_SCHEMAS.md`

### Patch sketch
- Keep Ollama/GPU workload reports as primary advisory context when classified usable.
- Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.
- Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.
- Add report metadata that distinguishes availability, execution and output usability.

### Suggestion outputs
- `python_code` `Tools/validation/check_ai_workload_report_quality.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/npu/run_npu_review.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/build_repository_change_proposals.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change would execute providers implicitly or by default.
- Any change would hide a failing/unusable AI workload report instead of reporting it.
- Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

### `output/validation/agent_review_patch_plan_smoke_project_complete_balanced_20260502-210841.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `302`
- SHA-256: `149f07a209d7c38d3df17249a5e644a4bf7a6a8b398e958e9f79363acb540995`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Patch Plan Smoke

- Passed: `True`
- Return code: `0`
- Patch plan count: `12`
- Fallback used: `True`
- Provider execution performed: `False`
- Patch application performed: `False`

## Warnings

- fallback_used is true; GPU planner produced no usable ready recommendation


```

### `output/validation/gpu_planner_json_contract_smoke_20260502-210841.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `925`
- SHA-256: `d98845c217da543038e9253b5f6b4df26e2f5337ab6bf4dde9d275b759811061`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Smoke

- Passed: `True`
- Case count: `4`
- Failed case count: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## `valid_recommendation`

- Passed: `True`
- Expected reason: ``
- Reason: ``
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`

## `malformed_json`

- Passed: `True`
- Expected reason: `json_parse_failure`
- Reason: `json_parse_failure`
- JSON OK: `False`
- Schema OK: `False`
- Context echo detected: `False`

## `schema_context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`


```

### `output/validation/npu_provider_environment_project_complete_20260502-210841.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `304`
- SHA-256: `ebcef793de1795cfc3f55063d9a02cad3467d28b6cee31e068b8067e70e75ded`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Provider Environment

- `passed`: `True`
- `npu_python`: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`
- `npu_python_exists`: `True`
- `openvino_import`: `True`
- `openvino_genai_import`: `True`
- `openvino_genai_pip_package`: `openvino-genai`
- `npu_available`: `True`

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
