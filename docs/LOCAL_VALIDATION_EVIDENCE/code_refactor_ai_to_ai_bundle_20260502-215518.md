# Local Validation Evidence Bundle

- Generated at: `2026-05-02T22:05:10`
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
- `included_artifact_count`: `15`
- `patch_plan_summary_seen`: `False`

## Reports

### `output/validation/python_syntax_code_refactor_20260502-215518.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/python_line_count_refactor_large_code_20260502-215518.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/npu_provider_environment_code_refactor_20260502-215518.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/gpu_planner_json_contract_smoke_code_refactor_20260502-215518.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_code_refactor_20260502-215518.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `115`

### `output/ai_pipeline/code_refactor_balanced_20260502-215518_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/code_refactor_balanced_20260502-215518_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `build_agent_review_patch_plan.py`

### `output/analysis/gpu_json_contract_replay_code_refactor_20260502-215518.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_code_refactor_20260502-215518.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Artifact manifest

- `output/validation/python_syntax_code_refactor_20260502-215518.json` exists=`True` size=`32226` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_refactor_large_code_20260502-215518.json` exists=`True` size=`3091` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_provider_environment_code_refactor_20260502-215518.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_code_refactor_20260502-215518.json` exists=`True` size=`3635` suffix=`.json` preview_chars=`1500`
- `output/analysis/code_interpreter_code_refactor_20260502-215518.json` exists=`True` size=`1169640` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/code_refactor_balanced_20260502-215518_orchestrator.json` exists=`True` size=`13759` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/code_refactor_balanced_20260502-215518_parallel_gpu.json` exists=`True` size=`121288` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_code_refactor_20260502-215518.json` exists=`True` size=`20229` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_code_refactor_20260502-215518.json` exists=`True` size=`2545` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `26467`
- SHA-256: `27057acf7f00d1a3c2b209aeb7bf6f2704d584130eb132f4c71cf56fa3f6d480`
- Content included: `True`
- Content truncated: `True`

```text
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
source_writes_
```

### `docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `14406`
- SHA-256: `64d94880d16b07ca14449ddde8c8a75c1e4ed8541277096eda104d8161588302`
- Content included: `True`
- Content truncated: `False`

```text
# Next Chat Handoff After PR115 — Full Python Inventory Refactor Review — 2026-05-02

## Purpose

Use this Markdown file as the first context document for the next local/GitHub AI session.

This is the post-PR115 entry handoff for testing the newly wired GPU planner JSON contract diagnostics and using them to drive a refactor-oriented review of Python code across the repository.

The run is still report-only unless the user explicitly asks to apply a specific manual patch plan.

## Repository baseline

```text
repository: C-F-tek/blender-audio-project
branch to sync: master
project: IA-Carmine
workflow: local validation + GitHub/API PRs
```

Already merged into `master`:

```text
PR #109: docs(ai): design manual-review code patch plan lane
PR #111: feat(ai): surface GPU repair-failure recommendations
PR #112: feat(ai): harden GPU planner JSON contract
PR #113: feat(ai): analyze GPU/NPU run sync and balanced profile
PR #114: feat(ai): replay GPU planner JSON contract on real outputs
PR #115: feat(ai): wire GPU planner JSON contract into runner diagnostics
```

Latest relevant master commit after PR #115:

```text
56bb6b0 feat(ai): wire GPU planner JSON contract into runner diagnostics
```

PR #115 changed the real GPU runner diagnostic path so future reports should prefer the shared contract classifiers:

```text
context_echo_detected
json_parse_failure
model_output_schema_mismatch
recommendations_filtered_out
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

Do not collapse post-PR115 failures back to the old generic `repair_attempt_failed` unless reading old pre-PR115 reports.

## Immediate next objective

Next evidence-backed PR title, if the run supports it:

```text
refactor(ai): split largest Python modules by full line-count evidence
```

Primary objective:

```text
Run the balanced post-PR115 complete review and make the AI see the complete Python file inventory, not only a top-N subset.
```

The AI must decide the actual refactor candidates from all counted Python files. Line count is evidence and prioritization, not a visibility filter.

## Mandatory repository/tool discovery before planning

Before proposing refactor plans, read the repository and reuse existing tools and docs. Do not reinvent helpers that already exist.

Required tool/doc anchors to inspect:

```text
AGENTS.md
docs/AGENT_REVIEW_CODE_PATCH_PLAN.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-review-request.md
docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-procedure.md
docs/LOCAL_AI_TASKS/gpu-npu-balanced-run-profile.md
docs/LOCAL_AI_TASKS/post-pr114-next-task-handoff.md
docs/LOCAL_AI_TASKS/next-chat-handoff-after-balanced-full-run-2026-05-02.md
docs/LOCAL_VALIDATION_EVIDENCE/README.md
Tools/ai/code_patch_plan_common.py
Tools/ai/code_edit_proposal_helpers.py
Tools/ai/build_agent_review_code_patch_plan.py
Tools/ai/build_code_edit_proposal_from_plan.py
Tools/ai/build_code_interpreter_report.py
Tools/ai/build_github_evidence_bundle.py
Tools/validation/build_python_line_count_csv.py
Tools/validation/run_agent_review_code_patch_plan_smoke.py
Tools/validation/check_python_syntax.py
Tools/validation/check_validation_report_contract.py
```

If a helper already exists, prefer reuse, extraction, or promotion over duplication.

## Function/helper promotion rule

During refactor review, explicitly evaluate whether functions should be promoted to reusable shared helpers.

Promote or reuse when a function/helper is:

```text
- already duplicated across Tools/ai, Tools/validation, Tools/workflow, or Tools/npu
- generic report-only plumbing: path normalization, JSON read/write, Markdown rendering, guardrails, compacting values, validation command lists
- useful for more than one tool lane
- side-effect-light and safe under project guardrails
```

Preferred promotion targets:

```text
Tools/ai/code_patch_plan_common.py
Tools/validation/report_utils.py
existing local helper modules in Tools/ai or Tools/validation
```

Do not create a new helper module if an existing shared module is a better fit.

A valid refactor plan should say one of:

```text
reuse_existing_helper
promote_existing_function
extract_new_shared_helper
keep_local_by_design
```

and justify the choice.

## Required pre-run full Python line-count evidence

Use the existing deterministic tool:

```text
Tools/validation/build_python_line_count_csv.py
```

This tool is report-only. It reads Python files and writes CSV/JSON/MD evidence. It does not execute providers, run Blender, apply patches, or modify source code except explicit output/evidence artifacts.

Run it before code interpreter and before the GPU/NPU orchestrator:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$env:PYTHONPATH = (Get-Location).Path

python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
  --markdown-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.md"
```

The JSON report contains summary/top metadata. The CSV contains the complete Python file inventory. Do not rely only on `top_files` from JSON.

Resolve the exact CSV path from the report:

```powershell
$LineCountReport = Get-Content ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" -Raw | ConvertFrom-Json
$LineCountCsv = $LineCountReport.csv_written
"LINE_COUNT_CSV=$LineCountCsv"
```

Create an untruncated Markdown view of every counted Python file from the CSV:

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

The full Markdown list is intentionally complete. If terminal output is long, the authoritative artifact is still `$LineCountAllMd`; do not summarize it to only top files.

## Refactor decision rule

The AI must inspect all Python files from `$LineCountAllMd` / `$LineCountCsv` and decide candidates.

Prioritization hints, not filters:

```text
- files with >= 400 physical lines
- files near the top of the full CSV ranking
- scripts with high orchestration/parsing/rendering coupling
- files already involved in AI tooling, validation, workflow, NPU/GPU orchestration, or Scripting/v61b template work
- functions that can become shared primitives for other tools
```

The AI may choose files below 400 lines if evidence shows strong duplication/coupling/reuse potential, but must justify why.

The AI must not claim it saw only the first 10 or first 20 files. It must treat the complete CSV/Markdown inventory as the available Python source list.

## Large-code refactor scope

Preferred refactor types:

```text
- extract pure helpers into existing package/module boundaries
- split orchestration from parsing/validation/report rendering
- move duplicated guardrail/report utilities into shared helpers
- promote already-factored helpers for reuse by other tool lanes
- reduce long functions while preserving CLI/output schema compatibility
- add focused validation/smoke tests for refactored seams
```

Do not request broad rewrites. Generate small manual-review patch plans with explicit target files, validation commands, and stop conditions.

## Legacy/refactor exclusion rule

Do not refactor legacy/archive/old/backup code by default.

Strict rule:

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

Allowed template examples:

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

If the GPU/NPU/post-validation layers identify a valuable legacy issue outside the allowed `Scripting/v61b` non-backup template lane, classify it as `advisory_only` or `needs_more_context`, not `ready_for_patch_plan`.

## Full balanced run parameters

Use the post-PR113 balanced profile. Do not increase token budget before seeing post-PR115 diagnostics.

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

Add the line-count JSON as an explicit report file to the orchestrator:

```powershell
--report-file ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
```

Add the full line-count Markdown as a context root so the GPU runner can read the complete Python file list as text:

```powershell
--context-root $LineCountAllMd `
```

