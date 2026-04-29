# GitHub Local Validation Workflow

## Purpose

This document defines the recommended local Git/GitHub workflow after AI-assisted refactoring, documentation updates, or pipeline changes.

It is optimized for this repository's current workflow:

```text
pull latest
run focused validation
run AI pipeline dry-run matrix
regenerate AI/NPU indexes
commit generated indexes only
push results
share reports for review
```

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
```

Use it especially after changes to the modular AI artifact pipeline or shared Blender compatibility helpers.

## Step 1: update local repository

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git pull --rebase origin master
```

Check state:

```powershell
git status
git log --oneline -n 20
```

Expected before validation:

```text
working tree clean
branch aligned with origin/master
```

## Step 2: run validation block

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

## Step 3: inspect AI pipeline reports

```powershell
Get-Content .\output\validation\ai_pipeline_modules.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw
```

The Markdown report is intended for quick human review. The JSON report remains the machine-readable source.

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

```powershell
git push origin master
```

Confirm:

```powershell
git status
git log --oneline -n 20
```

Expected final state:

```text
working tree clean
branch up to date with origin/master
latest commit is index regeneration or intended documentation/source update
```

## What to share for review

Share these outputs:

```powershell
git status
git log --oneline -n 20
Get-Content .\output\validation\ai_pipeline_modules.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.json -Raw
Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw
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

### Index generation emits warnings

Warnings should be reviewed but are not always blocking. If a syntax warning appears, inspect the generated manifest for `syntax_warnings`.

## Policy

Do not push generated indexes before checking validation results.

Do not commit output validation reports unless explicitly needed.

Do not modify Blender runtime packages while validating AI pipeline refactors.
