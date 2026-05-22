# ia_carmine/runtime/run context

## Role

`ia_carmine/runtime/run` is the canonical packaged entrypoint for IA-Carmine / Universo IA runs.

It is the public command behind:

```powershell
python -m ia_carmine.cli run ...
```

This package is not just a command wrapper. It is the operator-facing entrypoint where request files, explicit runtime parameters, runtime lanes, evidence and final product classification meet. `--dry-run` is only a preview; removing it starts the real provider path with GPU1/GPU0/NPU requested by default.

Current runtime route:

```text
operator_product_core
-> heap_context_closure
-> run_heap_runtime_completeness_gate
```

`contractor_universe` is not excluded. It is the compact scheduler/soft-time
model that must be folded into the same run universe as heap/pointer/revision
evidence. It must not become a second public product route or bypass provider
lane evidence. The main flow consumes that useful logic through the provider
leader packet `contractor_universe_surface_contract`, alongside startup
manifest, memory/chunks, broker evidence, matrix/lab and product boundary
surfaces.

There is no alternate runtime selector flag. Full smoke and legacy full-run
wrappers are not standalone product entry commands. They are downstream
verification or historical compatibility code, not public entry choices from
this command.

## Mandatory model contracts

Before changing this area, read:

```text
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

## Responsibilities

- Accept operator request files and explicit runtime parameters.
- Treat real, non-dry runs as provider-product runs by default.
- Route execution into maintained AI runtime packages.
- Keep the public run command stable while internal packages evolve.
- Preserve clear separation between command preview, runtime execution, evidence generation and final product artifacts.
- Preserve complete/full lane viability rules.
- Classify final state as product, no-op/non-applicable, blocked or unviable.
- Avoid turning provider prose, report existence or bundle existence into product success.

## Complete/full rule

In complete/full runs, required core lanes are not optional.

```text
valid evidence -> viable
missing evidence -> unviable
failed evidence -> unviable
degraded -> unviable
unavailable -> unviable
```

`degraded` and `unavailable` do not satisfy full mode. They are failure/unviable states for a complete run unless the run is explicitly partial/diagnostic and says so.

## Run lifecycle model

```text
operator request / request file
-> startup/preload/context
-> heap/exchange runtime entry
-> provider lane execution with GPU1 closure owner, GPU0 reviewer/refiner, NPU bounded micro audit
-> runtime tool/broker evidence
-> validator evidence
-> heap/exchange runtime exit
-> product/no-op/blocked/unviable classification
-> compact evidence or product artifact
```

A run that skips lifecycle stages without explicit partial/diagnostic classification is not complete.

## Output role

Outputs depend on the explicit run parameters. They may include:

```text
runtime reports
provider reports
runtime tool/broker reports
heap/exchange lifecycle artifacts
validation references
final readable products
code-product artifacts
full-run bundle ZIPs
blocked/unviable reason reports
```

These outputs must be classified. Raw output existence does not imply product success.

## Product classification

Use `docs/REAL_PRODUCT_RUN_MODEL.md`:

```text
evidence-only run -> useful diagnostics, not product
blocked product run -> valid safe exit, not product success
real product run -> concrete operation/product + validation + reviewable artifact
unviable full run -> required lane missing/failed/degraded/unavailable
```

The canonical final product is a single run outcome, not necessarily a code
diff. Valid product kinds are:

```text
code_patch_product
text_product
technical_plan_product
diagnostic_decision_product
blocked_continuation_product
```

Code products require concrete targets, diff/code and validation. Text or
technical-plan products must be complete operational documents approved through
the heap/pointer cycle, not raw provider prose. When the universe has not
closed coherently, the output must be `blocked_continuation_product` with
`resume_from_block_id`, pointer evidence and a soft-close reason.

Runtime limits such as budget, max iterations, max rounds and provider
revision count are governors. They must not be treated as proof that the
product is complete. If they stop progress before approval, the run exits with
continuation/block evidence rather than a hard empty product.

GPU1/Ollama opens review, coordinates native tool-calling through the broker
and closes/synthesizes the product state. GPU0/Ollama Vulkan may review, refine
and emit tool evidence, but it is not the primary closer. NPU/OpenVINO is required
as bounded micro-audit evidence in complete runs, but it must not hold the loop
open as the primary semantic provider.

Provider compute must be proven on accelerator lanes. `--require-ollama-gpu-residency`
is on for the canonical run and has no permissive CPU-provider bypass:
the operator must pass an explicit `--provider-model <MODELLO>` for real
provider runs. GPU1 requests `--ollama-gpu-layers all`; `ollama ps` / `100% GPU`
proves residency only, not useful provider work. Real GPU1 provider work also
requires non-replight generation, useful output, coherent token/duration metrics
and GPU runtime samples during the inference window. Operator observations such
as Task Manager evidence of inactive GPU compute are `operator_gpu_observation`
and may block GPU1 as `gpu1_no_observable_compute`.

GPU0 must use Ollama/Vulkan and produce review/refinement output with
`provider_work_verified=true`; OpenVINO GPU0 is diagnostic only and is not a
complete-run fallback. OpenVINO `NPU` must compile/execute the bounded
micro-provider and produce useful audit output. Device visibility, diagnostics
and short replight handshakes are health evidence only.
Only reports with `provider_work_verified=true` may count provider roles or set
`provider_execution_performed=true`. CPU remains valid only for runtime scripts,
broker orchestration, parsing, I/O and deterministic validators.

Provider boot is the hard live gate for real run-unica execution. Before heap
loop, proposal cycles, soft lock or long sidecar work can proceed, GPU1/Ollama,
GPU0/Ollama Vulkan and NPU/OpenVINO must be alive in the same provider window.
GPU1 then emits the short replight report with model/backend/device, loaded
status, generated phrase, token metrics, native tool policy, broker tool count
and declared functionality. GPU0/NPU useful workload is proven in the real
provider loop; their boot failure closes immediately as `provider_boot_gate_failed:*`.

The technical `final_root` is not the public product root. Every real run must
also publish or mirror the final product or blocked continuation package to:

```text
C:\Users\carmi\Documents\aicarmine_gui_launcher_lab_<stamp>
```

That package must be present even for `blocked_continuation_product` and must
include the readable decision files and pointer/resume evidence when available.

Soft close is elastic finalization. It must expose `soft_lock_state`,
`soft_lock_extension_count`, `open_pointer_count_final` and a pointer closure
table. If any pointer cannot be resolved inside the run, the valid public output
is `blocked_continuation_product` with `resume_from_block_id`, not an approved
product that drops unresolved blocks.

The soft-lock close rule is quorum based. GPU1 is the closure owner and may
choose `finalize_product`, `blocked_continuation`, `no_more_action` or
`needs_gpu0_refine`. GPU0 must answer `agree_close`, `veto_with_reason` or
`refine_once`. CPU validators decide whether the quorum is `ready_to_close`,
`blocked_continuation_ready`, `targeted_refine_allowed` or `blocked_with_reason`.
NPU is advisory-only in this phase: valid NPU micro evidence is kept as
`evidence_ready_non_closer`, but NPU does not keep the run alive and must not
become `latest_block_id`/closure cursor.

## Preflight gating

`run_real_product_preflight_gate` is downstream/static diagnostic evidence for
this entrypoint. A stale/static preflight failure must be reported and counted,
but it must not skip startup/provider when the preflight report still marks
`product_entry_allowed=true`. Only real runtime blockers, such as an explicit
product-entry denial or provider-lane activation failure, may block startup.

## Command preview boundary

A command preview is not a completed run.

```text
command rendered != run executed
return code exists != product exists
output folder exists != product exists
bundle ZIP exists != product exists
provider text exists != product exists
```

`--dry-run` must report the provider command that would run, including provider-generation flags, while keeping `execution_performed=false` and `provider_execution_performed=false`.

A completed run requires output artifacts, return codes, lane evidence, validation/product classification and no unviable required lane in complete/full mode.

## Relationship to other packages

`ia_carmine/runtime/run` routes into the actual runtime/product packages. Important
internal packages and downstream validators:

```text
ia_carmine/runtime/contractor_universe/TOOL_CONTEXT.md
ia_carmine/runtime/heap_exchange/TOOL_CONTEXT.md
ia_carmine/runtime/heap_runtime/TOOL_CONTEXT.md
ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md
ia_carmine/runtime/provider_runtime_blackboard/TOOL_CONTEXT.md
ia_carmine/runtime/runtime_tool/TOOL_CONTEXT.md
ia_carmine/product/code_product/TOOL_CONTEXT.md
ia_carmine/product/patch_product/TOOL_CONTEXT.md
Tools/validation/real_product/TOOL_CONTEXT.md
```

## Guardrails

- Do not silently downgrade complete/full runs to partial behavior.
- Do not use smoke/full-run validators as the product entry command.
- Do not add parallel runtime selector switches for competing run flows.
- Do not make GPU0/NPU/provider lanes optional by implementation convenience.
- Do not allow a real no-provider product run through this entrypoint.
- Do not accept CPU-only or unproven accelerator residency as provider evidence.
- Do not run code-product intake on empty/no-applicable/no-diff final products.
- Do not report full success with degraded or unavailable required lanes.
- Do not commit raw `output/**` from a run by default.
- Do not treat final readable output as apply-ready source change unless code/patch product boundaries pass.
- Inspect `ia_carmine/dispatch.py` and this package before changing the public run command.

## Extension notes

When run parameter semantics change, update together:

```text
ia_carmine/runtime/run/TOOL_CONTEXT.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
Tools/validation/real_product/TOOL_CONTEXT.md
Tools/validation/runtime_universe/TOOL_CONTEXT.md
```
