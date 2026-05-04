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

## Current canonical task runbooks

| Need | File |
|---|---|
| Full toolbox 0→10 repository run | `LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` |
| Code/refactor 0→10 run | `LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md` |
| Markdown cleanup and pruning governance | `DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |
| Local AI task routing | `LOCAL_AI_TASKS/README.md` |

## Inventories before broad changes

```powershell
python .\Tools\validation\build_markdown_inventory.py --repo-root . --output .\output\validation\markdown_inventory.json --markdown-output .\output\validation\markdown_inventory.md
python .\Tools\validation\build_script_inventory.py --repo-root . --output .\output\validation\script_inventory.json --csv-output .\output\validation\script_inventory.csv --markdown-output .\output\validation\script_inventory.md
```

Use Markdown inventory for obsolete/redundant docs. Use script inventory for tool/script discovery, CSV review, function/class/method visibility and refactor planning.

## Documentation families

| Family | Owner/index | Policy |
|---|---|---|
| Root entrypoints | `../AGENTS.md`, `../README.md`, `../WORKFLOW.md` | Short canonical flow only; no long runbooks. |
| Stable docs | `README.md` | Maintained source documentation. |
| Task runbooks | `LOCAL_AI_TASKS/README.md` | Current/historical task entrypoints. |
| Execution plans | `EXECUTION_PLANS/README.md` | Durable state records. |
| Evidence | `LOCAL_VALIDATION_EVIDENCE/` | Review snapshots, not source docs. |
| Generated/index context | `indexAI/**`, `Tools/npu/npu_code_*.md` | Regenerate; do not hand-edit. |
| Blender/application docs | `Scripting/**/README.md` and Blender docs below | Application-domain only. |

## Core stable docs

| File | Purpose |
|---|---|
| `DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` | Markdown lifecycle, pruning policy, missing-index review and add-before-prune rules. |
| `PROJECT_STATUS_POINT.md` | Current status checkpoint and recommended tasks. |
| `PROJECT_AI_CONSCIOUSNESS.md` | Compact operational memory and architecture boundary for AI agents. |
| `REFACTORING_AND_REUSE_PLAN.md` | Progressive encapsulation and reuse/refactoring strategy. |
| `QUALITY_GATE.md` | Cross-domain quality gates for packages, validators, generated Python and report contracts. |
| `DATA_FLOW.md` | App-agnostic data/report/provider flow. |
| `LOCAL_AI_WORKFLOW.md` | Local AI provider workflow and evidence handling. |
| `LOCAL_RUNS_TESTING_AND_EVIDENCE.md` | Local run, testing and evidence practices across workflows. |
| `JSON_SCHEMAS.md` | JSON/report contract notes. |
| `LOCAL_AI_CORE_TOOL_ACTIVATION.md` | App-agnostic activation lane for chunks, packs, broker packets, proposals and evidence. |
| `AI_WORKLOAD_REPORT_QUALITY_GATE.md` | Workload quality-gate contract. |
| `AI_CONTEXT_PACKS.md` | Task-scoped context packs and compact evidence. |
| `AI_SELECTIVE_PLANNER.md` | Report-only selective planner. |
| `AI_MEMORY_POLICY.md` | Memory retention, promotion and quarantine policy. |
| `GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Local Git/GitHub validation workflow. |
| `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` | GitHub-only continuation and local-validation handoff. |
| `NPU_GPU_PARALLELISM_PLAN.md` | NPU/GPU parallelism plan and lane boundaries. |
| `SMART_GUARDRAIL_APP.md` | Smart guardrail application concept and integration notes. |
| `TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md` | Tool-agnostic artifact expansion roadmap. |
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

```powershell
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

Do not commit `output/**`, generated DB files, renders or raw local reports.
