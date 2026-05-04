# Local AI Run Bootstrap

This file is the first local-run bootstrap for AI assistants working inside a checked-out copy of this repository.

Use it before changing files during local runs. It is intentionally operational and conservative.

## FIRST ENTRY — Unified Local AI 0-to-10

When Carmine asks for any of these phrases, this is the first procedure to open and follow:

```text
Tutto su tutto
full toolbox
0-10
cassetta degli attrezzi completa
multi-macro patch
multi-script
multi-fase
semi-automatic process
flusso unico
run completa
```

Primary current runbook:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Primary current launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Canonical full run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Quick 5-minute style run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

The current operating chain is:

```text
unified launcher command
  -> manifest-first run visibility
  -> inventories / reports / context packs / memory packet
  -> workload quality routing when provider is requested
  -> official pipeline adapter
  -> Ollama advisory / primary provider lane when explicitly enabled
  -> multistep provider probes when selected
  -> deterministic recommendations
  -> review-only patch specs / patch bundles
  -> explicit apply only after review
  -> validation
  -> PR
```

Full toolbox body model remains valid, but it is now driven by the unified launcher:

```text
Skeleton / contracts
Nervous system / orchestration
Brain / decision layer
Eyes / evidence collectors
Immune system / validators
Memory / SQLite-backed local state when enabled
Muscles / patch bundle apply lane only after explicit review
Bloodstream / compact evidence
Hands / GitHub + CLI
```

Do not start from `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` or `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md` as active entrypoints. They remain historical/supporting references for older validation semantics.

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
opening huge evidence bundles before the manifest/summary
starting from superseded 0-to-10 runbooks
```

## Visibility-first rule

Every local AI run must be understandable from compact surfaces before opening detailed evidence.

Required reading order after a run:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
compact Markdown or CSV summaries
detailed evidence only when needed
```

A run is not operationally clear if the next agent must open a giant bundle to understand what happened.

Do not create new monolithic AI-to-AI bundles without a companion manifest/summary.

## Length policy for local-run docs and evidence

```text
Active operator runbook: prefer ~500 lines or less.
Maintained source docs: prefer ~700 lines or less.
Generated compact evidence: prefer ~1200 lines or less.
Large evidence/historical bundles: allowed only when indexed and never as first entrypoint.
```

Long Markdown files must be classified by the Markdown inventory and either summarized, split, marked historical/evidence or kept out of the primary reading path.

## Hybrid master-AI / local-pipeline model

The current operating model is hybrid.

```text
Chat / GitHub-only AI / Codex-style control plane
  -> strategic planning, review, issue/PR orchestration, small edits, human-facing summaries

Local AI/NPU prototype pipeline
  -> heavy local context processing, validators, advisory packets, repository proposals, compact evidence

Human / master AI
  -> approves promotion from advisory/proposal outputs to patch specs, reviewed replacements, apply or merge
```

Codex/GitHub-only AI is not obsolete. It remains useful as a master/control-plane during the transition. The local pipeline should take the token-heavy local work and produce report-only/proposal-only artifacts for review.

## Non-interactive entrypoint mode

Local AI runners may be launched without an interactive chat.

For unified full runs, prefer:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b
```

For task-scoped adapter runs, pass a Markdown task file from:

```text
docs/LOCAL_AI_TASKS/
```

Current task index:

```text
docs/LOCAL_AI_TASKS/README.md
```

Task-scoped project-owned runner path:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_markdown_task.ps1 `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskBranch codex/full-context-ai-npu-golden-run `
  -RunnerCommand 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"'
```

A local AI runner started from a task file must still read `AGENTS.md` first, then this bootstrap, then the task file.

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

Do not continue if the working tree contains unrelated changes unless the task explicitly covers them or `-AllowDirty` is intentionally supplied to the unified launcher.

## Phase 1 - Mandatory reading set

At the start of every local AI run, read these files in order:

```text
AGENTS.md
WORKFLOW.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

Then continue with:

```text
docs/EXECUTION_PLANS/README.md
docs/TECH_DEBT_TRACKER.md
```

Then read the active task object:

```text
GitHub issue, PR body, execution plan or docs/LOCAL_AI_TASKS/*.md file referenced by the runner
```

For the current full-context golden path task, read:

```text
docs/LOCAL_AI_TASKS/full-context-ai-npu-golden-path.md
Tools/workflow/run_local_ai_markdown_task.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
docs/LOCAL_AI_WORKFLOW.md
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
| unified full 0-to-10 | full evidence -> recommendation -> patch-plan -> patch-bundle process | Provider only through explicit unified launcher command/flag |
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

Provider execution is valid only with explicit local commands and must produce compact evidence or manifests under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
output/local_ai_runs/
output/ai_pipeline/
output/validation/
```

`output/**` remains ignored/local unless compact evidence is intentionally promoted to a tracked documentation path.

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
update unified launcher documentation and visibility/length policy
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

For unified full 0-to-10 local runs, use:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b
```

For a quick full run, use:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b
```

For local pipeline runner validation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 `
  -PromptFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -TaskFile .\docs\LOCAL_AI_TASKS\full-context-ai-npu-golden-path.md `
  -RunDir .\output\local_ai_runs\full_context_golden_adapter_smoke `
  -DryRun
```

For selective-planner output validation:

```powershell
python .\Tools\ai\build_selective_execution_plan.py --repo-root . --output .\output\ai_pipeline\selective_execution_plan.json --markdown-output .\output\ai_pipeline\selective_execution_plan.md
python .\Tools\validation\check_selective_execution_plan.py --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json
```

For real GPU/NPU evidence, only when explicitly requested by Carmine and preferably through the unified launcher:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -UsePrimaryAdvisoryProvider `
  -Model gpt-oss:20b
```

The legacy multistep provider wrapper remains available as supporting detail, but it should not be the first entrypoint for a full 0-to-10 flow:

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
```

## Phase 7 - Reporting contract

At the end of a local run, report:

```text
branch name
changed files
line counts for created or modified scripts
validators run
validator pass/fail summary
manifest path
phase report paths
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
visibility/manifest statement
risk notes
follow-up
```

For docs/workflow-state cleanup PRs, explicitly state:

```text
No runtime files, provider behavior, generated indexes, full analysis JSON or Blender scripts touched.
```

## Current local task pointer

The preferred current end-to-end local task is tracked in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

The expected work is:

```text
exercise the unified full 0-to-10 process with selected modes, evidence collectors, optional GPU/NPU provider run, deterministic recommendations, workload quality routing, memory/context surfaces, patch-spec generation, review-safe patch bundle generation and explicit apply/validation when authorized
```

GPU/NPU execution remains explicit. If Carmine cannot run the local provider workflow, GitHub-only agents must stop at report-only/docs/validator work and request the exact local command/evidence bundle needed next.
