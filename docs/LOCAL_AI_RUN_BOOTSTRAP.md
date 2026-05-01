# Local AI Run Bootstrap

This file is the first local-run bootstrap for AI assistants working inside a checked-out copy of this repository.

Use it before changing files during local runs. It is intentionally operational and conservative.

## Purpose

The local AI should autonomously read the current task context and repository guardrails before planning or editing.

The bootstrap prevents these common failures:

```text
starting from stale context
editing runtime files during documentation/backend tasks
running providers implicitly
forgetting active execution plans
forgetting compact evidence bundles
mixing GitHub-only review with local workstation evidence
```

## Phase 0 - Repository sync preflight

Before running an AI task locally, the human or local AI should confirm:

```powershell
git status
git branch --show-current
git fetch origin
```

For new task branches, start from updated `master`:

```powershell
git switch master
git pull --ff-only origin master
git switch -c <task-branch>
```

Do not continue if the working tree contains unrelated changes unless the task explicitly covers them.

## Phase 1 - Mandatory reading set

At the start of every local AI run, read these files in order:

```text
AGENTS.md
WORKFLOW.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/README.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
docs/EXECUTION_PLANS/README.md
docs/TECH_DEBT_TRACKER.md
```

Then read the active task object:

```text
GitHub issue, PR body or execution plan referenced by the user
```

For the current post-PR #55 cleanup task, read:

```text
https://github.com/C-F-tek/blender-audio-project/issues/57
docs/EXECUTION_PLANS/active/2026-05-01_selective_planner_prototype.md
docs/AI_SELECTIVE_PLANNER.md
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_selective_planner_real_evidence.md
```

If a file is missing, report it as missing. Do not invent its contents.

## Phase 2 - Task classification

Classify the task before editing:

| Task class | Allowed scope | Provider execution |
|---|---|---|
| docs/workflow-state | Markdown docs, execution plans, issue/PR handoff notes | No |
| validation/evidence | validators, report-only builders, compact evidence docs | No implicit providers |
| provider diagnostics | explicit-run scripts and diagnostics only | Explicit only |
| core AI/backend | app-agnostic AI orchestration and validators | Explicit only when requested |
| Blender runtime | Blender scripts and scene behavior | Only when explicitly scoped |

When the task is documentation/workflow-state, do not touch Python runtime code unless a validator/doc contract requires it and the reason is documented.

## Phase 3 - Guardrails

Hard exclusions unless the current task explicitly overrides them:

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
production render/deploy actions
```

Do not execute Ollama/OpenVINO/GPU/NPU providers implicitly.

Provider execution is valid only with explicit local commands and must produce compact evidence under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

## Phase 4 - Planning contract

Before modifying files, produce a small plan with:

```text
task class
files expected to change
files that must not change
validators to run
expected output paths
stop conditions
```

Stop if the task would require destructive git operations, provider promotion, production deployment, secrets, billing, repository visibility changes, force-push or merge to protected branches.

## Phase 5 - Change policy

Prefer additive or narrow edits.

Allowed for docs/workflow-state tasks:

```text
move completed execution plans from active/ to completed/
update Status fields
add completion summaries
fix local Markdown links
update docs index entries when a stable doc exists
```

Not allowed for docs/workflow-state tasks:

```text
source-code refactors
runtime behavior changes
provider prompt/model/temperature changes
manual generated-index edits
full analysis JSON edits
```

## Phase 6 - Required validation selection

Select the smallest relevant validator set.

For documentation/workflow-state cleanup:

```powershell
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

For selective-planner output validation:

```powershell
python .\Tools\ai\build_selective_execution_plan.py --repo-root . --output .\output\ai_pipeline\selective_execution_plan.json --markdown-output .\output\ai_pipeline\selective_execution_plan.md
python .\Tools\validation\check_selective_execution_plan.py --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json
```

For real GPU/NPU evidence, only when explicitly requested by Carmine:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 `
  -Profile npu `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -Basename <basename> `
  -ProposalBasename <proposal-basename> `
  -EvidenceBasename <evidence-basename>

python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename <evidence-basename>
python .\Tools\validation\check_github_evidence_bundle.py --repo-root . --output .\output\validation\github_evidence_bundle.json
```

## Phase 7 - Reporting contract

At the end of a local run, report:

```text
branch name
changed files
line counts for created or modified scripts
validators run
validator pass/fail summary
compact evidence paths, when generated
risks
follow-up recommendations
```

If a validator was not run, say why.

## Phase 8 - PR contract

A local AI-generated PR should include:

```text
summary
scope
changed files
validation commands and results
provider execution statement
risk notes
follow-up
```

For docs/workflow-state cleanup PRs, explicitly state:

```text
No runtime files, provider behavior, generated indexes, full analysis JSON or Blender scripts touched.
```

## Current local task pointer

The current cleanup task is tracked in:

```text
GitHub issue #57
```

The expected work is:

```text
move the selective planner execution plan from active/ to completed/
update status fields
run documentation congruence and execution-plan validators
open a small docs/workflow-state PR
```

No GPU/NPU run is required for issue #57.
