# Documentation

This folder contains the stable technical documentation for `IA-Carmine Local AI Orchestration Workbench`.

The GitHub repository slug is still `C-F-tek/blender-audio-project`, but the active project identity is broader than Blender/audio. The current architecture centers on local AI orchestration, provider-lane routing, quality gates, GPU/NPU diagnostics, validation reports, memory/guardrail contracts and compact GitHub evidence bundles.

Blender/audio-reactive generation remains the first application domain and legacy production target. It is not the current architectural boundary.

## Canonical reading order

Use this order for humans, GitHub-only AI and local agents:

1. `../AGENTS.md`
2. `../README.md`
3. `../WORKFLOW.md`
4. `README.md`
5. `DOCUMENTATION_MAP_AND_PRUNING_PLAN.md`
6. `PROJECT_STATUS_POINT.md`
7. `DATA_FLOW.md`
8. `LOCAL_AI_WORKFLOW.md`
9. `JSON_SCHEMAS.md`
10. `LOCAL_AI_RUN_BOOTSTRAP.md` when working from a local checkout
11. `LOCAL_AI_TASKS/README.md`
12. `LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` for full IA-Carmine runs
13. `LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md` for AI-to-AI handoff
14. `../Tools/validation/README.md`
15. `../Tools/npu/pipeline/README.md`
16. `EXECUTION_PLANS/README.md`
17. `TECH_DEBT_TRACKER.md`
18. `MODULE_MAP.md`
19. Domain-specific Blender/audio docs only when entering that application area.

## Documentation governance

`DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` is the control point for the current Markdown cleanup lane.

Rules:

```text
new stable MD -> update the correct index
new overlapping MD -> mark older material as superseded/historical/domain-only
generated/evidence MD -> do not treat as source documentation
deletion -> requires explicit user approval
```

Before broad documentation cleanup, generate inventory evidence:

```powershell
python .\Tools\validation\build_markdown_inventory.py `
  --repo-root . `
  --output .\output\validation\markdown_inventory.json `
  --markdown-output .\output\validation\markdown_inventory.md
```

Then run:

```powershell
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

## Current validated provider posture

```text
Ollama -> GPU/CUDA -> primary advisory provider
OpenVINO -> NPU -> probe / guardrail / decode diagnostic
```

Validated decisions retained by the current docs:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
provider execution remains explicit and report-bound
```

## Documentation groups

### Core entrypoints and governance

| File | Purpose |
|---|---|
| `../AGENTS.md` | Mandatory operating contract for AI agents and automated reviewers. |
| `../README.md` | Human project identity and high-level architecture. |
| `../WORKFLOW.md` | Root operational lifecycle from scope to validation, evidence and PR. |
| `README.md` | This documentation index. |
| `DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` | Markdown map, lifecycle policy, missing-index evidence lane and prune rules. |
| `PROJECT_STATUS_POINT.md` | Current status checkpoint and next recommended tasks. |
| `DATA_FLOW.md` | App-agnostic data/report/provider flow. |
| `MODULE_MAP.md` | Repository areas and navigation map. |
| `TECH_DEBT_TRACKER.md` | Known debt and remediation queue. |

### Local AI, provider and validation workflow

| File | Purpose |
|---|---|
| `LOCAL_AI_RUN_BOOTSTRAP.md` | Local checkout bootstrap, reading set, task classification and guardrails. |
| `LOCAL_AI_WORKFLOW.md` | Local AI provider workflow, GPU/NPU parallelism and evidence handling. |
| `LOCAL_AI_TASKS/README.md` | Non-interactive Markdown task entrypoints for local AI runs. |
| `LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` | Canonical full-toolbox procedure. |
| `LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md` | Repo-native AI-to-AI next-task handoff. |
| `AI_WORKLOAD_REPORT_QUALITY_GATE.md` | Workload quality-gate drift and validation workflow. |
| `LOCAL_AI_CORE_TOOL_ACTIVATION.md` | App-agnostic activation lane for selected chunks, packs, broker packets, proposals and evidence. |
| `AI_CONTEXT_PACKS.md` | Task-scoped AI context pack profiles and compact evidence workflow. |
| `AI_SELECTIVE_PLANNER.md` | Report-only selective planner for validators and patch-spec candidates. |
| `GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Local Git/GitHub validation, index regeneration, commit and push workflow. |
| `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` | GitHub-only continuation mode and local-validation handoff. |
| `AI_MEMORY_POLICY.md` | Retention, promotion and quarantine policy for generic agent memory. |

