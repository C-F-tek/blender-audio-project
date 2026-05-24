# Tools/validation context

## Role

`Tools/validation` owns validators, smoke tests, contract checks and readiness gates for IA-Carmine. It verifies properties of the runtime and artifacts; it does not define product success by itself.

Canonical invocation:

```powershell
python -m Tools.validation <tool> [tool args...]
```

The source of truth for public validation tool names is `Tools/validation/dispatch.py`. Use `python -m Tools.validation --list` to inspect the current surface.

## Main families

### Validation gate

Use these when a workflow needs one repeatable entry point for a known suite.

Representative tools:

```text
run_validation_gate
run_core_runtime_guard_suite
check_validation_report_contract
```

The gate should aggregate evidence, not hide failing details. A passing gate proves only the checked contract, not the entire product.

### Heap runtime validation

Use these to verify startup, heap closure, source allowlists, terminal invariants, code execution and virtual development environment behavior.

Representative tools:

```text
run_heap_runtime_completeness_gate_smoke
run_heap_code_execution_tool_smoke
run_heap_virtual_dev_environment_smoke
run_heap_final_readable_product_smoke
run_heap_file_backed_request_startup_smoke
run_heap_source_allowlist_contract_smoke
run_heap_source_anchor_priority_smoke
run_heap_gate_terminal_invariants_smoke
```

Expected checks:

```text
startup context is loaded
broker/tool activity is recorded
source writes are blocked unless explicitly allowed
matrix/lab evidence is separate from provider text
final readable product is assembled from validated evidence
```

### Runtime universe and unified run contracts

Use these for lifecycle, observer, manifest, correlation and unified-chain contracts.

Representative tools:

```text
run_runtime_universe_smoke
unified_chain_contract
run_unified_chain_contract_smoke
run_unified_run_manifest_schema_smoke
run_unified_observer_extended_smoke
run_runtime_evidence_correlation_smoke
```

These tools should prevent drift between declared run manifests, actual outputs and final product artifacts.

### Runtime tool and broker validation

Use these to validate broker dispatch, provider tool loops, runtime file refs, NPU/GPU tool context and runtime tool capability contracts.

Representative tools:

```text
run_agent_runtime_tool_broker_smoke
check_runtime_tool_broker_dispatch_alignment
run_provider_tool_loop_smoke
run_provider_tool_evidence_chain_smoke
run_runtime_file_refs_smoke
run_gpu_runtime_tool_bootstrap_smoke
run_npu_runtime_tool_context_smoke
run_npu_runtime_tool_execution_smoke
```

A broker smoke must verify controlled invocation and guardrails. It must not bless arbitrary shell access.

### Provider mesh validation

Use these for GPU/NPU/OpenVINO/Ollama contracts and provider evidence quality.

Representative tools:

```text
check_gpu0_companion_contract
check_openvino_peer_topology_contract
run_openvino_peer_topology_contract_smoke
run_npu_micro_task_companion_smoke
legacy_run_ollama_tool_gateway_smoke
run_gpu_planner_json_contract_smoke
run_gpu_runner_provider_error_smoke
```

Provider validations prove lane availability or response shape. They do not prove that the provider produced an apply-ready patch.

### Code product, patch product and generated patch specs

Use these when a patch candidate, code product artifact, PatchKit bundle, or generated patch spec must be checked.

Representative tools:

```text
run_code_product_artifact_intake_smoke
run_patch_candidate_synthesis_smoke
run_patchkit_smoke
run_patchkit_bundle_contract_smoke
run_patch_suggestion_bundle_apply_smoke
check_patchkit_bundle_contract
check_patch_suggestion_product_separation
reviewed_patch_specs_check
```

Code-product validation must distinguish:

```text
real diff/code present -> review/apply candidate
already integrated -> no-op but valid
verified target with no diff -> evidence only
missing/truncated payload -> blocked/manual review
```

### Agent context, memory and review validation

Use these to verify context pack contracts, semantic chunks, memory policy, review sufficiency and patch plan quality.

Representative tools:

```text
check_ai_context_pack_contract
check_selected_semantic_chunks
run_shared_toolbox_ai_to_ai_bundle_smoke
check_agent_memory_policy
run_runtime_sqlite_persistent_write_smoke
run_agent_review_evidence_sufficiency_smoke
run_agent_review_patch_plan_smoke
run_agent_review_decision_loop_smoke
```

Persistent SQLite write validation must remain explicit. Runtime scratch SQLite is allowed only as runtime state and is not Git-trackable.

### Docs and repository hygiene validation

Use these when documentation and code contracts must stay aligned.

Representative tools:

```text
check_docs_links
check_docs_contract_drift
check_code_contract_drift
check_package_structure
check_python_syntax
check_file_line_limits
check_markdown_line_limits
build_script_inventory
build_python_line_count_csv
```

These tools are useful before and after large refactors to prevent stale Markdown and legacy invocation paths.

## Safe extension rules

- Register public validations in `Tools/validation/dispatch.py`.
- Name smokes by the property they verify, not by the implementation detail.
- Do not add smoke-only success markers that bypass product gates.
- Keep fixtures isolated from the real repository.
- Do not write source files from validation tools unless the tool is explicitly a controlled apply test against a fixture.
