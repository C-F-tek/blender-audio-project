# IA-Carmine — Handoff prossima chat — Heap blackboard runtime

Data: 2026-05-10
Repository: `C-F-tek/blender-audio-project`
Branch operativa: `master`
Modalita': lavoro locale/GitHub, repository privata, single-owner.

## Regole operative permanenti

- Non fare merge, force-push, rewrite history, deploy, modifiche a secret/permission/billing/visibility senza comando esplicito.
- Non committare `output/**`, `renders/**`, `*.db`, `*.sqlite`, `indexAI/code_chunks/**`.
- Non eseguire Blender runtime o FFmpeg runtime se non richiesto esplicitamente.
- Usare sempre Python di progetto quando si toccano NPU/OpenVINO/tool runtime:

```powershell
$ProjectPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $ProjectPython -c "import sys; print(sys.executable)"
```

- Per OpenVINO 2026.1 nel progetto usare `from openvino import Core`, non `from openvino.runtime import Core`.
- Quando si toccano script/codice indicare sempre il numero di righe risultante.

## Stato consolidato prima di questo handoff

Sono state applicate e pushate patch su `master` per:

1. debug lab brokerato nel product gate heap;
2. uso del Python di progetto per NPU/OpenVINO;
3. workload reale NPU opzionale con `--run-device-workload`;
4. quality gate piu' severo su source anchors, riferimenti ambigui e stub/placeholders;
5. stato finale `blocked_with_reason` quando la proposta contiene `pass`, funzioni solo commentate o blocchi non operativi.

Commit locali gia' pushati dall'utente durante la sessione:

- `9e1c03b` — `feat(ai): broker runtime debug lab in heap product gate`
- `cc6ac4c` — `fix(ai): harden heap proposal quality gate`

File modificati in queste patch:

- `Tools/ai/run_heap_runtime_completeness_gate.py`
- `Tools/ai/build_npu_micro_task_companion_report.py`
- `Tools/npu/_shared/npu_runtime.py`

## Evidenze runtime importanti

### NPU corretta con Python di progetto

Verifica manuale riuscita:

```powershell
$ProjectPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $ProjectPython -c "import openvino; print(openvino.__version__); from openvino import Core; print(Core().available_devices)"
```

Output osservato:

```text
2026.1.0-21367-63e31528c62-releases/2026/1
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

Nota tecnica: `openvino.runtime` non e' disponibile nell'ambiente corrente; il path corretto e' `from openvino import Core`.

### Workload reale NPU riuscito

Comando di prova riuscito:

```powershell
& $ProjectPython -m Tools.ai build_npu_micro_task_companion_report `
  --repo-root . `
  --request "test npu project env con workload reale su dispositivo NPU" `
  --python-exe $ProjectPython `
  --output .\output\validation\npu_project_env_probe_real_workload.json `
  --markdown-output .\output\validation\npu_project_env_probe_real_workload.md `
  --timeout-seconds 120 `
  --run-device-workload `
  --device-workload-seconds 5 `
  --device-workload-iterations 5000
```

Risultato osservato:

```text
npu_device_workload_requested    : True
npu_device_workload_performed    : True
npu_provider_execution_performed : True
mode                             : npu_openvino_micro_workload
iterations                       : circa 20k-22k in 5 secondi
output_preview                   : [2.0, 2.0, 2.0, 2.0]
python_exe                       : .venv\Scripts\python.exe
errors/warnings                  : vuoti
```

### Run heap con NPU reale

Run successive hanno mostrato:

- NPU workload reale eseguito su ogni revisione quando `--allow-npu-device-workload`/closure equivalente e' attivo.
- GPU0 esegue OpenVINO su `GPU.0`, ma rimane troppo diagnostica e poco companion reviewer.
- GPU1 continua a generare proposte con stub/comment-only in alcuni casi.
- Il quality gate ora rileva correttamente `bare_pass`, `comment_only_function_stub`, path ambigui e source refs non verificati.
- Il prodotto finale puo' finire correttamente in `blocked_with_reason` se la proposta non e' concreta.

