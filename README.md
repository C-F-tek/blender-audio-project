# IA-Carmine Local AI Orchestration Workbench

`C-F-tek/blender-audio-project` is now primarily a local AI orchestration, validation and guardrail workbench. The repository name is historical: Blender/audio remains the first application domain, but the active architecture is app-agnostic AI/backend orchestration.

## Canonical flow

```text
AGENTS.md
  -> README.md
  -> WORKFLOW.md
  -> docs/README.md
  -> docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
  -> docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
  -> task-specific docs / package README / target source file
```

For local AI runs, read `docs/LOCAL_AI_RUN_BOOTSTRAP.md` immediately after `AGENTS.md`.

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

## Unified local AI entrypoint

The active local AI operator entrypoint is:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Full selectable 0-to-10 run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Quick 5-minute style run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Deep run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity deep `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Legacy 0-to-10 runbooks remain historical/supporting references. Do not start new local AI runs from `full-toolbox-0-to-10-semi-automatic-procedure.md` or `code-refactor-0-to-10-procedure.md` unless the user explicitly requests that legacy/manual flow.

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
| Operational lifecycle | `WORKFLOW.md` |
| Unified full 0-to-10 local AI run | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` |
| Validators and inventories | `Tools/validation/README.md` |
| NPU/helper package | `Tools/npu/pipeline/README.md` |
| Repository area map | `docs/MODULE_MAP.md` |
| Documentation map and pruning | `docs/README.md`, then `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` |

## Inventory and evidence

Current documentation cleanup and refactoring should use both inventories:

```powershell
python .\Tools\validation\build_markdown_inventory.py --repo-root . --output .\output\validation\markdown_inventory.json --markdown-output .\output\validation\markdown_inventory.md
python .\Tools\validation\build_script_inventory.py --repo-root . --output .\output\validation\script_inventory.json --csv-output .\output\validation\script_inventory.csv --markdown-output .\output\validation\script_inventory.md
```

The Markdown inventory controls obsolete/redundant docs. The script inventory controls tool/script discovery, function/class visibility and refactor planning.

## Legacy Blender/audio role

The repository still contains mature Blender/audio-reactive workflows under `Scripting/`, including `Scripting/v61b/` and shared helpers. Treat them as application-domain assets; do not refactor or run them unless the task explicitly enters that milestone.
