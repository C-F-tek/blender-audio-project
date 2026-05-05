# Markdown split shadow

La lane Markdown split introduce refactoring documentale non distruttivo.

## Pipeline

```text
patch-spec markdown_split
-> dry-run
-> apply shadow
-> inspect generated directory
-> future replace-original patch
```

## Shadow output

Per `docs/example.md` viene creata:

```text
docs/example.md.split/
  README.md
  01-*.md
  02-*.md
```

Il file originale resta presente.

## Filename hardening

I nomi dei child document sono slug abbreviati e hashati per evitare errori
Windows su heading molto lunghi o caratteri non validi.

## Wrapper behavior

`run_full0to10_markdown_split_shadow.ps1` fallisce se il processo Python ritorna
codice non-zero. Non deve stampare `[OK]` dopo un errore applicativo.

## Perché non replace diretto

Sostituire `example.md` con directory `example.md/` richiede delete/rename del file
originale. Questo deve restare fuori dal primo applier e richiedere conferma
esplicita in una patch futura.
