# Tools/validation/runtime_universe context

## Role

`Tools/validation/runtime_universe` validates the wider runtime-universe layer: unified manifests, observer snapshots, execution plans, evidence correlation and hardcode guards.

## Responsibilities

- Check unified run manifest schema.
- Validate observer and snapshot reports.
- Check runtime evidence correlation.
- Validate selective execution plans.
- Check core activation and hardcode guards.
- Validate unified chain contracts.

## Representative command surface

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_runtime_universe_smoke ...
python -m Tools.validation run_unified_run_manifest_schema_smoke ...
python -m Tools.validation run_unified_observer_extended_smoke ...
python -m Tools.validation run_runtime_evidence_correlation_smoke ...
python -m Tools.validation check_runtime_evidence_correlation ...
python -m Tools.validation check_selective_execution_plan ...
python -m Tools.validation run_runtime_hardcode_guard_smoke ...
python -m Tools.validation unified_chain_contract ...
```

## Contract model

```text
runtime report -> manifest/feed/snapshot -> correlation check -> contract result
```

## Expected artifacts

```text
unified manifest report
observer snapshot report
runtime evidence correlation report
selective execution plan report
hardcode guard report
```

## Boundaries

- A runtime map or summary is not final product success.
- Evidence correlation should point to concrete artifacts.
- Stale generated reports should not override current source.

## Extension notes

When a new runtime-universe artifact is introduced, add a schema or correlation check here so later AI runs can trust its shape.