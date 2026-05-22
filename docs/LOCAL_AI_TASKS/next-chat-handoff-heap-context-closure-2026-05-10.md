# IA-Carmine — Handoff prossima chat — Heap context closure / shared memory / proposal composer — 2026-05-10

Repository:

```text
C-F-tek/blender-audio-project
```

Branch operativa corrente:

```text
master
```

Modalità operativa richiesta:

- Rispondere in italiano tecnico, diretto e operativo.
- Usare GitHub/API e codice reale della repo quando disponibile.
- Non reinventare architettura o stato: riprendere da questo handoff.
- Non fare merge distruttivi, force-push, rewrite history, delete, deploy, secret/permission/billing/visibility changes.
- Non committare `output/**`, `*.db`, `*.sqlite`, `renders/**`, backup locali `*.bak_*` o patch helper temporanei.
- Quando si toccano codice/script indicare sempre il numero di righe risultante.
- Su questa repo privata lavora solo l’operatore, quindi sono autorizzate patch safe e coerenti anche su problemi collaterali emersi dalla run.

---

## Stato sintetico

Stiamo trasformando `ia_carmine/runtime/heap_runtime/completeness_gate/cli.py` e il relativo wrapper `ia_carmine/runtime/heap_context_closure/cli.py` da semplice gate/report a ciclo heap operativo:

```text
input richiesta
→ preload contesto/docs/memoria/tooling
→ heap exchange persistente
→ proposal chunks multi-parte
→ GPU0 companion review/refine
→ NPU micro-task/workload/audit
→ runtime debug lab
→ quality gate deterministico
→ final composer
→ package finale in Documenti
```

Il principio architetturale da rispettare è questo:

```text
La fonte del sapere runtime deve essere l’heap, non la singola risposta di GPU1.
```

GPU1 non deve portarsi tutta la risposta dentro la propria finestra token. Deve produrre o migliorare blocchi persistenti. GPU0 deve criticare/refinare i blocchi non operativi. NPU deve produrre micro-task/audit piece e, quando abilitato, workload reale. Il composer finale deve assemblare i pezzi persistenti e produrre il pacchetto operatore.

---

## Commit recenti importanti già su `master`

Sono stati pushati su `master` questi commit rilevanti:

```text
9e1c03b  feat(ai): broker runtime debug lab in heap product gate
cc6ac4c  fix(ai): harden heap proposal quality gate
f4278e8  feat(ai): export heap proposal chunks as txt package
dd9e3f8  feat(ai): expose final proposal document paths
```

Effetti principali:

- `runtime_debug_lab` è entrato nel contratto di output reale del gate.
- Il quality gate ora blocca output con riferimenti source ambigui/non verificati e placeholder/stub tipo `pass` o funzioni comment-only.
- Il report NPU usa il Python di progetto `.venv\Scripts\python.exe` e non il Python globale quando richiesto.
- Il micro workload NPU reale funziona quando `--allow-npu-device-workload` / `--run-device-workload` è abilitato.
- Il composer finale esporta proposte complete in `Documents/aicarmine_heap_final_proposals_<stamp>/`.
- Il launcher espone direttamente i path scaricabili: `final_proposal_txt`, `final_proposal_markdown`, `final_proposal_json`, `final_download_manifest_txt`, `proposal_txt_outputs`.

---

## Stato NPU verificato

Problema iniziale:

```text
ModuleNotFoundError: No module named 'openvino.runtime'
```

Causa rilevata:

- il codice cercava `from openvino.runtime import Core`, ma nel venv reale funziona:

```powershell
$ProjectPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $ProjectPython -c "import openvino; print(openvino.__version__); from openvino import Core; print(Core().available_devices)"
```

Output verificato:

