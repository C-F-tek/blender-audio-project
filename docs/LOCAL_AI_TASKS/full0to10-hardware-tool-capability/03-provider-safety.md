# Provider safety

La lane hardware/tool capability non deve essere confusa con la run provider.

## Regola

```text
provider_execution_performed=false
generation_performed=false
model_load_performed=false
```

Le capability servono a decidere se una run Full0To10 reale può partire, non a
produrre raccomandazioni.
