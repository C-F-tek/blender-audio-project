# Problems and hygiene candidates — 2026-05-10

## Scopo

Questo file raccoglie candidati per l'igiene di domani dopo la stabilizzazione della run unica real product. Non è un piano di patch automatico e non autorizza delete distruttivi. Serve a scegliere interventi safe, code-driven e validabili.

## Stato attuale da preservare

- una entrata: `Tools/workflow/run_unified_real_product_pr.ps1`;
- centro dinamico: heap/exchange dentro `run_unified_local_ai_refactor.ps1`;
- peer runtime: GPU1/Ollama advisory, GPU0 OpenVINO workload, NPU micro peer;
- evidenza correlata: runtime evidence correlation post final chain contract;
- uscita: generated patch specs, apply report, `prepare_review_pr.py`, draft PR finale;
- no merge automatico;
- no output/index/db/renders nel prodotto finale.

## Candidati P0 — blocchi prodotto reale

### P0.1 — Prodotto generato ancora metadata-only

Sintomo:

- `operation_count=0`;
- `changed_count=0`;
- `metadata-only draft operation has no concrete replacements`;
- fallback `P-NEXT-NPU-OBSERVABILITY`.

Stato dopo #295/#296:

- metadata-only con `--apply` ora fallisce;
- proposal builder ora può leggere evidenza runtime current-stamp;
- patch-spec builder ora può trasportare `concrete_operations`.

Candidato igiene:

- verificare che il primo run post-sync produca `P-RUNTIME-PEER-EVIDENCE-FEED`;
- se torna `P-NEXT-NPU-OBSERVABILITY`, ispezionare `runtime_report_paths` dentro `repository_change_proposals*.json`;
- aggiungere report mancante alla discovery solo se è current-stamp e non generico.

Validazione:

- `python .\Tools\validation\run_repository_change_proposals_runtime_evidence_smoke.py --repo-root .`;
- `python .\Tools\validation\run_generated_patch_specs_empty_product_smoke.py --repo-root .`;
- `git diff --check`.

### P0.2 — GPU1/Ollama non consuma abbastanza heap evidence

Sintomo:

- GPU0 e NPU producono report, ma la proposal resta generica;
- `runtime_peer_evidence_summary.needs_concrete_generated_product` non viene visto;
- la proposta non contiene `concrete_operations`.

Candidato igiene:

- controllare `build_repository_change_proposals.py` discovery e filtro stamp;
- assicurare che `--runtime-report-stamp` sia allineato allo stamp reale della run;
- verificare che il launcher passi basename/stamp coerenti a proposal e patch-spec lanes.

Stop condition:

- non inventare patch concrete senza evidenza current-stamp;
- non leggere report stale solo perché sono gli ultimi modificati.

## Candidati P1 — affidabilità run unica

### P1.1 — Dirty tree attribution nel wrapper

Sintomo già visto:

- messaggio falso `Generated process gate task dirtied the repository`;
- in realtà erano sporchi `indexAI/code_chunks/**` o `docs/LOCAL_VALIDATION_EVIDENCE/**` da run precedente.

Candidato igiene:

- nel wrapper confrontare `git status --short` prima e dopo la creazione del task;
- fallire solo sul delta causato dal task;
- riportare separatamente `pre_existing_dirty_tree`.

Validazione:

- smoke con dirty preesistente safe;
- smoke con task sotto path non ignorato che deve fallire.

### P1.2 — Evidence fuori da output ancora troppo facile da sporcare

Sintomo:

- file `docs/LOCAL_VALIDATION_EVIDENCE/<stamp>_official_adapter_evidence.*` untracked dopo run;
- artifact evidence possono sporcare working tree prima della run successiva.

Candidato igiene:

- chiarire quali evidence sotto docs sono intenzionalmente versionabili e quali sono runtime output;
- se runtime, spostarli sotto `output/validation` o `output/local_ai_runs`;
- se versionabili, generarli solo in PR dedicate e non durante process-gate real run.

Stop condition:

- non cancellare evidence storica senza review;
- non cambiare policy artifact path senza validator.

### P1.3 — `indexAI/code_chunks/**` tracked rigenerato durante run

Sintomo:

- `semantic_code_chunks.json` e manifest risultano modificati;
- la run reale richiede working tree pulito.

Candidato igiene:

- decidere se questi file sono source/versioned index o runtime generated index;
- se runtime generated, produrre sotto `output/` o path ignored;
- se versioned, rigenerarli solo con comando esplicito di reindex e PR separata.

Stop condition:

- non rimuovere tracking senza decisione esplicita;
- non committare update index generato dentro PR prodotto runtime.

## Candidati P2 — osservabilità peer

### P2.1 — GPU0 workload osservabile ma breve

Sintomo:

- attività visibile ma troppo corta per diagnosi manuale;
- report passa ma non dà abbastanza campioni.

Candidato igiene:

- esporre parametri workload GPU0 nel wrapper se non già propagati;
- aggiungere nel report conteggi iterazioni, durata effettiva, device target e fallback path.

Validazione:

- report deve contenere durata >= soglia;
- se OpenVINO non vede GPU0, fallire esplicitamente.

### P2.2 — NPU micro peer ancora diagnostic-only

Sintomo:

- NPU parte all'inizio ma non partecipa come compute lane;
- report dichiara `npu_device_execution_performed=false`.

Candidato igiene:

- mantenere classificazione onesta;
- separare chiaramente `npu_probe`, `npu_decode_smoke`, `npu_micro_peer_context`, `npu_provider_compute_candidate`;
- non promuovere NPU a compute finché OpenVINO GenAI/NPU generation non produce report stabile.

Stop condition:

- nessuna falsa promozione a provider compute;
- nessuna modifica model/provider settings in PR di docs/igiene.

### P2.3 — Broker/tool telemetry e memoria condivisa

Sintomo:

- heap/exchange dichiara broker/memory, ma la proposal può non dimostrare quali report siano stati letti;
- il debug è disperso tra output/validation e output/local_ai_runs.

Candidato igiene:

- aggiungere a proposal e final manifest una lista compatta `runtime_report_paths` già letta;
- aggiungere `report_kinds_seen` con conteggi;
- correlare con `runtime_evidence_correlation`.

## Candidati P3 — documentazione e line budget

### P3.1 — `Tools/workflow/README.md` è sovradimensionato

Sintomo:

- contiene runbook, policy, contratti, appendici storiche e sezioni datate;
- supera la soglia preferita di runbook attivo.

Candidato igiene:

- mantenere in README solo index + operator routing;
- spostare dettagli in `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md` e documenti dedicati;
- non fare split cieco: preservare anchor usati dagli smoke.

Validazione:

- smoke che cercano anchor README devono passare;
- link doc aggiornati.

### P3.2 — Nomi storici Full0To10 vs run unica

Sintomo:

- alcuni validator e file mantengono alias legacy `full0to10_product_pr_chain_smoke`;
- la semantica reale ora è `single_dynamic_heap_exchange_run`.

Candidato igiene:

- documentare alias legacy come compatibilità;
- non rinominare tutto in massa;
- aggiungere solo campi `legacy_alias_absorbed_by_unified_run` quando serve.

### P3.3 — Error handling PowerShell

Sintomo:

- ci sono ancora `throw` PowerShell che producono errori non strutturati;
- esiste già structured wrapper error path.

Candidato igiene:

- sostituire progressivamente throw non gestiti con funzione/contratto error report esistente;
- preservare exit code non-zero;
- emettere JSON con `kind`, `errors`, `warnings`, `provider_execution_performed`, `patch_application_performed`, `source_writes_performed`.

## Ordine consigliato domani

1. sync master e validazioni smoke #295/#296;
2. una run reale process-gate corta ma completa;
3. se fallisce, classificare in P0.1/P0.2 prima di toccare altro;
4. se produce PR, ispezionare touched files e line counts;
5. solo dopo, igiene P1 su dirty-tree/artifact paths;
6. infine docs/README split se necessario.

## Comandi rapidi di triage

~~~powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path

Get-ChildItem .\output\validation -Filter "*003859*.json" | Select-Object Name,Length,LastWriteTime
Get-ChildItem .\output\patch_specs -Recurse -Filter "*.json" | Select-Object FullName,Length,LastWriteTime

& $RepoPy .\Tools\validation\run_repository_change_proposals_runtime_evidence_smoke.py --repo-root .
& $RepoPy .\Tools\validation\run_generated_patch_specs_empty_product_smoke.py --repo-root .

git status --short
git diff --check
~~~
