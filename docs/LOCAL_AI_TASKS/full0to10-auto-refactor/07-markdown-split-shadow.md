# Markdown split shadow

La lane Markdown split è secondaria rispetto a SQLite FTS5/GPU/tool quality.
È mantenuta come strumento futuro, ma gli output shadow sono quarantinati sotto
`output/validation/...`.

## Pipeline

```text
patch-spec markdown_split
-> dry-run
-> apply shadow in output/validation
-> inspect generated directory
-> future replace-original patch only with explicit confirmation
```

## Quarantine output

Il wrapper usa di default:

```text
output/validation/full0to10_markdown_split_shadow_files/
```

Non deve creare directory `.md.split/` accanto ai sorgenti.

## Cleanup

Se esistono vecchie directory shadow generate accanto ai sorgenti:

```powershell
Get-ChildItem -Recurse -Directory -Filter "*.md.split" |
  Remove-Item -Recurse -Force
```

## Filename hardening

I nomi dei child document sono slug abbreviati e hashati per evitare errori
Windows su heading molto lunghi o caratteri non validi.
