# OpenAI Harness Engineering + Symphony — Appunti AI-friendly

Data creazione: 2026-04-29 16:47:22 UTC

Fonti ufficiali OpenAI:

- Harness Engineering: usare Codex in un mondo agent-first — https://openai.com/it-IT/index/harness-engineering/
- An open-source spec for Codex orchestration: Symphony — https://openai.com/index/open-source-codex-orchestration-symphony/

> Scopo: trasformare i due articoli OpenAI in note operative riusabili per `IA-Carmine Local AI Orchestration Workbench`: repository AI-friendly, orchestrazione agentica, validazione, documentazione versionata, dry-run, guardrail, telemetria, capability manifest e workflow GitHub.

This file is reference guidance, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

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
telemetria e capability manifest
feedback reinserito nel repository
```

Per IA-Carmine questo conferma la direzione attuale:

```text
flusso unico tramite run_unified_local_ai_refactor.ps1
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensità, non scope
perimetro di tutto espandibile in modo esplicito
AGENTS.md come indice compatto
docs/ come fonte di verità
WORKFLOW.md come workflow operativo
Tools/ai/pipeline/ modulare
Tools/npu/pipeline/ come helper package app-agnostico in decomposizione staged
manifest-first visibility
runtime telemetry + capability manifest
shared AI-to-AI bundle
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
umano/master-AI:
  - definisce obiettivo tecnico
  - valida comportamento runtime quando serve
  - decide cosa entra in master
  - autorizza apply/merge/push sensibili

agente/local-AI:
  - crea patch modulari o patch plan
  - aggiorna documentazione
  - genera report
  - produce telemetria/capability/evidence
  - propone refactor
  - prepara test, dry-run e bundle AI-to-AI
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
  telemetry contracts
  bundle contracts
```

Applicazione attuale:

```text
AGENTS.md
docs/README.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
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
telemetry summary
capability manifest
AI-to-AI bundle
```

Applicazione:

```text
Tools/ai/pipeline/refactor_status.py
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/PROJECT_STATUS_POINT.md
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json/md
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
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
telemetria che distingue executed/failed/blocked/degraded
```

Applicazione diretta:

```text
Tools/validation/check_ai_pipeline_modules.py
Tools/validation/check_npu_pipeline_modules.py
Tools/validation/check_npu_pipeline_helper_tests.py
Tools/validation/check_npu_pipeline_docs.py
Tools/validation/check_package_structure.py
Tools/ai/run_pipeline_dry_run_matrix.py
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/ai/build_runtime_tool_capability_manifest.py
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
```

### 2.5 La deriva va gestita come garbage collection

Quando gli agenti generano molto codice o documentazione, tendono a replicare pattern esistenti, anche se imperfetti.

Rimedio operativo:

```text
doc gardening
refactor ricorrenti
golden principles
pulizia tecnica piccola e frequente
report di qualità
telemetry completeness checks
task di manutenzione automatici o semi-automatici
```

Applicazione:

```text
docs/PROJECT_STATUS_POINT.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/QUALITY_GATE.md
Scripting/shared/
Tools/validation/
Tools/npu/pipeline/
docs/LOCAL_VALIDATION_EVIDENCE/
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

Per il progetto, l'equivalente leggero è:

```text
WORKFLOW.md
docs/PROJECT_STATUS_POINT.md
docs/EXECUTION_PLANS/
docs/TECH_DEBT_TRACKER.md
docs/LOCAL_AI_TASKS/
docs/LOCAL_VALIDATION_EVIDENCE/
GitHub issues o checklist Markdown
unified launcher manifest
runtime telemetry/capability manifests
shared AI-to-AI bundle
```

### 3.3 Un agente per task, workspace isolato

Principio Symphony:

```text
Per ogni task aperto, garantire un agente in esecuzione nel proprio workspace.
```

Applicazione futura possibile:

```text
task: validare launcher Full0To10
task: completare external controls
task: verificare telemetry completeness
task: arricchire project-tool-registry.md
task: validare NPU helper package
task: wire IO helper in Tools/npu/run_dual_ai_pipeline.py dopo validazione
```

Ogni task dovrebbe avere:

```text
input chiaro
workspace/branch
criterio di accettazione
output atteso
manifest/report/telemetry
stato finale
```

### 3.4 WORKFLOW.md come processo versionato

Symphony evidenzia che il workflow deve essere scritto nel repository, non nella testa delle persone.

Nel progetto, file equivalenti già presenti:

```text
WORKFLOW.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/PATCH_SPEC_WORKFLOW.md
docs/QUALITY_GATE.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

`WORKFLOW.md` è lifecycle root; il launcher runbook è l'entrypoint operativo per full-run/local-AI.

### 3.5 Orchestrazione minimale, non prodotto monolitico

Symphony è utile come specifica/reference implementation, non necessariamente come prodotto da copiare.

Lezione pratica:

```text
non serve copiare Symphony
serve applicare il principio:
  task -> workspace -> agente -> validazione -> report -> telemetry -> review
```

---

## 4. Applicazione concreta a IA-Carmine

### 4.1 Stato attuale già coerente

Il progetto ha già molte componenti allineate:

```text
AGENTS.md come guida iniziale
docs/ come fonte di verità
WORKFLOW.md come processo operativo root
PROJECT_STATUS_POINT.md come stato operativo
AI_PIPELINE_REFACTOR_STATUS.md come status marker
AI_PIPELINE_ARCHITECTURE.md come mappa architetturale
Tools/ai/pipeline/ come architettura modulare
Tools/npu/pipeline/ come helper package app-agnostico in staged decomposition
run_pipeline_dry_run_matrix.py come validazione planned-only ripetibile
run_unified_local_ai_refactor.ps1 come launcher unico
runtime telemetry e capability manifest come proof-of-work accessory
Scripting/shared/ come libreria condivisa
```

### 4.2 Cosa mantenere coerente subito

#### A. Mantenere `WORKFLOW.md` e launcher runbook aggiornati

Scopo:

```text
root lifecycle + active executable owner
```

Contenuti da mantenere coerenti:

```text
1. Read canonical docs
2. Select task
3. Use unified launcher for broad local-AI work
4. Preserve Full0To10 = TUTTO SU TUTTO
5. Use focused validation only for focused edits/debug
6. Attach evidence + patch plan + telemetry/capability/final summary for full-run handoff
7. Keep output/** and DB files out of commits
8. Human/master-AI reviews apply/merge/push
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
telemetry/capability expectations when relevant
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
build_runtime_tool_usage_telemetry.py
build_runtime_tool_capability_manifest.py
build_full_toolbox_run_telemetry_summary.py
```

---

## 5. Mapping concetti OpenAI -> progetto

| Concetto OpenAI | Traduzione nel progetto |
|---|---|
| Harness engineering | `Tools/ai/pipeline/`, `Tools/npu/pipeline/`, `Tools/validation/`, `Tools/workflow/` |
| AGENTS.md come indice | `AGENTS.md` breve + `docs/README.md` |
| Knowledge base versionata | `docs/`, `indexAI/`, manifest JSON, telemetry/capability/bundle artifacts |
| Agent readability | moduli piccoli, status marker, report Markdown, final summaries |
| Guardrail meccanici | validators, dry-run matrix, schema report, telemetry completeness checks |
| Issue tracker come control plane | GitHub issues / patch_specs / execution plans |
| Worktree/workspace isolato | branch o cartella output per task |
| Proof of work | JSON/MD report, dry-run output, telemetry, capability manifest, git diff |
| Garbage collection del debito | TECH_DEBT_TRACKER + doc pruning + refactor ricorrenti |
| WORKFLOW.md | root operational lifecycle already present |
| Full-run orchestration | `run_unified_local_ai_refactor.ps1` + `Full0To10` contract |

---

## 6. Checklist consigliata per il prossimo ciclo

```text
[ ] Verificare localmente launcher Full0To10 dopo il blocco MD
[ ] Verificare che evidence + patch plan + telemetry/capability/final summary viaggino insieme
[ ] Validare che dry-run matrix resti planned-only e non full-run proof
[ ] Arricchire project-tool-registry.md da inventory/evidence successive
[ ] Continuare a mantenere docs/README.md, AGENTS.md, PROJECT_STATUS_POINT.md e current-code-flow-guide coerenti con lo stato reale
[ ] Promuovere nuove lane nel perimetro tutto solo con manifest/report/telemetry/bundle visibility
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
patch_specs = coda modifiche meccaniche solo dopo approvazione
runtime telemetry = prova esecutiva accessoria
capability manifest = prova di capacità disponibili
shared AI-to-AI bundle = handoff compatto tra AI/operatori
```

Il punto chiave non è “far scrivere codice all'AI”, ma rendere il repository talmente leggibile, verificabile, telemetrizzato e orchestrabile che un agente possa lavorare senza perdere contesto e senza produrre deriva.

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
  - telemetry
  - capability manifest
  - AI-to-AI handoff
recommended_target_docs:
  - AGENTS.md
  - docs/README.md
  - docs/PROJECT_STATUS_POINT.md
  - docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
  - docs/AI_PIPELINE_ARCHITECTURE.md
  - docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
  - Tools/npu/pipeline/README.md
```
