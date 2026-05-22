# Heap Loop Problems Addendum — continued code-driven analysis — 2026-05-11

Repository:

```text
C-F-tek/blender-audio-project
```

Branch:

```text
codex/heap-loop-problems-20260511
```

## Scope

Continuazione dell'analisi GitHub-only sul loop heap dopo il primo documento:

```text
docs/LOCAL_AI_TASKS/heap-loop-problems-2026-05-11.md
```

Questa e' ancora una modifica document-only. Nessun provider, nessun Blender/FFmpeg runtime, nessuna patch applicata, nessun output runtime committato.

---

## Finding 10 — Reconciliation post-run non equivale a contesto consumato dai provider

### Evidenza code-driven

Esiste:

```text
ia_carmine/reconcile_heap_report_with_startup_reload.py
```

Il tool legge:

```text
startup_context_memory_reload/heap_context_memory_reload_manifest.json
heap_runtime_completeness_gate_report.json
```

e poi aggiorna il report heap con:

```text
startup_preload_integrated=True
startup_preload_requirement_refs
completed_requirements
missing_requirements
context_artifact_refs
```

### Problema

Questa riconciliazione avviene dopo il gate, quindi non prova che GPU1/GPU0/NPU abbiano letto o consumato il contesto durante il loop. Prova solo che il report finale puo' essere arricchito dopo l'esecuzione.

La differenza operativa e' critica:

```text
post-run report patching != pre-provider heap knowledge
```

### Impatto

Il sistema puo' apparire completo nel report finale, ma il ciclo provider potrebbe aver lavorato senza artifact refs di startup nel blackboard.

### Azione consigliata

Lo smoke “startup context ingestion” deve leggere `events.jsonl` o lo snapshot heap generato prima/durante il primo round e verificare eventi pre-provider, non solo campi nel report finale riconciliato.

---

## Finding 11 — Reconciler rifiuta startup degradato, in contrasto con policy degradable

### Evidenza code-driven

`reconcile_heap_report_with_startup_reload.py` calcola:

```text
startup_degraded = startup_reload_degraded is True or degraded_requirements non vuoto
```

Se `startup_degraded` e' vero aggiunge errore:

```text
startup manifest is degraded; refusing to reconcile missing base requirements
```

### Problema

La policy corrente desiderata per il preload e':

```text
strict_startup_reload=false -> continua se input_ready_before_heap=true e artifact utili esistono, marcando startup_reload_degraded=true
```

Il reconciler invece impedisce di usare artifact utili quando il manifest e' degradato. Questo e' prudente ma contrasta con il contratto “degradable”.

### Impatto

Una run con `build_ai_context_pack.py` advisory failed ma artifact utili puo' continuare nel launcher, ma poi perdere integrazione formale nel report riconciliato.

### Azione consigliata

Introdurre una policy esplicita nel reconciler:

```text
--allow-degraded-startup
```

oppure derivare dal manifest:

```text
strict_startup_reload=false
input_ready_before_heap=true
artifact_useful=true
```

In quel caso il reconciler deve integrare refs e mantenere warning/blocchi degradati, non fallire.

---

## Finding 12 — `useful_artifact_refs()` guarda anche `execution.artifacts`, ma il manifest startup usa `artifact_summaries`

### Evidenza code-driven

`prepare_heap_context_memory_reload.py` produce per ogni tool execution campi come:

```text
artifact_paths
existing_artifact_paths
useful_artifact_paths
artifact_summaries
```

`reconcile_heap_report_with_startup_reload.py` estrae artifact refs dal blocco top-level `artifacts`, poi tenta anche:

```text
for artifact in execution.get("artifacts") or []
```

### Problema

Il campo `artifacts` non risulta coerente con la shape prodotta da `run_tool()` nel preload. Questo non rompe totalmente il reconciler perche' il top-level `artifacts` esiste, ma riduce la copertura dei refs utili granulari per singolo tool.

### Impatto

Il report finale potrebbe perdere path specifici prodotti solo nei `useful_artifact_paths` o `artifact_summaries` dei tool executions.

### Azione consigliata

Aggiornare `useful_artifact_refs()` per leggere anche:

```text
execution.useful_artifact_paths
execution.existing_artifact_paths
execution.artifact_paths
execution.artifact_summaries[].path
```

---

## Finding 13 — `operational_memory_write` e startup preload non sono allineati

### Evidenza code-driven

`python -m ia_carmine.cli run_heap_runtime_completeness_gate` include tra i requirement base:

```text
operational_memory_write
operational_memory_search
```

`prepare_heap_context_memory_reload.py` esegue in startup:

```text
python -m ia_carmine.cli agent_runtime_sqlite_memory --action status --scope operational
python -m ia_carmine.cli agent_runtime_sqlite_memory --action search --scope operational
```

ma non risulta una `remember` operational durante il preload.

`python -m ia_carmine.cli agent_runtime_sqlite_memory` supporta `remember` operational e garantisce che il DB operativo stia sotto `output/**`.

### Problema

Il gate richiede `operational_memory_write`, ma il preload dimostra solo status/search. Se il loop non scrive un fatto operativo nella scratch memory, il requirement puo' restare concettualmente scoperto.

### Impatto

La memoria comune non diventa veramente “working tray” del loop: viene interrogata, ma non necessariamente alimentata con stato run-specific.

### Azione consigliata

Durante startup o al primo round heap, scrivere in operational memory un record safe tipo:

```text
action=remember
scope=operational
role=heap_startup_reload
summary=startup context/memory reload manifest
content=<manifest path + degraded status + artifact refs summary>
tag=heap_startup_context
```

