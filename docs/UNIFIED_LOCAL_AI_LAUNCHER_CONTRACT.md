# Unified Local AI Launcher Contract

## Purpose

Compact contract for `Tools/workflow/run_unified_local_ai_refactor.ps1` and its manifest output.

This file exists so agents do not need to inspect long historical JSON-schema notes before understanding the unified launcher contract.

For launcher manifest semantics, this compact contract is canonical. If this file conflicts with broad historical notes in `docs/JSON_SCHEMAS.md`, prefer this file for the unified launcher and update `JSON_SCHEMAS.md` later as a schema catalog task.

## Producer

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

## Primary runbook

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Manifest path pattern

Current default:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

After the external-controls patch, the root output directory should be operator-selectable through launcher CLI parameters.

## Required root fields

The manifest should include at minimum:

```text
schema_version
kind
generated_at
repo_root
mode
mode_name
full_0_to_10_requested
available_modes
profile
model
run_intensity
python_exe
python_exe_requested
pythonpath
ia_carmine_python_env
stamp
task_file
task_branch
run_dir
provider_execution_requested
primary_provider_requested
workload_quality_report
workload_quality_routing_ok
multistep_provider_workflow_requested
ollama_probe_requested
npu_probe_requested
npu_decode_smoke_requested
memory_in_enabled
memory_out_enabled
quality_gate_passed
reset_apply_requested
patch_application_performed
patch_specs_requested
build_evidence_requested
memory_db
save_inputs_to_memory_db
context_files
report_files
phase_status
phase_reports
warnings
errors
```

## Phase status contract

`phase_status` must be a map keyed by phase name.

Values may be:

```text
true
false
structured list/object with stdout/stderr/status
```

If a phase is selected but skipped intentionally, the skip must be visible either in `phase_status`, `warnings`, or a phase-specific report.

Silent phase loss is not allowed for `-Full0To10`.

## Phase report contract

`phase_reports` should map stable phase names to produced report paths.

Expected keys when phases are selected:

```text
markdown_inventory
docs_links
json_contract
script_inventory
script_inventory_csv
task_scoped_contract
official_packet
official_proposals
ollama_packet
ollama_proposals
workload_quality
legacy_full_toolbox_integrated
patch_specs_manifest
patch_specs_validation
```

Exact keys may grow, but missing selected-phase reports should be explicit.

## Visibility contract

A local-AI run is valid only if a GitHub-only or next local agent can inspect it in this order:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
compact Markdown or CSV summaries
detailed evidence only when needed
```

The manifest is the first machine-readable entrypoint. Long evidence bundles are never the first operational interface.

## Full0To10 contract

When `full_0_to_10_requested=true`, the manifest should show all default capabilities as either enabled/completed or explicitly disabled by user flags.

Full0To10 always means full coverage: TUTTO SU TUTTO. Intensity profiles may tune budgets and capacity, but they must not silently remove core lanes.

Expected defaults unless disabled:

```text
Markdown inventory and docs link validation requested
JSON/report contract validation requested
Python/script inventory requested
semantic chunks requested
context pack requested
agent state/memory input-output requested
repository consistency and validation evidence requested
runtime tool broker telemetry requested
runtime tool capability manifest requested
Ollama advisory requested
primary provider routing requested
provider diagnostics requested
workload quality routing requested
multistep provider workflow requested
Ollama probe requested
NPU probe requested
NPU decode smoke requested
legacy full-toolbox integrated lane requested
patch specs requested
evidence requested
shared AI-to-AI bundle summary requested
patch_application_performed=false
```

Allowed explicit disablers:

```text
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-NoMemoryWrite
-NoEvidence
-NoPatchSpecs
```

If a core lane is unavailable, the manifest must record the unavailable-tool/provider failure in `phase_status`, `warnings`, `errors` or a phase report. Missing evidence without an explicit disabler or failure record is a failed full run.

## Run intensity contract

`run_intensity` changes capacity, not scope.

```text
quick    = full coverage with reduced budget
balanced = full coverage with default budget
deep     = full coverage with expanded budget
custom   = full coverage with operator-supplied budget
```

A quick Full0To10 run is not a smoke test. Smoke remains a separate mode and must not be used as evidence that the full-run contract passed.

## Quality gate contract

When primary provider routing is requested:

```text
workload_quality_report must point to the quality report path
workload_quality_routing_ok must be true or the run must fail clearly
quality_gate_passed must not hide missing workload quality routing
```

In `-DryRun`, missing quality routing may be marked as planned, not executed.

## Memory contract

SQLite memory is local/private runtime state.

Expected manifest fields:

```text
memory_in_enabled
memory_out_enabled
memory_db
save_inputs_to_memory_db
```

Policy:

```text
Do not commit SQLite DB files.
Do not commit output/** runtime memory outputs.
Commit only compact evidence/summary when explicitly needed.
```

## External-controls extension contract

The next launcher patch should add manifest fields for selected external controls:

```text
output_root
validation_output_dir
ai_pipeline_output_dir
ai_packets_output_dir
patch_spec_output_dir
local_runs_output_dir
evidence_output_dir
external_context_files
external_report_files
external_artifact_files
official_basename
official_proposal_basename
ollama_basename
ollama_proposal_basename
multistep_basename
multistep_proposal_basename
context_pack_basename
context_pack_evidence_basename
```

Until that patch lands, these fields are planned, not guaranteed.

## Length policy

The manifest should stay compact enough to inspect quickly.

If a phase produces long evidence, the manifest should reference:

```text
summary path
manifest path
compact evidence path
raw ignored output path
```

Do not embed giant raw provider output directly in the launcher manifest.

## Guardrails

The launcher manifest must preserve:

```text
patch_application_performed=false by default
no commit/push/merge action by launcher
no Blender runtime by launcher
no FFmpeg runtime by launcher
provider execution only when explicit
reset deletion only with exact confirmation
```

## Validation

Recommended local checks after launcher edits:

```powershell
$null = [scriptblock]::Create((Get-Content .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Raw))
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Full0To10 -DryRun -SkipGitSync -NoBranch -AllowDirty
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links_unified_launcher_contract.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract_unified_launcher_contract.json
git diff --check
```
