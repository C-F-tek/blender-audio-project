# Patch suggestion bundle final phase

Status: active final-phase runbook aligned to current code  
Scope: IA-Carmine full toolbox flow, deterministic patch suggestion application, review PR preparation.

## Code-verified current state

This document describes the current implementation, not the future product target.

Current script family:

```text
Tools/ai/apply_patch_suggestion_bundle.py
Tools/ai/patch_suggestion_bundle/cli.py
Tools/ai/prepare_review_pr.py
Tools/validation/run_patch_suggestion_bundle_apply_smoke.py
Tools/validation/check_patch_suggestion_product_separation.py
```

Current behavior from code:

```text
apply_patch_suggestion_bundle.py discovers stamped/current suggestion JSON reports.
apply_patch_suggestion_bundle.py dedupes explicit --suggestion-report paths against Stamp discovery.
apply_patch_suggestion_bundle.py can apply only deterministic operations when --apply is supplied.
apply_patch_suggestion_bundle.py creates/switches a review branch when requested, but does not commit.
apply_patch_suggestion_bundle.py may push the review branch when --push-review-branch is supplied, but does not force-push.
prepare_review_pr.py stages only explicit --include-path allowlist entries.
prepare_review_pr.py rejects output/**, generated chunks, renders and DB/SQLite paths.
prepare_review_pr.py can commit, push and call gh pr create when requested.
prepare_review_pr.py currently does not auto-discover include paths from patch_suggestion_bundle_apply results.
prepare_review_pr.py currently does not pass --draft to gh pr create.
check_patch_suggestion_product_separation.py is report-only and validates apply reports or smoke wrapper reports.
```

Do not document automatic path discovery or automatic draft PR creation as active until the code implements it.

## Product target versus current implementation

Target product loop:

```text
Task Markdown input
-> unified launcher Full0To10 run
-> provider/tool/broker/validator/evidence loop
-> deterministic patch suggestion extraction
-> deterministic patch apply on CARMINEai/* review branch
-> product-vs-supplemental separation validation
-> review PR preparation
-> GitHub PR for human review
```

Current implementation gap:

```text
Review PR staging still requires explicit ReviewPrIncludePath / --include-path.
Draft PR creation is not implemented in prepare_review_pr.py.
Automatic include-path derivation from patch_suggestion_bundle_apply results is a follow-up.
```

## Runtime variables

Use the same Python and stamp conventions as the unified launcher and Python full-toolbox workflow.

```powershell
$env:IA_CARMINE_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path
$ProjectPython = $env:IA_CARMINE_PYTHON
$Stamp = "<launcher-owned-stamp>"
```

`$Stamp` belongs to the launcher run. Internal tools consume that value; they should not create a second unrelated stamp for the same product run.

The tool computes the compact artifact stamp used by the full-toolbox engine.

## Stamp-driven discovery

The final phase must be driven by the same run stamp used by the full toolbox run.

Do not hardcode one specific timestamped report filename. Pass the workflow stamp through `--Stamp`:

```powershell
& $ProjectPython .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --Stamp $Stamp `
  --output .\output\validation\patch_suggestion_bundle_apply_dry_run.json
```

The tool discovers matching local JSON reports under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
output/patch_specs/
output/validation/
output/ai_pipeline/
output/ai_packets/
```

It also includes current non-stamped suggestion/proposal reports when present:

```text
output/ai_pipeline/repository_update_suggestions.json
output/ai_pipeline/repository_change_proposals.json
```

Use `--no-current-suggestions` only for debugging a stamp-only run.

## Safety contract

The final apply phase is conservative by design:

```text
No provider execution.
No Blender execution.
No FFmpeg execution.
No SQLite writes.
No Git commit in apply_patch_suggestion_bundle.py.
No merge.
No force-push.
No delete.
No output/** target edits.
No renders/** target edits.
No indexAI/code_chunks/** or indexAI/project_code_chunks/** target edits.
```

Apply policy:

```text
apply is allowed only on a dedicated review branch
branch name must match an allowed prefix
current default allowed prefixes are CARMINEai/ and codex/
master/main apply is refused by branch policy
```

