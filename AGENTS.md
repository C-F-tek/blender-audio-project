# AGENTS.md

This is the primary repository contract for AI assistants, local agents, automated review systems and GitHub-only assistants working on this repository.

## Mandatory contract

Before planning, editing, validating, opening a PR or suggesting changes, the agent must:

1. read `AGENTS.md`;
2. read `CHATGPT.md` and `CHATGPT/README.md` when resuming ChatGPT-assisted, local-AI, full-toolbox or handoff-driven work;
3. read `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` for the current branch phase when present;
4. read `docs/LOCAL_AI_RUN_BOOTSTRAP.md` when working from or delegating to a local checkout;
5. follow hard guardrails unless the human explicitly approves a normally restricted action;
6. report task/request conflicts before modifying files;
7. inspect the target source/document before proposing a patch.

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
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
CHATGPT/next-chat-handoff-*.md           # when present and relevant
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md          # local checkout only
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
nearest package/tool README
target file
```

For full toolbox, refactor, provider or 0-to-10 local AI runs, use the unified launcher as the active entrypoint:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current compact operational state lives in:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
```

Current active task:

```text
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
```

Historical PR handoffs and old master-branch runbooks are not active entrypoints. If historical details are needed, recover them from git history or compact evidence, not from active task docs.

## Current active branch phase

```text
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
```

The runtime bundle is a GitHub draft release asset linked from PR #187 and is intentionally not committed to the repository. Do not infer bundle contents from file existence alone.

The earlier broker telemetry gap is resolved/historical unless a new regression is found. Use `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` for the recent telemetry baseline.

## ChatGPT operational memory

`CHATGPT/` is a lightweight operational-memory surface for long ChatGPT-assisted repository sessions.

Agents must treat it as discoverable advisory context:

```text
CHATGPT.md                         # root pointer
CHATGPT/README.md                  # index and reading order
CHATGPT/next-chat-handoff-*.md     # current handoff state
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
```

Rules:

```text
Read CHATGPT notes early when resuming a handoff or local-AI workflow.
Use CHATGPT notes to avoid repeating known chat/tooling failures.
Do not let CHATGPT notes override AGENTS.md, source code, validation reports or canonical docs.
Keep CHATGPT notes small, plain Markdown and useful to local context pack builders.
```

## Current provider posture

```text
Ollama/GPU is the primary advisory lane when explicitly enabled and quality-gated.
NPU/OpenVINO is a validated smoke/probe/diagnostic lane, not general advisory.
Provider execution must be explicit and report-bound.
Visible provider degradation can be acceptable when quality-gated and recovered in telemetry/bundle evidence.
Blender runtime is frozen unless explicitly scoped.
```

## Unified 0-to-10 rule

A valid `-Full0To10` run must include every major phase unless the operator disables a phase explicitly with a `-No*` flag.

Expected by default:

```text
pipeline adapter ufficiale eseguito
packet/proposals generati
Ollama advisory usato or explicitly diagnosed as degraded
patch specs creati e validati
primary provider routing completo or explicit recovered provider diagnostic
workload quality routing presente
multistep provider workflow richiesto
probe Ollama/NPU richiesti
context pack presente
SQLite memory IN/OUT presente quando non disabilitata
quality gate registrato nel manifest
runtime broker report produced and absorbed into telemetry
patch_application_performed=false
```

Disablers must be explicit:

```text
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-NoMemoryWrite
-NoEvidence
-NoPatchSpecs
```

Do not accept silent fallback such as provider requested but quality routing missing.

## Full-run intensity rule

Every `-Full0To10` variation is TUTTO SU TUTTO.

`-RunIntensity quick|balanced|deep|custom` changes budget, rounds, context limits, token limits and keep-alive only. It must not remove core lanes, downgrade evidence coverage, skip broker telemetry or replace a full run with a smoke run.

A missing full-run lane is valid only when one of these is true:

```text
explicit -No* disabler is present
manifest/report records unavailable-tool or provider failure
-DryRun records the phase as planned but not executed
```

## Important folders

| Path | Meaning |
|---|---|
| `CHATGPT/` | Lightweight ChatGPT/session operational memory and handoff notes. Read early for resumed AI-assisted work. |
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

## Patch delivery policy

Small documentation edits and tiny code fixes may be patched directly.

For long, multi-file or delicate changes, especially on workflow, broker, memory, GPU/NPU provider or runner code, produce a ZIP patch bundle with:

```text
README.md
run_patch_bundle.py
patches/00_check_repo_ready.py
patches/01_*.py
```

Patch bundles must be idempotent where possible, block on unexpected dirty working trees, print resulting line counts for modified scripts and never commit automatically.

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
