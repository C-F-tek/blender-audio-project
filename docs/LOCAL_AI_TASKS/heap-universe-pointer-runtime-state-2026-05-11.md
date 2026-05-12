# Heap universe pointer runtime state — 2026-05-11

## Stato consolidato

Questa nota registra lo stato code-driven del layer esterno heap/universe dopo la PR #298 `feat(ai): externalize heap launcher profiles` e le successive patch di bug fixing su pointer contract, post-run package, revision context e launcher command.

Il gate runtime principale resta invariato: la logica nuova opera intorno al gate tramite profili, adapter post-run, composer lungo, block pointer manifest, revision context per la run successiva e command builder.

## Vincoli rispettati

Non modificare questi componenti per questa fase:

- `Tools/ai/run_heap_runtime_completeness_gate.py`
- tool call/runtime provider interni del gate
- semantica di pass/fail del gate
- merge policy automatica o deploy

Il nuovo layer opera intorno al gate, non dentro il gate.

## Profili launcher attuali

Il file `Tools/ai/heap_runtime_launcher_profiles.json` espone solo questi profili:

- `fast_external_heap`
- `balanced_external_heap`
- `deep_external_heap`
- `strict_startup_external_heap`
- `dry_packaging_external_heap`

`full0to10` / `Full0To10` e' nomenclatura storica non piu' registrata nei profili launcher correnti. I comandi operativi devono usare i profili sopra.

## File code-driven coinvolti

### `Tools/ai/heap_runtime_launcher_profiles.json`

Schema corrente: `schema_version = 3`.

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

I profili operativi usano `revision_context_mode = auto_latest`. Il profilo `dry_packaging_external_heap` usa `revision_context_mode = off` per evitare che un dry-run di packaging consumi automaticamente task di revisione precedenti.

### `Tools/ai/build_heap_runtime_launcher_command.py`

Questo tool non esegue il runtime heap. Genera comandi PowerShell reviewabili.

Funzioni correnti:

- legge `heap_runtime_launcher_profiles.json`;
- materializza CLI args supportati da `run_heap_runtime_context_closure.py`;
- preserva metadati esterni non ancora CLI-bound;
- cerca il latest `output/validation/heap_context_closure_*/external_heap_revision_context.json` quando il profilo usa `revision_context_mode = auto_latest`;
- inietta un riassunto bounded del revision context direttamente dentro `--request`;
- espone nel report JSON `revision_context_requires_concrete_rewrite`, `revision_context_priority_next_action` e `revision_context_candidate_applicability_summary`;
- genera il comando run principale;
- genera comandi debug step-by-step per block pointer manifest e revision context;
- genera `postrun_package_command` per `run_external_heap_postrun_package.py`;
- puo' stampare il comando post-run con `--include-postrun-package-command`.

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

Stato attuale:

- i pointer sono product contract per recupero decisioni, navigazione forward/back-refinement/resume e composizione del prodotto finale lungo;
- `provider_execution_performed` e' una guardrail evidence separata e non viene dedotta dalla sola presenza di blocchi;
- se `--max-blocks` limita i blocchi esposti, il manifest conserva `source_block_count`, `all_roles_present` e il provider execution calcolato sui blocchi sorgente completi;
- i proposal block separano `candidate_response_preview`, `diagnostic_preview` e `preview_source`.

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

- GPU1 puo' andare avanti o indietro sui pointer;
- GPU1 puo' propagare import, variabili, funzioni, classi o contratti scoperti in un blocco successivo verso blocchi precedenti compatibili;
- GPU1 non deve propagare simboli se il candidato e' marcato non concreto;
- GPU0 puo' rivalutare anche blocchi vecchi in parallelo;
- NPU puo' auditarli in parallelo per guardrail, placeholder, path inventati, source write non dichiarati, ripetizione e candidate applicability flags;
- il ciclo riparte da `resume_from_block_id`.

Stato attuale:

- conserva `pointer_product_contract`, `pointer_contract_role`, `provider_execution_semantics`, `causal_chain_passed` e `product_acceptance_passed`;
- espone `pointer_block_count`, `source_block_count`, `pointer_max_blocks_applied`, `roles_present`, `all_roles_present`;
- propaga nei task `candidate_response_preview` e `diagnostic_preview` separati;
- classifica candidati non applicabili con `candidate_applicability_flags` e `candidate_concrete_enough`;
- salta la propagazione simboli da candidati non concreti usando `symbol_propagation_skipped` e `symbol_propagation_skip_reason`;
- aggrega a top-level `candidate_applicability_summary`, `requires_concrete_rewrite` e `priority_next_action`.

