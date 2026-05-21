# IA Universe model-to-code map

## Status

Current semantic bridge between the IA-Carmine core models and the repository code/tool surface.

This document explains how the models that define **Universo IA** become real packages, dispatcher commands, artifacts and validators.

## Universo IA formula

```text
HEAP_EXCHANGE_USEFUL_MODEL
+ STANDALONE_HEAP_SURFACE_MODEL
+ PROVIDER_LANES_UNIFIED_MIND_MODEL
+ REAL_PRODUCT_RUN_MODEL
+ COMPACT_EVIDENCE_MODEL
+ PATCH_CODE_PRODUCT_BOUNDARY_MODEL
= Universo IA
```

The complete application is the coexistence of these models. None of them is sufficient alone.

## Dispatcher rule

The concrete code surface starts from dispatchers:

```powershell
python -m Tools.ai <tool> [args...]
python -m Tools.validation <tool> [args...]
python -m Tools.workflow <tool> [args...]
python -m Tools.npu <tool> [args...]
python -m Tools.docs <tool> [args...]
python -m Tools.git <tool> [args...]
python -m Tools.repo_patch_runner <tool> [args...]
```

Source of public command names:

```text
Tools/ai/dispatch.py
Tools/validation/dispatch.py
Tools/workflow/dispatch.py
Tools/npu/dispatch.py
Tools/docs/dispatch.py
Tools/git/dispatch.py
Tools/repo_patch_runner/dispatch.py
```

Do not infer tool availability from random script filenames when a dispatcher exists.

---

# 1. Heap/exchange useful model

## Concept

```text
controlled input -> shared heap/exchange -> cooperating lanes -> evidence -> deterministic exit product
```