Esempio di stato corretto quando il gate blocca:

```text
product_status             : blocked_with_reason
quality_output_passed      : False
provider_revision_count    : 4+
runtime_debug_lab_required : True
runtime_debug_lab_passed   : True
response_file_reference_quality.passed : True
implementation_quality.passed          : False
```

Questo e' desiderabile: meglio bloccare che dichiarare pronto un prodotto con stub.

## Problema architetturale ancora aperto

Il runtime heap e' ancora troppo simile a una pipeline sequenziale:

```text
GPU1 -> GPU0 -> NPU -> gate
```

Questo modello e' sbagliato per l'obiettivo del progetto.

Il modello corretto e':

```text
startup reload contesto/memoria/docs/repo
↓
heap state pronto
↓
heartbeat loop
  ogni entita' legge lo stato comune
  ogni entita' pubblica facts / needs / claims / critiques / proposal parts / audit pieces
  GPU0 puo' criticare e raffinare anche senza nuova risposta GPU1
  NPU puo' auditare contesto, guardrail, workload, source anchors e quality signals anche senza nuova risposta GPU1
  GPU1 e' planner/synthesizer, non proprietario unico del prodotto
  tool deterministici validano e scrivono segnali oggettivi
↓
composer finale assembla blocchi validi e decide ready/blocked
```

Quindi il runtime non deve modellare i provider come catena rigida. Deve modellarli come worker event-driven su blackboard condiviso.

## Semantica corretta dei parametri

### `max-iterations`

Non deve significare "numero di risposte GPU1".

Deve significare:

```text
numero massimo di heartbeat heap / cicli di stato condiviso
```

Un heartbeat e' un ciclo in cui lo scheduler guarda lo stato heap corrente, decide quali lane sono utili, pubblica task, raccoglie eventi, riduce lo stato, valuta qualita' e decide se continuare, comporre o bloccare.

### `max-provider-revisions`

Non deve significare pipeline `GPU1 -> GPU0 -> NPU` ripetuta.

Deve essere solo il limite massimo di revisioni/proposte prodotte o rielaborate dai provider.

GPU0 e NPU devono poter lavorare anche senza nuova proposta GPU1 se esiste stato da auditare, criticare, validare o arricchire.

### `budget-minutes`

Da verificare. Deve essere wall-clock budget sull'intera run, non solo su singoli provider. Serve una metrica esplicita nel report:

```text
started_at
ended_at
elapsed_seconds
budget_seconds
budget_exhausted
heartbeat_count
provider_revision_count
```

Se non e' gia' garantito, va patchato.

## Design target: heap scheduler reale

Struttura concettuale desiderata:

```python
while not budget_expired() and heartbeat < max_iterations:
    state = heap.load_state()

    tasks = scheduler.plan_next_tasks(state)
    # esempi:
    # - reload_context
    # - gpu1_generate_part
    # - gpu0_review_part
    # - npu_audit_part
    # - debug_lab_validate
    # - deterministic_compose_patch_plan

    results = run_ready_tasks(tasks)  # parallelizzabile dove possibile

    for result in results:
        heap.append_event(result)
        heap.reduce_into_state(result)

    quality = quality_gate.evaluate(heap.state)

    if quality.ready:
        composer.compose_final(heap.state)
        break

    if quality.blocked_but_recoverable:
        scheduler.inject_recovery_tasks(quality.errors)

    if quality.unrecoverable or no_progress:
        composer.compose_blocked_with_reason(heap.state)
        break
```

Stato heap desiderato:

```text
HEAP_STATE:
  request
  startup_context
  memory_inventory
  docs_context
  semantic_chunks
  tool_catalog
  facts[]
  needs[]
  claims[]
  proposals[]
  critiques[]
  gpu0_reviews[]
  npu_audits[]
  debug_lab_results[]
  quality_signals[]
  composer_fragments[]
```

## Ruolo corretto delle lane

### GPU1

GPU1 deve essere planner/synthesizer/cumulative responder, ma non deve essere l'unica fonte del prodotto finale.

Deve sapere esplicitamente che:

