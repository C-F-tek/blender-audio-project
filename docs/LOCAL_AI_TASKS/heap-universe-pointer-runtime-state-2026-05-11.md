# Heap universe pointer runtime state — 2026-05-11

## Stato consolidato

Questa nota registra lo stato code-driven dopo la chiusura e il merge della PR #298 `feat(ai): externalize heap launcher profiles` e dopo l'aggiunta dell'orchestratore post-run esterno.

La PR e' stata portata su `master`. Il gate runtime principale resta invariato: la logica nuova e' esterna al gate e opera come profili, adapter post-run, composer lungo, contesto di revisione per la run successiva e orchestratore post-run.

## Vincoli rispettati

Non modificare questi componenti per questa fase:

- `Tools/ai/run_heap_runtime_completeness_gate.py`
- tool call/runtime provider interni del gate
- semantica di pass/fail del gate
- merge policy automatica o deploy

Il nuovo layer opera intorno al gate, non dentro il gate.

## File code-driven coinvolti

### `Tools/ai/heap_runtime_launcher_profiles.json`

Schema corrente: `schema_version = 3`.

Il file espone profili esterni per il runtime heap:

- `fast_external_heap`
- `balanced_external_heap`
- `deep_external_heap`
- `strict_startup_external_heap`
- `dry_packaging_external_heap`

Gruppi configurabili:

- `runtime`
- `startup_context`
- `revision_context`
- `heap_universe`
- `hardware`
- `outputs`

Campi importanti:

- `context_document_count`
- `context_document_preview_chars`
- `semantic_code_chunk_limit`
- `semantic_code_chunk_preview_chars`
- `semantic_evidence_chunk_limit`
- `memory_search_limit`
- `tool_catalog_limit`
- `revision_context_mode`
- `revision_context_max_tasks`
- `universe_roles`
- `universe_max_steps`
- `block_pointer_protocol`
- `max_blocks_per_step`
- `max_block_chars`
- `max_revision_depth`
- `allow_backrefinement`
- `allow_forward_pointers`
- `require_resume_pointer`
- `require_refines_pointer`

I profili operativi usano `revision_context_mode = auto_latest`.

Il profilo `dry_packaging_external_heap` usa `revision_context_mode = off`, per evitare che un dry-run di packaging consumi automaticamente task di revisione precedenti.

### `Tools/ai/build_heap_runtime_launcher_command.py`

Questo tool non esegue il runtime heap. Genera comandi PowerShell reviewabili.

Funzioni correnti:

- legge `heap_runtime_launcher_profiles.json`;
- materializza CLI args supportati da `run_heap_runtime_context_closure.py`;
- preserva metadati esterni non ancora CLI-bound;
- cerca il latest `output/validation/heap_context_closure_*/external_heap_revision_context.json` quando il profilo usa `revision_context_mode = auto_latest`;
- inietta un riassunto bounded del revision context direttamente dentro `--request`;
- genera anche i comandi post-run per block pointer manifest e revision context.

Nota architetturale: il feed del revision context avviene nel testo `--request`, non tramite modifica del gate.

### `Tools/ai/build_external_heap_block_pointer_manifest.py`

Produce `external_heap_block_pointer_manifest.json/md` a partire da una run directory.

Modella output persistenti come blocchi e puntatori:

- `previous_block_id`
- `next_block_id`
- `refines_block_id`
- `resume_from_block_id`

Ruoli previsti:

- `gpu1_planner`
- `gpu0_reviewer_refiner`
- `npu_auditor`

Scopo: uscire dal limite della singola finestra token. Le AI possono lavorare su blocchi persistenti, non solo sul testo immediato della risposta provider.

### `Tools/ai/build_external_heap_revision_context.py`

Produce `external_heap_revision_context.json/md` da:

- `external_heap_block_pointer_manifest.json`
- `heap_final_proposal_composer.json`
- `heap_final_causality_normalized.json`

Genera task per la run successiva:

- `gpu1_rewrite_rejected_*`
- `gpu1_propagate_symbols_*`
- `gpu0_parallel_recheck_*`
- `npu_parallel_audit_*`