Also include normal code/doc roots:

```powershell
--context-root docs `
--context-root Tools\ai `
--context-root Tools\validation `
--context-root Tools\workflow `
--context-root Tools\npu `
--context-root Scripting\v61b `
--context-root Scripting\shared `
```

## Context files for post-validation AI packet

Include this handoff, relevant docs, shared helper files, and the complete line-count Markdown in `$ContextFiles`:

```powershell
".\docs\LOCAL_AI_TASKS\next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md",
".\docs\AGENT_REVIEW_CODE_PATCH_PLAN.md",
".\Tools\ai\code_patch_plan_common.py",
".\Tools\ai\code_edit_proposal_helpers.py",
".\Tools\validation\build_python_line_count_csv.py",
$LineCountAllMd,
".\output\validation\python_line_count_refactor_large_code_$Stamp.md",
```

Include the line-count JSON in `$ReportFiles`:

```powershell
".\output\validation\python_line_count_refactor_large_code_$Stamp.json",
```

## Final evidence bundle inputs

The compact bundle should include the complete line-count inventory as an artifact, not only the summary JSON:

```powershell
--report ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
--artifact $LineCountAllMd `
--artifact $LineCountCsv `
```

If the exact CSV name differs because the tool generated its own timestamp from `now_iso()`, always use `$LineCountCsv` from the JSON report.

## Expected post-PR115 comparison

After the run, compare these metrics against the previous balanced run:

```text
gpu_empty_recommendations_reason
context_echo_detected_count
json_parse_failure_count
model_output_schema_mismatch_count
valid_recommendation_output_count
fallback_patch_plan_count
npu_audit_round_coverage
npu_to_gpu_avg_duration_ratio
```

Expected diagnostic improvement:

```text
The top-level GPU empty recommendation reason should no longer collapse to repair_attempt_failed when the shared contract can classify the actual failure mode.
```

A successful diagnostic-only outcome can still have:

```text
gpu_recommendation_count=0
fallback_patch_plan_count>0
manual_review_required=true
patch_application_performed=false
source_writes_performed=false
```

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
no automatic patch application
no Blender runtime execution
no SQLite/database commit
no raw output/** commit
no full analysis JSON commit outside compact evidence bundle
no NPU advisory promotion
no OpenVINO GPU primary lane
manual review required for patch plans
```

Refactor-specific guardrails:

```text
no legacy/archive/old/backup/bak refactor plans as ready_for_patch_plan
except Scripting/v61b non-backup template files
no broad rewrite of large files in one PR
no provider/model setting changes during refactor PRs unless explicitly requested
preserve CLI arguments and report schemas unless a migration plan is explicit
prefer reuse/promotion of existing helpers over new duplication
```

## Commit policy

For the full validation run:

```text
commit the smallest bundle that proves the decision
```

Allowed to commit:

```text
docs/LOCAL_VALIDATION_EVIDENCE/<compact_bundle>.json
docs/LOCAL_VALIDATION_EVIDENCE/<compact_bundle>.md
optional docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_<timestamp>.csv if it is referenced by the bundle and needed for the refactor decision
```

Do not commit:

```text
output/**
renders/**
*.db
*.sqlite
full_analysis*.json
*analysis_full*.json
```

## Short prompt for next chat

```text
Leggi integralmente `docs/LOCAL_AI_TASKS/next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md`.

Repository: C-F-tek/blender-audio-project.
Branch: master.
Project: IA-Carmine.

Riprendi esattamente dallo stato descritto nel file.
Prima della run completa esegui `Tools/validation/build_python_line_count_csv.py` e produci anche un Markdown completo, non troncato, con tutti i file Python presenti nel CSV.
Leggi la repo: ci sono tool e helper già scritti/fattorizzati. Usa gli MD di riferimento per approfondire prima di proporre nuovi refactor.
Valuta la promozione o il riuso di funzioni già fattorizzate o fattorizzabili da altre parti del tool.
Non limitare la review ai primi 10 o 20 file più densi: usa tutto l'inventario Python e lascia decidere al planner/refactor layer.
Non fare refactor legacy/archive/old/backup/bak fuori dal template `Scripting/v61b` non-backup.
Non cambiare provider/model settings.
Non fare prompt rewriting se non richiesto.
Non applicare patch automaticamente.
Dopo ogni modifica prepara comandi locali di validazione e bundle compatto secondo la policy evidence.
```

```

### `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `12430`
- SHA-256: `761012517b6af20afb6bb9d65fceaeeacbffe4895b459bd4d0bdba9168653678`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Code Patch Plan

## Purpose

This document defines the report-only lane for turning repository review evidence into safe, manual-review code patch plans.

The goal is to extend the current documentation patch-plan workflow toward code editing without enabling automatic source mutation.

This lane may describe code edits and related documentation follow-up work. It must not apply either code or documentation patches automatically.

## Relationship to existing lanes

Existing documentation patch-plan lane:

```text
local evidence / review reports
  -> Tools/ai/build_agent_review_patch_plan.py
  -> output/patch_specs/agent_review_patch_plan.json
  -> Tools/validation/run_agent_review_patch_plan_smoke.py
  -> manual-review documentation edits
  -> Git-trackable evidence bundle
```

Code patch-plan lane:

```text
code_contract_drift report
  -> Tools/ai/build_agent_review_code_patch_plan.py
  -> output/patch_specs/agent_review_code_patch_plan.json
  -> Tools/validation/run_agent_review_code_patch_plan_smoke.py
  -> manual review
  -> optional small hand-applied code PR
```

Complete code edit proposal helper:

```text
manual-review code patch plan item
  -> Tools/ai/code_edit_proposal_helpers.py
  -> code_edit_proposal metadata
  -> validators + stop conditions
  -> human applies or rejects the edit in a separate implementation step
```

Documentation follow-up bridge:

```text
agent_review_code_patch_plan report
  -> Tools/ai/build_code_patch_docs_followup.py
  -> output/patch_specs/agent_review_code_docs_followup.json
  -> manual-review documentation queue
```

The bridge lets code-plan output notify the documentation lane. It is not an apply queue.

## Required default behavior

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
apply_mode = report_only_manual_review_code_patch_plan
```

For complete code edit proposals:

```text
kind = code_edit_proposal
apply_mode = report_only_manual_review_code_edit_proposal
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
```

For docs follow-up reports:

```text
kind = agent_review_code_docs_followup
apply_mode = report_only_manual_review_docs_followup
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
```

A report that violates these defaults should fail validation unless the task explicitly authorizes a later, separate reviewed implementation phase.

## JSON report shape

```json
{
  "schema_version": 1,
  "kind": "agent_review_code_patch_plan",
  "passed": true,
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_manual_review_code_patch_plan",
  "manual_review_required": true,
  "patch_plan_count": 0,
  "code_patch_plans": [],
  "errors": [],
  "warnings": []
}
```

Each `code_patch_plans[]` item should be small and reviewable:

```json
{
  "id": "code_patch_001",
  "area": "validation",
  "risk": "low",
  "status": "ready_for_manual_review",
  "target_files": ["Tools/validation/example.py"],
  "rationale": "Why the edit is needed.",
  "edit_strategy": "How the edit should be made.",
  "proposed_patch": "optional bounded preview only",
  "validation_commands": [
    "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
    "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
    "git diff --check"
  ],
  "stop_conditions": [
    "Stop if the target file does not exist unless the task explicitly authorizes a new source file.",
    "Stop if the patch touches output/**.",
    "Stop if validation fails.",
    "Stop if Blender runtime execution is required."
  ],
  "manual_review_required": true
}
```

## Complete code edit proposal helper

Helper:

```text
Tools/ai/code_edit_proposal_helpers.py
```

This helper is the first coding-complete primitive for the code-editor lane. It does not apply edits. It builds a complete proposal object containing:

```text
target path
target metadata: exists, suffix, line_count, sha256
edit kind: no_op, structured_edit, unified_diff
bounded unified diff preview
structured operations
rationale
edit strategy
validation commands
stop conditions
manual review status
```

Supported edit kinds:

```text
no_op
structured_edit
unified_diff
```

Supported structured operations:

```text
replace
insert_after
insert_before
delete
append
```

A complete proposal must remain metadata-only:

```text
source_writes_performed = false
patch_application_performed = false
provider_execution_performed = false
```

The helper validates that target files do not escape the repository, do not target blocked artifacts, and include validators. For Python targets it automatically adds:

```powershell
python -m py_compile .\<target-file>
```

alongside repository validators:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

A unified-diff proposal must reference the normalized target file and include standard diff markers:

```text
---
+++
@@
```

The helper rejects or flags proposals that mention blocked fragments such as:

```text
output/
renders/
.sqlite
.db
full_analysis
analysis_full
```

## Builder, fixtures and smoke validator

Builder:

```text
Tools/ai/build_agent_review_code_patch_plan.py
```

Fixture inputs:

```text
Tools/ai/fixtures/code_contract_drift_fixture.json
Tools/ai/fixtures/agent_review_code_patch_plan_fixture.json
```

Smoke validator:

```text
Tools/validation/run_agent_review_code_patch_plan_smoke.py
```

Build from fixture:

```powershell
python .\Tools\ai\build_agent_review_code_patch_plan.py `
  --repo-root . `
  --code-contract-drift-report .\Tools\ai\fixtures\code_contract_drift_fixture.json `
  --output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --markdown-output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.md
```