- puo' scrivere proposal chunks parziali;
- non deve comprimere tutto in una singola risposta;
- il composer finale assemblera' i blocchi;
- se un blocco viene bocciato da GPU0/NPU/quality gate, deve produrre una revisione mirata, non ripetere lo stesso testo.

### GPU0

GPU0 non deve essere solo workload diagnostico su OpenVINO.

Deve diventare companion reviewer operativo:

- controlla se i proposal chunks sono troppo simili;
- trova path ambigui e basename non ancorati;
- boccia stub, `pass`, TODO, comment-only code;
- valuta patchability e concretezza;
- confronta proposta con source candidates;
- richiede debug lab su blocchi sospetti;
- produce critique strutturate nel heap.

### NPU

NPU non deve essere solo capability probe.

Deve produrre micro-task/audit piece riusabili:

- capability proof reale (`npu_openvino_micro_workload`);
- audit guardrail;
- audit source anchors;
- audit dichiarazioni false (`patch applied`, `source writes`, `provider execution`);
- audit quality signals;
- facts compatti da inserire nello stato condiviso.

Quando il workload reale e' richiesto e riesce, il report deve pubblicare eventi/facts nel heap, non restare solo telemetria laterale.

### Debug lab

Il debug lab e' attivo ma non ancora usato abbastanza come strumento operativo.

Deve diventare un vero laboratorio Python controllato, simile a una mini execution environment:

- no `free_shell`;
- operazioni allowlistate;
- repo-root constrained;
- niente source write sotto `output/**`;
- cattura stdout/stderr/returncode/artifacts;
- valida patch sketch, import, CLI, JSON schema, path, file existence;
- puo' eseguire micro-script generati solo se confinati e non distruttivi;
- produce report JSON/MD consumabili dal heap/composer.

## Startup context/memory reload: punto critico

Il caricamento del contesto e' piu' complesso di una semplice concatenazione di file.

Devono essere usati i tool gia' responsabili della run unica e i loro artifact devono entrare nello heap prima dei provider. Altrimenti GPU1/GPU0/NPU risultano scollegate o lavorano su contesto incompleto.

Tool da usare/integrare come fase iniziale:

- `Tools/ai/build_agent_agnostic_tool_inventory.py`
- `Tools/ai/build_agent_memory_inventory.py`
- `python -m Tools.ai agent_runtime_sqlite_memory` / runtime sqlite memory wrapper effettivo
- `Tools/ai/build_agent_transient_request_context.py`
- `Tools/ai/select_semantic_code_chunks.py`
- `Tools/ai/build_ai_context_pack.py`
- `Tools/ai/build_semantic_evidence_chunks.py`
- eventuali tool storici della run unica per context pack/evidence bundle/chunk manifest/composer

Il launcher `Tools/ai/run_heap_runtime_context_closure.py` ha iniziato a fare startup reload, ma una run ha fallito cosi':

```text
startup_reload_performed : true
startup_reload_passed    : false
heap_returncode          : 2
heap_stderr_tail         : startup context/memory reload failed; heap run skipped
```

Causa osservata nel tail: `build_ai_context_pack.py` ha prodotto artifact ma `passed=false` e returncode 2, con file inclusi/troncati. Il launcher ha quindi saltato l'heap.

Fix richiesto:

- non trattare ogni `passed=false` del context pack come abort assoluto se gli artifact minimi sono presenti;
- distinguere `fatal_reload_failure` da `degraded_context_pack`;
- pubblicare nel heap gli eventi `memory_context_reload` con stato `passed`, `degraded` o `failed`;
- procedere con heap run se il task file input-ready e gli artifact minimi esistono;
- bloccare solo se mancano artifact obbligatori o se il tool segnala errore realmente fatale;
- inserire nel task file/heap manifest i path degli artifact caricati, non solo il testo concatenato.

## Composer finale e output Documenti

Il composer finale deve sempre eseguire packaging, anche quando il prodotto e' `blocked_with_reason`.

Output richiesto a fine run:

```text
C:\Users\carmi\Documents\aicarmine_heap_final_proposals_<stamp>\
  aicarmine_heap_final_proposals_<stamp>.md
  aicarmine_heap_final_proposals_<stamp>.txt
  aicarmine_heap_final_proposals_<stamp>.json
  proposal_chunks\heap_proposal_revision_*.md
  proposal_chunks\heap_proposal_revision_*.json
```

Il launcher ha gia' mostrato che questo packaging e' possibile in alcune run, ma va reso affidabile e non dipendente dal successo pieno del prodotto.

Regola: se la run produce chunks, provider reports o quality failures, il composer deve scrivere comunque una proposta finale o un dossier di blocco scaricabile in Documenti.

## Problemi osservati nelle proposte generate

Il modello locale ha prodotto spesso proposte generiche tipo:

```python
def update_policy():
    # Implementazione della politica
    pass
```

Il quality gate ora le rileva come:

```text
placeholder_hits: ['bare_pass', 'comment_only_function_stub']
implementation_quality.passed: false
product_status: blocked_with_reason
```

Questo comportamento e' corretto, ma manca la recovery operativa: dopo il blocco, lo scheduler deve cambiare strategia.

Esempi di recovery corretta:

- chiedere a GPU0 una critique puntuale sui file reali;
- chiedere a NPU un audit su source anchors e guardrail;
- usare deterministic composer/code-plan builder invece di richiedere a GPU1 la stessa proposta;
- spezzare il problema in blocchi `part_001`, `part_002`, ecc.;
- imporre exact repo-relative paths;
- usare debug lab per validare import/CLI/schema.

## Prossima patch consigliata

Titolo suggerito:

```text
feat(ai): run heap providers as event-driven blackboard workers
```

Obiettivi patch:

1. Inserire `HeapScheduler` o equivalente nel runtime heap.
2. Separare heartbeat da provider revisions.
3. Rendere GPU0 e NPU lane indipendenti/event-driven, non subordinate alla risposta GPU1.
4. Pubblicare startup reload come eventi/facts nello heap prima dei provider.
5. Rendere `run_heap_runtime_context_closure.py` tollerante a context pack degradato se gli artifact minimi esistono.
6. Fare in modo che NPU workload facts entrino nello heap/shared memory.
7. Fare in modo che GPU0 produca review strutturata su chunks/source anchors/stub/progress.
8. Fare in modo che il quality gate, quando trova stub, generi recovery tasks invece di ripetere la stessa pipeline.
9. Fare sempre packaging finale in `Documents\aicarmine_heap_final_proposals_<stamp>`.
10. Verificare budget enforcement wall-clock e aggiungere metriche `elapsed_seconds`, `budget_exhausted`, `heartbeat_count`.

## Validazioni consigliate dopo la patch

### Compile

```powershell
python -m py_compile `
  .\Tools\ai\run_heap_runtime_completeness_gate.py `
  .\Tools\ai\run_heap_runtime_context_closure.py `
  .\Tools\ai\build_npu_micro_task_companion_report.py `
  .\Tools\npu\_shared\npu_runtime.py
```

### NPU reale

```powershell
$ProjectPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $ProjectPython -m Tools.ai build_npu_micro_task_companion_report `
  --repo-root . `
  --request "test npu project env con workload reale su dispositivo NPU" `
  --python-exe $ProjectPython `
  --output .\output\validation\npu_project_env_probe_real_workload.json `
  --markdown-output .\output\validation\npu_project_env_probe_real_workload.md `
  --timeout-seconds 120 `
  --run-device-workload `
  --device-workload-seconds 5 `
  --device-workload-iterations 5000
```

Atteso:

```text
npu_device_workload_requested    : True
npu_device_workload_performed    : True
npu_provider_execution_performed : True
mode                             : npu_openvino_micro_workload
```

### Closure heap con startup reload e composer

```powershell
$ProjectPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $ProjectPython -m Tools.ai run_heap_runtime_context_closure `
  --repo-root . `
  --python-exe $ProjectPython `
  --budget-minutes 10 `
  --max-iterations 6 `
  --max-provider-revisions 6 `
  --timeout-seconds 1200 `
  --npu-device-workload-seconds 5 `
  --npu-device-workload-iterations 5000 `
  --request "Esegui MVP/refine heap con proposal chunks multi-parte, GPU0 companion review, NPU micro workload reale, debug lab e composer finale. Usa file sorgente verificati, contesto repo/docs/memoria precaricato, blocca stub/pass/placeholder e produci proposte operative multiple."
```

