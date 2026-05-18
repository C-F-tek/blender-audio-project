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
python -m Tools.ai check_npu_provider_environment `
  --repo-root . `
  --output ".\output\validation\npu_provider_environment_project_complete_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_project_complete_$Stamp.md"

Get-Content ".\output\validation\npu_provider_environment_project_complete_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, provider_execution_performed, patch_application_performed
```

## 3. Run project-only static gates

```powershell
python -m Tools.validation.docs_hygiene.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_project_complete_$Stamp.json"

python -m Tools.ai build_code_interpreter_report `
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
python -m Tools.ai run_agent_gpu_npu_parallel_orchestrator `
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
  ".\Tools\ai\provider_mesh\gpu_npu_parallel_orchestrator\cli.py",
  ".\Tools\ai\provider_mesh\gpu_deep_planning_review\cli.py",
  ".\Tools\ai\provider_mesh\gpu_deep_planning_supervised\cli.py",
  ".\Tools\ai\agent_review\patch_plan\cli.py",
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
python -m Tools.ai agent_review_patch_plan `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_${Stamp}_orchestrator.json" `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output ".\output\patch_specs\agent_review_patch_plan_project_complete_$Stamp.json" `
  --markdown-output ".\output\patch_specs\agent_review_patch_plan_project_complete_$Stamp.md"

python -m Tools.validation run_agent_review_patch_plan_smoke `
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

python -m Tools.ai.repository_product.github_evidence_bundle `
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
python -m Tools.validation check_github_evidence_bundle `
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
