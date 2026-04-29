# Workflow

## Purpose

This file is the root operational workflow for `blender-audio-project`.

It is intended for human maintainers and AI agents. It defines the standard path from task selection to validation, index regeneration, commit and review.

## Core principle

Work should move through small, explicit, validated tasks.

```text
read context
  -> choose one task
  -> define scope
  -> change minimal files
  -> run focused validation
  -> regenerate indexes when needed
  -> commit clear result
  -> share proof-of-work reports
```

## Required reading before work

Read in this order:

```text
AGENTS.md
docs/README.md
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
```

For code changes, also read the nearest package/tool README and the target source file.

## Task lifecycle

### 1. Define the task

A task should have:

```text
goal
scope
files likely touched
validation commands
expected output
risk level
```

For non-trivial tasks, create an execution plan under:

```text
docs/EXECUTION_PLANS/active/
```

### 2. Prepare repository

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git status
git pull --rebase origin master
git status
```

If the working tree is not clean before starting, stop and decide whether to commit, stash, or discard the existing changes.

### 3. Make a focused change

Rules:

```text
small scope
no unrelated formatting
no destructive rewrite of stable Blender packages
no generated full-analysis JSON edits
no runtime package migration without validation
```

### 4. Run focused validation

For most repository changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_docs_links.py --repo-root .
```

For AI pipeline changes:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

For longer local validation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

### 5. Regenerate indexes when needed

Regenerate after source, docs, workflow, validation or pipeline changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

### 6. Inspect changes

```powershell
git status
git diff --stat
```

If generated indexes changed, commit them intentionally.

### 7. Commit

Use concise commit messages:

```text
docs: add execution planning workflow
docs: add tech debt tracker
feat(shared): add blender compatibility helper
feat(validation): add markdown local link checker
fix(validation): accept utf-8 bom json artifacts
chore: regenerate ai and npu indexes
```

### 8. Push

```powershell
git push origin master
```

### 9. Share proof of work

For local validation, share:

```powershell
git status
git log --oneline -n 20
Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw
Get-Content .\output\validation\ai_pipeline_modules.json -Raw
Get-Content .\output\validation\refactor_status_consistency.json -Raw
Get-Content .\output\validation\docs_links.json -Raw
```

For workflow-run validation, also share:

```powershell
Get-ChildItem .\output\local_validation -File | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

## Execution plans

Execution plans are used for multi-step work that should not live only in chat history.

Location:

```text
docs/EXECUTION_PLANS/
```

States:

```text
active      work currently planned or in progress
completed   work finished and validated
abandoned   work stopped intentionally
```

## Tech debt tracking

Use:

```text
docs/TECH_DEBT_TRACKER.md
```

Track technical debt when:

```text
there is a known problem
it is not fixed immediately
it affects future agents or maintainers
it requires validation or migration later
```

## AI-agent operating rule

AI agents should not treat conversation history as the only source of truth.

Durable project state should be written into:

```text
docs/
WORKFLOW.md
Tools/validation/
Tools/workflow/
indexAI/
output/*_report.md
```

## Do not do without explicit approval

```text
delete files
rewrite Scripting/v61b/main_v61b.py
split Ready To Jazz monolith
change render output behavior
change FFmpeg final-output behavior
add dependencies
modify full frame-level analysis JSON
run heavy Blender/GPU workloads automatically
change schema-v6 report meanings
```