Controlli attesi:

```powershell
$Report = Get-Content "$RunDir\heap_runtime_completeness_gate_report.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$Report.metrics | Select-Object product_status,quality_output_passed,heartbeat_count,provider_revision_count,runtime_debug_lab_passed
$Report.real_run_output_contract.response_file_reference_quality | Format-List
```

Attesi minimi:

- `startup_reload_performed = true`
- `startup_reload_passed = true` oppure `startup_reload_status = degraded` ma heap non saltato se artifact minimi presenti
- `npu_device_workload_performed = true`
- `gpu0_review` presente e non solo workload summary
- `proposal_iteration_artifacts` non vuoto
- nessun `unverified_source_file_refs`
- nessun `ambiguous_source_file_refs`
- nessun `bare_pass`, `TODO`, `placeholder`, `comment_only_function_stub` nel prodotto ready
- se rimangono stub, `product_status = blocked_with_reason`
- `composer_documents_dir` valorizzato anche se blocked

## Prompt operativo da incollare nella prossima chat

```text
Leggi integralmente docs/LOCAL_AI_TASKS/next-chat-handoff-heap-blackboard-runtime-2026-05-10.md.

Repository: C-F-tek/blender-audio-project.
Branch: master.
Project: IA-Carmine.

Riprendi esattamente da questo handoff. Non reinventare architettura o stato.

Obiettivo: trasformare run_heap_runtime_completeness_gate / run_heap_runtime_context_closure da pipeline provider sequenziale a heap blackboard event-driven con heartbeat scheduler.

Punti obbligatori:
- max-iterations = heartbeat heap, non numero di risposte GPU1.
- max-provider-revisions = limite revisioni provider, non pipeline rigida.
- GPU0 e NPU devono poter lavorare anche senza nuova risposta GPU1, se lo stato heap contiene materiale da criticare/auditare/validare.
- startup reload di docs/repo/memoria/context deve usare i tool gia' responsabili della run unica e inserire artifact/facts nello heap prima dei provider.
- il context reload non deve abortire l'heap se build_ai_context_pack produce artifact minimi ma ritorna degraded; deve pubblicare evento degraded e procedere quando sicuro.
- NPU deve usare Python di progetto e `from openvino import Core`; il workload reale deve entrare nello heap come facts/audit piece.
- GPU0 deve diventare companion reviewer operativo, non solo workload diagnostico.
- quality gate deve bloccare stub/pass/comment-only e generare recovery tasks, non ripetere loop identico.
- composer finale deve assemblare proposal chunks/reviews/audit/debug results e salvare sempre MD/TXT/JSON in Documenti: `C:\Users\carmi\Documents\aicarmine_heap_final_proposals_<stamp>`.
- se tocchi codice/script indica il numero di righe risultante.

Non fare merge/rewrite/force-push/deploy/secret/permission/billing/visibility changes. Non committare output/**, renders/**, *.db, *.sqlite, indexAI/code_chunks/**.
```

## Criterio di successo reale

Non basta che `provider_execution_performed=true`.

La run e' valida solo se:

1. il contesto iniziale e' precaricato nello heap;
2. GPU0/NPU/GPU1 producono eventi indipendenti e riusabili;
3. NPU workload reale e audit facts sono presenti nello stato condiviso;
4. GPU0 produce review/critiche operative;
5. le proposte sono multi-chunk e non limitate dal contesto della singola risposta GPU1;
6. il composer finale assembla il prodotto completo o un blocco motivato;
7. il prodotto ready non contiene stub/pass/comment-only;
8. in caso di blocco viene comunque scritto il dossier completo in Documenti.
