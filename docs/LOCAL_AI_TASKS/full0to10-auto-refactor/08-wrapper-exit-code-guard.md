# Auto-refactor wrapper exit-code guard

Il wrapper dell'applier controllato non deve mascherare errori Python.

## Fix

`run_full0to10_auto_refactor_apply.ps1` ora:

- costruisce gli argomenti;
- esegue Python;
- salva `$LASTEXITCODE`;
- lancia `throw` se diverso da zero;
- stampa `[OK]` solo dopo successo.

## Policy

L'applier resta prudente: solo cleanup sicuri possono essere applicati.
