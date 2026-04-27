# Patch specs

Questa cartella contiene gli spec JSON usati da `Tools/repo_patch_runner/apply_repo_mods.py`.

## Flusso automatico GitHub Actions

1. Crea o committa uno spec JSON in:

```text
patch_specs/inbox/<nome_patch>.json
```

2. La GitHub Action `.github/workflows/apply_repo_mods.yml` esegue:

```text
python Tools/repo_patch_runner/apply_repo_mods.py --spec <spec> --dry-run
python Tools/repo_patch_runner/apply_repo_mods.py --spec <spec> --write --no-backup --show-diff
```

3. Se la patch riesce:

- modifica i file richiesti;
- sposta lo spec in `patch_specs/applied/`;
- crea un commit automatico `Apply repo patch specs`.

## Convenzione

- `inbox/`: spec JSON da applicare.
- `applied/`: spec JSON già applicati dalla Action.

## Sicurezza operativa

Il runner accetta solo percorsi relativi alla root del repository e valida le stringhe attese prima/dopo la patch.
