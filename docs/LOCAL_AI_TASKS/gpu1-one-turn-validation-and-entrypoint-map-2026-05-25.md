# GPU1 one-turn validation and entrypoint map — 2026-05-25

## Purpose

This document completes the implementation-point search for the GPU1 one-turn production gate by mapping:

```text
- provider command construction;
- runtime class composition / entrypoint;
- static real-product validators;
- live provider gate validators;
- bundle completeness validators.
```

Constraint:

```text
Do not import or execute the validator/preflight from full run.
The full run must own the one-turn logic in production runtime.
```

## 1. Provider command construction

File:

```text
ia_carmine/runtime/heap_gate/provider_command_specs.py
```

Function:

```text
build_provider_command_specs(...)
```

Observed behavior:

```text
- builds GPU1/GPU0/NPU provider commands;
- GPU1 command uses `python -m ia_carmine run_local_provider_probe`;
- GPU1 command receives `--prompt __GPU1_CUMULATIVE_PROMPT__`;
- provider_execution.py later rewrites prompt into file-backed prompt when needed;
- gpu1_native_tool_chat_loop.py later rewrites the command again into chat-history subturn mode.
```

Patch implication:

```text
Do not change the public GPU1 provider command surface unless necessary.
The one-turn logic belongs after command construction, in the production GPU1 chat loop and evidence gate.
```

Optional prompt/config additions:

```text
- expose a mode flag/metadata meaning `gpu1_one_turn_gate_required=true` for complete/full provider runs;
- keep it metadata/reporting only if command surface changes are risky;
- avoid new public run selector flags.
```

## 2. Runtime class composition and entrypoint

File:

```text
ia_carmine/runtime/heap_runtime/completeness_gate/cli.py
```

Observed behavior:

`HeapRuntimeCompletenessGate` is assembled from mixins:

```text
RuntimeGateInitMixin
RuntimeGateSourceRefsMixin
RuntimeGateStartupContextMixin
RuntimeGateProposalCycleAMixin
RuntimeGateProposalCycleBMixin
RuntimeGateHeapExchangeMixin
RuntimeGateMatrixLabMixin
RuntimeGateToolBrokerMixin
RuntimeGateLoopStepsMixin
RuntimeGateProviderContextMixin
RuntimeGateProviderCommandsMixin
RuntimeGateProviderRefinementMixin
RuntimeGateProviderPromptMixin
RuntimeGateProviderExecutionMixin
RuntimeGateRunLoopMixin
```

Patch implication:

```text
A helper module such as `ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py` can be used by existing mixins without changing the CLI or creating a new runner.
```

Do not add:

```text
python -m ia_carmine.cli gpu1_one_turn_run
```

The canonical entry remains:

```text
python -m ia_carmine.cli run
```

## 3. Static completeness contract validator

File:

```text
Tools/validation/heap_runtime/completeness_gate_contract.py
```

Observed behavior:

The validator checks static wiring for:

```text
startup manifest
GPU1/GPU0/NPU lane specs
provider teamwork
provider launch manifest
provider process evidence
matrix evidence consumption
```

Current gap:

```text
It does not check for any `gpu1_one_turn_*` production contract.
```

Patch requirement:

Add static checks:

```text
- `ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py` exists;
- `gpu1_native_tool_chat_loop.py` imports/calls production gate helper;
- `provider_execution.py` checks one-turn gate before sidecars;
- `run_loop_metrics.py` exposes one-turn gate metrics;
- `terminal_invariants.py` blocks complete/full success when gate is missing/failed;
- runtime code does not import `Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight`.
```

## 4. Real-product runtime mesh contract

File:

```text
Tools/validation/real_product/runtime_mesh_contract/cli.py
```

Observed behavior:

This validator checks the canonical run mesh:

```text
Task MD IN
python -m ia_carmine.cli run
heap_context_closure
GPU1/GPU0/NPU provider lanes
runtime broker and deterministic validators
CODE_PRODUCT_FULL_PATCH / final readable product
```

It checks many current provider mesh capabilities but not the one-turn gate.

Patch requirement:

Add capability:

```text
gpu1_one_turn_runtime_gate_contract
```

Static tokens to check:

```text
gpu1_one_turn_runtime_gate
gpu1_one_turn_runtime_gate_passed
gpu1_one_turn_tool_result_consumed
gpu1_one_turn_final_product_delta_valid
gpu0_npu_started_before_gpu1_one_turn_closed
```

Files to include in static scan:

```text
ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py
ia_carmine/runtime/heap_gate/gpu1_native_tool_chat_loop.py
ia_carmine/runtime/heap_gate/provider_execution.py
ia_carmine/runtime/heap_gate/run_loop_metrics.py
ia_carmine/runtime/heap_gate/terminal_invariants.py
```

