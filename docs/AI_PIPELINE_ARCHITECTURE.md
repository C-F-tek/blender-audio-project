# AI Pipeline Architecture

## Status

Current architecture reference for the modular AI artifact pipeline.

This document is subordinate to the unified launcher, heap/exchange operating model and full-run evidence contract.

Current operating model:

```text
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

## Purpose

Architecture contract for the modular AI artifact pipeline in `IA-Carmine Local AI Orchestration Workbench`.

Read before changing:

```text
Tools/ai/run_parallel_artifact_pipeline.py
Tools/ai/pipeline/
Tools/validation/check_ai_pipeline_modules.py
Tools/ai/run_pipeline_dry_run_matrix.py
```

This is not a command catalog. Current command and owner sources:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Relationship to main runtime architecture

Canonical runtime topology:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

The AI artifact pipeline is one implementation lane inside the wider runtime. It should publish compact state, report references and planned artifacts into the shared runtime heap / blackboard model rather than becoming an isolated orchestration island.

Pipeline reports become useful when joined with heap/exchange lifecycle state, broker execution state, semantic tool registry metadata, deterministic validator results, patchkit or patch bridge reports and telemetry/event stream summaries.

## Current status

Status: active architecture reference, subordinate to unified launcher and full-run evidence contract.

The original monolithic orchestration logic has been split into focused modules. The public CLI and schema-v6 report shape should remain compatible.

Direct entrypoint:

```text
Tools/ai/run_parallel_artifact_pipeline.py
```

It should stay focused on:

```text
parse CLI
resolve repo/output paths
run preflight
build commands and steps
build schedule
execute schedule
run remediation loop
build/write report
return exit code
```

## Full-run integration doctrine

`-Full0To10` is **TUTTO SU TUTTO**. The AI artifact pipeline can contribute dry-run reports, planned artifacts and validation evidence, but it is not sufficient to prove a full run by itself.

Dry-run matrix evidence proves planned-only behavior. It does not prove provider execution, broker tool execution, runtime capability availability, patch application state, heap/exchange lifecycle state, patchkit application state or source-write state.

When pipeline reports influence evidence, recommendations, patch plans or patch specs, handoff must include companion surfaces:

```text
heap/exchange runtime entry
heap/exchange runtime state
heap/exchange runtime exit product
heap/exchange lifecycle report
patchkit apply report when source writes were selected
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when repository visibility or maintainability is in scope
main runtime blackboard / broker / registry / validator / telemetry state when available
```

## Module map

| Module | Responsibility |
|---|---|
| `defaults.py` | Central constants: schema version, default output path, smart-context sizes, NPU worker count, report filenames. |
| `models.py` | Core dataclasses and enums: `PipelineLane`, `PipelineStep`, `PipelineResult`, `PipelineReport`. |
| `runner.py` | Low-level command execution: `run_step`, `run_serial`, `run_parallel`. |
| `compat.py` | Compatibility adapters from reusable models to existing schema-v6 report dictionaries. |
| `artifact_contracts.py` | Expected artifact names, slugging, file metadata, planned output calculation. |
| `cli.py` | CLI parser and public command flags. |
| `preflight.py` | Non-invasive input, environment and workstation checks. |
| `steps.py` | Command construction plus serial/parallel `PipelineStep` builders. |
| `scheduler.py` | Lane-aware execution schedule and policy for serial/paralleled execution. |
| `orchestrator.py` | Concrete execution helpers for serial and parallel step lists. |
| `schema_report.py` | Schema-v6 report builders, report writing and compact summary generation. |
| `guardrail_models.py` | Typed normalization of remediation queue requests and pass results. |
| `remediation.py` | Guardrail action queue loading and auto-safe remediation pass execution. |

## Core extension policy

Good core additions are:

```text
package-neutral
deterministic where practical
small enough to validate directly
free of Ready To Jazz or Blender-scene assumptions
compatible with existing schema-v6 report meanings
visible through launcher manifest/report surfaces when selected
compatible with telemetry/capability handoff when part of full-run evidence
compatible with shared runtime heap / blackboard contract when runtime state is introduced
compatible with heap/exchange lifecycle reporting when product lanes depend on it
compatible with patchkit as reviewed source-write boundary when source edits are produced
within file-size policy or split by responsibility
```

Prefer focused owners such as report helpers, provider preflight helpers, memory policy helpers, artifact manifest helpers, telemetry summary helpers, file-line evidence helpers or dry-run fixture builders.

## Direct pipeline flow

```text
CLI args
  -> preflight
  -> build_step_commands
  -> build_serial_steps / build_parallel_steps
  -> build_schedule
  -> execute_schedule
  -> execute_remediation_loop
  -> build_report
  -> write_report_if_requested