Semantica:

- GPU1 puo' andare avanti o indietro sui pointer.
- GPU1 puo' propagare import, variabili, funzioni, classi o contratti scoperti in un blocco successivo verso blocchi precedenti compatibili.
- GPU0 puo' rivalutare anche blocchi vecchi in parallelo.
- NPU puo' auditarli in parallelo per guardrail, placeholder, path inventati, source write non dichiarati e ripetizione.
- Il ciclo riparte da `resume_from_block_id`.

Bug corretto durante la validazione locale: la prima estrazione import era troppo permissiva e catturava righe successive. Ora l'estrazione simboli lavora riga per riga.

L'adapter copia anche JSON/MD nella cartella Documents del composer quando `documents_dir` e' disponibile, e aggiorna il manifest download.

### `Tools/ai/compose_external_heap_block_response.py`

Produce `external_heap_primary_long_response.md/json`.

Questo output non sostituisce il vecchio composer: estende il pacchetto del composer esistente.

Comportamento:

- legge pointer manifest, composer JSON e causality JSON;
- ricostruisce una risposta lunga da blocchi persistenti;
- se ci sono blocchi accettati, usa quelli come risposta principale;
- se non ci sono blocchi accettati, puo' includere storia rigettata e blocchi peer per debug;
- copia MD/JSON nella cartella Documents del composer quando possibile;
- aggiorna `DOWNLOADS.txt` del composer.

### `Tools/ai/normalize_heap_final_causality.py`

Separa due concetti che prima potevano essere ambigui:

- `causal_chain_status` / `causal_chain_passed`
- `product_acceptance_status` / `product_acceptance_passed`

Caso valido osservato:

- catena causale passata;
- prodotto bloccato;
- tutte le proposal rigettate;
- nessun falso positivo.

### `Tools/ai/run_external_heap_postrun_package.py`

Nuovo orchestratore esterno post-run.

Non sostituisce il vecchio composer e non modifica il gate. Automatizza la sequenza esterna per una run `heap_context_closure_*` esistente:

1. `normalize_heap_final_causality.py`
2. `build_external_heap_block_pointer_manifest.py`
3. `compose_external_heap_block_response.py`
4. `build_external_heap_revision_context.py`

Output principale:

- `external_heap_postrun_package.json`

Campi/garanzie:

- `provider_execution_performed = false`
- `patch_application_performed = false`
- `source_writes_performed = false`
- fail-fast se uno step esterno non passa;
- default su latest `output/validation/heap_context_closure_*` se `--run-dir` non viene passato.

## Flusso operativo attuale

1. Generare comando launcher da profilo:

```powershell
python .\Tools\ai\build_heap_runtime_launcher_command.py `
  --repo-root . `
  --profile balanced_external_heap `
  --include-block-pointer-command `
  --include-revision-context-command `
  --output .\output\validation\heap_launcher_command_balanced.json
```

2. Il command builder, se presente un revision context precedente, lo inietta in `--request`.

3. Eseguire il comando generato.

4. Post-run consigliato tramite orchestratore:

```powershell
python .\Tools\ai\run_external_heap_postrun_package.py `
  --repo-root . `
  --include-rejected-history `
  --include-peer-blocks
```

5. La run successiva consuma il revision context precedente tramite profilo `auto_latest`.

## Stato logico dell'universo heap

L'universo heap e' ora modellato come:

```text
request corrente
→ startup preload/context/memory/tool/docs
→ GPU1 planner produce proposal blocks
→ GPU0 reviewer/refiner rivaluta anche pointer vecchi
→ NPU auditor audita anche pointer vecchi
→ vecchio composer produce package base
→ external postrun package normalizza causality
→ external postrun package genera block pointer manifest
→ external postrun package ricostruisce output file-based lungo
→ external postrun package genera revision context per run successiva
→ nuova run consuma revision context nel request
```

Questa architettura permette a GPU1 di generare output molto lungo in blocchi. Se durante un blocco successivo emergono nuovi import, variabili o contratti, GPU1 puo' creare task di propagazione verso blocchi precedenti, farli rivalutare in parallelo da GPU0/NPU e poi riprendere dal cursore forward corretto.

