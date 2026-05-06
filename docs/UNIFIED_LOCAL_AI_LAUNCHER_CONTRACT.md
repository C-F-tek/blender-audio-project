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

## Current operational bridge

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

Current compact validator note:

```text
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
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
ai_peer_exchange_required
ai_peer_exchange_contract_passed
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
python_line_count_csv
file_line_limit_report
semantic_chunk_manifest
selected_chunks_evidence
repository_consistency_map
repository_consistency_smoke
discovery_or_index_repair_report
task_scoped_contract
official_packet
official_proposals
ollama_packet
ollama_proposals
workload_quality
legacy_full_toolbox_integrated
ai_peer_exchange
ai_peer_exchange_contract
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
compact Markdown, CSV/count or file-line-limit summaries
detailed evidence only when needed
```

The manifest is the first machine-readable entrypoint. Long evidence bundles are never the first operational interface.

## Full0To10 contract

When `full_0_to_10_requested=true`, the manifest should show all default capabilities as either enabled/completed or explicitly disabled by user flags.

Full0To10 always means full coverage: TUTTO SU TUTTO. Intensity profiles may tune budgets and capacity, but they must not silently remove core lanes.

Limitations are backlog to overcome, not reasons to skip available tools. A lane/tool is unavailable only when current code, telemetry, capability manifest, provider diagnostic or validator evidence says so.

Expected defaults unless disabled:

```text
Markdown inventory and docs link validation requested
JSON/report contract validation requested
Python/script inventory requested
Python line-count CSV/Markdown surface requested when inventory lanes run
file-line-limit JSON/Markdown surface requested when maintainability is in scope
function/class/method CSV surface requested when script inventory supports it
semantic chunks requested
selected chunk evidence requested when chunk selection evidence is available
context pack requested
agent state/memory input-output requested
repository consistency and validation evidence requested
auto-discovery/index drift visibility requested when scanner/index drift is suspected
index repair must be plan/report-first unless explicitly requested
runtime tool broker telemetry requested
runtime/hardware capability manifest requested
Ollama advisory requested
primary provider routing requested
GPU1/Ollama primary advisory planner requested
GPU0/OpenVINO companion peer worker requested
AI peer-exchange contract requested
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

## LightFull0To10 contract

Current code also exposes an evidence-only profile through:

```text
-LightFull0To10
Tools/workflow/run_unified_light_full0to10_profile.ps1
Tools/workflow/run_full0to10_light_evidence_only.ps1
```

This is not a replacement for full provider-capable `Full0To10`. It is a lightweight evidence/profile lane that produces `full0to10_light_evidence_only_run.json/md` plus a promotion JSON.

Observed behavior from code:

```text
provider_execution_performed=false
patch_application_performed=false
blender_runtime_execution_performed=false
ffmpeg_execution_performed=false
```

LightFull0To10 may run optional proof/quality steps such as startup guard, track input contract, repo-quality packet, Markdown line-limit check, accelerator/provider governance reports, provider invocation/bridge reports, memory visibility assertion, provider feedback loop and final product quality package. Missing optional step scripts are represented as skipped/failed step records rather than silent full-run success.

`LightFull0To10` is useful for GitHub-reviewable evidence and promotion planning. It must not be cited as proof that provider execution, patch apply, Blender runtime or FFmpeg runtime occurred.

## Run intensity contract

`run_intensity` changes capacity, not scope.

```text
quick    = full coverage with reduced budget
balanced = full coverage with default budget
deep     = full coverage with expanded budget
custom   = full coverage with operator-supplied budget
```

A quick Full0To10 run is not a smoke test. Smoke remains a separate mode and must not be used as evidence that the full-run contract passed.

## Discovery, index repair, CSV/count and file-line contract

Discovery, count and line-limit surfaces are evidence lanes, not source authority.

Expected report/summary surfaces when relevant:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
file-line-limit JSON/MD
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD when available
repository consistency map/smoke JSON/MD
auto-discovery report when scanner visibility drift is suspected
index repair plan/report when generated indexes are stale or missing
```

Policy:

```text
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Do not hand-edit generated chunk/index artifacts as source.
Index repair is plan/report-first unless the user explicitly requests regeneration or apply.
CSV/count/file-line-limit surfaces are sizing and discovery evidence; they do not override source code or canonical docs.
File-line-limit reports do not rewrite, split, delete or apply patches.
```

## 400-line policy

Maintained docs and source files follow a hard 400-line policy:

```text
Markdown >400 lines -> compact index + <file>.md/part-001.md layout.
Code/script >400 lines -> compact entrypoint + responsibility-based module/package split.
Existing oversized files -> technical debt to refactor progressively, not blind split targets.
```

Validator:

```text
Tools/validation/check_file_line_limits.py
```

Current behavior of the general validator:

```text
kind=file_line_limit_report
provider_execution_performed=false
patch_application_performed=false
source_writes_performed=false
persistent_memory_write_performed=false
includes .md, .py, .ps1, .psm1, .psd1, .sh, .bat, .cmd, .js, .ts, .tsx, .jsx
excludes .git, venv/.venv, __pycache__, node_modules, output, renders, indexAI/code_chunks, indexAI/project_code_chunks
```


## Provider-capable Python preflight

Provider/OpenVINO/NPU/GPU0 validation requires a Python interpreter that can import the provider runtime packages.

The normal repository `.venv` is valid for generic repository validation only if it contains the provider packages required by the selected lane.

Required for OpenVINO GPU.0/NPU provider validation:

```text
numpy
openvino
openvino-genai Required operator preflight before interpreting GPU.0/NPU provider failures:

$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"

& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"

Expected IA-Carmine workstation visibility when provider runtime is correctly selected:

['CPU', 'GPU.0', 'GPU.1', 'NPU']

If numpy, openvino or openvino-genai is missing, classify the failure as provider_python_environment_missing_dependency, not as GPU.0/NPU provider failure.

If GPU.0 is not visible after imports succeed, classify the failure as OpenVINO device visibility/runtime configuration, not as Python selection failure.

GPU.1 may be visible through OpenVINO, but it remains reserved for CUDA/Ollama and must not receive OpenVINO workload.
rn## Quality gate contract

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
index repair/regeneration only when explicit and report-bound
```

## Validation

Recommended local checks after launcher edits are owned by the unified launcher runbook and focused validator docs. Include at least:

```text
PowerShell syntax check for Tools/workflow/run_unified_local_ai_refactor.ps1
launcher Full0To10 dry-run when local execution is available
LightFull0To10 evidence-only run when validating lightweight evidence behavior
docs link validation
validation report contract check
file-line-limit report when maintainability is in scope
git diff --check
```
