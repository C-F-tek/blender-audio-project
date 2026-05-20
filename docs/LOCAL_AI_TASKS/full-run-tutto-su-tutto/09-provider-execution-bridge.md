# Provider execution bridge

Il bridge collega il dry-run plan a una futura real-run.

## Sequenza

```text
provider invocation dry-run plan
real-run gate
command plan
workload output paths
bridge evidence
final product inclusion
```

## Regola

Il bridge non esegue provider. Produce solo il piano finale prima di una
eventuale lane reale.
