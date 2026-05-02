# Local Validation Evidence Bundle

- Generated at: `2026-05-02T20:10:41`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `13`
- `patch_plan_summary_seen`: `True`

## Reports

### `output/validation/python_syntax_project_complete_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/npu_provider_environment_project_complete_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/code_interpreter_project_complete_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `112`

### `output/ai_pipeline/project_complete_20260502-195523_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `build_agent_review_patch_plan.py`

### `output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `post_validation_ai_work_packet`
- Passed: `True`
- Ollama: `{'used': False, 'model': None, 'error': '', 'text_preview': ''}`

### `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/ai_pipeline/repository_change_proposals.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `repository_change_proposals`
- Passed: `True`

### `output/patch_specs/agent_review_patch_plan_project_complete_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`
- Patch plan summary count: `12`
- Fallback used: `True`
- Manual review required: `True`

### `output/validation/agent_review_patch_plan_smoke_project_complete_20260502-195523.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`
- Warnings: `['fallback_used is true; GPU planner produced no usable ready recommendation']`

## Patch plan summary

### `output/patch_specs/agent_review_patch_plan_project_complete_20260502-195523.json`

- Patch plan count: `12`
- Fallback used: `True`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### fallback_doc_code_001 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/config_model.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

#### fallback_doc_code_002 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/diagnostics.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

#### fallback_doc_code_003 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

#### fallback_doc_code_004 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

#### fallback_doc_code_005 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_SOURCE_MAP.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

#### fallback_doc_code_006 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_SOURCE_MAP.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

#### fallback_doc_code_007 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code-quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

#### fallback_doc_code_008 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code_quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

#### fallback_doc_code_009 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/ci.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

#### fallback_doc_doc_001 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

#### fallback_doc_doc_002 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/JSON_SCHEMAS.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

#### fallback_doc_doc_003 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/README.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.


## Artifact manifest

- `output/validation/python_syntax_project_complete_20260502-195523.json` exists=`True` size=`31633` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_provider_environment_project_complete_20260502-195523.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/analysis/code_interpreter_project_complete_20260502-195523.json` exists=`True` size=`1144493` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/project_complete_20260502-195523_orchestrator.json` exists=`True` size=`20138` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json` exists=`True` size=`168570` suffix=`.json` preview_chars=`1500`
- `output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json` exists=`True` size=`190374` suffix=`.json` preview_chars=`1500`
- `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json` exists=`True` size=`7530` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/repository_change_proposals.json` exists=`True` size=`7816` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/agent_review_patch_plan_project_complete_20260502-195523.json` exists=`True` size=`60479` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_patch_plan_smoke_project_complete_20260502-195523.json` exists=`True` size=`1313` suffix=`.json` preview_chars=`1287`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/project-complete-ai-to-ai-review-request.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `5012`
- SHA-256: `4820d57bccde654d2b88fd31d1932fb757dc5c93ed4abb7a1f00b4c66fc3384d`
- Content included: `True`
- Content truncated: `False`

```text
# Project Complete AI-to-AI Review Request

## Purpose

Canonical Markdown request for a project-only complete local AI run.

This file is the first task document to provide to the local AI workflow. The run must not start from ad-hoc chat instructions only.

## Core flow

```text
read this Markdown request
read the official local AI runbook
run the local project analysis tools
run the local GPU planner
run the local NPU checkpoint auditor when available
run the post-validation packet step
run the manual-review fallback plan step when needed
build a compact evidence bundle
validate the bundle
commit and push only the compact bundle and small notes
review results from GitHub evidence
```

## Required reading order

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md
docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md
docs/PROJECT_STATUS_POINT.md
docs/AGENT_REVIEW_CODE_PATCH_PLAN.md
docs/TOOL_AGNOSTIC_ARTIFACT_EXPANSION.md
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/build_agent_review_patch_plan.py
Tools/ai/build_github_evidence_bundle.py
Tools/validation/run_agent_review_patch_plan_smoke.py
Tools/validation/check_github_evidence_bundle.py
```

If instructions conflict, stop and report the conflict instead of continuing.

## Run type

```text
run_type: complete
scope: project-only
local_ai_lanes: enabled
```

A complete run means all applicable local tools and local AI lanes are active for the selected scope.

Enabled lanes:

```text
static code interpreter
validation tools
artifact and bundle tools
GPU planner
NPU checkpoint auditor when available
post-validation packet
manual-review fallback plan builder
bundle validation
```

## Project-only scope

Include:

```text
Tools/ai
Tools/validation
Tools/npu
Tools/workflow
Scripting/v61b
Scripting/shared
docs
```

Exclude as analysis targets:

```text
old script legacy/**
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/**
Scripting/v61b_backgood/**
renders/**
```

Local output reports may be used as inputs, but raw local output files are not the Git review artifact. The Git review artifact is the compact bundle under `docs/LOCAL_VALIDATION_EVIDENCE/`.

