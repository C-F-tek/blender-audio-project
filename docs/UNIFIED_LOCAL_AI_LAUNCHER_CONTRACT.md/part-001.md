<!-- IA-CARMINE-MD-SPLIT: part -->
# UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT — parte 001 di 002

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Unified Local AI Launcher Contract

## Purpose

Compact contract for `Tools/workflow/run_unified_local_ai_refactor.ps1` and its manifest output.

The operator-facing real product entrypoint is `Tools/workflow/run_unified_real_product_pr.ps1`; it performs mandatory preflight and delegates the dynamic center to this launcher. This contract describes the launcher/manifest layer, not the outer wrapper policy.

For current real product run guidance, use:

```text
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
```

For launcher manifest semantics, this compact contract is canonical. If this file conflicts with broad historical notes in `docs/JSON_SCHEMAS.md`, prefer this file for the unified launcher and update `JSON_SCHEMAS.md` later as a schema catalog task.

## Producer

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

## Product wrapper

```text
Tools/workflow/run_unified_real_product_pr.ps1
```

The wrapper owns product entry, mandatory preflight, `-ProcessGateTask`, review PR flags and final product validation. The launcher owns the heap/exchange execution surface and produced manifest.

## Primary runbooks

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
```

## Current operational bridge

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
```

## Main runtime architecture

The launcher must remain compatible with the main runtime architecture contract:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Current runtime topology:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / Ollama planner
├─ GPU0 OpenVINO observable support workload
├─ NPU micro peer diagnostic/report lane
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
├─ generated patch-spec product lane
├─ runtime evidence correlation
└─ telemetry/event stream
```

Current launcher code does not need to implement every future runtime component at once. When a component is not yet implemented, the manifest/evidence should either omit it clearly or record it as planned/unavailable, not silently imply execution.

Current compact validator note:

```text
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
```

## Manifest path pattern

Current default:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

The root output directory should remain operator-selectable through launcher CLI parameters where supported.

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
runtime_evidence_correlation_requested
runtime_evidence_correlation_report
memory_db
save_inputs_to_memory_db
context_files
report_files
phase_status
phase_reports
warnings
errors
```

Product-wrapper reports may additionally include review-PR/product fields such as:

```text
review_pr_prepare_report
review_pr_final_product_contract_report
review_pr_branch
review_pr_base_branch
review_pr_push_requested
review_pr_create_requested
review_pr_draft_requested
generated_patch_specs_apply_report
generated_patch_specs_concrete_operation_count
generated_patch_specs_changed_count
```

Future runtime-architecture fields should be additive, for example:

```text
blackboard_state_report
broker_execution_report
semantic_tools_registry_snapshot
runtime_event_stream_summary
deterministic_validator_authority_report
gpu1_primary_advisory_status
gpu0_coworker_openvino_status
npu_microtask_responder_status
```

Do not add these fields as fake success markers. Add them only when the code can report real state, planned state, unavailable state or explicit skip state.

## Phase status contract

`phase_status` must be a map keyed by phase name.

Values may be:

```text
true
false
structured list/object with stdout/stderr/status
```

If a phase is selected but skipped intentionally, the skip must be visible either in `phase_status`, `warnings`, or a phase-specific report.

Silent phase loss is not allowed for real unified runs.

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
ai_peer_exchange
ai_peer_exchange_contract
patch_specs_manifest
patch_specs_validation
generated_patch_specs_apply
heap_exchange_runtime_entry
heap_peer_runtime_manifest
heap_exchange_closure_audit
heap_exchange_runtime_exit_product
final_chain_contract
runtime_evidence_correlation
repository_change_proposals
review_pr_prepare
review_pr_final_product_contract
```

Legacy full-toolbox integrated evidence is explicit and diagnostic; it is not auto-enabled by `-Full0To10` compatibility spelling.

Expected future keys for the main runtime architecture:

```text
blackboard_state
broker_execution
semantic_tools_registry
deterministic_validator_authority
runtime_event_stream
gpu1_primary_advisory
gpu0_coworker_openvino
npu_microtask_responder
```

Exact keys may grow, but missing selected-phase reports should be explicit.
