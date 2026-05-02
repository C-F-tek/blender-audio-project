# Code Refactor 0 -> 10 Procedure — IA-Carmine

## Purpose

Use this guide when the user asks to start a code refactor cycle.

This is the canonical 0 -> 10 operating procedure for report-only code refactoring in `C-F-tek/blender-audio-project` after PR #116.

It combines:

```text
- current post-PR116 repository state
- full Python line-count inventory
- repository/tool discovery before planning
- helper/function reuse and promotion review
- balanced GPU/NPU AI-to-AI run
- manual-review code patch-plan lane
- compact evidence bundle policy
```

Default mode:

```text
report-only
manual-review-only
no automatic patch application
no Blender runtime
no raw output/** commit
```

## Current context baseline

Repository:

```text
repository: C-F-tek/blender-audio-project
branch to sync: master
project: IA-Carmine
workflow: local validation + GitHub/API PRs
```

Merged baseline at the time this guide was written:

```text
PR #109: docs(ai): design manual-review code patch plan lane
PR #111: feat(ai): surface GPU repair-failure recommendations
PR #112: feat(ai): harden GPU planner JSON contract
PR #113: feat(ai): analyze GPU/NPU run sync and balanced profile
PR #114: feat(ai): replay GPU planner JSON contract on real outputs
PR #115: feat(ai): wire GPU planner JSON contract into runner diagnostics
PR #116: docs(ai): add post-PR115 full Python refactor handoff
```

Relevant current master commits:

```text
56bb6b0 feat(ai): wire GPU planner JSON contract into runner diagnostics
5dfd127 docs(ai): add post-PR115 full Python refactor handoff
```

Primary post-PR116 entry handoff:

```text
docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md
```

## Core rule

A code refactor cycle must not start from intuition only.

It must start from:

```text
1. current repo state
2. current docs/runbooks
3. full Python line-count CSV
4. complete Python inventory Markdown, not top-N only
5. existing reusable tools/helpers
6. report-only validation evidence
```

Line count is a signal, not a filter. The planner must see all counted Python files and decide candidates.

## Refactor-specific guardrails

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
no automatic patch application
no Blender runtime execution
no SQLite/database commit
no raw output/** commit
no full analysis JSON commit outside compact evidence bundle
no NPU advisory promotion
no OpenVINO GPU primary lane
manual review required for patch plans
```

Code refactor guardrails:

```text
no broad rewrite of large files in one PR
no provider/model setting changes unless explicitly requested
no prompt rewriting unless explicitly requested
preserve CLI arguments and report schemas unless a migration plan is explicit
prefer reuse/promotion of existing helpers over new duplication
always include validation commands and stop conditions
```

Legacy/refactor exclusion:

```text
Do not create ready-for-patch refactor plans for paths containing:
legacy
archive
old
backup
bak
```

Exception:

```text
Scripting/v61b/** is the current template lane and may be reviewed/refactored only when the path is not a backup path.
```

Allowed examples:

```text
Scripting/v61b/*.py
Scripting/v61b/**/*.py
```

Disallowed examples:

```text
Scripting/v61b/**/backup*/**
Scripting/v61b/**/*backup*.py
Scripting/v61b/**/*bak*.py
any path outside Scripting/v61b containing legacy/archive/old/backup/bak
```

If a legacy/archive/backup issue is valuable but outside scope, classify it as:

```text
advisory_only
needs_more_context
```

not:

```text
ready_for_patch_plan
```

---

# 0 -> 10 Procedure

## 0. Sync repository and shell setup

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short
git log --oneline -10

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
"STAMP=$Stamp"
```

Expected:

```text
git status --short is empty
HEAD is master/origin/master
```

Do not continue if local source files are dirty unless the user explicitly says those changes are intentional input.

## 1. Read repository instructions and reference docs

Read these before planning or running a refactor cycle:

```powershell
Get-Content .\AGENTS.md -TotalCount 260
Get-Content .\docs\LOCAL_AI_RUN_BOOTSTRAP.md -TotalCount 260
Get-Content .\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md -TotalCount 420
Get-Content .\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-review-request.md -TotalCount 300
Get-Content .\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-procedure.md -TotalCount 420
Get-Content .\docs\LOCAL_AI_TASKS\gpu-npu-balanced-run-profile.md -TotalCount 280
Get-Content .\docs\LOCAL_AI_TASKS\post-pr114-next-task-handoff.md -TotalCount 340
Get-Content .\docs\LOCAL_AI_TASKS\next-chat-handoff-after-balanced-full-run-2026-05-02.md -TotalCount 380
Get-Content .\docs\LOCAL_AI_TASKS\next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md -TotalCount 520
Get-Content .\docs\LOCAL_VALIDATION_EVIDENCE\README.md -TotalCount 240
```

Purpose:

```text
avoid reinventing architecture
reuse existing project rules
respect evidence/bundle policy
stay aligned with current post-PR115 diagnostics
```

## 2. Discover existing tools/helpers before proposing refactor

Inspect existing reusable primitives before inventing new modules:

```powershell
Get-Content .\Tools\ai\code_patch_plan_common.py -TotalCount 360
Get-Content .\Tools\ai\code_edit_proposal_helpers.py -TotalCount 420
Get-Content .\Tools\ai\build_agent_review_code_patch_plan.py -TotalCount 420
Get-Content .\Tools\ai\build_code_edit_proposal_from_plan.py -TotalCount 420
Get-Content .\Tools\ai\build_code_interpreter_report.py -TotalCount 360
Get-Content .\Tools\ai\build_github_evidence_bundle.py -TotalCount 420
Get-Content .\Tools\validation\build_python_line_count_csv.py -TotalCount 320
Get-Content .\Tools\validation\run_agent_review_code_patch_plan_smoke.py -TotalCount 360
Get-Content .\Tools\validation\check_python_syntax.py -TotalCount 260
Get-Content .\Tools\validation\check_validation_report_contract.py -TotalCount 300
```

Search for already-factored utilities:

```powershell
Get-ChildItem .\Tools -Recurse -File -Filter *.py |
  Select-String -Pattern "def repo_rel|def resolve_path|def write_json|def render_markdown|report_only_guardrails|write_json_and_markdown|normalize_repo_path|load_line_counts" |
  Select-Object Path, LineNumber, Line |
  Format-Table -AutoSize
```

Helper decision taxonomy for every proposed refactor:

```text
reuse_existing_helper
promote_existing_function
extract_new_shared_helper
keep_local_by_design
```

Promotion candidates:

```text
path normalization
JSON read/write
Markdown report rendering
guardrail blocks
compact value/list helpers
validation command generation
line-count loading/parsing
report-only schema fields
forbidden target checks
```

Preferred promotion targets:

```text
Tools/ai/code_patch_plan_common.py
Tools/validation/report_utils.py
existing local helper modules in Tools/ai or Tools/validation
```

Do not create a new shared helper module if an existing one is a better fit.

## 3. Build full Python line-count evidence

Run the deterministic line-count tool:

```powershell
python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
  --markdown-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.md"
```

Inspect report summary:

```powershell
$LineCountReport = Get-Content ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" -Raw | ConvertFrom-Json
$LineCountCsv = $LineCountReport.csv_written

$LineCountReport |
  Select-Object passed, file_count, total_lines, csv_written, errors, warnings

"LINE_COUNT_CSV=$LineCountCsv"
```

Create a full untruncated Markdown inventory from the CSV:

