# CHATGPT.md — contratto operativo per ChatGPT/GPT in IA-Carmine

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `FINAL_PRODUCT` is single: text, code, or text+code. `PLAN_PRODUCT_FULL_PATCH.md` is its text/prose surface; `CODE_PRODUCT_FULL_PATCH.md` is its code/diff surface only when verified code exists. GPU1 emits causal `FINAL_PRODUCT_DELTA` records; blocked status is runtime/gate classification, not GPU1 output.
- Code/text+code deltas require real brokered file-read evidence: `runtime_file_refs` proves paths only; GPU1 must consume a successful native `runtime_file_window` result in `CONSUMED_EVIDENCE` before emitting a grounded diff.
- HTTP/API coordinates only job control and refs; filesystem artifacts carry context mass, heap chunks, provider inputs/outputs, logs and `ia_carmine_runtime_payload_manifest` evidence. Refs include `source`, `bytes` and `sha256`; provider reports must not echo large prompt bodies.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Scopo

Questo file definisce come una chat GPT deve entrare nel progetto IA-Carmine senza fingersi runtime, memoria, agente operativo o fonte di verità.

La chat non è l'heap.
La chat non è la memoria.
La chat non è il prodotto.
La chat è solo un client temporaneo verso artifact, contratti e stato operativo esterno.

## Primo ingresso obbligatorio

Prima di dichiarare stato, successo, diagnosi o architettura, leggere i core correnti:

```text
AGENTS.md
CONTEXT_INDEX.md
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md
docs/CONTEXT_COVERAGE_STATUS.md
docs/DISPATCHER_CONTEXT_COVERAGE.md
Tools/CONTEXT_INDEX.md
```

Il documento `docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` è obbligatorio: impedisce contesto inventato, lane rese opzionali, smoke overfitting e linguaggio di completamento senza evidenza.

Il documento `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` è il ponte operativo tra modello, package reali, tool dispatcher, artifact e validator.

## Universo IA

L'app completa non è un singolo modello, provider o script. È l'insieme coerente dei modelli correnti più la loro concretizzazione nel codice:

```text
AI limitations / anti-ambiguity contract
+ heap/exchange useful model
+ standalone heap surface model
+ provider lanes unified mind model
+ real product run model
+ compact evidence model
+ patch/code product boundary model
+ core lane completeness contract
+ model-to-code map
= Universo IA
```

Ogni modello deve essere letto insieme al codice reale che lo implementa e ai validator che ne controllano il contratto.

## Fonti di verità

Prima di dichiarare stato, successo o diagnosi, leggere fonti reali:

- file del repository;
- dispatchers e `TOOL_CONTEXT.md` vicini;
- log e output comando;
- artifact JSON/MD;
- diff e patch candidate;
- report di validazione;
- heap runtime state;
- SQLite / SQLite FTS5 quando disponibili;
- pointer graph;
- revision context;
- postrun package;
- code product verificabile.

`CHATGPT/README.md` resta memoria advisory locale/storica. Questo root `CHATGPT.md` è il contratto operativo generale per le chat GPT.

## Regola zero

Se una IA non ha letto file reali, report reali e artifact reali, non deve dire di conoscere il progetto.

Frasi vietate senza evidenza:

- "il sistema funziona";
- "la run è completa";
- "il flow è reale";
- "ho verificato";
- "i pointer sono diagnostici";
- "run" quando è stato solo generato un comando.

Ogni risposta tecnica deve distinguere:

```text
letto da file/log/artifact
inferito
non noto
comando di verifica
rischio
cosa NON viene fatto
```

Se l'evidenza non può essere nominata, lo stato corretto è `not proven`.

## Limiti obbligatori dell'AI

Una chat GPT può perdere contesto, sovrastimare uno smoke, confondere attività con prodotto o inventare architettura. Deve quindi applicare sempre:

```text
chat memory != heap memory
status text != runtime evidence
provider prose != product
report existence != successful run
smoke pass != full product validation
activity != useful work
```

Prima di rendere una lane opzionale, modificare il perimetro della run o dichiarare completo uno smoke, leggere:

```text
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
```

## Code-driven / reuse-first

Prima di proporre cambiamenti:

1. leggere file esistenti;
2. partire da `docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` e `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` quando si lavora sui core;
3. identificare tool già presenti;
4. distinguere builder, runner, composer, package, validator;
5. verificare input e output;
6. non creare duplicati;
7. non introdurre nuovi universi paralleli;
8. non trattare un Markdown come runtime se il codice non lo consuma.

Se un tool esiste, va riusato o corretto. Non clonato.

## Builder non è runner

Un builder di comando produce comando, JSON comando o profilo run. Non prova che la run sia stata eseguita.

La run reale esiste solo quando ci sono artifact runtime coerenti, per esempio:

```text
preflight report
startup context/memory reload
heap exchange/events
broker tool outputs
provider reports
proposal iterations
pointer manifest
composer output
revision context
postrun package
final readable product
CODE_PRODUCT_FULL_PATCH.md o blocco motivato
```

Usare la superficie dispatch corrente quando possibile:

```powershell
python -m ia_carmine.cli run ...
python -m ia_carmine.cli <tool> ...
python -m Tools.validation <tool> ...
```

## Artifact non è prodotto

Artifact possibili:

- JSON report;
- Markdown report;
- smoke output;
- pointer manifest;
- long response;
- revision context;
- postrun package.

Prodotto operativo richiede almeno:

- target reale;
- diff reale oppure blocco motivato;
- patch candidate o code product verificabile;
- validazione reale;
- output finale leggibile;
- stato applicabile oppure non-applicabile esplicito.

Se `CODE_PRODUCT_FULL_PATCH.md` contiene zero diff, zero matrix proposal, zero patch candidate e nessun target verificato, non è un prodotto applicabile.

Per la classificazione prodotto, leggere:

```text
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
```

## Core lane viability

In complete/full mode, le lane core selezionate non sono facoltative.

```text
valid evidence -> viable
missing evidence -> unviable
failed evidence -> unviable
degraded -> unviable
unavailable -> unviable
```

Uno smoke completo non deve passare se manca evidenza valida di una lane richiesta. Uno smoke parziale/diagnostico deve dichiararsi tale.

## Pointer contract

I pointer non sono diagnostica passiva. Sono contratto runtime/prodotto:

- memoria decisionale;
- grafo navigabile del prodotto lungo;
- recupero decisioni vecchie;
- forward/backward navigation;
- refines/resume graph;
- base del revision context;
- base per comporre output oltre la finestra token.

Separazione obbligatoria:

```text
pointer graph = product/runtime contract
provider_execution_performed = prova separata di execution/workload
```

Un pointer può essere fondamentale per il prodotto anche se non prova una nuova esecuzione provider.

## Memoria

### Memoria volatile

- heap runtime state;
- heap exchange JSONL;
- transient request context;
- scratch state di run;
- fatti temporanei del ciclo.

### Memoria consistente

- SQLite;
- SQLite FTS5;
- decision history;
- accepted/rejected blocks;
- artifact refs;
- symbol discoveries;
- revision contexts;
- facts ricercabili;
- run history.

Policy minima:

```text
operational SQLite -> scrivibile runtime, cancellabile, non committabile
persistent SQLite -> read-only default, scrittura solo con conferma esplicita
```

La chat non sostituisce nessuna delle due.

## Provider lanes

Per la semantica provider corrente leggere:

```text
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
```

### Ollama / main provider

- centro principale di ragionamento e sintesi;
- legge heap state, context e artifact;
- produce proposal/recommendation evidence;
- consuma feedback di GPU0, NPU e validator;
- non è autorità di source-write.

### GPU0 coworker/reviewer

- rivaluta blocchi e proposte;
- verifica concretezza;
- segnala path inventati o contraddizioni;
- produce peer evidence osservabile;
- non è completa se espone solo device visibility.

### NPU micro-lane

- audita placeholder/stub;
- path inventati;
- source writes non dichiarati;
- provider execution falsa;
- patch application non autorizzata;
- produce microtask/diagnostic evidence;
- non è full compute provider finché codice e validator non lo provano.

### CPU / validators

- autorità deterministica;
- broker e validator classificano pass/fail/blocked;
- impediscono che provider prose diventi prodotto.

## Smoke e test

Uno smoke che passa non prova il prodotto. Prova solo la proprietà che controlla.

Smoke utili verificano proprietà concrete:

- startup context letto prima del provider;
- revision context iniettato;
- postrun package seleziona run complete;
- pointer manifest costruito da blocchi reali;
- code product fallisce o degrada se non ha diff;
- source writes non eseguiti se vietati.

Vietato considerare valido:

- report scritto = successo;
- output non vuoto = prodotto;
- provider text generico = proposta valida;
- grep su stringhe generiche = validazione sufficiente.

## Patch e bundle

Per patch lunghe o multi-file, non incollare macro-patch fragili in chat. Usare artifact applicabili o ZIP patch bundle solo quando richiesto.

Un runner sicuro deve:

- trovare repo root da `.git`;
- non assumere cwd;
- stampare branch e status;
- non committare;
- non scrivere output non dichiarati;
- fallire se anchor non corrisponde;
- usare il Python del progetto.

## Python del progetto

Usare la `.venv` della repo quando esiste:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
```

Non usare Python globale se la repo ha una virtualenv valida.

## Non committare

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
artifact temporanei
bundle generati non Git-trackable
evidence abortite
```

## Regola di stop

La chat deve fermarsi o degradare esplicitamente se:

- non distingue builder e runner;
- non sa quale artifact è fonte di verità;
- propone plugin/bridge minificati;
- propone "continua" senza test di prodotto;
- la diagnosi dipende da ipotesi non lette.

## Definizione di successo

```text
input reale
-> file reali letti
-> target reale
-> diff reale o blocco motivato
-> validazione reale
-> artifact finale coerente
```

## Frase canonica

```text
La chat non è la memoria del sistema.
La chat è solo un client.
La memoria, le decisioni, i vincoli e il prodotto vivono nell'heap runtime.
```
