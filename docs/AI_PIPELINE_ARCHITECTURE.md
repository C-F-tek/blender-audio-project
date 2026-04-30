# AI Pipeline Architecture

## Purpose

This document describes the modular AI artifact pipeline architecture in `blender-audio-project`.

It is intended for human maintainers and AI agents. Read it before changing files under:

```text
Tools/ai/run_parallel_artifact_pipeline.py
Tools/ai/pipeline/
Tools/validation/check_ai_pipeline_modules.py
Tools/ai/run_pipeline_dry_run_matrix.py
```

## Current status

Status: `modular schedule complete, pending local dry-run validation`

The original monolithic orchestration logic has been split into focused modules. The public CLI and schema-v6 report shape are intended to remain compatible.

The current entrypoint is intentionally thin:

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

The AI pipeline core is app-agnostic infrastructure, not a closed list of files. Add new reusable functions, dataclasses or focused modules when they make validation, reporting, scheduling, provider integration, guardrails or memory policy clearer.

Good core additions are:

```text
package-neutral
deterministic where practical
small enough to validate directly
free of Ready To Jazz or Blender-scene assumptions
compatible with existing schema-v6 report meanings
```

Avoid broad utility modules. Prefer a focused owner such as report helpers, provider preflight helpers, memory policy helpers, artifact manifest helpers or dry-run fixture builders.

## Data flow

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

## Validation commands

Use these commands after changes to the pipeline:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\validation\check_ai_pipeline_modules.py --repo-root . --output .\output\validation\ai_pipeline_modules.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
```

Then run the repository-level checks:

```powershell
python .\Tools\validation\check_package_structure.py --repo-root .
python .\Tools\validation\check_json_artifacts.py --repo-root .
```

## Expected dry-run outputs

The dry-run matrix writes:

```text
output/ai_pipeline/dry_run_matrix_report.json
output/ai_pipeline/dry_run_matrix/base/ai_pipeline_dry_run_report.json
output/ai_pipeline/dry_run_matrix/no_auto_remediation/ai_pipeline_dry_run_report.json
output/ai_pipeline/dry_run_matrix/no_npu_guardrail/ai_pipeline_dry_run_report.json
output/ai_pipeline/dry_run_matrix/with_validation/ai_pipeline_dry_run_report.json
output/ai_pipeline/dry_run_matrix/with_chunks/ai_pipeline_dry_run_report.json
```

Check these fields first:

```text
passed
summary
schedule
lanes
guardrail_remediation_loop
```

## Modification rules

Allowed low-risk changes:

```text
additive helper functions
focused app-agnostic core utilities
report summary additions
new dry-run cases
new validation checks
internal dataclasses that preserve report compatibility
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
```

## Current next actions

1. Run the local validation/dry-run matrix.
2. Regenerate AI/NPU indexes.
3. Commit regenerated index files only.
4. Review dry-run reports for failed steps, schedule shape and guardrail loop behavior.
5. Only after successful dry-runs, continue with richer lane execution policy or Markdown report output.
