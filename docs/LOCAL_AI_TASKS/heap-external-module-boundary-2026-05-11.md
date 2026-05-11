# Heap External Module Boundary — 2026-05-11

Repository:

```text
C-F-tek/blender-audio-project
```

Branch:

```text
codex/heap-loop-problems-20260511
```

## Decisione architetturale

Il gate runtime non deve essere modificato per inseguire il modello heap.

Il gate resta un contratto stabile/black-box della run unica. L'heap deve essere adattato come modulo esterno di analisi e proposta, collegabile alla run unica quando il suo comportamento sara' maturo.

Modello corretto:

```text
run unica / gate stabile
  -> artifact report / validation report / provider evidence
  -> heap external analysis module
  -> proposal/recommendation package
  -> operator review / PR candidate
```

Non il contrario:

```text
heap sperimentale che forza modifiche nel gate stabile
```

## Implicazione pratica

La patch corrente non deve introdurre modifiche in:

```text
Tools/ai/run_heap_runtime_completeness_gate.py
```

Se manca un campo, un riferimento, una memoria o un artifact utile, la correzione deve stare in uno di questi layer:

```text
Tools/ai/prepare_heap_context_memory_reload.py
Tools/ai/reconcile_heap_report_with_startup_reload.py
Tools/ai/run_heap_runtime_context_closure.py
Tools/ai/compose_heap_final_proposals.py
Tools/ai/provider_runtime_heap.py
Tools/ai/agent_runtime_sqlite_memory.py
```

oppure in un nuovo adapter esterno, per esempio:

```text
Tools/ai/heap_external_analysis_adapter.py
```

## Stato della PR #297 rispetto a questa decisione

La PR #297 rispetta il vincolo per i fix gia' applicati:

- non modifica `run_heap_runtime_completeness_gate.py`;
- corregge il reconciler per accettare startup degradato con artifact utili;
- corregge il launcher per passare `--allow-degraded-startup` al reconciler quando opportuno;
- migliora la raccolta artifact refs senza richiedere cambi al gate.

## Cosa considerare bug reale adesso

### 1. Reconciler troppo rigido

Gia' corretto in PR #297:

```text
startup_reload_degraded=true + artifact utili + strict=false
```

non deve bloccare la riconciliazione report/composer.

### 2. Artifact refs incompleti

Gia' corretto in PR #297 per reconciler e launcher:

```text
top-level artifacts
tool_executions[].useful_artifact_paths
tool_executions[].existing_artifact_paths
tool_executions[].artifact_paths
tool_executions[].artifact_summaries[].path
legacy tool_executions[].artifacts
```

### 3. Operational memory write non dimostrata

Da correggere fuori dal gate.

Target consigliato:

```text
Tools/ai/prepare_heap_context_memory_reload.py
```

L'heap/preload deve scrivere un record operativo nella scratch memory sotto `output/**`, usando:

```text
Tools/ai/agent_runtime_sqlite_memory.py --action remember --scope operational
```

Contenuto consigliato:

```text
role=heap_startup_reload
summary=startup context/memory reload manifest
content=<manifest path + startup_reload_degraded + artifact refs summary>
tag=heap_startup_context
tag=<stamp>
```

Questo adatta l'heap e non richiede modifiche al gate.

### 4. Product causality/composer flags

Da correggere fuori dal gate.

Target consigliato:

```text
Tools/ai/compose_heap_final_proposals.py
```

Il composer deve distinguere:

```text
composer_packaging_performed=true
product_causality_passed=false|true|unknown
```

La causalita' non va dedotta modificando il gate; va calcolata dagli artifact disponibili:

```text
startup manifest
heap report
provider reports
proposal chunks
reconciliation report
context_artifact_refs
```

## Nuovo ordine patch corretto

1. `fix(ai): reconcile degraded startup artifacts outside gate`  — gia' applicato in PR #297.
2. `fix(ai): record heap startup reload into operational scratch memory`.
3. `feat(ai): expose external heap product causality in composer`.
4. `feat(ai): add heap external analysis adapter for run-unica artifacts`.
5. `docs(ai): document heap as external analysis/proposal module for run unica`.

## Validazione locale attuale fornita dall'operatore

Evidenza operatore:

```text
git diff --check: passed
git status --short: clean
validation_report_contract: latest listed reports passed except historical zero_to_ten_retirement_* artifacts missing required repo_root/passed
```

I due artifact storici non conformi osservati:

```text
output/validation/zero_to_ten_retirement_delete_report.json
output/validation/zero_to_ten_retirement_inventory.json
```

sono output locali, non parte della PR #297, e non devono essere committati.

## Regola da non dimenticare

Quando l'heap diventera' maturo, deve agganciarsi alla run unica come modulo esterno per analisi e proposta:

```text
read evidence -> build heap state -> exchange/refine -> produce proposal package
```

Non deve imporre modifiche al gate stabile della run unica.