## Main request

Review the current project AI and tooling pipeline after PR #109 was merged.

Focus on:

```text
static analysis versus provider recommendation agreement
whether GPU planning produces actionable recommendations from ready evidence
whether NPU checkpoint auditing is useful and non-blocking
whether fallback manual-review plan generation is still needed
which one or two project-only targets should become the next small review PR
```

Produce advisory outputs and manual-review candidates only.

## AI improvement impressions

In addition to evidence-backed recommendations, provide a separate section named `AI improvement impressions`.

This section should contain operational impressions that emerged while reading the repository, running the local tools, comparing reports and observing provider behavior.

Each impression must be clearly marked as one of:

```text
evidence-backed
inferred from multiple signals
speculative but potentially useful
```

For each impression include:

```text
short title
why it may improve the project
evidence or signals that triggered it
risk if ignored
minimal next action
whether it should become a task, issue, doc update or future PR
```

Useful impression categories include:

```text
architecture simplification
pipeline reuse in other projects
tooling ergonomics
evidence quality
provider orchestration
GPU/NPU workload split
manual-review friction
bundle/audit readability
validator coverage
future refactor candidates
```

Do not present impressions as facts unless the evidence supports them. Do not propose automatic edits from impressions. Convert them into reviewable task candidates only.

## Required final artifact

```text
docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_<timestamp>.json
docs/LOCAL_VALIDATION_EVIDENCE/project_complete_ai_to_ai_bundle_<timestamp>.md
```

The bundle must include this Markdown request as an included artifact so the reviewer can see the exact task given to the local AI system.

## Recommendation format

Each useful recommendation should include:

```text
target file or module
reason from evidence
risk level
minimal review strategy
validation commands
stop conditions
static/provider agreement status
```

Prefer small project infrastructure or tooling targets over large visual legacy scripts.

## Stop conditions

Stop and report if:

```text
required evidence is missing and cannot be regenerated safely
the GPU planner is unavailable for a complete run
NPU auditing would block GPU planning instead of acting as support
any tool attempts automatic patching
raw local output files would become the committed review artifact
```

```

### `output/analysis/code_interpreter_project_complete_20260502-195523.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6959`
- SHA-256: `f4c8509905fd9981965800df332fb1f9004059bfd8bf416ccf0260a44ca18032`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `226`
- Parsed files: `226`
- Total lines: `60020`
- Total functions: `2175`
- Total classes: `90`
- Risk signals: `43`
- TODO/FIXME markers: `21`
- Recommendation count: `112`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Scripting/v61b/animation.py` — `1079` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `714` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `628` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/workflow/workflow_debug.py` — `607` lines, risk `medium`
- `Tools/ai/build_repository_change_proposals.py` — `582` lines, risk `medium`
- `Tools/ai/build_ai_context_pack.py` — `575` lines, risk `medium`
- `Tools/ai/run_pipeline_dry_run_matrix.py` — `573` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_plan.py` — `562` lines, risk `medium`
- `Scripting/v61b/atmosphere_setup.py` — `554` lines, risk `medium`
- `Tools/ai/suggest_repository_updates.py` — `551` lines, risk `medium`

## Recommendations

- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected
- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module
- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected
- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_011` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected
- `code_static_012` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_013` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_014` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected
- `code_static_015` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_017` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected
- `code_static_018` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_019` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected
- `code_static_020` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_021` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_022` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_023` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_024` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_025` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_026` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_027` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_028` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_029` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_030` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_031` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_patch_specs_from_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_033` `Tools/ai/build_repository_change_proposals.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_034` `Tools/ai/build_selective_execution_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_035` `Tools/ai/build_workload_quality_lane_routing.py` risk `medium`: complex functions detected
- `code_static_036` `Tools/ai/check_local_resource_lanes.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/check_npu_provider_environment.py` risk `medium`: large functions detected, complex functions detected, static risk calls detected
- `code_static_038` `Tools/ai/model_json.py` risk `medium`: complex functions detected
- `code_static_039` `Tools/ai/pipeline/preflight.py` risk `medium`: complex functions detected
- `code_static_040` `Tools/ai/pipeline/remediation.py` risk `medium`: large functions detected, complex functions detected, TODO/FIXME markers detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/ai_pipeline/project_complete_20260502-195523_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1170`
- SHA-256: `76f6a2fedd4670d7b8bd3103b1be9f8c22479397faf8bec749d06b4b1bb40289`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `True`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `0`
- `elapsed_seconds`: `706.195`
- `npu_audit_count`: `5`
- `npu_audit_success_count`: `5`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `repair_attempt_failed`
- `gpu_evidence_ready_for_manual_patch_count`: `12`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `5`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `True`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: `repair_attempt_failed`
- `manual_review_required`: `True`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `4` status=`finished` class=`usable_audit_text` success=`True`
- round `8` status=`finished` class=`usable_audit_text` success=`True`
- round `12` status=`finished` class=`usable_audit_text` success=`True`
- round `16` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `882`
- SHA-256: `e8e4e1e676b1679ec688e2cf4d29a774e2b889699c6dbb3231a5d846bfacdfe3`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `True`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `668.685`
- Round count: `24`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- JSON parse error count: `16`
- Empty recommendations reason: `repair_attempt_failed`
- Evidence ready for manual patch count: `12`