## 5. Live provider gate validator

File:

```text
Tools/validation/real_product/live_provider_gate/cli.py
```

Observed behavior:

The live gate validates a `local_provider_probe` report and required lanes such as Ollama/NPU.

Current gap:

```text
It validates live provider execution, but not the GPU1 one-turn chain.
```

Patch options:

Option A — extend live gate:

```text
--gpu1-one-turn-gate <path>
--require-gpu1-one-turn
```

Then validate:

```text
kind == gpu1_one_turn_runtime_gate
passed == true
tool_result_consumed_by_gpu1 == true
final_product_delta_valid == true
```

Option B — create focused validator:

```text
Tools/validation/heap_runtime/gpu1_one_turn_runtime_gate/cli.py
```

Prefer Option B if live_provider_gate should remain strictly about provider/probe liveness.

## 6. Full-run bundle completeness validator

Files:

```text
Tools/validation/_shared/full_run_bundle_completeness.py
Tools/validation/real_product/check_full_run_bundle_completeness/cli.py
```

Observed behavior:

Bundle validation checks ZIP members and required recursive roots, but only against the builder report/artifact list. It does not know that `gpu1_one_turn_runtime_gate` is required.

Patch requirement:

After the production gate is added to the final product package/bundle manifest, require it in bundle validation.

Possible requirement:

```text
required_artifact_kind: gpu1_one_turn_runtime_gate
```

or path pattern:

```text
**/gpu1_one_turn_runtime_gate*.json
```

Acceptance:

```text
Full-run bundle cannot pass completeness validation if the GPU1 one-turn gate artifact is missing from the final evidence package.
```

## 7. Existing provider activation smoke

File:

```text
Tools/validation/heap_runtime/provider_loop_activation_smoke/cli.py
```

Patch requirement already identified:

```text
Update stale expectation around GPU1 native request scope.
```

Correct one-turn expectation:

```text
tool_result_scope == primary_pending_gpu1_resume_evidence
gpu1_followup_required == true
cannot_close_product == true
```

Then add tests for:

```text
- production gate helper exists;
- full-run runtime does not import preflight validator;
- no-tool GPU1 prose stays raw evidence;
- native tool call alone is not one-turn pass;
- broker result not consumed is blocker;
- consumed broker result + valid delta passes.
```

## 8. Exact implementation dependency graph

Recommended production data path:

```text
provider_command_specs.py
  -> builds GPU1 provider command
provider_execution.py
  -> calls run_gpu1_native_tool_chat_loop(...)
gpu1_native_tool_chat_loop.py
  -> runs GPU1 subturn 0
  -> publish_provider_report_native_tool_calls(...)
  -> gate.run_bridge()
provider_runtime_blackboard/broker_bridge/cli.py
  -> executes broker requests and appends broker_result events
  -> preserves lane/revision/subturn/chat_history_ref/request_id metadata
gpu1_native_tool_chat_loop.py
  -> appends role=tool message
  -> runs GPU1 subturn 1
  -> calls build_gpu1_one_turn_runtime_gate(...)
gpu1_one_turn_gate.py
  -> writes kind=gpu1_one_turn_runtime_gate
provider_commands.py / provider_report_absorption.py
  -> preserve gate fields into provider report graph
provider_execution.py
  -> blocks sidecars if gate failed
proposal_cycle_a.py / run_loop_metrics.py
  -> expose final product + gate metrics
terminal_invariants.py
  -> blocks complete/full success if gate missing/failed
bundle validators
  -> require gate artifact in final evidence package
```

## 9. Updated validation plan

After patch, run at least:

```powershell
python -m py_compile `
  ia_carmine\runtime\heap_gate\gpu1_one_turn_gate.py `
  ia_carmine\runtime\heap_gate\gpu1_native_tool_chat_loop.py `
  ia_carmine\runtime\heap_gate\provider_execution.py `
  ia_carmine\runtime\heap_gate\provider_commands.py `
  ia_carmine\runtime\heap_gate\provider_report_absorption.py `
  ia_carmine\runtime\heap_gate\run_loop_metrics.py `
  ia_carmine\runtime\heap_gate\terminal_invariants.py

python -m Tools.validation run_provider_loop_activation_smoke --repo-root .
python -m Tools.validation run_heap_gate_terminal_invariants_smoke --repo-root .
python -m Tools.validation check_real_product_runtime_mesh_contract --repo-root .
python -m Tools.validation check_full_run_bundle_completeness --help

git diff --check
```

## 10. Final diagnosis

The implementation target is now precise:

```text
No new runner.
No preflight import.
No validator dependency.
Add one production helper and wire its report through existing runtime graph, metrics, invariants and bundle validation.
```
