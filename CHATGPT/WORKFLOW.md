# WORKFLOW.md — IA-Carmine Heap Universe Workflow

## Scopo

Questo documento descrive il workflow canonico dell'universo heap: tool obbligatori, memoria, chunk, pointer, salti, composer, revision context e prodotti finali.

Non certifica che l'implementazione corrente funzioni end-to-end. Definisce il contratto da rispettare.

## Obiettivo

Trasformare una richiesta operativa in un ciclo verificabile:

```text
request
→ task contract
→ preflight
→ startup reload
→ heap state
→ memoria
→ chunk
→ tool evidence
→ provider lanes
→ proposal blocks
→ pointer graph
→ composer
→ revision context
→ postrun package
→ code product se verificato
```

## Strati dell'universo heap

```text
User request
→ task contract
→ preflight
→ required context initializer
→ startup context/memory reload
→ memoria consistente SQLite/FTS5
→ memoria volatile heap runtime
→ chunking source/evidence/proposal
→ broker tool evidence
→ provider lanes GPU1/GPU0/NPU
→ quality gates
→ proposal blocks
→ pointer graph
→ salti next/previous/refines/resume
→ old composer
→ external long response
→ revision context
→ postrun package
→ code product gate
```

## 1. Task contract

La richiesta utente deve diventare contratto operativo:

```text
objective
scope
non-goals
allowed actions
forbidden actions
target output
required evidence
validation commands
acceptance criteria
block conditions
```

## 2. Preflight

Verifica:

```text
repo root
Python venv
tool disponibili
policy locali
required context files
smoke minimi
guardrail
```

Il preflight non produce prodotto finale. Blocca o degrada la run.

## 3. Required context initializer

I file required non vanno rimossi per far passare il test.

Regola:

```text
presente → ok
mancante ma inizializzabile → crea template + evidence
mancante non inizializzabile → blocca
```

Output:

```text
startup_required_ai_context_files.json
startup_required_ai_context_files.md
```

## 4. Startup context/memory reload

Tool concettuale:

```text
Tools/ai/prepare_heap_context_memory_reload.py
```

Carica:

```text
required context files
repo docs map
tool catalog
shared memory inventory
operational memory status
operational memory search
transient request context
semantic code chunks
AI context pack
AI context pack evidence
semantic evidence chunks
heap startup task file
```

Output:

```text
startup_context_memory_reload/
  heap_context_memory_reload_manifest.json
  heap_startup_input_ready_context.md
  startup_required_ai_context_files.json
  startup_repo_docs_map.json
  startup_semantic_code_chunks.json
  startup_tool_catalog.json
  startup_memory_inventory.json
  startup_operational_memory_status.json
  startup_operational_memory_search.json
  startup_transient_request_context.json
  startup_ai_context_pack/
  startup_ai_context_pack_evidence/
  startup_semantic_evidence_chunks.json
```

Regola:

```text
heap_startup_input_ready_context.md deve essere letto come contenuto
e pubblicato nello heap prima del ciclo provider.
```

## 5. Memoria volatile

Stato della run corrente:

```text
heap_exchange_runtime_state.jsonl
heap_runtime_exit_output.json
heap_exchange_runtime_exit_product.json
startup_transient_request_context
runtime facts
provider round state
scratch state
temporary decisions
```

Serve per coordinare GPU1/GPU0/NPU durante il ciclo.

## 6. Memoria consistente — SQLite / SQLite FTS5

Obbligatoria.

Contiene:

```text
sessions
runs
tasks
facts
decisions
artifact refs
tool executions
provider outputs
proposal blocks
accepted/rejected decisions
symbol discoveries
file/path evidence
validation results
revision contexts
```

Operazioni minime:

```text
write_fact
write_decision
write_artifact_ref
write_rejected_block
write_accepted_block
write_symbol_discovery
search_facts
search_decisions
search_similar_errors
search_previous_targets
```

Distinzione:

```text
memoria volatile = stato run corrente
memoria consistente = memoria interrogabile fra run
```

## 7. Chunk

Tipi:

```text
source/code chunks
semantic code chunks
semantic evidence chunks
context chunks
memory chunks
proposal chunks
provider chunks
audit chunks
long response chunks
code product chunks
```

Ogni chunk deve avere:

```text
id
kind
source_path
content/hash
role
producer
consumer
quality
accept/reject status
pointer links se applicabile
```

## 8. Broker tool evidence

Il broker collega tool e heap.

Output per ogni tool:

```text
tool request
tool execution
returncode
stdout/stderr tail
artifact refs
summary
passed/failed
side effects
guardrail flags
```

Tool/requisiti minimi:

```text
tool_catalog → build_agent_agnostic_tool_inventory
shared_memory → build_agent_memory_inventory
operational_memory_write/search → runtime_sqlite_memory
shared_context_chunks → build_agent_transient_request_context
semantic_code_chunks → select_semantic_code_chunks
ai_context_pack → build_ai_context_pack
semantic_evidence_chunks → build_semantic_evidence_chunks
validation_evidence → validation tools
```

## 9. Provider lanes

### GPU1 planner

- autore primario;
- consuma heap, startup, revision context;
- produce proposal chunks;
- può avanzare e tornare indietro;
- propaga import/variabili/classi/funzioni scoperte tardi;
- riprende da `resume_from_block_id`.

### GPU0 reviewer/refiner

- rivaluta pointer vecchi;
- propone refinement;
- verifica concretezza;
- blocca path inventati;
- propone refines/resume.

### NPU auditor

- audita guardrail;
- placeholder/stub;
- path inventati;
- source writes non dichiarati;
- provider execution falsa;
- patch application non autorizzata;
- accetta o respinge.

## 10. Proposal iterations

Output:

```text
team_context/proposal_iterations/heap_proposal_revision_*.json
team_context/proposal_iterations/heap_proposal_revision_*.md
```

Formato minimo:

```text
TARGET_FILES
PROBLEM
EVIDENCE
IMPLEMENTATION_CHANGES
CODE_OR_PATCH_SKETCH
VALIDATION_COMMANDS
RISKS
EXIT_DECISION
POINTER_ACTION
```

Bloccare se:

```text
TODO
pass
placeholder
stub
path/to/artifact
file inventati
target non verificati
validation command inventati
similarity=1.000 senza progresso
```

## 11. Quality gates

Devono bloccare:

```text
proposta generica
placeholder/stub
path inventati
source writes non dichiarati
patch application non autorizzata
provider execution falsa
output senza target
code product senza diff
diff senza validazione
```

## 12. Pointer graph

Non è diagnostica. È product contract.

Edge:

```text
next
previous
refines
resume_from
```

Significato:

```text
next = avanzamento forward
previous = navigazione indietro
refines = blocco che corregge blocco precedente
resume_from = punto da cui riprendere dopo backtracking
```

Separazione:

```text
pointer graph = prodotto/runtime contract
provider_execution_performed = evidenza separata di provider/workload
```

## 13. Salti operativi

### Forward

```text
proposal_001 → proposal_002 → proposal_003
```

### Backward

```text
proposal_003 scopre import sqlite3
→ torna a proposal_001/proposal_002
→ propaga simbolo/contratto
→ riprende da proposal_003
```

### Refine

```text
proposal_004 refines proposal_002
```

### Resume

```text
dopo correzione, riprendi dal resume_from_block_id
```

### Peer

```text
GPU1 continua avanti
GPU0 rivaluta pointer vecchi
NPU audita pointer vecchi
```

## 14. Revision context

Tool:

```text
Tools/ai/build_external_heap_revision_context.py
```

Output:

```text
external_heap_revision_context.json
external_heap_revision_context.md
```

Campi:

```text
protocol
source_pointer_protocol
can_resume_universe
product_acceptance_status
resume_from_block_id
latest_block_id
parallel_task_count
gpu1_task_count
gpu0_task_count
npu_task_count
tasks[]
runtime_instruction
priority_next_action
```

Task:

```text
gpu1_rewrite_rejected_block
gpu1_backpropagate_symbol_contract
gpu0_parallel_recheck_old_pointer
npu_parallel_guardrail_audit_old_pointer
verify_patchable_target
resume_forward_from_block
```

## 15. Composer vecchio

Output canonici:

```text
heap_final_proposal_composer.json
heap_final_proposal_composer.md
aicarmine_heap_final_proposals_*.txt
aicarmine_heap_final_proposals_*.md
aicarmine_heap_final_proposals_*.json
proposal_chunks/
proposal_chunks_txt/
DOWNLOADS.txt
```

Resta parte dell'output. Non va sostituito.

## 16. External long response composer

Tool:

```text
Tools/ai/compose_external_heap_block_response.py
```

Output:

```text
external_heap_primary_long_response.md
external_heap_primary_long_response.json
```

Scopo:

```text
ricostruire risposta lunga da blocchi persistenti
superare limite token
mostrare risposta completa e parti
includere rejected history
includere peer blocks
```

Si aggiunge al composer vecchio.

## 17. Postrun package

Tool:

```text
Tools/ai/run_external_heap_postrun_package.py
```

Scopo:

```text
selezionare solo run complete
raccogliere output vecchio e nuovo
copiare in Documents
scrivere download manifest
```

Output:

```text
C:\Users\carmi\Documents\aicarmine_heap_final_proposals_<stamp>\
```

Contenuti attesi:

