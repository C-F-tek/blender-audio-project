# Markdown line-budget Downloads bundles

## Regola ricorsiva

```text
file Markdown mantenuto <= 400 righe
se supera 400 righe -> directory con README.md e child docs numerati
```

## Uso nel loop

Il prossimo bundle può concatenare i bundle reali da `Downloads` tramite:

```powershell
python .\output\validation\patch_bundles\full0to10_chained_md_budget_repo_quality_patch_bundle\run_patch_bundle.py `
  --chain-download-md-budget `
  --apply-doc-split
```

## Policy

Gli ZIP restano fuori repo. La repo contiene procedura, tool risultanti,
validator e Markdown sorgenti modificati.
