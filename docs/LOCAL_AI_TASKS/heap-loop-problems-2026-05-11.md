# Heap Loop Problems — code-driven notes — 2026-05-11

Repository:

```text
C-F-tek/blender-audio-project
```

Branch di lavoro:

```text
codex/heap-loop-problems-20260511
```

## Scope

Analisi GitHub-only, code-driven, del loop heap e dei componenti che dovrebbero alimentare le IA durante il ciclo:

```text
input -> preload tool/docs/memory/context -> heap shared state -> provider lanes -> proposal chunks -> review/audit -> composer
```

Questa modifica e' document-only. Non esegue provider, non applica patch, non scrive output runtime, non tocca Blender/FFmpeg, non committa `output/**`, `*.db`, `*.sqlite`, `renders/**` o artifact locali.

## Policy operative applicate

- La fonte del sapere runtime deve essere l'heap, non la singola risposta GPU1.
- Il preload deve essere tool-owned, tracciato e degradabile solo quando gli artifact sono utili e leggibili.
- GPU0 deve essere companion reviewer/refiner, non solo workload diagnostico.
- NPU resta micro-task/workload/audit companion; non e' advisor primario.
- Ogni failure non corretta in questa fase viene annotata qui come problema operativo e candidata a patch successiva.

## Finding 1 — Startup task-file passato al gate, ma ingestione heap da provare/hardenare

### Evidenza code-driven

`ia_carmine/runtime/heap_context_closure/cli.py` costruisce `startup_context_memory_reload/heap_startup_input_ready_context.md` tramite `ia_carmine/context/heap_context_memory_reload/cli.py` e lo passa a `ia_carmine/runtime/heap_runtime/completeness_gate/cli.py` con `--task-file` quando il file esiste.

`ia_carmine/runtime/heap_runtime/completeness_gate/cli.py` contiene funzioni per lifecycle reload:

```text
publish_startup_memory_context_reload_events()
append_reload_lifecycle_event()
```

Queste funzioni generano eventi `memory_context_reload` per requirement come:

```text
tool_catalog
shared_memory
operational_memory_search
shared_context_chunks
semantic_code_chunks
ai_context_pack
semantic_evidence_chunks
```

Dalla ricerca GitHub-only non e' stato possibile provare in modo sufficiente che `publish_startup_memory_context_reload_events()` venga sempre invocata prima delle iterazioni provider. Questo non va trattato come certezza di funzione morta, ma come rischio di wiring non dimostrato.

### Impatto

Se il task-file resta solo un argomento/path e non viene trasformato in fatti/eventi heap con artifact refs, il sistema puo' degradare di nuovo in una catena lineare:

```text
GPU1 legge richiesta/testo
GPU0 fa workload laterale
NPU fa micro-audit laterale
composer assembla pezzi poveri
```

anziche':

```text
preload -> heap facts/evidence refs -> provider consumption -> proposal chunks -> review/audit -> composer
```

### Azione consigliata

Aggiungere uno smoke dedicato, per esempio:

```text
Tools/validation/run_heap_startup_context_ingestion_smoke.py
```

Lo smoke deve verificare che, prima del primo provider round, il runtime heap contenga eventi/fatti con:

```text
startup_manifest
startup_task_file
tool_catalog artifact refs
memory inventory refs
operational memory refs
transient context refs
semantic chunk refs
context pack refs/degraded status
```

Se il test fallisce, patchare `python -m ia_carmine.cli run_heap_runtime_completeness_gate` per invocare esplicitamente il lifecycle reload in fase init e appendere gli artifact refs come `fact`/`evidence_response` o `provider_evidence`.

## Finding 2 — `build_ai_context_pack.py`: il failure non e' spiegabile solo con truncation

### Evidenza code-driven

`ia_carmine/context/agent_context/ai_context_pack/cli.py` imposta `entry["truncated"] = True` quando un file supera il budget, ma la truncation viene registrata come warning. Il pack fallisce (`passed=false`, return code `2`) quando un required file e' mancante, non incluso, o viola policy.

Evidenza storica gia' versionata:

```text
docs/LOCAL_VALIDATION_EVIDENCE/project_self_improvement_context_pack_evidence.json
```

mostra un context pack `passed=true` con `truncated_file_count=14`. Quindi `truncated_file_count > 0` non e' da solo una causa di failure.

### Impatto

La diagnosi precedente orientata a `truncated_file_count=5` rischia di cercare nel punto sbagliato. Il problema reale da catturare e' uno tra:

```text
required_missing
policy_error
read_error
context character budget exhausted
path escapes repo
forbidden path
```

### Azione consigliata

In `ia_carmine/context/heap_context_memory_reload/cli.py`, quando `ai_context_pack_reload` e' degradato, estrarre e riportare nel manifest almeno:

```text
errors
warnings
required_missing
forbidden_path_count
included_file_count
truncated_file_count
included_paths[path, required, included, truncated]
```

Il warning deve indicare la causa specifica, non solo `returncode=2`.

## Finding 3 — Required context initializer utile, ma non copre ogni required path

### Evidenza code-driven

`ia_carmine/ensure_ai_context_required_files.py` legge i required files dal profilo di `build_ai_context_pack.py` e inizializza solo documenti Markdown noti e compatti, come:

```text
docs/README.md
docs/PATCH_SPEC_WORKFLOW.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
```

I required Python files non vengono creati automaticamente, correttamente. Se mancano, finiscono in `missing_unhandled` e il tool fallisce.

### Impatto

La policy e' corretta, ma il launcher/preload deve esporre l'esatto path mancante o bloccato, altrimenti l'operatore vede solo uno startup reload failed generico.

### Azione consigliata

Far confluire `missing_unhandled` e `created_files` nel manifest startup e nel task-file heap.

## Finding 4 — GPU0 companion ancora da provare come reviewer/refiner operativo

### Evidenza code-driven

Il gate contiene controlli di qualita' e veto cross-lane (`response_file_reference_quality`, `cross_lane_proposal_veto`, `heap_parallel_cycle_assessment`) e l'handoff operativo indica che GPU0 deve diventare reviewer/refiner reale dei proposal chunks.

Non e' sufficiente provare che GPU0 esegua workload OpenVINO; bisogna provare che riceva:

```text
proposal chunk corrente
proposal chunk precedente
quality diagnosis
source-anchor feedback
blocking reasons
```

e restituisca una decisione operativa:

```text
accept
reject
refine
needs_source_anchor
needs_concrete_patch
```

### Impatto

Senza questa prova, GPU0 resta una lane diagnostica parallela, non una coscienza critica del loop.

### Azione consigliata

Aggiungere campi/report/smoke:

```text
gpu0_review_received_previous_revision
gpu0_review_received_quality_diagnosis
gpu0_review_decision
gpu0_review_source_anchor_count
gpu0_review_blocking_reason_count
```

## Finding 5 — NPU micro-task/audit rischia di restare side-channel

### Evidenza code-driven

Il gate valuta la presenza NPU in `heap_parallel_cycle_assessment()` e l'handoff richiede che NPU micro-task/workload/audit entri nel proposal context, non solo in un provider report laterale.

### Impatto

Se il composer non include refs e sintesi NPU, il pacchetto finale perde una parte del controllo incrociato.

### Azione consigliata

Nel composer finale verificare e riportare:

```text
npu_audit_refs
npu_workload_performed
npu_workload_passed
npu_workload_iterations
npu_audit_summary
```

almeno nel JSON finale e nel TXT/MD operatore.

## Finding 6 — Payload heap compatto: rischio di truncation silenziosa dei contenuti lunghi

### Evidenza code-driven

`ia_carmine/runtime/provider_runtime_blackboard/cli.py` applica `compact_payload(..., max_chars=8000)`. Questo e' un guardrail corretto, ma se si tenta di inserire contenuto lungo direttamente nell'evento heap, l'evento diventa preview/truncated.

### Impatto

Un provider potrebbe credere che l'heap contenga tutto il contesto, mentre in realta' contiene solo preview.

### Azione consigliata

Per il preload usare principalmente:

```text
artifact refs
hash
summary_fields
passed/degraded/error cause
```