## Current model doc

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
```

## Code families

```text
Tools/ai/heap_exchange/
Tools/ai/heap_runtime/
Tools/ai/heap_gate/
Tools/ai/provider_runtime_blackboard/
Tools/ai/runtime_tool/
Tools/validation/heap_exchange/
Tools/validation/heap_runtime/
Tools/validation/runtime_tool/
```

## Main tool commands

Only `python -m Tools.ai run ...` is the product entry command for this model.
The other commands in this list are auxiliary product packaging, review,
inspection or apply-boundary tools; they are not alternate product run flows.

```powershell
python -m Tools.ai heap_exchange_runtime_entry ...
python -m Tools.ai heap_exchange_runtime_exit ...
python -m Tools.ai heap_exchange_peer_runtime_manifest ...
python -m Tools.ai heap_exchange_task_ingress_contract ...
python -m Tools.ai heap_exchange_closure_audit ...
python -m Tools.ai run_heap_runtime_completeness_gate ...
python -m Tools.ai provider_runtime_blackboard ...
python -m Tools.ai provider_runtime_broker_bridge ...
python -m Tools.ai provider_runtime_live_signals ...
python -m Tools.ai provider_runtime_validation_bridge ...
python -m Tools.ai build_provider_runtime_heap_from_peer_reports ...
python -m Tools.ai runtime_tool_broker ...
python -m Tools.ai agent_runtime_tool_broker ...
python -m Tools.ai runtime_file_refs ...
python -m Tools.ai agent_runtime_debug_lab ...
```

## Validation commands

```powershell
python -m Tools.validation check_heap_exchange_runtime_lifecycle ...
python -m Tools.validation run_heap_exchange_runtime_lifecycle_smoke ...
python -m Tools.validation run_heap_exchange_closure_audit_smoke ...
python -m Tools.validation run_heap_peer_runtime_manifest_smoke ...
python -m Tools.validation run_heap_runtime_completeness_gate_smoke ...
python -m Tools.validation run_provider_tool_loop_smoke ...
python -m Tools.validation run_provider_tool_evidence_chain_smoke ...
python -m Tools.validation run_runtime_file_refs_smoke ...
python -m Tools.validation run_agent_runtime_debug_lab_smoke ...
```

## Artifacts/evidence

Expected artifact families:

```text
heap runtime entry report
heap runtime state/event report
peer runtime manifest
broker/tool reports
runtime blackboard reports
provider runtime bridge reports
runtime file reference manifest
runtime debug lab report
heap exchange exit product
lifecycle validator report
blocked/success classification
```

## Semantic rule

The heap is the shared state. The exchange is the observable event layer. A run without visible events and artifacts is not a useful heap/exchange run.

---

# 2. Standalone heap surface model

## Concept

```text
strict request -> preload surfaces -> heap facts -> exchange events -> broker/provider/validator evidence -> composer package
```

## Current model doc

```text
docs/STANDALONE_HEAP_SURFACE_MODEL.md
```

## Code families

```text
Tools/ai/heap_context_memory_reload/
Tools/ai/agent_context/
Tools/ai/agent_memory/
Tools/ai/runtime_tool/
Tools/ai/heap_final_proposals/
Tools/ai/external_heap/
Tools/validation/agent_context/
Tools/validation/agent_memory/
Tools/validation/heap_runtime/
```

## Main tool commands

```powershell
python -m Tools.ai heap_context_memory_reload ...
python -m Tools.ai reconcile_heap_report_with_startup_reload ...
python -m Tools.ai build_agent_agnostic_tool_inventory ...
python -m Tools.ai build_agent_memory_inventory ...
python -m Tools.ai ai_context_pack ...
python -m Tools.ai build_agent_transient_request_context ...
python -m Tools.ai semantic_evidence_chunks ...
python -m Tools.ai select_semantic_code_chunks ...
python -m Tools.ai agent_runtime_sqlite_memory ...
python -m Tools.ai runtime_sqlite_memory ...
python -m Tools.ai build_external_heap_revision_context ...
python -m Tools.ai build_external_heap_block_pointer_manifest ...
python -m Tools.ai external_heap_postrun_package ...
python -m Tools.ai heap_final_proposals ...
python -m Tools.ai normalize_heap_final_causality ...
python -m Tools.ai assemble_heap_final_readable_product ...
```

## Validation commands

```powershell
python -m Tools.validation check_ai_context_pack_contract ...
python -m Tools.validation check_selected_semantic_chunks ...
python -m Tools.validation run_agent_memory_routing_policy_smoke ...
python -m Tools.validation run_runtime_sqlite_persistent_write_smoke ...
python -m Tools.validation run_heap_startup_context_ingestion_smoke ...
python -m Tools.validation run_heap_final_readable_product_smoke ...
python -m Tools.validation test_composer_decision ...
python -m Tools.validation test_proposal_gate ...
```

## Artifacts/evidence

Expected artifact families:

```text
tool inventory
memory inventory
SQLite memory report
semantic chunks manifest
AI context pack
transient request context
heap task file
external heap revision context
external heap pointer manifest
postrun package
final proposal/composer package
```

## Semantic rule

The heap must not depend on hidden model memory. Preload, memory, chunks, namespaces and tool catalog must become explicit heap facts.

---

# 3. Provider lanes unified mind model

## Concept

```text
one operational mind -> specialized provider departments -> shared heap evidence -> deterministic product decision
```

## Current model doc

```text
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
```

## Provider departments

```text
Ollama / main provider = central planner and synthesis lane
GPU0 / OpenVINO = coworker/reviewer lane
NPU / OpenVINO = micro-task/tool/device provider
CPU validators = deterministic authority
```

## Code families

```text
Tools/ai/provider_mesh/
Tools/ai/provider_runtime_blackboard/
Tools/ai/contractor_universe/
Tools/ai/heap_provider/
Tools/npu/provider_mesh/
Tools/npu/dual_ai_pipeline/
Tools/validation/provider_mesh/
Tools/validation/heap_provider/
```

## Main tool commands

```powershell
python -m Tools.ai ollama_tool_gateway ...
python -m Tools.ai provider_mesh_runtime ...
python -m Tools.ai run_local_provider_probe ...
python -m Tools.ai gpu_deep_planning_supervised ...
python -m Tools.ai gpu_deep_planning_review ...
python -m Tools.ai gpu_npu_parallel_orchestrator ...
python -m Tools.ai build_openvino_gpu0_workload_report ...
python -m Tools.ai build_gpu0_companion_task_lane ...
python -m Tools.ai run_gpu0_peer_companion_worker ...
python -m Tools.ai build_npu_micro_task_companion_report ...
python -m Tools.ai check_npu_provider_environment ...
python -m Tools.ai runtime_hardware_capability ...
python -m Tools.ai provider_runtime_blackboard ...
python -m Tools.ai run ...
python -m Tools.ai provider_runtime_live_signals ...
python -m Tools.ai heap_provider_budget_governor ...
python -m Tools.ai heap_provider_invocation_contract ...
python -m Tools.npu run_dual_ai_pipeline ...
```

## Validation commands

```powershell
python -m Tools.validation run_ollama_tool_gateway_smoke ...
python -m Tools.validation run_openvino_peer_topology_contract_smoke ...
python -m Tools.validation check_openvino_peer_topology_contract ...
python -m Tools.validation check_gpu0_companion_contract ...
python -m Tools.validation run_npu_micro_task_companion_smoke ...
python -m Tools.validation run_observable_peer_activity_contract_smoke ...
python -m Tools.validation run_heap_provider_budget_governor_smoke ...
python -m Tools.validation run_heap_provider_invocation_contract_smoke ...
python -m Tools.validation check_runtime_hardware_delegation_contract ...
```

## Artifacts/evidence

Expected artifact families:

```text
Ollama provider report
GPU0 workload report
GPU0 companion/peer report
NPU microtask companion report
provider runtime blackboard state
contractor universe local compact evidence
provider live signals report
provider lane evidence
runtime hardware capability report
provider degraded/blocked classification
```

## Semantic rule

Provider agreement is not product success. Ollama may propose, GPU0 may review, NPU may audit, but CPU validators and concrete product boundaries decide whether anything can be called a real product.

---

# 4. Real product run model

## Concept

```text
task MD -> heap/exchange evidence -> candidate operations -> code/patch product -> validation -> reviewable product
```

## Current model doc

```text
docs/REAL_PRODUCT_RUN_MODEL.md
```

## Code families

```text
Tools/ai/run/
Tools/ai/operator_product_core/
Tools/ai/code_product/
Tools/ai/generated_patch_specs/
Tools/ai/repository_product/
Tools/validation/real_product/
Tools/validation/generated_patch_specs/
Tools/validation/repository_product/
Tools/validation/code_product/
```

## Main tool commands

```powershell
python -m Tools.ai run ...
python -m Tools.ai operator_product_view ...
python -m Tools.ai code_product_artifact_intake ...
python -m Tools.ai analyze_code_product_artifact ...
python -m Tools.ai full_run_bundle_zip ...
python -m Tools.ai generated_patch_specs_from_proposals ...
python -m Tools.ai generated_patch_specs_apply ...
python -m Tools.ai agent_review_prepare_pr ...
python -m Tools.ai build_review_pr_prepare_args ...
```

## Validation commands

```powershell
python -m Tools.validation run_real_product_preflight_gate ...
python -m Tools.validation run_real_product_preflight_gate_smoke ...
python -m Tools.validation check_real_product_runtime_mesh_contract ...
python -m Tools.validation run_real_product_runtime_mesh_contract_smoke ...
python -m Tools.validation check_review_pr_final_product_contract ...
python -m Tools.validation check_review_pr_product_readiness ...
python -m Tools.validation run_generated_patch_specs_empty_product_smoke ...
python -m Tools.validation run_code_product_artifact_intake_smoke ...
```

## Artifacts/evidence

Expected artifact families:

```text
operator request file
real product preflight report
runtime mesh report
full-run bundle ZIP
code product artifact
patch spec apply report
review preparation artifact
product readiness report
blocked reason when product is not real
```

## Semantic rule

Evidence-only runs are useful but are not product. Metadata-only specs are not product. A blocked state is valid when explicit.

---

# 5. Compact evidence model

## Concept

```text
raw runtime output -> selected facts -> compact evidence -> Git-trackable reference
```

## Current model doc

```text
docs/COMPACT_EVIDENCE_MODEL.md
```

## Code/document families

```text
docs/LOCAL_VALIDATION_EVIDENCE/
Tools/ai/repository_product/
Tools/ai/runtime_universe/
Tools/ai/agent_context/shared_toolbox_bundle
Tools/validation/docs_hygiene/
Tools/validation/runtime_universe/
```

## Main tool commands

```powershell
python -m Tools.ai build_github_evidence_bundle ...
python -m Tools.ai github_evidence_bundle_build_github_evidence_bundle_ready ...
python -m Tools.ai enrich_github_evidence_bundle_code_plan ...
python -m Tools.ai shared_toolbox_bundle ...
python -m Tools.ai build_unified_run_observer_snapshot ...
python -m Tools.ai build_unified_raw_debug_good_info_feed ...
python -m Tools.ai runtime_file_refs ...
```

## Validation commands

```powershell
python -m Tools.validation check_github_evidence_bundle ...
python -m Tools.validation run_shared_toolbox_ai_to_ai_bundle_smoke ...
python -m Tools.validation run_runtime_evidence_correlation_smoke ...
python -m Tools.validation check_runtime_evidence_correlation ...
python -m Tools.validation run_runtime_file_refs_smoke ...
python -m Tools.validation check_docs_links ...
python -m Tools.validation check_json_artifacts ...
```

## Artifacts/evidence

Expected committed evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.md
docs/LOCAL_VALIDATION_EVIDENCE/*.json
compact bundle summaries
file reference manifests
```

