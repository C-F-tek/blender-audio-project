# Project tool registry generation task

## Objective

Create a stable, non-dated project tool registry:

```text
docs/LOCAL_AI_TASKS/project-tool-registry.md
The registry must be derived from current stable documentation and repository code, not from historical evidence bundles.

Primary sources

Use:

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
root-level Python entrypoints such as analyze_wav.py and build_track_summary.py
Hard exclusions for ordinary patch targets

Do not create ordinary patch plans targeting:

docs/LOCAL_VALIDATION_EVIDENCE/**
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_*_cloud_semantic_deterministic_chunks/**
output/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
renders/**
*.db
*.sqlite

Historical evidence may be read only as context, never used as the primary patch target.

Required registry taxonomy

Classify tools with one or more of:

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
Required fields

For each registry entry include:

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
Expected output

Create or update only:

docs/LOCAL_AI_TASKS/project-tool-registry.md
Acceptance criteria

The patch plan should primarily target:

docs/LOCAL_AI_TASKS/project-tool-registry.md

The run must also expose:

provider_advisory_state
provider_failure_reasons
degraded_provider_components

in the shared toolbox final summary.

The run must not propose ordinary patch targets under:

docs/LOCAL_VALIDATION_EVIDENCE/**
output/**
indexAI/code_chunks/**

Patch application must remain false.
Source writes must remain false except generated reports/evidence.