```text
2026.1.0-21367-63e31528c62-releases/2026/1
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

Dopo fix, il probe NPU reale ha prodotto:

```text
npu_device_workload_requested    : True
npu_device_workload_performed    : True
npu_provider_execution_performed : True
mode                             : npu_openvino_micro_workload
iterations                       : ~20k-22k in 5s
output_preview                   : [2.0, 2.0, 2.0, 2.0]
python_exe                       : C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe
```

Nota importante: il fatto che l’output sia molto regolare è atteso per un micro workload deterministico; non è una prova sufficiente di “ragionamento NPU”, ma è prova di device path OpenVINO/NPU funzionante. La NPU, nel progetto attuale, è companion/auditor di micro-task e workload bounded, non planner primario.

---

## Stato GPU0

GPU0 oggi esegue workload OpenVINO su `GPU.0` e produce report come companion lane. Output tipico:

```text
GPU0 peer ha eseguito il tool OpenVINO su GPU.0: iterations=800-900 circa, inference_seconds=0.100..., output_preview=[1.0, 1.0, 1.0, 1.0].
```

Problema ancora aperto:

- GPU0 è ancora troppo diagnostica/passiva.
- Deve diventare companion reviewer/refiner reale dei proposal chunks.
- Deve bocciare o raffinare blocchi generici, stub, `pass`, comment-only, riferimenti file ambigui, validation command inventati.
- Deve produrre un giudizio operativo sul blocco: `accept`, `reject`, `refine`, `needs_source_anchor`, `needs_concrete_patch`.

---

## Stato quality gate / proposal loop

Risultato importante: il sistema ora sa bloccare prodotti non uscibili.

Run recente con `heap_quality_gate_probe_20260510-212615`:

```text
product_status             : blocked_with_reason
quality_output_passed      : False
provider_revision_count    : 4
runtime_debug_lab_required : True
runtime_debug_lab_passed   : True
```

Motivo del blocco:

```text
placeholder/stub code detected: ['bare_pass', 'comment_only_function_stub']
```

Source reference quality corretta:

```text
unverified_source_file_refs : []
ambiguous_source_file_refs  : []
passed                      : True
```

Quindi il sistema ha fatto un passo avanti: non accetta più riferimenti ambigui come `policy.py`, `reporting.py`, `runner.py` se non ancorati al path repo-relative completo.

Problema ancora aperto:

- Il proposal loop sa salvare più revisioni, ma GPU1 tende a ripetere la stessa proposta generica.
- Alcune revisioni sono state bloccate perché troppo simili alla precedente:

```text
proposal revision too similar to previous iteration: similarity=1.000
```

- Le proposte spesso contengono ancora sketch tipo:

```python
def sync_gpu_npu():
    pass
```

Questo deve restare bloccante.

---

## Stato composer / export in Documenti

È stato aggiunto il composer finale:

```text
ia_carmine/product/heap_final_proposals/cli.py
```

È stato aggiunto/aggiornato il launcher:

```text
ia_carmine/runtime/heap_context_closure/cli.py
```

Obiettivo:

- anche se il prodotto è `blocked_with_reason`, salvare comunque il pacchetto completo per revisione operatore;
- evitare perdita dei blocchi per limiti token;
- rendere scaricabile/leggibile la proposta completa in TXT.

Output atteso dopo run riuscita fino al composer:

```text
C:\Users\carmi\Documents\aicarmine_heap_final_proposals_<stamp>\
  aicarmine_heap_final_proposals_<stamp>.md
  aicarmine_heap_final_proposals_<stamp>.txt
  aicarmine_heap_final_proposals_<stamp>.json
  aicarmine_heap_final_proposals_<stamp>_DOWNLOADS.txt
  proposal_chunks\heap_proposal_revision_001.md/json
  proposal_chunks_txt\heap_proposal_revision_001.txt
  proposal_chunks_txt\heap_proposal_revision_002.txt
  ...