Guardrail: DB sotto `output/**`, mai persistent memory salvo conferma esplicita.

---

## Finding 14 — Composer e' piu' maturo del gate: raccoglie GPU0/NPU/startup, ma opera a posteriori

### Evidenza code-driven

`ia_carmine/product/heap_final_proposals/cli.py` raccoglie:

```text
startup manifest
proposal iterations
provider reports
GPU0 reviews
NPU audits/workload
blocking issues
action list
Documents package
```

Gestisce anche fallback heap report.

### Problema

Il composer assembla bene cio' che trova, ma non puo' correggere il fatto che una lane non abbia consumato il contesto in fase decisionale.

### Impatto

Il composer puo' rendere leggibile un run incompleto, ma non trasforma una catena scollegata in heap operativo.

### Azione consigliata

Aggiungere nel composer una sezione/flag di integrita' causale:

```text
startup_context_seen_before_first_provider_event
startup_artifact_refs_seen_in_heap_events
provider_proposal_refs_startup_context
```

Se questi flag sono falsi, il composer deve indicare:

```text
composer_packaging_performed=true
product_causality_passed=false
```

---

## Finding 15 — Event taxonomy del heap non ha un tipo esplicito `context_memory_reload`

### Evidenza code-driven

`provider_runtime_heap.py` consente questi event types:

```text
user_request
provider_state
task_state
fact
need
tool_catalog_request
tool_catalog_response
evidence_request
evidence_response
broker_request
broker_result
claim
validation_signal
decision
candidate_operation
patch_plan_signal
product_signal
provider_evidence
```

La funzione `append_reload_lifecycle_event()` in `python -m ia_carmine.cli run_heap_runtime_completeness_gate` incapsula il reload come payload `kind=memory_context_reload`, ma deve per forza usare uno degli event type generici tramite `append_heap_exchange_event()`.

### Problema

Il concetto e' presente ma non tipizzato a livello di heap event taxonomy. Questo rende piu' difficile scrivere smoke/validator semplici: bisogna cercare payload.kind invece di event_type.

### Azione consigliata

Senza rompere compatibilita', usare `event_type="provider_evidence"` o `event_type="fact"` in modo stabile e documentare:

```text
payload.kind == memory_context_reload
payload.reload_event == <tool_catalog_reload|shared_memory_reload|...>
```

In alternativa, aggiungere un nuovo event type `context_memory_reload` con test di compatibilita'.

---

## Finding 16 — Broker allowlist espone tool utili ma il loop deve dimostrare request/result, non solo catalogo

### Evidenza code-driven

`agent_runtime_tool_broker.py` espone tool allowlisted rilevanti:

```text
build_agent_memory_inventory
build_agent_agnostic_tool_inventory
build_agent_transient_request_context
select_semantic_code_chunks
build_ai_context_pack
build_semantic_evidence_chunks
agent_runtime_debug_lab
runtime_sqlite_memory
```

### Problema

Il fatto che il catalogo esista non dimostra che i provider abbiano fatto richieste brokerizzate e che i risultati siano rientrati nello heap.

### Impatto

Il loop puo' soddisfare documentazione/capability manifest ma non il comportamento operativo:

```text
need -> broker_request -> broker_result -> shared_evidence -> decision
```

### Azione consigliata

Aggiungere contatori e smoke su eventi:

```text
broker_request_count
broker_result_count
broker_result_refs_nonempty
shared_evidence_from_broker_count
pending_broker_request_count == 0
```

Il product gate non dovrebbe dichiarare product causality completa se ci sono broker requests pendenti o risultati non collegati a `shared_evidence`.

---

## Finding 17 — Naming: `startup_preload_integrated` nel report puo' essere fuorviante

### Evidenza code-driven

Il reconciler imposta:

```text
startup_preload_integrated=True
```

quando integra i requirement nel report post-run.

### Problema

Il nome sembra indicare integrazione nel runtime heap, ma il tool integra il report JSON finale, non necessariamente l'heap event stream consumato dai provider.

### Azione consigliata

Separare i campi:

```text
startup_preload_reconciled_into_report=true
startup_preload_ingested_into_heap=<true|false|unknown>
startup_preload_seen_by_provider_lanes=<true|false|unknown>
```

---

## Patch order consigliato aggiornato

Ordine piu' sicuro:

1. `test(ai): add heap startup context ingestion smoke`
2. `fix(ai): emit startup preload artifact refs into heap before provider loop`
3. `fix(ai): allow degraded startup reconciliation when artifacts are useful`
4. `fix(ai): record operational memory startup write in scratch DB`
5. `feat(ai): expose product causality flags in composer`
6. `test(ai): assert broker request/result/evidence closure`

---

## Acceptance criteria per la prossima patch codice

Una run/smoke deve provare almeno:

```text
startup_task_file_exists=true
startup_manifest_exists=true
startup_manifest.input_ready_before_heap=true
startup_reload_degraded propagated into heap event/fact
memory_context_reload events exist before first provider result
artifact_refs non-empty
operational_memory_write performed against output/** scratch DB
broker pending requests == 0 after broker pass
composer.product_causality_passed computed
```

---

## Decisione operativa aggiornata

Il prossimo intervento non dovrebbe partire dal composer, perche' il composer e' gia' abbastanza forte come packaging. Il collo di bottiglia e' prima:

```text
startup preload -> heap event stream -> provider consumption
```

Quindi la prima patch codice deve aggiungere test e wiring pre-provider, non solo migliorare l'export finale.