## Decision

- `ready_for_patch_plan`: `False`
- `ready_count`: `0`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `True`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `manual_review_required`: `True`

## Recommendations


```

### `output/ai_packets/gpu_planner_nonempty_recommendations_advisory.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3973`
- SHA-256: `df251fad3c39f4fa7f0e4950bf17aa3bc643465640a98a87aca0b997e9804110`
- Content included: `True`
- Content truncated: `False`

```text
# Post-Validation AI Work Packet

- Generated at: `2026-05-01T20:50:40`
- Repo: `C:\Users\carmi\blender\blender-audio-project`
- Profile: `core`
- Ollama used: `False`
- Packet manifest: `C:\Users\carmi\blender\blender-audio-project\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json`

## Advisory context routing

- Enforced: `True`
- Provider execution performed: `False`
- Advisory lanes: `ollama`
- Excluded advisory lanes: `npu`

## Deterministic suggestions

### P1 — Fix failing validation reports before new runtime work

- Area: `validation`
- Details: C:\Users\carmi\blender\blender-audio-project\output\validation\ai_workload_report_quality.json: ['npu: alphabetic character ratio is too low', 'npu: word count is too low', 'npu: report appears numeric/hex-like rather than natural language']

### P2 — Review active execution plans before opening the next milestone

- Area: `execution_plans`
- Details: docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md; docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md; docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md; docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_ai_pipeline_report_contracts.md; docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_output_policy_provider_preflight.md; docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md; docs/EXECUTION_PLANS/active/2026-04-30_runtime_safe_provider_report_adoption.md; docs/EXECUTION_PLANS/active/2026-04-30_validator_report_consistency_review.md

### P2 — Prefer additive observability before provider or Blender runtime changes

- Area: `agnostic_core`
- Details: Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.

## Inputs

### Trusted context files
- `AGENTS.md`
- `WORKFLOW.md`
- `docs/AI_DOCS_ENTRYPOINT.md`
- `docs/PROJECT_STATUS_POINT.md`
- `docs/TECH_DEBT_TRACKER.md`
- `docs/REFACTORING_AND_REUSE_PLAN.md`
- `docs/JSON_SCHEMAS.md`
- `docs/AI_ARTIFACT_SCHEMAS.md`
- `Tools/npu/pipeline/README.md`
- `Tools/validation/README.md`
- `./docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md`
- `./Tools/ai/run_agent_gpu_deep_planning_review.py`
- `./Tools/ai/run_agent_gpu_deep_planning_supervised.py`
- `./Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py`
- `./Tools/ai/build_agent_review_patch_plan.py`

### Report files
- `output/validation/python_syntax.json`
- `output/validation/ai_pipeline_modules.json`
- `output/validation/npu_pipeline_modules.json`
- `output/validation/npu_pipeline_helper_tests.json`
- `output/validation/npu_pipeline_docs.json`
- `output/validation/provider_result_parsing.json`
- `output/validation/provider_result_report.json`
- `output/validation/ai_workload_report_quality.json`
- `output/validation/ai_workload_quality_lane_routing.json`
- `output/validation/npu_decode_quality_remediation.json`
- `output/validation/npu_decode_smoke_diagnostic.json`
- `output/validation/npu_runtime_output_manifest.json`
- `output/validation/local_ai_resource_lanes.json`
- `output/validation/local_provider_probe.json`
- `output/validation/execution_plan_status.json`
- `output/validation/validation_report_contract.json`
- `output/validation/docs_links.json`
- `./output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json`
- `output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.json`

## Guardrails

- Advisory only: do not auto-apply edits from this packet.
- Output/input paths are configurable; defaults are not part of the architecture boundary.
- Validate locally before committing generated indexes.
- Keep provider execution changes in a separate explicitly scoped milestone.

```

### `output/ai_packets/gpu_planner_nonempty_recommendations_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3476`
- SHA-256: `c13cf9413bd6e464df8b12b81138ae78a1dec8b8a06d76f8b31c5f6215410c9f`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-01T20:50:40`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-AI-WORKLOAD-REPORT-QUALITY-GATE — Gate AI workload reports before using them as advisory context

- Priority: `P1`
- Area: `local_ai_workloads`
- Change type: `workload_quality_gate`
- Apply mode: `manual_review_only`
- Rationale: AI workload report quality found usable lanes: ollama; unusable lanes: npu. Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed.

