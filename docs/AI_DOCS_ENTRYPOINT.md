# AI Docs Entrypoint

## Status

Current `docs/` entrypoint for AI agents.

This file is a routing bridge only. It must point to current source-of-truth maps and must not preserve old first-read orders that predate heap/exchange lifecycle and patchkit.

## Purpose

This file is the quick entrypoint for any AI agent, coding assistant or automated reviewer that starts inside `docs/` instead of the repository root.

The canonical root entrypoint remains:

```text
../AGENTS.md
```

Use this file only to understand how the documentation folder is organized and which documents are relevant before editing code.

## First rule

Do not treat `docs/` as passive background text.

In this repository, `docs/` is the contract layer for:

- project architecture;
- AI workflow;
- validation expectations;
- safe modification policy;
- reusable pipeline direction;
- NPU/helper package boundaries;
- generated artifact acceptance rules;
- heap/exchange lifecycle boundaries;
- patchkit source-write boundaries.

## Minimum reading path

For a new AI session, read:

1. `../AGENTS.md`
2. `../README.md`
3. `../WORKFLOW.md`
4. `README.md`
5. `AI_ONBOARDING.md`
6. `LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md`
7. `LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md`
8. `LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md`
9. `MAIN_RUNTIME_ARCHITECTURE.md`
10. `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/README.md`

Older reference onboarding/source-map documents are useful only after this path.

## Task-specific routing

| Work area | Read |
|---|---|
| Current AI orientation | `LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md`, `AI_ONBOARDING.md` |
| Heap/exchange and patchkit | `LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md`, `MAIN_RUNTIME_ARCHITECTURE.md` |
| Unified launcher/full run | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md`, `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/README.md`, `LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md` |
| Documentation staleness | `LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md` |
| AI pipeline orchestration | `AI_PIPELINE_ARCHITECTURE.md`, `AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md` |
| Guardrails, evals, validation | `AI_GUARDRAILS_VALIDATION_GUIDE.md`, `AI_ARTIFACT_SCHEMAS.md`, `JSON_SCHEMAS.md` |
| NPU/OpenVINO/local inference | `AI_NPU_RUNTIME_REFERENCE_GUIDE.md`, `../Tools/npu/pipeline/README.md` |
| Generated Blender packages | `AI_GENERATED_PACKAGE_STANDARD.md`, `PACKAGE_CREATION_WORKFLOW.md`, `QUALITY_GATE.md` |
| Runtime compatibility | `COMPATIBILITY.md`, `BLENDER_SCRIPT_ENTRYPOINTS.md` |
| GitHub/local validation flow | `GITHUB_LOCAL_VALIDATION_WORKFLOW.md`, `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` |
| Mechanical patch workflow | `PATCH_SPEC_WORKFLOW.md`, `../patch_specs/README.md`, `../Tools/ai/patchkit/apply_patch_bundle.py` |
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

They should be used to guide architecture and validation decisions, not to bypass local contracts.

If one of these files conflicts with heap/exchange, patchkit, launcher or current source behavior, inspect source and update the smallest current map first.

## Safe behavior

When entering through `docs/`, an AI agent should:

1. identify the task area;
2. read the matching guide;
3. inspect current source before proposing patches;
4. avoid destructive edits;
5. preserve existing Blender behavior;
6. prefer additive docs, validators and helper modules;
7. keep generated indexes out of source-level refactors;
8. report assumptions and local validation gaps;
9. record discovered code/doc coherence problems in `problems.md` when they are not fixed in the current PR.

## Update rule

When adding stable documentation:

1. add the file under `docs/`;
2. link it from `docs/README.md` when possible;
3. explain whether it is a contract, a guide, a status marker or a historical note;
4. update related package README files if the rule is package-specific;
5. update `LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md` if the file changes orientation/staleness behavior.
