# AI Onboarding

## Purpose

First-session guide for AI agents entering `IA-Carmine Local AI Orchestration Workbench`.

This file is a compact onboarding bridge. It is not a command catalog, not generated evidence and not a place for long patch-plan blocks.

## First rule

Before proposing or editing:

```text
read current source/canonical docs
inspect existing owners and nearby helpers
reuse existing scripts/helpers first
make the smallest safe change
keep maintained files small and reviewable
```

Canonical rule:

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
```

## Current doctrine

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
CSV/index/discovery/file-line-limit surfaces = evidence lanes when relevant
provider/GPU/NPU/broker lanes = report/evidence-bound and owner-controlled
monolithic or historical runbooks = keep out of primary flow
```

## Primary reading order

Use this order unless a task file says otherwise:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/LOCAL_AI_TASKS/obsolete-monolithic-docs-review-2026-05-07.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
Tools/workflow/README.md
Tools/ai/README.md
Tools/validation/README.md
nearest package/tool README
target source/doc file
```

Generated evidence, old handoffs, old split runbooks and `indexAI/` material are context only. They do not override current source code, owner maps, launcher manifests or validation evidence.

## Main runtime architecture

Current target architecture:

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

Canonical contract:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Provider/tool execution must stay routed through the current owners documented in:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
```

## Current baseline

| Area | Current source |
|---|---|
| Operator launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` |
| Launcher runbook | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Launcher contract | `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Code-derived behavior | `docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md` |
| Script families and variants | `docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md` |
| Owner boundaries | `docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md` |
| Data-flow variants | `docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md` |
| Validator/smoke cycles | `docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md` |
| Monolithic/obsolete docs review | `docs/LOCAL_AI_TASKS/obsolete-monolithic-docs-review-2026-05-07.md` |
| AI tools | `Tools/ai/README.md` |
| Workflow tools | `Tools/workflow/README.md` |
| Validators | `Tools/validation/README.md` and validator-smoke map |
| Compact evidence | `docs/LOCAL_VALIDATION_EVIDENCE/` |

## Full-run handoff checklist

A production run-unica handoff is not complete from one artifact alone.

Review together:

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

Never infer success only from:

```text
file exists
patch plan exists
dry-run matrix passed
provider report exists
NPU smoke passed
reviewed patch spec exists
large Markdown mentions it
```

## Small-file rule

Maintained files must remain compact.

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

Markdown split layout is exact:

```text
path/name.md
path/name.md/part-001.md
path/name.md/part-002.md
```

Legacy extensionless split folders are historical only.

## Common traps

- Do not assume every status document is current; compare it with source and current maps.
- Do not treat old `current-*` docs as current if a newer code-derived map exists.
- Do not treat `indexAI/` as source code. It is generated context.
- Do not commit `indexAI/code_chunks/**` or `output/**`.
- Do not overwrite full frame-by-frame analysis JSON files.
- Do not start normal local-AI work from internal provider scripts.
- Do not bypass `agent_runtime_tool_broker.py` for provider tool execution.
- Do not bypass `apply_patch_suggestion_bundle.py` for patch suggestion dry/apply.
- Do not bypass `prepare_review_pr.py` for staging/commit/push/PR preparation.
- Do not create duplicate validators when `Tools/validation` already owns the check.
- Do not claim `Full0To10` success from focused validation, dry-run reports, provider reports, NPU smoke, large Markdown content or file existence alone.

## Task routing

| Task type | Preferred first move |
|---|---|
| Documentation clarity | Read current maps, patch docs directly, keep edits small. |
| Main runtime architecture | Read `docs/MAIN_RUNTIME_ARCHITECTURE.md` and owner maps. |
| Launcher/full-run work | Start from unified launcher runbook and contract. |
| Provider mesh work | Read `py_mesh.py`, AI tools README, peer-exchange principle and owner maps. |
| Patch suggestion / review PR | Read patch-suggestion final phase and owner map. |
| Validation/smoke | Use `validator-smoke-cycle-map-2026-05-07.md`. |
| GitHub-only work | Read GitHub continuation guide, but verify against source and current maps. |
| Blender/application runtime | Read application-domain docs and target source; keep separate from core AI tooling. |

## Reporting template

Every implementation response should include:

```text
changed files
purpose
line counts for created or modified scripts
assumptions
validation commands and results, or explicit GitHub-only validation limits
telemetry/capability/final-summary artifacts reviewed when relevant
provider/runtime/media side-effect status
risks
recommended next step
```

For documentation-only changes, script line counts can be reported as `not applicable`.