Expected non-committed raw output:

```text
output/**
*.db
*.sqlite
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
large generated chunk directories
```

## Semantic rule

Compact evidence supports decisions. It is not product by itself unless it supports a concrete code/patch/review product path.

---

# 6. Patch/code product boundary model

## Concept

```text
evidence -> plan -> candidate operation -> code/patch product -> reviewed apply boundary -> validation -> commit/review
```

## Current model doc

```text
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

## Code families

```text
Tools/ai/code_product/
Tools/ai/patch_product/
Tools/ai/patchkit/
Tools/repo_patch_runner/
Tools/validation/code_product/
Tools/validation/patch_product/
```

## Main tool commands

```powershell
python -m Tools.ai build_code_interpreter_report ...
python -m Tools.ai build_code_edit_proposal_from_plan ...
python -m Tools.ai code_product_artifact_intake ...
python -m Tools.ai analyze_code_product_artifact ...
python -m Tools.ai patch_plan_generator ...
python -m Tools.ai patch_suggestion_bundle ...
python -m Tools.ai synthesize_patch_candidates ...
python -m Tools.ai apply_patch_bundle ...
python -m Tools.repo_patch_runner apply_repo_mods ...
```

## Validation commands

```powershell
python -m Tools.validation run_code_product_artifact_intake_smoke ...
python -m Tools.validation run_patch_candidate_synthesis_smoke ...
python -m Tools.validation check_patch_suggestion_product_separation ...
python -m Tools.validation run_patchkit_smoke ...
python -m Tools.validation run_patchkit_bundle_contract_smoke ...
python -m Tools.validation check_patchkit_bundle_contract ...
```

## Artifacts/evidence

Expected artifact families:

```text
CODE_PRODUCT_FULL_PATCH.md
code-product intake report
patch candidate report
patch suggestion bundle
PatchKit bundle
PatchKit dry-run/apply report
repo-patch-runner apply report
validation report
```

## Semantic rule

Provider prose and patch plans are not apply-ready. Source writes require reviewed code/patch product and explicit apply boundary.

---

# Offuscated but important runtime bridge tools

These tools are easy to miss because they do not name a high-level model directly, but they are operational glue:

```text
provider_runtime_broker_bridge
provider_runtime_live_signals
provider_runtime_validation_bridge
build_provider_runtime_heap_from_peer_reports
runtime_file_refs
runtime_hardware_capability
agent_runtime_debug_lab
full_run_bundle_zip
```

Treat them as bridge/support tools. They should not be interpreted as final products by themselves.

# Core-first procedure

When unsure where to start, use this order:

```text
1. Read AGENTS.md and CONTEXT_INDEX.md.
2. Read this model-to-code map.
3. Read the relevant Universo IA model docs.
4. Pick the relevant model.
5. Open the listed code family TOOL_CONTEXT.md files.
6. Inspect the listed dispatcher command in dispatch.py.
7. Inspect target source.
8. Run or reference the listed validators.
9. Publish only compact evidence or a real code/patch product.
```

# Current limitations

- This map is dispatcher-driven, not an exhaustive per-file source audit.
- If dispatcher and this map disagree, inspect dispatcher/source and update this map.
- If a context file is marked `stub`, `stub-missing` or `partial` in `docs/CONTEXT_COVERAGE_STATUS.md`, inspect source before relying on it.