```powershell
$LineCountAllMd = ".\output\validation\python_line_count_all_python_files_$Stamp.md"
$Rows = Import-Csv $LineCountCsv | Sort-Object {[int]$_.Lines} -Descending
$TotalLines = ($Rows | Measure-Object -Property Lines -Sum).Sum
$FileCount = ($Rows | Measure-Object).Count

$Lines = @()
$Lines += "# Full Python Line Count Inventory"
$Lines += ""
$Lines += "- Stamp: `$Stamp`"
$Lines += "- CSV: `$LineCountCsv`"
$Lines += "- File count: `$FileCount`"
$Lines += "- Total Python lines: `$TotalLines`"
$Lines += "- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20."
$Lines += ""
$Lines += "| Lines | File |"
$Lines += "|---:|---|"
foreach ($Row in $Rows) {
  $Lines += "| $($Row.Lines) | `$($Row.File)` |"
}
$Lines | Set-Content -Path $LineCountAllMd -Encoding UTF8

Get-Content $LineCountAllMd -Raw
```

Rule:

```text
The complete inventory is the input. Do not reduce the planner view to only top 10/top 20 files.
```

## 4. Static validation and code interpreter report

Run baseline syntax validation:

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_code_refactor_$Stamp.json"
```

Run static/code interpreter style report with current tool roots and template roots:

```powershell
python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/npu `
  --input Tools/workflow `
  --input Scripting/v61b `
  --input Scripting/shared `
  --output ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" `
  --markdown-output ".\output\analysis\code_interpreter_code_refactor_$Stamp.md"
```

Inspect summary:

```powershell
Get-Content ".\output\validation\python_syntax_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, checked_count, failed_count, errors, warnings

Get-Content ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, errors, warnings
```

Stop if syntax validation fails unexpectedly.

## 5. Contract/tool smoke before provider run

Post-PR115 diagnostics depend on the GPU JSON contract helpers. Validate them before a long run:

```powershell
python -m py_compile `
  .\Tools\ai\gpu_planner_json_contract.py `
  .\Tools\ai\replay_gpu_planner_json_contract.py `
  .\Tools\ai\analyze_gpu_npu_run_sync.py `
  .\Tools\ai\build_gpu_repair_failure_recommendation.py `
  .\Tools\ai\run_agent_gpu_deep_planning_review.py `
  .\Tools\ai\run_agent_gpu_deep_planning_supervised.py `
  .\Tools\validation\run_gpu_planner_json_contract_smoke.py

python .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  --repo-root . `
  --output ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json" `
  --markdown-output ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.md"
```

Inspect:

```powershell
Get-Content ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, case_count, failed_case_count, patch_application_performed, source_writes_performed
```

## 6. NPU/provider preflight

Run NPU provider environment check:

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.md"
```

Inspect:

```powershell
Get-Content ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, provider_execution_performed, patch_application_performed, errors, warnings
```

## 7. Run balanced GPU/NPU complete review

Use the balanced profile. Do not increase token budget before evaluating post-PR115 diagnostics.

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
  --report-file ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" `
  --report-file ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
  --context-root docs `
  --context-root Tools\ai `
  --context-root Tools\validation `
  --context-root Tools\workflow `
  --context-root Tools\npu `
  --context-root Scripting\v61b `
  --context-root Scripting\shared `
  --context-root $LineCountAllMd `
  --run-npu-auditor-provider `
  --npu-auditor-every-rounds 3 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 420 `
  --npu-max-context-chars 8000 `
  --npu-max-prompt-chars 1200 `
  --npu-max-new-tokens 384 `
  --npu-final-wait-seconds 180 `
  --checkpoint-dir ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_checkpoints" `
  --gpu-output ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_parallel_gpu.json" `
  --gpu-markdown-output ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_parallel_gpu.md" `
  --output ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_orchestrator.json" `
  --markdown-output ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_orchestrator.md"
```

Monitor in a second PowerShell:

```powershell
nvidia-smi -l 1
```

Checkpoint monitor:

```powershell
while ($true) {
  Get-ChildItem ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_checkpoints" -Filter "round_*.json" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime |
    Select-Object -Last 8 Name, LastWriteTime, Length |
    Format-Table -AutoSize
  Start-Sleep 10
  Clear-Host
}
```

## 8. Inspect post-PR115 diagnostics

Inspect orchestrator/GPU result:

```powershell
$OrchOut = ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_orchestrator.json"
$GpuOut = ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_parallel_gpu.json"

