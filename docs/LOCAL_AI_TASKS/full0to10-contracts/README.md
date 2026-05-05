# Full0To10 contracts

Questa directory contiene la documentazione modulare della lane di controllo contratti
Full0To10. La policy è evitare Markdown mostri: ogni file mantenuto deve restare
compatto e specializzato.

## Documenti

- `01-bundle-completeness.md` — superfici obbligatorie del bundle completo.
- `02-sqlite-memory-visibility.md` — visibilità SQLite/memory senza versionare DB.
- `03-hardware-delegation.md` — contratto CPU/GPU/NPU e parallelismo sicuro.

## Tool

- `Tools/validation/check_full0to10_bundle_contracts.py`
- `Tools/validation/run_full0to10_bundle_contracts_smoke.py`
- `Tools/validation/full0to10_contracts/`

## Principio

Full0To10 significa TUTTO su TUTTO:

```text
discovery -> CSV/index -> context -> provider diagnostics -> memory visibility
-> telemetry -> capability -> recommendations -> patch plan -> evidence bundle
```

La lane non deve applicare patch automaticamente, non deve scrivere DB persistenti
senza conferma, e non deve committare artifact runtime.
