
Di seguito descrivo l’architettura dell’universo heap come emerge dai log, dagli artifact e dai documenti caricati, senza sostenere che oggi funzioni end-to-end. È una descrizione del contratto progettuale e del wiring osservato, non una certificazione di qualità.

1. Definizione: cosa è “universo heap”

L’universo heap non è un singolo script, non è il composer, non è il pointer manifest, non è un bundle ZIP e non è la chat.

È il runtime operativo persistente in cui una richiesta entra, viene trasformata in stato condiviso, passa attraverso tool/evidence/provider, genera blocchi di proposta, viene collegata tramite pointer graph, viene composta in output leggibile e produce contesto per la run successiva.

La forma sintetica corretta è:

user request
→ preflight
→ startup reload contesto/memoria/tool/docs
→ heap state condiviso
→ broker/tool evidence
→ provider lanes GPU1/GPU0/NPU
→ proposal iterations
→ pointer graph
→ composer finale
→ post-run package
→ revision context per run successiva

Nei documenti caricati questo concetto è espresso chiaramente: la chat non deve essere la memoria/coscienza del progetto; deve essere solo un client verso uno stato operativo condiviso. La memoria, le decisioni, i vincoli e il prodotto vivono negli artifact/runtime heap.

2. Principio centrale

Il principio fondante è:

La chat non conosce il progetto.
Il progetto deve costringere l’IA a leggere stato, artifact, contratti, pointer e revision context.

Quindi l’universo heap serve a superare il limite classico della chat:

prompt singolo
contesto volatile
memoria non affidabile
risposte lunghe tagliate
decisioni perse
patch scollegate

sostituendolo con:

artifact persistenti
state condiviso
evidence verificabile
pointer graph
revision context
composer file-based
postrun package
run successive che riprendono da stato precedente

Questo è il punto più importante: l’IA non deve ricordare; deve recuperare e consumare stato esterno.

3. Entry point: builder ≠ runner

Qui c’è una distinzione fondamentale.

build_heap_runtime_launcher_command.py

È un command builder. Genera il comando da eseguire, ma non lancia la run.

Questa distinzione era già stata identificata nei log: il builder “prints/writes a command” e stampa la command line; il launcher vero è Tools/ai/run_heap_runtime_context_closure.py.

Quindi:

build_heap_runtime_launcher_command.py
= produce comando / JSON comando / profilo run
≠ esegue universo heap
run_heap_runtime_context_closure.py

È il runtime launcher effettivo. È il punto che orchestra:

preflight
startup reload
heap runtime completeness gate
composer
post-run package
revision context

Il comando generato dal builder è solo una condizione di ingresso. La run è reale solo se dopo l’esecuzione compaiono artifact runtime: heap exchange, provider_teamwork, proposal iterations, pointer manifest, composer output, revision context. Nei log è stato detto esplicitamente: “il comando è solo una condizione di ingresso; la run universo è provata solo dagli artifact prodotti durante l’esecuzione”.

4. Fase 1 — Request / Task contract

La richiesta utente non dovrebbe rimanere solo testo nel prompt.

Deve diventare un task contract operativo:

request originale
→ obiettivo
→ regole
→ vincoli
→ path reali
→ divieti
→ formato output atteso
→ criteri di blocco

Esempio di richiesta corretta:

Run heap esterno BALANCED:
- usa preload completo repo/docs/memoria/tool
- scrivi startup reload nella operational scratch memory
- usa GPU1 planner, GPU0 reviewer/refiner, NPU audit
- gestisci output oltre il contesto tramite artifact/chunk/pointer
- produci proposal chunks concreti con path repo reali
- blocca placeholder/stub

Se questo resta solo prompt testuale, non è ancora universo heap. Deve entrare nello stato condiviso e negli artifact.

5. Fase 2 — Preflight

Il preflight verifica la base minima prima di far partire il runtime.

Dovrebbe controllare:

repo root valida
python del progetto
tool disponibili
file richiesti
policy locali
smoke minimi
guardrail
assenza di condizioni bloccanti

Il preflight non deve produrre il prodotto finale. Deve decidere se il runtime può procedere.

Errore osservato in passato: il launcher poteva dichiarare startup_reload_performed=true e startup_reload_passed=true anche quando la preflight aveva impedito lo startup reale; questo generava heap senza contesto e provider non partiti.

Contratto corretto:

preflight fallisce
→ startup non deve risultare performed/passed
→ launcher deve bloccare o degradare esplicitamente
6. Fase 3 — Startup reload

Questa è una delle fasi più importanti.

Il tool centrale è:

Tools/ai/prepare_heap_context_memory_reload.py

Scopo: caricare prima del ciclo provider tutto ciò che serve per rendere l’heap uno stato operativo e non una chat lunga.

Dovrebbe raccogliere:

required context files
repo docs map
tool catalog
shared memory
operational memory status
operational memory search
transient request context
semantic code chunks
AI context pack
AI context pack evidence
semantic evidence chunks
heap startup task file

