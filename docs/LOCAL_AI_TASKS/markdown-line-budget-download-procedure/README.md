# Markdown line-budget Downloads procedure

## Scopo

I bundle reali restano in `Downloads`. La repo versiona solo la procedura e,
quando eseguita, i file sorgenti/tool effettivamente prodotti.

## Concatenazione

Questa procedura può essere eseguita in catena con:

```text
full0to10_chained_md_budget_repo_quality_patch_bundle
```

## Bundle attesi

```powershell
$Downloads = "$env:USERPROFILE\Downloads"

$Zip01 = Join-Path $Downloads "01_ia_carmine_md_line_budget_tools_patch_bundle.zip"
$Zip02 = Join-Path $Downloads "02_ia_carmine_md_line_budget_apply_bundle.zip"
$Zip03 = Join-Path $Downloads "03_ia_carmine_md_line_budget_all_in_one_bundle.zip"
```

## Non versionare

```text
Downloads/*.zip
output/**
```
