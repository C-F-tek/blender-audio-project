# AI Reference Source Map

## Purpose

This file maps external AI-engineering references considered useful for this repository to local project documentation, validators and safe implementation areas.

The goal is to make the concepts available to AI agents without committing full upstream repositories into this project and without bypassing the current IA-Carmine launcher, evidence, telemetry and guardrail contracts.

This file is reference mapping, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

## Current doctrine

Every external reference must be translated into the current project operating model:

```text
one canonical launcher flow
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
smoke = separate non-full mode
perimeter of tutto can expand explicitly
telemetry accompanies evidence and patch plans for completeness
```

External concepts are useful only when they improve one of these local surfaces:

```text
AGENTS.md / docs guidance
unified launcher manifest
phase_status / phase_reports
validators and schema contracts
runtime tool usage telemetry
runtime tool capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
compact evidence
manual-review patch plans/specs
```

Telemetry does not replace evidence or patch plans. It is the required companion that explains whether the related lanes executed, failed, were blocked, degraded, disabled or planned-only.

## Source map

| External reference family | Project use | Local canonical files |
|---|---|---|
| AGENTS.md conventions | Entry-point rules for AI coding agents, safe commands, permission boundaries, reading order and handoff expectations. | `AGENTS.md`, `README.md`, `WORKFLOW.md`, `docs/README.md`, `docs/AI_ONBOARDING.md` |
| OpenVINO / NPU references | Local inference, NPU-oriented helper contracts, provider-free preparation, fallback strategy and diagnostic-only NPU posture until quality promotion. | `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`, `Tools/npu/pipeline/README.md`, `Tools/validation/check_npu_pipeline_modules.py` |
| ONNX Runtime / runtime-agnostic inference | Separation between model, provider, orchestration, provider diagnostics and handoff telemetry. | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, `Tools/ai/build_full_toolbox_run_telemetry_summary.py` |
| Guardrails-style validation | Schema-first output validation, rejections, repair loops, explicit failure reports and completeness checks. | `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`, `docs/JSON_SCHEMAS.md`, `docs/AI_ARTIFACT_SCHEMAS.md`, `docs/QUALITY_GATE.md`, `Tools/validation/` |
| Promptfoo / eval-oriented workflows | Repeatable prompt and artifact checks before accepting generated outputs. Dry-run matrix remains planned-only proof. | `Tools/ai/run_pipeline_dry_run_matrix.py`, `Tools/validation/`, `output/validation/` |
| DeepEval / LLM quality metrics | Qualitative scoring ideas for generated plans and artifacts, without replacing local evidence/telemetry contracts. | `docs/QUALITY_GATE.md`, `docs/AI_PIPELINE_OPTIMIZATION.md`, `docs/AI_SELECTIVE_PLANNER.md` |
| OpenAI Evals-style task sets | Dataset/task-driven regression checks for agent behavior. | `docs/EXECUTION_PLANS/`, `Tools/validation/`, future eval fixtures |
| Model Context Protocol concepts | Tool/context boundary discipline, explicit contracts and capability visibility. | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, `Tools/ai/build_runtime_tool_capability_manifest.py` |
| OpenAI Harness / Symphony concepts | Agent-first repository design, task/workspace orchestration, proof-of-work reports and workflow versioning. | `docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md`, `WORKFLOW.md`, `docs/EXECUTION_PLANS/`, `Tools/workflow/run_unified_local_ai_refactor.ps1` |
| Git-trackable local evidence bundles | Compact review evidence for GitHub-only agents without committing ignored `output/**` reports. | `Tools/ai/build_github_evidence_bundle.py`, `Tools/validation/check_github_evidence_bundle.py`, `docs/LOCAL_VALIDATION_EVIDENCE/` |
| Runtime tool telemetry and capability manifests | Completeness accessory for evidence, patch plans and broker/tool execution state. | `Tools/ai/build_runtime_tool_usage_telemetry.py`, `Tools/ai/build_runtime_tool_capability_manifest.py`, `Tools/ai/build_full_toolbox_run_telemetry_summary.py`, `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| Manual-review patch-plan workflows | Documentation-only patch-plan handoff, validation and compact task-scoped evidence. Full-run-derived patch plans require telemetry/capability context. | `docs/PATCH_SPEC_WORKFLOW.md`, `docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md`, `Tools/validation/run_agent_review_patch_plan_full_validation.py`, `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md` |

## Adopted principles

### 1. Keep the repository as the source of truth

AI agents should rely on project files first, then use external references only as background.

Priority order:

1. `AGENTS.md`;
2. `README.md` and `WORKFLOW.md`;
3. `docs/README.md`;
4. `docs/LOCAL_AI_RUN_BOOTSTRAP.md`;
5. `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md`;
6. `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` when launcher/manifest semantics are involved;
7. current execution plans;
8. current validators, schema docs and telemetry/bundle docs;
9. external references summarized here.

### 2. Do not vendor full external repositories

Full external repositories are useful for local study but should not be committed unless a specific file is small, license-compatible and intentionally adapted.

Preferred pattern:

```text
external concept
  -> local guide in docs/
  -> local validator or schema
  -> local launcher/report/telemetry/bundle surface
