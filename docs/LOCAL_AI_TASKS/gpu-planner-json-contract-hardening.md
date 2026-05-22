# GPU Planner JSON Contract Hardening

## Purpose

This note documents the first hardening layer after PR #111.

The immediate goal is to reduce ambiguous GPU planner failures by classifying model output more precisely before it reaches recommendation merge/filter logic.

## Added helper

```text
ia_carmine/_shared/gpu_planner_json_contract.py
```

The helper is report-only and does not run providers.

It validates:

```text
JSON parseability
expected top-level recommendation schema
context echo outputs
recommendation object shape
risk/status enums
target_files, validation_commands and stop_conditions list types
```

## Added smoke

```text
Tools/validation/provider_mesh/gpu_planner_json_contract_smoke/cli.py
```

Smoke cases:

```text
valid_recommendation -> accepted
context_echo -> classified as context_echo_detected
malformed_json -> classified as json_parse_failure
```

## Why this matters

The project-complete AI-to-AI run showed:

```text
GPU/Ollama provider execution completed
round_count=24
json_parse_error_count=16
repair_attempt_count=18
recommendation_count=0
evidence_ready_for_manual_patch_count=12
empty_recommendations_reason=repair_attempt_failed
```

The included raw preview also showed the model returning a `files` payload with `content_preview` entries instead of the expected recommendation object. That is not only invalid JSON recovery; it is a task-shape failure.

## New classifications

```text
json_parse_failure
context_echo_detected
model_output_schema_mismatch
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

## Intended integration path

This PR deliberately adds a reusable helper and smoke first.

Next integration step:

```text
replace local duplicated GPU parse/classification code with gpu_planner_json_contract.validate_model_response_contract
```

Target files:

```text
ia_carmine/providers/provider_mesh/gpu_deep_planning_review/cli.py
ia_carmine/providers/provider_mesh/gpu_deep_planning_supervised/cli.py
```

## Guardrails

```text
no provider/model setting changes
no automatic patch application
no source writes through patch runner
no Blender runtime execution
no raw output/** commit
manual review required
```
