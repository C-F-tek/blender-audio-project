<!-- IA-CARMINE-MD-SPLIT: part -->
# LOCAL_AI_RUN_BOOTSTRAP — parte 002 di 002

Sorgente indice: [`../LOCAL_AI_RUN_BOOTSTRAP.md`](../LOCAL_AI_RUN_BOOTSTRAP.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Phase 1 - Mandatory reading set

At the start of every local AI run, read these files in order:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
WORKFLOW.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
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
| validation/evidence | validators, report-only builders, compact evidence docs | No implicit providers outside Full0To10/provider-selected flows |
| provider diagnostics | explicit-run scripts and diagnostics only | Through launcher provider/probe phases only |
| runtime broker/tooling | broker-safe report-only tools and telemetry | Through launcher/broker only |
| tool promotion | docs, registry, report-only wrappers and safe validation | No implicit providers outside Full0To10/provider-selected flows |
| core AI/backend | app-agnostic AI orchestration and validators | Full0To10/provider-selected flows are opt-out by lane |
| unified run unica / Full0To10 | full evidence -> recommendation -> patch-plan -> patch-bundle process | Provider/probe/workload-quality lanes included by default unless disabled/unavailable |
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
prompt prose
models
temperatures
production render/deploy actions
```

Do not execute Ollama/OpenVINO/GPU/NPU providers outside Full0To10/provider-selected workflows.

Provider execution is valid when the operator selects `-Full0To10` or provider/probe modes, and must produce compact evidence or manifests under:

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
| Quick run unica | `Full0To10` with quick intensity parameters |
| Balanced run unica | `Full0To10` with balanced intensity parameters |
| Deep run unica | `Full0To10` with deep intensity parameters |
| Custom run unica | `Full0To10` with explicit operator parameters |
| Provider evidence | `Full0To10` or provider mode; provider/probe/workload-quality lanes included unless disabled/unavailable |
| Runtime broker telemetry | `Full0To10` or full-toolbox decision loop with broker telemetry evidence |
| Tool promotion/inventory | `python`, `context_pack`, `agent_state` and report-only validation phases |
| Patch-spec generation | `patch_specs` phase or `Full0To10` default |
| Reset planning/apply | `reset` mode with reset guardrails |
| Script/tool inventory | `python` phase |
| Semantic chunks/context/memory | `chunks`, `context_pack`, `agent_state` phases |
| Discovery/index/CSV-count evidence | inventory, chunks, repository-consistency and validation phases; index repair stays plan/report-first |
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
runtime tool capability manifest status
full toolbox telemetry summary status
discovery/index/CSV-count evidence status
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
runtime capability manifest statement
full toolbox telemetry summary statement
discovery/index/CSV-count evidence statement
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

The current review-first local task is tracked in:

```text
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
```

Current compact state:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

The previously critical broker telemetry task is closed and validated by run `20260505-073332`:

```text
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
```

The external-controls task remains a follow-up, not the current active task unless explicitly selected:

```text
docs/LOCAL_AI_TASKS/next-chat-unified-launcher-external-controls.md
```

The audio/media output guardrail is tracked in:

```text
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

The expected current work is:

```text
inspect the 20260505-143844 refactor/reuse runtime bundle, classify recommendations and patch plans, verify telemetry/capability/provider/workload/discovery/index/CSV surfaces, then select review-first refactor/reuse changes only after evidence review
```

GPU/NPU execution is included by default in Full0To10 when available and quality-gated, unless explicitly disabled or diagnosed unavailable. Audio/media output remains forbidden unless an explicit application-domain task enables it. If Carmine cannot run the local provider workflow, GitHub-only agents must stop at report-only/docs/validator work and request the exact unified launcher command/evidence bundle needed next.
