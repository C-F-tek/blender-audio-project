# Markdown line-budget Downloads bundles

## Regola ricorsiva

```text
file Markdown mantenuto <= 400 righe
se supera 400 righe -> directory con README.md e child docs numerati
```

## Uso nel loop

I bundle locali in `Downloads` o `output/validation/patch_bundles/**` sono transienti e non sono documentati come comandi tracciati.

Procedura corretta:

```text
1. ricreare il bundle da strumenti tracciati aggiornati;
2. applicarlo solo dopo review manuale;
3. non committare output/validation/patch_bundles/**;
4. validare i file sorgente/docs modificati con git diff --check e validator pertinenti.
```

## Policy

Gli ZIP restano fuori repo. La repo contiene procedura, tool risultanti,
validator e Markdown sorgenti modificati.
