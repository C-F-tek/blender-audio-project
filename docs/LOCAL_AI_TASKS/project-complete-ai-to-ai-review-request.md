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
ia_carmine/providers/provider_mesh/gpu_npu_parallel_orchestrator/cli.py
ia_carmine/providers/provider_mesh/gpu_deep_planning_review/cli.py
ia_carmine/providers/provider_mesh/gpu_deep_planning_supervised/cli.py
ia_carmine/product/agent_review/patch_plan/cli.py
ia_carmine/product/repository_product/github_evidence_bundle.py
Tools/validation/agent_review/patch_plan_smoke/cli.py
Tools/validation/repository_product/github_evidence_bundle/cli.py
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
ia_carmine
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
