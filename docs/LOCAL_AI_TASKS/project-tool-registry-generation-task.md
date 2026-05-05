# Project tool registry generation task

## Objective

Create exactly one stable registry file:

```text
docs/LOCAL_AI_TASKS/project-tool-registry.md
```

This is the primary and only intended patch target for this task. The registry must be derived from current stable documentation and repository code, not from historical evidence bundles.

## Hard requirement

The patch plan must target exactly:

```text
docs/LOCAL_AI_TASKS/project-tool-registry.md
```

Do not propose ordinary patch plans for:

```text
docs/AI_ONBOARDING.md
docs/AI_REFERENCE_ONBOARDING.md
docs/AI_REFERENCE_SOURCE_MAP.md
docs/LOCAL_VALIDATION_EVIDENCE/**
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_*_cloud_semantic_deterministic_chunks/**
output/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
renders/**
*.db
*.sqlite
```

Historical evidence may be read only as context, never used as the primary patch target.

## Primary sources

Use:

```text
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/README.md
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/validation/**
Tools/workflow/**
Tools/npu/**
Scripting/v61b/**
analyze_wav.py
build_track_summary.py
```

## Required taxonomy

Classify each tool with one or more of:

```text
PROJECT_TOOL
BROKER_TOOL
FULL_RUN_EVIDENCE
PROVIDER_DIAGNOSTIC
PATCH_PLAN_SUPPORT
MEMORY_LANE
DOCS_MAINTENANCE
BLENDER_AUDIO_PIPELINE
LOCAL_UI_OR_MANUAL
GIT_WRITE_TOOL
SUPPORT_LIBRARY
GENERATED_OR_CANDIDATE
```

## Required fields

Each registry entry must include:

```text
path
tool_id
classification
current_status
broker_eligible
full_run_lane
provider_execution
source_writes
runtime_outputs
git_tracked_outputs
validation_command
guardrails
promotion_notes
```

## Broker eligibility rules

A `BROKER_TOOL` must not:

```text
execute arbitrary shell
run Blender
run FFmpeg
perform Git writes
apply patches
write persistent SQLite unless explicitly allowed
execute real provider calls unless it is a safe diagnostic
write source files
```

## Expected output

Create or update only:

```text
docs/LOCAL_AI_TASKS/project-tool-registry.md
```

Do not create other source or documentation files for this task.

## Acceptance criteria

```text
project-tool-registry.md exists
project-tool-registry.md has entries for Tools/ai, Tools/validation, Tools/workflow, Tools/npu, root audio tools, Scripting/v61b
patch_application_performed = false
source_writes_performed = false except generated reports/evidence
patch_plan target is docs/LOCAL_AI_TASKS/project-tool-registry.md
no ordinary patch targets under docs/LOCAL_VALIDATION_EVIDENCE/**
no ordinary patch targets under output/**
no ordinary patch targets under indexAI/code_chunks/**
```

## Required final summary fields

The run must expose these fields in the shared toolbox final summary:

```text
provider_advisory_state
provider_failure_reasons
degraded_provider_components
patch_application_performed
source_writes_performed
```

## Guardrails

```text
Do not promote Blender, FFmpeg or audio runtime tools to broker tools.
Do not use docs/LOCAL_VALIDATION_EVIDENCE/** as ordinary patch-plan target.
Do not target output/** or indexAI/code_chunks/**.
Do not commit runtime artifacts.
Do not run Blender.
Do not run FFmpeg.
Do not apply patches automatically.
```
