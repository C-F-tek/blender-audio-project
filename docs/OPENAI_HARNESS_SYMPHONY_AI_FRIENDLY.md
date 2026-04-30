# OpenAI Harness Engineering + Symphony — Appunti AI-friendly

Data creazione: 2026-04-29 16:47:22 UTC

Fonti ufficiali OpenAI:

- Harness Engineering: usare Codex in un mondo agent-first — https://openai.com/it-IT/index/harness-engineering/
- An open-source spec for Codex orchestration: Symphony — https://openai.com/index/open-source-codex-orchestration-symphony/

> Scopo: trasformare i due articoli OpenAI in note operative riusabili per `blender-audio-project`: repository AI-friendly, orchestrazione agentica, validazione, documentazione versionata, dry-run, guardrail e workflow GitHub.

---

## 1. Sintesi esecutiva

I due articoli descrivono una transizione tecnica:

```text
sviluppo tradizionale
  -> sviluppo assistito da agenti
  -> repository progettato per agenti
  -> workflow orchestrato tramite ticket/task
  -> agenti che lavorano in workspace isolati
  -> umani che guidano obiettivi, vincoli, accettazione e priorità
```

Il messaggio operativo più importante è che l'efficacia degli agenti non dipende solo dal modello, ma dal sistema attorno al modello:

```text
documentazione strutturata
strumenti locali
validazione automatica
guardrail
issue/task workflow
repo leggibile dall'agente
report osservabili
feedback reinserito nel repository
```

Per `blender-audio-project` questo conferma la direzione già intrapresa:

```text
AGENTS.md come indice
docs/ come fonte di verità
WORKFLOW.md come workflow operativo
Tools/ai/pipeline/ modulare
Tools/npu/pipeline/ come helper package app-agnostico in decomposizione staged
dry-run matrix
report Markdown/JSON
status marker machine-readable
validazioni locali
rigenerazione indexAI/NPU context
```

---

## 2. Harness Engineering: idee principali

### 2.1 Repository agent-first

OpenAI descrive un esperimento: sviluppare un prodotto interno partendo da repository vuoto, con codice generato da Codex e umani nel ruolo di guida, revisione, definizione di obiettivi e creazione di feedback loop.

Concetto chiave:

```text
Gli umani guidano.
Gli agenti eseguono.
```

Applicazione pratica:

```text
umano:
  - definisce obiettivo artistico/tecnico
  - valida comportamento Blender/render
  - decide cosa entra in master

agente:
  - crea patch modulari
  - aggiorna documentazione
  - genera report
  - propone refactor
  - prepara test e dry-run
```

### 2.2 AGENTS.md non deve essere un'enciclopedia

Un singolo `AGENTS.md` enorme degrada rapidamente.

Pattern consigliato:

```text
AGENTS.md
  -> indice breve
  -> rimandi a docs strutturati
  -> regole principali
  -> workflow di ingresso
```

La conoscenza reale deve stare nel repository:

```text
docs/
  architecture
  workflow
  quality gates
  status
  execution plans
  generated context
```

Applicazione al progetto:

```text
AGENTS.md
docs/README.md
docs/PROJECT_AI_CONSCIOUSNESS.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/AI_PIPELINE_ARCHITECTURE.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
Tools/npu/pipeline/README.md
```

### 2.3 Rendere il repository leggibile dall'agente

Principio:

```text
Ciò che l'agente non può vedere nel repository, per lui non esiste.
```

Informazioni come decisioni, convenzioni, workflow, stato dei refactor e criteri di qualità devono essere versionate in file accessibili:

```text
Markdown
JSON
schema
manifest
report
status marker
script di validazione
```

Applicazione:

```text
Tools/ai/pipeline/refactor_status.py
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/PROJECT_STATUS_POINT.md
output/ai_pipeline/dry_run_matrix_report.md
indexAI/project_code_manifest.json
Tools/npu/npu_code_manifest.json
Tools/npu/pipeline/README.md
```

### 2.4 Architettura e gusto devono essere codificati

La documentazione da sola non basta. I vincoli architetturali devono essere applicabili meccanicamente.

Esempi di vincoli utili:

```text
moduli con responsabilità chiara
limiti di dimensione file
direzioni di dipendenza
test strutturali
linter custom
messaggi di errore orientati all'agente
report che indicano correzioni
```

Applicazione diretta:

```text
Tools/validation/check_ai_pipeline_modules.py
Tools/validation/check_npu_pipeline_modules.py
Tools/validation/check_npu_pipeline_helper_tests.py
Tools/validation/check_npu_pipeline_docs.py
Tools/validation/check_package_structure.py
Tools/ai/run_pipeline_dry_run_matrix.py
Tools/ai/pipeline/schema_report.py
Tools/ai/pipeline/scheduler.py
```

### 2.5 La deriva va gestita come garbage collection

Quando gli agenti generano molto codice, tendono a replicare pattern esistenti, anche se imperfetti.

Rimedio operativo:

```text
doc gardening
refactor ricorrenti
golden principles
pulizia tecnica piccola e frequente
report di qualità
task di manutenzione automatici o semi-automatici
```

Applicazione:

```text
docs/PROJECT_STATUS_POINT.md
docs/REFACTORING_AND_REUSE_PLAN.md
docs/QUALITY_GATE.md
Scripting/shared/
Tools/validation/
Tools/npu/pipeline/
output/local_validation/
```

---

## 3. Symphony: idee principali

### 3.1 Problema: context switching umano

Gli agenti interattivi via CLI o UI sono potenti, ma se ogni sessione richiede supervisione costante, l'umano diventa collo di bottiglia.

Passaggio concettuale:

```text
gestire sessioni agentiche
  -> gestire task/ticket/obiettivi
```

### 3.2 Issue tracker come control plane

Symphony usa un task tracker come stato operativo:

```text
ticket aperto
  -> workspace isolato
  -> agente assegnato
  -> lavoro continuo
  -> PR/report/proof-of-work
  -> review
  -> merge o follow-up task
```

Per il progetto, un equivalente leggero è:

```text
WORKFLOW.md
docs/PROJECT_STATUS_POINT.md
docs/EXECUTION_PLANS/
docs/TECH_DEBT_TRACKER.md
patch_specs/inbox/
output/local_validation/
GitHub issues o checklist Markdown
dry-run matrix report
```

### 3.3 Un agente per task, workspace isolato

Principio Symphony:

```text
Per ogni task aperto, garantire un agente in esecuzione nel proprio workspace.
```

Applicazione futura possibile:

```text
task: validare blender_compat
task: migrare un call-site v61b
task: generare report markdown
task: correggere dry-run matrix
task: rigenerare indexAI
task: validare NPU helper package
task: wire IO helper in run_dual_ai_pipeline.py dopo validazione
```

Ogni task dovrebbe avere:

```text
input chiaro
workspace/branch
criterio di accettazione
output atteso
report
stato finale
```

### 3.4 WORKFLOW.md come processo versionato

Symphony evidenzia che il workflow deve essere scritto nel repository, non nella testa delle persone.

Nel progetto, file equivalenti già presenti:

```text
WORKFLOW.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/PATCH_SPEC_WORKFLOW.md
docs/QUALITY_GATE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
Tools/workflow/run_local_validation_after_refactor.ps1
Tools/workflow/run_npu_pipeline_helper_validation.ps1
```

`WORKFLOW.md` è l'entrypoint operativo root; i documenti in `docs/` e i runner in `Tools/workflow/` sono i dettagli eseguibili.

### 3.5 Orchestrazione minimale, non prodotto monolitico

Symphony è utile come specifica/reference implementation, non necessariamente come prodotto da copiare.

Lezione pratica:

```text
non serve copiare Symphony
serve applicare il principio:
  task -> workspace -> agente -> validazione -> report -> review
```

---

## 4. Applicazione concreta a blender-audio-project

### 4.1 Stato attuale già coerente

Il progetto ha già molte componenti allineate:

```text
AGENTS.md come guida iniziale
docs/ come fonte di verità
WORKFLOW.md come processo operativo root
PROJECT_AI_CONSCIOUSNESS.md come memoria operativa
AI_PIPELINE_REFACTOR_STATUS.md come status marker
AI_PIPELINE_ARCHITECTURE.md come mappa architetturale
GITHUB_LOCAL_VALIDATION_WORKFLOW.md come workflow versionato
Tools/ai/pipeline/ come architettura modulare
Tools/npu/pipeline/ come helper package app-agnostico in staged decomposition
run_pipeline_dry_run_matrix.py come validazione ripetibile
run_local_validation_after_refactor.ps1 come runner unattended
run_npu_pipeline_helper_validation.ps1 come runner focalizzato NPU helper
Scripting/shared/ come libreria condivisa
```

