# Operational wrapper guards

Il quality gate deve considerare i wrapper come parte della sicurezza.

## Regole

- nessun `[OK]` se il comando Python fallisce;
- ogni wrapper deve propagare exit code;
- shadow output deve stare sotto `output/validation`;
- startup check strict deve poter fallire quando richiesto.

## Smoke

```text
run_full0to10_workflow_exit_code_guard_smoke.py
run_full0to10_markdown_shadow_guard_smoke.py
check_full0to10_generated_artifact_quarantine.py
```
