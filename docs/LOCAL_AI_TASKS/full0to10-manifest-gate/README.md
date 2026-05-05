# Full0To10 manifest gate

Questa directory documenta il gate post-bundle della run Full0To10.

## Componenti

- `Tools/ai/build_full0to10_run_manifest.py`
- `Tools/workflow/run_full0to10_manifest_contract_gate.ps1`
- `Tools/validation/run_full0to10_manifest_gate_smoke.py`

## Scopo

Il gate costruisce un manifest ricorsivo della run e poi esegue il validator
contratti introdotto nella patch precedente.

## Output locali

```text
output/validation/full0to10_manifest_contract_gate/
```

Gli output sono runtime artifact locali e non vanno committati.