```

Unified full-run context is documented in:

```text
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
```

## Report compatibility

The report schema remains version `6`.

Important compatibility fields:

```text
schema_version
generated_at
repo_root
output_dir
dry_run
passed
preflight
step_count
lanes
wave_entrypoint_review
smart_context
guardrail_remediation_loop
steps
post_run_expected_outputs
```

Additive fields include:

```text
summary
schedule
```

When a schema-v6 pipeline report is used as full-run evidence input, surrounding bundle/telemetry must still expose:

```text
provider_execution_performed
patch_application_performed
source_writes_performed
heap_exchange_runtime_entry when product lanes are selected
heap_exchange_runtime_exit_product when product lanes are selected
heap_exchange_runtime_lifecycle when product lanes are selected
runtime tool execution state when relevant
provider degradation state when relevant
file-line-limit state when maintainability is relevant
blackboard/broker/registry/validator/telemetry state when relevant
```

## File-size policy

Maintained pipeline source and docs follow the active file-size policy:

```text
preferred active runbook <= 400 lines
active Markdown hard threshold <= 500 lines
maintained source/script target <= 400 lines
```

Markdown split layout:

```text
name.md
name.md/part-001.md
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Validation ownership

Focused direct validation is appropriate only when changing or debugging the pipeline itself. Broad local-AI validation should route through the unified launcher.

Validation selector:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Expected dry-run outputs

The dry-run matrix writes local ignored reports such as:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix/<case>/ai_pipeline_dry_run_report.json
```

Check these fields first:

```text
passed
summary
schedule
lanes
guardrail_remediation_loop
```

Do not commit raw `output/**` reports. Use compact evidence only when review needs Git-trackable summaries.

## Modification rules

Allowed low-risk changes:

```text
additive helper functions
focused app-agnostic core utilities
report summary additions
new dry-run cases
new validation checks
internal dataclasses that preserve report compatibility
telemetry/capability references when pipeline outputs join full-run handoff
file-line evidence references when maintainability is in scope
heap/exchange lifecycle references when product lanes join full-run handoff
patchkit references when reviewed source-write products are produced
blackboard/broker/registry contract references when integrating the main runtime architecture
```

Higher-risk changes requiring local dry-run matrix validation:

```text
changing CLI defaults
changing schedule policy
changing remediation loop behavior
changing report schema fields
changing command construction
```

Avoid without explicit approval:

```text
running real NPU/GPU/Blender workloads from validation tools
changing Blender runtime packages
modifying full frame-level JSON data
changing existing schema-v6 field meanings
claiming full-run success from dry-run matrix evidence alone
silently bypassing the broker unico executor once runtime execution is centralized
bypassing heap/exchange lifecycle for product-path claims
bypassing patchkit when a reviewed patchkit bundle can express the source-write change
```

## Current next actions

```text
validate launcher-owned usage through unified runbook when local execution is available
keep dry-run matrix evidence clearly marked planned-only
attach pipeline outputs to telemetry/capability/final-summary context when used for recommendations or patch plans
include heap/exchange lifecycle context when product lanes are selected
keep patchkit reports visible when source-write boundary is selected
keep file-line evidence visible when maintainability is in scope
regenerate indexes only under scoped task
add blackboard, broker, registry, validator-authority and telemetry surfaces incrementally with deterministic reports first
```
