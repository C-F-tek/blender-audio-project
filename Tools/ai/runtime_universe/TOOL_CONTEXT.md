# Tools/ai/runtime_universe context

## Role

`Tools/ai/runtime_universe` contains higher-level runtime universe builders, flow maps, execution plans, smart gatekeeping and unified run feed builders.

It describes and summarizes the runtime system around a run; it is not a replacement for the heap runtime itself.

## Main responsibilities

- Build runtime universe models and reports.
- Render flow maps for tool/runtime/data relationships.
- Build selective execution plans.
- Provide smart gatekeeper checks.
- Build unified observer/conversation/raw debug feeds.
- Patch or validate unified chain/launcher wiring when explicitly requested.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m Tools.ai runtime_flow_map ...
python -m Tools.ai selective_execution_plan ...
python -m Tools.ai smart_ai_gatekeeper ...
python -m Tools.ai build_unified_ai_conversation_feed ...
python -m Tools.ai build_unified_chain_contract_args ...
python -m Tools.ai build_unified_raw_debug_good_info_feed ...
python -m Tools.ai build_unified_run_observer_snapshot ...
```

## Conceptual model

```text
request
-> startup context/memory reload
-> heap state and brokered tools
-> provider lanes
-> proposal iterations
-> pointer graph
-> composer/final product
-> postrun package and revision context
```

The universe layer helps map and explain this system, but product validity still depends on runtime artifacts, matrix/lab evidence and code product checks.

## Outputs

Typical outputs include:

```text
runtime universe report
flow map
selective execution plan
unified observer snapshot
unified conversation/feed artifacts
raw debug information feed
```

## Guardrails

- Do not treat a map/summary as proof of product success.
- Do not add a new universe when existing heap/runtime tools should be fixed.
- Do not bypass validation gates with summary-only artifacts.
- Keep observer/feed outputs separate from final product.

## Extension notes

Add new universe features when they improve observability, planning, or contract enforcement. If they affect runtime decisions, add validation under `Tools/validation/runtime_universe`.
