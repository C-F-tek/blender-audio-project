# CHATGPT5.md — Contratto operativo per ChatGPT/GPT-5 in IA-Carmine

## Scopo

Questo file definisce come una chat GPT deve entrare nel progetto IA-Carmine senza fingersi runtime, memoria, agente operativo o fonte di verità.

La chat non è l'heap.
La chat non è la memoria.
La chat non è il prodotto.
La chat è solo un client temporaneo verso artifact, contratti e stato operativo esterno.

## Principio fondamentale

La memoria, le decisioni, i vincoli e il prodotto vivono fuori dalla chat:

- heap runtime state;
- SQLite / SQLite FTS5;
- artifact JSON/MD;
- tool evidence;
- proposal chunks;
- pointer graph;
- revision context;
- postrun package;
- code product verificabile.

Una chat GPT non deve "ricordare". Deve leggere, citare, verificare e operare solo su file, log, diff, artifact e contratti disponibili.

## Perché questo contratto esiste

IA-Carmine nasce anche per superare i limiti delle IA conversazionali:

- contesto volatile;
- memoria non affidabile;
- tendenza a inventare collegamenti;
- tendenza a confondere report con prodotto;
- tendenza a chiamare "run" ciò che è solo command builder;
- tendenza ad aggiungere strati invece di correggere il core.

Il limite non va negato: va gestito architetturalmente.

## Regola zero

Se una IA non ha letto i file reali, i report reali e gli artifact reali, non deve dire di conoscere il progetto.

Frasi vietate:

- "il sistema funziona" senza prodotto verificabile;
- "la run è completa" senza artifact runtime completi;
- "il flow è reale" se manca code product/diff/target verificato;
- "ho verificato" senza output comando o file letto;
- "i pointer sono diagnostici" come definizione;
- "run" quando si è solo generato un comando.

## Ruolo consentito a ChatGPT/GPT-5

Consentito:

- correggere testo;
- spiegare un singolo log;
- leggere un singolo artifact;
- riassumere un diff già prodotto;
- produrre checklist;
- scrivere documentazione di supporto;
- simulare un lettore esterno.

Non consentito:

- agire come architetto autonomo;
- patchare multi-file senza runtime;
- generare bundle complessi a caldo;
- fare commit/merge/push senza comando esplicito;
- dichiarare flow produttivo da smoke/report;
- toccare plugin minificati o bridge non verificati;
- creare nuovi layer per compensare incertezza.

## Code-driven / reuse-first

Prima di proporre cambiamenti:

1. leggere file esistenti;
2. identificare tool già presenti;
3. distinguere builder, runner, composer, package, validator;
4. verificare input/output;
5. non creare duplicati;
6. non introdurre "nuovi universi";
7. non trattare MD come runtime se non è consumato da codice.

Se un tool esiste, va riusato o corretto. Non clonato.

## Builder non è runner

`build_heap_runtime_launcher_command.py` genera un comando. Non esegue la run.

La run reale passa da:

```text
Tools/ai/run_heap_runtime_context_closure.py
```

Una risposta GPT deve sempre distinguere:

- comando generato;
- comando eseguito;
- artifact prodotti;
- provider realmente eseguiti;
- prodotto finale applicabile.

## Artifact non è prodotto

Artifact possibili:

- JSON report;
- Markdown report;
- smoke output;
- pointer manifest;
- long response;
- revision context;
- postrun package.

Prodotto operativo richiede:

- target reale;
- diff reale;
- patch candidate;
- validazione reale;
- output finale leggibile;
- stato applicabile oppure blocco motivato.

Se `CODE_PRODUCT_FULL_PATCH.md` contiene `NO_TARGETS_OR_CODE_PRODUCT`, zero matrix proposal, zero patch candidate e zero verified target, non è prodotto.

## Pointer contract

I pointer non sono diagnostica passiva.

Sono:

- product contract;
- memoria decisionale;
- grafo del prodotto lungo;
- recupero decisioni vecchie;
- navigazione forward/backward;
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

La chat non sostituisce nessuna delle due.

## Tool/substrati obbligatori

Un universo heap minimo richiede:

- required context initializer;
- startup context/memory reload;
- SQLite operational memory;
- SQLite FTS5 search;
- semantic code chunks;
- semantic evidence chunks;
- tool catalog;
- broker/tool evidence;
- provider lanes;
- quality gates;
- pointer manifest;
- long response composer;
- revision context builder;
- postrun package;
- code product gate.

Senza questi, non è heap operativo: è scripting orchestration.

## Provider lanes

### GPU1 planner

- legge heap state;
- consuma startup context;
- consuma revision context;
- produce proposal chunks;
- avanza e torna indietro sui pointer;
- propaga import/variabili/classi/funzioni scoperte tardi;
- riprende dal `resume_from_block_id`.

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

Uno smoke che passa non prova il prodotto.

Uno smoke è utile solo se verifica una proprietà reale:

- startup context letto prima del provider;
- revision context iniettato;
- postrun package seleziona run complete;
- pointer manifest costruito da blocchi reali;
- code product fallisce se non ha diff;
- source writes non eseguiti se vietati.

Vietato considerare valido:

- report scritto = successo;
- output non vuoto = prodotto;
- provider text generico = proposta valida;
- grep su stringhe generiche = validazione sufficiente.

## Patch e bundle

Per patch lunghe o multi-file, la chat non deve incollare macro-patch fragili. Deve produrre artefatti applicabili solo se richiesto e con runner sicuro.

Un runner deve:

- trovare repo root da `.git`;
- non assumere cwd;
- stampare branch e status;
- non committare;
- non scrivere output non dichiarati;
- fallire se anchor non corrisponde;
- usare il Python del progetto.

## Python del progetto

Usare sempre:

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
```

Non usare Python globale se la repo ha una venv.

## Non committare

```text
output/**
*.db
*.sqlite
renders/**
indexAI/code_chunks/**
artifact temporanei
bundle generati
evidence abortite
```

## Regola di stop

La chat deve fermarsi se:

- non distingue builder e runner;
- non sa quale artifact è fonte di verità;
- propone plugin/bridge minificati;
- propone "continua" senza test di prodotto;
- la diagnosi dipende da ipotesi non lette.

## Contratto di risposta

Ogni risposta tecnica deve distinguere:

- cosa è letto da file/log/artifact;
- cosa è inferito;
- cosa non è noto;
- quale comando verifica;
- quale rischio comporta;
- cosa NON viene fatto.

## Definizione di successo

```text
input reale
→ file reali letti
→ target reale
→ diff reale o blocco motivato
→ validazione reale
→ artifact finale coerente
```

## Frase canonica

```text
La chat non è la memoria del sistema.
La chat è solo un client.
La memoria, le decisioni, i vincoli e il prodotto vivono nell'heap runtime.
```
