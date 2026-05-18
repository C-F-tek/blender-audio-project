# Heap universe resume flow handoff — 2026-05-12

## Stato operativo accertato

Questa nota registra il punto reale dopo la run locale `heap_context_closure_20260512-144115` e le correzioni fatte per rendere il ciclo `cold run -> revision context -> resume run` comprensibile e ripetibile.

Il punto importante non e' che il composer sia passato. Il punto importante e' che il runtime heap e' finalmente entrato nell'universo operativo:

```text
preflight_passed = true
startup_reload_passed = true
startup_can_continue = true
heap_passed = true
heap_returncode = 0
fallback_heap_report_written = false
provider_execution_performed = true
proposal_count = 3
provider_report_count = 9
gpu0_review_count = 6
npu_audit_count = 6
```

Il composer resta correttamente bloccato:

```text
product_status = blocked_with_reason
quality_output_passed = false
accepted_proposal_count = 0
rejected_proposal_count = 3
```

Questo e' un blocco di qualita' del prodotto, non un fallimento del ciclo heap. La run e' stata utile per produrre pointer, audit, provider evidence e revision context.

## Concetto chiave: due stati separati

Il flusso ora deve distinguere sempre questi due concetti:

```text
causal_chain_passed
product_acceptance_passed
```

`causal_chain_passed=true` significa che l'universo runtime ha funzionato: preload, heap, provider lanes, pointer, package e revision context sono stati prodotti.

`product_acceptance_passed=false` significa che le proposte prodotte non sono applicabili. Nel caso osservato GPU1 ha prodotto blocchi con placeholder/stub; GPU0 e NPU li hanno rigettati correttamente.

Quindi una run valida puo' avere:

```text
causal_chain_passed = true
product_acceptance_passed = false
requires_concrete_rewrite = true
priority_next_action = rewrite_non_concrete_candidates
```

## Catena corretta

La catena operativa corretta e':

```text
COLD RUN
  -> preload repo/docs/memoria/tool
  -> startup task-file
  -> context_memory pubblica input nel ProviderRuntimeHeap
  -> GPU1/GPU0/NPU lavorano nello stesso heap
  -> composer produce prodotto o blocco motivato
  -> postrun package normalizza causality
  -> block pointer manifest
  -> external revision context

RESUME RUN
  -> riceve external_heap_revision_context.json
  -> se requires_concrete_rewrite=true, GPU1 riscrive prima i blocchi non concreti
  -> GPU0 rivaluta i vecchi pointer
  -> NPU audita i vecchi pointer
  -> solo dopo puo' riprendere forward
```

Il resume non e' un comando separato "fuori universo". E' il ciclo successivo dello stesso universo, alimentato dal revision context prodotto dal ciclo precedente.

## Bugfix applicati nella branch

Branch GitHub:

```text
codex/heap-universe-resume-docs-fixes
```

### 1. `Tools/ai/provider_runtime_blackboard/cli.py`

Problema osservato:

```text
ValueError: unsupported provider lane: 'context_memory'
ValueError: unsupported runtime heap event type: 'startup_task_file_context'
```

Causa: `python -m Tools.ai run_heap_runtime_completeness_gate` pubblicava il preload startup come evento causale di heap usando `source="context_memory"` e `event_type="startup_task_file_context"`, ma `ProviderRuntimeHeap` non esponeva ancora quella lane/event type nell'allowlist.

Correzione:

- aggiunta lane `context_memory`;
- aggiunto event type `startup_task_file_context`;
- aggiornata architettura snapshot con `context_memory = startup_context_memory_reload_and_task_file_input`.

Questa e' la correzione piu' pulita: il preload non deve fingersi broker. Il broker esegue tool; `context_memory` rappresenta il contesto/memoria gia' materializzato nel task-file.

### 2. `python -m Tools.ai build_external_heap_revision_context`

Problemi osservati:

1. Regex non importabile:

```text
re.error: global flags not at the start of the expression
```

2. Revision context che marcava come concreti blocchi in realta' non concreti:

```text
requires_concrete_rewrite = false
priority_next_action = review_or_continue
candidate_concrete_enough = true
```

anche se i blocchi contenevano:

```text
bare_pass
comment_only_function_stub
unresolved_angle_bracket_token
invalid_ps1_py_compile_validation
```

Correzione:

- rimosso uso errato di flag inline `(?is)` non all'inizio regex;
- detector spostato da solo `candidate_response_preview` a funzione `candidate_text_from_block()`;
- classificazione ora usa candidate response, source preview, diagnostic preview, rejection reasons, warning/error metadata e qualita' blocco;
- aggiunti flag:
  - `bare_pass`;
  - `comment_only_function_stub`;
  - `unresolved_angle_bracket_token`;
  - `invalid_ps1_py_compile_validation`;
  - `generic_diff_without_file_context`;
- `candidate_block_concrete_enough()` forza `false` se uno di questi marker e' presente;
- la propagazione simboli e' bloccata se il candidato non e' concreto.

### 3. `Tools/validation/run_external_heap_revision_context_applicability_smoke.py`

Nuovo smoke offline, senza provider e senza source writes.

Copre la regressione specifica:

- blocco con `<id-or-empty>`;
- blocco con `pass`;
- blocco con funzione comment-only/stub;
- blocco con `py_compile` su `.ps1`;
- verifica che `requires_concrete_rewrite=true`;
- verifica che `priority_next_action=rewrite_non_concrete_candidates`;
- verifica che `symbol_propagation_skipped=true`.

## Comandi locali di validazione

Da repository root:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path
```

Compilazione/import:

```powershell
& $RepoPy -m py_compile `
  .\Tools\ai\provider_runtime_blackboard\cli.py `
  -m Tools.ai build_external_heap_revision_context `
  .\Tools\ai\run_external_heap_postrun_package.py `
  .\Tools\ai\heap_context_closure\cli.py `
  .\Tools\ai\heap_runtime\completeness_gate\cli.py `
  .\Tools\validation\run_external_heap_revision_context_applicability_smoke.py

& $RepoPy -c "import Tools.ai.build_external_heap_revision_context as m; print('revision_context_import_ok')"
& $RepoPy -c "from Tools.ai.provider_runtime_heap import normalize_lane, normalize_event_type; print(normalize_lane('context_memory')); print(normalize_event_type('startup_task_file_context'))"
```

Smoke detector:

```powershell
& $RepoPy -m Tools.validation run_external_heap_revision_context_applicability_smoke `
  --output .\output\validation\external_heap_revision_context_applicability_smoke.json
```

Output atteso:

```text
passed = true
requires_concrete_rewrite = true
priority_next_action = rewrite_non_concrete_candidates
symbol_propagation_skipped = true
candidate_concrete_enough = false
```

## Rigenerare il revision context dalla run buona

Usare la run locale che ha gia' heap passed:

```powershell
$RunDir = "C:\Users\carmi\blender\blender-audio-project\output\validation\heap_context_closure_20260512-144115"

& $RepoPy -m Tools.ai build_external_heap_revision_context `
  --pointer-manifest (Join-Path $RunDir "external_heap_block_pointer_manifest.json") `
  --composer-json (Join-Path $RunDir "heap_final_proposal_composer.json") `
  --causality-json (Join-Path $RunDir "heap_final_causality_normalized.json") `
  --output (Join-Path $RunDir "external_heap_revision_context.json") `
  --markdown-output (Join-Path $RunDir "external_heap_revision_context.md")
```

Controlli attesi:

```powershell
$Revision = Get-Content (Join-Path $RunDir "external_heap_revision_context.json") -Raw -Encoding UTF8 | ConvertFrom-Json

$Revision |
  Select-Object `
    operational_revision_context,
    can_resume_universe,
    proposal_block_count,
    provider_execution_performed,
    requires_concrete_rewrite,
    priority_next_action |
  Format-List

$Revision.candidate_applicability_summary | Format-List

$Revision.tasks |
  Where-Object { $_.task_type -eq "rewrite_rejected_block" } |
  Select-Object task_id,candidate_concrete_enough,symbol_propagation_skipped,candidate_applicability_flags |
  Format-Table -AutoSize
```

