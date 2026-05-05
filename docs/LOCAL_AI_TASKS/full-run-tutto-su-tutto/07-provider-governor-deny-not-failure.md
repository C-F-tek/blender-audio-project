# Provider governor: deny is not failure

Il provider governor può negare una run provider.

## Regola

```text
deny = policy decision valida
failure = errore strutturale
```

## Impatto CLI

Default:

```text
deny -> exit code 0
```

Modalità stretta:

```text
--strict-permit + deny -> exit code 1
```

## Perché

Il pre-run deve poter produrre evidence anche quando la risposta corretta è
"non eseguire provider".
