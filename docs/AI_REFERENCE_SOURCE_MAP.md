# AI Reference Source Map

## Purpose

This file maps external AI-engineering references considered useful for this repository to local project documentation, validators and safe implementation areas.

The goal is to make concepts available to AI agents without committing full upstream repositories into this project and without bypassing the current IA-Carmine run-unica launcher, evidence, telemetry, discovery/index/CSV/file-line-limit and guardrail contracts.

This file is reference mapping, not a command catalog and not a managed patch-plan evidence container.

Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large tool/schema catalogs such as `Tools/validation/README.md` and `docs/JSON_SCHEMAS.md` are references only. They must not be treated as first operational entrypoints if too large or truncated.

## Current doctrine

Every external reference must be translated into the current project operating model:

```text
master contains PR #187 unified launcher baseline
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
smoke = separate non-full mode
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
400 lines = hard limit for maintained docs and source files
limitations = backlog to overcome, not reasons to skip available tools
telemetry accompanies evidence and patch plans for completeness
```

External concepts are useful only when they improve one of these local surfaces:

```text
AGENTS.md / docs guidance
run-unica launcher manifest
phase_status / phase_reports
validators and schema contracts
runtime tool usage telemetry
runtime tool capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
compact evidence
CSV/count and discovery/index evidence
file-line-limit evidence
manual-review patch plans/specs
```

Telemetry does not replace evidence or patch plans. It is the required companion that explains whether the related lanes executed, failed, were blocked, degraded, disabled, unavailable or planned-only.

## Current branch phase

```text
Baseline: master after PR #187 merge
Current documentation PR: #193 docs(ai): align operational docs with post-PR187 code state
Next clean report-only foundation candidate: PR #192
Useful but diverged evidence branch: PR #191
Mode: GitHub-only/API when maintainer is away
```

## Source map

