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

## Project Python and environment

Use the same interpreter contract used by the Python full-toolbox engine:

```text
IA_CARMINE_PYTHON
```

Recommended local resolver:

```powershell
if (-not $env:IA_CARMINE_PYTHON) {
  if (Test-Path .\.venv\Scripts\python.exe) {
    $env:IA_CARMINE_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
  } elseif (Test-Path .\venv\Scripts\python.exe) {
    $env:IA_CARMINE_PYTHON = (Resolve-Path .\venv\Scripts\python.exe).Path
  } elseif (Test-Path .\.venv314\Scripts\python.exe) {
    $env:IA_CARMINE_PYTHON = (Resolve-Path .\.venv314\Scripts\python.exe).Path
  } else {
    $env:IA_CARMINE_PYTHON = "python"
  }
}

$ProjectPython = $env:IA_CARMINE_PYTHON
& $ProjectPython --version
```

Do not use a random shell `python` if `IA_CARMINE_PYTHON` is already set.

## Stamp-driven rule

Use the same Python workflow parameter used by the full-toolbox engine:

```text
--Stamp
```

The final phase internally applies the same compact artifact-stamp normalization used by:

```text
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py
compact_artifact_stamp()
```

Example:

```powershell
$Stamp = "post_patchable_doc_python_probe_20260507-180555"
```

Do not hardcode one specific report filename such as:

```text
patch_notes_quality_product_post_patchable_doc_python_probe_20260507-180555.json
```

Instead, pass `--Stamp $Stamp` and let the tool discover matching local JSON reports under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
output/patch_specs/
output/validation/
output/ai_pipeline/
output/ai_packets/
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
& $ProjectPython .\Tools\validation\run_patch_suggestion_bundle_apply_smoke.py `
  --repo-root . `
  --output .\output\validation\patch_suggestion_bundle_apply_smoke.json

Get-Content .\output\validation\patch_suggestion_bundle_apply_smoke.json -Raw |
  ConvertFrom-Json |
  Select-Object passed, smoke_stamp, discovered_reports, errors, warnings
```

## Find the canonical Stamp

Prefer the exact `--Stamp` value used for the full-toolbox run. If you need to infer it from local outputs, inspect recent full-toolbox files:

```powershell
Get-ChildItem `
  .\docs\LOCAL_VALIDATION_EVIDENCE, `
  .\output\patch_specs, `
  .\output\validation, `
  .\output\ai_pipeline, `
  .\output\ai_packets `
  -Recurse `
  -Filter *.json `
  -ErrorAction SilentlyContinue |
Where-Object {
  $_.Name -match 'full_toolbox|patch|suggest|proposal|recommend|plan|agent_review'
} |
Sort-Object LastWriteTime -Descending |
Select-Object -First 40 LastWriteTime, FullName |
Format-Table -AutoSize
```

For the post-patchable probe run, use the full artifact stamp prefix:

```powershell
$Stamp = "post_patchable_doc_python_probe_20260507-180555"
```

Using only the trailing time fragment can work for simple filenames, but `--Stamp` should match the Python workflow stamp whenever possible.

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
    discovered_reports, `
    operation_count, `
    changed_count, `
    applied_count, `
    failed_count, `
    manual_review_required, `
    errors, `
    warnings
```

Dry-run must show:

```text
applied_count = 0
```

If `discovered_report_count = 0`, the stamp is wrong or the run artifacts are not present locally.

## Apply on PR branch only

Apply only after dry-run is clean and the current branch is the PR branch.

```powershell
git branch --show-current
git status --short

& $ProjectPython .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --Stamp $Stamp `
  --output .\output\validation\patch_suggestion_bundle_apply.json `
  --apply
```

The tool refuses `--apply` outside branches matching `codex/*` unless explicitly overridden.

## Optional: explicit reports plus Stamp

You can combine explicit reports with stamp discovery:

```powershell
& $ProjectPython .\Tools\ai\apply_patch_suggestion_bundle.py `
  --repo-root . `
  --Stamp $Stamp `
  --suggestion-report .\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.json `
  --output .\output\validation\patch_suggestion_bundle_apply_dry_run.json
```

Explicit missing report paths still fail fast. Stamp discovery avoids hardcoded timestamped filenames.

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
$EvidenceStamp = Get-Date -Format "yyyyMMdd-HHmmss"

& $ProjectPython .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename patch_suggestion_bundle_final_phase_$EvidenceStamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\validation\patch_suggestion_bundle_apply.json `
  --report .\output\validation\patch_suggestion_bundle_apply_smoke.json `
  --report .\output\validation\python_syntax_after_patch_suggestion_bundle.json `
  --report .\output\validation\validation_report_contract_after_patch_suggestion_bundle.json
```

Commit only the generated compact evidence JSON/MD if it is useful for PR review.
