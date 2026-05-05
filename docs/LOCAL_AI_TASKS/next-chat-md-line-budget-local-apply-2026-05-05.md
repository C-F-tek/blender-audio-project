# IA-Carmine — Next bundle MD — Markdown line budget local continuation

Repository: `C-F-tek/blender-audio-project`  
Branch operativa consigliata: `codex/unified-local-ai-refactor-launcher` oppure branch locale dedicata derivata da questa  
Data: 2026-05-05  
Scopo: continuare localmente dopo il download dei bundle ZIP per applicare una policy ricorsiva sui Markdown: file `.md` attivi non oltre 400 righe; oltre soglia diventano cartelle con parti Markdown.

## 1. Contesto operativo

Questo bundle non esegue modifiche da solo. È un handoff Markdown operativo.

Hai già scaricato in `Downloads`:

```text
01_ia_carmine_md_line_budget_tools_patch_bundle.zip
02_ia_carmine_md_line_budget_apply_bundle.zip
03_ia_carmine_md_line_budget_all_in_one_bundle.zip
```

I primi due sono il percorso consigliato:

```text
01 = installa tool e validator
02 = usa i tool per dry-run/apply dello split ricorsivo
03 = alternativa all-in-one
```

## 2. Guardrail obbligatori

Non fare:

```text
git add .
git add output
git add .\output
commit di output/**
commit di renders/**
commit di *.db / *.sqlite
commit di indexAI/code_chunks/**
commit di indexAI/project_code_chunks/**
merge su master
force-push
rewrite history
delete distruttivi
deploy
Blender runtime
FFmpeg runtime
provider reali non richiesti
```

Consentito:

```text
branch dedicato
patch locale idempotente
dry-run
apply esplicito con flag
validator locali
commit mirato
PR
```

## 3. Preparazione locale

Apri PowerShell nella repo:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git status --short
```

Se vuoi lavorare su branch dedicato:

```powershell
git fetch origin
git switch codex/unified-local-ai-refactor-launcher
git pull --ff-only origin codex/unified-local-ai-refactor-launcher
git switch -c codex/md-line-budget-recursive-split
git status --short
```

Se il branch esiste già:

```powershell
git switch codex/md-line-budget-recursive-split
git status --short
```

## 4. Path ZIP in Downloads

```powershell
$Downloads = "$env:USERPROFILE\Downloads"

$Zip01 = Join-Path $Downloads "01_ia_carmine_md_line_budget_tools_patch_bundle.zip"
$Zip02 = Join-Path $Downloads "02_ia_carmine_md_line_budget_apply_bundle.zip"
$Zip03 = Join-Path $Downloads "03_ia_carmine_md_line_budget_all_in_one_bundle.zip"

Test-Path $Zip01
Test-Path $Zip02
Test-Path $Zip03
```

Tutti devono restituire `True`.

## 5. Step 1 — installa tool e validator

```powershell
$Dest01 = ".\output\validation\patch_bundles\01_md_line_budget_tools"
Expand-Archive $Zip01 -DestinationPath $Dest01 -Force
python "$Dest01\run_patch_bundle.py"
```

Validazione immediata:

```powershell
python -m py_compile `
  .\Tools\docs\split_large_markdown.py `
  .\Tools\validation\check_markdown_line_limits.py

python .\Tools\docs\split_large_markdown.py --repo-root . --max-lines 400