$orch = Get-Content $OrchOut -Raw | ConvertFrom-Json
$gpu = Get-Content $GpuOut -Raw | ConvertFrom-Json

$orch |
  Select-Object passed, elapsed_seconds, gpu_recommendation_count, gpu_empty_recommendations_reason, gpu_evidence_ready_for_manual_patch_count, gpu_recommended_next_layer, npu_audit_count, npu_audit_success_count, patch_application_performed

$gpu |
  Select-Object passed, round_count, recommendation_count, empty_recommendations_reason, context_echo_detected_count, json_parse_error_count, model_output_schema_mismatch_count, evidence_ready_for_manual_patch_count, recommended_next_layer

$gpu.rounds |
  Select-Object round, json_ok, schema_ok, context_echo_detected, model_output_schema_mismatch, raw_recommendation_candidate_count, filtered_recommendation_count, empty_recommendations_reason, contract_empty_recommendations_reason |
  Format-Table -AutoSize
```

Expected post-PR115 improvement:

```text
Top-level GPU reason should prefer context_echo_detected/json_parse_failure/model_output_schema_mismatch/evidence_ready_but_no_gpu_plan instead of generic repair_attempt_failed.
```

A diagnostic-only success may still have:

```text
gpu_recommendation_count=0
manual_review_required=true
patch_application_performed=false
source_writes_performed=false
```

## 9. Replay contract, analyze sync, build post-validation/refactor packet

Replay GPU JSON contract:

```powershell
python .\Tools\ai\replay_gpu_planner_json_contract.py `
  --repo-root . `
  --gpu-report $GpuOut `
  --output ".\output\analysis\gpu_json_contract_replay_code_refactor_$Stamp.json" `
  --markdown-output ".\output\analysis\gpu_json_contract_replay_code_refactor_$Stamp.md"
```

Analyze GPU/NPU sync:

```powershell
python .\Tools\ai\analyze_gpu_npu_run_sync.py `
  --repo-root . `
  --orchestrator $OrchOut `
  --output ".\output\analysis\gpu_npu_run_sync_code_refactor_$Stamp.json" `
  --markdown-output ".\output\analysis\gpu_npu_run_sync_code_refactor_$Stamp.md"
```

Build post-validation AI packet context:

```powershell
$ContextFiles = @(
  ".\docs\LOCAL_AI_TASKS\code-refactor-0-to-10-procedure.md",
  ".\docs\LOCAL_AI_TASKS\next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md",
  ".\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md",
  ".\Tools\ai\code_patch_plan_common.py",
  ".\Tools\ai\code_edit_proposal_helpers.py",
  ".\Tools\ai\build_agent_review_code_patch_plan.py",
  ".\Tools\validation\build_python_line_count_csv.py",
  $LineCountAllMd,
  ".\output\validation\python_line_count_refactor_large_code_$Stamp.md",
  ".\output\analysis\code_interpreter_code_refactor_$Stamp.md",
  ".\output\analysis\gpu_json_contract_replay_code_refactor_$Stamp.md",
  ".\output\analysis\gpu_npu_run_sync_code_refactor_$Stamp.md"
)

$ReportFiles = @(
  $OrchOut,
  $GpuOut,
  ".\output\validation\python_syntax_code_refactor_$Stamp.json",
  ".\output\validation\python_line_count_refactor_large_code_$Stamp.json",
  ".\output\analysis\code_interpreter_code_refactor_$Stamp.json",
  ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json",
  ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json",
  ".\output\analysis\gpu_json_contract_replay_code_refactor_$Stamp.json",
  ".\output\analysis\gpu_npu_run_sync_code_refactor_$Stamp.json"
)

