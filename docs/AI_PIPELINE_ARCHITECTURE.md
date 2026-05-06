# AI Pipeline Architecture

## Purpose

This document describes the modular AI artifact pipeline architecture in `IA-Carmine Local AI Orchestration Workbench`.

It is intended for human maintainers and AI agents. Read it before changing files under:

```text
Tools/ai/run_parallel_artifact_pipeline.py
Tools/ai/pipeline/
Tools/validation/check_ai_pipeline_modules.py
Tools/ai/run_pipeline_dry_run_matrix.py
```

This file is an architecture contract, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Large validator catalogs such as `Tools/validation/README.md` are references only and must not become primary operational entrypoints if too large or truncated.

## Relationship to the main runtime architecture

The canonical runtime topology is defined in:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

The AI artifact pipeline is one implementation lane inside that wider runtime. It should publish compact state, report references and planned artifacts into the shared runtime heap / blackboard model rather than becoming an isolated orchestration island.

Current target topology:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Pipeline reports are not final authority by themselves. They become useful when joined with broker execution state, semantic tool registry metadata, deterministic validator results and telemetry/event stream summaries.

## Current status

Status: `modular schedule complete, subordinate to unified launcher and full-run evidence contract`

The original monolithic orchestration logic has been split into focused modules. The public CLI and schema-v6 report shape are intended to remain compatible.

The local AI artifact pipeline is now an implementation lane inside the wider unified local-AI flow. It must not be treated as a replacement for the full `TUTTO SU TUTTO` launcher path.

The current direct entrypoint remains intentionally thin:

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

Dry-run matrix evidence proves planned-only behavior. It does not prove provider execution, broker tool execution, runtime capability availability, patch application state or source-write state.

When pipeline reports influence evidence, recommendations, patch plans or patch specs, the handoff must include companion telemetry/capability surfaces:

```text
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
CSV/index/discovery/file-line evidence when repository visibility or maintainability is in scope
main runtime blackboard / broker / registry / validator / telemetry state when available
```

Telemetry does not replace pipeline reports. It explains whether the lanes that produced or consumed those reports executed, failed, were blocked, degraded, disabled or planned-only.

Limitations are backlog to overcome, not reasons to skip available tools.

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

## Core Extension Policy

The AI pipeline core is app-agnostic infrastructure, not a closed list of files. Add new reusable functions, dataclasses or focused modules when they make validation, reporting, scheduling, provider integration, guardrails, telemetry or memory policy clearer.

Good core additions are:

```text
package-neutral
deterministic where practical
small enough to validate directly
free of Ready To Jazz or Blender-scene assumptions
compatible with existing schema-v6 report meanings
visible through launcher manifest/report surfaces when selected
compatible with telemetry/capability handoff when part of full-run evidence
compatible with the shared runtime heap / blackboard contract when runtime state is introduced
under 400 lines per maintained source file or split by responsibility
```

Avoid broad utility modules. Prefer a focused owner such as report helpers, provider preflight helpers, memory policy helpers, artifact manifest helpers, telemetry summary helpers, file-line evidence helpers or dry-run fixture builders.

## Data flow

Direct pipeline flow:

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

Unified full-run flow around it:

```text
unified launcher manifest
  -> selected pipeline/dry-run lanes
  -> pipeline reports
  -> validation reports
  -> compact evidence when selected
  -> recommendations / patch plans when selected
  -> runtime telemetry and capability context
  -> discovery/index/CSV/file-line context when relevant
  -> shared AI-to-AI bundle/final summary
  -> main runtime blackboard / broker / registry / CPU-validator state when available
```

## Report compatibility

The report schema remains version `6`.

Important compatibility fields preserved:

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

Additional report fields added during modularization:

```text
summary
schedule
```

These fields are additive and should not break existing consumers.

When a schema-v6 pipeline report is used as full-run evidence input, surrounding bundle/telemetry must still expose:

```text
provider_execution_performed
patch_application_performed
source_writes_performed
runtime tool execution state when relevant
provider degradation state when relevant
file-line-limit state when maintainability is relevant
blackboard/broker/registry/validator/telemetry state when relevant
```

## 400-line policy

Maintained pipeline source and docs follow the hard 400-line policy.

```text
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

## Validation ownership

Use the unified launcher runbook for current broad commands.

Focused direct validation is appropriate only when changing or debugging the pipeline itself. Broad local-AI validation should route through the unified launcher.

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
creating or expanding maintained pipeline files beyond 400 lines without split/refactor plan
silently bypassing the broker unico executor once runtime execution is centralized
```

## Current next actions

1. Validate launcher-owned usage of the pipeline through the unified runbook when local execution is available.
2. Keep dry-run matrix evidence clearly marked as planned-only.
3. Keep pipeline outputs attached to telemetry/capability/final-summary context when they influence recommendations or patch plans.
4. Keep file-line evidence visible when pipeline/docs maintainability is in scope.
5. Regenerate AI/NPU indexes only when a scoped task requires it.
6. Only after successful dry-runs, continue with richer lane execution policy or Markdown report output.
7. When implementing the main runtime architecture, add blackboard, broker, registry, validator-authority and telemetry surfaces incrementally with deterministic reports first.
