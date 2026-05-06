# IA-Carmine Local AI Orchestration Workbench

`C-F-tek/blender-audio-project` is now primarily a local AI orchestration, validation and guardrail workbench. The repository name is historical: Blender/audio remains the first application domain, but the active architecture is app-agnostic AI/backend orchestration.

## Current operating doctrine: TUTTO SU TUTTO

The project now treats full local AI runs as serious whole-repository operations: **TUTTO SU TUTTO**.

A full run is not a narrow smoke, not a single-lane provider call and not a partial documentation scan. Every `-Full0To10` variation must cover all active repository lanes unless a capability is explicitly disabled, unavailable or recorded as degraded.

Full0To10 is opt-out by lane: once selected, provider/probe/workload-quality, telemetry, discovery, index and CSV/count lanes are included by default. If the operator does not want a lane, the operator must disable it explicitly with `-No*` flags or a documented exclusion.

The meaning of `tutto` is intentionally expandable. New stable lanes, registries, validators, broker tools, provider diagnostics, evidence surfaces, memory/context builders and repository-consistency checks must be added to the full-run contract when they become production-ready. Expansion must be explicit in docs, manifests and evidence summaries; silent scope reduction is not allowed.

## Canonical reading flow

```text
AGENTS.md
  -> CHATGPT.md
  -> CHATGPT/README.md
  -> docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
  -> README.md
  -> WORKFLOW.md
  -> docs/README.md
  -> docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
  -> docs/LOCAL_AI_RUN_BOOTSTRAP.md
  -> docs/LOCAL_AI_TASKS/README.md
  -> docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
  -> docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
  -> docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
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

Current compact operational bridge:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

These files are advisory memory. They do not override `AGENTS.md`, source code, validation reports or canonical docs.

## Current architecture

```text
local reports / generated artifacts
  -> bounded context and inventory evidence
  -> validation and quality gates
  -> provider lane classification
  -> Ollama/GPU advisory lane for Full0To10 when available and quality-gated
  -> OpenVINO/NPU probe, guardrail and decode diagnostics for Full0To10 when available
  -> deterministic recommendations
  -> manual-review patch plans / patch bundles
  -> runtime broker telemetry
  -> shared production AI-to-AI bundle
  -> PR review / human merge
```

Provider posture:

| Lane | Provider | Role |
|---|---|---|
| GPU/CUDA | Ollama | Primary advisory/planning lane for Full0To10 unless explicitly disabled or diagnosed unavailable; quality-gated. |
| NPU/OpenVINO | OpenVINO GenAI | Probe, guardrail and decode-smoke diagnostics for Full0To10 unless explicitly disabled or diagnosed unavailable. Not general advisory. |
| Blender/audio/media runtime | Blender Python / FFmpeg / audio tools | Legacy/application target. Frozen unless explicitly scoped. |

## Canonical local AI entrypoint

The active local AI operator entrypoint is implemented in code on `master`:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Its canonical runbook is:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Use that runbook for current commands, `-Full0To10`, intensity profiles, provider flags, reset mode, memory controls, patch-spec generation and validation modes.

Legacy monolithic 0-to-10 runbooks are removed from active documentation. Historical details must be recovered from git history or compact evidence when needed; do not recreate parallel active-start runbooks.

## Current code-derived state

`master` already includes PR #187. Therefore the unified launcher is no longer a candidate branch artifact; it is the baseline implementation.

Current next candidate after code inspection:

```text
PR #192 feat(ai): add full0to10 report-only foundation checks
```

PR #192 adds report-only code for:

```text
recursive Full0To10 evidence ZIP bundle creation
bundle completeness validation
runtime hardware capability manifest for CPU/GPU.0/NPU/NVIDIA visibility
hardware/delegation report-only contract validation
```

PR #191 contains useful Full0To10 quick evidence from `20260506-004242`, but the branch diverged after #187 and should be mined, regenerated or summarized before any merge decision.

## Current stable docs

| Need | Start here |
|---|---|
| Agent contract and guardrails | `AGENTS.md` |
| ChatGPT/session memory and handoff notes | `CHATGPT.md`, then `CHATGPT/README.md` |
| Current code/state bridge | `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` |
| Active refactor/reuse planning task | `docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md` |
| Recent telemetry baseline | `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` |
| Operational lifecycle | `WORKFLOW.md` |
| Documentation index | `docs/README.md` |
| Local checkout bootstrap | `docs/LOCAL_AI_RUN_BOOTSTRAP.md` |
| Unified full 0-to-10 local AI run | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Current code/tool/evidence flow | `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` |
| Runtime broker telemetry resolved context | `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` |
| No audio/media output guardrail | `docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md` |
| Tool placement audit | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` |
| Tool promotion/insertion | `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Unified launcher manifest contract | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Validators and inventories | `Tools/validation/README.md` |
| NPU/helper package | `Tools/npu/pipeline/README.md` |
| Repository area map | `docs/MODULE_MAP.md` |
| Documentation map and pruning | `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |
| Workflow helper policy | `docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md` |

## Current active work

```text
Baseline: master after PR #187 merge
Primary launcher: Tools/workflow/run_unified_local_ai_refactor.ps1
Current bridge: docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
Next candidate: PR #192 report-only Full0To10 foundation checks
Mode: review-only until explicit human instruction
```

## Operating rules

Do not infer project state from the repository name. Current core/backend work must not:

```text
modify Blender runtime packages
produce audio playback/export or media output
run FFmpeg encode/mux or Blender render
modify full analysis JSON files
commit output/**, renders/**, generated media, *.db or *.sqlite
hand-edit generated indexes
change Full0To10 from opt-out-by-lane to silent opt-in per capability
promote NPU/OpenVINO to primary advisory
merge to master without explicit user command
```

Use compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` instead of raw `output/**` reports.

## Audio/media output policy

Normal AI/tooling runs are evidence/report workflows, not media-generation workflows.

Forbidden unless explicitly scoped as application-domain work:

```text
audio playback
audio export
WAV/MP3/AAC conversion
FFmpeg encode/mux
Blender render
video generation
media output side effect
```

Detailed policy:

```text
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

## Inventory and evidence

Current documentation cleanup and refactoring use:

```text
Markdown inventory
script/function/class/method inventory
CSV/count evidence surfaces
auto-discovery and index repair reports/plans
tool placement audit
validation report contracts
runtime broker telemetry
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
