# AI Docs Entrypoint

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
- generated artifact acceptance rules.

## Minimum reading path

For a new AI session, read:

1. `../AGENTS.md`
2. `../WORKFLOW.md`
3. `README.md`
4. `AI_REFERENCE_ONBOARDING.md`
5. `AI_REFERENCE_SOURCE_MAP.md`
6. `PROJECT_AI_CONSCIOUSNESS.md`
7. `AI_ONBOARDING.md`
8. `AI_PIPELINE_REFACTOR_STATUS.md`
9. `AI_PIPELINE_ARCHITECTURE.md`
10. `QUALITY_GATE.md`

## Task-specific routing

| Work area | Read |
|---|---|
| AI pipeline orchestration | `AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `AI_PIPELINE_ARCHITECTURE.md` |
| Guardrails, evals, validation | `AI_GUARDRAILS_VALIDATION_GUIDE.md`, `JSON_SCHEMAS.md`, `AI_ARTIFACT_SCHEMAS.md` |
| NPU/OpenVINO/local inference | `AI_NPU_RUNTIME_REFERENCE_GUIDE.md`, `../Tools/npu/pipeline/README.md` |
| Generated Blender packages | `AI_GENERATED_PACKAGE_STANDARD.md`, `PACKAGE_CREATION_WORKFLOW.md`, `QUALITY_GATE.md` |
| Runtime compatibility | `COMPATIBILITY.md`, `BLENDER_SCRIPT_ENTRYPOINTS.md` |
| GitHub/local validation flow | `GITHUB_LOCAL_VALIDATION_WORKFLOW.md`, `GITHUB_ONLY_AI_CONTINUATION_GUIDE.md` |
| Mechanical patch workflow | `PATCH_SPEC_WORKFLOW.md`, `../patch_specs/README.md` |
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

## Safe behavior

When entering through `docs/`, an AI agent should:

1. identify the task area;
2. read the matching guide;
3. inspect current source before proposing patches;
4. avoid destructive edits;
5. preserve existing Blender behavior;
6. prefer additive docs, validators and helper modules;
7. keep generated indexes out of source-level refactors;
8. report assumptions and local validation gaps.

## Update rule

When adding stable documentation:

1. add the file under `docs/`;
2. link it from `docs/README.md` when possible;
3. explain whether it is a contract, a guide, a status marker or a historical note;
4. update related package README files if the rule is package-specific.