| External reference family | Project use | Local canonical files |
|---|---|---|
| AGENTS.md conventions | Entry-point rules for AI coding agents, safe commands, permission boundaries, reading order and handoff expectations. | `AGENTS.md`, `CHATGPT.md`, `CHATGPT/README.md`, `README.md`, `WORKFLOW.md`, `docs/README.md`, `docs/AI_ONBOARDING.md` |
| OpenVINO / NPU references | Local inference, NPU-oriented helper contracts, provider-free preparation, fallback strategy and diagnostic-only NPU posture until quality promotion. | `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`, `Tools/npu/pipeline/README.md`, `Tools/validation/check_npu_pipeline_modules.py` |
| ONNX Runtime / runtime-agnostic inference | Separation between model, provider, orchestration, provider diagnostics and handoff telemetry. | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, `Tools/ai/build_full_toolbox_run_telemetry_summary.py` |
| Guardrails-style validation | Schema-first output validation, rejections, repair loops, explicit failure reports and completeness checks. | `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`, `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md`, `docs/AI_ARTIFACT_SCHEMAS.md`, `docs/QUALITY_GATE.md`, `Tools/validation/` |
| Promptfoo / eval-oriented workflows | Repeatable prompt and artifact checks before accepting generated outputs. Dry-run matrix remains planned-only proof. | `Tools/ai/run_pipeline_dry_run_matrix.py`, `Tools/validation/`, `output/validation/` |
| DeepEval / LLM quality metrics | Qualitative scoring ideas for generated plans and artifacts, without replacing local evidence/telemetry contracts. | `docs/QUALITY_GATE.md`, `docs/AI_PIPELINE_OPTIMIZATION.md`, `docs/AI_SELECTIVE_PLANNER.md` |
| OpenAI Evals-style task sets | Dataset/task-driven regression checks for agent behavior. | `docs/EXECUTION_PLANS/`, `Tools/validation/`, future eval fixtures |
| Model Context Protocol concepts | Tool/context boundary discipline, explicit contracts and capability visibility. | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`, `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, runtime capability manifests |
| OpenAI Harness / Symphony concepts | Agent-first repository design, task/workspace orchestration, proof-of-work reports and workflow versioning. | `docs/OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md`, `WORKFLOW.md`, `docs/EXECUTION_PLANS/`, `Tools/workflow/run_unified_local_ai_refactor.ps1` |
| Git-trackable local evidence bundles | Compact review evidence for GitHub-only agents without committing ignored `output/**` reports. | `Tools/ai/build_github_evidence_bundle.py`, `Tools/validation/check_github_evidence_bundle.py`, `docs/LOCAL_VALIDATION_EVIDENCE/` |
| Runtime tool telemetry and capability manifests | Completeness accessory for evidence, patch plans and broker/tool execution state. | `Tools/ai/build_runtime_tool_usage_telemetry.py`, runtime capability manifest builders, `Tools/ai/build_full_toolbox_run_telemetry_summary.py`, `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| Discovery/index/CSV-count surfaces | Repository visibility, refactor/reuse evidence, sizing, callable inventory and scanner/index drift handling. | `docs/DATA_FLOW.md`, `docs/LOCAL_AI_WORKFLOW.md`, `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md`, `Tools/validation/build_markdown_inventory.py`, `Tools/validation/build_script_inventory.py` |
| File line-limit surfaces | Maintained docs/source file size evidence for the 400-line policy. | `Tools/validation/check_file_line_limits.py`, `docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md` |
| Manual-review patch-plan workflows | Documentation-only patch-plan handoff, validation and compact task-scoped evidence. Run-unica-derived patch plans require telemetry/capability/discovery context. | `docs/PATCH_SPEC_WORKFLOW.md`, current `docs/LOCAL_AI_TASKS/*.md`, `docs/LOCAL_VALIDATION_EVIDENCE/` |

## Adopted principles

### 1. Keep the repository as the source of truth

AI agents should rely on project files first, then use external references only as background.

Priority order:

1. `AGENTS.md`;
2. `CHATGPT.md` and `CHATGPT/README.md`;
3. `docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md`;
4. `docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md`;
5. `docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md`;
6. `README.md` and `WORKFLOW.md`;
7. `docs/README.md`;
8. `docs/LOCAL_AI_RUN_BOOTSTRAP.md`;
9. `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md`;
10. `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` when launcher/manifest semantics are involved;
11. current execution plans and current task docs;
12. current validators, schema docs, telemetry/bundle docs and compact evidence;
13. external references summarized here.

`docs/JSON_SCHEMAS.md` remains a broad schema notebook/catalog and must not override compact current contracts.

### 2. Do not vendor full external repositories

Full external repositories are useful for local study but should not be committed unless a specific file is small, license-compatible and intentionally adapted.

Preferred pattern:

```text
external concept
  -> local guide in docs/
  -> local validator or schema
  -> local launcher/report/telemetry/bundle/discovery surface
```

### 3. Convert knowledge into enforceable contracts

A reference is useful to this repository when it results in at least one of:

- a clear rule in `AGENTS.md` or `docs/`;
- a schema requirement;
- a validator check;
- a launcher mode/manifest field;
- a telemetry or capability manifest field;
- a CSV/count or discovery/index evidence surface;
- a file-line-limit evidence surface;
- a package README update;
- a documented execution plan;
- a shared AI-to-AI bundle/final-summary field.

### 4. Keep AI instructions compact

Large instructions degrade agent reliability. Long background belongs in catalog/supporting docs; immediate rules belong in `AGENTS.md`, compact bridge docs and package-level README files.

Maintained Markdown and source files should stay under 400 lines. Oversized files are technical debt to measure and split progressively.

### 5. Prefer provider-agnostic architecture

The project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.

Provider-agnostic does not mean provider-invisible. Provider degradation, fallback and quality-gate state must be visible in telemetry/bundle handoff when provider output influences evidence or patch plans.

### 6. Keep local evidence Git-trackable and task-scoped

Full validation/provider reports belong under ignored `output/**`. GitHub-visible evidence should be compact, task-scoped and written under `docs/LOCAL_VALIDATION_EVIDENCE/` by a validator or evidence bundle builder.

When a patch plan comes from run-unica evidence, include or reference the companion telemetry/capability/final-summary and discovery/index/CSV/file-line-limit artifacts.

### 7. Treat limitations as backlog to overcome

A limitation note is not a reason to skip available tools.

```text
limitation documented -> backlog item to overcome
current validator failure -> current blocker/degraded state
current capability manifest unavailable -> current unavailable state
historical note saying no tool access -> obsolete unless current evidence confirms it
```

## Run-unica proof-of-work rule

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
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
```

Do not infer run-unica success from:

```text
file existence
dry-run matrix success
provider report existence
NPU smoke success
patch plan existence
reviewed patch spec existence
large Markdown mentions it
```

## Local reference folders

Optional local-only folders:

```text
docs/external_references/
docs/references/
```

These folders are intentionally optional local study locations. Their absence in the committed branch is expected and must not be treated as a broken documentation reference, missing source artifact, or request to vendor upstream repositories.

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
6. add telemetry/capability/handoff implications when the reference affects run-unica evidence or patch plans;
7. add CSV/index/discovery/file-line-limit implications when it affects repository inventory or refactor/reuse flows;
8. update `docs/README.md` if the new document is stable.
