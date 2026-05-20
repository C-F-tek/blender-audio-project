# Provider invocation dry-run plan

Il permit del governor viene trasformato in un piano di invocazione dry-run.

## Sequenza

```text
provider governor permit
dry-run invocation plan
workload report contract
expected evidence contract
NPU audit hooks
final product package inclusion
```

## Regola

Il dry-run plan non esegue provider. Prepara soltanto:

- comandi teorici;
- output obbligatori;
- evidence attesa;
- audit NPU;
- stop condition.

## Prossimo salto

Il loop successivo potrà collegare il dry-run plan al bundle finale e poi
preparare una real-run gated separata.
