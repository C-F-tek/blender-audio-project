# Repo Patch Runner

Questo tool applica modifiche mirate a file del repository usando uno spec JSON.

È pensato per evitare di riscrivere file molto grandi quando serve cambiare solo pochi blocchi.
Nelle prossime chat si può preparare solo un JSON con le operazioni richieste, verificarlo in `--dry-run` e poi applicarlo con `--write`.

## Uso

Dalla root del repository:

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_spec.json --dry-run
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\patch_spec.json --write --show-diff
```

## Caratteristiche

- Legge file UTF-8 e rimuove un eventuale BOM iniziale.
- Accetta solo percorsi relativi alla root del repository.
- Crea backup in `.repo_patch_backups/` prima di scrivere, salvo `--no-backup`.
- Stampa numero righe prima/dopo.
- Supporta sostituzioni esatte, regex, insert prima/dopo anchor.
- Valida stringhe obbligatorie o vietate prima e dopo la patch.

## Spec JSON minimo

```json
{
  "version": 1,
  "description": "Esempio sostituzione sicura",
  "operations": [
    {
      "path": "Scripting/example.py",
      "replacements": [
        {
          "type": "exact",
          "old": "vecchio testo",
          "new": "nuovo testo",
          "count": 1
        }
      ],
      "require_contains_after": ["nuovo testo"],
      "forbid_contains_after": ["vecchio testo"]
    }
  ]
}
```

## Tipi di replacement

### exact

```json
{
  "type": "exact",
  "old": "testo vecchio",
  "new": "testo nuovo",
  "count": 1
}
```

### regex

```json
{
  "type": "regex",
  "pattern": "foo\\((.*?)\\)",
  "new": "bar(\\1)",
  "count": 1,
  "flags": ["MULTILINE", "DOTALL"]
}
```

### insert_after

```json
{
  "type": "insert_after",
  "anchor": "riga ancora",
  "insert": "\nnuova riga",
  "count": 1
}
```

### insert_before

```json
{
  "type": "insert_before",
  "anchor": "riga ancora",
  "insert": "nuova riga\n",
  "count": 1
}
```

## Esempio operativo

```powershell
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\Tools\repo_patch_runner\example_fix_blender_51_musgrave.json --dry-run
python .\Tools\repo_patch_runner\apply_repo_mods.py --spec .\Tools\repo_patch_runner\example_fix_blender_51_musgrave.json --write --show-diff
```

Poi:

```powershell
git status
git add <file-modificati>
git commit -m "Messaggio commit"
git push origin master
```
