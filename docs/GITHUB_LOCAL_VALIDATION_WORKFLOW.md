# GitHub Local Validation Workflow

## Purpose

This document defines the recommended local Git/GitHub workflow after AI-assisted refactoring, documentation updates, or pipeline changes.

It is optimized for the current IA-Carmine workflow:

```text
pull latest
choose unified launcher mode/intensity
run focused validation or full 0-to-10 flow
inspect manifest-first outputs
promote only compact evidence when needed
commit intended docs/source/index changes
push results
share reports for review
```

## Primary one-command workflow

Use the unified launcher as the primary local validation and local-AI orchestration entrypoint:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b
```

Quick validation/docs run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode md,python,contract,full_validation `
  -RunIntensity quick
```

Dry-run check for launcher planning:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -DryRun `
  -SkipGitSync `
  -NoBranch `
  -AllowDirty
```

The primary run artifact is:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

Read this manifest before opening long reports.

## Supporting legacy validation wrapper

The older validation wrapper remains available as a supporting focused tool:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

Use this when explicitly validating the legacy validation batch itself or when the unified launcher delegates to it.

It writes logs and summaries under:

```text
output/local_validation/
```

It does not commit or push automatically.

Use this variant when the repository is already pulled and you do not want the script to call Git:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError
```

## Focused NPU helper validation

For changes under `Tools/npu/pipeline/`, `Tools/validation/check_npu_pipeline_*.py`, or the NPU decomposition docs, run the focused workflow first:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

This workflow runs:

```text
NPU helper import/contract smoke
NPU helper unit-test report
NPU helper documentation/module alignment
Python syntax validation
```

Expected reports:

```text
output/validation/npu_pipeline_modules.json
output/validation/npu_pipeline_helper_tests.json
output/validation/npu_pipeline_docs.json
output/validation/python_syntax.json
```

It does not execute Blender, NPU, GPU, Ollama, FFmpeg or provider calls.

## When to use this workflow

Use it after changes to:

```text
AGENTS.md
README.md
docs/
Scripting/shared/
Tools/ai/
Tools/ai/pipeline/
Tools/validation/
Tools/npu/
Tools/npu/pipeline/
Tools/workflow/
```

Use focused NPU helper workflow before the full runner when working on NPU helper contracts. Use the unified launcher for broad validation and full local-AI evidence flows.

## Visibility-first rule

Every run must be reviewed in this order:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
compact Markdown or CSV summaries
detailed evidence only when needed
```

Do not begin review from a long bundle.

## Step 1: update local repository

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git fetch origin
git status --short
```

For master:

```powershell
git switch master
git pull --ff-only origin master
```

For a PR branch:

```powershell
git switch <branch>
git pull --ff-only
```

Check state:

```powershell
git status
git log --oneline -n 20
```

Expected before validation:

```text
working tree clean or intentionally dirty with -AllowDirty
branch aligned with target remote branch
```

## Step 2: run validation block

Preferred unified block:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode md,json,python,chunks,context_pack,agent_state,official,contract,full_validation `
  -RunIntensity quick
```

Focused NPU helper block when applicable:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

Manual full validation block remains available when debugging individual validators:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_model_json.py --repo-root . --output .\output\validation\ai_model_json.json
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_modules.py --repo-root . --output .\output\validation\npu_pipeline_modules.json
python .\Tools\validation\check_npu_pipeline_helper_tests.py --repo-root . --output .\output\validation\npu_pipeline_helper_tests.json
python .\Tools\validation\check_npu_pipeline_docs.py --repo-root . --output .\output\validation\npu_pipeline_docs.json
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy.json
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

## Step 3: inspect reports

Primary inspection:

```powershell
$ManifestPath = Get-ChildItem .\output\local_ai_runs -Recurse -Filter unified_local_ai_refactor_manifest.json |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1 -ExpandProperty FullName

Get-Content $ManifestPath -Raw | ConvertFrom-Json | Select-Object mode, full_0_to_10_requested, run_intensity, provider_execution_requested, quality_gate_passed, phase_reports, errors, warnings
```

Focused AI pipeline reports:

```powershell
Get-Content .\output\validation\ai_pipeline_modules.json -Raw
Get-Content .\output\validation\generated_python_policy.json -Raw
Get-Content .\output\validation\generated_artifact_path_policy.json -Raw
Get-Content .\output\validation\generated_blender_script_policy.json -Raw
Get-Content .\output\validation\ai_dry_run_matrix_contract.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw
```

NPU helper reports:

```powershell
Get-Content .\output\validation\npu_pipeline_modules.json -Raw
Get-Content .\output\validation\npu_pipeline_helper_tests.json -Raw
Get-Content .\output\validation\npu_pipeline_docs.json -Raw
```

The Markdown reports are intended for quick human review. JSON reports remain the machine-readable source.

For individual dry-run cases:

```powershell
Get-ChildItem .\output\ai_pipeline\dry_run_matrix -Recurse -Filter ai_pipeline_dry_run_report.json
```