```

### 3. Convert knowledge into enforceable contracts

A reference is only useful to this repository when it results in at least one of:

- a clear rule in `AGENTS.md` or `docs/`;
- a schema requirement;
- a validator check;
- a launcher mode/manifest field;
- a telemetry or capability manifest field;
- a package README update;
- a documented execution plan;
- a shared AI-to-AI bundle/final-summary field.

### 4. Keep AI instructions compact

Large instructions degrade agent reliability. Long background belongs in `docs/`; immediate rules belong in `AGENTS.md` and package-level README files.

### 5. Prefer provider-agnostic architecture

The project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.

Provider-agnostic does not mean provider-invisible. Provider degradation, fallback and quality-gate state must be visible in telemetry/bundle handoff when provider output influences evidence or patch plans.

### 6. Keep local evidence Git-trackable and task-scoped

Full validation/provider reports belong under ignored `output/**`. GitHub-visible evidence should be compact, task-scoped and written under `docs/LOCAL_VALIDATION_EVIDENCE/` by a validator or evidence bundle builder.

For the agent-review documentation patch-plan lane, use:

```text
Tools/validation/run_agent_review_patch_plan_full_validation.py
```

This wrapper builds and validates `agent_review_doc_patch_plan_evidence.*` without provider execution or automatic patch application.

When the patch plan comes from full-run evidence, include or reference the companion telemetry/capability/final-summary artifacts.

## Full-run proof-of-work rule

A broad local-AI proof-of-work is not complete unless these surfaces are reviewed together when relevant:

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

Do not infer full-run success from:

```text
file existence
dry-run matrix success
provider report existence
NPU smoke success
patch plan existence
reviewed patch spec existence
```

## Local reference folders

Optional local-only folders:

```text
docs/external_references/
docs/references/
```

These folders are intentionally optional local study locations. Their absence in the committed branch is expected and must not be treated as a broken documentation reference, a missing source artifact, or a request to vendor upstream repositories.

Suggested `.gitignore` entries if those folders are used:

```gitignore
docs/external_references/
docs/references/
```

## Maintenance rules

When adding a new reference:

1. add it to this source map;
2. explain why it matters to this repository;
3. map it to concrete local files;
4. avoid copying large upstream content;
5. add or update a validator when the rule is enforceable;
6. add telemetry/capability/handoff implications when the reference affects full-run evidence or patch plans;
7. update `docs/README.md` if the new document is stable.

<!-- IA-CARMINE:PATCH-PLAN-APPLICATION:START -->

## IA-Carmine patch-plan application notes

This managed block was generated from `output/patch_specs/agent_review_patch_plan.json`.
It records the manual-review patch-plan decisions for this file without applying runtime/provider changes.

### `det_doc_code_005` — `doc_code`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/AI_REFERENCE_SOURCE_MAP.md`
- Manual review required: `True`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

### `det_doc_code_006` — `doc_code`

- Source: `gpu_recommendation`
- Status: `ready_for_manual_review`
- Risk: `low`
- Target file: `docs/AI_REFERENCE_SOURCE_MAP.md`
- Manual review required: `True`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.
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

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_005:docs-ai_reference_source_map.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_005`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/AI_REFERENCE_SOURCE_MAP.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_005:docs-ai_reference_source_map.md -->

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN id=det_doc_code_006:docs-ai_reference_source_map.md -->

### IA-Carmine agent-review patch note

This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.

- Plan id: `det_doc_code_006`
- Area: `doc_code`
- Source: `gpu_recommendation`
- Risk: `low`
- Target: `docs/AI_REFERENCE_SOURCE_MAP.md`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.
- Validation commands:
  - `python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json`
  - `python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json`
  - `git diff --check`
  - `git status --short`
- Stop conditions:
  - Stop if the referenced file exists after refreshing master.
  - Stop if the fix requires creating runtime code instead of correcting documentation or references.
  - Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_code_006:docs-ai_reference_source_map.md -->
