# Documentation

Stable documentation index for `IA-Carmine Local AI Orchestration Workbench`.

The repository slug is still `C-F-tek/blender-audio-project`, but the active architecture is local AI orchestration, provider-lane routing, validation, evidence, telemetry and manual-review patch planning. Blender/audio remains the first application domain, not the architectural boundary.

## Doctrine index: TUTTO SU TUTTO

All documentation that describes full local-AI work must preserve the same doctrine: **TUTTO SU TUTTO**.

A full run means whole-repository coverage across active lanes, not a partial scan. Intensity profiles may reduce cost or expand depth, but they must not reduce semantic scope.

Full0To10 is opt-out by lane: provider/probe/workload-quality, runtime telemetry, capability manifests, discovery, index repair visibility and CSV/count surfaces are included by default unless explicitly disabled, diagnosed unavailable, represented as dry-run planned state or excluded by a documented operator decision.

When the project gains a stable new lane, registry, validator, broker capability, provider diagnostic, evidence surface, memory/context tool, discovery/index surface or CSV/count surface, that capability becomes a candidate expansion of `tutto` and must be either wired into the full-run contract or explicitly excluded with rationale.

## Limitation policy

Architectural and operational limitations remain important because they are the backlog to overcome.

They must not be used as static reasons to skip available tools. Use all relevant tool lanes by default; mark a lane unavailable or degraded only when current code, manifests, telemetry, provider diagnostics or validator reports prove it.

Canonical limitation/backlog file:

```text
KNOWN_LIMITATIONS.md
```

## Large Markdown rule

Markdown that is too large to be reliably opened by a future chat, local AI context pack or GitHub-only reviewer must not be a primary operational entrypoint.

Large Markdown may exist as historical/supporting reference, generated compact evidence with manifest/summary, schema catalog, application-domain documentation or forensic material.

Current policy:

```text
LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
```

## Single reading flow

Use this flow unless a task file says otherwise:

```text
../AGENTS.md
../CHATGPT.md
../CHATGPT/README.md
LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
../README.md
../WORKFLOW.md
README.md
DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
LOCAL_AI_RUN_BOOTSTRAP.md        # local checkout only
LOCAL_AI_TASKS/README.md         # task entrypoints
LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
WORKFLOW_HELPER_SCRIPTS_POLICY.md
PROJECT_STATUS_POINT.md
DATA_FLOW.md
LOCAL_AI_WORKFLOW.md
../Tools/validation/README.md
../Tools/npu/pipeline/README.md
MODULE_MAP.md
nearest package/tool README
target file
```

`JSON_SCHEMAS.md` is intentionally not part of the primary reading flow. It is a broad schema notebook/catalog. Prefer `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` and compact current-state docs for active run-unica semantics.

This documentation index is descriptive only. It must not carry executable PowerShell command blocks because task commands and launcher flags change faster than stable documentation indexes.

## Current canonical task runbooks

| Need | File |
|---|---|
| Current operational bridge | `LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` |
| Large Markdown policy | `LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md` |
| Active refactor/reuse planning | `LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md` |
| Refactor/reuse run coherence note | `LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md` |
| Recent telemetry baseline / broker resolved context | `LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` |
| Unified full 0-to-10 local AI workflow | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Current code/tool/evidence flow | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` |
| Project-wide tool placement audit | `LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` |
| Project tool promotion/insertion rules | `LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Unified launcher manifest/phase contract | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Workflow helper/push-capable script policy | `WORKFLOW_HELPER_SCRIPTS_POLICY.md` |
| Local AI task routing/index | `LOCAL_AI_TASKS/README.md` |
| Markdown cleanup and pruning governance | `DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |

Legacy monolithic 0-to-10 runbooks are no longer indexed as active documentation. Use git history or compact evidence when forensic comparison is required.

## Current active work

```text
Baseline: master after PR #187 merge
Primary launcher: Tools/workflow/run_unified_local_ai_refactor.ps1
Next candidate: PR #192 report-only Full0To10 foundation checks
Mode: review-only until explicit human instruction
```

## Operational command policy

Current commands live in task runbooks and tool-specific READMEs, not in this index.

Primary command source:

```text
LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Task-specific command sources:

```text
LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
../FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
```

Historical/supporting references such as `LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md`, `LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md` and `LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-2026-05-05.md` may be read for forensic comparison or regression review only. They must not override the unified launcher runbook, current operational state or the compact launcher contract.

Tool-specific command sources:

```text
../Tools/validation/README.md
../Tools/npu/pipeline/README.md
```

If this index needs to mention a workflow, link to the canonical document instead of copying executable commands.

## Inventories before broad changes

Use Markdown, script, discovery and count surfaces before broad documentation cleanup or refactor planning.

Inventory roles:

| Inventory | Purpose |
|---|---|
| Markdown inventory | Obsolete/redundant docs, missing indexes, length and lifecycle classification. |
| Script inventory | Tool/script discovery, CSV review, function/class/method visibility and refactor planning. |
| Python line-count CSV/MD | Size evidence for refactor planning and review reporting. |
| Function/class/method CSV | Method/class/helper reuse visibility and duplication triage. |
| Auto-discovery/index repair report | Detect scanner/index drift and plan repairs before changing generated indexes. |
| Tool placement audit | Repository-wide classification of canonical and non-canonical tools, including scripts outside `Tools/**`. |
| Tool promotion guide | Rules for promoting scripts into project tools, broker tools and full-run lanes. |
| File line-limit report | Report-only check for the 400-line policy on docs and source files. |

Commands for these inventories live in the unified launcher runbook and validator README.

Policy:

```text
CSV/count outputs are evidence surfaces, not source authority.
Generated indexes and code chunks are not hand-maintained source.
Do not commit output/** or indexAI/code_chunks/**.
Index repair is plan/report-first unless explicitly requested.
```