```text
aicarmine_heap_final_proposals_*.txt
aicarmine_heap_final_proposals_*.md
aicarmine_heap_final_proposals_*.json
aicarmine_heap_final_proposals_*_DOWNLOADS.txt
external_heap_primary_long_response.md
external_heap_primary_long_response.json
external_heap_revision_context.json
external_heap_revision_context.md
external_heap_block_pointer_manifest.json
proposal_chunks/
proposal_chunks_txt/
```

## 18. Code product gate

Il code product esiste solo con:

```text
target file verificati
patch candidate
diff reale
validation command reale
source writes dichiarati se avvenuti
guardrail passati
```

Output:

```text
FINAL_READABLE_PRODUCT.md
CODE_PRODUCT_FULL_PATCH.md
code product zip
code execution matrix
patch candidate report
```

Se manca target/diff:

```text
NO_TARGETS_OR_CODE_PRODUCT
```

Non è un prodotto.

## 19. Run directory

```text
output/validation/heap_context_closure_<stamp>/
```

Contiene:

```text
heap_runtime_context_closure_launcher.json
heap_context_preflight_gate.json
heap_context_preflight_gate.md
startup_context_memory_reload/
heap_runtime_completeness_gate_report.json
heap_runtime_completeness_gate_report.md
heap_exchange/
broker_bridge/tool_outputs/
provider_teamwork/
team_context/
heap_final_proposal_composer.json
heap_final_proposal_composer.md
heap_final_causality_normalized.json
external_heap_block_pointer_manifest.json
external_heap_primary_long_response.md
external_heap_primary_long_response.json
external_heap_revision_context.json
external_heap_revision_context.md
external_heap_postrun_package.json
```

## 20. Builder command

Il builder non lancia run:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy .\Tools\ai\build_heap_runtime_launcher_command.py `
  --repo-root . `
  --profile balanced_external_heap `
  --include-postrun-package-command `
  --output .\output\validation\heap_launcher_command_balanced.json
```

## 21. Run diretta

```powershell
cd C:\Users\carmi\blender\blender-audio-project

$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy .\Tools\ai\run_heap_runtime_context_closure.py `
  --repo-root . `
  --python-exe $RepoPy `
  --request "Run heap esterno BALANCED: preload completo, startup reload, GPU1 planner, GPU0 reviewer/refiner, NPU audit, chunk/pointer/revision context, proposal chunks concreti, blocco placeholder/stub." `
  --budget-minutes 10 `
  --max-iterations 4 `
  --max-provider-revisions 3 `
  --timeout-seconds 1200 `
  --preflight-timeout-seconds 120 `
  --npu-device-workload-seconds 5.0 `
  --npu-device-workload-iterations 5000 `
  --startup-max-memory-chars 64000 `
  --startup-max-context-files 80 `
  --startup-max-chars-per-file 12000 `
  --allow-provider-generation
```

## 22. Postrun

```powershell
& $RepoPy .\Tools\ai\run_external_heap_postrun_package.py `
  --repo-root . `
  --include-rejected-history `
  --include-peer-blocks
```

## 23. Verifiche

```powershell
$RunDir = Get-ChildItem .\output\validation -Directory |
  Where-Object Name -like "heap_context_closure_*" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

Get-Content (Join-Path $RunDir.FullName "heap_runtime_context_closure_launcher.json") -Raw | ConvertFrom-Json |
  Select-Object preflight_passed,startup_reload_passed,heap_passed,composer_passed,launcher_passed,composer_documents_dir

Get-Content (Join-Path $RunDir.FullName "external_heap_revision_context.json") -Raw | ConvertFrom-Json |
  Select-Object product_acceptance_status,resume_from_block_id,latest_block_id,parallel_task_count,gpu1_task_count,gpu0_task_count,npu_task_count
```

## 24. Successo

Una run è utile se produce:

```text
startup reload
heap report
provider_teamwork
proposal_iterations
pointer manifest
external long response
revision context
postrun package
Documents output
```

Una run è code product solo se produce:

```text
target verificati
diff reale
patch candidate valida
CODE_PRODUCT_FULL_PATCH applicabile
```

## 25. Fallimento

Fallire esplicitamente se:

```text
Matrix concrete proposal count = 0
Matrix code product count = 0
Generated code product count = 0
Patch candidate report = None
Verified target count = None
NO_TARGETS_OR_CODE_PRODUCT
```

## 26. Regola finale

```text
Non basta che la macchina giri.
Non basta che scriva report.
Non basta che produca pointer.
Non basta che crei una long response.

Il sistema funziona solo quando conserva memoria, recupera decisioni, produce blocchi verificabili, compone output lungo, genera revision context e, quando richiesto, produce diff reale validato.
```
