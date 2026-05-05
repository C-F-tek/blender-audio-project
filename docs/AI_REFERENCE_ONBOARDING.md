# AI Reference Onboarding

## Purpose

This document explains how external AI, NPU, validation and agent-engineering references are made available to AI agents working on this repository.

The repository should not vendor full external documentation trees. Instead, it exposes a curated, versioned documentation layer that tells agents which project files are authoritative, which external concepts are adopted, and how those concepts map to this codebase.

This document is reference onboarding, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

## Current doctrine

All external concepts must be mapped to the current IA-Carmine operating model:

```text
one canonical launcher flow
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
smoke = separate non-full mode
perimeter of tutto can expand explicitly
telemetry accompanies evidence and patch plans for completeness
```

Telemetry is not a replacement for validation reports, evidence or patch plans. It is the required companion that explains whether provider/tool/patch-plan lanes executed, failed, were blocked, degraded, disabled or planned-only.

## Operating model

AI agents entering the repository should use this order:

1. read `AGENTS.md`;
2. read `README.md` and `WORKFLOW.md`;
3. read `docs/README.md`;
4. read `docs/LOCAL_AI_RUN_BOOTSTRAP.md`;
5. read `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md`;
6. read `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` when launcher/manifest semantics are involved;
7. read this document;
8. read `docs/AI_REFERENCE_SOURCE_MAP.md`;
9. read the specific project guide matching the task:
   - `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`;
   - `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`;
   - `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`;
10. read the existing project-specific contracts:
   - `docs/AI_EXTERNAL_KNOWLEDGE.md`;
   - `docs/AI_PIPELINE_ARCHITECTURE.md`;
   - `docs/AI_PIPELINE_REFACTOR_STATUS.md`;
   - `docs/AI_MEMORY_POLICY.md`;
   - `docs/QUALITY_GATE.md`;
   - `docs/JSON_SCHEMAS.md`;
   - `docs/AI_ARTIFACT_SCHEMAS.md`;
11. for manual-review documentation patch plans, read:
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
- a reason to bypass `AGENTS.md`, the unified launcher, execution plans, validators or telemetry/capability handoff surfaces.

## Repository policy

Full external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:

```text
docs/external_references/
docs/references/
```

These folders are optional local study locations. Their absence in the committed branch is expected and must not be treated as a broken documentation reference, missing source artifact or request to copy external material into the repository.

The committed repository should contain only curated project-specific reference notes, such as:

```text
docs/AI_REFERENCE_ONBOARDING.md
docs/AI_REFERENCE_SOURCE_MAP.md
docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md
docs/AI_GUARDRAILS_VALIDATION_GUIDE.md
docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md
docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md
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
- keep patch application manual-review-only;
- when a documentation patch plan is derived from full-run evidence, include or reference the companion telemetry/capability/final-summary artifacts.

## Full-run evidence and reference rules

A full-run reference or handoff is incomplete if it only points to evidence or a patch plan.

Use the full group:

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
```

GitHub-only agents may rely on local/runtime facts only when those facts are committed, pasted by the maintainer or included in a PR/comment with concrete fields.

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
9. report uncertainty rather than inventing unsupported repository state;
10. attach telemetry/capability/final-summary context when reviewing full-run evidence or patch plans.

## Task routing

| Task | Read first |
|---|---|
| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md` |
| NPU/OpenVINO/local inference changes | `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md` |
| JSON validation, guardrails, evals | `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md` |
| Agent instructions or AI onboarding | `docs/AI_REFERENCE_SOURCE_MAP.md`, `docs/AI_ONBOARDING.md` and `AGENTS.md` |
| Manual-review documentation patch plans | `docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md` and `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| Generated Blender script rules | `docs/QUALITY_GATE.md`, `docs/COMPATIBILITY.md`, `docs/AI_GENERATED_PACKAGE_STANDARD.md` |
| Full-run evidence or patch-plan review | `docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md`, `docs/QUALITY_GATE.md`, telemetry/capability/final-summary artifacts |

## Safe extension rule

If a new external reference becomes useful, do not paste large upstream docs into this repository.

Instead:

1. add the source to `docs/AI_REFERENCE_SOURCE_MAP.md`;
2. describe only the project-relevant concept;
3. map it to local files and validators;
4. add telemetry/capability/handoff implications if it affects full-run evidence or patch plans;
5. add a focused project rule if needed;
6. keep the original source as an external reference.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:START -->

## IA-Carmine patch-plan application notes

This managed block was generated from `output/patch_specs/agent_review_patch_plan.json`.
It records the manual-review patch-plan decisions for this file without applying runtime/provider changes.

### `det_doc_code_003` — `doc_code`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/AI_REFERENCE_ONBOARDING.md`
- Manual review required: `True`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

### `det_doc_code_004` — `doc_code`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/AI_REFERENCE_ONBOARDING.md`
- Manual review required: `True`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:END -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_003:docs-ai_reference_onboarding.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_003`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/AI_REFERENCE_ONBOARDING.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_003:docs-ai_reference_onboarding.md -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_004:docs-ai_reference_onboarding.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_004`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/AI_REFERENCE_ONBOARDING.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_004:docs-ai_reference_onboarding.md -->
