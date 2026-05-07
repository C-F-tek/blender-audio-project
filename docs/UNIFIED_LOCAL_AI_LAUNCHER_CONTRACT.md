# Unified Local AI Launcher Contract

## Purpose

Compact contract for `Tools/workflow/run_unified_local_ai_refactor.ps1` and its manifest output.

This file is canonical for the unified launcher. If broad historical notes conflict with this file, prefer this file for launcher behavior and update historical/schema catalogs later.

## Producer

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

## Primary runbook

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Main runtime architecture

The launcher must remain compatible with:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Target topology:

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

## Unified product contract

The full product is owned by the unified launcher, not by a manual chain of standalone scripts.

Canonical product loop:

```text
Task Markdown input
-> launcher-owned Stamp and environment
-> Full0To10 context/chunk/agent-state preparation
-> GPU1 primary advisory / planner
-> GPU0 OpenVINO companion peer worker
-> NPU non-blocking micro/tool-support lane
-> runtime broker tool execution
-> runtime heap / blackboard evidence
-> deterministic repository validators
-> raw reports under output/**
-> compact AI-to-AI bundle, telemetry and evidence
-> deterministic patch suggestion extraction
-> safe patch application on CARMINEai/* review branch
-> product-vs-supplemental separation validation
-> automatic source/doc path discovery from apply report
-> draft GitHub PR for human review
```

The internal tool family remains reuse-first implementation detail:

```text
Tools/ai/build_task_patch_suggestion_report.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/ai/prepare_review_pr.py
Tools/validation/check_patch_suggestion_product_separation.py
```

Direct invocation of these scripts is allowed for diagnostics/replay only. Production operation should be driven by the launcher.

## Stamp and environment ownership

`Stamp` is a launcher-owned run variable. The launcher either receives it from the operator or creates/resolves it once and propagates it to subtools.

Subtools must not invent a separate stamp convention for the same run.

Provider-capable Python is also launcher-owned and must be locked for the run:

```text
IA_CARMINE_PYTHON = resolved provider-capable repo Python
PYTHONPATH = repo root
```

Expected provider-visible environment on the IA-Carmine workstation:

```text
CPU, GPU.0, GPU.1, NPU
```

If the selected Python cannot import `numpy`, `openvino` or `openvino-genai`, classify the failure as provider Python environment failure, not as GPU0/NPU failure.

## Manifest path pattern

Current default:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

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
build_task_patch_suggestion_report_requested
review_pr_apply_deterministic_suggestions_requested
prepare_review_pr_requested
review_pr_branch
review_pr_created
review_pr_url
memory_db
save_inputs_to_memory_db
context_files
report_files
phase_status
phase_reports
warnings
errors
```

Do not add fake success markers. Add fields only when code reports real, planned, unavailable, degraded or skipped state.

## Phase report contract

Expected keys when phases are selected include:

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
patch_suggestion_report
patch_suggestion_bundle_apply
patch_suggestion_product_separation
review_pr_prepare
```

Missing selected-phase reports must be explicit in `phase_status`, `warnings`, `errors` or a phase-specific report.

## Full0To10 contract

When `full_0_to_10_requested=true`, the manifest should show all default capabilities as enabled/completed or explicitly disabled/unavailable/degraded.

Full0To10 means full coverage: **TUTTO SU TUTTO**. Intensity profiles tune budget and capacity, not scope.

Expected defaults unless disabled:

```text
Markdown inventory and docs link validation
JSON/report contract validation
Python/script inventory
Python line-count CSV/Markdown surface
file-line-limit surface when maintainability is in scope
semantic chunks and selected chunk evidence when available
context pack
agent state/memory input-output
repository consistency and validation evidence
auto-discovery/index drift visibility when relevant
runtime tool broker telemetry
runtime/hardware capability manifest
Ollama advisory
primary provider routing
GPU1/Ollama primary advisory planner
GPU0/OpenVINO companion peer worker and tool-request producer
NPU/OpenVINO non-blocking micro/tool-support lane
AI peer-exchange contract
provider diagnostics
workload quality routing
multistep provider workflow
Ollama probe
NPU probe
NPU decode smoke
legacy full-toolbox integrated lane
patch specs
evidence
shared AI-to-AI bundle summary
```

Patch application and PR creation are not default side effects of `-Full0To10` alone. They become valid launcher-owned product actions only when explicit product flags are supplied:

```text
-BuildTaskPatchSuggestionReport
-ReviewPrApplyDeterministicSuggestions
-PrepareReviewPr
-ReviewPrPush
-ReviewPrCreate
```

## Product PR side-effect contract

Default launcher posture remains report/proposal-only.

The launcher may apply patches, commit, push and create a draft PR only in the explicit review-PR product phase:

```text
ReviewPrApplyDeterministicSuggestions -> controlled deterministic source/doc writes on CARMINEai/*
PrepareReviewPr -> staged product paths, commit, optional push, optional draft PR
```

Required guardrails:

```text
branch must be CARMINEai/* for product review PRs
master/main apply is refused
output/** is never staged
indexAI/code_chunks/** and indexAI/project_code_chunks/** are never staged
*.db, *.sqlite, *.sqlite3 are never staged
renders/** is never staged
PR is draft by default
merge to master remains human-only
force-push/rewrite history/delete are not allowed
```

## Allowed explicit disablers

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

If a core lane is unavailable, the manifest must record unavailable-tool/provider failure in `phase_status`, `warnings`, `errors` or a phase report. Silent lane loss is a failed full run.

## LightFull0To10 contract

`-LightFull0To10` is evidence-only and not a replacement for provider-capable Full0To10.

Expected behavior:

```text
provider_execution_performed=false
patch_application_performed=false
blender_runtime_execution_performed=false
ffmpeg_execution_performed=false
```

It must not be cited as proof that provider execution, patch apply or draft-PR product execution occurred.

## Run intensity contract

```text
quick    = full coverage with reduced budget
balanced = full coverage with default budget
deep     = full coverage with expanded budget
custom   = full coverage with operator-supplied budget
```

A quick Full0To10 run is not a smoke test.

## Memory and raw output policy

SQLite memory is local/private runtime state.

```text
Do not commit SQLite DB files.
Do not commit output/** runtime outputs directly.
Commit only compact evidence/summary when explicitly needed.
```

Raw `output/**` reports are official process inputs, not Git source artifacts. They may feed bundle/evidence/telemetry/PR-preparation phases.

## Guardrails

The launcher manifest must preserve:

```text
no Blender runtime unless explicitly scoped outside this AI/tooling flow
no FFmpeg runtime unless explicitly scoped outside this AI/tooling flow
provider execution only when explicit through Full0To10/provider flags
reset deletion only with exact confirmation
index repair/regeneration only when explicit and report-bound
providers as advisory/helper/microtask lanes, not direct mutation authorities
broker unico executor as guardrail-enforcing execution gateway
deterministic validators as CPU authority for pass/fail claims
telemetry/event stream for executed, skipped and degraded phases
```

## Validation after launcher/product edits

Include at least:

```text
PowerShell parser check for Tools/workflow/run_unified_local_ai_refactor.ps1 when touched
python -m py_compile for touched Python scripts
launcher Full0To10 dry-run or focused product dry-run when local execution is available
docs link validation
validation report contract check
file-line-limit report when maintainability is in scope
git diff --check
```
