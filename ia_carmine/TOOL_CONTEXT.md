# ia_carmine context

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `CODE_PRODUCT_FULL_PATCH.md` is the final patch/code product; `PLAN_PRODUCT_FULL_PATCH.md` is the final recomposed GPU1 prompt/chat product, with pointer graph and recovery/congruence as technical attachments.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Role

`ia_carmine` is the main IA-Carmine runtime and product surface. It owns the operator launcher, heap runtime, provider mesh, context/memory reload, brokered tools, code-product generation, patch-product synthesis, repository product tools, runtime evidence and AI-to-AI bundle artifacts.

Canonical invocation:

```powershell
python -m ia_carmine.cli <tool> [tool args...]
```

The source of truth for public tool names is `ia_carmine/dispatch.py`. Do not infer supported commands from old root-level script names; use the dispatcher or `python -m ia_carmine.cli --list`.

## Main families

### Operator run and launcher

Use these when the operator wants to start from a Markdown request, choose repo/output directories, run a full product cycle and review/apply a generated code product.

Representative tools:

```text
run
operator_product_gui
operator_product_view
code_product_artifact_intake
analyze_code_product_artifact
```

Expected flow:

```text
request MD -> operator launcher/controller -> heap runtime closure -> final readable product
-> CODE_PRODUCT_FULL_PATCH.md -> intake/review -> optional safe apply
```

`Apply safe` must remain a reviewed action. It must not be confused with provider proposal generation.

### Heap runtime and blackboard

Use these for the shared runtime universe: startup context, heap state, broker activity, provider claims, proposal chunks, pointer/revision context and final product assembly.

Representative tools:

```text
heap_context_memory_reload
run_heap_runtime_completeness_gate
run_heap_code_execution_tool
run_heap_code_execution_matrix
run_heap_virtual_dev_environment
heap_event_pointers
heap_final_proposals
assemble_heap_final_readable_product
```

Operational rule:

```text
provider text != code product
matrix/lab diff evidence = source for code product
```

### Context, memory and semantic input

Use these before provider work or as startup inputs. They collect tool inventory, memory, transient request state, context packs and semantic evidence chunks.

Representative tools:

```text
build_agent_agnostic_tool_inventory
build_agent_memory_inventory
runtime_sqlite_memory
agent_runtime_sqlite_memory
build_agent_transient_request_context
ai_context_pack
semantic_evidence_chunks
select_semantic_code_chunks
shared_toolbox_bundle
```

Memory policy:

```text
operational SQLite -> output/ai_runtime_memory/operational_context.sqlite
persistent SQLite -> indexAI/agent_memory/agent_memory.sqlite
```

Operational memory can be written by the run. Persistent memory must remain read-only unless an explicit persistent-write confirmation is provided.

### Broker and runtime tools

Use these when a provider or runtime component must request tool work through a controlled broker instead of direct arbitrary execution.

Representative tools:

```text
agent_runtime_tool_broker
runtime_tool_broker
build_runtime_tool_capability_manifest
runtime_file_refs
agent_runtime_debug_lab
```

Broker guardrails must distinguish generated report writes from source writes. Runtime output under `output/**` is not a source patch unless explicitly promoted through a reviewed code product.

### Provider mesh

Use these for provider lanes and hardware-specific diagnostics.

Representative tools:

```text
legacy_gpu_deep_planning_supervised
legacy_gpu_deep_planning_review
legacy_gpu_npu_parallel_orchestrator
legacy_npu_gpu_deep_review_auditor
legacy_ollama_tool_gateway
provider_mesh_runtime
run_local_provider_probe
check_local_resource_lanes
build_ollama_gpu0_peer_report
build_openvino_hardware_governance_report
```

The historical gateway/deep-planning/orchestrator names are no longer exposed
under their old public command names. Their `legacy_*` dispatcher aliases are
marked `LEGACY_NON_RUN_UNICA_COMMANDS` in `ia_carmine/dispatch.py`. They remain
inspectable compatibility surfaces, but current run-unica evidence must flow
through `run`, `heap_context_closure`, `gpu1_dynamic_context_pack` and native
broker tool-call artifacts.

`check_local_resource_lanes` is a resource/provider preflight, not a static
source inspection. Its `provider_execution_performed=false` field only means no
provider generation/workload was proven; the report must still expose resource
mechanics and probe counters when it touches Ollama/OpenVINO/device discovery.

Intended provider roles:

```text
GPU1/Ollama -> planner/proposal lane
GPU0/Ollama Vulkan -> reviewer/refiner/peer workload lane
NPU/OpenVINO -> sampled auditor and guardrail lane
CPU/helper -> broker, validators, file scanning, matrix, composer
```

### Code product and patch product

Use these only when a target, diff, patch candidate, or code-product artifact exists.

Representative tools:

```text
build_code_interpreter_report
build_code_edit_proposal_from_plan
build_code_patch_artifact_pack
build_code_patch_docs_followup
patch_plan_generator
patch_plan_quality_product
patch_suggestion_bundle
synthesize_patch_candidates
full_run_bundle_zip
```

A valid code product must contain real diff/code or an explicit non-applicable status. Do not call `verified target with no diff` an apply-ready patch.

### Repository product and evidence bundles

Use these to summarize repository state and publish compact Git-trackable evidence, not raw runtime output.

Representative tools:

```text
build_repository_consistency_map
repository_consistency_map
repository_change_proposals
repository_update_suggestions
megalithic_repo_review
build_github_evidence_bundle
enrich_github_evidence_bundle_code_plan
```

Do not copy raw `output/**`, checkpoint directories, databases, render artifacts or large generated chunks into Git.

## Safe extension rules

- Add a new tool under an existing package family when possible.
- Register public tool names in `ia_carmine/dispatch.py`.
- Keep implementation modules internal and focused.
- Validate with package invocation, not legacy file-path invocation.
- Prefer small CLIs calling reusable core modules.
- Do not add new direct source-writing paths without explicit guardrails and smoke coverage.
