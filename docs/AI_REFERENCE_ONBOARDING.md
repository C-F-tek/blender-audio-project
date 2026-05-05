# AI Reference Onboarding

## Purpose

This document explains how external AI, NPU, validation and agent-engineering references are made available to AI agents working on this repository.

The repository should not vendor full external documentation trees. Instead, it exposes a curated, versioned documentation layer that tells agents which project files are authoritative, which external concepts are adopted, and how those concepts map to this codebase.

This document is compact reference onboarding, not a command catalog and not a managed patch-plan evidence container.

Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large tool/schema catalogs such as `Tools/validation/README.md` and `docs/JSON_SCHEMAS.md` are references only. They must not be treated as first operational entrypoints if too large or truncated.

## Current doctrine

All external concepts must be mapped to the current IA-Carmine operating model:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
smoke = separate non-full mode
CSV/index/discovery surfaces are evidence lanes when relevant
large Markdown must not be a primary operational entrypoint
telemetry accompanies evidence and patch plans for completeness
```

Telemetry is not a replacement for validation reports, evidence or patch plans. It is the required companion that explains whether provider/tool/patch-plan lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

## Current branch phase

```text
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
```

The runtime bundle is a GitHub draft release asset linked from PR #187 and is intentionally not committed to the repository. Do not infer bundle contents from file existence alone.

## Operating model

AI agents entering the repository should use this order:

1. read `AGENTS.md`;
2. read `CHATGPT.md` and `CHATGPT/README.md`;
3. read `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`;
4. read `docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md`;
5. read `README.md` and `WORKFLOW.md`;
6. read `docs/README.md`;
7. read `docs/LOCAL_AI_RUN_BOOTSTRAP.md`;
8. read `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md`;
9. read `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` when launcher/manifest semantics are involved;
10. read this document;
11. read `docs/AI_REFERENCE_SOURCE_MAP.md`;
12. read the specific project guide matching the task:
   - `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`;
   - `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`;
   - `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`;
13. read existing project-specific contracts as references, not primary entrypoints:
   - `docs/AI_EXTERNAL_KNOWLEDGE.md`;
   - `docs/AI_PIPELINE_ARCHITECTURE.md`;
   - `docs/AI_PIPELINE_REFACTOR_STATUS.md`;
   - `docs/AI_MEMORY_POLICY.md`;
   - `docs/QUALITY_GATE.md`;
   - `docs/AI_ARTIFACT_SCHEMAS.md`;
   - `docs/JSON_SCHEMAS.md` only as a broad schema notebook/catalog;
14. for manual-review documentation patch plans, prefer compact evidence and the current task-specific route under `docs/LOCAL_AI_TASKS/` and `docs/LOCAL_VALIDATION_EVIDENCE/`.

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
- a reason to bypass `AGENTS.md`, the unified launcher, execution plans, validators, telemetry/capability handoff surfaces or large-Markdown policy;
- a place for long generated patch-plan/evidence blocks.

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

Documentation patch plans generated from local AI evidence should use repository task/evidence routes instead of long chat paste, ignored report commits or managed blocks embedded into onboarding docs.

Rules:

- keep full local reports under ignored `output/**`;
- commit only compact task-scoped evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`;
- keep documentation-only patch plans provider-free unless they are explicitly derived from run-unica evidence;
- when a documentation patch plan is derived from run-unica evidence, include or reference the companion telemetry/capability/final-summary and discovery/index/CSV-count artifacts;
- keep patch application manual-review-only.

## Run-unica evidence and reference rules

A run-unica reference or handoff is incomplete if it only points to evidence or a patch plan.

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
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
```

GitHub-only agents may rely on local/runtime facts only when those facts are committed, pasted by the maintainer or included in a PR/comment with concrete fields.

## Large Markdown rule

Markdown that is too large to be reliably opened by a future chat, local AI context pack or GitHub-only reviewer must not be a primary operational entrypoint.

Reference/candidate examples:

```text
docs/JSON_SCHEMAS.md
Tools/validation/README.md
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

Use compact bridges, manifests and current-state docs first.

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
10. attach telemetry/capability/final-summary context when reviewing run-unica evidence or patch plans;
11. attach CSV/index/discovery context when reviewing refactor/reuse or repository-wide inventory evidence;
12. demote or bridge oversized Markdown instead of using it as a primary entrypoint.

## Task routing

| Task | Read first |
|---|---|
| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md` |
| NPU/OpenVINO/local inference changes | `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md` |
| JSON validation, guardrails, evals | `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md` |
| Agent instructions or AI onboarding | `docs/AI_REFERENCE_SOURCE_MAP.md`, `docs/AI_ONBOARDING.md` and `AGENTS.md` |
| Manual-review documentation patch plans | Current task docs plus compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` |
| Generated Blender script rules | `docs/QUALITY_GATE.md`, `docs/COMPATIBILITY.md`, `docs/AI_GENERATED_PACKAGE_STANDARD.md` |
| Run-unica evidence or patch-plan review | `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`, telemetry/capability/final-summary artifacts, CSV/index/discovery surfaces when relevant |

## Safe extension rule

If a new external reference becomes useful, do not paste large upstream docs into this repository.

Instead:

1. add the source to `docs/AI_REFERENCE_SOURCE_MAP.md`;
2. describe only the project-relevant concept;
3. map it to local files and validators;
4. add telemetry/capability/handoff implications if it affects run-unica evidence or patch plans;
5. add CSV/index/discovery implications if it affects repository inventory or refactor/reuse flows;
6. add a focused project rule if needed;
7. keep the original source as an external reference.
