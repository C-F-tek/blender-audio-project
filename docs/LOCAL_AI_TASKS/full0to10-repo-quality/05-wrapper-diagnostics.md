# Wrapper diagnostics

Il core Python repo-quality può passare anche se il wrapper precedente non
mostrava abbastanza dettagli.

## Fix

`run_full0to10_repo_quality_packet.ps1` ora mostra:

- path JSON reale;
- path output file;
- stdout/stderr Python;
- `passed`;
- `errors`;
- `warnings`;
- input mancanti;
- manifest user output.

## DiagnosticsOnly

`-DiagnosticsOnly` permette di raccogliere packet diagnostico senza bloccare il
workflow quando il JSON è stato prodotto ma `passed=false`.

## Regola

Una failure strutturale deve restare errore. Un finding di qualità deve essere
leggibile nel packet, non nascosto dietro un exit code generico.