Natural-language suggestions and proposal-only `manual_patch_suggestion` items are not rewritten into code automatically. They are reported as `manual_review_required`.

## Product vs supplemental output

The final phase separates review output into two classes:

```text
essential_patch_suggestion_items
supplemental_telemetry_debug_items
```

Essential/product-facing suggestions must have:

```text
safe concrete source/doc target files
title or rationale
patch sketch or deterministic operation
validation commands or stop conditions
```

Telemetry, evidence, debug and validation-status-only items remain supplemental. They are useful for diagnosis, but they are not enough to close the product loop as an applicable patch suggestion.

Readiness fields:

```text
patch_product_status
ready_for_patch_suggestion_review
manual_review_product.product_facing_manual_review_count
manual_review_product.supplemental_manual_review_count
manual_review_product.deterministic_operation_count
manual_review_product.deterministic_apply_ready
```

The product loop is review-ready only when `patch_product_status` is either:

```text
deterministic_patch_operations_ready
manual_review_product_suggestions_ready
```

`no_applicable_patch_product` means the run produced telemetry/debug context, but no concrete patch product to review.

## Supported deterministic operations

Suggestion/proposal JSON may contain explicit operations:

```text
replace_once
append_once
insert_after_once
insert_before_once
write_file
```

Accepted target path keys include:

```text
path
target
target_file
file
file_path
```

Accepted operation keys include:

```text
operation
op
action
patch_operation
edit_operation
```

Proposal-only operations are preserved for manual review:

```text
manual_patch_suggestion
proposal_only
manual_review_only
```

## Smoke validation

```powershell
& $ProjectPython .\Tools\validation\run_patch_suggestion_bundle_apply_smoke.py `
  --repo-root . `
  --output .\output\validation\patch_suggestion_bundle_apply_smoke.json

& $ProjectPython .\Tools\validation\run_full0to10_product_pr_chain_smoke.py `
  --repo-root . `
  --output .\output\validation\full0to10_product_pr_chain_smoke.json `
  --markdown-output .\output\validation\full0to10_product_pr_chain_smoke.md

Get-Content .\output\validation\patch_suggestion_bundle_apply_smoke.json -Raw |
  ConvertFrom-Json |
  Select-Object passed, smoke_stamp, discovered_reports, current_suggestion_reports, errors, warnings
```

## Dry-run by Stamp

Dry-run must be the first real invocation. It reads matching reports and writes only an output validation report.

```powershell
& $ProjectPython .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --Stamp $Stamp `
  --output .\output\validation\patch_suggestion_bundle_apply_dry_run.json

Get-Content .\output\validation\patch_suggestion_bundle_apply_dry_run.json -Raw |
  ConvertFrom-Json |
  Select-Object `
    passed, `
    Stamp, `
    artifact_stamp, `
    discovered_report_count, `
    current_suggestion_report_count, `
    operation_count, `
    changed_count, `
    applied_count, `
    failed_count, `
    patch_product_status, `
    ready_for_patch_suggestion_review, `
    manual_review_required, `
    errors, `
    warnings
```

Dry-run must show:

```text
applied_count = 0
```

If `discovered_report_count = 0`, the stamp is wrong or the run artifacts are not present locally. If `current_suggestion_report_count = 0`, the current non-stamped reports are not present locally.

## Inspect manual-review proposals

```powershell
$dry = Get-Content .\output\validation\patch_suggestion_bundle_apply_dry_run.json -Raw | ConvertFrom-Json

$dry.manual_review_product |
  Select-Object `
    patch_product_status, `
    ready_for_patch_suggestion_review, `
    deterministic_operation_count, `
    product_facing_manual_review_count, `
    supplemental_manual_review_count |
  Format-List

$dry.essential_patch_suggestion_items |
  Select-Object -First 40 |
  Format-List

$dry.supplemental_telemetry_debug_items |
  Select-Object -First 40 |
  Format-List
```

## Apply on review branch only

Apply only after dry-run is clean and the current branch is a review branch.

```powershell
git branch --show-current
git status --short

& $ProjectPython .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --Stamp $Stamp `
  --output .\output\validation\patch_suggestion_bundle_apply.json `
  --apply
