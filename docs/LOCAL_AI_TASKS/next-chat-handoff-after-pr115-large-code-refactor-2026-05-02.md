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
