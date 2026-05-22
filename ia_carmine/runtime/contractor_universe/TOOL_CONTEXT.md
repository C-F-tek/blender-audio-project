# ia_carmine/runtime/contractor_universe context

## Role

`ia_carmine/runtime/contractor_universe` is the compact heap scheduler / soft-time model
for the canonical run universe. It compacts the existing Universo IA
provider-lane model into explicit priority-heap tasks, a logical clock and
GPU1/GPU0/NPU contractor roles.

It is not excluded from the run model, but the current deterministic scaffold is
not enough to satisfy a complete provider run by itself. It must be integrated
inside the single canonical flow:

```text
python -m ia_carmine.cli run
-> operator_product_core
-> heap_context_closure
-> run_heap_runtime_completeness_gate
-> heap/pointer/revision/product reconstruction
```

## Boundaries

- It is not registered as a second public dispatcher command.
- It does not import `Tools.validation` from the runtime core.
- It does not perform telemetry, source writes, patch application or provider
  execution in the initial deterministic backend.
- It produces local compact evidence only: `run.json`, `run.md`,
  `pointer_graph.json`, blackboard snapshot and event log.
- It must not become an alternate product flow outside the dispatcher-owned
  run path.

## Current status

Initial diagnostic/runtime scaffold for heap scheduling and soft-time closure.
The useful pieces are `UniverseHeap`, `LogicalClock` and contractor role
semantics. `surface.py` exposes those semantics to the main heap/provider
leader packet as `contractor_universe_surface_contract`; this keeps the logic
inside the single canonical universe instead of creating a second route.
Provider execution remains unproven until real provider adapters or the heap
gate leave observable GPU1/GPU0/NPU evidence.

Validation:

```powershell
python -m Tools.validation run_contractor_universe_surface_contract_smoke
```
