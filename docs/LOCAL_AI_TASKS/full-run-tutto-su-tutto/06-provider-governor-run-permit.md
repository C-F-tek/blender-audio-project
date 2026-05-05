# Provider governor run permit

Il provider governor introduce il permesso di run come artifact separato dalla
run reale.

## Sequenza

```text
accelerator control
quality gate
budget
NPU audit plan
policy requirements
run permit
final product package
```

## Regola

Il permit può essere prodotto senza generazione provider. Produrre il permit non
significa eseguire il provider.

## Condizioni

- operator intent;
- quality gate;
- accelerator scheduler in pre-run blocked mode;
- GPU mind richiede launcher;
- workload quality validator disponibile;
- NPU audit plan;
- GPU.0 guardrail.

## Output

```text
full0to10_provider_governor.json
full0to10_provider_run_permit.json
full0to10_provider_governor_telemetry.json
full0to10_provider_governor.md
```
