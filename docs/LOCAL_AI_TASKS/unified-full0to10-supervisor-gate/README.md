# Unified Full0To10 supervisor gate

Questo wrapper rende operativa la sequenza:

```text
unified launcher -> manifest builder -> contract validator
```

senza modificare direttamente il monolite `run_unified_local_ai_refactor.ps1`.

## Entry point

```text
Tools/workflow/run_unified_full0to10_with_contract_gate.ps1
```

## Perché wrapper separato

- riduce rischio su launcher lungo;
- permette smoke con `-SkipLauncher`;
- conserva il gate anche se il launcher fallisce;
- mantiene path e output sotto controllo;
- non cambia policy di DB/output.