Esempio stato osservato su run reale:

```text
causal_chain_passed = true
product_acceptance_passed = false
requires_concrete_rewrite = true
priority_next_action = rewrite_non_concrete_candidates
candidate_applicability_summary.non_concrete_candidate_task_count = 3
candidate_applicability_summary.symbol_propagation_skipped_task_count = 3
```

### `Tools/ai/compose_external_heap_block_response.py`

Produce `external_heap_primary_long_response.md/json`.

Questo output non sostituisce il vecchio composer: estende il pacchetto del composer esistente.

Comportamento:

- legge pointer manifest, composer JSON e causality JSON;
- ricostruisce una risposta lunga da blocchi persistenti;
- se ci sono blocchi accettati, usa quelli come risposta principale;
- se non ci sono blocchi accettati, puo' includere storia rigettata e blocchi peer per debug;
- eredita `provider_execution_performed` dal pointer manifest e usa l'ispezione blocchi solo come fallback;
- espone `pointer_max_blocks_applied`, `source_block_count`, `pointer_block_count` e `all_roles_present`;
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

La normalizzazione conserva `provider_execution_performed` quando presente nel composer/report sorgente.

### `Tools/ai/run_external_heap_postrun_package.py`

Orchestratore esterno post-run.

Non sostituisce il vecchio composer e non modifica il gate. Automatizza la sequenza esterna per una run `heap_context_closure_*` esistente:

1. `normalize_heap_final_causality.py`
2. `build_external_heap_block_pointer_manifest.py`
3. `compose_external_heap_block_response.py`
4. `build_external_heap_revision_context.py`

Output principale:

- `external_heap_postrun_package.json`

Campi/garanzie:

- `packaging_complete` indica se la catena esterna ha prodotto gli artifact attesi;
- `hard_failure` distingue fallimento tecnico da prodotto bloccato;
- `provider_execution_performed` aggrega l'evidenza reale da causality, pointer manifest, long response e revision context;
- `product_acceptance_passed` resta separato da `passed`, perche' il package puo' essere valido anche quando il prodotto e' bloccato;
- `patch_application_performed = false`;
- `source_writes_performed = false`;
- default su latest `output/validation/heap_context_closure_*` se `--run-dir` non viene passato.

### `Tools/validation/run_heap_runtime_launcher_command_smoke.py`

Smoke dedicato alla generazione comando heap esterno.

Non esegue provider, non lancia heap runtime e non tocca il gate.

Valida:

- returncode zero del command builder;
- `schema_version = 6` del JSON command;
- profilo `balanced_external_heap`;
- presenza di `postrun_package_command`;
- caricamento di revision context;
- injection del revision context dentro `--request`;
- esposizione di `requires_concrete_rewrite` e `priority_next_action` nel report;
- injection della priorita' rewrite nel request;
- injection di `symbol_propagation_skipped` e `candidate_not_concrete_enough` nel request;
- target corretto per `run_heap_runtime_context_closure.py`;
- target corretto per `run_external_heap_postrun_package.py`.

Lo smoke crea una fixture sotto `output/validation/heap_context_closure_smoke_revision_context/external_heap_revision_context.json`. Questa e' un output artifact, non una source write. Lo smoke marca `source_writes_performed = false` e usa `output_artifact_writes_performed` per indicare la fixture.

## Flusso operativo attuale

1. Generare comando launcher da profilo:

```powershell
python .\Tools\ai\build_heap_runtime_launcher_command.py `
  --repo-root . `
  --profile balanced_external_heap `
  --include-postrun-package-command `
  --output .\output\validation\heap_launcher_command_balanced.json
```

2. Il command builder, se presente un revision context precedente, lo inietta in `--request`.

3. Se il revision context espone `requires_concrete_rewrite=true`, la run deve prima riscrivere i candidati non concreti e non propagare simboli da sketch/stub.

4. Eseguire il comando principale salvato in `command`.

5. Post-run consigliato: eseguire `postrun_package_command` dal JSON generato.