### 4.2 Cosa migliorare subito

#### A. Mantenere `WORKFLOW.md` aggiornato

Scopo:

```text
root-level workflow per umani e agenti
```

Contenuti da mantenere coerenti:

```text
1. Pull/rebase
2. Read docs
3. Pick task
4. Modify small scope
5. Run focused validation
6. Run full validation when needed
7. Regenerate indexes
8. Commit
9. Push
10. Share reports
```

#### B. Usare `docs/EXECUTION_PLANS/`

Struttura:

```text
docs/EXECUTION_PLANS/
  README.md
  active/
  completed/
  abandoned/
```

Per ogni task complesso:

```text
goal
scope
files
validation
risk
progress log
decision log
result
```

#### C. Mantenere `docs/TECH_DEBT_TRACKER.md`

Per evitare deriva:

```text
id
area
symptom
risk
recommended fix
status
last reviewed
```

#### D. Mantenere checks agent-friendly

Esempi:

```text
check_docs_links.py
check_refactor_status_consistency.py
check_ai_pipeline_modules.py
check_npu_pipeline_modules.py
check_npu_pipeline_helper_tests.py
check_npu_pipeline_docs.py
```

---

## 5. Mapping concetti OpenAI -> progetto

| Concetto OpenAI | Traduzione nel progetto |
|---|---|
| Harness engineering | `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, `Tools/validation/`, `Tools/workflow/` |
| AGENTS.md come indice | `AGENTS.md` breve + `docs/README.md` |
| Knowledge base versionata | `docs/`, `indexAI/`, manifest JSON |
| Agent readability | moduli piccoli, status marker, report Markdown |
| Guardrail meccanici | validators, dry-run matrix, schema report |
| Issue tracker come control plane | GitHub issues / patch_specs / execution plans |
| Worktree/workspace isolato | branch o cartella output per task |
| Proof of work | JSON/MD report, dry-run output, git diff |
| Garbage collection del debito | TECH_DEBT_TRACKER + refactor ricorrenti |
| WORKFLOW.md | root operational workflow already present |

---

## 6. Checklist consigliata per il prossimo ciclo

### Da fare sul repository

```text
[ ] Validare la PR/batch NPU helper con runner focalizzato
[ ] Validare la PR/batch NPU helper con full local validation runner
[ ] Rigenerare indexAI/NPU context dopo validazione
[ ] Se verde, mergeare la PR/batch NPU helper
[ ] Aprire una nuova fase stretta per wiring IO helper in Tools/npu/run_dual_ai_pipeline.py
[ ] Continuare a mantenere docs/README.md, AGENTS.md e PROJECT_AI_CONSCIOUSNESS.md coerenti con lo stato reale
```

### Da fare sul PC locale

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git fetch origin
git checkout codex/npu-pipeline-decomposition-away-batch
git pull --ff-only
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

---

## 7. Raccomandazione per il progetto

La direzione più forte è trasformare il repository in un sistema operativo per agenti:

```text
docs = conoscenza
Tools/validation = guardrail
Tools/workflow = automazione locale
Tools/ai/pipeline = orchestrazione
Tools/npu/pipeline = helper contracts per pipeline locale AI/NPU
Scripting/shared = infrastruttura riusabile
indexAI = memoria generata
patch_specs = coda modifiche meccaniche
output/*_report.md = proof of work
```

Il punto chiave non è “far scrivere codice all'AI”, ma rendere il repository talmente leggibile, verificabile e orchestrabile che un agente possa lavorare senza perdere contesto e senza produrre deriva.

---

## 8. Note operative per knowledge base

Classificazione consigliata:

```yaml
type: external_knowledge
source: OpenAI official blog
topics:
  - agent-first engineering
  - Codex
  - harness engineering
  - repository knowledge base
  - AI-readable documentation
  - agent orchestration
  - Symphony
  - workflow automation
  - guardrails
  - dry-run validation
recommended_target_docs:
  - AGENTS.md
  - docs/README.md
  - docs/PROJECT_AI_CONSCIOUSNESS.md
  - docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
  - docs/AI_PIPELINE_ARCHITECTURE.md
  - docs/REFACTORING_AND_REUSE_PLAN.md
  - Tools/npu/pipeline/README.md
```