$params = @{
  Profile     = "core"
  ContextFile = $ContextFiles
  ReportFile  = $ReportFiles
}

& .\Tools\workflow\run_post_validation_ai_packet.ps1 @params
```

Manual-review code patch-plan lane, when a code-contract/refactor report is available:

```powershell
python .\Tools\ai\build_agent_review_code_patch_plan.py `
  --repo-root . `
  --code-contract-drift-report .\output\ai_pipeline\repository_change_proposals.json `
  --line-count-csv $LineCountCsv `
  --output ".\output\patch_specs\agent_review_code_patch_plan_code_refactor_$Stamp.json" `
  --markdown-output ".\output\patch_specs\agent_review_code_patch_plan_code_refactor_$Stamp.md"
```

Validate code patch-plan if generated:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report ".\output\patch_specs\agent_review_code_patch_plan_code_refactor_$Stamp.json" `
  --output ".\output\validation\agent_review_code_patch_plan_smoke_code_refactor_$Stamp.json"
```

If the code patch-plan builder does not have suitable input yet, do not fake a plan. Use the full run/replay/sync/line-count evidence bundle as the result and make the next recommended step explicit.

## 10. Build compact evidence bundle, validate, commit safely

Collect reports:

```powershell
$Reports = @(
  ".\output\validation\python_syntax_code_refactor_$Stamp.json",
  ".\output\validation\python_line_count_refactor_large_code_$Stamp.json",
  ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json",
  ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json",
  ".\output\analysis\code_interpreter_code_refactor_$Stamp.json",
  $OrchOut,
  $GpuOut,
  ".\output\analysis\gpu_json_contract_replay_code_refactor_$Stamp.json",
  ".\output\analysis\gpu_npu_run_sync_code_refactor_$Stamp.json",
  ".\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json",
  ".\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json",
  ".\output\ai_pipeline\repository_change_proposals.json",
  ".\output\patch_specs\agent_review_code_patch_plan_code_refactor_$Stamp.json",
  ".\output\validation\agent_review_code_patch_plan_smoke_code_refactor_$Stamp.json"
) | Where-Object { Test-Path $_ }
```

Build bundle:

```powershell
python -m Tools.ai.build_github_evidence_bundle `
  --repo-root . `
  --basename code_refactor_ai_to_ai_bundle_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',') `
  --artifact ".\docs\LOCAL_AI_TASKS\code-refactor-0-to-10-procedure.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md" `
  --artifact ".\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md" `
  --artifact $LineCountAllMd `
  --artifact $LineCountCsv `
  --artifact ".\output\validation\python_line_count_refactor_large_code_$Stamp.md" `
  --artifact ".\output\analysis\code_interpreter_code_refactor_$Stamp.md" `
  --artifact ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_orchestrator.md" `
  --artifact ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_parallel_gpu.md" `
  --artifact ".\output\analysis\gpu_json_contract_replay_code_refactor_$Stamp.md" `
  --artifact ".\output\analysis\gpu_npu_run_sync_code_refactor_$Stamp.md" `
  --artifact ".\output\patch_specs\agent_review_code_patch_plan_code_refactor_$Stamp.md" `
  --max-included-artifact-chars 16000 `
  --max-included-artifacts 20
```

Validate bundle:

```powershell
python -m Tools.validation.check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\code_refactor_ai_to_ai_bundle_$Stamp.json" `
  --output ".\output\validation\code_refactor_ai_to_ai_bundle_${Stamp}_validation.json"

Get-Content ".\output\validation\code_refactor_ai_to_ai_bundle_${Stamp}_validation.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```

Final checks:

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_code_refactor_final_$Stamp.json"

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output ".\output\validation\validation_report_contract_code_refactor_final_$Stamp.json"