python .\Tools\validation\check_markdown_line_limits.py --repo-root . --max-lines 400
```

Atteso:

```text
dry-run eseguito
nessun commit automatico
nuovi tool presenti
report eventuali sotto output/validation/**
```

## 6. Step 2 — dry-run dello split

```powershell
$Dest02 = ".\output\validation\patch_bundles\02_md_line_budget_apply"
Expand-Archive $Zip02 -DestinationPath $Dest02 -Force
python "$Dest02\run_patch_bundle.py"
```

Questo deve solo mostrare cosa verrebbe modificato.

## 7. Step 3 — apply reale dello split

Esegui solo se il dry-run è coerente:

```powershell
python "$Dest02\run_patch_bundle.py" --apply-doc-split
```

Poi valida:

```powershell
python .\Tools\validation\check_markdown_line_limits.py --repo-root . --max-lines 400
git diff --check
git status --short
```

## 8. Modalità alternativa all-in-one

Usala solo se preferisci un unico ZIP:

```powershell
$Dest03 = ".\output\validation\patch_bundles\03_md_line_budget_all_in_one"
Expand-Archive $Zip03 -DestinationPath $Dest03 -Force
python "$Dest03\run_patch_bundle.py"
python "$Dest03\run_patch_bundle.py" --apply-doc-split
```

## 9. File attesi installati dal bundle 01

```text
Tools/docs/split_large_markdown.py
Tools/docs/README.md
Tools/validation/check_markdown_line_limits.py
docs/LOCAL_AI_TASKS/markdown-line-budget-policy.md
```

Tutti i Markdown aggiunti dal bundle sono sotto 400 righe.

## 10. Cosa controllare dopo apply

Elenco modifiche:

```powershell
git diff --name-only
git status --short
```

Controllo linee dei Markdown modificati:

```powershell
git diff --name-only |
  Where-Object { $_ -like "*.md" } |
  ForEach-Object {
    [PSCustomObject]@{
      File = $_
      Lines = (Get-Content $_ | Measure-Object -Line).Lines
    }
  } |
  Sort-Object Lines -Descending |
  Format-Table -AutoSize
```

Stop se un Markdown attivo supera 400 righe.

## 11. Git add mirato

Aggiungi i tool installati:

```powershell
git add `
  .\Tools\docs\split_large_markdown.py `
  .\Tools\docs\README.md `
  .\Tools\validation\check_markdown_line_limits.py `
  .\docs\LOCAL_AI_TASKS\markdown-line-budget-policy.md
```

Aggiungi i Markdown split/modificati solo dopo verifica:

```powershell
git diff --name-only
```

Non aggiungere:

```text
output/**
docs/LOCAL_VALIDATION_EVIDENCE/**
renders/**
indexAI/**
*.db
*.sqlite
```

## 12. Commit e push

```powershell
git diff --cached --name-only
git commit -m "docs(ai): enforce markdown line budget with recursive split tooling"
git push -u origin codex/md-line-budget-recursive-split
```

## 13. PR body suggerito

```markdown
## Summary

Adds local Markdown line-budget tooling and applies recursive Markdown split policy:

- active Markdown target: max 400 lines;
- large Markdown files become short stubs plus sibling folders containing split parts;
- split is recursive;
- runtime outputs remain local and uncommitted;
- validator checks active Markdown line limits.

## Guardrails

- No `output/**` committed.
- No SQLite DB committed.
- No Blender runtime.
- No FFmpeg runtime.
- No provider execution.
- No automatic Git operations from the bundle.

## Validation

```powershell
python -m py_compile `
  .\Tools\docs\split_large_markdown.py `
  .\Tools\validation\check_markdown_line_limits.py

python .\Tools\validation\check_markdown_line_limits.py --repo-root . --max-lines 400
git diff --check
git status --short
```
```

## 14. Stop conditions

Blocca e non committare se:

```text
git diff --check fallisce
check_markdown_line_limits fallisce
output/** appare nello staging
docs/LOCAL_VALIDATION_EVIDENCE/** appare nello staging senza richiesta esplicita
split modifica file non attesi
file MD attivo resta sopra 400 righe
```

## 15. Nota per la prossima chat

Dopo la PR, passare alla prossima fase:

```text
1. controllare riduzione rumore Markdown;
2. rilanciare repository consistency;
3. verificare che source docs e generated/evidence docs siano separati;
4. aggiornare docs map solo se necessario;
5. non applicare patch automatiche sui finding massivi.
```
