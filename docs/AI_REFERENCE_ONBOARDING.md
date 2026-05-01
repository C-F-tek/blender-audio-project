# AI Reference Onboarding

## Purpose

This document explains how external AI, NPU, validation and agent-engineering references are made available to AI agents working on this repository.

The repository should not vendor full external documentation trees. Instead, it exposes a curated, versioned documentation layer that tells agents which project files are authoritative, which external concepts are adopted, and how those concepts map to this codebase.

## Operating model

AI agents entering the repository should use this order:

1. read `AGENTS.md`;
2. read `WORKFLOW.md`;
3. read `docs/README.md`;
4. read this document;
5. read `docs/AI_REFERENCE_SOURCE_MAP.md`;
6. read the specific project guide matching the task:
   - `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`;
   - `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`;
   - `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`;
7. read the existing project-specific contracts:
   - `docs/AI_EXTERNAL_KNOWLEDGE.md`;
   - `docs/AI_PIPELINE_ARCHITECTURE.md`;
   - `docs/AI_PIPELINE_REFACTOR_STATUS.md`;
   - `docs/AI_MEMORY_POLICY.md`;
   - `docs/QUALITY_GATE.md`;
   - `docs/JSON_SCHEMAS.md`;
   - `docs/AI_ARTIFACT_SCHEMAS.md`;
8. for manual-review documentation patch plans, read:
   - `docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md`;
   - `Tools/validation/run_agent_review_patch_plan_full_validation.py`;
   - `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md`.

## What this layer is

This layer is:

- a stable AI-readable map of external concepts adopted by the project;
- a project-specific translation of external documentation into repository rules;
- a navigation aid for future AI coding sessions;
- a contract for generating, validating and reviewing AI artifacts;
- a compact alternative to committing full external repositories.

## What this layer is not

This layer is not:

- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;
- a replacement for local validation;
- a runtime dependency;
- a permission to perform destructive changes;
- a reason to bypass `AGENTS.md`, execution plans or validators.

## Repository policy

Full external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:

```text
docs/external_references/
docs/references/
```

The committed repository should contain only:

```text
docs/AI_REFERENCE_ONBOARDING.md
docs/AI_REFERENCE_SOURCE_MAP.md
docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
docs/AI_GUARDRAILS_VALIDATION_GUIDE.md
docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md
```

This keeps remote AI agents effective without bloating the repository.

## Manual-review patch-plan evidence route

Documentation patch plans generated from local AI evidence should use the repository task/evidence route instead of long chat paste or ignored report commits.

For the agent-review documentation lane:

```text
docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md
Tools/validation/run_agent_review_patch_plan_full_validation.py
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
```

Rules:

- keep full local reports under ignored `output/**`;
- commit only compact task-scoped evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`;
- keep provider execution explicit-only and disabled for documentation-only patch plans;
- keep patch application manual-review-only.

## Recommended agent behavior

When an AI agent uses this reference layer, it should:

1. identify the target work area;
2. read the related guide;
3. map external concepts to existing project files;
4. avoid introducing new dependencies unless explicitly approved;
5. prefer additive documentation, validators and helper modules;
6. preserve current Blender package behavior;
7. keep NPU helper work provider-free unless a validated phase says otherwise;
8. update `docs/README.md` when adding stable documentation;
9. report uncertainty rather than inventing unsupported repository state.

## Task routing

| Task | Read first |
|---|---|
| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md` |
| NPU/OpenVINO/local inference changes | `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md` |
| JSON validation, guardrails, evals | `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md` |
| Agent instructions or AI onboarding | `docs/AI_REFERENCE_SOURCE_MAP.md` and `AGENTS.md` |
| Manual-review documentation patch plans | `docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md` and `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| Generated Blender script rules | `docs/QUALITY_GATE.md`, `docs/COMPATIBILITY.md`, `docs/AI_GENERATED_PACKAGE_STANDARD.md` |

## Safe extension rule

If a new external reference becomes useful, do not paste large upstream docs into this repository.

Instead:

1. add the source to `docs/AI_REFERENCE_SOURCE_MAP.md`;
2. describe only the project-relevant concept;
3. map it to local files and validators;
4. add a focused project rule if needed;
5. keep the original source as an external reference.