git diff --check
git status --short
```

Commit only compact Git-trackable evidence:

```powershell
git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\code_refactor_ai_to_ai_bundle_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\code_refactor_ai_to_ai_bundle_$Stamp.md"
```

Optionally add line-count CSV only if it is referenced by the bundle and needed for the decision:

```powershell
git add $LineCountCsv
```

Check staged files:

```powershell
git diff --cached --name-only
```

Must not include:

```text
output/**
renders/**
*.db
*.sqlite
```

Commit and push branch/PR, not direct to master unless explicitly requested:

```powershell
git commit -m "test(ai): add code refactor AI-to-AI evidence bundle"
git push -u origin codex/code-refactor-ai-to-ai-evidence
```

Open PR:

```powershell
gh pr create `
  --repo C-F-tek/blender-audio-project `
  --base master `
  --head codex/code-refactor-ai-to-ai-evidence `
  --title "test(ai): add code refactor AI-to-AI evidence bundle" `
  --body "Adds compact report-only evidence for the post-PR115 code refactor review. Includes full Python line-count inventory, GPU/NPU diagnostics, replay/sync reports, and guardrail-preserving bundle. No output/** artifacts committed."
```

---

# Refactor implementation phase after evidence

Do not implement code refactors automatically from the run.

When the user chooses one manual-review plan, create a focused implementation PR:

```text
one refactor seam per PR
small target set
preserve CLI/report schema
add or update smoke validation
include line counts for any touched code/script file
commit compact evidence only
```

For each implementation PR, report resulting line counts for touched code/script files.

## Fast summary command after code refactor run

```powershell
@{
  Stamp = $Stamp
  LineCount = (Get-Content ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" -Raw | ConvertFrom-Json |
    Select-Object passed, file_count, total_lines, csv_written)
  Orchestrator = (Get-Content ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_orchestrator.json" -Raw | ConvertFrom-Json |
    Select-Object passed, elapsed_seconds, gpu_recommendation_count, gpu_empty_recommendations_reason, npu_audit_count, npu_audit_success_count)
  GPU = (Get-Content ".\output\ai_pipeline\code_refactor_balanced_${Stamp}_parallel_gpu.json" -Raw | ConvertFrom-Json |
    Select-Object round_count, recommendation_count, empty_recommendations_reason, context_echo_detected_count, json_parse_error_count, model_output_schema_mismatch_count, evidence_ready_for_manual_patch_count)
  Replay = (Get-Content ".\output\analysis\gpu_json_contract_replay_code_refactor_$Stamp.json" -Raw | ConvertFrom-Json |
    Select-Object replayed_round_count, context_echo_detected_count, json_parse_failure_count, model_output_schema_mismatch_count, valid_recommendation_output_count)
  Sync = (Get-Content ".\output\analysis\gpu_npu_run_sync_code_refactor_$Stamp.json" -Raw | ConvertFrom-Json).metrics
} | ConvertTo-Json -Depth 6
```

## Short prompt to start a future refactor chat

```text
Leggi integralmente `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md`.

Repository: C-F-tek/blender-audio-project.
Branch: master.
Project: IA-Carmine.

Avvia il ciclo 0 -> 10 di refactoring codice descritto nella guida.
Prima della run completa genera il CSV line-count con `Tools/validation/build_python_line_count_csv.py` e un Markdown completo, non troncato, di tutti i file Python presenti nel CSV.
Leggi repo, tool e MD di riferimento: esistono helper già scritti/fattorizzati.
Valuta riuso/promozione di funzioni già fattorizzate o fattorizzabili da altre parti del tool.
Non limitare la review ai primi 10 o 20 file più densi: usa tutto l'inventario Python e lascia decidere al planner/refactor layer.
Non fare refactor legacy/archive/old/backup/bak fuori dal template `Scripting/v61b` non-backup.
Non cambiare provider/model settings.
Non fare prompt rewriting se non richiesto.
Non applicare patch automaticamente.
Dopo ogni modifica prepara comandi locali di validazione e bundle compatto secondo la policy evidence.
Quando tocchi codice/script, indica sempre il numero di righe risultante.
```
