# AI Docs Entrypoint

## Status

Current `docs/` entrypoint for AI agents.

This file is a routing bridge only. It points to current source-of-truth maps and must not preserve old first-read orders that predate the context-index and dispatcher-coverage layer.

## Purpose

Use this file when an AI agent, coding assistant or automated reviewer starts inside `docs/` instead of the repository root.

The canonical root entrypoints are:

```text
../AGENTS.md
../CHATGPT.md
../CONTEXT_INDEX.md
```

## Current first-read path

For a new AI session, read in this order:

```text
../AGENTS.md
../CHATGPT.md
../CONTEXT_INDEX.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
../Tools/CONTEXT_INDEX.md
docs/CONTEXT_INDEX.md
../Scripting/CONTEXT_INDEX.md
```

Then open the nearest area/family `TOOL_CONTEXT.md` before touching code.

## First rule

Do not treat `docs/` as passive background text.

In this repository, `docs/` is the contract and evidence layer for:

- project architecture;
- AI workflow;
- validation expectations;
- safe modification policy;
- reusable pipeline direction;
- NPU/helper package boundaries;
- generated artifact acceptance rules;
- heap/exchange lifecycle boundaries;
- patchkit/source-write boundaries;
- dispatcher-driven context navigation.

## Current routing documents

| Need | Read |
| --- | --- |
| Whole-repo entrypoint | `../CONTEXT_INDEX.md` |
| Context coverage status | `docs/CONTEXT_COVERAGE_STATUS.md` |
| Dispatcher-to-family coverage | `docs/DISPATCHER_CONTEXT_COVERAGE.md` |
| Documentation folder navigation | `docs/CONTEXT_INDEX.md` |
| Tool family navigation | `../Tools/CONTEXT_INDEX.md` |
| Scripting/package navigation | `../Scripting/CONTEXT_INDEX.md` |
| Root surface map | `docs/ROOT_SURFACE_CONTEXT.md` |
| Non-Tools script surface | `docs/SCRIPT_SURFACE_CONTEXT.md` |
| Optional mapping procedure | `docs/MAPPING_TOOL_EVIDENCE.md` |

## Historical/task-specific references

Older orientation files remain useful only after the current first-read path:

```text
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
MAIN_RUNTIME_ARCHITECTURE.md
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/README.md
AI_ONBOARDING.md
```

Use them as task-specific background, not as the current navigation root.

## Task-specific routing

| Work area | Read |
|---|---|
| Current AI orientation | `../CONTEXT_INDEX.md`, `docs/CONTEXT_COVERAGE_STATUS.md`, `docs/DISPATCHER_CONTEXT_COVERAGE.md` |
| Heap/exchange and patchkit | `LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md`, `MAIN_RUNTIME_ARCHITECTURE.md`, `../Tools/ai/CONTEXT_INDEX.md` |
| Unified launcher/full run | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md`, `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/README.md`, `../Tools/ai/run/TOOL_CONTEXT.md` |
| Documentation staleness | `docs/CONTEXT_COVERAGE_STATUS.md`, `LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md` |
| AI pipeline orchestration | `AI_PIPELINE_ARCHITECTURE.md`, `AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `../Tools/ai/pipeline/TOOL_CONTEXT.md` |
| Guardrails, evals, validation | `AI_GUARDRAILS_VALIDATION_GUIDE.md`, `AI_ARTIFACT_SCHEMAS.md`, `JSON_SCHEMAS.md`, `../Tools/validation/CONTEXT_INDEX.md` |
| NPU/OpenVINO/local inference | `AI_NPU_RUNTIME_REFERENCE_GUIDE.md`, `../Tools/npu/CONTEXT_INDEX.md` |
| Generated Blender packages | `AI_GENERATED_PACKAGE_STANDARD.md`, `PACKAGE_CREATION_WORKFLOW.md`, `QUALITY_GATE.md`, `../Scripting/CONTEXT_INDEX.md` |
| Runtime compatibility | `COMPATIBILITY.md`, `BLENDER_SCRIPT_ENTRYPOINTS.md`, `../Scripting/CONTEXT_INDEX.md` |
| GitHub/local validation flow | `GITHUB_LOCAL_VALIDATION_WORKFLOW.md`, `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md`, `../Tools/git/CONTEXT_INDEX.md` |
| Mechanical patch workflow | `PATCH_SPEC_WORKFLOW.md`, `../Tools/ai/patchkit/TOOL_CONTEXT.md`, `../Tools/repo_patch_runner/CONTEXT_INDEX.md` |
| Larger refactors | `EXECUTION_PLANS/README.md`, `TECH_DEBT_TRACKER.md`, `REFACTORING_AND_REUSE_PLAN.md` |

## How to use external-reference guides

The files below summarize external AI/NPU/validation references in project-specific form:

```text
AI_REFERENCE_ONBOARDING.md
AI_REFERENCE_SOURCE_MAP.md
AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
AI_GUARDRAILS_VALIDATION_GUIDE.md
AI_NPU_RUNTIME_REFERENCE_GUIDE.md
```

They should guide architecture and validation decisions, not bypass local contracts.

If one conflicts with current context indexes, dispatcher coverage, heap/exchange, patchkit, launcher or source behavior, inspect source and update the smallest current map first.

## Safe behavior

When entering through `docs/`, an AI agent should:

1. identify the task area;
2. read the current index/coverage files first;
3. open the nearest family `TOOL_CONTEXT.md`;
4. inspect current source before proposing patches;
5. avoid destructive edits;
6. preserve existing Blender behavior;
7. prefer additive docs, validators and helper modules;
8. keep generated indexes out of source-level refactors;
9. report assumptions and local validation gaps;
10. record discovered code/doc coherence problems in `problems.md` when they are not fixed in the current PR.

## Update rule

When adding stable documentation:

1. add the file under the nearest appropriate folder;
2. link it from the nearest `CONTEXT_INDEX.md` when it changes navigation;
3. update `docs/CONTEXT_COVERAGE_STATUS.md` when it changes coverage;
4. update `docs/DISPATCHER_CONTEXT_COVERAGE.md` when it changes dispatcher/family coverage;
5. explain whether it is a contract, guide, status marker or historical note.