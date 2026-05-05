<!-- IA-CARMINE-MD-SPLIT: part -->
# OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY — parte 002 di 002

Sorgente indice: [`../OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md`](../OPENAI_HARNESS_SYMPHONY_AI_FRIENDLY.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

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
