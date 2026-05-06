# IA-Carmine — Historical handoff — Refactor/reuse full-run — 20260505-143844

## Current status of this note

This note is **historical / forensic context**.

It remains useful for understanding the refactor/reuse full-run `20260505-143844`, its runtime bundle and its recommendation/patch-plan evidence, but it is no longer the current repository state by itself.

Before acting on any branch, PR, command or task reference in this file, read current state first:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

The main runtime architecture target is now:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Use this historical handoff as evidence context only. Do not treat `codex/unified-local-ai-refactor-launcher` or PR `#187` as the current active branch/PR without checking GitHub state.

## Original repository context

Repository:

```text
C-F-tek/blender-audio-project
```

Original branch at the time:

```text
codex/unified-local-ai-refactor-launcher
```

Original PR at the time:

```text
#187 feat(workflow): add unified local AI refactor launcher
```

Current interpretation:

```text
PR #187 is merged baseline context, not the current active branch by itself.
Use docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md for active branch/PR interpretation.
```

## Modalità richiesta

Lavora GitHub-only/API finché non viene richiesto esplicitamente accesso locale.

Non fare:

```text
merge su master
delete distruttivi
force-push
rewrite history
deploy
modifiche a secret/permission/billing/visibility
commit di output/**
commit di indexAI/code_chunks/**
commit di *.db / *.sqlite
commit di renders/**
Blender runtime
FFmpeg runtime
provider execution reale senza richiesta
patch specs apply automatico
```

Quando tocchi codice/script, indica sempre il numero di righe risultante.

## Dottrina corrente

```text
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensità, non perimetro
telemetria accompagna evidence e patch plan per completezza
AI-to-AI bundle, runtime telemetry, capability manifest e full toolbox telemetry summary sono parte del canale operativo
```

## Stato consolidato recente al momento della run

Commit rilevanti:

```text
86015c2 docs(debt): track triple-quote patch risk
ea88d14 fix(validation): avoid invalid escape warnings in command examples
013af90 fix(workflow): add execution-tail disable switch
3d6cb13 fix(workflow): disable transcript tail for smoke runs
2acb0a9 fix(workflow): accept launcher startup check report args
```

Fix consolidati:

```text
startup_check.py supporta --repo-root, --output, --text-output
-NoExecutionTail evita blocco finale sulle run lunghe
invalid escape warning risolti senza triple quote/raw multiline rewrite
triple quote/raw multiline problem tracciato come rischio attivo P1
```

## Task usata

```text
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
```

Obiettivo:

```text
refactor/reuse metodi
promozione helper/classi/base-class
support library comuni
tool promotion safe
centralizzazione report/manifest/path/provider/telemetry helpers
patch plan review-only
```

## Run completata

Stamp:

```text
20260505-143844
```

Manifest:

```text
output/local_ai_runs/20260505-143844_agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_unified/pipeline/unified_local_ai_refactor_manifest.json
```

Decision loop integrato:

```text
output/validation/agent_review_full_toolbox_decision_loop_20260505-143844_integrated.json
```

Esito:

```text
passed=true
recommendation_count=3
patch_plan_count=3
input_nonfatal_warning_count=0
fatal_report_failure_count=0
provider_execution_requested=true
patch_specs_requested=true
patch_application_performed=false
execution_tail_disabled=true
```

Warning osservati:

```text
Generate provider workload probe inputs failed with exit code 2
Ollama probe did not pass; Ollama workload report not written
```

Interpretazione:

```text
provider/Ollama advisory degradato
run comunque completata
decision loop passato
non rilanciare solo per questi warning
leggere provider diagnostics e workload quality dal bundle
```

## Bundle runtime fonte primaria per questa run storica

Draft release:

```text
https://github.com/C-F-tek/blender-audio-project/releases/tag/untagged-b6fed38234e80d7bc861
```

Asset:

```text
ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
```

Per analisi storica di questa run, ispezionare:

```text
manifest
decision loop integrato
recommendations
patch_plan
runtime_tool_usage_telemetry
runtime_tool_capability_manifest
full_toolbox_run_telemetry_summary
shared_toolbox_ai_to_ai_bundle
provider diagnostics
ai_workload_report_quality
warning policy
```

## Obiettivo originario nuova chat

Selezionare una mega patch controllata di refactor/reuse, review-first.

Classificare ogni proposta come:

```text
SAFE_MECHANICAL
MANUAL_REVIEW
LOCAL_VALIDATION_REQUIRED
BLENDER_RUNTIME_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE
```

Ogni patch proposta deve indicare:

```text
target file
motivazione evidence
rischio
validazione minima
line count risultante per codice/script
perché non tocca runtime vietati
```

## Triple quote / raw multiline problem

Problema attivo P1 in:

```text
docs/TECH_DEBT_TRACKER.md
TD-025 Python string patch hygiene
AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md
```

Regola:

```text
Non usare riscritture multilinea ampie triple-quoted/raw multiline per command-example cleanup.
Preferire edit one-line minimale, path POSIX-style ./Tools/... o backslash doppi.
Validare con python -m py_compile, git diff --check, line count e focused diff review.
```

## Prompt storico da incollare solo per forensic replay

Leggi integralmente il file Markdown allegato `CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md`.

Repository: `C-F-tek/blender-audio-project`

Nota: questo prompt è storico. Prima di usarlo, aggiornare branch/PR/stato con:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
GitHub current branch / PR state
```

Regole operative:

```text
- Rispondi in italiano tecnico, diretto e operativo.
- Usa il contenuto dell’MD e il bundle runtime come fonti primarie solo per analisi storica della run 20260505-143844.
- Lavora GitHub-only/API finché non richiedo esplicitamente comandi locali.
- Non fare merge su master.
- Non fare delete, force-push, rewrite history, deploy, modifiche a secret/permessi/billing/visibility.
- Non committare output/**, indexAI/code_chunks/**, *.db, *.sqlite, renders/**.
- Non eseguire Blender runtime.
- Non eseguire FFmpeg runtime.
- Non eseguire provider reali senza richiesta esplicita.
- Non applicare patch specs automaticamente.
- Quando tocchi codice/script, indica sempre il numero di righe risultante.
- Ricorda che Full0To10 significa TUTTO SU TUTTO; quick/balanced/deep/custom sono intensità, non perimetro.
- Telemetria, capability manifest, full toolbox telemetry summary e AI-to-AI bundle devono accompagnare evidence e patch plan.
- Il triple quote/raw multiline problem è rischio attivo P1: non usare riscritture multilinea ampie per command-example cleanup.
```

Obiettivo storico:

```text
analizzare il bundle della full run refactor/reuse 20260505-143844, leggere decision loop/recommendations/patch plan/telemetria/bundle/provider diagnostics/workload quality, e selezionare una mega patch controllata di refactor/reuse metodi/classi/helper/tool promotion, mantenendo tutto review-only finché non do istruzione esplicita di applicare patch.
```