Non dumpare integralmente context pack o documenti lunghi dentro singoli eventi heap.

## Finding 7 — Doppia selezione semantic chunks: helper startup ad hoc vs tool broker

### Evidenza code-driven

`ia_carmine/context/heap_context_memory_reload/cli.py` implementa una selezione deterministica locale `collect_semantic_code_chunks()`. Il broker espone gia' il tool allowlisted:

```text
select_semantic_code_chunks
```

### Impatto

Due selettori possono divergere: uno nel preload e uno nel broker/tool loop. Questo puo' generare differenze tra contesto iniziale e contesto richiesto dalle IA nel loop.

### Azione consigliata

Scelta consigliata:

1. o il preload usa il tool broker/selector canonico;
2. o il selector ad hoc viene documentato come fallback deterministic/no-index e il manifest riporta chiaramente `selection_policy`.

## Finding 8 — Closure audit esiste ma va chiarito se e' parte della closure launcher

### Evidenza code-driven

Esistono:

```text
python -m ia_carmine.cli heap_exchange_closure_audit
Tools/validation/heap_exchange/closure_audit_smoke/cli.py
```

Questi provano la disponibilita' di una deterministic/script audit lane prima della closure. Il launcher context closure invece esegue startup reload, heap gate, reconciliation e composer.

### Impatto

Se la closure audit resta separata, il nome “closure” del launcher puo' sembrare piu' forte di quanto il contratto finale provi realmente.

### Azione consigliata

Rendere la closure audit una fase opzionale/esplicita del launcher o documentare che e' un validator esterno da eseguire nel bundle evidence.

## Finding 9 — Manca uno smoke specifico per “startup context became heap state”

### Problema

Oggi ci sono smoke su gate, closure audit e altri helper, ma il rischio piu' importante e' specifico:

```text
startup_context_memory_reload artifact refs -> heap event/fact/evidence state before provider loop
```

### Azione consigliata

Aggiungere test con repo temporanea che crea un manifest/task-file minimale e verifica che il gate produca eventi con:

```text
memory_context_reload
artifact_refs non vuoti
startup_reload_degraded propagato
input_ready_before_heap propagato
```

## Problemi non corretti in questa modifica

Questa branch non corregge codice perche' la correzione sicura richiede almeno uno smoke mirato prima del wiring runtime. Correggere direttamente il gate senza smoke rischia di mascherare la differenza tra:

```text
task-file passato come argomento
```

e:

```text
task-file e manifest diventati conoscenza heap consumabile dalle lanes
```

## Prossimi target patch consigliati

```text
ia_carmine/runtime/heap_runtime/completeness_gate/cli.py
ia_carmine/runtime/heap_context_closure/cli.py
ia_carmine/context/heap_context_memory_reload/cli.py
ia_carmine/product/heap_final_proposals/cli.py
Tools/validation/heap_runtime/completeness_gate_smoke/cli.py
Tools/validation/run_heap_startup_context_ingestion_smoke.py
```

## Validazione suggerita dopo la prossima patch codice

```powershell
python -m py_compile .\ia_carmine\runtime\heap_runtime\completeness_gate\cli.py
python -m py_compile .\ia_carmine\runtime\heap_context_closure\cli.py
python -m py_compile .\ia_carmine\context\heap_context_memory_reload\cli.py
python -m py_compile .\ia_carmine\product\heap_final_proposals\cli.py
python -m py_compile .\Tools\validation\run_heap_startup_context_ingestion_smoke.py

python -m Tools.validation run_heap_startup_context_ingestion_smoke --repo-root . --output .\output\validation\heap_startup_context_ingestion_smoke.json
python -m Tools.validation run_heap_runtime_completeness_gate_smoke --repo-root . --output .\output\validation\heap_runtime_completeness_gate_smoke.json
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json

git diff --check
git status --short
```

## Decisione operativa

La prossima patch safe dovrebbe partire dal test “startup context ingestion smoke”. Solo dopo quel test conviene modificare il gate per rendere provabile che il preload tool-owned sia davvero entrato nello heap condiviso prima del ciclo provider.