### Evidence summary

```json
{
  "workload_quality_decision": {
    "quality_report_present": true,
    "usable_lanes": [
      "ollama"
    ],
    "unusable_lanes": [
      "npu"
    ],
    "ollama_gpu_primary_advisory_allowed": true,
    "npu_excluded_from_primary_advisory": true,
    "routing_policy": "usable_text_lanes_only_for_advisory_context"
  }
}
```

### Target files
- `Tools/validation/check_ai_workload_report_quality.py`
- `Tools/npu/run_npu_review.py`
- `Tools/ai/suggest_repository_updates.py`
- `Tools/ai/build_repository_change_proposals.py`
- `Tools/validation/README.md`
- `docs/JSON_SCHEMAS.md`

### Patch sketch
- Keep Ollama/GPU workload reports as primary advisory context when classified usable.
- Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.
- Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.
- Add report metadata that distinguishes availability, execution and output usability.

### Suggestion outputs
- `python_code` `Tools/validation/check_ai_workload_report_quality.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/npu/run_npu_review.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/build_repository_change_proposals.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change would execute providers implicitly or by default.
- Any change would hide a failing/unusable AI workload report instead of reporting it.
- Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

### `output/ai_pipeline/repository_change_proposals.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `3476`
- SHA-256: `f2f6602adaa4a76ea8240d6a2a1d89edc7ffe0123ac49cf962aeb57512e2770d`
- Content included: `True`
- Content truncated: `False`

```text
# Repository Change Proposals

- Generated at: `2026-05-02T20:10:23`
- Profile: `core`
- Apply mode: `manual_review_only`
- Proposal count: `1`

## P-AI-WORKLOAD-REPORT-QUALITY-GATE — Gate AI workload reports before using them as advisory context

- Priority: `P1`
- Area: `local_ai_workloads`
- Change type: `workload_quality_gate`
- Apply mode: `manual_review_only`
- Rationale: AI workload report quality found usable lanes: ollama; unusable lanes: npu. Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed.

### Evidence summary

```json
{
  "workload_quality_decision": {
    "quality_report_present": true,
    "usable_lanes": [
      "ollama"
    ],
    "unusable_lanes": [
      "npu"
    ],
    "ollama_gpu_primary_advisory_allowed": true,
    "npu_excluded_from_primary_advisory": true,
    "routing_policy": "usable_text_lanes_only_for_advisory_context"
  }
}
```

### Target files
- `Tools/validation/check_ai_workload_report_quality.py`
- `Tools/npu/run_npu_review.py`
- `Tools/ai/suggest_repository_updates.py`
- `Tools/ai/build_repository_change_proposals.py`
- `Tools/validation/README.md`
- `docs/JSON_SCHEMAS.md`

### Patch sketch
- Keep Ollama/GPU workload reports as primary advisory context when classified usable.
- Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.
- Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.
- Add report metadata that distinguishes availability, execution and output usability.

### Suggestion outputs
- `python_code` `Tools/validation/check_ai_workload_report_quality.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/npu/run_npu_review.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/suggest_repository_updates.py` (manual_patch_suggestion, manual_review_only)
- `python_code` `Tools/ai/build_repository_change_proposals.py` (manual_patch_suggestion, manual_review_only)
- `markdown` `Tools/validation/README.md` (manual_patch_suggestion, manual_review_only)
- `markdown` `docs/JSON_SCHEMAS.md` (manual_patch_suggestion, manual_review_only)

### Validation
- `python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json`
- `powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json`

### Stop conditions
- Any change would execute providers implicitly or by default.
- Any change would hide a failing/unusable AI workload report instead of reporting it.
- Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.

## Guardrail

These are proposals only. They must not be auto-applied without explicit review.

```

### `output/patch_specs/agent_review_patch_plan_project_complete_20260502-195523.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7021`
- SHA-256: `4d797ebe1367bb07275f522417e6fc8e62f86a81a184a00795ee3bd25f1dd26f`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Patch Plan

- Passed: `True`
- Apply mode: `report_only_manual_review_patch_plan`
- Provider execution performed: `False`
- Patch application performed: `False`
- Patch plan count: `12`
- Fallback used: `True`
- Manual review required: `True`

## Inputs

- `orchestrator`: `output/ai_pipeline/project_complete_20260502-195523_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json`
- `orchestrator_kind`: `agent_gpu_npu_parallel_orchestrator`
- `evidence_kind`: `agent_review_evidence_sufficiency`
- `gpu_kind`: `agent_gpu_deep_planning_supervised`

## Patch plans

### fallback_doc_code_001 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/config_model.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

### fallback_doc_code_002 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `Scripting/shared/diagnostics.py` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

### fallback_doc_code_003 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

### fallback_doc_code_004 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

### fallback_doc_code_005 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/external_references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/external_references`.

