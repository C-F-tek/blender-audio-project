# Workflow

## Purpose

This file is the root operational workflow for `blender-audio-project`.

It is intended for human maintainers and AI agents. It defines the standard path from task selection to validation, post-validation AI work-packet generation, index regeneration, commit and review.

## Core principle

Work should move through small, explicit, validated tasks.

```text
read context
  -> choose one task
  -> define scope
  -> change minimal files
  -> run focused validation
  -> build post-validation AI work packet when useful
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
docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
```

For NPU helper/backend work, also read:

```text
Tools/npu/pipeline/README.md
Tools/validation/README.md
docs/EXECUTION_PLANS/README.md
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

For master work:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git status
git pull --rebase origin master
git status
```

For PR branch work:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git fetch origin
git checkout <branch>
git pull --ff-only
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
no provider/model execution behavior changes unless explicitly scoped
```

### 4. Run focused validation

For most repository changes:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
python .\Tools\validation\check_docs_links.py --repo-root .
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
```

For AI pipeline changes:

```powershell
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\validation\check_refactor_status_consistency.py --repo-root . --output .\output\validation\refactor_status_consistency.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

For NPU helper/backend changes:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

For generated Python or generated-file policy changes:

```powershell
python .\Tools\validation\check_generated_python_policy.py --repo-root . --output .\output\validation\generated_python_policy.json
python .\Tools\validation\check_generated_blender_script_policy.py --repo-root . --output .\output\validation\generated_blender_script_policy.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --output .\output\validation\generated_artifact_path_policy.json
```

For longer local validation:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
```

The full runner now builds an advisory post-validation AI work packet by default.

### 5. Build post-validation AI work packet

For a standalone advisory packet after manual tests:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1
```

Optional local Ollama draft:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -UseOllama
```

Generated files:

```text
output/ai_pipeline/repository_update_suggestions.json
output/ai_pipeline/repository_update_suggestions.md
```

Policy:

```text
advisory only
no auto-apply
no source modification
no provider execution unless -UseOllama is explicitly passed
```

### 6. Regenerate indexes when needed

Regenerate after source, docs, workflow, validation or pipeline changes:

```powershell
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

### 7. Inspect changes

```powershell
git status
git diff --stat
```

If generated indexes changed, commit them intentionally.

### 8. Commit

Use concise commit messages:

```text
docs: add execution planning workflow
docs: add tech debt tracker
feat(shared): add blender compatibility helper
feat(validation): add markdown local link checker
fix(validation): accept utf-8 bom json artifacts
test(npu): validate helper package locally
chore: regenerate ai and npu indexes
```

### 9. Push

For master:

```powershell
git push origin master
```

For a PR branch:

```powershell
git push origin <branch>
```

### 10. Share proof of work

For local validation, share:

```powershell
git status
git log --oneline -n 20
Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw
Get-Content .\output\ai_pipeline\repository_update_suggestions.md -Raw
Get-Content .\output\validation\ai_pipeline_modules.json -Raw
Get-Content .\output\validation\npu_pipeline_modules.json -Raw
Get-Content .\output\validation\npu_pipeline_helper_tests.json -Raw
Get-Content .\output\validation\execution_plan_status.json -Raw
Get-Content .\output\validation\npu_pipeline_docs.json -Raw
Get-Content .\output\validation\generated_python_policy.json -Raw
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

Folder/status consistency is enforced by:

```powershell
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
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

The post-validation AI work packet is the preferred local handoff artifact after tests.

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
change NPU/Ollama provider execution behavior
```
