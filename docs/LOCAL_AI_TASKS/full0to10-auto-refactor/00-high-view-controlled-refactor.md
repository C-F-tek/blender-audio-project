# High view controlled refactor

Il refactoring controllato diventa una lane primaria del workflow CarmineLike.

## Pipeline

```text
scan repo
-> classify candidates
-> generate patch-specs
-> dry-run controlled applier
-> inspect report/diff
-> apply allowlisted specs
-> validate
-> commit
```

## Stato corrente

Il primo applier supporta solo cleanup sicuri:

- trailing whitespace;
- final newline.

Questo è intenzionale: prima si stabilizza il contratto, poi si estendono i kind.

## Futuri utilizzi

La stessa architettura potrà supportare:

- split Markdown > 500 righe;
- split codice > 300 righe;
- migrazione di funzioni helper;
- wiring docs/bundle/capability;
- hardening GPU/NPU telemetry contract;
- normalizzazione dei path;
- update automatico di indici/manifest.

Ogni nuovo kind deve entrare come patch separata, con smoke dedicato.
