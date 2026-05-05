# Next loop priority

Dopo effective-use optimization, la priorità non è ancora run reale.

## Priorità 1: bundle integration

Il prodotto qualitativo deve essere incluso nel bundle finale come evidence:

- `full0to10_effective_use_quality_product.md`;
- `full0to10_effective_use_tool_telemetry.json`;
- `full0to10_provider_hardening_contracts.json`;
- `full0to10_effective_use_optimization.json`.

## Priorità 2: runtime tool usage

Il registry runtime deve essere usato dal broker o dal supervisor in modo
tracciato. L'obiettivo è vedere:

```text
request -> tool invocation -> telemetry -> evidence bundle
```

## Priorità 3: provider hardening

Prima di generazione provider:

- quality stack pulito;
- workload report quality pulito;
- GPU/Ollama readiness;
- NPU/GPU.0 contract;
- no `.md.split/` source-side;
- no DB committati.

## Priorità 4: real run

La run reale diventa sensata solo quando il quality stack non segnala blocker.