Atteso:

```text
operational_revision_context = true
can_resume_universe = true
provider_execution_performed = true
requires_concrete_rewrite = true
priority_next_action = rewrite_non_concrete_candidates
non_concrete_candidate_task_count = 3
symbol_propagation_skipped_task_count = 3
```

## Resume run da lanciare dopo

Il resume deve consumare il revision context come stato operativo del ciclo precedente:

```powershell
$NextStamp = Get-Date -Format "yyyyMMdd-HHmmss"
$RunDir = "C:\Users\carmi\blender\blender-audio-project\output\validation\heap_context_closure_20260512-144115"
$RevisionContext = Join-Path $RunDir "external_heap_revision_context.json"

& $RepoPy -m Tools.ai run_heap_runtime_context_closure `
  --repo-root . `
  --python-exe $RepoPy `
  --stamp $NextStamp `
  --revision-context $RevisionContext `
  --revision-context-max-tasks 12 `
  --request "RESUME RUN heap universo FAST: consuma il revision context operativo precedente come stato del ciclo. Se requires_concrete_rewrite=true, GPU1 deve prima riscrivere i candidati non concreti indicati dai task, usando path repo reali esistenti, diff concreti con contesto reale e comandi di validazione corretti per tipo file. Non propagare simboli da blocchi marcati non concreti. GPU0 e NPU devono rivalutare i blocchi riscritti in parallelo. Produci provider teamwork evidence, proposal chunks nuovi, pointer manifest e revision context successivo." `
  --budget-minutes 5 `
  --max-iterations 2 `
  --max-rounds 8 `
  --max-provider-revisions 2 `
  --timeout-seconds 600 `
  --preflight-timeout-seconds 90 `
  --npu-device-workload-seconds 3.0 `
  --npu-device-workload-iterations 2500 `
  --startup-max-memory-chars 32000 `
  --startup-max-context-files 48 `
  --startup-max-chars-per-file 8000 `
  --allow-provider-generation
```

## Cosa verificare dopo il resume

Il resume non deve essere giudicato solo da `composer_passed`.

Verificare prima:

```text
preflight_passed = true
startup_reload_passed = true
startup_can_continue = true
heap_passed = true
fallback_heap_report_written = false
provider_execution_performed = true
external_postrun_package_passed = true
```

Poi verificare la qualita' prodotto:

```text
accepted_proposal_count
rejected_proposal_count
blocking_issue_count
candidate_applicability_summary
requires_concrete_rewrite
priority_next_action
```

Se il resume produce ancora `bare_pass`, `comment_only_function_stub`, `<id-or-empty>` o `py_compile` su `.ps1`, il prossimo bug non e' piu' nel revision-context adapter: e' nel contratto/prompt che guida GPU1 durante `rewrite_non_concrete_candidates`.

## Nota su master locale

Al momento dello stato riportato dall'operatore:

```text
git branch --show-current = master
git status --short:
 M python -m Tools.ai build_external_heap_revision_context
 M Tools/ai/heap_context_memory_reload/cli.py
 M Tools/ai/heap_runtime/completeness_gate/cli.py
 M Tools/ai/heap_context_closure/cli.py
```

La branch GitHub non deve essere applicata alla cieca sopra quei file locali senza prima confrontare diff. In particolare `python -m Tools.ai run_heap_runtime_completeness_gate` locale contiene fix manuali sui publish/eventi startup; la patch GitHub preferisce correggere l'allowlist heap in `provider_runtime_heap.py` cosi' `context_memory` resta una lane reale e non viene degradato a broker.

## Prossime priorita'

1. Portare localmente la patch branch o cherry-pick selettivo.
2. Eseguire smoke applicability.
3. Rigenerare revision context dalla run `20260512-144115`.
4. Lanciare resume run.
5. Se GPU1 ripete sketch, patchare il contratto provider/rewrite prompt per trasformare `rewrite_non_concrete_candidates` in vincolo hard, non in consiglio testuale.
