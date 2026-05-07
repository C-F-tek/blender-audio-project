# Patch suggestion bundle final phase

Status: active final-phase runbook  
Scope: IA-Carmine full toolbox flow, patch suggestion application, local PR verification.

## Objective

After the full toolbox run produces patch notes, telemetry and suggestion/proposal JSON, the final phase is allowed to apply only deterministic, reviewable patch operations on a dedicated PR branch.

This phase is implemented by:

```text
Tools/ai/apply_patch_suggestion_bundle.py
Tools/validation/run_patch_suggestion_bundle_apply_smoke.py
```

## Safety contract

The final phase is conservative by design:

```text
No provider execution.
No Blender execution.
No FFmpeg execution.
No SQLite writes.
No Git commit.
No Git push.
No merge.
No force-push.
No delete.
No output/** target edits.
No renders/** target edits.
No indexAI/code_chunks/** or indexAI/project_code_chunks/** target edits.
```

Natural-language suggestions are not rewritten into code automatically. They are reported as `manual_review_required`.

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

## Local PR sync

Use a dedicated review branch. Do not apply this phase directly on `master`.

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin

git switch codex/apply-python-doc-suggestion-wave1 2>$null
if ($LASTEXITCODE -ne 0) {
  git switch -c codex/apply-python-doc-suggestion-wave1 origin/codex/apply-python-doc-suggestion-wave1
}

git pull --ff-only origin codex/apply-python-doc-suggestion-wave1

git status --short
```

## Smoke validation

```powershell
python .\Tools\validation\run_patch_suggestion_bundle_apply_smoke.py `
  --repo-root . `
  --output .\output\validation\patch_suggestion_bundle_apply_smoke.json

Get-Content .\output\validation\patch_suggestion_bundle_apply_smoke.json -Raw |
  ConvertFrom-Json |
  Select-Object passed, errors, warnings
```

## Dry-run against local suggestion reports

Example with one or more local JSON reports:

```powershell
python .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --suggestion-report .\docs\LOCAL_VALIDATION_EVIDENCE\patch_notes_quality_product_post_patchable_doc_python_probe_20260507-180555.json `
  --output .\output\validation\patch_suggestion_bundle_apply_dry_run.json

Get-Content .\output\validation\patch_suggestion_bundle_apply_dry_run.json -Raw |
  ConvertFrom-Json |
  Select-Object passed, operation_count, changed_count, applied_count, failed_count, manual_review_required, errors, warnings
```

Dry-run must show `applied_count = 0`.

## Apply on PR branch only

Apply only after dry-run is clean and the current branch is the PR branch.

```powershell
git branch --show-current
git status --short

python .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --suggestion-report .\docs\LOCAL_VALIDATION_EVIDENCE\patch_notes_quality_product_post_patchable_doc_python_probe_20260507-180555.json `
  --output .\output\validation\patch_suggestion_bundle_apply.json `
  --apply
```

The tool refuses `--apply` outside branches matching `codex/*` unless explicitly overridden.

## Post-apply validation

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax_after_patch_suggestion_bundle.json

python .\Tools\validation\check_validation_report_contract.py `
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

## Commit and push to PR branch

Do not use `git add .`.

```powershell
git add `
  .\Tools\ai\apply_patch_suggestion_bundle.py `
  .\Tools\validation\run_patch_suggestion_bundle_apply_smoke.py `
  .\docs\LOCAL_AI_TASKS\patch-suggestion-bundle-final-phase.md

git commit -m "feat(ai): apply patch suggestions as final toolbox phase"
git push -u origin codex/apply-python-doc-suggestion-wave1
```

When local suggestion reports produce source/doc edits, add only the reviewed files changed by the tool. Never add `output/**`, `*.db`, `*.sqlite`, `renders/**`, or generated patch bundles.

## Evidence bundle after local apply

After local apply and validation, build compact Git-trackable evidence if needed:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename patch_suggestion_bundle_final_phase_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\validation\patch_suggestion_bundle_apply.json `
  --report .\output\validation\patch_suggestion_bundle_apply_smoke.json `
  --report .\output\validation\python_syntax_after_patch_suggestion_bundle.json `
  --report .\output\validation\validation_report_contract_after_patch_suggestion_bundle.json
```

Commit only the generated compact evidence JSON/MD if it is useful for PR review.