## Bug o limiti residui annotati

### 1. Feed revision context nel launcher core non applicato direttamente

Tentativo diretto di patchare `run_heap_runtime_context_closure.py` e' stato evitato/bloccato durante la modifica remota per payload troppo grande. La soluzione applicata e' piu' sicura e coerente con il vincolo di non toccare gate/tool call: il revision context viene iniettato dal command builder nel testo `--request`.

Impatto: funzionale, ma il launcher core non espone ancora flag dedicati tipo `--revision-context`.

Possibile patch futura, se necessaria:

```text
feat(ai): add native revision-context argument to heap closure launcher
```

Target potenziale:

- `Tools/ai/run_heap_runtime_context_closure.py`

Vincolo: non toccare `run_heap_runtime_completeness_gate.py`.

### 2. Alcuni campi profilo sono metadati esterni, non ancora CLI-bound

Esempi:

- `context_document_count`
- `semantic_code_chunk_limit`
- `memory_search_limit`
- `tool_catalog_limit`

Questi campi sono preservati in `external_metadata` dal command builder ma non tutti hanno ancora una corrispondenza CLI diretta nel launcher o nei tool di preload.

Possibile patch futura:

```text
feat(ai): bind external profile context budgets into startup preload selectors
```

Target potenziali:

- `Tools/ai/build_heap_runtime_launcher_command.py`
- `Tools/ai/prepare_heap_context_memory_reload.py`

### 3. Orchestratore post-run non e' ancora integrato automaticamente nel launcher

La sequenza post-run e' ora automatizzabile con `run_external_heap_postrun_package.py`, ma il launcher non la invoca automaticamente.

Possibile patch futura:

```text
feat(ai): let heap closure launcher optionally run external postrun package
```

Target potenziale:

- `Tools/ai/run_heap_runtime_context_closure.py`

Vincolo: mantenere opzionale e non sostituire il vecchio composer.

## Comandi locali consigliati dopo sync master

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git checkout master
git pull --ff-only origin master

$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy -m py_compile `
  .\Tools\ai\build_heap_runtime_launcher_command.py `
  .\Tools\ai\normalize_heap_final_causality.py `
  .\Tools\ai\build_external_heap_block_pointer_manifest.py `
  .\Tools\ai\compose_external_heap_block_response.py `
  .\Tools\ai\build_external_heap_revision_context.py `
  .\Tools\ai\run_external_heap_postrun_package.py
```

Generare comando run:

```powershell
& $RepoPy .\Tools\ai\build_heap_runtime_launcher_command.py `
  --repo-root . `
  --profile balanced_external_heap `
  --include-block-pointer-command `
  --include-revision-context-command `
  --output .\output\validation\heap_launcher_command_balanced.json
```

Controllare se il revision context precedente e' stato caricato:

```powershell
$Cmd = Get-Content .\output\validation\heap_launcher_command_balanced.json -Raw -Encoding UTF8 | ConvertFrom-Json

$Cmd |
  Select-Object `
    schema_version,
    profile_name,
    revision_context_loaded,
    revision_context_path,
    revision_context_task_count |
  Format-List
```

Eseguire post-run package dopo la run:

```powershell
& $RepoPy .\Tools\ai\run_external_heap_postrun_package.py `
  --repo-root . `
  --include-rejected-history `
  --include-peer-blocks
```

## Decisione operativa

La fase attuale e' chiusa positivamente:

- PR #298 mergeata su `master`;
- gate invariato;
- tool call interni del gate invariati;
- profili esterni attivi;
- pointer manifest attivo;
- long response integrata nel package Documents del composer;
- revision context generato e consumabile dalla run successiva;
- bug estrazione import corretto;
- sequenza post-run esterna automatizzabile tramite orchestratore dedicato.

Prossima priorita': bindare i budget profilo non ancora CLI-bound o rendere opzionale il post-run package direttamente dal launcher, a seconda della prossima evidenza runtime.
