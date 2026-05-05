# Local AI Run Bootstrap

This file is the first local-run bootstrap for AI assistants working inside a checked-out copy of this repository.

Use it before changing files during local runs. It is intentionally operational and conservative.

## FIRST ENTRY — Unified Local AI 0-to-10

When Carmine asks for any of these phrases, open the unified launcher runbook first:

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
quick test
smoke
full validation
provider run
GPU/NPU run
memory handoff
patch specs
reset
tool promotion
runtime broker telemetry
```

Primary current runbook:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Primary current launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current stable supporting docs:

```text
FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md
```

No other local-AI runner is an active first entrypoint. Supporting wrappers may be called by the launcher, but they must not be used as separate operator paths unless a future PR explicitly promotes them into the launcher manifest/phase contract.

## One-flow rule

All local-AI execution profiles must be modeled as launcher modes, profiles or flags.

This includes:

```text
quick tests
smoke tests
full runs
deep runs
full validation
documentation cleanup
script/tool inventory
provider runs
Ollama advisory
NPU probes
multistep provider workflow
SQLite memory handoff
context packs
semantic chunks
patch-spec generation
runtime broker telemetry
project-tool promotion evidence
reset cleanup
legacy full-toolbox integrated behavior
```

Do not start from these as first entrypoints:

```text
run_local_ai_markdown_task.ps1
run_local_ai_task_via_pipeline.ps1
run_post_validation_ai_packet.ps1
run_parallel_ai_provider_multistep.ps1
run_local_validation_after_refactor.ps1
run_agent_review_full_toolbox_decision_loop_integrated.ps1
full-toolbox-0-to-10-semi-automatic-procedure.md
historical PR handoff or master-branch code-refactor runbooks
```

They are implementation lanes, historical material or scoped helpers behind the unified launcher.

## Current operating chain

```text
unified launcher command from unified-local-ai-refactor-launcher.md
  -> manifest-first run visibility
  -> inventories / reports / context packs / memory packet
  -> workload quality routing when provider is requested
  -> official pipeline adapter when selected
  -> Ollama advisory / primary provider lane when explicitly enabled
  -> multistep provider probes when selected
  -> deterministic recommendations
  -> review-only patch specs / patch bundles
  -> runtime broker report and telemetry
  -> shared production AI-to-AI bundle
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
using a supporting wrapper as an active first entrypoint
triggering audio/media output during AI/tooling runs
```

## Visibility-first rule

Every local AI run must be understandable from compact surfaces before opening detailed evidence.

Required reading order after a run:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
production AI-to-AI bundle
runtime tool telemetry and capability manifest
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

Unified local AI pipeline
  -> heavy local context processing, validators, advisory packets, repository proposals, compact evidence

Human / master AI
  -> approves promotion from advisory/proposal outputs to patch specs, reviewed replacements, apply or merge
```

Codex/GitHub-only AI is not obsolete. It remains useful as a master/control-plane during the transition. The unified local pipeline should take the token-heavy local work and produce report-only/proposal-only artifacts for review.

## Non-interactive entrypoint mode

Local AI runners may be launched without an interactive chat, but the launcher remains the entrypoint.

Use the unified launcher runbook for current commands and flags:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

A local AI runner started from a task file must still read `AGENTS.md` first, then this bootstrap, then the task file. The task file may define task intent, but execution still routes through the unified launcher unless a human explicitly scopes a one-off helper invocation.

## Phase 0 - Repository sync preflight

Before running an AI task locally, confirm:

```text
current branch
remote sync state
working tree state
whether dirty changes are intentional
Python/venv resolution
ignored output/cache/state files are not staged
```

Do not continue if the working tree contains unrelated changes unless the task explicitly covers them or `-AllowDirty` is intentionally supplied to the unified launcher.

## Phase 1 - Mandatory reading set

At the start of every local AI run, read these files in order:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
WORKFLOW.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
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

If a file is missing, report it as missing. Do not invent its contents.

## Phase 2 - Task classification

Classify the task before editing:

| Task class | Allowed scope | Provider execution |
|---|---|---|
| docs/workflow-state | Markdown docs, execution plans, issue/PR handoff notes | No |
| validation/evidence | validators, report-only builders, compact evidence docs | No implicit providers |
| provider diagnostics | explicit-run scripts and diagnostics only | Through launcher provider/probe phases only |
| runtime broker/tooling | broker-safe report-only tools and telemetry | Through launcher/broker only |
| tool promotion | docs, registry, report-only wrappers and safe validation | No implicit providers |
| core AI/backend | app-agnostic AI orchestration and validators | Explicit only when selected |
| unified full 0-to-10 | full evidence -> recommendation -> patch-plan -> patch-bundle process | Provider only through explicit unified launcher command/flag |
| Blender/audio/media runtime | Blender scripts, audio output, FFmpeg, render or encode behavior | Only when explicitly scoped as application-domain work |

When the task is documentation/workflow-state, do not touch Python runtime code unless a validator/doc contract requires it and the reason is documented.

## Phase 3 - Guardrails

Hard exclusions unless the current task explicitly overrides them:

```text
Blender runtime
Audio playback
Audio export
FFmpeg encode or mux operations
Video/media generation
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

Provider execution is valid only with explicit launcher flags and must produce compact evidence or manifests under:

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
launcher mode/profile/flags expected to validate the change
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
audio/media output generation
```

## Phase 6 - Required validation selection

Select validation through the unified launcher whenever possible.

Mapping:

| Need | Launcher route |
|---|---|
| Documentation/workflow-state cleanup | `md,contract,full_validation` phases |
| Quick full loop | `Full0To10` with quick intensity |
| Balanced full loop | `Full0To10` with balanced intensity |
| Deep full loop | `Full0To10` with deep intensity |
| Provider evidence | `Full0To10` or provider mode with explicit provider/probe flags |
| Runtime broker telemetry | `Full0To10` or full-toolbox decision loop with broker telemetry evidence |
| Tool promotion/inventory | `python`, `context_pack`, `agent_state` and report-only validation phases |
| Patch-spec generation | `patch_specs` phase or `Full0To10` default |
| Reset planning/apply | `reset` mode with reset guardrails |
| Script/tool inventory | `python` phase |
| Semantic chunks/context/memory | `chunks`, `context_pack`, `agent_state` phases |
| Audio/media runtime | No default launcher validation path; requires explicit application-domain task. |

Focused validators may still be invoked directly only when the task is explicitly scoped to that validator or when debugging the validator itself.

## Phase 7 - Reporting contract

At the end of a local run, report:

```text
branch name
changed files
line counts for created or modified scripts
launcher mode/profile/flags used
validators or phases run
validator/phase pass/fail summary
manifest path
phase report paths
compact evidence paths, when generated
provider/runtime execution status
runtime broker telemetry status
audio/media output status
patch application status
risks
follow-up recommendations
```

If a validator or launcher phase was not run, say why.

## Phase 8 - PR contract

A local AI-generated PR should include:

```text
summary
scope
changed files
launcher mode/profile/flags or focused validation command
provider execution statement
runtime broker telemetry statement
audio/media output statement
visibility/manifest statement
risk notes
follow-up
```

For docs/workflow-state cleanup PRs, explicitly state:

```text
No runtime files, provider behavior, generated indexes, full analysis JSON, Blender scripts or audio/media outputs touched.
```

## Current local task pointer

The preferred current end-to-end local task is tracked in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

The current P0 validation task is tracked in:

```text
docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md
```

The audio/media output guardrail is tracked in:

```text
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

The expected work is:

```text
exercise the unified full 0-to-10 process with selected modes, evidence collectors, optional GPU/NPU provider run, deterministic recommendations, workload quality routing, memory/context surfaces, runtime broker telemetry, patch-spec generation, review-safe patch bundle generation and explicit apply/validation when authorized
```

GPU/NPU execution remains explicit. Audio/media output remains forbidden unless an explicit application-domain task enables it. If Carmine cannot run the local provider workflow, GitHub-only agents must stop at report-only/docs/validator work and request the exact unified launcher command/evidence bundle needed next.
