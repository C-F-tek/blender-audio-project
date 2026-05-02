# Next Chat Handoff After Balanced Full Run — 2026-05-02

## Purpose

Use this Markdown file as the first context document in the next ChatGPT/AI session.

It captures the current repository state, the merged PR sequence, the latest full local AI run, the exact next task, and the canonical `0 -> 10` operating procedure for future complete runs.

The goal is to avoid losing time reconstructing state.

## Repository

```text
repository: C-F-tek/blender-audio-project
branch to use: master
current workflow: GitHub/API + local validation when requested
project: IA-Carmine
```

## Current master baseline

The following work is already merged into `master`:

```text
PR #109: docs(ai): design manual-review code patch plan lane
PR #111: feat(ai): surface GPU repair-failure recommendations
PR #112: feat(ai): harden GPU planner JSON contract
PR #113: feat(ai): analyze GPU/NPU run sync and balanced profile
PR #114: feat(ai): replay GPU planner JSON contract on real outputs
```

Latest pushed full-run evidence commit:

```text
1d42078 test(ai): add balanced project complete AI-to-AI evidence bundle
```

Important post-PR114 handoff already exists:

```text
docs/LOCAL_AI_TASKS/post-pr114-next-task-handoff.md
```

This file is a more compact and operational new-chat handoff.

## Essential result from the latest balanced full run

Run stamp:

```text
20260502-210841
```

Committed bundle:

```text
docs/LOCAL_VALIDATION_EVIDENCE/project_complete_balanced_ai_to_ai_bundle_20260502-210841.json
docs/LOCAL_VALIDATION_EVIDENCE/project_complete_balanced_ai_to_ai_bundle_20260502-210841.md
```

Git state after push:

```text
HEAD -> master
origin/master -> master
working tree clean
```

Observed summary:

```text
orchestrator passed=true
gpu_recommendation_count=0
gpu_empty_recommendations_reason=repair_attempt_failed
npu_audit_count=5
npu_audit_success_count=5
fallback_patch_plan_count=12
manual_review_required=true
patch_application_performed=false
source_writes_performed=false
```

GPU JSON contract replay on the balanced run:

```text
replayed_round_count=20
context_echo_detected_count=1
json_parse_failure_count=18
model_output_schema_mismatch_count=1
valid_recommendation_output_count=0
```

GPU/NPU sync on the balanced run:

```text
gpu_round_count=20
npu_audit_count=5
npu_audit_success_count=5
npu_audit_round_coverage=0.25
avg_gpu_round_seconds=26.208
avg_npu_audit_seconds=101.6
npu_to_gpu_avg_duration_ratio=3.877
gpu_elapsed_seconds=524.16
```

Comparison against previous full run:

```text
old json_parse_failure=22 -> new json_parse_failure=18
old model_output_schema_mismatch=2 -> new model_output_schema_mismatch=1
old npu_coverage=0.208 -> new npu_coverage=0.25
old npu_to_gpu_ratio=4.241 -> new npu_to_gpu_ratio=3.877
old elapsed roughly 668/706 sec -> new elapsed 524.16 sec
```

Interpretation:

```text
Balanced parameters improved timing and reduced JSON failures, but did not produce valid GPU recommendations yet.
The GPU planner still needs diagnostic wiring and prompt hardening.
Do not tune tokens again before wiring the contract helper into the runner.
```

## Current most important next task

Next PR title:

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

Required behavior:

```text
Use Tools.ai.gpu_planner_json_contract.validate_model_response_contract() inside the real GPU runner diagnostic path.
Classify model responses as json_parse_failure, model_output_schema_mismatch, context_echo_detected, evidence_ready_but_no_gpu_plan, or valid_json_empty_recommendations.
Preserve legacy fields for compatibility.
Do not change provider/model settings in this PR.
Do not rewrite prompts in this PR.
Do not apply patches automatically.
```

Recommended new branch:

```text
codex/wire-gpu-json-contract-runner
```

Recommended PR scope:

```text
1. import validate_model_response_contract and result_to_dict into Tools/ai/run_agent_gpu_deep_planning_review.py
2. extend parse/recommendation diagnostics with contract_* fields
3. aggregate new reason precedence while preserving legacy output shape
4. add/update a small doc note if needed
5. validate locally
6. commit one compact PR evidence bundle only
```

Reason precedence for new diagnostics:

```text
context_echo_detected
json_parse_failure
model_output_schema_mismatch
recommendations_filtered_out
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

Keep `repair_attempt_failed` only as legacy compatibility for older reports, not as the preferred new classifier.

## Do not mix with prompt hardening yet

Prompt hardening is the next separate PR after diagnostic wiring.

Future PR title:

```text
feat(ai): harden GPU planner prompt JSON-only footer
```

That later PR may add:

```text
JSON-only footer
schema-only output example
explicit no top-level files/content_preview/content/raw context echo
compact retry lane
shorter response schema
```

But do not combine that with runner diagnostic wiring.

## Guardrails

Never do these without explicit command:

```text
delete
force-push
rewrite history
merge to master/protected branch
change secrets/permissions/billing/visibility
deploy production
```

Project guardrails:

```text
no provider execution unless explicitly part of a local complete run
no automatic patch application
no Blender runtime execution
no SQLite/database commit
no raw output/** commit
no full analysis JSON commit outside compact evidence bundle
no NPU advisory promotion
no OpenVINO GPU primary lane
manual review required for patch plans
```

## Bundle retention law

Canonical policy:

```text
docs/LOCAL_VALIDATION_EVIDENCE/README.md
```

Rule:

```text
commit the smallest bundle that proves the decision
```

For normal PRs:

```text
one final compact evidence bundle
no duplicate failed bundles unless after-fix evidence is required
prefer <= 10 included artifacts
prefer <= 1 MB total PR evidence
```

Do not delete existing bundles automatically. Cleanup/removal requires explicit human approval.

## Full runs with full tools

Definition used in this project:

```text
full run / complete run / full tools = all applicable local project tools and AI lanes active
```

A complete run includes:

```text
static Python syntax validation
code interpreter/static code report
NPU/provider preflight
GPU/Ollama planner provider execution
NPU checkpoint auditor provider execution when available
post-validation AI packet
fallback manual-review patch-plan builder
patch-plan smoke validation
GPU JSON contract replay
GPU/NPU sync analysis
compact GitHub evidence bundle
bundle validation
commit/push only compact bundle
GitHub audit from committed evidence
```

Complete run is still report-only:

```text
patch_application_performed=false
source_writes_performed=false
blender_runtime_execution_performed=false
sqlite_write_performed=false
manual_review_required=true
```

## Current best complete-run parameters

Use the balanced profile from PR #113 / latest full run:

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

Do not increase GPU token budget before runner wiring and prompt hardening.

## 0 -> 10 canonical complete-run procedure

### 0. Sync and shell setup

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short
git log --oneline -8

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
"STAMP=$Stamp"
```

### 1. Read official request/runbooks

```powershell
Get-Content .\AGENTS.md -TotalCount 220
Get-Content .\docs\LOCAL_AI_RUN_BOOTSTRAP.md -TotalCount 220
Get-Content .\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md -TotalCount 260
Get-Content .\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-procedure.md -TotalCount 360
Get-Content .\docs\LOCAL_AI_TASKS\gpu-npu-balanced-run-profile.md -TotalCount 260
Get-Content .\docs\LOCAL_AI_TASKS\post-pr114-next-task-handoff.md -TotalCount 320
Get-Content .\docs\LOCAL_AI_TASKS\next-chat-handoff-after-balanced-full-run-2026-05-02.md -TotalCount 360
Get-Content .\docs\LOCAL_VALIDATION_EVIDENCE\README.md -TotalCount 220
```

### 2. NPU/provider preflight

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output ".\output\validation\npu_provider_environment_project_complete_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_project_complete_$Stamp.md"
```

### 3. Static gates

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

### 4. Contract/tool smoke

```powershell
python -m py_compile `
  .\Tools\ai\gpu_planner_json_contract.py `
  .\Tools\ai\replay_gpu_planner_json_contract.py `
  .\Tools\ai\analyze_gpu_npu_run_sync.py `
  .\Tools\ai\build_gpu_repair_failure_recommendation.py `
  .\Tools\validation\run_gpu_planner_json_contract_smoke.py

python .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  --repo-root . `
  --output ".\output\validation\gpu_planner_json_contract_smoke_$Stamp.json" `
  --markdown-output ".\output\validation\gpu_planner_json_contract_smoke_$Stamp.md"
```

### 5. Full GPU/NPU orchestrator

```powershell
python .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py `
  --repo-root . `
  --budget-minutes 30 `
  --max-rounds 20 `
  --files-per-round 8 `
  --max-context-files 220 `
  --max-chars-per-file 6000 `
  --max-new-tokens 3600 `
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
  --npu-auditor-every-rounds 3 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 420 `
  --npu-max-context-chars 8000 `
  --npu-max-prompt-chars 1200 `
  --npu-max-new-tokens 384 `
  --npu-final-wait-seconds 180 `
  --checkpoint-dir ".\output\ai_pipeline\project_complete_balanced_${Stamp}_checkpoints" `
  --gpu-output ".\output\ai_pipeline\project_complete_balanced_${Stamp}_parallel_gpu.json" `
  --gpu-markdown-output ".\output\ai_pipeline\project_complete_balanced_${Stamp}_parallel_gpu.md" `
  --output ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json" `
  --markdown-output ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.md"
```

### 6. Inspect orchestrator

```powershell
$orch = Get-Content ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json" -Raw | ConvertFrom-Json
$orch | Select-Object passed, elapsed_seconds, gpu_recommendation_count, gpu_empty_recommendations_reason, npu_audit_count, npu_audit_success_count
$orch.gpu_summary
$orch.decision
```

### 7. Replay GPU JSON contract

```powershell
python .\Tools\ai\replay_gpu_planner_json_contract.py `
  --repo-root . `
  --gpu-report ".\output\ai_pipeline\project_complete_balanced_${Stamp}_parallel_gpu.json" `
  --output ".\output\analysis\gpu_json_contract_replay_balanced_$Stamp.json" `
  --markdown-output ".\output\analysis\gpu_json_contract_replay_balanced_$Stamp.md"
```

### 8. Analyze GPU/NPU sync

```powershell
python .\Tools\ai\analyze_gpu_npu_run_sync.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json" `
  --output ".\output\analysis\gpu_npu_run_sync_balanced_$Stamp.json" `
  --markdown-output ".\output\analysis\gpu_npu_run_sync_balanced_$Stamp.md"
```

### 9. Post-validation packet and fallback patch-plan

```powershell
$GpuReport = ".\output\ai_pipeline\project_complete_balanced_${Stamp}_parallel_gpu.json"

$ContextFiles = @(
  ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md",
  ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-procedure.md",
  ".\docs\LOCAL_AI_TASKS\post-pr114-next-task-handoff.md",
  ".\docs\LOCAL_AI_TASKS\next-chat-handoff-after-balanced-full-run-2026-05-02.md",
  ".\docs\LOCAL_AI_TASKS\gpu-json-contract-runner-integration.md",
  ".\docs\LOCAL_AI_TASKS\gpu-npu-balanced-run-profile.md",
  ".\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py",
  ".\Tools\ai\run_agent_gpu_deep_planning_review.py",
  ".\Tools\ai\run_agent_gpu_deep_planning_supervised.py",
  ".\Tools\ai\gpu_planner_json_contract.py",
  ".\output\analysis\code_interpreter_project_complete_$Stamp.md",
  ".\output\analysis\gpu_json_contract_replay_balanced_$Stamp.md",
  ".\output\analysis\gpu_npu_run_sync_balanced_$Stamp.md"
)

$ReportFiles = @(
  ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json",
  $GpuReport,
  ".\output\analysis\code_interpreter_project_complete_$Stamp.json",
  ".\output\validation\npu_provider_environment_project_complete_$Stamp.json",
  ".\output\validation\gpu_planner_json_contract_smoke_$Stamp.json",
  ".\output\analysis\gpu_json_contract_replay_balanced_$Stamp.json",
  ".\output\analysis\gpu_npu_run_sync_balanced_$Stamp.json"
)

$params = @{
  Profile     = "core"
  ContextFile = $ContextFiles
  ReportFile  = $ReportFiles
}

& .\Tools\workflow\run_post_validation_ai_packet.ps1 @params

python .\Tools\ai\build_agent_review_patch_plan.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json" `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output ".\output\patch_specs\agent_review_patch_plan_project_complete_balanced_$Stamp.json" `
  --markdown-output ".\output\patch_specs\agent_review_patch_plan_project_complete_balanced_$Stamp.md"

python .\Tools\validation\run_agent_review_patch_plan_smoke.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json" `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output ".\output\validation\agent_review_patch_plan_smoke_project_complete_balanced_$Stamp.json" `
  --markdown-output ".\output\validation\agent_review_patch_plan_smoke_project_complete_balanced_$Stamp.md"
```

### 10. Bundle, validate, push

```powershell
$Reports = @(
  ".\output\validation\python_syntax_project_complete_$Stamp.json",
  ".\output\validation\npu_provider_environment_project_complete_$Stamp.json",
  ".\output\validation\gpu_planner_json_contract_smoke_$Stamp.json",
  ".\output\analysis\code_interpreter_project_complete_$Stamp.json",
  ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json",
  ".\output\ai_pipeline\project_complete_balanced_${Stamp}_parallel_gpu.json",
  ".\output\analysis\gpu_json_contract_replay_balanced_$Stamp.json",
  ".\output\analysis\gpu_npu_run_sync_balanced_$Stamp.json",
  ".\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json",
  ".\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json",
  ".\output\ai_pipeline\repository_change_proposals.json",
  ".\output\patch_specs\agent_review_patch_plan_project_complete_balanced_$Stamp.json",
  ".\output\validation\agent_review_patch_plan_smoke_project_complete_balanced_$Stamp.json"
) | Where-Object { Test-Path $_ }

python -m Tools.ai.build_github_evidence_bundle `
  --repo-root . `
  --basename project_complete_balanced_ai_to_ai_bundle_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-procedure.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\post-pr114-next-task-handoff.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\next-chat-handoff-after-balanced-full-run-2026-05-02.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\gpu-npu-balanced-run-profile.md" `
  --artifact ".\docs\LOCAL_VALIDATION_EVIDENCE\README.md" `
  --artifact ".\output\analysis\code_interpreter_project_complete_$Stamp.md" `
  --artifact ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.md" `
  --artifact ".\output\ai_pipeline\project_complete_balanced_${Stamp}_parallel_gpu.md" `
  --artifact ".\output\analysis\gpu_json_contract_replay_balanced_$Stamp.md" `
  --artifact ".\output\analysis\gpu_npu_run_sync_balanced_$Stamp.md" `
  --artifact ".\output\patch_specs\agent_review_patch_plan_project_complete_balanced_$Stamp.md" `
  --max-included-artifact-chars 12000 `
  --max-included-artifacts 20

python -m Tools.validation.check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_balanced_ai_to_ai_bundle_$Stamp.json" `
  --output ".\output\validation\project_complete_balanced_ai_to_ai_bundle_${Stamp}_validation.json"

git status --short
git diff --check

git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_balanced_ai_to_ai_bundle_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_balanced_ai_to_ai_bundle_$Stamp.md"

git diff --cached --name-only
git commit -m "test(ai): add balanced project complete AI-to-AI evidence bundle"
git push origin master

git status --short
git log --oneline -8
```

## Fast summary command after full run

```powershell
@{
  Stamp = $Stamp
  Orchestrator = (Get-Content ".\output\ai_pipeline\project_complete_balanced_${Stamp}_orchestrator.json" -Raw | ConvertFrom-Json |
    Select-Object passed, elapsed_seconds, gpu_recommendation_count, gpu_empty_recommendations_reason, npu_audit_count, npu_audit_success_count)
  Replay = (Get-Content ".\output\analysis\gpu_json_contract_replay_balanced_$Stamp.json" -Raw | ConvertFrom-Json |
    Select-Object replayed_round_count, context_echo_detected_count, json_parse_failure_count, model_output_schema_mismatch_count, valid_recommendation_output_count)
  Sync = (Get-Content ".\output\analysis\gpu_npu_run_sync_balanced_$Stamp.json" -Raw | ConvertFrom-Json).metrics
} | ConvertTo-Json -Depth 6
```

## Immediate next action for the next chat

Do not run another full tool run immediately.

Next step should be a focused PR:

```text
feat(ai): wire GPU planner JSON contract into runner diagnostics
```

Then after merge, run the full `0 -> 10` procedure again and compare:

```text
json_parse_failure_count
model_output_schema_mismatch_count
context_echo_detected_count
valid_recommendation_output_count
gpu_empty_recommendations_reason
fallback_patch_plan_count
npu_audit_round_coverage
npu_to_gpu_avg_duration_ratio
```

## Short prompt to paste into next chat

```text
Leggi integralmente `docs/LOCAL_AI_TASKS/next-chat-handoff-after-balanced-full-run-2026-05-02.md`.

Repository: C-F-tek/blender-audio-project.
Branch: master.
Project: IA-Carmine.

Riprendi esattamente dallo stato descritto nel file.
Non reinventare architettura o stato.
Procedi con la prossima PR consigliata: `feat(ai): wire GPU planner JSON contract into runner diagnostics`.
Usa GitHub/API per leggere e modificare la repo.
Non fare merge su master senza mio comando esplicito.
Non cambiare provider/model settings in questa PR.
Non fare prompt rewriting in questa PR.
Non applicare patch automaticamente.
Quando tocchi codice/script, indica sempre il numero di righe risultante.
Dopo ogni modifica prepara comandi locali di validazione e bundle compatto secondo la policy evidence.
```
