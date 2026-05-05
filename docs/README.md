# Documentation

Stable documentation index for `IA-Carmine Local AI Orchestration Workbench`.

The repository slug is still `C-F-tek/blender-audio-project`, but the active architecture is local AI orchestration, provider-lane routing, validation, evidence, telemetry and manual-review patch planning. Blender/audio remains the first application domain, not the architectural boundary.

## Single reading flow

Use this flow unless a task file says otherwise:

```text
../AGENTS.md
../README.md
../WORKFLOW.md
README.md
DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
LOCAL_AI_RUN_BOOTSTRAP.md        # local checkout only
LOCAL_AI_TASKS/README.md         # task entrypoints
LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
WORKFLOW_HELPER_SCRIPTS_POLICY.md
PROJECT_STATUS_POINT.md
DATA_FLOW.md
LOCAL_AI_WORKFLOW.md
JSON_SCHEMAS.md
../Tools/validation/README.md
../Tools/npu/pipeline/README.md
MODULE_MAP.md
nearest package/tool README
target file
```

This documentation index is descriptive only. It must not carry executable PowerShell command blocks because task commands and launcher flags change faster than stable documentation indexes.

## Current canonical task runbooks

| Need | File |
|---|---|
| Unified full 0-to-10 local AI workflow | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Current code/tool/evidence flow | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` |
| Runtime broker telemetry P0 validation | `LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md` |
| Post-broker evidence interpretation | `LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-2026-05-05.md` |
| Project-wide tool placement audit | `LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` |
| Project tool promotion/insertion rules | `LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Unified launcher manifest/phase contract | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` |
| Workflow helper/push-capable script policy | `WORKFLOW_HELPER_SCRIPTS_POLICY.md` |
| Local AI task routing/index | `LOCAL_AI_TASKS/README.md` |
| Markdown cleanup and pruning governance | `DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |

Legacy monolithic 0-to-10 runbooks are no longer indexed as active documentation. Use git history or compact evidence when forensic comparison is required.

## Operational command policy

Current commands live in task runbooks and tool-specific READMEs, not in this index.

Primary command source:

```text
LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Task-specific command sources:

```text
LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md
LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
../FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
```

Tool-specific command sources:

```text
../Tools/validation/README.md
../Tools/npu/pipeline/README.md
```

If this index needs to mention a workflow, link to the canonical document instead of copying executable commands.

## Inventories before broad changes

Use Markdown and script inventories before broad documentation cleanup or refactor planning.

Inventory roles:

| Inventory | Purpose |
|---|---|
| Markdown inventory | Obsolete/redundant docs, missing indexes, length and lifecycle classification. |
| Script inventory | Tool/script discovery, CSV review, function/class/method visibility and refactor planning. |
| Tool placement audit | Repository-wide classification of canonical and non-canonical tools, including scripts outside `Tools/**`. |
| Tool promotion guide | Rules for promoting scripts into project tools, broker tools and full-run lanes. |

Commands for these inventories live in the unified launcher runbook and validator README.

## Documentation families

| Family | Owner/index | Policy |
|---|---|---|
| Root entrypoints | `../AGENTS.md`, `../README.md`, `../WORKFLOW.md` | Short canonical flow only; no long runbooks. |
| Stable docs | `README.md` | Maintained source documentation. |
| Task runbooks | `LOCAL_AI_TASKS/README.md` | Current task input, supporting detail and historical handoffs only. |
| Unified local AI launcher | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | Active 0-to-10 local AI execution guide. |
| Current code flow | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` | Current launcher/provider/broker/bundle/evidence flow. |
| Tool governance | `LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md`, `LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` | Tool discovery, placement and promotion rules. |
| Broker telemetry follow-up | `LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-2026-05-05.md` | Active P0 validation task until a post-fix run confirms broker telemetry absorption. |
| Unified launcher contract | `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` | Compact manifest/phase/status contract for the launcher. |
| Workflow helper policy | `WORKFLOW_HELPER_SCRIPTS_POLICY.md` | Classification and guardrails for shell/GUI/push-capable helpers. |
| Execution plans | `EXECUTION_PLANS/README.md` | Durable state records. |
| Evidence | `LOCAL_VALIDATION_EVIDENCE/` | Review snapshots, not source docs. |
| Generated/index context | `indexAI/**`, `Tools/npu/npu_code_*.md` | Regenerate; do not hand-edit. |
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