```

The tool refuses `--apply` outside branches matching the allowed prefixes unless explicitly overridden by future code changes.

## Product separation validation

Validate either the direct apply report or the smoke wrapper report:

```powershell
& $ProjectPython .\Tools\validation\check_patch_suggestion_product_separation.py `
  --repo-root . `
  --report .\output\validation\patch_suggestion_bundle_apply.json `
  --require-product `
  --require-supplemental `
  --output .\output\validation\patch_suggestion_product_separation.json

Get-Content .\output\validation\patch_suggestion_product_separation.json -Raw |
  ConvertFrom-Json |
  Select-Object passed, kind, metrics, errors, warnings
```

## Current unified launcher review PR phase

The unified launcher can call `prepare_review_pr.py` through:

```text
-PrepareReviewPr
-ReviewPrBranch
-ReviewPrBaseBranch
-ReviewPrRemote
-ReviewPrTitle
-ReviewPrCommitMessage
-ReviewPrIncludePath
-ReviewPrPush
-ReviewPrCreate
```

Current requirement: pass explicit `-ReviewPrIncludePath` values for the reviewed files that may be staged and committed.
When `-PrepareReviewPr` or `-ReviewPrApplyDeterministicSuggestions` is selected, the unified launcher now runs `check_patch_suggestion_product_separation.py --require-product` between `patch_suggestion_final_phase` and `prepare_review_pr.py`. That keeps the real workflow trace aligned with the focused smoke instead of validating only isolated Python modules.

Example shape:

```powershell
$Stamp = "review_pr_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$ReviewPrIncludePaths = @(
  ".\docs\LOCAL_AI_TASKS\patch-suggestion-bundle-final-phase.md"
)

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . `
  -TaskFile .\docs\LOCAL_AI_TASKS\pr206-patch-suggestion-product-full-run-2026-05-07.md `
  -Stamp $Stamp `
  -Profile core `
  -Model qwen2.5-coder:14b `
  -Full0To10 `
  -RunIntensity quick `
  -PrepareReviewPr `
  -ReviewPrBranch "CARMINEai/review-$Stamp" `
  -ReviewPrTitle "feat(ai): review patch suggestion product $Stamp" `
  -ReviewPrCommitMessage "feat(ai): review patch suggestion product" `
  -ReviewPrIncludePath ($ReviewPrIncludePaths -join ",") `
  -ReviewPrPush `
  -ReviewPrCreate
```

Add `-ReviewPrApplyDeterministicSuggestions` only when deterministic operations are present and the dry-run product has already been inspected. In a real Full0To10 run the repository usually already has fresh ignored `output/` artifacts, so pair deterministic apply with reviewed `-AllowDirty`; the final staging step still uses explicit `-ReviewPrIncludePath` and must not stage `output/**`.

For this workstation snapshot, `qwen2.5-coder:14b` was the preferred Ollama model for strict JSON provider probing. Re-check model health before treating this as permanent.

## Post-apply validation

```powershell
& $ProjectPython .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax_after_patch_suggestion_bundle.json

& $ProjectPython .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract_after_patch_suggestion_bundle.json

git diff --check
git status --short
```

Inspect changed files before commit:

```powershell
git diff --stat
git diff -- .
```

## Evidence bundle after local apply

After local apply and validation, build compact Git-trackable evidence if needed:

```powershell
$EvidenceStamp = Get-Date -Format "yyyyMMdd-HHmmss"

& $ProjectPython .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename patch_suggestion_bundle_final_phase_$EvidenceStamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\validation\patch_suggestion_bundle_apply.json `
  --report .\output\validation\patch_suggestion_bundle_apply_smoke.json `
  --report .\output\validation\patch_suggestion_product_separation.json `
  --report .\output\validation\python_syntax_after_patch_suggestion_bundle.json `
  --report .\output\validation\validation_report_contract_after_patch_suggestion_bundle.json
```

Commit only the generated compact evidence JSON/MD if it is useful for PR review.

## Follow-up implementation candidates

These are not current behavior:

```text
prepare_review_pr.py auto-discovery of changed paths from patch_suggestion_bundle_apply results
prepare_review_pr.py --draft or launcher ReviewPrDraft flag
full launcher product command that requires no explicit ReviewPrIncludePath
```
