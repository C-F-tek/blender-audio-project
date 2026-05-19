# CHATGPT.md — contratto operativo per ChatGPT/GPT in IA-Carmine

## Scopo

Questo file definisce come una chat GPT deve entrare nel progetto IA-Carmine senza fingersi runtime, memoria, agente operativo o fonte di verità.

La chat non è l'heap.
La chat non è la memoria.
La chat non è il prodotto.
La chat è solo un client temporaneo verso artifact, contratti e stato operativo esterno.

## Fonti di verità

Prima di dichiarare stato, successo o diagnosi, leggere fonti reali:

- file del repository;
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

## Code-driven / reuse-first

Prima di proporre cambiamenti:

1. leggere file esistenti;
2. identificare tool già presenti;
3. distinguere builder, runner, composer, package, validator;
4. verificare input e output;
5. non creare duplicati;
6. non introdurre nuovi universi paralleli;
7. non trattare un Markdown come runtime se il codice non lo consuma.

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
python -m Tools.ai run ...
python -m Tools.ai <tool> ...
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

### GPU1 planner

- legge heap state;
- consuma startup context;
- consuma revision context;
- produce proposal chunks;
- propaga import, variabili, classi, funzioni e contratti scoperti tardi;
- riprende da `resume_from_block_id` quando serve.

### GPU0 reviewer/refiner

- rivaluta blocchi vecchi;
- propone refines/resume;
- verifica concretezza;
- segnala path inventati;
- blocca proposte deboli.

### NPU auditor

- audita placeholder/stub;
- path inventati;
- source writes non dichiarati;
- provider execution falsa;
- patch application non autorizzata;
- ripetizioni;
- accettabilità del blocco.

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