6. Per debug manuale restano disponibili anche `block_pointer_command` e `revision_context_command`.

7. La run successiva consuma il revision context precedente tramite profilo `auto_latest`.

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

Questa architettura permette a GPU1 di generare output lungo in blocchi persistenti. Se durante un blocco successivo emergono nuovi import, variabili o contratti, GPU1 puo' creare task di propagazione verso blocchi precedenti, farli rivalutare in parallelo da GPU0/NPU e poi riprendere dal cursore forward corretto. Se il blocco e' uno sketch/stub non concreto, il revision context blocca la propagazione simboli e forza `rewrite_non_concrete_candidates`.

## Bug o limiti residui annotati

### 1. Feed revision context nel launcher core non applicato direttamente

Tentativo diretto di patchare `run_heap_runtime_context_closure.py` e' stato evitato/bloccato durante modifica remota per payload troppo grande. La soluzione applicata e' piu' sicura e coerente con il vincolo di non toccare gate/tool call: il revision context viene iniettato dal command builder nel testo `--request`.

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

### 3. Post-run package non e' ancora invocato automaticamente dal launcher core

La sequenza post-run e' ora automatizzabile con `run_external_heap_postrun_package.py` e il command builder genera `postrun_package_command`, ma `run_heap_runtime_context_closure.py` non lo invoca automaticamente.

Possibile patch futura:

```text
feat(ai): let heap closure launcher optionally run external postrun package
```

Target potenziale:

- `Tools/ai/run_heap_runtime_context_closure.py`

Vincolo: mantenere opzionale e non sostituire il vecchio composer.

### 4. Il prodotto resta bloccato finche' GPU1 produce sketch generici

La run reale validata ha catena causale e provider execution OK, ma `product_acceptance_passed=false` perche' i proposal chunk sono non concreti. Il prossimo ciclo deve consumare `priority_next_action=rewrite_non_concrete_candidates` e produrre proposal con:

- file repo-relative reali;
- funzioni/classi esistenti;
- diff o operazioni concrete;
- comandi di validazione esistenti;
- nessun placeholder/stub;
- nessuna propagazione simboli da codice non concreto.

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
  .\Tools\ai\run_external_heap_postrun_package.py `
  .\Tools\validation\run_heap_runtime_launcher_command_smoke.py
```

Generare comando run + post-run:

```powershell
& $RepoPy .\Tools\ai\build_heap_runtime_launcher_command.py `
  --repo-root . `
  --profile balanced_external_heap `
  --include-postrun-package-command `
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
    revision_context_task_count,
    revision_context_requires_concrete_rewrite,
    revision_context_priority_next_action |
  Format-List

$Cmd.revision_context_candidate_applicability_summary.flag_counts | Format-List
```

Eseguire run e post-run:

```powershell
Invoke-Expression $Cmd.command
Invoke-Expression $Cmd.postrun_package_command
```

Eseguire smoke command builder:

```powershell
& $RepoPy .\Tools\validation\run_heap_runtime_launcher_command_smoke.py `
  --repo-root . `
  --output .\output\validation\heap_runtime_launcher_command_smoke.json `
  --markdown-output .\output\validation\heap_runtime_launcher_command_smoke.md
```

## Decisione operativa

La fase attuale e' coerente:

- gate invariato;
- tool call interni del gate invariati;
- profili esterni attivi;
- pointer manifest attivo come product contract, non sola diagnostica;
- provider execution preservato lungo causality, pointer, long response, revision context e post-run;
- long response integrata nel package Documents del composer;
- revision context generato e consumabile dalla run successiva;
- candidate response e diagnostic preview separati;
- candidati non concreti marcati e aggregati;
- propagazione simboli bloccata da sketch/stub;
- command builder inietta rewrite priority nel request;
- sequenza post-run esterna automatizzabile tramite orchestratore dedicato;
- command builder produce `postrun_package_command`;
- smoke command builder aggiornato a schema 6 e rewrite priority.

Prossima priorita': eseguire un nuovo ciclo con profilo `balanced_external_heap` o `deep_external_heap` e verificare se GPU1 produce almeno una proposta concreta applicabile. Se continua a produrre sketch, il bug successivo e' nel prompt/contratto del gate o nella trasformazione di `rewrite_non_concrete_candidates` in vincoli hard per la proposta.
