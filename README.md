# IA-Carmine Local AI Orchestration Workbench

`C-F-tek/blender-audio-project` is now primarily a local AI orchestration, validation, telemetry and guardrail workbench.

The repository name is historical. Blender/audio remains the first application domain, but the active architecture is app-agnostic AI/backend orchestration.

## Current operating doctrine: TUTTO SU TUTTO

The project treats full local AI runs as serious whole-repository operations: **TUTTO SU TUTTO**.

A full run is not a narrow smoke, not a single-lane provider call and not a partial documentation scan. Every `-Full0To10` variation must cover all active repository lanes unless a capability is explicitly disabled, unavailable or recorded as degraded.

Full0To10 is opt-out by lane. Once selected, provider/probe/workload-quality, telemetry, discovery, index and CSV/count lanes are included by default. If the operator does not want a lane, the operator must disable it explicitly with `-No*` flags or a documented exclusion.

The meaning of `tutto` is expandable. New stable lanes, registries, validators, broker tools, provider diagnostics, evidence surfaces, memory/context builders and repository-consistency checks must be added to the full-run contract when they become production-ready.

## Main runtime architecture

Canonical contract:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Current target topology:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Runtime meaning:

```text
provider lanes advise, classify, plan or respond through explicit roles;
broker unico executor is the execution gateway for registered tools;
semantic tools registry is the capability source of truth;
deterministic CPU validators remain local pass/fail authority;
telemetry/event stream records executed, skipped, degraded and blocked phases.
```

This architecture is implemented incrementally. Do not claim that a lane executed unless manifest, telemetry, provider diagnostics or validator evidence proves it.

## Canonical reading flow

```text
AGENTS.md
  -> CHATGPT.md
  -> CHATGPT/README.md
  -> docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
  -> docs/MAIN_RUNTIME_ARCHITECTURE.md
  -> docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
  -> README.md
  -> WORKFLOW.md
  -> docs/README.md
  -> docs/LOCAL_AI_RUN_BOOTSTRAP.md
  -> docs/LOCAL_AI_TASKS/README.md
  -> docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
  -> docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
  -> task-specific docs / package README / target source file
```

The root README is descriptive only. It must not carry executable PowerShell command blocks because launcher options change faster than project identity docs.

## Current local AI entrypoint

The active local AI operator entrypoint is implemented on `master`:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Canonical runbook:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Launcher manifest contract:

```text
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Use those documents for current commands, `-Full0To10`, intensity profiles, provider flags, reset mode, memory controls, patch-spec generation and validation modes.

## Current code-derived state

```text
Baseline: master after PR #187 merge
Primary launcher: Tools/workflow/run_unified_local_ai_refactor.ps1
Current bridge: docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
Current documentation architecture PR: #196 docs(ai): add main runtime architecture contract
Mode: review-only until explicit human instruction
```

Do not treat `codex/unified-local-ai-refactor-launcher` or PR #187 as the active branch anymore. PR #187 is the merged baseline.

Historical PR/evidence branches such as PR #191/#192 may be useful context only when current GitHub state and committed evidence confirm relevance.

## Current stable docs

| Need | Start here |
|---|---|
| Agent contract and guardrails | `AGENTS.md` |
| ChatGPT/session memory and handoff notes | `CHATGPT.md`, then `CHATGPT/README.md` |
| Current code/state bridge | `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` |
| Main runtime architecture | `docs/MAIN_RUNTIME_ARCHITECTURE.md` |
| Unified launcher manifest contract | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Documentation index | `docs/README.md` |
| Unified full 0-to-10 local AI run | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Current code/tool/evidence flow | `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` |
| Recent telemetry baseline | `docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` |
| Active refactor/reuse planning task | `docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md` |
| Large Markdown policy | `docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md` |
| 400-line validator contract | `docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md` |
| Tool placement audit | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` |
| Tool promotion/insertion | `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Validators and inventories | `Tools/validation/README.md` |
| NPU/helper package | `Tools/npu/pipeline/README.md` |
| Repository area map | `docs/MODULE_MAP.md` |
| Documentation map and pruning | `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |
| Workflow helper policy | `docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md` |

## ChatGPT operational memory

`CHATGPT/` contains lightweight handoff and chat/tooling recovery notes for long AI-assisted repository sessions.

Read it early when resuming full-toolbox, local-AI, provider, patch-bundle or ChatGPT-assisted work:

```text
CHATGPT.md
CHATGPT/README.md
CHATGPT/DISCOVERY_CONTRACT.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
```

These files are advisory memory. They do not override `AGENTS.md`, source code, validation reports or canonical docs.

## Full-run handoff completeness

A production run-unica handoff is not complete from evidence or patch plan alone.

Review this group together:

```text
launcher manifest
phase_status / phase_reports
evidence artifacts
patch-plan artifacts when produced
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
blackboard/broker/registry/validator/event-stream reports when implemented
```

Never infer success only from file existence, focused validator output, dry-run matrix output, provider report existence, NPU smoke, patch plan existence or large Markdown text.

## 400-line rule

Maintained documentation and source files must stay within 400 lines.

```text
Markdown >400 lines: keep original file as index and move content into <file>.md/part-001.md, part-002.md, ...
Code/script >400 lines: keep entrypoint compact and move implementation into a same-purpose package/module folder split by responsibility.
Existing over-400-line files are technical debt and should be refactored progressively when touched for relevant work.
```

## Operating rules

Do not infer project state from the repository name. Current core/backend work must not:

```text
modify Blender runtime packages without explicit scope
produce audio playback/export or media output
run FFmpeg encode/mux or Blender render
modify full analysis JSON files
commit output/**, renders/**, generated media, *.db or *.sqlite
hand-edit generated indexes
change Full0To10 from opt-out-by-lane to silent opt-in per capability
promote NPU/OpenVINO to primary advisory without quality-gated architecture change
create tool execution paths outside broker/registry/validator/telemetry architecture
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

GitHub PR descriptions and repository-facing summaries should point to canonical docs instead of duplicating executable commands.

Required wording principle:

```text
Root/project descriptions describe purpose and canonical docs.
Operational commands live in docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md.
Runtime architecture lives in docs/MAIN_RUNTIME_ARCHITECTURE.md.
```

## Legacy Blender/audio role

The repository still contains mature Blender/audio-reactive workflows under `Scripting/`, including `Scripting/v61b/` and shared helpers.

Treat them as application-domain assets. Do not refactor or run them unless the task explicitly enters that milestone.
