# Operational guardrails

Questo loop chiude guardrail operativi P1/P2.

## Wrapper exit code

I wrapper devono controllare `$LASTEXITCODE` prima di stampare `[OK]`.

## Markdown shadow

Lo shadow split deve restare sotto:

```text
output/validation
```

Non deve scrivere `.md.split/` accanto ai sorgenti.

## Startup check

`startup_check.py` può restare diagnostic-only. Per uso bloccante si usa:

```text
Tools/workflow/run_full0to10_startup_check_guard.ps1 -StrictExit
```

## Generated artifacts

Prima del commit va controllato che non siano presenti:

- `indexAI/code_chunks/**`;
- `indexAI/project_code_chunks/**`;
- `docs/LOCAL_VALIDATION_EVIDENCE/**`;
- `*.sqlite`;
- `*.db`.