## Documentation families

| Family | Owner/index | Policy |
|---|---|---|
| Root entrypoints | `../AGENTS.md`, `../README.md`, `../WORKFLOW.md` | Short canonical flow only; no long runbooks. |
| Stable docs | `README.md` | Maintained source documentation. |
| Task runbooks | `LOCAL_AI_TASKS/README.md` | Current task input, supporting detail and historical handoffs only. |
| Current operational state | `LOCAL_AI_TASKS/current-operational-state-2026-05-05.md` | Compact current state bridge for post-#187 master and active candidate PRs. |
| Large Markdown policy | `LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md` | Keeps oversized Markdown out of primary operational paths. |
| Refactor/reuse planning | `LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md` | Active review-only task for helper/class/tool reuse planning. |
| Recent telemetry state | `LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` | Recent baseline and resolved broker context. |
| Unified local AI launcher | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | Active 0-to-10 local AI execution guide. |
| Current code flow | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` | Current launcher/provider/broker/bundle/evidence/discovery/CSV flow. |
| Tool governance | `LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md`, `LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` | Tool discovery, placement and promotion rules. |
| Limitations backlog | `KNOWN_LIMITATIONS.md` | Current limits to overcome; not a static prohibition list. |
| Broker telemetry follow-up | `LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md` | Broker telemetry is resolved unless a new regression is found. |
| Unified launcher contract | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` | Compact manifest/phase/status contract for the launcher. |
| Workflow helper policy | `WORKFLOW_HELPER_SCRIPTS_POLICY.md` | Classification and guardrails for shell/GUI/push-capable helpers. |
| Execution plans | `EXECUTION_PLANS/README.md` | Durable state records. |
| Evidence | `LOCAL_VALIDATION_EVIDENCE/` | Review snapshots, not source docs. |
| Generated/index context | `indexAI/**`, `Tools/npu/npu_code_*.md` | Regenerate; do not hand-edit. |
| Schema notebook/catalog | `JSON_SCHEMAS.md` | Broad/historical schema notes; not a primary operational entrypoint. |
| Blender/application docs | `Scripting/**/README.md` and Blender docs below | Application-domain only. |

## Core stable docs

| File | Purpose |
|---|---|
| `DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` | Markdown lifecycle, pruning policy, missing-index review and add-before-prune rules. |
| `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` | Compact launcher manifest, phase-status, visibility, Full0To10 and external-controls contract. |
| `WORKFLOW_HELPER_SCRIPTS_POLICY.md` | Shell/GUI/debug/push-capable helper classification and guardrails. |
| `PROJECT_STATUS_POINT.md` | Current status checkpoint and recommended tasks. |
| `DATA_FLOW.md` | App-agnostic data/report/provider flow. |
| `LOCAL_AI_WORKFLOW.md` | Local AI provider workflow and evidence handling. |
| `JSON_SCHEMAS.md` | Broad historical JSON/report contract notes; prefer compact contract docs for active workflows. |
| `LOCAL_AI_CORE_TOOL_ACTIVATION.md` | App-agnostic activation lane for chunks, packs, broker packets, proposals and evidence. |
| `AI_WORKLOAD_REPORT_QUALITY_GATE.md` | Workload quality-gate contract. |
| `AI_CONTEXT_PACKS.md` | Task-scoped context packs and compact evidence. |
| `AI_SELECTIVE_PLANNER.md` | Report-only selective planner. |
| `AI_MEMORY_POLICY.md` | Memory retention, promotion and quarantine policy. |
| `GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Local Git/GitHub validation workflow. |
| `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` | GitHub-only continuation and local-validation handoff. |
| `MODULE_MAP.md` | Repository area map. |
| `TECH_DEBT_TRACKER.md` | Known debt and remediation queue. |

## AI artifact contracts

| File | Purpose |
|---|---|
| `AI_PIPELINE_ARCHITECTURE.md` | Modular AI artifact pipeline map. |
| `AI_PIPELINE_REFACTOR_STATUS.md` | Stable refactor status marker. |
| `AI_ARTIFACT_SCHEMAS.md` | AI artifact schema notes. |
| `GENERATED_PYTHON_ADAPTER_TEMPLATE.md` | Future generated Python adapter template. |
| `PATCH_SPEC_WORKFLOW.md` | Safe JSON patch-spec workflow. |
| `AI_REFERENCE_ONBOARDING.md` | AI-to-AI reference onboarding. |
| `AI_REFERENCE_SOURCE_MAP.md` | Source map for AI references and evidence. |
| `AI_EXTERNAL_KNOWLEDGE.md` | External AI-coding knowledge adapted to this repo. |
| `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md` | External agent engineering patterns mapped to project actions. |

## Blender/audio docs

Use only when entering the application domain:

```text
PROJECT_OVERVIEW.md
BLENDER_SCRIPT_ENTRYPOINTS.md
AUDIO_ANALYSIS_PIPELINE.md
AI_GENERATED_PACKAGE_STANDARD.md
PACKAGE_CREATION_WORKFLOW.md
QUALITY_GATE.md
RENDER_WORKFLOW.md
FFMPEG_WORKFLOW.md
COMPATIBILITY.md
SHARED_SCRIPTING_UTILITIES.md
```

## Setup/operations docs

```text
INSTALLATION.md
USAGE.md
KNOWN_LIMITATIONS.md
LOCAL_WORKSTATION_TARGET.md
DEVELOPER_GUIDE.md
PROJECT_AUDIT.md
```

## Validation for doc changes

Use the unified launcher `md,contract,full_validation` flow or the validator README for exact commands.

Do not commit `output/**`, generated DB files, renders or raw local reports.