### AI artifact and pipeline contracts

| File | Purpose |
|---|---|
| `JSON_SCHEMAS.md` | JSON/report contract notes and schema gap index. |
| `AI_PIPELINE_ARCHITECTURE.md` | Modular AI artifact pipeline map. |
| `AI_PIPELINE_REFACTOR_STATUS.md` | Stable refactor status marker. |
| `AI_ARTIFACT_SCHEMAS.md` | AI artifact schema notes and validation report contracts. |
| `GENERATED_PYTHON_ADAPTER_TEMPLATE.md` | Template for future generated Python application adapters. |
| `PATCH_SPEC_WORKFLOW.md` | Safe JSON patch-spec workflow and dry-run/apply commands. |
| `AI_REFERENCE_ONBOARDING.md` | AI-to-AI reference onboarding for current local AI/evidence lanes. |
| `AI_REFERENCE_SOURCE_MAP.md` | Source map for AI reference docs and local evidence workflows. |
| `AI_EXTERNAL_KNOWLEDGE.md` | External AI-coding knowledge adapted to this project. |
| `OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md` | External agent-first engineering patterns mapped into project actions. |

### Validation and package-local documentation

| File | Purpose |
|---|---|
| `../Tools/validation/README.md` | Validation command catalog and report contracts. |
| `../Tools/npu/pipeline/README.md` | App-agnostic NPU/provider helper package contract. |
| `../Tools/git/README.md` | Git helper documentation. |
| `../Scripting/**/README.md` | Package-local Blender/application guidance. |

### Compact evidence

`LOCAL_VALIDATION_EVIDENCE/` contains compact Git-trackable evidence snapshots from ignored local output trees.

Policy:

```text
evidence MD/JSON is review evidence, not canonical source documentation
do not add evidence files to stable reading order unless a specific bundle is the current proof point
do not commit evidence from aborted or partial runs unless explicitly approved
```

### Legacy Blender/audio application domain

These docs are relevant only when working on Blender/audio outputs:

| File | Purpose |
|---|---|
| `PROJECT_OVERVIEW.md` | Historical/high-level project overview. |
| `BLENDER_SCRIPT_ENTRYPOINTS.md` | Known Blender script entry points and execution notes. |
| `AUDIO_ANALYSIS_PIPELINE.md` | Audio analysis workflow and generated data. |
| `AI_GENERATED_PACKAGE_STANDARD.md` | Expected structure of generated Blender packages. |
| `PACKAGE_CREATION_WORKFLOW.md` | Operational workflow for creating future Blender packages. |
| `QUALITY_GATE.md` | Acceptance checks for generated packages. |
| `RENDER_WORKFLOW.md` | Blender rendering workflow. |
| `FFMPEG_WORKFLOW.md` | Final video encoding workflow. |
| `COMPATIBILITY.md` | Blender/version compatibility notes. |
| `SHARED_SCRIPTING_UTILITIES.md` | Shared Blender utility policy and modules. |

### Setup and operations

| File | Purpose |
|---|---|
| `INSTALLATION.md` | Environment setup notes. |
| `USAGE.md` | Common usage notes. |
| `KNOWN_LIMITATIONS.md` | Known gaps and incomplete areas. |
| `LOCAL_WORKSTATION_TARGET.md` | Local workstation target notes. |
| `DEVELOPER_GUIDE.md` | Practical workflow for development and review. |
| `PROJECT_AUDIT.md` | Technical assessment, risks and next actions. |

## Style rules

Use direct, explicit documentation.

Rules:

```text
mark unverified information as not specified
prefer tables for file maps and contracts
keep provider execution modes explicit
keep package-specific Blender instructions near the package
keep global AI/provider/validation rules in root entrypoints and docs/
do not document generated artifacts as manually maintained source
update the correct index when adding a maintained Markdown file
```

## Refactoring note

The repository should move toward reusable AI/backend modules first. Legacy Blender package reuse remains valuable, but shared utility extraction must not break working packages and must stay outside the current GPU/NPU orchestration milestone unless explicitly scoped.