### fallback_doc_code_006 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `docs/references` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `docs/references`.

### fallback_doc_code_007 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code-quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

### fallback_doc_code_008 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/code_quality.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

### fallback_doc_code_009 — doc_code
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Patch the source Markdown only; do not create missing code/runtime files from this fallback. Review the referenced path `github/workflows/ci.yml` and decide whether it is stale, intentionally future-facing, or should point to an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

### fallback_doc_doc_001 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

### fallback_doc_doc_002 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['docs/JSON_SCHEMAS.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

### fallback_doc_doc_003 — doc_doc
- Source: `evidence_sufficiency_fallback`
- Risk: `low`
- Target files: `['Tools/validation/README.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a small targeted cross-reference for `code_contract_drift`, `docs_contract_drift`. Do not duplicate large contract sections; link or summarize the canonical location instead.

## Guardrail

This artifact is a plan only. It contains no replacements and must not be treated as an apply queue.

```

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `35905`
- SHA-256: `a2216b89a69fc267b8015cfcbf775591b4c8b05abd127aef322936947f80683c`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_review_evidence_sufficiency",
  "generated_at": "2026-05-01T17:46:48",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_evidence_sufficiency",
  "inputs": {
    "refined_review": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json",
    "refined_proposals": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_proposals_v3.json",
    "refined_proposal_count": 2,
    "context_reports": [
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agent_memory_inventory.json",
        "exists": true,
        "kind": "agent_memory_inventory",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agnostic_tool_inventory.json",
        "exists": true,
        "kind": "agent_agnostic_tool_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "tool_count": 166,
          "category_counts": {
            "validator": 50,
            "provider_probe_or_adapter": 41,
            "orchestrator_pipeline": 30,
            "support_tool": 28,
            "agent_context_builder": 6,
            "proposal_or_review_builder": 5,
            "git_helper": 3,
            "review_helper": 3
          },
          "owner_lane_counts": {
            "npu_explicit_provider_tool": 65,
            "cpu_validation": 29,
            "gpu_cuda_explicit_provider_tool": 27,
            "cpu_support": 22,
            "cpu_orchestration": 18,
            "cpu_context_builder": 3,
            "cpu_proposal_builder": 2
          },
          "consumed_lane_counts": {
            "cpu": 166,
            "npu": 123,
            "gpu_cuda": 89
          },
          "apply_mode_counts": {
            "not_declared": 121,
            "manual_review_only": 20,
            "report_only": 16,
            "explicit_git_operation": 9
          },
          "provider_execution_default_counts": {
            "none_or_reported": 151,
            "explicit_only": 15
          }
        }
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_transient_request_context.json",
        "exists": true,
        "kind": "agent_transient_request_context",
        "passed": true,
        "error": "",
        "summary": {}
      }
    ]
  },
  "areas": {
    "doc_code": {
      "area": "doc_code",
      "item_count": 9,
      "ready_for_manual_patch_count": 9,
      "needs_more_context_count": 0,
      "items": [
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/config_model.py",
          "candidate_references": [
            "Scripting/shared/config_model.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/config_model.py",
                "Scripting/shared/config_model.py"
              ],
              "snippet": " still needing staged decomposition. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do"
            },
            {
              "path": "Scripting/shared/config_model.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/diagnostics.py",
          "candidate_references": [
            "Scripting/shared/diagnostics.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/diagnostics.py",
                "Scripting/shared/diagnostics.py"
              ],
              "snippet": "on. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do not assume every status document"
            },
            {
              "path": "Scripting/shared/diagnostics.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/external_references",
          "candidate_references": [
            "docs/external_references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/external_references",
                "docs/external_references"
              ],
              "snippet": "rnal repositories.\n\n## What this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;\n- a replacement for local validation;\n- a runtime dependency;\n- a permission to perform destructive changes;\n- a reason to bypass `AGENTS.md`, execution plans or validators.\n\n## Repository policy\n\nFull external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nThe committed repository should contain only:\n\n```text\ndocs/AI_REFERENCE_ONBOARDING.md\ndocs/AI_REFERENCE_SOURCE_MAP.md\ndocs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\ndocs/AI_GUARDRAILS_VALIDATION_GUIDE.md\ndocs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md\n```\n\nThis keeps remote AI agents effective without bloating the repository.\n\n## Recommended agent behavior\n\nWhen an AI agent uses this reference layer, it should:\n\n1. identify the target work area;\n2. read the related guide;\n3. map external concepts to existing project files;\n4. avoid introducing new dependencies unless explicitly approved;\n5. prefer additive documentation, validators and helper modules;\n6. preserve current Blender package behavior;\n7. keep NPU helper work provider-free unless a validated phase says otherwise;\n8. update `docs/README.md` when adding stable documentation;\n9. report uncertainty rather than inventing unsupported repository state.\n\n## Task routing\n\n| Task | Read first |\n|---|---|\n| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_"
            },
            {
              "path": "docs/external_references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/references",
          "candidate_references": [
            "docs/references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/references",
                "docs/references"
           
```

### `output/ai_pipeline/project_complete_20260502-195523_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `20138`
- SHA-256: `fdf74c5801328d125e3d5d7bbb422b25f0ebb4327d487b85648685e7fc59a3e9`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-02T20:09:33",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 706.195,
  "gpu_returncode": 0,
  "gpu_stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 668.685,\n  \"round_count\": 24,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"empty_recommendations_reason\": \"repair_attempt_failed\",\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "repair_attempt_failed",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "gpu_summary": {
    "passed": true,
    "round_count": 24,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 16,
    "repair_attempt_count": 18,
    "empty_recommendations_reason": "repair_attempt_failed",
    "evidence_ready_for_manual_patch_count": 12,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
    "decision": {
      "ready_for_patch_plan": false,
      "ready_count": 0,
      "needs_more_context_count": 0,
      "fallback_patch_plan_recommended": true,
      "npu_auditor_non_blocking": true,
      "npu_unusable_or_failed_count": 0,
      "npu_audit_success_count": 0,
      "npu_auditor_disabled_reason": "",
      "recommended_next_layer": "build_agent_review_patch_plan.py",
      "manual_review_required": true
    }
  },
  "checkpoint_dir": "output/ai_pipeline/project_complete_20260502-195523_checkpoints",
  "npu_audit_count": 5,
  "npu_audit_success_count": 5,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-02T19:58:59",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:01:07",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "gpu_review_blocked": false
    },
    {
      "round": 4,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_004.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_004_npu_async_audit.json",
      "started_at": "2026-05-02T20:01:09",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_004_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:03:19",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_004_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_004_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "gpu_review_blocked": false
    },
    {
      "round": 8,
      "checkpoint": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_008.json",
      "audit_output": "output/ai_pipeline/project_complete_20260502-195523_checkpoints/round_008_npu_async_audit.json",
      "started_at": "2026-05-02T20:03:21",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\project_complete_20260502-195523_checkpoints\\round_008_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "600",
        "--max-context-chars",
        "4000",
        "--max-prompt-chars",
        "1500",
        "--max-new-tokens",
        "512",
        "--run-npu"
      ],
      "finished_at": "2026-05-02T20:05:23",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_008_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\project_complete_20260502-195523_checkpoints\\\\round_008_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": tru
```

### `output/ai_pipeline/project_complete_20260502-195523_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `168570`
- SHA-256: `de0459178f46139aed0082527cee52e879b86d459684b84c0addb822396109c8`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-02T20:08:56",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
  "model_used": "qwen2.5-coder:14b",
  "ollama_base_url": "http://127.0.0.1:11434",
  "budget_minutes": 30,
  "elapsed_seconds": 668.685,
  "context_file_count": 240,
  "round_count": 24,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 70.87,
      "file_count": 10,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md",
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md"
      ],
      "response_chars": 21255,
      "raw_response_preview": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"AGENTS.md\",\n      \"exists\": true,\n      \"lines\": 123,\n      \"chars\": 4567,\n      \"content_preview\": \"# AGENTS.md\\n\\n## Purpose\\n\\nThis file is the main machine-readable entry point for any AI agent, coding assistant or automated reviewer that starts inside this repository.\\n\\nIt should contain practical instructions for AI systems:\\n\\n- repository identity;\\n- important folders;\\n- safe commands;\\n- validation commands;\\n- permission boundaries;\\n- refactoring rules;\\n- expected reporting format.\"\n    },\n    {\n      \"path\": \"WORKFLOW.md\",\n      \"exists\": true,\n      \"lines\": 150,\n      \"chars\": 6789,\n      \"content_preview\": \"# WORKFLOW.md\\n\\n## Purpose\\n\\nThis document outlines the general workflow for contributing to this repository, including guidelines for code submission, validation, and review.\\n\\n## Key Steps\\n\\n1. **Fork the Repository**: Create a fork of the main repository on GitHub.\\n2. **Clone Your Fork**: Clone your forked repository to your local machine.\\n3. **Create a New Branch**: For each new feature or bug fix, create a new branch from the `main` branch.\"\n    },\n    {\n      \"path\": \"README.md\",\n      \"exists\": true,\n      \"lines\": 100,\n      \"chars\": 4567,\n      \"content_preview\": \"# README.md\\n\\n## Welcome to the Blender Audio Project!\\n\\nThis repository contains the source code for the Blender Audio Project, an open-source project aimed at enhancing audio capabilities within Blender.\\n\\n## Getting Started\\n\\nTo get started with contributing to this project, follow these steps:\\n\\n1. **Clone the Repository**: Clone the main repository from GitHub.\"\n    },\n    {\n      \"path\": \"JSON_SCHEMAS.md\",\n      \"exists\": true,\n      \"lines\": 200,\n      \"chars\": 8901,\n      \"content_preview\": \"# JSON_SCHEMAS.md\\n\\n## Purpose\\n\\nThis document outlines the JSON schemas used within this repository for various configuration and data files. JSON schemas ensure that these files are structured correctly and contain all necessary fields.\\n\\n## Schemas Overview\\n\\n- **config.json**: Contains project-wide configuration settings.\\n- **data.json**: Stores data required by the application.\"\n    },\n    {\n      \"path\": \"AI_REFERENCE_ONBOARDING.md\",\n      \"exists\": true,\n      \"lines\": 180,\n      \"chars\": 7654,\n      \"content_preview\": \"# AI_REFERENCE_ONBOARDING.md\\n\\n## Purpose\\n\\nThis document serves as a reference for onboarding new AI agents and coding assistants to this repository. It provides an overview of the project structure, key components, and best practices.\\n\\n## Key Components\\n\\n- **AGENTS.md**: The main entry point for AI agents, containing practical instructions.\"\n    },\n    {\n      \"path\": \"AI_REFERENCE_SOURCE_MAP.md\",\n      \"exists\": true,\n      \"lines\": 190,\n      \"chars\": 8765,\n      \"content_preview\": \"# AI_REFERENCE_SOURCE_MAP.md\\n\\n## Purpose\\n\\nThis document maps the source code of this repository to its various components and functionalities. It helps AI agents understand how different",
      "parsed_response": {
        "summary": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"AGENTS.md\",\n      \"exists\": true,\n      \"lines\": 123,\n      \"chars\": 4567,\n      \"content_preview\": \"# AGENTS.md\\n\\n## Purpose\\n\\nThis file is the main machine-readable entry point for any AI agent, coding assistant or automated reviewer that starts inside this repository.\\n\\nIt should contain practical instructions for AI systems:\\n\\n- repository identity;\\n- important folders;\\n- safe commands;\\n- validation commands;\\n- permission boundaries;\\n- refactoring rules;\\n- expected reporting format.\"\n    },\n    {\n      \"path\": \"WORKFLOW.md\",\n      \"exists\": true,\n      \"lines\": 150,\n      \"chars\": 6789,\n      \"content_preview\": \"# WORKFLOW.md\\n\\n## Purpose\\n\\nThis document outlines the general workflow for contributing to this repository, including guidelines for code submission, validation, and review.\\n\\n## Key Steps\\n\\n1. **Fork the Repository**: Create a fork of the main repository on GitHub.\\n2. **Clone Your Fork**: Clone your forked repository to your local machine.\\n3. **Create a New Branch**: For each new feature or bug fix, create a new branch from the `main` branch.\"\n    },\n    {\n      \"path\": \"README.md\",\n      \"exists\": true,\n      \"lines\": 100,\n      \"chars\": 4567,\n      \"content_preview\": \"# README.md\\n\\n## Welcome to the Blender Audio Project!\\n\\nThis repository contains the source code for the Blender Audio Project, an open-source project aimed at enhancing audio capabilities within Blender.\\n\\n## Getting Started\\n\\nTo get started with contributing to this project, follow these steps:\\n\\n1. **Clone the Repository**: Clone the main repository from GitHub.\"\n    },\n    {\n      \"path\": \"JSON_SCHEMAS.md\",\n      \"exists\": true,\n      \"lines\": 200,\n      \"chars\": 8901,\n      \"content_preview\": \"# JSON_SCHEMAS.md\\n\\n## Purpose\\n\\nThis document outlines the JSON schemas used within this repository for various configuration and data files. JSON schemas ensure that these files are structured correctly and contain all nec",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "model_response_not_valid_json"
        ],
        "next_best_action": "review raw model response"
      },
      "json_ok": false,
      "parse_error": "JSONDecodeError: Expecting ',' delimiter: line 289 column 6 (char 20752)",
      "repair_attempt_count": 2,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "empty_recommendations_reason": "repair_attempt_failed",
      "evidence_ready_for_manual_patch_count": 12,
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 33.478,
      "file_count": 10,
      "files": [
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md",
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
        "docs/AI_REFERENCE_ONBOARDING.md",
        "docs/AI_REFERENCE_SOURCE_MAP.md",
        "docs/AI_SELECTIVE_PLANNER.md",
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md"
      ],
      "response_chars": 9543,
      "raw_response_preview": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"AGENTS.md\",\n      \"content\": \"# AGENTS.md\\n\\n## Purpose\\n\\nThis file outlines the rules and guidelines for AI coding agents working within this repository. It includes safe commands, permission boundaries, and reading order.\\n\\n## Safe Commands\\n\\n- `git pull`\\n- `git push`\\n- `python run_agent.py`\\n\\n## Permission Boundaries\\n\\nAI agents are allowed to:\\n\\n- Read files in the repository\\n- Write changes to local branches\\n- Execute safe commands listed above\\n\\n## Reading Order\\n\\n1. `AGENTS.md`\\n2. `WORKFLOW.md`\\n3. `docs/README.md`\\n4. Current execution plans\\n5. Current validators and schema docs\\n6. External references summarized in `docs/AI_REFERENCE_SOURCE_MAP.md`\"\n    },\n    {\n      \"path\": \"WORKFLOW.md\",\n      \"content\": \"# WORKFLOW.md\\n\\n## Purpose\\n\\nThis file describes the general workflow for contributing to this repository, including branching strategies, pull request processes, and code review guidelines.\\n\\n## Branching Strategies\\n\\n- Use feature branches for new features: `feature/feature-name`\\n- Use bugfix branches for fixing issues: `bugfix/issue-number`\\n- Use release branches for preparing releases: `release/version-number`\\n\\n## Pull Request Process\\n\\n1. Create a feature or bugfix branch from the main branch.\\n2. Implement changes and ensure all tests pass.\\n3. Open a pull request to the main branch.\\n4. Wait for code review and address any feedback.\\n5. Once approved, merge the pull request into the main branch.\\n\\n## Code Review Guidelines\\n\\n- Ensure code follows the project's coding standards.\\n- Verify that all tests are passing.\\n- Check for adherence to `AGENTS.md` rules.\"\n    },\n    {\n      \"path\": \"docs/README.md\",\n      \"content\": \"# README.md\\n\\n## Purpose\\n\\nThis file provides an overview of the documentation in this repository, including guides, validation rules, and execution plans.\\n\\n## Documentation Overview\\n\\n- **AI Provider Agnostic Pipeline Guide**: `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md`\\n- **NPU Runtime Reference Guide**: `docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md`\\n- **Guardrails Validation Guide**: `docs/AI_GUARDRAILS_VALIDATION_GUIDE.md`\\n- **JSON Schemas**: `docs/JSON_SCHEMAS.md`\\n- **AI Artifact Schemas**: `docs/AI_ARTIFACT_SCHEMAS.md`\\n\\n## Usage Instructions\\n\\n1. Read the relevant guide for your task.\\n2. Map external concepts to local files and validators.\\n3. Follow the project's coding standards and rules.\"\n    },\n    {\n      \"path\": \"docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\",\n      \"content\": \"# AI Provider Agnostic Pipeline Guide\\n\\n## Purpose\\n\\nThis guide explains how to implement a provider-agnostic pipeline for inference tasks, ensuring that the code can work with different providers like OpenVINO, Ollama, or local Python tools.\\n\\n## Key Concepts\\n\\n- **Orchestration**: Separation between model, provider, and orchestration logic.\\n- **Provider-Free Preparation**: Preparing the environment without hard-coding a specific provider.\\n- ",
      "parsed_response": {
        "files": [
          {
            "path": "AGENTS.md",
            "content": "# AGENTS.md\n\n## Purpose\n\nThis file outlines the rules and guidelines for AI coding agents working within this repository. It includes safe commands, permission boundaries, and reading order.\n\n## Safe Commands\n\n- `git pull`\n- `git push`\n- `python run_agent.py`\n\n## Permission Boundaries\n\nAI agents are allowed to:\n\n- Read files in the repository\n- Write changes to local branches\n- Execute safe commands listed above\n\n## Reading Order\n\n1. `AGENTS.md`\n2. `WORKFLOW.md`\n3. `docs/README.md`\n4. Current execution plans\n5. Current validators and schema docs\n6. External references summarized in `docs/AI_REFERENCE_SOURCE_MAP.md`"
          },
          {
            "path": "WORKFLOW.md",
            "content": "# WORKFLOW.md\n\n## Purpose\n\nThis file describes the general workflow for contributing to this repository, including branching strategies, pull request processes, and code review guidelines.\n
```

### `output/validation/agent_review_patch_plan_smoke_project_complete_20260502-195523.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `302`
- SHA-256: `149f07a209d7c38d3df17249a5e644a4bf7a6a8b398e958e9f79363acb540995`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Patch Plan Smoke

- Passed: `True`
- Return code: `0`
- Patch plan count: `12`
- Fallback used: `True`
- Provider execution performed: `False`
- Patch application performed: `False`

## Warnings

- fallback_used is true; GPU planner produced no usable ready recommendation


```

### `output/validation/npu_provider_environment_project_complete_20260502-195523.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `304`
- SHA-256: `ebcef793de1795cfc3f55063d9a02cad3467d28b6cee31e068b8067e70e75ded`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Provider Environment

- `passed`: `True`
- `npu_python`: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`
- `npu_python_exists`: `True`
- `openvino_import`: `True`
- `openvino_genai_import`: `True`
- `openvino_genai_pip_package`: `openvino-genai`
- `npu_available`: `True`

```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
