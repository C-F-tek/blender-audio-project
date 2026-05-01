# AI Reference Source Map

## Purpose

This file maps the external AI-engineering references considered useful for this repository to local project documentation, validators and safe implementation areas.

The goal is to make the concepts available to AI agents without committing full upstream repositories into this project.

## Source map

| External reference family | Project use | Local canonical files |
|---|---|---|
| AGENTS.md conventions | Entry-point rules for AI coding agents, safe commands, permission boundaries and reading order. | `AGENTS.md`, `docs/README.md`, `docs/AI_ONBOARDING.md` |
| OpenVINO / NPU references | Local inference, NPU-oriented helper contracts, provider-free preparation, fallback strategy. | `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`, `Tools/npu/pipeline/README.md`, `Tools/validation/check_npu_pipeline_modules.py` |
| ONNX Runtime / runtime-agnostic inference | Separation between model, provider and orchestration. | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `Tools/ai/pipeline/`, `Tools/npu/pipeline/` |
| Guardrails-style validation | Schema-first output validation, rejections, repair loops, explicit failure reports. | `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`, `docs/JSON_SCHEMAS.md`, `docs/AI_ARTIFACT_SCHEMAS.md`, `Tools/validation/` |
| Promptfoo / eval-oriented workflows | Repeatable prompt and artifact checks before accepting generated outputs. | `Tools/ai/run_pipeline_dry_run_matrix.py`, `Tools/validation/`, `output/validation/` |
| DeepEval / LLM quality metrics | Qualitative scoring ideas for generated plans and artifacts. | `docs/QUALITY_GATE.md`, `docs/AI_PIPELINE_OPTIMIZATION.md` |
| OpenAI Evals-style task sets | Dataset/task-driven regression checks for agent behavior. | `docs/EXECUTION_PLANS/`, `Tools/validation/`, future eval fixtures |
| Model Context Protocol concepts | Tool/context boundary discipline and explicit contracts. | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `Tools/ai/pipeline/`, `Tools/npu/pipeline/` |
| Git-trackable local evidence bundles | Compact review evidence for GitHub-only agents without committing ignored `output/**` reports. | `Tools/ai/build_github_evidence_bundle.py`, `Tools/validation/check_github_evidence_bundle.py`, `docs/LOCAL_VALIDATION_EVIDENCE/` |
| Manual-review patch-plan workflows | Documentation-only patch-plan handoff, validation and compact task-scoped evidence. | `docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md`, `Tools/validation/run_agent_review_patch_plan_full_validation.py`, `docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md` |

## Adopted principles

### 1. Keep the repository as the source of truth

AI agents should rely on project files first, then use external references only as background.

Priority order:

1. `AGENTS.md`;
2. `WORKFLOW.md`;
3. `docs/README.md`;
4. current execution plans;
5. current validators and schema docs;
6. external references summarized here.

### 2. Do not vendor full external repositories

Full external repositories are useful for local study but should not be committed unless a specific file is small, license-compatible and intentionally adapted.

Preferred pattern:

```text
external concept
  -> local guide in docs/
  -> local validator or schema
  -> local workflow command
```

### 3. Convert knowledge into enforceable contracts

A reference is only useful to this repository when it results in at least one of:

- a clear rule in `AGENTS.md` or `docs/`;
- a schema requirement;
- a validator check;
- a workflow command;
- a package README update;
- a documented execution plan.

### 4. Keep AI instructions compact

Large instructions degrade agent reliability. Long background belongs in `docs/`; immediate rules belong in `AGENTS.md` and package-level README files.

### 5. Prefer provider-agnostic architecture

The project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.

### 6. Keep local evidence Git-trackable and task-scoped

Full validation/provider reports belong under ignored `output/**`. GitHub-visible evidence should be compact, task-scoped and written under `docs/LOCAL_VALIDATION_EVIDENCE/` by a validator or evidence bundle builder.

For the agent-review documentation patch-plan lane, use:

```text
Tools/validation/run_agent_review_patch_plan_full_validation.py
```

This wrapper builds and validates `agent_review_doc_patch_plan_evidence.*` without provider execution or automatic patch application.

## Local reference folders

Optional local-only folders:

```text
docs/external_references/
docs/references/
```

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
6. update `docs/README.md` if the new document is stable.
