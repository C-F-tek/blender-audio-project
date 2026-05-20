# Tools/ai/heap_exchange context

## Role

`Tools/ai/heap_exchange` owns heap/exchange lifecycle support artifacts: runtime entry, runtime exit, peer runtime manifests, task ingress contracts, closure audits and lifecycle wiring support.

This area concretizes:

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Responsibilities

- Record/verify controlled runtime entry into the heap/exchange.
- Build peer runtime manifests describing participating lanes.
- Build task ingress contracts so request/context entry is explicit.
- Build runtime exit products or blocked-state reports.
- Build closure/audit reports for exchange lifecycle evidence.
- Keep exchange output linked to runtime state, provider evidence and validation artifacts.
- Support lifecycle wiring patches only when explicitly scoped.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m Tools.ai heap_exchange_runtime_entry ...
python -m Tools.ai heap_exchange_runtime_exit ...
python -m Tools.ai heap_exchange_peer_runtime_manifest ...
python -m Tools.ai heap_exchange_task_ingress_contract ...
python -m Tools.ai heap_exchange_closure_audit ...
python -m Tools.ai patch_unified_heap_exchange_lifecycle_wiring ...
```

## Lifecycle model

```text
task/request
-> runtime entry
-> task ingress contract
-> peer/lane manifest
-> heap/runtime state and exchange events
-> provider/tool/validator evidence
-> runtime exit product or blocked reason
-> closure audit
```

The lifecycle is not complete when only an input file or provider answer exists.

## Output role

Outputs from this area are exchange/lifecycle support artifacts. They help the runtime universe describe what happened across a run.

Expected artifacts include:

```text
runtime entry report
task ingress contract
peer runtime manifest
runtime exit report
closure audit report
lifecycle wiring report
```

## Boundaries

- Heap exchange support is not a substitute for heap runtime state.
- Runtime entry is not proof of product success.
- Runtime exit must classify product or blocked state.
- Peer manifests are evidence of lane registration, not proof of useful lane output.
- Keep generated exchange artifacts out of Git unless selected as compact evidence.
- Inspect `Tools/ai/dispatch.py` before assuming a package is public CLI surface.

## Validation expectations

Relevant validation areas:

```powershell
python -m Tools.validation check_heap_exchange_runtime_lifecycle ...
python -m Tools.validation run_heap_exchange_runtime_lifecycle_smoke ...
python -m Tools.validation run_heap_exchange_closure_audit_smoke ...
python -m Tools.validation run_heap_exchange_review_bridge_smoke ...
python -m Tools.validation run_heap_peer_runtime_manifest_smoke ...
python -m Tools.validation run_task_ingress_contract_smoke ...
```

## Notes

When adding lifecycle artifacts, update `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` and validation together.