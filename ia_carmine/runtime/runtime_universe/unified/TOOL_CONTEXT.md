# ia_carmine/runtime/runtime_universe/unified context

## Role

`ia_carmine/runtime/runtime_universe/unified` contains unified-run feed, observer, contract-argument and debug-information helpers.

## Responsibilities

- Build unified AI conversation feeds.
- Build unified chain contract argument artifacts.
- Build unified raw debug information feeds.
- Build unified run observer snapshots.
- Support small wiring/error-policy patch helpers when explicitly invoked through dispatcher tools.

## Representative commands

Use through the AI dispatcher:

```powershell
python -m ia_carmine.cli build_unified_ai_conversation_feed ...
python -m ia_carmine.cli build_unified_chain_contract_args ...
python -m ia_carmine.cli build_unified_raw_debug_good_info_feed ...
python -m ia_carmine.cli build_unified_run_observer_snapshot ...
python -m ia_carmine.cli patch_unified_chain_contract_wiring ...
python -m ia_carmine.cli patch_unified_launcher_error_policy ...
```

## Output role

Outputs are unified runtime feed, observer and contract artifacts. They help inspect the run universe but are not final product artifacts by themselves.

## Notes

- Unified observer/feed files are support artifacts.
- Check current runtime reports before relying on older feeds.
- Add validation under `Tools/validation/runtime_universe` when schema or contract behavior changes.
