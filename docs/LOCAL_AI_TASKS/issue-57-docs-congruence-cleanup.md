# Local AI Entrypoint: Issue 57 Docs Congruence Cleanup

This is a non-interactive task file for a local AI runner.

The human may launch a local command that points the AI runner at this Markdown file. The AI must not require additional chat instructions to start.

## Absolute first instruction

Before planning, editing, validating or opening a PR, read and obey these files in order:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

Then read this task file again and continue from the task contract below.

If the local AI cannot read `AGENTS.md` or `docs/LOCAL_AI_RUN_BOOTSTRAP.md`, it must stop and report the missing file. It must not infer their contents.

## Task source

GitHub issue:

```text
#57 - Local AI task: docs congruence cleanup after selective planner merge
```

Repository:

```text
C-F-tek/blender-audio-project
```

Start from updated `master`.

## Required local git preflight

Run or verify equivalent state:

```powershell
git status
git branch --show-current
git fetch origin
git switch master
git pull --ff-only origin master
```

Create a task branch if not already on one:

```powershell
git switch -c codex/docs-congruence-cleanup
```

Stop if the working tree contains unrelated changes.

## Task classification

```text
docs/workflow-state
```

Provider execution is not required.

GPU/NPU execution is not required.

## Goal

Move completed execution plans from `docs/EXECUTION_PLANS/active/` to `docs/EXECUTION_PLANS/completed/`, update their status fields, and validate documentation/execution-plan congruence.

Known target:

```text
docs/EXECUTION_PLANS/active/2026-05-01_selective_planner_prototype.md
```

Expected destination:

```text
docs/EXECUTION_PLANS/completed/2026-05-01_selective_planner_prototype.md
```

## Required content update

In the moved file, set or add:

```text
Status: completed
Date: 2026-05-01
Completed: 2026-05-01
```

Add a concise completion summary referencing:

```text
PR #55
merge commit f88c8453e0945bcb117372a3aa62e597010f030f
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_selective_planner_real_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_selective_planner_real_evidence.md
```

Preserve the existing validation commands and guardrail notes unless they are stale or contradicted by the completion state.

## Allowed changes

Allowed:

```text
move completed execution-plan Markdown files
update execution-plan status fields
add completion summaries
fix local Markdown links caused by the move
update documentation indexes only if needed for link/congruence correctness
```

## Forbidden changes

Do not touch:

```text
Blender runtime
Ready To Jazz
Scripting/shared/blender_compat.py
full analysis JSON
generated indexes manually
provider behavior
prompt prose
models
temperatures
provider orchestration
source runtime code unrelated to documentation validation
```

Do not execute providers implicitly.

Do not run Blender or FFmpeg.

## Required validation

Run:

```powershell
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

Optional:

```powershell
git status
git diff --stat
```

## Acceptance criteria

- `docs/EXECUTION_PLANS/active/2026-05-01_selective_planner_prototype.md` no longer exists.
- `docs/EXECUTION_PLANS/completed/2026-05-01_selective_planner_prototype.md` exists.
- The moved plan has `Status: completed`.
- `check_execution_plan_status.py` passes.
- `check_docs_links.py` passes, or any warnings are documented as non-blocking and unrelated to the move.
- `check_validation_report_contract.py` passes, or any warnings are documented as non-blocking and unrelated to the move.
- `git diff --check` passes.
- No runtime/provider/generated-index/full-analysis files are changed.

## Expected PR report

Open a small PR with:

```text
Title: docs(plan): complete selective planner execution plan
Scope: docs/workflow-state only
Changed files
Validation commands and pass/fail summary
Provider execution statement: not performed / not required
Risk: low
Follow-up: none unless validators report warnings
```

## Stop conditions

Stop and report if:

```text
AGENTS.md is missing
LOCAL_AI_RUN_BOOTSTRAP.md is missing
the target active execution plan is missing and no completed equivalent exists
a validator reports an error that requires touching forbidden files
the task would require provider execution
unrelated local changes are present
```

## Final local report

At the end, report:

```text
branch name
changed files
validator results
whether providers were executed
whether runtime/generated-index/full-analysis files were touched
PR URL, if opened
```