```

Il launcher ora deve esporre nel JSON finale:

```json
{
  "composer_documents_dir": "...",
  "final_proposal_txt": "...",
  "final_proposal_markdown": "...",
  "final_proposal_json": "...",
  "final_download_manifest_txt": "...",
  "proposal_txt_outputs": ["..."]
}
```

---

## Problema nuovo: startup context/memory reload ancora incompleto

Run recente:

```text
ia_carmine/runtime/heap_context_closure/cli.py
```

ha prodotto:

```json
{
  "startup_reload_performed": true,
  "startup_reload_passed": false,
  "heap_returncode": 2,
  "composer_returncode": 2,
  "heap_stderr_tail": "startup context/memory reload failed; heap run skipped",
  "composer_stderr_tail": "heap report missing; composer skipped"
}
```

Il fallimento avviene nella fase startup reload, precisamente nel tool:

```text
ia_carmine/context/agent_context/ai_context_pack/cli.py
```

Command tail indicava returncode `2` ma stdout JSON:

```json
{
  "passed": false,
  "profile": "project_self_improvement",
  "included_file_count": 11,
  "truncated_file_count": 5,
  "provider_execution_performed": false
}
```

Interpretazione operativa:

- Il preload è partito e alcuni tool hanno funzionato:
  - `python -m ia_carmine.cli build_agent_agnostic_tool_inventory`
  - `python -m ia_carmine.cli build_agent_memory_inventory`
  - `python -m ia_carmine.cli build_agent_transient_request_context`
- però `build_ai_context_pack.py` ha segnato `passed=false` probabilmente per policy interna su file troncati, profilo, evidenza o limiti.
- Il launcher attuale tratta qualsiasi startup reload failed come blocco totale e salta heap/composer.

Punto fondamentale da portare avanti:

```text
Il caricamento del contesto è più complesso di un semplice elenco di file markdown.
```

Deve usare i tool responsabili già presenti in repo e inserire i loro artifact nell’heap prima del ciclo provider. Altrimenti le IA risultano scollegate: GPU1 vede solo frammenti, GPU0 non ha il quadro per criticare, NPU produce audit isolato e il composer assembla pezzi poveri.

---

## Direzione corretta per il preload contesto/memoria

Il preload deve essere una fase canonica `input-ready-before-heap`, non un accessorio.

Deve usare almeno questi tool già presenti o equivalenti storici di run unica:

```text
ia_carmine/context/agent_context/agnostic_tool_inventory/cli.py
ia_carmine/context/agent_context/memory_inventory/cli.py
python -m ia_carmine.cli agent_runtime_sqlite_memory
ia_carmine/context/agent_context/transient_request_context/cli.py
ia_carmine/select_semantic_code_chunks.py
ia_carmine/context/agent_context/ai_context_pack/cli.py
ia_carmine/context/agent_context/semantic_evidence_chunks/cli.py
ia_carmine/runtime/run_gpu_planner_json_contract_smoke.py
python -m ia_carmine.cli agent_runtime_debug_lab
```

La fase startup dovrebbe produrre un manifest unico:

```text
startup_context_memory_reload/heap_context_memory_reload_manifest.json
startup_context_memory_reload/heap_context_memory_reload_manifest.md
startup_context_memory_reload/heap_startup_input_ready_context.md
```

Il `heap_startup_input_ready_context.md` deve contenere riferimenti e sintesi dei pezzi caricati, non solo testo libero. Deve diventare il `--task-file` passato a:

```text
ia_carmine/runtime/heap_runtime/completeness_gate/cli.py
```

Contratto desiderato:

```json
{
  "input_ready_before_heap": true,
  "load_context_into_heap": true,
  "tool_catalog_loaded": true,
  "shared_memory_loaded": true,
  "operational_memory_loaded": true,
  "repo_docs_loaded": true,
  "semantic_code_chunks_loaded": true,
  "ai_context_pack_loaded": true,
  "semantic_evidence_chunks_loaded": true,
  "heap_task_file_written": true
}
```

Se un tool produce `passed=false` ma artifact utili e leggibili, valutare una policy più sfumata:

- `strict_startup_reload=true`: blocca tutto.
- `strict_startup_reload=false`: continua ma marca `startup_reload_degraded=true` e inserisce l’errore nel heap come fatto operativo.

Questa distinzione è importante perché il composer dovrebbe poter salvare comunque i risultati/diagnostica anche quando il preload è degradato.

---

## Obiettivo prossima patch

Obiettivo immediato consigliato:

```text
fix(ai): make heap context startup reload tool-owned and degradable
```

Target probabili:

```text
ia_carmine/context/heap_context_memory_reload/cli.py
ia_carmine/runtime/heap_context_closure/cli.py
ia_carmine/context/agent_context/ai_context_pack/cli.py   # solo se il failure è una policy troppo rigida o poco spiegata
ia_carmine/product/heap_final_proposals/cli.py
```

Azioni richieste:

1. Ispezionare `ia_carmine/context/heap_context_memory_reload/cli.py` e capire perché `build_ai_context_pack.py` ritorna `2` con `included_file_count=11` e `truncated_file_count=5`.
2. Capire se `build_ai_context_pack.py` sta fallendo correttamente o se il launcher deve accettare un output degradato.
3. Far sì che startup reload scriva sempre un manifest leggibile anche in failure parziale.
4. Far sì che il launcher non salti automaticamente composer/export: se heap non parte, il composer o un fallback composer deve almeno esportare startup manifest, stdout/stderr e proposta diagnostica in `Documents`.
5. Inserire nel task-file heap un blocco esplicito che dica alle IA quali artifact di contesto devono consultare e come:

```text
CONTEXT LOADED INTO HEAP:
- tool catalog: <path>
- memory inventory: <path>
- operational memory search/write: <path>
- transient request context: <path>
- ai context pack: <path or degraded>
- semantic chunks: <path>
- repo docs map: <path list>
```

6. Rendere GPU0 companion reviewer più forte: deve ricevere anche il blocco precedente e la quality diagnosis, non solo eseguire workload.
7. Rendere NPU micro-task piece parte del proposal context, non solo provider report a lato.
8. Il final composer deve assemblare:
   - proposte accettate;
   - proposte rifiutate con motivazione;
   - NPU workload/audit;
   - GPU0 review/refine;
   - debug lab report;
   - context/preload manifest;
   - action list concreta per patch successive.

---

## Comando run corrente consigliato

Dopo pull e py_compile:

```powershell
$ProjectPython = (Resolve-Path .\.venv\Scripts\python.exe).Path

