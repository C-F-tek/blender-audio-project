# IA-Carmine Local AI Orchestration Workbench

`C-F-tek/blender-audio-project` is now primarily a local AI orchestration, validation and guardrail workbench. The repository name is historical: Blender/audio remains the first application domain, but the active architecture is app-agnostic AI/backend orchestration.

## Canonical reading flow

```text
AGENTS.md
  -> CHATGPT.md
  -> CHATGPT/README.md
  -> README.md
  -> WORKFLOW.md
  -> docs/README.md
  -> docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
  -> docs/LOCAL_AI_RUN_BOOTSTRAP.md
  -> docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
  -> task-specific docs / package README / target source file
```

The root README is descriptive only. It must not carry executable PowerShell command blocks because launcher options change faster than project identity docs.

## ChatGPT operational memory

`CHATGPT/` contains lightweight handoff and chat/tooling recovery notes for long AI-assisted repository sessions.

Read it early when resuming full-toolbox, local-AI, provider, patch-bundle or ChatGPT-assisted work:

```text
CHATGPT.md
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
```

These files are advisory memory. They do not override `AGENTS.md`, source code, validation reports or canonical docs.

## Current architecture

```text
local reports / generated artifacts
  -> bounded context and inventory evidence
  -> validation and quality gates
  -> provider lane classification
  -> Ollama/GPU advisory lane when explicitly enabled and quality-gated
  -> OpenVINO/NPU probe, guardrail and decode diagnostics
  -> deterministic recommendations
  -> manual-review patch plans / patch bundles
  -> PR review / human merge
```

Provider posture:

| Lane | Provider | Role |
|---|---|---|
| GPU/CUDA | Ollama | Primary advisory/planning lane when explicitly requested and quality-gated. |
| NPU/OpenVINO | OpenVINO GenAI | Probe, guardrail and decode-smoke diagnostics. Not general advisory. |
| Blender runtime | Blender Python | Legacy/application target. Frozen unless explicitly scoped. |

## Canonical local AI entrypoint

The active local AI operator entrypoint is:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Use that runbook for current commands, `-Full0To10`, intensity profiles, provider flags, reset mode, memory controls, patch-spec generation and validation modes.

Legacy monolithic 0-to-10 runbooks are removed from active documentation. Historical details must be recovered from git history or compact evidence when needed; do not recreate parallel active-start runbooks.

## Operating rules

Do not infer project state from the repository name. Current core/backend work must not:

```text
modify Blender runtime packages
modify full analysis JSON files
commit output/**, renders/**, *.db or *.sqlite
hand-edit generated indexes
change provider/model settings implicitly
promote NPU/OpenVINO to primary advisory
merge to master without explicit user command
```

Use compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` instead of raw `output/**` reports.

## Primary entrypoints

| Need | Start here |
|---|---|
| Agent contract and guardrails | `AGENTS.md` |
| ChatGPT/session memory and handoff notes | `CHATGPT.md`, then `CHATGPT/README.md` |
| Operational lifecycle | `WORKFLOW.md` |
| Unified full 0-to-10 local AI run | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Unified launcher manifest contract | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Validators and inventories | `Tools/validation/README.md` |
| NPU/helper package | `Tools/npu/pipeline/README.md` |
| Repository area map | `docs/MODULE_MAP.md` |
| Documentation map and pruning | `docs/README.md`, then `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |
| Workflow helper policy | `docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md` |

## Inventory and evidence

Current documentation cleanup and refactoring use:

```text
Markdown inventory
script/function/class/method inventory
validation report contracts
compact GitHub evidence bundles
```

Commands for these tools live in the unified launcher runbook and tool-specific README files, not in this root README.

## GitHub / PR description policy

GitHub PR descriptions and repository-facing summaries should point to the canonical launcher runbook instead of duplicating executable commands.

Required wording principle:

```text
Root/project descriptions describe purpose and canonical docs.
Operational commands live in docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md.
```

## Legacy Blender/audio role

The repository still contains mature Blender/audio-reactive workflows under `Scripting/`, including `Scripting/v61b/` and shared helpers. Treat them as application-domain assets; do not refactor or run them unless the task explicitly enters that milestone.
