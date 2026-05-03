# AGENTS.md

This is the primary repository contract for AI assistants, local agents, automated review systems and GitHub-only assistants working on this repository.

## Mandatory contract

Before planning, editing, validating, opening a PR or suggesting changes, the agent must:

1. read `AGENTS.md`;
2. read `docs/LOCAL_AI_RUN_BOOTSTRAP.md` when working from or delegating to a local checkout;
3. follow hard guardrails unless the human explicitly approves a normally restricted action;
4. report task/request conflicts before modifying files;
5. inspect the target source/document before proposing a patch.

## Repository identity

| Field | Value |
|---|---|
| Working title | `IA-Carmine Local AI Orchestration Workbench` |
| Repository | `C-F-tek/blender-audio-project` |
| Main language | Python |
| Active architecture | Local AI orchestration, validation, provider routing, guardrail/evidence workflows |
| Primary provider lane | `Ollama -> GPU/CUDA -> primary advisory` |
| Secondary provider lane | `OpenVINO -> NPU -> probe / guardrail / decode diagnostic` |
| Legacy domain | Blender audio-reactive scene automation |

The repository name is historical. Do not infer that Blender/audio is the current architectural boundary.

## Canonical reading order

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md          # local checkout only
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
nearest package/tool README
target file
```

For full toolbox or refactor runs, use:

```text
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md
```

## Current provider posture

```text
Ollama/GPU is the primary advisory lane when explicitly enabled and quality-gated.
NPU/OpenVINO is a validated smoke/probe/diagnostic lane, not general advisory.
Provider execution must be explicit and report-bound.
Blender runtime is frozen unless explicitly scoped.
```

## Important folders

| Path | Meaning |
|---|---|
| `Tools/ai/` | AI orchestration, provider probes, evidence bundles, recommendations and patch-plan tooling. |
| `Tools/workflow/` | Local workflow runners and post-validation packet generation. |
| `Tools/npu/` | NPU/OpenVINO support, context builders and runtime diagnostics. |
| `Tools/npu/pipeline/` | App-agnostic helper package for provider/report/path/prompt contracts. |
| `Tools/validation/` | Non-invasive validators and inventory builders. |
| `docs/` | Stable documentation contracts and project state. |
| `docs/LOCAL_VALIDATION_EVIDENCE/` | Compact Git-trackable summaries of ignored local reports. |
| `docs/EXECUTION_PLANS/` | Durable task records. |
| `Scripting/` | Blender application-domain packages. Frozen for core/backend work. |
| `indexAI/` | Generated indexes/context/patch material. Do not hand-refactor as source. |

## Allowed by default

```text
read files
inspect repository structure
add or update non-destructive documentation
add report-only validators and inventory tools
create manual-review patch specs/bundles
run focused local validation when execution is available
open/update PRs without merging
```

## Requires explicit human approval

```text
delete files
force-push
rewrite history
merge to master/protected branch
change secrets, permissions, billing or visibility
deploy production
rename repository
run long Blender renders or heavy GPU workloads
change provider/model execution semantics
add dependencies
move package entrypoints
rewrite large Blender scripts
modify full frame-level analysis JSON
```

## Never commit

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw checkpoints
large full analysis JSON outside compact evidence policy
```

## Refactoring rules

```text
prefer existing helpers before creating new ones
keep path/JSON/provider/evidence logic app-agnostic when practical
keep generated indexes out of source-level refactors
keep artistic scene behavior separate from infrastructure refactors
do not migrate Blender packages broadly unless explicitly scoped
```

## Reporting contract

For code/script changes report:

```text
changed files
purpose
resulting line count for every created/modified script
validation performed or missing
provider/runtime execution status
risks
follow-up recommendations
```

A workflow change is incomplete unless it produces compact evidence or clearly states which checks are missing.