Important report fields:

```text
passed
summary
schedule
lanes
guardrail_remediation_loop
steps
```

## Step 4: regenerate AI/NPU indexes only when needed

Generated indexes are not source-of-truth docs. Regenerate only when structural/code changes require it:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

Expected generated files:

```text
indexAI/project_code_index.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
Tools/npu/npu_code_manifest.json
```

Generated chunk folders may also change:

```text
indexAI/project_code_chunks/
Tools/npu/npu_code_chunks/
```

Policy:

```text
Do not hand-edit generated indexes.
Do not commit generated chunks unless repository policy for that path explicitly tracks them.
Do not regenerate indexes just because a docs-only PR ran validation.
```

## Step 5: inspect Git changes

```powershell
git status
git diff --stat
git diff --check
```

If validation produced only local output reports, they should normally remain uncommitted.

If generated indexes changed, commit them only when intentional and useful for review.

If source files changed unexpectedly, stop and review before committing.

## Step 6: commit intended changes

For documentation/source changes:

```powershell
git add <intended-files>
git commit -m "<scope>: <message>"
```

For intentional generated AI/NPU index regeneration:

```powershell
git add Tools/npu/npu_code_context.md `
        Tools/npu/npu_code_index.md `
        Tools/npu/npu_code_manifest.json `
        indexAI/project_code_index.md `
        indexAI/project_code_manifest.json

git commit -m "chore: regenerate ai and npu indexes"
```

If chunks are tracked and changed, inspect `git status` and add them intentionally.

## Step 7: push

For master, only after explicit approval when required by project guardrails:

```powershell
git push origin master
```

For a feature branch or PR branch:

```powershell
git push origin <branch>
```

Confirm:

```powershell
git status
git log --oneline -n 20
```

Expected final state:

```text
working tree clean except intentionally ignored local artifacts
branch up to date with remote
latest commit is intended documentation/source/index update
```

## What to share for review

Share these first:

```powershell
git status
git log --oneline -n 20
$ManifestPath
Get-Content $ManifestPath -Raw
```

Then share focused reports if relevant:

```powershell
Get-Content .\output\validation\ai_pipeline_modules.json -Raw
Get-Content .\output\validation\npu_pipeline_modules.json -Raw
Get-Content .\output\validation\npu_pipeline_helper_tests.json -Raw
Get-Content .\output\validation\npu_pipeline_docs.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw
Get-ChildItem .\output\local_validation -File | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

If any dry-run failed, also share the failed case report:

```powershell
Get-Content .\output\ai_pipeline\dry_run_matrix\<case>\ai_pipeline_dry_run_report.json -Raw
```

## Optional Blender compatibility smoke check

`Scripting/shared/blender_compat.py` is intentionally import-safe outside Blender, but its Blender-facing functions require `bpy`.

Normal Python validation should compile it:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
```

Manual Blender validation can be done later in a disposable scene by testing:

```text
create_sound_strip
clear_sequence_editor
set_frame_range_from_seconds
safe_create_noise_texture_node
```

Do not migrate runtime package code to `blender_compat.py` before this manual Blender validation.

A non-invasive smoke helper is available:

```powershell
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
```

Outside Blender it only validates import safety and marks runtime checks as skipped. Run the same script with Blender Python or `blender --background --python` to validate audio-strip and node behavior.

## Troubleshooting

### `git commit` says nothing to commit

This is fine if indexes did not change.

Check:

```powershell
git status
git diff --stat
```

### Dry-run matrix fails

Run with continued execution to collect all failures:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

Then inspect:

```powershell
Get-Content .\output\ai_pipeline\dry_run_matrix_report.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw
```

### Pipeline module smoke validator fails

Inspect:

```powershell
Get-Content .\output\validation\ai_pipeline_modules.json -Raw
```

Most likely failure classes:

```text
import path issue
schema/report mismatch
step builder mismatch
entrypoint import issue
```

### NPU helper validation fails

Run the focused workflow first:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

Then inspect:

```powershell
Get-Content .\output\validation\npu_pipeline_modules.json -Raw
Get-Content .\output\validation\npu_pipeline_helper_tests.json -Raw
Get-Content .\output\validation\npu_pipeline_docs.json -Raw
```

Most likely failure classes:

```text
helper import/export mismatch
fixture contract drift
README/module map drift
legacy compatibility alias mismatch
migration readiness gate mismatch
```

### Index generation emits warnings

Warnings should be reviewed but are not always blocking. If a syntax warning appears, inspect the generated manifest for `syntax_warnings`.

## Policy

Do not push generated indexes before checking validation results.

Do not commit output validation reports unless explicitly needed.

Do not modify Blender runtime packages while validating AI pipeline or NPU helper refactors.

Do not wire `Tools/npu/pipeline/` helpers into `Tools/npu/run_dual_ai_pipeline.py` until focused NPU helper validation, full local validation and index regeneration pass.

Do not treat push-capable workflow helpers as default validation commands. Any push-capable helper must require explicit user intent and visible git status review.
