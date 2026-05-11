# Heap post-run run-selection guard — 2026-05-11

## Contesto

Questo documento registra correzioni code-driven applicate al layer esterno heap post-run e al command builder.

Vincolo operativo confermato: non modificare il formato o il contenuto dell'output finale generato dall'heap. La risposta completa e le sue parti devono restare visibili come gia' previsto da:

- `external_heap_primary_long_response.md/json`
- `external_heap_block_pointer_manifest.json/md`
- `external_heap_revision_context.json/md`
- package Documents del vecchio composer

Le patch non toccano `compose_external_heap_block_response.py`, non cambiano il long response e non modificano il gate.

## Bug 1 — selezione run post-run troppo permissiva

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

### Fix applicato

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

## Bug 2 — auto-latest revision context del command builder poteva leggere fixture smoke

File coinvolti:

```text
Tools/ai/build_heap_runtime_launcher_command.py
Tools/validation/run_heap_runtime_launcher_command_smoke.py
```

Il command builder usava:

```text
output/validation/heap_context_closure_*/external_heap_revision_context.json
```

per `revision_context_mode = auto_latest`.

Questo aveva lo stesso rischio della post-run chain: una fixture smoke poteva essere trattata come contesto reale della run precedente.

### Fix applicato

`build_heap_runtime_launcher_command.py` ora carica revision context automatico solo da run complete:

```text
heap_context_closure_* + heap_final_proposal_composer.json + external_heap_revision_context.json
```

Il JSON command passa a:

```json
"schema_version": 6,
"revision_context_selection_policy": "latest_complete_heap_context_closure_with_composer_json"
```

quando il profilo usa `revision_context_mode = auto_latest` senza `--revision-context` esplicito.

Lo smoke `run_heap_runtime_launcher_command_smoke.py` e' stato aggiornato: ora passa la fixture con `--revision-context`, quindi testa l'injection esplicita senza dipendere dall'auto-latest. Il report smoke passa a:

```json
"schema_version": 2,
"source_writes_performed": false,
"output_artifact_writes_performed": true
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

Le patch sono solo guardrail di selezione run/revision context per evitare falsi target derivati da fixture locali.

## Comandi locali consigliati

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git checkout master
git pull --ff-only origin master

$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy -m py_compile `
  .\Tools\ai\run_external_heap_postrun_package.py `
  .\Tools\ai\build_heap_runtime_launcher_command.py `
  .\Tools\validation\run_heap_runtime_launcher_command_smoke.py
```

Dopo una run reale heap:

```powershell
& $RepoPy .\Tools\ai\run_external_heap_postrun_package.py `
  --repo-root . `
  --include-rejected-history `
  --include-peer-blocks
```

Controllo post-run:

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

Controllo command builder:

```powershell
& $RepoPy .\Tools\ai\build_heap_runtime_launcher_command.py `
  --repo-root . `
  --profile balanced_external_heap `
  --include-postrun-package-command `
  --output .\output\validation\heap_launcher_command_balanced.json

$Cmd = Get-Content .\output\validation\heap_launcher_command_balanced.json -Raw -Encoding UTF8 | ConvertFrom-Json

$Cmd |
  Select-Object `
    schema_version,
    revision_context_selection_policy,
    revision_context_loaded,
    revision_context_path,
    revision_context_task_count |
  Format-List
```

Atteso:

```text
schema_version : 6
revision_context_selection_policy : latest_complete_heap_context_closure_with_composer_json | off | explicit_revision_context
```

Smoke:

```powershell
& $RepoPy .\Tools\validation\run_heap_runtime_launcher_command_smoke.py `
  --repo-root . `
  --output .\output\validation\heap_runtime_launcher_command_smoke.json `
  --markdown-output .\output\validation\heap_runtime_launcher_command_smoke.md
```

## Stato

Fix applicati su `master`.

Prossima verifica utile: eseguire una run reale e osservare il comportamento degli output senza modificare il long response composer.
