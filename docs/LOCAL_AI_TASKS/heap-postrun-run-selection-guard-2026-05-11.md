# Heap post-run run-selection guard — 2026-05-11

## Contesto

Questo documento registra una correzione code-driven applicata al layer esterno heap post-run.

Vincolo operativo confermato: non modificare il formato o il contenuto dell'output finale generato dall'heap. La risposta completa e le sue parti devono restare visibili come gia' previsto da:

- `external_heap_primary_long_response.md/json`
- `external_heap_block_pointer_manifest.json/md`
- `external_heap_revision_context.json/md`
- package Documents del vecchio composer

La patch non tocca `compose_external_heap_block_response.py`, non cambia il long response e non modifica il gate.

## Bug trovato

File coinvolto:

```text
Tools/ai/run_external_heap_postrun_package.py
```

Il selettore automatico della run usava la directory piu' recente con nome:

```text
output/validation/heap_context_closure_*
```

Questo era troppo permissivo.

Dopo l'introduzione dello smoke `Tools/validation/run_heap_runtime_launcher_command_smoke.py`, puo' esistere una fixture locale:

```text
output/validation/heap_context_closure_smoke_revision_context/external_heap_revision_context.json
```

Questa fixture serve solo per verificare l'injection del revision context nel command builder. Non e' una run heap completa e non contiene:

```text
heap_final_proposal_composer.json
```

Rischio: `run_external_heap_postrun_package.py`, senza `--run-dir`, poteva selezionare la fixture smoke come latest run e fallire per composer mancante.

## Fix applicato

Il selettore latest ora considera solo directory complete:

```text
heap_context_closure_* + heap_final_proposal_composer.json presente
```

Semantica aggiornata:

```text
latest_complete_heap_context_closure_with_composer_json
```

Il report `external_heap_postrun_package.json` usa ora:

```json
"schema_version": 2,
"run_dir_selection_policy": "latest_complete_heap_context_closure_with_composer_json"
```

se `--run-dir` non viene passato.

Se `--run-dir` viene passato esplicitamente, il report usa:

```json
"run_dir_selection_policy": "explicit_run_dir"
```

## Cosa non cambia

Non cambia:

- il vecchio composer;
- il gate;
- i provider;
- i tool call interni;
- la risposta finale lunga;
- le parti del long response;
- i pointer presenti nel manifest;
- il revision context prodotto.

La patch e' solo un guardrail di selezione run per evitare falsi target post-run.

## Comandi locali consigliati

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git checkout master
git pull --ff-only origin master

$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy -m py_compile .\Tools\ai\run_external_heap_postrun_package.py
```

Dopo una run reale heap:

```powershell
& $RepoPy .\Tools\ai\run_external_heap_postrun_package.py `
  --repo-root . `
  --include-rejected-history `
  --include-peer-blocks
```

Controllo:

```powershell
$RunDir = Get-ChildItem .\output\validation -Directory |
  Where-Object { $_.Name -like "heap_context_closure_*" -and (Test-Path (Join-Path $_.FullName "heap_final_proposal_composer.json")) } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

$Post = Get-Content (Join-Path $RunDir.FullName "external_heap_postrun_package.json") -Raw -Encoding UTF8 | ConvertFrom-Json

$Post |
  Select-Object `
    schema_version,
    passed,
    run_dir,
    run_dir_selection_policy,
    long_response_markdown,
    revision_context_json |
  Format-List
```

Atteso:

```text
schema_version           : 2
run_dir_selection_policy : latest_complete_heap_context_closure_with_composer_json
```

## Stato

Fix applicato su `master`.

Prossima verifica utile: eseguire una run reale e osservare il comportamento degli output senza modificare il long response composer.