Validate fixture report:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\Tools\ai\fixtures\agent_review_code_patch_plan_fixture.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke.json
```

Validate generated report:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_built.json
```

The builder and smoke validator preserve:

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

They do not apply patches, run providers, run Blender or write source files.

## Documentation follow-up bridge

When a code patch plan proposes code changes, the docs follow-up bridge emits a related documentation review queue.

Bridge:

```text
Tools/ai/build_code_patch_docs_followup.py
```

Run:

```powershell
python .\Tools\ai\build_code_patch_docs_followup.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\patch_specs\agent_review_code_docs_followup.json `
  --markdown-output .\output\patch_specs\agent_review_code_docs_followup.md
```

The bridge maps code target areas to likely documentation surfaces, for example:

| Code area/path | Candidate docs |
|---|---|
| `Tools/validation/**` | `Tools/validation/README.md`, `docs/JSON_SCHEMAS.md`, `docs/CONTRACT_DRIFT_VALIDATION.md` |
| `Tools/workflow/**` | `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md`, `docs/LOCAL_AI_TASKS/README.md`, `WORKFLOW.md` |
| `Tools/ai/**` | `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md`, `docs/JSON_SCHEMAS.md`, `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md` |
| `Tools/npu/**` | `docs/LOCAL_AI_WORKFLOW.md`, `docs/LOCAL_WORKSTATION_TARGET.md`, `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md` |

Docs follow-up suggestions remain manual-review-only. They should be reviewed after the related code patch plan is accepted or materially changed.

## Allowed targets

A code patch plan may target source files only when all conditions hold:

```text
file exists, unless the task explicitly authorizes a new source file
file is not under output/**
file is not generated index content
file is not full analysis JSON
file is not a SQLite/database artifact
edit is small and target-specific
validation commands are listed
stop conditions are explicit
```

## Blocked targets

The code patch-plan lane must reject or mark blocked any plan touching:

```text
output/**
*.db
*.sqlite
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
full_analysis*.json
*analysis_full*.json
Blender runtime execution paths without explicit runtime task scope
provider credentials, secrets, billing, permissions or repository visibility
```

## Smoke validator expectations

The smoke validator checks:

```text
kind == agent_review_code_patch_plan
apply_mode == report_only_manual_review_code_patch_plan
manual_review_required == true
provider_execution_performed == false
patch_application_performed == false
source_writes_performed == false
patch_plan_count == len(code_patch_plans)
all target files are allowed or explicitly declared future/new-file candidates
all plans include validation_commands and stop_conditions
no forbidden path appears in target_files or proposed_patch metadata
```

The smoke validator must not:

```text
apply patches
run providers
run Blender
write source files
read ignored output/** reports unless explicitly supplied as input evidence
```

## Evidence bundle integration

The existing evidence bundle builder should summarize code patch-plan and docs follow-up reports in the same compact style used for documentation patch plans.

Recommended code-plan summary fields:

```text
patch_plan_count
manual_review_required
provider_execution_performed
patch_application_performed
source_writes_performed
plans[].id
plans[].area
plans[].risk
plans[].status
plans[].target_files
plans[].rationale
plans[].edit_strategy
plans[].validation_commands
plans[].stop_conditions
```

Recommended code edit proposal summary fields:

```text
id
target_file
edit_kind
manual_review_required
ready_for_manual_review
target_sha256
target_line_count
rationale
edit_strategy
validation_commands
stop_conditions
```

Recommended docs-follow-up summary fields:

```text
docs_followup_count
manual_review_required
provider_execution_performed
patch_application_performed
source_writes_performed
suggestions[].id
suggestions[].source_code_patch_plan_id
suggestions[].target_files
suggestions[].rationale
suggestions[].edit_strategy
```

The bundle may include `proposed_patch` only as a bounded preview. Full raw artifacts should remain local unless they are deliberately small, reviewed and Git-trackable.

## Line-count evidence usage

Use `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv` as a sizing hint before prioritizing code patch plans.

Large files require narrower patch scope. The CSV is useful but may be stale, so always inspect current file content before generating or applying any code patch.

## Guardrails

This lane must remain:

```text
report-only by default
manual-review-only
provider-free unless a separate explicit evidence step already ran
patch-application-free
source-write-free until a human-approved implementation phase
Blender-runtime-free
NPU advisory promotion-free
OpenVINO GPU primary-lane-free
```

## Recommended next implementation sequence

```text
1. Run code_contract_drift.
2. Build agent_review_code_patch_plan from the drift report.
3. Validate the code patch plan with run_agent_review_code_patch_plan_smoke.py.
4. Optionally build complete code_edit_proposal metadata for selected plan items.
5. Build agent_review_code_docs_followup from the code patch plan.
6. Review code and docs queues together.
7. Only then consider a separate hand-applied code/docs PR generated from reviewed plans.
```

```

### `output/validation/python_line_count_all_python_files_20260502-215518.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `15527`
- SHA-256: `c0b60c23ddad21bdef6c63178ac80fbd3fb808f85604dc0de12603d72733601c`
- Content included: `True`
- Content truncated: `False`

```text
# Full Python Line Count Inventory

- Stamp: `20260502-215518`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260502-215526.csv`
- File count: `277`
- Total Python lines: `77731`
- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20.

| Lines | File |
|---:|---|
| 2197 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` |
| 1773 | `Tools/npu/run_dual_ai_pipeline.py` |
| 1513 | `old script legacy/spaziotempo_asset_visual_v61.py` |
| 1262 | `Scripting/v61b/scene_tuning_panel.py` |
| 1230 | `Tools/workflow/workflow_state.py` |
| 1174 | `old script legacy/spaziotempo_asset_visual_v6.py` |
| 1097 | `Scripting/v61b_backgood/scene_tuning_panel.py` |
| 1079 | `Scripting/v61b/animation.py` |
| 1019 | `Scripting/v61b_backgood/animation.py` |
| 969 | `old script legacy/spaziotempo_album_visual_v5.py` |
| 738 | `Tools/workflow/gui/workflow_gui.py` |
| 737 | `Scripting/v61b/physics_setup.py` |
| 729 | `Tools/ai/run_agent_gpu_deep_planning_review.py` |
| 725 | `Scripting/v61b_backgood/asset_setup.py` |
| 725 | `Scripting/v61b/asset_setup.py` |
| 720 | `Scripting/v61b_backgood/physics_setup.py` |
| 711 | `Tools/npu/build_music_context.py` |
| 710 | `old script legacy/spaziotempo_album_visual_v3.py` |
| 657 | `Scripting/v61b/materials.py` |
| 628 | `Tools/npu/run_npu_review.py` |
| 627 | `Tools/validation/check_npu_pipeline_modules.py` |
| 618 | `Tools/ai/build_selective_execution_plan.py` |
| 607 | `Tools/workflow/workflow_debug.py` |
| 582 | `Tools/ai/build_repository_change_proposals.py` |
| 575 | `Tools/ai/build_ai_context_pack.py` |
| 573 | `Tools/ai/run_pipeline_dry_run_matrix.py` |
| 562 | `Tools/ai/build_agent_review_patch_plan.py` |
| 554 | `Scripting/v61b/atmosphere_setup.py` |
| 551 | `Tools/ai/suggest_repository_updates.py` |
| 544 | `Tools/ai/agent_state.py` |
| 543 | `Scripting/v61b_backgood/atmosphere_setup.py` |
| 519 | `Tools/ai/run_megalithic_repo_review.py` |
| 513 | `Scripting/v61b_backgood/materials.py` |
| 499 | `Tools/ai/build_agent_review_code_patch_plan.py` |
| 497 | `Tools/validation/ai_pipeline_report_contracts.py` |
| 490 | `Tools/npu/npu_guardrail_service.py` |
| 489 | `Tools/ai/refine_megalithic_review_signals.py` |
| 487 | `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| 483 | `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` |
| 478 | `Tools/ai/run_agent_gpu_deep_planning_supervised.py` |
| 471 | `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` |
| 469 | `normalize_scene_spec.py` |
| 446 | `Tools/validation/check_reviewed_patch_specs.py` |
| 443 | `Tools/repo_patch_runner/apply_repo_mods.py` |
| 442 | `Tools/ai/promote_patch_spec_draft.py` |
| 439 | `Scripting/v61b/config.py` |
| 437 | `Tools/ai/build_code_interpreter_report.py` |
| 436 | `Tools/npu/build_project_ai_index.py` |
| 425 | `Tools/validation/check_ai_context_pack_contract.py` |
| 422 | `Tools/workflow/gui/components/storage_dashboard.py` |
| 422 | `Tools/npu/ollama_runtime.py` |
| 419 | `Tools/workflow/scene_brief.py` |
| 414 | `Tools/ai/build_patch_specs_from_proposals.py` |
| 411 | `Tools/ai/run_npu_gpu_deep_review_auditor.py` |
| 408 | `Tools/ai/build_agent_agnostic_tool_inventory.py` |
| 402 | `Tools/npu/build_npu_code_context.py` |
| 401 | `Tools/validation/check_github_evidence_bundle.py` |
| 400 | `Tools/validation/check_patch_spec_drafts.py` |
| 399 | `Scripting/v61b/encode_ffmpeg_v61b.py` |
| 398 | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` |
| 397 | `Tools/ai/build_agent_memory_inventory.py` |
| 395 | `Scripting/v61b_backgood/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/encode_image_sequence_v61b.py` |
| 394 | `Tools/ai/build_agent_review_evidence_sufficiency.py` |
| 392 | `Tools/validation/check_code_contract_drift.py` |
| 392 | `Tools/ai/build_full_context_golden_proposals.py` |
| 392 | `Scripting/v61b/fog_dynamics.py` |
| 390 | `Tools/workflow/gui/components/artifact_browser.py` |
| 376 | `Scripting/v61b_backgood/encode_image_sequence_v61b.py` |
| 369 | `Tools/npu/generated_blender_script_candidate_FristNear.py` |
| 369 | `Tools/npu/generated_blender_script_candidate.py` |
| 369 | `indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py` |
| 366 | `Tools/validation/check_repository_change_proposals.py` |
| 359 | `Tools/validation/test_npu_pipeline_helpers.py` |
| 358 | `Scripting/v61b_backgood/config.py` |
| 357 | `Tools/ai/build_local_ai_enrichment_plan.py` |
| 355 | `Tools/npu/build_ai_service_packet.py` |
| 353 | `Tools/workflow/project_awareness.py` |
| 341 | `Tools/validation/check_ai_dry_run_matrix_contract.py` |
| 339 | `Tools/validation/check_selected_semantic_chunks.py` |
| 335 | `Tools/ai/check_local_resource_lanes.py` |
| 331 | `Tools/validation/apply_docs_contract_drift_fixes.py` |
| 327 | `Tools/npu/build_npu_knowledge_broker_packet.py` |
| 326 | `Tools/npu/build_blender_manual_context.py` |
| 324 | `Tools/workflow/workflow_shell.py` |
| 321 | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` |
| 319 | `Tools/workflow/gui/workflow_gui_modern.py` |
| 317 | `Tools/validation/check_local_ai_adapter_manifest.py` |
| 314 | `Tools/ai/run_npu_decode_smoke_diagnostic.py` |
| 314 | `Tools/ai/build_music_intermediates.py` |
| 307 | `Tools/validation/check_full_context_golden_proposals.py` |
| 307 | `Tools/ai/agent_memory_policy.py` |
| 304 | `Tools/ai/build_analysis_input_bundle.py` |
| 302 | `Tools/ai/gpu_planner_json_contract.py` |
| 301 | `Scripting/v61b/hotpatch/accent_patch.py` |
| 297 | `Tools/npu/pipeline/providers.py` |
| 291 | `Tools/ai/select_semantic_code_chunks.py` |
| 290 | `Tools/validation/check_ai_pipeline_modules.py` |
| 286 | `Tools/ai/build_gpu_repair_failure_recommendation.py` |
| 286 | `Scripting/v61b/hotpatch/diagnostics.py` |
| 284 | `Tools/workflow/startup_check.py` |
| 283 | `Tools/validation/run_agent_review_patch_plan_smoke.py` |
| 283 | `Tools/ai/build_agent_transient_request_context.py` |
| 278 | `Tools/workflow/gui/components/session_overview.py` |
| 273 | `Tools/ai/analyze_gpu_npu_run_sync.py` |
| 270 | `Tools/validation/check_full_context_golden_docs_contract.py` |
| 270 | `Scripting/v61b/render_setup.py` |
| 267 | `Tools/workflow/ai_runtime_diagnostics.py` |
| 267 | `Scripting/v61b_backgood/render_setup.py` |
| 266 | `Tools/ai/build_code_patch_docs_followup.py` |
| 260 | `Tools/validation/check_ai_workload_report_quality.py` |
| 259 | `Tools/validation/check_docs_contract_drift.py` |
| 258 | `Tools/ai/build_code_patch_artifact_pack.py` |
| 257 | `analyze_wav.py` |
| 256 | `Tools/validation/run_agnostic_context_stack_smoke.py` |
| 250 | `Tools/ai/build_code_edit_proposal_from_plan.py` |
| 245 | `Tools/ai/build_megalithic_review_pr_draft.py` |
| 240 | `Tools/ai/review_wave_entrypoints.py` |
| 240 | `Scripting/v61b_backgood/fog_dynamics.py` |
| 238 | `Tools/validation/check_selective_execution_plan.py` |
| 238 | `Tools/npu/run_ollama_music_agent.py` |
| 232 | `Tools/ai/smart_ai_gatekeeper.py` |
| 232 | `Tools/ai/replay_gpu_planner_json_contract.py` |
| 231 | `Tools/ai/enrich_github_evidence_bundle_code_plan.py` |
| 230 | `Tools/validation/check_ai_dry_run_matrix_outputs.py` |
| 229 | `Tools/validation/check_npu_knowledge_broker_packet.py` |
| 225 | `Tools/validation/build_python_line_count_csv.py` |
| 222 | `Tools/validation/check_generated_artifact_path_policy.py` |
| 222 | `Tools/ai/workload_quality.py` |
| 221 | `Scripting/v61b/spaziotempo/core/registry.py` |
| 219 | `Tools/workflow/smart_ai_context.py` |
| 217 | `Tools/validation/generated_file_policy.py` |
| 217 | `Tools/ai/artifact_domain_registry.py` |
| 216 | `Tools/ai/code_patch_plan_common.py` |
| 211 | `Tools/ai/github_evidence_bundle_reports.py` |
| 210 | `Tools/validation/run_gpu_planner_json_contract_smoke.py` |
| 209 | `Tools/validation/check_local_ai_enrichment_plan.py` |
| 209 | `Tools/ai/github_evidence_bundle_markdown.py` |
| 207 | `Tools/validation/check_core_activation_agnostic_contract.py` |
| 206 | `Scripting/v61b_backgood/hotpatch/render_patch.py` |
| 206 | `Scripting/v61b/hotpatch/render_patch.py` |
| 204 | `Tools/validation/run_agent_review_evidence_sufficiency_smoke.py` |
| 203 | `Tools/validation/run_code_edit_proposal_smoke.py` |
| 203 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` |
| 201 | `Tools/validation/run_agent_review_code_patch_plan_smoke.py` |
| 201 | `Tools/ai/code_edit_proposal_helpers.py` |
| 200 | `Tools/ai/validate_ai_artifacts.py` |
| 200 | `Scripting/v61b/main_v61b.py` |
| 198 | `Scripting/v61b/world_setup.py` |
| 197 | `Tools/validation/generated_python_policy.py` |
| 197 | `Tools/ai/pipeline/steps.py` |
| 189 | `Tools/ai/check_npu_provider_environment.py` |
| 187 | `Tools/validation/check_validation_report_contract.py` |
| 186 | `Tools/workflow/git_auto_push.py` |
| 186 | `Tools/ai/build_workload_quality_lane_routing.py` |
| 185 | `Tools/ai/pipeline/remediation.py` |
| 183 | `Tools/workflow/gui/components/action_panel.py` |
| 183 | `Tools/validation/check_ai_dry_run_matrix_cases.py` |
| 182 | `Tools/workflow/gui/components/live_output_panel.py` |
| 182 | `Tools/ai/run_local_provider_probe.py` |
| 181 | `Tools/workflow/gui/workflow_gui_with_push.py` |
| 181 | `Scripting/v61b_backgood/main_v61b.py` |
| 174 | `Scripting/v61b_backgood/world_setup.py` |
| 173 | `Tools/validation/check_generated_blender_script_policy.py` |
| 161 | `Scripting/shared/image_sequence.py` |
| 160 | `Tools/npu/npu_runtime.py` |
| 159 | `Tools/validation/check_npu_decode_quality_remediation.py` |
| 159 | `Scripting/v61b/fog_filaments.py` |
| 157 | `Tools/npu/pipeline/__init__.py` |
| 153 | `Tools/ai/github_evidence_bundle_io.py` |
| 152 | `Tools/ai/pipeline/models.py` |
| 150 | `Scripting/v61b/hotpatch/lighting_patch.py` |
| 149 | `Tools/validation/check_refactor_status_consistency.py` |
| 148 | `Tools/npu/build_runtime_output_manifest.py` |
| 147 | `Tools/validation/check_blender_shared_compat_smoke.py` |
| 147 | `Tools/npu/build_provider_result_report.py` |
| 146 | `Tools/ai/github_evidence_bundle_decisions.py` |
| 144 | `Tools/workflow/artifact_consult.py` |
| 142 | `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` |
| 142 | `Tools/ai/build_github_evidence_bundle.py` |
| 141 | `Tools/validation/check_docs_links.py` |
| 140 | `Scripting/shared/blender_compat.py` |
| 134 | `Tools/ai/github_evidence_bundle_artifacts.py` |
| 134 | `Scripting/shared/ffmpeg_encoder.py` |
| 133 | `Scripting/v61b/hotpatch/fog_patch.py` |
| 133 | `Scripting/shared/render_profiles.py` |
| 132 | `Tools/validation/check_json_artifacts.py` |
| 132 | `Scripting/v61b/spaziotempo/core/collections.py` |
| 130 | `Tools/ai/model_json.py` |
| 128 | `Tools/ai/build_agent_state_packet.py` |
| 127 | `Tools/npu/run_npu_artifact_reviewer.py` |
| 127 | `Tools/npu/pipeline/artifact_paths.py` |
| 125 | `Tools/validation/check_agent_memory_policy.py` |
| 125 | `Tools/validation/check_generated_python_policy.py` |
| 125 | `Scripting/v61b_backgood/hotpatch/accent_patch.py` |
| 125 | `Tools/npu/pipeline/reports.py` |
| 124 | `Scripting/v61b_backgood/hotpatch/fog_patch.py` |
| 123 | `Tools/validation/check_execution_plan_status.py` |
| 119 | `Tools/validation/check_ai_model_json.py` |
| 118 | `Tools/ai/pipeline/schema_report.py` |
| 117 | `Tools/workflow/workflow_shell_with_push.py` |
| 117 | `Tools/validation/check_package_structure.py` |
| 113 | `build_track_summary.py` |
| 111 | `Tools/npu/ai_memory_context.py` |
| 110 | `Tools/workflow/asset_inventory.py` |
| 107 | `Tools/npu/pipeline/config.py` |
| 107 | `Tools/ai/pipeline/markdown_report.py` |
| 105 | `Tools/validation/check_python_syntax.py` |
| 104 | `Tools/ai/pipeline/preflight.py` |
| 103 | `Scripting/v61b/hotpatch/runner.py` |
| 102 | `Tools/ai/pipeline/runner.py` |
| 102 | `Scripting/shared/path_utils.py` |
| 99 | `Tools/npu/pipeline/prompts.py` |
| 97 | `Tools/ai/pipeline/guardrail_models.py` |
| 97 | `Scripting/v61b_backgood/scene_utils.py` |
| 97 | `Scripting/v61b/scene_utils.py` |
| 96 | `Tools/validation/check_npu_pipeline_docs.py` |
| 92 | `Tools/workflow/gui/components/st_theme.py` |
| 91 | `Tools/npu/build_semantic_code_chunks.py` |
| 91 | `Scripting/v61b_backgood/hotpatch/common.py` |
| 91 | `Scripting/v61b/hotpatch/common.py` |
| 88 | `Scripting/shared/json_io.py` |
| 86 | `Tools/ai/pipeline/artifact_contracts.py` |
| 85 | `Scripting/v61b_backgood/hotpatch/lighting_patch.py` |
| 84 | `Tools/npu/pipeline/validators.py` |
| 83 | `Tools/validation/check_provider_result_parsing.py` |
| 81 | `Scripting/v61b_backgood/io_utils.py` |
| 81 | `Scripting/v61b/io_utils.py` |
| 80 | `Tools/npu/pipeline/fixtures.py` |
| 79 | `Scripting/_template_audio_reactive_package/main.py` |
| 75 | `Tools/npu/pipeline/context_builder.py` |
| 75 | `Scripting/_template_audio_reactive_package/encode_ffmpeg.py` |
| 74 | `Tools/ai/pipeline/reports.py` |
| 73 | `Tools/ai/pipeline/compat.py` |
| 70 | `Tools/npu/pipeline/runner.py` |
| 70 | `Tools/ai/pipeline/refactor_status.py` |
| 69 | `Tools/ai/review_agent_memory.py` |
| 68 | `Tools/npu/pipeline/migration_readiness.py` |
| 66 | `Tools/ai/pipeline/scheduler.py` |
| 65 | `Tools/validation/check_ai_pipeline_report_contract.py` |
| 65 | `Tools/ai/run_parallel_artifact_pipeline.py` |
| 64 | `Tools/validation/check_artifact_domain_registry.py` |
| 63 | `Scripting/v61b/hot_update_scene_v61b.py` |
| 61 | `Tools/npu/pipeline/io_utils.py` |
| 61 | `Scripting/v61b_backgood/hot_update_scene_v61b.py` |
| 60 | `Scripting/v61b_backgood/hotpatch/runner.py` |
| 59 | `Tools/validation/check_npu_pipeline_helper_tests.py` |
| 56 | `Tools/npu/pipeline/artifact_writer.py` |
| 53 | `Tools/ai/merge_ai_candidates.py` |
| 52 | `Tools/npu/pipeline/legacy_compat.py` |
| 51 | `Scripting/v61b/reload_utils.py` |
| 51 | `Scripting/_template_audio_reactive_package/audio_mapping.py` |
| 50 | `Tools/validation/report_utils.py` |
| 50 | `Tools/ai/pipeline/cli.py` |
| 49 | `Scripting/_template_audio_reactive_package/config.py` |
| 35 | `Scripting/_template_audio_reactive_package/materials.py` |
| 31 | `Tools/ai/pipeline/orchestrator.py` |
| 29 | `Scripting/v61b_backgood/camera_setup.py` |
| 29 | `Scripting/v61b/camera_setup.py` |
| 26 | `Scripting/_template_audio_reactive_package/render_settings.py` |
| 26 | `Scripting/_template_audio_reactive_package/camera.py` |
| 23 | `Tools/ai/pipeline/__init__.py` |
| 23 | `Scripting/_template_audio_reactive_package/lighting.py` |
| 21 | `Scripting/_template_audio_reactive_package/scene_objects.py` |
| 20 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/render_profiles_reference.py` |
| 19 | `Scripting/v61b/spaziotempo/features/catalog.py` |
| 15 | `Tools/ai/pipeline/defaults.py` |
| 13 | `Scripting/shared/__init__.py` |
| 4 | `Scripting/v61b/spaziotempo/__init__.py` |
| 3 | `Scripting/v61b_backgood/hotpatch/__init__.py` |
| 3 | `Scripting/v61b/hotpatch/__init__.py` |
| 1 | `Scripting/v61b_backgood/__init__.py` |
| 1 | `Tools/workflow/gui/components/__init__.py` |
| 1 | `Scripting/v61b/spaziotempo/features/__init__.py` |
| 1 | `Scripting/v61b/__init__.py` |
| 1 | `Scripting/v61b/spaziotempo/core/__init__.py` |

```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260502-215526.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `12994`
- SHA-256: `efd0ce953e18e77190ba7070b78f13818a0d1e468a65613e2e4dbf27d1793b06`
- Content included: `True`
- Content truncated: `False`

```text
File,Lines
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1773
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
old script legacy/spaziotempo_asset_visual_v6.py,1174
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Tools/ai/run_agent_gpu_deep_planning_review.py,729
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Scripting/v61b/materials.py,657
Tools/npu/run_npu_review.py,628
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_selective_execution_plan.py,618
Tools/workflow/workflow_debug.py,607
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,575
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/build_agent_review_patch_plan.py,562
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Tools/ai/agent_state.py,544
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/ai/build_agent_review_code_patch_plan.py,499
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
Tools/ai/run_agent_gpu_deep_planning_supervised.py,478
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/ai/build_code_interpreter_report.py,437
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/npu/ollama_runtime.py,422
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/ai/run_npu_gpu_deep_review_auditor.py,411
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_github_evidence_bundle.py,401
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
Scripting/v61b/encode_image_sequence_v61b.py,395
Scripting/v61b/hotpatch/hero_material_patch.py,395
Scripting/v61b_backgood/hotpatch/hero_material_patch.py,395
Tools/ai/build_agent_review_evidence_sufficiency.py,394
Scripting/v61b/fog_dynamics.py,392
Tools/ai/build_full_context_golden_proposals.py,392
Tools/validation/check_code_contract_drift.py,392
Tools/workflow/gui/components/artifact_browser.py,390
Scripting/v61b_backgood/encode_image_sequence_v61b.py,376
indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py,369
Tools/npu/generated_blender_script_candidate.py,369
Tools/npu/generated_blender_script_candidate_FristNear.py,369
Tools/validation/check_repository_change_proposals.py,366
Tools/validation/test_npu_pipeline_helpers.py,359
Scripting/v61b_backgood/config.py,358
Tools/ai/build_local_ai_enrichment_plan.py,357
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,353
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/npu/build_blender_manual_context.py,326
Tools/workflow/workflow_shell.py,324
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/validation/check_local_ai_adapter_manifest.py,317
Tools/ai/build_music_intermediates.py,314
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/ai/build_analysis_input_bundle.py,304
Tools/ai/gpu_planner_json_contract.py,302
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/select_semantic_code_chunks.py,291
Tools/validation/check_ai_pipeline_modules.py,290
Scripting/v61b/hotpatch/diagnostics.py,286
Tools/ai/build_gpu_repair_failure_recommendation.py,286
Tools/workflow/startup_check.py,284
Tools/ai/build_agent_transient_request_context.py,283
Tools/validation/run_agent_review_patch_plan_smoke.py,283
Tools/workflow/gui/components/session_overview.py,278
Tools/ai/analyze_gpu_npu_run_sync.py,273
Scripting/v61b/render_setup.py,270
Tools/validation/check_full_context_golden_docs_contract.py,270
Scripting/v61b_backgood/render_setup.py,267
Tools/workflow/ai_runtime_diagnostics.py,267
Tools/ai/build_code_patch_docs_followup.py,266
Tools/validation/check_ai_workload_report_quality.py,260
Tools/validation/check_docs_contract_drift.py,259
Tools/ai/build_code_patch_artifact_pack.py,258
analyze_wav.py,257
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_edit_proposal_from_plan.py,250
Tools/ai/build_megalithic_review_pr_draft.py,245
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/ai/replay_gpu_planner_json_contract.py,232
Tools/ai/smart_ai_gatekeeper.py,232
Tools/ai/enrich_github_evidence_bundle_code_plan.py,231
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/validation/build_python_line_count_csv.py,225
Tools/ai/workload_quality.py,222
Tools/validation/check_generated_artifact_path_policy.py,222
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/generated_file_policy.py,217
Tools/ai/code_patch_plan_common.py,216
Tools/ai/github_evidence_bundle_reports.py,211
Tools/validation/run_gpu_planner_json_contract_smoke.py,210
Tools/ai/github_evidence_bundle_markdown.py,209
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py,203
Tools/validation/run_code_edit_proposal_smoke.py,203
Tools/ai/code_edit_proposal_helpers.py,201
Tools/validation/run_agent_review_code_patch_plan_smoke.py,201
Scripting/v61b/main_v61b.py,200
Tools/ai/validate_ai_artifacts.py,200
Scripting/v61b/world_setup.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/ai/check_npu_provider_environment.py,189
Tools/validation/check_validation_report_contract.py,187
Tools/ai/build_workload_quality_lane_routing.py,186
Tools/workflow/git_auto_push.py,186
Tools/ai/pipeline/remediation.py,185
Tools/validation/check_ai_dry_run_matrix_cases.py,183
Tools/workflow/gui/components/action_panel.py,183
Tools/ai/run_local_provider_probe.py,182
Tools/workflow/gui/components/live_output_panel.py,182
Scripting/v61b_backgood/main_v61b.py,181
Tools/workflow/gui/workflow_gui_with_push.py,181
Scripting/v61b_backgood/world_setup.py,174
Tools/validation/check_generated_blender_script_policy.py,173
Scripting/shared/image_sequence.py,161
Tools/npu/npu_runtime.py,160
Scripting/v61b/fog_filaments.py,159
Tools/validation/check_npu_decode_quality_remediation.py,159
Tools/npu/pipeline/__init__.py,157
Tools/ai/github_evidence_bundle_io.py,153
Tools/ai/pipeline/models.py,152
Scripting/v61b/hotpatch/lighting_patch.py,150
Tools/validation/check_refactor_status_consistency.py,149
Tools/npu/build_runtime_output_manifest.py,148
Tools/npu/build_provider_result_report.py,147
Tools/validation/check_blender_shared_compat_smoke.py,147
Tools/ai/github_evidence_bundle_decisions.py,146
Tools/workflow/artifact_consult.py,144
Tools/ai/build_github_evidence_bundle.py,142
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/validation/check_docs_links.py,141
Scripting/shared/blender_compat.py,140
Scripting/shared/ffmpeg_encoder.py,134
Tools/ai/github_evidence_bundle_artifacts.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/model_json.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/validation/check_package_structure.py,117
Tools/workflow/workflow_shell_with_push.py,117
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/validation/check_python_syntax.py,105
Tools/ai/pipeline/preflight.py,104
Scripting/v61b/hotpatch/runner.py,103
Scripting/shared/path_utils.py,102
Tools/ai/pipeline/runner.py,102
Tools/npu/pipeline/prompts.py,99
Scripting/v61b/scene_utils.py,97
Scripting/v61b_backgood/scene_utils.py,97
Tools/ai/pipeline/guardrail_models.py,97
Tools/validation/check_npu_pipeline_docs.py,96
Tools/workflow/gui/components/st_theme.py,92
Scripting/v61b/hotpatch/common.py,91
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Scripting/shared/json_io.py,88
Tools/ai/pipeline/artifact_contracts.py,86
Scripting/v61b_backgood/hotpatch/lighting_patch.py,85
Tools/npu/pipeline/validators.py,84
Tools/validation/check_provider_result_parsing.py,83
Scripting/v61b/io_utils.py,81
Scripting/v61b_backgood/io_utils.py,81
Tools/npu/pipeline/fixtures.py,80
Scripting/_template_audio_reactive_package/main.py,79
Scripting/_template_audio_reactive_package/encode_ffmpeg.py,75
Tools/npu/pipeline/context_builder.py,75
Tools/ai/pipeline/reports.py,74
Tools/ai/pipeline/compat.py,73
Tools/ai/pipeline/refactor_status.py,70
Tools/npu/pipeline/runner.py,70
Tools/ai/review_agent_memory.py,69
Tools/npu/pipeline/migration_readiness.py,68
Tools/ai/pipeline/scheduler.py,66
Tools/ai/run_parallel_artifact_pipeline.py,65
Tools/validation/check_ai_pipeline_report_contract.py,65
Tools/validation/check_artifact_domain_registry.py,64
Scripting/v61b/hot_update_scene_v61b.py,63
Scripting/v61b_backgood/hot_update_scene_v61b.py,61
Tools/npu/pipeline/io_utils.py,61
Scripting/v61b_backgood/hotpatch/runner.py,60
Tools/validation/check_npu_pipeline_helper_tests.py,59
Tools/npu/pipeline/artifact_writer.py,56
Tools/ai/merge_ai_candidates.py,53
Tools/npu/pipeline/legacy_compat.py,52
Scripting/_template_audio_reactive_package/audio_mapping.py,51
Scripting/v61b/reload_utils.py,51
Tools/ai/pipeline/cli.py,50
Tools/validation/report_utils.py,50
Scripting/_template_audio_reactive_package/config.py,49
Scripting/_template_audio_reactive_package/materials.py,35
Tools/ai/pipeline/orchestrator.py,31
Scripting/v61b/camera_setup.py,29
Scripting/v61b_backgood/camera_setup.py,29
Scripting/_template_audio_reactive_package/camera.py,26
Scripting/_template_audio_reactive_package/render_settings.py,26
Scripting/_template_audio_reactive_package/lighting.py,23
Tools/ai/pipeline/__init__.py,23
Scripting/_template_audio_reactive_package/scene_objects.py,21
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/render_profiles_reference.py,20
Scripting/v61b/spaziotempo/features/catalog.py,19
Tools/ai/pipeline/defaults.py,15
Scripting/shared/__init__.py,13
Scripting/v61b/spaziotempo/__init__.py,4
Scripting/v61b/hotpatch/__init__.py,3
Scripting/v61b_backgood/hotpatch/__init__.py,3
Scripting/v61b/__init__.py,1
Scripting/v61b/spaziotempo/core/__init__.py,1
Scripting/v61b/spaziotempo/features/__init__.py,1
Scripting/v61b_backgood/__init__.py,1
Tools/workflow/gui/components/__init__.py,1

```

### `output/validation/python_line_count_refactor_large_code_20260502-215518.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1691`
- SHA-256: `78e62fef41fa2d9d057e8e3dfb480f72155a3757b63dea5520ae6b678c01a10a`
- Content included: `True`
- Content truncated: `False`

```text
# Python Line Count CSV

- Passed: `True`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260502-215526.csv`
- File count: `277`
- Total lines: `77731`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest Python files

- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` — `2197` lines
- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines
- `old script legacy/spaziotempo_asset_visual_v61.py` — `1513` lines
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines
- `Tools/workflow/workflow_state.py` — `1230` lines
- `old script legacy/spaziotempo_asset_visual_v6.py` — `1174` lines
- `Scripting/v61b_backgood/scene_tuning_panel.py` — `1097` lines
- `Scripting/v61b/animation.py` — `1079` lines
- `Scripting/v61b_backgood/animation.py` — `1019` lines
- `old script legacy/spaziotempo_album_visual_v5.py` — `969` lines
- `Tools/workflow/gui/workflow_gui.py` — `738` lines
- `Scripting/v61b/physics_setup.py` — `737` lines
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `729` lines
- `Scripting/v61b/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/physics_setup.py` — `720` lines
- `Tools/npu/build_music_context.py` — `711` lines
- `old script legacy/spaziotempo_album_visual_v3.py` — `710` lines
- `Scripting/v61b/materials.py` — `657` lines
- `Tools/npu/run_npu_review.py` — `628` lines

## Guardrail

This artifact is line-count evidence only. It is not a patch plan and it must not be committed from `output/**`.

```

### `output/analysis/code_interpreter_code_refactor_20260502-215518.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6915`
- SHA-256: `3340723ec8274d7924f5e5cab56cdfec166eb8fa9e7703ca2396a6df9f3a157a`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `231`
- Parsed files: `231`
- Total lines: `61338`
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
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `729` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
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

### `output/ai_pipeline/code_refactor_balanced_20260502-215518_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1024`
- SHA-256: `ce5d331637c0edd207f062a44a3d75dd82b3512df9c9390f7a4abc7c59d02e45`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `322.095`
- `npu_audit_count`: `3`
- `npu_audit_success_count`: `3`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `gpu_evidence_ready_for_manual_patch_count`: `12`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `3`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `True`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: `context_echo_detected`
- `manual_review_required`: `True`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `3` status=`finished` class=`usable_audit_text` success=`True`
- round `6` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/code_refactor_balanced_20260502-215518_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `961`
- SHA-256: `46c9203e1f5f23c21a3cbc33506c2f55d5926b84e745e55daeb36ed2015d68cf`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `292.995`
- Round count: `20`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- JSON parse error count: `16`
- Context echo detected count: `1`
- Model output schema mismatch count: `4`
- Empty recommendations reason: `context_echo_detected`
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

### `output/analysis/gpu_json_contract_replay_code_refactor_20260502-215518.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `670`
- SHA-256: `c51c0ef6ba8321f098c002e61c46c9cb1129ce8f2d7b3abd5ab8602961643853`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `20`
- Context echo detected: `1`
- JSON parse failures: `16`
- Schema mismatches: `3`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `context_echo_detected`: `1`
- `json_parse_failure`: `16`
- `model_output_schema_mismatch`: `3`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_code_refactor_20260502-215518.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1498`
- SHA-256: `f09af5395e9502518d3b7febe6910b796d98fd43d96fb0bd8a3cb9fbe89ff579`
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
- `npu_audit_count`: `3`
- `npu_audit_success_count`: `3`
- `npu_audit_round_coverage`: `0.15`
- `avg_gpu_round_seconds`: `16.105`
- `p50_gpu_round_seconds`: `16.105`
- `p90_gpu_round_seconds`: `16.105`
- `avg_npu_audit_seconds`: `102.667`
- `p50_npu_audit_seconds`: `102.0`
- `p90_npu_audit_seconds`: `104.0`
- `npu_to_gpu_avg_duration_ratio`: `6.375`
- `gpu_elapsed_seconds`: `322.095`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_summary_or_elapsed_estimate`

## Suggested balanced profile

- `npu_auditor_every_rounds`: `6`
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


```

### `output/ai_pipeline/code_refactor_balanced_20260502-215518_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `13759`
- SHA-256: `fcd5b5a799c70e6ebdf6ddbf51ab7291ef3df6610445a99af5ed081c1cd8d046`
- Content included: `True`
- Content truncated: `False`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-02T22:02:20",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 322.095,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 292.995,\n  \"round_count\": 20,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"empty_recommendations_reason\": \"context_echo_detected\",\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/code_refactor_balanced_20260502-215518_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/code_refactor_balanced_20260502-215518_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "context_echo_detected",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "gpu_summary": {
    "passed": true,
    "round_count": 20,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 16,
    "repair_attempt_count": 0,
    "empty_recommendations_reason": "context_echo_detected",
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
  "checkpoint_dir": "output/ai_pipeline/code_refactor_balanced_20260502-215518_checkpoints",
  "npu_audit_count": 3,
  "npu_audit_success_count": 3,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/code_refactor_balanced_20260502-215518_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/code_refactor_balanced_20260502-215518_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-02T21:57:06",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_001_npu_async_audit_metadata.json",
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
      "finished_at": "2026-05-02T21:58:50",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
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
      "checkpoint": "output/ai_pipeline/code_refactor_balanced_20260502-215518_checkpoints/round_003.json",
      "audit_output": "output/ai_pipeline/code_refactor_balanced_20260502-215518_checkpoints/round_003_npu_async_audit.json",
      "started_at": "2026-05-02T21:58:52",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_003.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_003_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_003_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_003_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_003_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_003_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_003_npu_async_audit_metadata.json",
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
      "finished_at": "2026-05-02T22:00:34",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_checkpoints\\\\round_003_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_checkpoints\\\\round_003_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
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
      "checkpoint": "output/ai_pipeline/code_refactor_balanced_20260502-215518_checkpoints/round_006.json",
      "audit_output": "output/ai_pipeline/code_refactor_balanced_20260502-215518_checkpoints/round_006_npu_async_audit.json",
      "started_at": "2026-05-02T22:00:36",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_006.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_006_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_006_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_006_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_006_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_006_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\code_refactor_balanced_20260502-215518_checkpoints\\round_006_npu_async_audit_metadata.json",
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
      "finished_at": "2026-05-02T22:02:18",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_checkpoints\\\\round_006_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\code_refactor_balanced_20260502-215518_checkpoints\\\\round_006_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "gpu_review_blocked": false
    }
  ],
  "decision": {
    "gpu_review_blocked_by_npu": false,
    "npu_auditor_mode": "parallel_best_effort",
    "npu_audit_success_count": 3,
    "ready_for_patch_plan": false,
    "fallback_patch_plan_recommended": true,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
    "gpu_empty_recommendations_reason": "context_echo_detected",
    "manual_review_required": true
  },
  "guardrails": {
    "gpu_continues_without_waiting_for_npu": true,
    "npu_auditor_non_blocking": true,
    "npu_primary_advisory": false,
    "patch_application_performed": false,
    "real_github_pr_created": false,
    "sqlite_write_performed": false,
    "persistent_memory_write_performed": false
  }
}

```

### `output/ai_pipeline/code_refactor_balanced_20260502-215518_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `121288`
- SHA-256: `8eb402fd67bb3d08d81f1207300e82552f72d491f3beb9c31210af518ffadc14`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-02T22:01:51",
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
  "elapsed_seconds": 292.995,
  "context_file_count": 220,
  "round_count": 20,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 6.248,
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
      "response_chars": 389,
      "raw_response_preview": "It seems like you have a detailed set of documentation for managing AI-generated content within a Blender project. This includes guidelines on package standards, guardrails and validation processes, shared utilities, and more. If you need assistance with any specific part of this documentation or if there's anything else I can help with related to your project, feel free to let me know!",
      "parsed_response": {
        "summary": "It seems like you have a detailed set of documentation for managing AI-generated content within a Blender project. This includes guidelines on package standards, guardrails and validation processes, shared utilities, and more. If you need assistance with any specific part of this documentation or if there's anything else I can help with related to your project, feel free to let me know!",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "json_ok": false,
      "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "json_parse_failure",
      "contract": {
        "json_ok": false,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
        "schema_errors": [],
        "raw_response_sha256": "d384fd48cfd78e463b7c10b8087d1f1391f1b25c5f75da7cd1efd55cde62d9d6",
        "raw_response_chars": 389,
        "top_level_keys": [],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "empty_recommendations_reason": "json_parse_failure"
      },
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
      "elapsed_seconds": 10.629,
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
      "response_chars": 1753,
      "raw_response_preview": "It seems like you have provided a detailed set of documentation files related to an AI pipeline project. These files cover various aspects such as the architecture, refactoring status, provider-agnostic guidelines, and optimization strategies. Here's a summary of the key points from each file:\n\n1. **AI_PIPELINE_ARCHITECTURE.md**:\n   - Describes the modular architecture of the AI artifact pipeline.\n   - Lists the main components like `defaults.py`, `models.py`, `runner.py`, etc.\n   - Explains the data flow and interaction between different modules.\n\n2. **AI_PIPELINE_REFACTOR_STATUS.md**:\n   - Provides a status marker for the current state of the pipeline refactor.\n   - Indicates that the modular split is complete but local validation is pending.\n   - Lists the steps required for local validation, including running specific Python scripts and regenerating indexes.\n\n3. **AI_PIPELINE_OPTIMIZATION.md**:\n   - Outlines the optimization priorities and strategies for improving the pipeline.\n   - Discusses the current state of the modular split and the need for further refinement of lane policies and Markdown report generation.\n\n4. **AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md**:\n   - Explains how to design a provider-agnostic AI pipeline.\n   - Defines the roles of different layers (orchestration, provider, artifact) in the pipeline.\n   - Provides guidelines for implementing runtime-agnostic stages and handling provider failures.\n\nThese documents are essential for maintaining and extending the AI pipeline project. They ensure that the pipeline remains modular, reusable across different providers, and optimized for performance and reliability. If you have any specific questions or need further assistance with these files, feel free to ask!",
      "parsed_response": {
        "summary": "It seems like you have provided a detailed set of documentation files related to an AI pipeline project. These files cover various aspects such as the architecture, refactoring status, provider-agnostic guidelines, and optimization strategies. Here's a summary of the key points from each file:\n\n1. **AI_PIPELINE_ARCHITECTURE.md**:\n   - Describes the modular architecture of the AI artifact pipeline.\n   - Lists the main components like `defaults.py`, `models.py`, `runner.py`, etc.\n   - Explains the data flow and interaction between different modules.\n\n2. **AI_PIPELINE_REFACTOR_STATUS.md**:\n   - Provides a status marker for the current state of the pipeline refactor.\n   - Indicates that the modular split is complete but local validation is pending.\n   - Lists the steps required for local validation, including running specific Python scripts and regenerating indexes.\n\n3. **AI_PIPELINE_OPTIMIZATION.md**:\n   - Outlines the optimization priorities and strategies for improving the pipeline.\n   - Discusses the current state of the modular split and the need for further refinement of lane policies and Markdown report generation.\n\n4. **AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md**:\n   - Explains how to design a provider-agnostic AI pipeline.\n   - Defines the roles of different layers (orchestration, provider, artifact) in the pipeline.\n   - Provides guidelines for implementing runtime-agnostic stages and handling provider failures.\n\nThese documents are essential for maintaining and extending the AI pipeline project. They ensure that the pipeline remains modular, reusable across different providers, and optimized for performance and reliability. If you have any specific questions or need further assistance with these files, feel free to ask!",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "json_ok": false,
      "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "json_parse_failure",
      "contract": {
        "json_ok": false,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "ModelJsonParseError: Unable to parse model JSON: Expecting value: line 1 column 1 (char 0)",
        "schema_errors": [],
        "raw_response_sha256": "655e9324c3b5f40b45dc414bde2a258ca0dbcbd894cfbc6914efe997c86297fa",
        "raw_response_chars": 1753,
        "top_level_keys": [],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "empty_recommendations_reason": "json_parse_failure"
      },
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
      "elapsed_seconds": 26.042,
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
        "summary": "```json\n{\n  \"path\": \"docs/CODE_CONSULTATION_REPORT.md\",\n  \"exists\": true,\n  \"lines\": 151,\n  \"chars\": 6000,\n  \"content_preview\": \"# Code Consultation Report\\n\\n## Scope\\n\\nThis report summarizes a broad code consultation of `blender-audio-project` after the GitHub code-quality check was launched.\\n\\nThe review is non-destructive. No working Blender script was refactored or modified.\\n\\n## Repository status\\n\\n- Repository: `C-F-tek/blender-audio-project`\\n- Default branch: `master`\\n- Visibility: private\\n- GitHub App permissions observed: admin, maintain, pull, push, triage\\n- Repository size observed: about 2564 KB\\n\\n## Code quality workflow visibility\\n\\nNo workflow run was visible through the available GitHub connector for the checked commits.\\n\\nThe following common workflow paths were not found:\\n\\n```text\\n.github/workflows/code-quality.yml\\n.github/workflows/code_quality.yml\\n.github/workflows/ci.yml\\n```\\n\\nThis means that the code-quality action may be external, not indexed through the available API endpoint, manually launched in a way not returned by commit workflow lookup, or not yet committed as a workflow file.\\n\\n## Source index consulted\\n\\nThe main source index consulted was:\\n\\n```text\\nindexAI/project_code_index.md\\nindexAI/project_code_manifest.json\\n```\\n\\nThe index reports:\\n\\n- 98 indexed files\\n- 212 code chunks\\n- generated timestamp: `2026-04-27T14:41:27`\\n\\nImportant: this index predates the latest documentation and template additions. It should be regenerated.\\n\\n## Main code areas\\n\\n### Root tools\\n\\n| File | Role | Assessment |\\n|---|---|---|\\n| `analyze_wav.py` | WAV analysis, low/mid/high/onset/beat extraction, Blender JSON generation | Good functional core. Needs dependency documentation and optional validation. |\\n| `build_track_summary.py` | Compact summary builder from analysis JSON | Useful, but default paths are track-specific. Should be made more generic or documented as local defaults. |\\n| `normalize_scene_spec.py` | Scene-s",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "json_ok": false,
      "parse_error": "ModelJsonParseError: Unable to parse model JSON: Invalid control character at: line 6 column 5241 (char 5339)",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "json_parse_failure",
      "contract": {
        "json_ok": false,
        "schema_ok": false,
        "context_echo_detected": false,
        "parse_error": "ModelJsonParseError: Unable to parse model JSON: Invalid control character at: line 6 column 5241 (char 5339)",
        "schema_errors": [],
        "raw_response_sha256": "a5cc23b018373eb72f3d88740656bece602c08007417db915597e4520335af2b",
        "raw_response_chars": 5369,
        "top_level_keys": [],
        "recommendation_count": 0,
        "valid_recommendation_count": 0,
        "invalid_recommendation_count": 0,
        "empty_recommendations_reason": "json_parse_failure"
      },
      "repair_attempt_count": 0,
```

### `output/validation/gpu_planner_json_contract_smoke_code_refactor_20260502-215518.md`

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

### `output/validation/npu_provider_environment_code_refactor_20260502-215518.md`

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
