# Run permit contract

Il run permit è un contratto.

## Campi essenziali

- `permit_allowed`;
- `decision`;
- `failed_requirements`;
- `budget`;
- `npu_audit`;
- `execution_contract`.

## Regola

Anche quando `permit_allowed=true`, questa patch non esegue provider. Il permit
è input di una futura run esplicita.