Nel tuo output recente, una startup corretta produceva artifact come:

startup_required_ai_context_files.json/.md
startup_repo_docs_map.json/.md
startup_semantic_code_chunks.json/.md
startup_tool_catalog.json/.md
startup_memory_inventory.json/.md
startup_operational_memory_status.json/.md
startup_operational_memory_search.json/.md
startup_transient_request_context.json/.md
startup_ai_context_pack/*.json/*.md
startup_semantic_evidence_chunks.json/.md
heap_startup_input_ready_context.md

Il task file heap_startup_input_ready_context.md non deve essere solo un path: deve essere letto e pubblicato dentro l’heap prima del ciclo provider. Nei log passati era stato individuato proprio il bug “gate legge path ma non contenuto”.

Contratto corretto:

startup reload
→ produce task file + artifact
→ task file viene letto
→ contenuto entra nello heap state
→ provider consumano quello stato
7. Fase 4 — Heap runtime completeness gate

Il gate è il ciclo operativo centrale.

Nome osservato:

Tools/ai/run_heap_runtime_completeness_gate.py

Il suo ruolo non dovrebbe essere “generare una risposta finale”, ma:

leggere heap/context
coordinare broker/tool evidence
preparare input provider
raccogliere provider outputs
validare qualità
produrre proposal iterations
scrivere heap exchange runtime state
decidere product_status

Artifact attesi:

heap_runtime_completeness_gate_report.json
heap_runtime_completeness_gate_report.md
heap_exchange/heap_runtime_exit_output.json
heap_exchange/heap_exchange_runtime_exit_product.json
heap_exchange/heap_exchange_runtime_state.jsonl
team_context/proposal_iterations/*
provider_teamwork/*
broker_bridge/tool_outputs/*

Il gate dovrebbe bloccare quando:

proposal generiche
placeholder/stub
path inventati
file non verificati
source writes non dichiarati
provider execution non provata
patch applicate senza permesso
8. Broker / tool evidence

Il broker porta dentro l’heap evidenze reali.

Esempi di requisiti/tool osservati nei log:

tool_catalog
shared_memory
operational_memory_write
operational_memory_search
shared_context_chunks
semantic_code_chunks
ai_context_pack
semantic_evidence_chunks
validation_evidence

Esempi di tool coinvolti:

build_agent_agnostic_tool_inventory
build_agent_memory_inventory
runtime_sqlite_memory
build_agent_transient_request_context
select_semantic_code_chunks
build_ai_context_pack
build_semantic_evidence_chunks
run_gpu_planner_json_contract_smoke

Questi artifact non sono il prodotto. Sono evidence substrate: il materiale che GPU1/GPU0/NPU devono consumare.

9. Provider lanes

L’universo heap prevede più lane operative. Il concetto ricorrente è:

GPU1 = planner/autore primario
GPU0 = reviewer/refiner parallelo
NPU = auditor/guardrail leggero
GPU1 planner

Ruolo:

legge heap state
consuma startup context
consuma revision context
produce proposal chunks
può avanzare e tornare indietro sui pointer
può scoprire import/variabili/classi/funzioni tardi
può generare task di propagazione sui blocchi precedenti
riprende poi dal resume_from_block_id

Questa è una parte forte del tuo concetto: GPU1 non deve solo scrivere avanti. Se scopre un simbolo necessario tardi, deve poter tornare indietro, propagare il contratto, far rivalutare e poi riprendere il flusso forward.

GPU0 reviewer/refiner

Ruolo:

rivaluta blocchi vecchi
propone refines_block_id
propone resume_from_block_id
verifica concretezza
verifica path repo reali
rileva placeholder/stub
può lavorare in parallelo sui pointer vecchi
NPU auditor

Ruolo:

audit leggero
guardrail
placeholder/stub
path inventati
source writes non dichiarati
provider execution falsa
patch_application falsa
ripetizioni
decisione accept/reject

Nei log e negli output compaiono tasks tipo:

gpu0_parallel_recheck_old_pointer
npu_parallel_guardrail_audit_old_pointer
gpu1_rewrite_rejected_block
gpu1_backpropagate_symbol_contract

Questo è il cuore dell’idea “non lineare”: il lavoro non è solo avanti; è avanti/indietro con revisione parallela.

10. Proposal iterations

Le proposal iterations sono blocchi persistenti, non una risposta unica.

Path tipico:

team_context/proposal_iterations/heap_proposal_revision_*.json
team_context/proposal_iterations/heap_proposal_revision_*.md

Ogni proposal block dovrebbe avere almeno:

TARGET_FILES
PROBLEM
EVIDENCE
IMPLEMENTATION_CHANGES
CODE_OR_PATCH_SKETCH oppure PATCH_SKETCH
VALIDATION_COMMANDS
RISKS
EXIT_DECISION
POINTER_ACTION
CURRENT_POINTER

Se un proposal block contiene:

TODO
pass
placeholder
path/to/artifact
src/falso.py
file non esistente
diff non verificato

deve essere rejected.

L’external long response che hai caricato mostra proprio questo problema: il blocco contiene un path inventato src/agent_review_decision_loop.py, validation command inventati e blocking issues che dichiarano source refs non verificati e path non allowlisted.

Quindi il sistema ha già un detector concettuale: la proposta può essere ricostruita, ma deve essere bloccata se inventa path o produce patch non fondate.

11. Pointer graph

Questo è uno dei nuclei più importanti.

Il pointer graph non è diagnostica passiva. È:

product contract
decision recovery
long response composition
navigation graph
runtime continuation state

Il contratto corretto emerso è:

pointer graph = prodotto/runtime contract
provider_execution_performed = flag separato di evidenza provider/workload

Nei log è scritto esplicitamente che la frase “i pointer sono solo diagnostica” era sbagliata. I pointer servono a ricostruire output lungo, recuperare decisioni vecchie, capire rejected/accepted, abilitare GPU0/NPU su blocchi vecchi, abilitare backtracking GPU1 e preparare revision context.

Tipi di edge:

next
previous
refines
resume_from

Significato:

next:
  continua la catena forward

previous:
  permette navigazione indietro

refines:
  questo blocco corregge/raffina un blocco precedente

resume_from:
  indica dove riprendere dopo backtracking/correzione

Ogni block può contenere:

block_id
block_type
role
step_index
source_path
markdown_path
previous_block_id
next_block_id
refines_block_id
resume_from_block_id
quality_passed
accepted
sha256
preview
pointer_contract

Esempio di contratto corretto osservato nell’external long response:

product_contract=True
decision_recovery=True
supports_forward_navigation=True
supports_backrefinement=True
supports_resume=True
provider_execution_is_separate_guardrail=True

12. Composer vecchio vs external composer

Ci sono due livelli.

Composer “vecchio”

Produce output canonici della run:

heap_final_proposal_composer.json
heap_final_proposal_composer.md
aicarmine_heap_final_proposals_*.txt
aicarmine_heap_final_proposals_*.md
aicarmine_heap_final_proposals_*.json
proposal_chunks/
proposal_chunks_txt/
DOWNLOADS.txt

Questo composer non deve essere sostituito.

External heap block response composer

Tool osservato:

Tools/ai/compose_external_heap_block_response.py

Produce:

external_heap_primary_long_response.md
external_heap_primary_long_response.json

Scopo:

ricostruire una risposta lunga file-based
usando blocchi persistenti e pointer
oltre la finestra token del provider

L’external long response dichiara infatti che è “l’output principale file-based dell’heap esterno” e che ricostruisce risposta lunga usando blocchi persistenti e puntatori come product contract, non la singola finestra token del provider.

Contratto corretto:

composer vecchio resta output base
external long response si aggiunge
postrun package raccoglie entrambi
Documents package deve contenere entrambi
13. Post-run package

Tool osservato:

Tools/ai/run_external_heap_postrun_package.py

Scopo:

prendere l’ultima run completa valida
raccogliere composer vecchio
raccogliere pointer manifest
raccogliere long response
raccogliere revision context
copiare/impacchettare output finale in Documents

Output tipico:

C:\Users\carmi\Documents\aicarmine_heap_final_proposals_<stamp>\

Contenuti attesi:

aicarmine_heap_final_proposals_<stamp>.txt
aicarmine_heap_final_proposals_<stamp>.md
aicarmine_heap_final_proposals_<stamp>.json
aicarmine_heap_final_proposals_<stamp>_DOWNLOADS.txt
external_heap_primary_long_response.md
external_heap_primary_long_response.json
external_heap_revision_context.json
external_heap_revision_context.md
proposal_chunks/
proposal_chunks_txt/

La parte importante: il postrun deve selezionare solo run complete, non output parziali/fallback. Nei log caricati compare proprio il tema della “run selection guard” e del caricare revision context solo da run complete.

14. Revision context

Tool osservato:

Tools/ai/build_external_heap_revision_context.py

Output:

external_heap_revision_context.json
external_heap_revision_context.md

Scopo: trasformare il prodotto bloccato o parzialmente riuscito in lavoro operativo per la run successiva.

Campi osservati:

protocol
source_pointer_protocol
causal_chain_status
product_acceptance_status
proposal_block_count
gpu0_block_count
npu_block_count
resume_from_block_id
latest_block_id
parallel_task_count
gpu1_task_count
gpu0_task_count
npu_task_count
tasks[]
runtime_instruction

Tipi task osservati:

gpu1_rewrite_rejected_block
gpu1_backpropagate_symbol_contract
gpu0_parallel_recheck_old_pointer
npu_parallel_guardrail_audit_old_pointer

Questo è il meccanismo che rende l’universo multi-ciclo:

ciclo 1:
  request nuova
  → heap/provider/composer/postrun
  → crea external_heap_revision_context.json

ciclo 2:
  consuma external_heap_revision_context.json del ciclo 1
  → riscrive/rivaluta/propaga
  → produce nuovo revision context

ciclo 3:
  consuma quello del ciclo 2

Nei log caricati è espresso chiaramente: il resume non deve stare fuori dal concetto di universo; è il ciclo successivo dello stesso universo.

15. COLD RUN vs RESUME RUN
Cold run

È la prima run di una sessione universo:

nessun revision context precedente
carica repo/docs/memoria/tool
produce prima catena proposal/pointer
produce primo postrun package
produce primo revision context
Resume run

Non è una modalità concettualmente separata. È il ciclo successivo.

legge revision context precedente
consuma tasks[]
riscrive rejected blocks
propaga simboli indietro
fa rivalutare GPU0/NPU vecchi pointer
riprende da resume_from_block_id
produce nuovi blocchi
produce nuovo revision context

Il problema tecnico attuale è che external_heap_revision_context.json nasce dopo il primo ciclo; quindi una singola run non può consumare un revision context che ancora non esiste. Per testare l’universo completo serve una sessione multi-ciclo.

16. Provider execution guardrail

provider_execution_performed non deve essere vero solo perché esistono blocchi provider/pointer.

Deve essere vero solo se c’è evidenza esplicita:

provider_execution_performed=True
workload_performed=True
provider report reale
GPU/NPU workload reale

Quindi:

pointer block presente
≠ provider execution provata

Questo serve a impedire che il grafo prodotto falsifichi l’esecuzione.

Contratto:

pointer graph = prodotto / continuità / decision recovery
provider_execution_performed = evidenza separata di workload/provider reale

Questo è documentato nei log relativi alla correzione semantica dei pointer.

17. Code product layer

Questo è lo strato che oggi risulta più debole.

Output atteso:

FINAL_READABLE_PRODUCT.md
CODE_PRODUCT_FULL_PATCH.md
bundle zip finale
diff reale
patch candidate
matrix

Ma l’artifact CODE_PRODUCT_FULL_PATCH.md che hai caricato mostrava:

Matrix concrete proposal count: 0
Matrix code product count: 0
Generated code product count: 0
Patch candidate report: None
Patch candidate passed count: 0
Verified target count: None
Code product status: NO_TARGETS_OR_CODE_PRODUCT

Quindi, per quello specifico caso, non era un prodotto applicabile.

Nel contratto corretto, il code product deve nascere solo se esiste almeno:

target reale
diff reale
patch candidate validato
source file verificato
validation command coerente

Se no, deve fallire prima, non produrre un file finale vuoto mascherato da prodotto.

18. Output principali dell’universo
Run directory
output/validation/heap_context_closure_<stamp>/

Contiene:

heap_runtime_context_closure_launcher.json
heap_context_preflight_gate.json/.md
startup_context_memory_reload/
heap_runtime_completeness_gate_report.json/.md
heap_exchange/
broker_bridge/tool_outputs/
provider_teamwork/
team_context/
heap_final_proposal_composer.json/.md
heap_final_causality_normalized.json
external_heap_block_pointer_manifest.json
external_heap_primary_long_response.md/.json
external_heap_revision_context.json/.md
external_heap_postrun_package.json
Startup reload outputs
startup_required_ai_context_files.*
startup_repo_docs_map.*
startup_semantic_code_chunks.*
startup_tool_catalog.*
startup_memory_inventory.*
startup_operational_memory_status.*
startup_operational_memory_search.*
startup_transient_request_context.*
startup_ai_context_pack/*
startup_ai_context_pack_evidence/*
startup_semantic_evidence_chunks.*
heap_startup_input_ready_context.md
Provider outputs
provider_teamwork/gpu1_*.json
provider_teamwork/gpu0_*.json
provider_teamwork/npu_*.json
Proposal outputs
team_context/proposal_iterations/heap_proposal_revision_*.json
team_context/proposal_iterations/heap_proposal_revision_*.md
proposal_chunks/
proposal_chunks_txt/
Product graph outputs
external_heap_block_pointer_manifest.json
external_heap_primary_long_response.md
external_heap_primary_long_response.json
external_heap_revision_context.json
external_heap_revision_context.md
Human/operator package
C:\Users\carmi\Documents\aicarmine_heap_final_proposals_<stamp>\
19. Test di verità: cosa prova una run reale

Non basta:

il builder stampa un comando
il comando contiene --allow-provider-generation
il comando contiene revision context nel prompt
un JSON viene scritto
uno smoke passa

Una run universo reale è provata da:

heap_exchange_runtime_state.jsonl popolato
startup_reload_passed true o degraded dichiarato con artifact utili
provider_teamwork/*.json con GPU1/GPU0/NPU reali
provider_execution_performed vero solo se fondato
proposal_iterations nuovi
pointer manifest con nuovi proposal/provider blocks
revision context aggiornato
composer con proposta concreta oppure blocco motivato
postrun package completo
Documents output coerente

Nei log è formulato chiaramente: il livello comando può sembrare corretto, ma il livello universo è dimostrato solo dagli artifact runtime.

20. Il flusso completo in schema
[Operatore]
   |
   v
[Request / Task Contract]
   |
   v
[build_heap_runtime_launcher_command.py]
   |   solo genera comando
   v
[run_heap_runtime_context_closure.py]
   |
   +--> [Preflight]
   |
   +--> [prepare_heap_context_memory_reload.py]
   |       - required files
   |       - repo docs
   |       - memory
   |       - tool catalog
   |       - context pack
   |       - semantic chunks
   |       - startup task file
   |
   +--> [run_heap_runtime_completeness_gate.py]
   |       |
   |       +--> [Broker / Tool Evidence]
   |       |
   |       +--> [Heap Exchange State]
   |       |
   |       +--> [Provider Lanes]
   |              - GPU1 planner
   |              - GPU0 reviewer/refiner
   |              - NPU auditor
   |
   +--> [Proposal Iterations]
   |       - revision_000
   |       - revision_001
   |       - ...
   |
   +--> [Composer vecchio]
   |       - heap_final_proposal_composer.*
   |       - aicarmine_heap_final_proposals.*
   |
   +--> [Pointer Manifest]
   |       - external_heap_block_pointer_manifest.json
   |
   +--> [External Long Response]
   |       - external_heap_primary_long_response.*
   |
   +--> [Revision Context]
   |       - external_heap_revision_context.*
   |
   +--> [Postrun Package]
           - Documents/aicarmine_heap_final_proposals_<stamp>/
21. Stato concettuale attuale

Come lo conosco io, il progetto non è “un agente”. È un tentativo di costruire un runtime di coordinamento dove:

chat = client
heap = stato operativo
tool = sensori/attuatori
provider lanes = entità operative
pointer graph = prodotto navigabile e memoria decisionale
composer = ricostruzione output
revision context = continuità fra cicli
postrun package = consegna operatore

La parte forte del concetto è il superamento del limite della chat tramite stato esterno persistente.

La parte debole osservata è che spesso il sistema ha dimostrato:

artifact generation
reporting
smoke passing
diagnostica strutturata

ma non sempre:

diff reale
patch candidate valida
code product applicabile
target verificato

Quindi l’universo heap, come architettura, è questo:

un sistema a cicli persistenti che dovrebbe trasformare richieste operative in blocchi di proposta verificabili, navigabili, revisionabili e componibili in prodotto finale.

Ma lo stato operativo reale mostrato dagli artifact è più prudente:

il runtime può produrre stato, pointer, long response e revision context;
il code product applicabile non è ancora dimostrato come affidabile.
aggiungi anhce i tool che nono possso moancare come  sqllite sqlliteff5 memoria consistente, memeoria volatile, chiunk, oponter, i salti per i prodotti  spiega tiutto
Ragionato per 44s

Sì. Nell’architettura dell’universo heap vanno esplicitati anche i tool/substrati obbligatori, perché senza quelli “heap” resta solo una sequenza di script. La formulazione corretta è: l’universo heap non è solo provider + composer; è un sistema con memoria persistente, memoria volatile, chunking, pointer graph, salti di revisione, strumenti di evidenza e prodotti finali componibili.

1. Strati obbligatori dell’universo heap

Schema completo:

User request
→ task contract
→ preflight
→ required context initializer
→ startup context/memory reload
→ memoria consistente
→ memoria volatile heap runtime
→ chunking source/evidence/proposal
→ broker tool evidence
→ provider lanes GPU1/GPU0/NPU
→ proposal blocks
→ pointer graph
→ salti forward/back/refine/resume
→ composer vecchio
→ external long response
→ revision context
→ postrun package
→ code product / final readable product

Il principio resta: la chat non è la memoria; la memoria sta in heap, artifact, pointer, SQLite, chunk e revision context. Nei file caricati il concetto è esplicito: la chat è solo un client, mentre memoria, decisioni, vincoli e prodotto devono vivere nell’heap runtime.

2. Tool che non possono mancare
A. SQLite / SQLite FTS5: memoria consistente

Quando dici sqliteff5, tecnicamente lo leggo come SQLite + FTS5, cioè SQLite persistente con full-text search.

Questo strato non è opzionale. Serve a dare memoria consistente, non volatile.

Deve contenere almeno:

sessions
runs
tasks
facts
decisions
artifacts
tool executions
provider outputs
proposal blocks
accepted/rejected decisions
symbol discoveries
file/path evidence
validation results
revision contexts

Ruolo:

memoria persistente
recupero decisionale
ricerca full-text
indicizzazione per run/progetto/task
base per revision context
base per future run

Senza SQLite/FTS5, ogni run dipende da file sparsi sotto output/validation/** e la memoria diventa fragile.

Contratto minimo:

SQLite = stato storico affidabile
FTS5 = ricerca testuale su decisioni, blocchi, errori, path, simboli

Esempio concettuale:

runtime_sqlite_memory.write()
→ registra task, decisione, artifact, blocco, motivo reject

runtime_sqlite_memory.search()
→ recupera decisioni vecchie, bug simili, path già validati, blocchi respinti

Questo è diverso dai file JSON della run: i JSON sono artifact; SQLite è memoria interrogabile.

B. Memoria consistente vs memoria volatile
Memoria consistente

È quella che deve sopravvivere:

SQLite / FTS5
artifact indicizzati
revision context
pointer manifest
postrun package
decision history
accepted/rejected blocks

Serve per:

riprendere run future
non perdere decisioni
evitare che la chat debba ricordare
ricostruire perché un blocco è stato accettato o respinto
recuperare target/file/path già verificati
Memoria volatile

È lo stato vivo della run corrente:

heap_exchange_runtime_state.jsonl
heap_runtime_exit_output.json
heap_exchange_runtime_exit_product.json
startup_transient_request_context
working heap state
provider round state
broker scratch state
temporary facts
current task cursor

Serve per:

coordinare GPU1/GPU0/NPU nel ciclo attuale
passare evidenze tra provider
registrare stato incrementale
non perdere cosa è successo nel round corrente

Differenza secca:

memoria volatile = stato della run adesso
memoria consistente = memoria interrogabile fra run

Se una run produce solo volatile ma non persiste in SQLite/revision context, il sistema non impara.
Se persiste tutto ma non ha volatile runtime, il sistema non coopera in tempo reale.

Servono entrambe.

3. Chunk: unità operative dell’universo

I chunk non sono “pezzi di testo”. Sono unità operative tracciabili.

Tipi di chunk indispensabili:

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
Source / semantic code chunks

Servono a dare al modello porzioni reali di codice:

path repo-relative
range / simboli
hash
contenuto
ruolo
dipendenze note

Devono impedire path inventati.

Evidence chunks

Contengono output di tool e validatori:

py_compile
smoke
git diff --check
tool catalog
memory inventory
provider report
NPU audit
GPU0 review
Proposal chunks

Sono i blocchi prodotti da GPU1 e revisionati da GPU0/NPU.

Devono avere formato operativo:

TARGET_FILES
PROBLEM
EVIDENCE
IMPLEMENTATION_CHANGES
CODE_OR_PATCH_SKETCH
VALIDATION_COMMANDS
RISKS
EXIT_DECISION

Se mancano path reali o compaiono placeholder/stub, il blocco deve essere rejected.

Long response chunks

Servono a superare il limite token del provider. Il composer non deve affidarsi a una singola risposta lunga; deve ricostruire la risposta finale da blocchi persistenti.

Questo è coerente con il ruolo dichiarato del pointer context: product_graph_decision_recovery_and_long_response_composition.

4. Pointer graph: non diagnostica, ma product contract

Il pointer graph è uno dei nuclei del sistema.

Non è:

decorazione
diagnostica passiva
indice secondario

È:

product contract
decision recovery
navigation graph
long response composition graph
runtime continuation graph

Nel revision context caricato il pointer contract è esplicito:

product_contract = true
decision_recovery = true
supports_forward_navigation = true
supports_backrefinement = true
supports_resume = true
provider_execution_is_separate_guardrail = true

Questo vuol dire:

i pointer costruiscono il prodotto
ma non dimostrano da soli che il provider ha eseguito

Il flag provider_execution_performed deve restare separato: vero solo con evidenza reale di provider/workload.

5. Tipi di pointer / salti

I salti sono il meccanismo che rende l’universo non lineare.

next
blocco A → blocco B

Avanzamento normale.

Serve a dire:

continua da qui
questa è la prossima parte del prodotto
previous
blocco B → blocco A

Navigazione indietro.

Serve a ricostruire la catena e a recuperare contesto precedente.

refines
blocco B raffina blocco A

Serve quando un blocco corregge, riscrive o migliora un blocco precedente.

Esempio:

proposal_002 refines proposal_001
resume_from
dopo correzione/rifinitura, riprendi da questo blocco

È fondamentale per non perdere il cursore forward.

Esempio:

GPU1 scopre in proposal_003 che serve import sqlite3.
Genera task di propagazione verso proposal_001/proposal_002.
Poi resume_from = proposal_003.
Salto simbolico / propagation jump

Questo è il caso che hai descritto:

GPU1 sta scrivendo avanti.
Scopre una variabile/import/contratto necessario.
Torna indietro sui blocchi compatibili.
Propaga simbolo.
Fa rivalutare GPU0/NPU.
Riprende avanti.

Nel revision context è esplicitato: GPU1 può avanzare o tornare indietro; se scopre import, variabile, classe o contratto deve generare task di propagazione sui blocchi precedenti, far rivalutare GPU0/NPU e poi riprendere dal resume_from_block_id.

6. Revision context: il ponte fra una run e la successiva

Il revision context è il file che trasforma l’output precedente in lavoro operativo per la run successiva.

Output:

external_heap_revision_context.json
external_heap_revision_context.md

Campi fondamentali:

can_resume_universe
source_pointer_protocol
pointer_product_contract
pointer_contract_role
resume_from_block_id
latest_block_id
tasks[]
runtime_instruction
product_acceptance_status
candidate_applicability_summary
priority_next_action

Nel file caricato il sistema dichiara:

can_resume_universe = true
pointer_contract_role = product_graph_decision_recovery_and_long_response_composition
product_acceptance_status = blocked
priority_next_action = blocked_no_verified_target

Questo significa:

la run può riprendere
ma non deve inventare target
se non c’è target patchabile verificato, deve bloccare

Il revision context non è riassunto. È un piano operativo per la prossima run.

7. Tasks del revision context

I task sono i “salti” trasformati in lavoro schedulabile.

Tipi indispensabili:

rewrite_rejected_block
backpropagate_symbol_contract
parallel_recheck_old_pointer
parallel_guardrail_audit_old_pointer
resume_forward_from_block
verify_patchable_target
promote_candidate_to_code_product

Nel materiale caricato compaiono task reali come:

gpu1_rewrite_rejected_proposal_...
gpu1_propagate_symbols_...
gpu0_parallel_recheck_...
npu_parallel_audit_...

con istruzioni per riscrivere blocchi rejected, propagare import/variabili e far rivalutare vecchi pointer in parallelo.

GPU1 tasks
rewrite_rejected_block
backpropagate_symbol_contract
resume_forward
GPU0 tasks
parallel_recheck_old_pointer
refinement proposal
path/source validation
NPU tasks
parallel_guardrail_audit_old_pointer
placeholder/stub audit
source write audit
provider execution audit

Questo è il punto: il sistema non deve solo produrre una proposta nuova; deve produrre lavoro distribuito su vecchi e nuovi blocchi.

8. Tool obbligatori del runtime
8.1 Required context initializer

Serve a evitare che required files mancanti degradino la startup.

Funzione:

verifica file richiesti
inizializza file mancanti se safe
blocca se manca un file non inizializzabile
produce evidence

Non deve “rimuovere required files” per far passare il test. Deve inizializzarli o bloccare.

8.2 AI context pack builder

Serve a costruire il contesto canonico:

AGENTS.md
README
WORKFLOW
docs principali
tooling index
validation docs
task docs
file sorgente rilevanti

Output:

ai_context_pack.json
ai_context_pack.md
ai_context_pack_evidence.json
8.3 Repository docs map

Serve a sapere quali MD sono canonici, obsoleti, mancanti o generati.

Senza docs map, gli MD diventano rumore.

8.4 Tool catalog

Serve a sapere quali strumenti esistono davvero.

Deve elencare:

nome tool
path
input
output
side effects
safe/unsafe
può scrivere source?
può scrivere output?
può eseguire provider?
può applicare patch?
8.5 Runtime SQLite memory

Tool necessario:

runtime_sqlite_memory

Operazioni minime:

write fact
write decision
write artifact ref
write rejected block
write accepted block
write symbol discovery
search facts
search decisions
search similar errors
search previous targets
8.6 SQLite FTS5 search

Il motore FTS5 deve cercare:

path
simboli
funzioni
errori
decisioni
task
motivi reject
validation outputs

Non basta grep su file sparsi.

8.7 Semantic code chunker

Serve a selezionare codice reale.

Deve produrre:

selected_semantic_code_chunks.json
selected_semantic_code_chunks.md

Con:

path reale
snippet
role
hash
score
source existence verified
8.8 Semantic evidence chunker

Serve a indicizzare output di validazione, provider, tool, report.

Esempi:

semantic_evidence_chunks.json
semantic_evidence_chunks.md
chunks/
8.9 Broker bridge

Serve a collegare tool e heap:

tool request
tool execution
tool output
artifact refs
summary
returncode
passed/failed

Senza broker, i tool sono esecuzioni scollegate.

8.10 Provider probes

Tool/lane:

GPU1 provider
GPU0 peer workload/reviewer
NPU micro-task auditor

Devono scrivere artifact verificabili:

provider_teamwork/gpu1_*.json
provider_teamwork/gpu0_*.json
provider_teamwork/npu_*.json
8.11 Quality gate

Deve bloccare:

placeholder/stub
TODO operativo
pass
path/to/artifact
path inventati
file non verificati
diff assente
similarità 1.000
patch non applicabile
8.12 Pointer manifest builder

Tool:

build_external_heap_block_pointer_manifest.py

Produce:

external_heap_block_pointer_manifest.json

Ruolo:

costruisce grafo blocchi
collega next/previous/refines/resume
marca accepted/rejected
calcola roles_present
calcola block_count / edge_count
separa provider_execution_performed
8.13 External long response composer

Tool:

compose_external_heap_block_response.py

Produce:

external_heap_primary_long_response.md
external_heap_primary_long_response.json

Ruolo:

ricostruisce risposta lunga
usa proposal blocks
usa peer blocks
include rejected history se richiesto
non sostituisce composer vecchio
8.14 Revision context builder

Tool:

build_external_heap_revision_context.py

Produce:

external_heap_revision_context.json
external_heap_revision_context.md

Ruolo:

prepara prossima run
genera tasks
sceglie resume_from_block_id
identifica latest_block_id
estrae simboli
distingue no patchable target da rewrite necessario
8.15 Postrun package

Tool:

run_external_heap_postrun_package.py

Ruolo:

seleziona run completa
raccoglie output vecchio e nuovo
copia in Documents
scrive DOWNLOADS manifest
include long response
include revision context
include pointer manifest
9. Prodotti finali: cosa deve uscire
A. Prodotto umano leggibile
aicarmine_heap_final_proposals_<stamp>.md
aicarmine_heap_final_proposals_<stamp>.txt
external_heap_primary_long_response.md

Serve all’operatore.

B. Prodotto macchina
aicarmine_heap_final_proposals_<stamp>.json
external_heap_primary_long_response.json
external_heap_revision_context.json
external_heap_block_pointer_manifest.json

Serve alla prossima run.

C. Prodotto di continuità
external_heap_revision_context.json

È il più importante per superare il limite della chat.

D. Prodotto patch/code
CODE_PRODUCT_FULL_PATCH.md
FINAL_READABLE_PRODUCT.md
patch candidate report
code execution matrix
diff reali

Questo deve esistere solo se:

target verificato
diff reale
validation reale
patch candidate validato

Nel caso che hai caricato, il code product non c’era: Matrix concrete proposal count, Matrix code product count e Generated code product count erano tutti 0, con status NO_TARGETS_OR_CODE_PRODUCT.

10. Salti per i prodotti

I “salti” non servono solo a navigare. Servono a costruire il prodotto.

Salto forward
proposal_001 → proposal_002 → proposal_003

Costruisce la sequenza.

Salto backward
proposal_003 scopre import sqlite3
→ torna a proposal_001/proposal_002
→ aggiunge contratto simbolico
→ riprende da proposal_003
Salto refines
proposal_004 corregge proposal_002

Il prodotto finale deve usare la versione raffinata, non necessariamente l’ultima in ordine cronologico.

Salto resume
dopo refactor indietro, riprendi da proposal_003

Serve a non perdere il punto operativo.

Salto peer
GPU0 prende proposal_001
NPU prende proposal_001
GPU1 continua proposal_003

Mentre GPU1 va avanti, GPU0/NPU lavorano su vecchi blocchi.

Salto product composition

Il composer deve attraversare:

accepted proposal blocks
refined proposal blocks
peer evidence blocks
audit blocks
revision context

e decidere:

cosa entra nel prodotto finale
cosa resta rejected history
cosa diventa task successivo
11. Stato ideale di una run completa

Una run completa sana dovrebbe dire:

preflight_passed = true
startup_reload_passed = true
startup_reload_degraded = false oppure degraded esplicito
heap_passed = true
roles_present = GPU1/GPU0/NPU
provider_execution_performed = true se provider/workload reale
proposal_block_count > 0
accepted_block_count > 0 oppure blocked con reason concreta
pointer_block_count > 0
edge_count > 0
external_long_response generated
revision_context generated
documents_copy_performed = true
code_product generated solo se target/diff validi

Se non c’è accepted block, deve produrre:

product_acceptance_status = blocked
priority_next_action = motivo concreto
tasks[] per prossima run

Nel revision context caricato il sistema lo fa: product_acceptance_status è blocked, priority_next_action è blocked_no_verified_target, e i pointer restano product contract.

12. Formula finale dell’universo heap

La definizione completa, includendo i tool che non possono mancare, è questa:

Universo heap =
  stato runtime volatile
+ memoria persistente SQLite/FTS5
+ context reload deterministico
+ chunking codice/evidenza/proposte
+ broker tool evidence
+ provider lanes GPU1/GPU0/NPU
+ quality gates
+ pointer graph product-contract
+ salti next/previous/refines/resume
+ composer vecchio
+ external long-response composer
+ revision context builder
+ postrun package
+ code product gate

E il contratto operativo:

Nessuna IA deve essere fonte di verità.
Ogni IA deve leggere heap/memoria/artifact.
Ogni decisione deve finire in memoria o artifact.
Ogni blocco deve essere navigabile via pointer.
Ogni output lungo deve essere componibile da chunk.
Ogni run successiva deve poter riprendere dal revision context.
Ogni patch deve nascere solo da target verificati e diff reali.

Questa è la forma completa dell’universo. Non “script che girano”, ma memoria + chunk + pointer + salti + composer + revision context + prodotto verificabile.