& $ProjectPython -m ia_carmine heap_context_closure `
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

Per leggere il pacchetto finale:

```powershell
$RunDir = Get-ChildItem .\output\validation -Directory |
  Where-Object Name -like "heap_context_closure_*" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

$Launcher = Get-Content (Join-Path $RunDir.FullName "heap_runtime_context_closure_launcher.json") -Raw -Encoding UTF8 | ConvertFrom-Json

$Launcher |
  Select-Object `
    launcher_passed,
    startup_reload_passed,
    heap_passed,
    composer_packaging_performed,
    composer_blocking_issue_count,
    final_proposal_txt,
    final_download_manifest_txt,
    composer_documents_dir |
  Format-List

if ($Launcher.final_proposal_txt -and (Test-Path $Launcher.final_proposal_txt)) {
  Get-Content $Launcher.final_proposal_txt -Raw -Encoding UTF8
}
```

---

## Cosa aggiungere nella prossima chat dai risultati run

L’operatore fornirà i risultati della prossima run. Aggiungerli qui/nel nuovo handoff sotto questa sezione:

```text
RUN RESULTS TO ADD:
- run_dir:
- startup_reload_passed:
- startup_manifest:
- startup_task_file:
- heap_returncode:
- heap_passed:
- composer_returncode:
- composer_packaging_performed:
- composer_documents_dir:
- final_proposal_txt:
- product_status:
- quality_output_passed:
- provider_revision_count:
- NPU workload performed/passed/iterations/seconds:
- GPU0 review/refine quality:
- proposal chunk count:
- accepted proposal chunks:
- rejected proposal chunks:
- blocking issues:
- next concrete patch targets:
```

---

## Diagnosi finale da non dimenticare

Il problema non è solo “far partire uno script”.

Il problema reale è garantire che l’heap sia alimentato da contesto strutturato e persistente:

```text
repo docs + memoria + tool catalog + semantic chunks + runtime evidence + provider reports
```

Se questi dati non vengono caricati nell’heap tramite i tool responsabili, il sistema torna a essere una catena di chiamate scollegate:

```text
GPU1 produce testo generico
GPU0 fa solo workload diagnostico
NPU fa solo micro workload isolato
debug lab passa ma non guida il prodotto
composer assembla output povero
```

La direzione corretta è:

```text
preload tool-owned → heap shared state → provider companion lanes → proposal chunks → deterministic quality gates → final composer/package
```

La prossima patch deve quindi concentrarsi su startup context/memory reload come contratto operativo dell’heap, con fallback degradato ma sempre esportabile in Documenti.
