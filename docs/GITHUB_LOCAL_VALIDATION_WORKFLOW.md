# GitHub Local Validation Workflow

## Purpose

This document defines the recommended local Git/GitHub workflow after AI-assisted refactoring, documentation updates, or pipeline changes.

It is optimized for this repository's current workflow:

```text
pull latest
run focused validation
run AI pipeline dry-run matrix when needed
regenerate AI/NPU indexes
commit generated indexes only
push results
share reports for review
```

## One-command unattended workflow

For a longer unattended run, use the local runner:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

This script runs the broad local validation batch, including syntax checks, AI pipeline checks, NPU helper smoke/unit checks, generated artifact policies, dry-run matrix checks, package/JSON checks, index regeneration and Git status/diff reporting.

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
```

Use the focused NPU helper workflow before the full runner when working on NPU helper contracts. Use the full runner especially after changes to the modular AI artifact pipeline, shared Blender compatibility helpers or validation workflows.

## Step 1: update local repository

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git pull --rebase origin master
```

For a PR branch:

```powershell
git fetch origin
git checkout <branch>
git pull --ff-only
```

Check state:

```powershell
git status
git log --oneline -n 20
```

Expected before validation:

```text
working tree clean
branch aligned with target remote branch
```

## Step 2: run validation block

Focused NPU helper block when applicable:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

Manual full validation block:

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

AI pipeline reports:

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

## Step 4: regenerate AI/NPU indexes

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

## Step 5: inspect Git changes

```powershell
git status
git diff --stat
```

If validation produced only local output reports, they should normally remain uncommitted unless intentionally tracked.

If only generated AI/NPU indexes changed, continue with Step 6.

If source files changed unexpectedly, stop and review before committing.

## Step 6: commit generated indexes

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

For master:

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
working tree clean
branch up to date with remote
latest commit is index regeneration or intended documentation/source update
```

## What to share for review

Share these outputs:

```powershell
git status
git log --oneline -n 20
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
