# MONOLITICO — FULL0TO10 TUTTO SU TUTTO — Bundle completo, SQLite attivo, MD apribili — 2026-05-05

## Regola operativa in cima

`Full0To10` significa **TUTTO su TUTTO**.

Non significa run parziale, non significa solo provider, non significa solo advisory, non significa solo manifest.

La run unica deve produrre e rendere disponibile **tutto il prodotto necessario per valutazioni di ogni genere sulla run**.

Quindi:

```text
SQLite/memory lane deve essere attiva nel perimetro Full0To10 salvo opt-out esplicito.
CSV/index/discovery devono partire a inizio run come factual base.
Il bundle deve includere davvero tutto ciò che serve alla revisione: file singoli e directory ricorsive necessarie.
Se una directory evidence viene prodotta, non basta il manifest quando la review richiede i contenuti.
Il bundle deve includere anche directory come full_toolbox_<STAMP>_cloud_semantic_deterministic_chunks/.
Nessuna lane deve sparire silenziosamente: active, disabled, degraded, blocked, failed o unavailable devono essere visibili.
```

La directory locale:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260505-193057_cloud_semantic_deterministic_chunks/
```

non era entrata nello ZIP `20260505-193057` perché la seconda procedura `Compress-Archive -Path "$EvidenceDir\*${Stamp}*.md/json/csv"` non includeva la directory ricorsiva.

Questo è da considerare **difetto di bundle completeness**, non dettaglio secondario.

## Stato chat

Questa chat è diventata pesante e operativamente obsoleta.

Ripartire da questo file in una nuova chat.

Non ricostruire tutto da memoria conversazionale. Usare questo handoff, i file canonici e il bundle/evidence reale.

## Repository

```text
Repository: C-F-tek/blender-audio-project
Branch: codex/unified-local-ai-refactor-launcher
PR corrente: #187 feat(workflow): add unified local AI refactor launcher
Ultimo bundle analizzato: ia_carmine_unused_useful_tool_promotion_full_run_bundle_20260505-193057.zip
Commit ZIP pushato: 4cbfaf5
Modalità: GitHub-only/API finché non richiesto accesso locale
```

## Guardrail sempre validi

Non fare:

```text
merge su master
delete distruttivi
force-push
rewrite history
deploy
modifiche secret/permission/billing/visibility
commit output/**
commit indexAI/code_chunks/**
commit indexAI/project_code_chunks/**
commit *.db / *.sqlite / *.sqlite3
commit renders/**
Blender runtime
FFmpeg runtime
patch specs apply automatico
```

Quando si tocca codice/script, indicare sempre il numero di righe risultante.

## Correzione dottrinale richiesta

La prossima evoluzione della run unica deve essere irrobustita così:

```text
Full0To10 = tutto attivo salvo opt-out esplicito.
SQLite/memory non deve essere bloccato di default nel perimetro Full0To10; deve essere presente come lane, almeno report/scratch/manifest, con persistent write protetta da conferma.
NPU/GPU0 possono diventare helper/coworker solo dopo capability/report/broker contract.
Il bundle deve essere completo, ricorsivo e verificato.
La review non deve dipendere da file locali non inclusi nel bundle.
```

Distinzione importante:

```text
SQLite/memory lane attiva = sì, nel perimetro Full0To10.
Persistent SQLite write = protetta, visibile e confermata esplicitamente.
Raw DB commit = mai.
```

## Bundle completeness obbligatoria

Ogni run unica seria deve produrre un bundle ZIP completo.

Il bundle deve includere, quando prodotti:

```text
launcher manifest
phase_status / phase_reports
workflow report
integrated decision-loop report
deterministic recommendations
agent-review patch plan
provider diagnostics
ai_workload_report_quality
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV when available
Python line-count CSV/MD
repository consistency map/smoke
auto-discovery report when relevant
index repair plan/report when relevant
all generated evidence directories needed for review, recursively
artifact list
post-run git status
```

Special rule:

```text
If docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunks/ exists and is part of review evidence, include it recursively in the bundle.
Do not include only its manifest and call the bundle complete.
```

## Bundle builder requirement

A future patch must add or harden a real bundle builder/checker.

Required behavior:

```text
build bundle input list from artifact manifest, not fragile globs only
include required directories recursively
exclude forbidden paths
verify every listed artifact exists before zipping
write artifact_list_<STAMP>.txt/json
write git_status_after_run_<STAMP>.txt
write bundle_completeness_report_<STAMP>.json/md
fail or warn clearly when required directories are missing
```

Forbidden in bundle source unless explicitly allowed:

```text
output/** raw unbounded tree
indexAI/code_chunks/** as source artifact
indexAI/project_code_chunks/** as source artifact
*.db / *.sqlite / *.sqlite3
renders/**
raw audio/video/media
```

Allowed in bundle:

```text
selected compact evidence
selected generated evidence directories under docs/LOCAL_VALIDATION_EVIDENCE/
manifest/report files needed for review
ZIP itself as uploaded/release/chat artifact
```

## SQLite/memory requirement

SQLite/memory must be treated as part of TUTTO su TUTTO.

Current direction:

```text
runtime_sqlite_memory exists in capability manifest
memory lane should participate in Full0To10 as report/scratch/search/manifest lane
persistent write remains explicit-confirm only
raw DB never committed
memory manifest/summary must enter telemetry and shared bundle when memory lane runs
```

Next architecture target:

```text
SQLite heap memory
FTS5 keyword/BM25
embedding cache
context namespace
memory_add_text
memory_add_file
memory_search
memory_export_manifest
hybrid search with FTS fallback
```

## NPU/GPU0 direction

Do not promote NPU to primary advisory.

Correct model:

```text
GPU/Ollama primary lane = planner/advisor/patch-plan reasoning
NPU/OpenVINO = bounded tool-proxy helper
Intel GPU0/OpenVINO = report-only coworker first, then bounded worker after contracts
CPU = deterministic validators/inventory/reporting
SQLite = shared heap memory
runtime broker = policy/routing/telemetry/capability control plane
```

Before real worker activation:

```text
NPU tool-proxy request/response schema
GPU0 worker request/response schema
runtime hardware capability manifest
broker delegation contract
telemetry counters
validators
no-source-write guardrails
bundle visibility
```

## MD size policy

Non scrivere file Markdown enormi non apribili.

Regola:

```text
Se un MD mantenuto supera 500 righe, diventa o viene affiancato da una directory documentale <nome>.md/.
Dentro: README.md + file numerati piccoli.
La regola è ricorsiva.
```

Gli agenti devono sapere che un path che finisce in `.md` può essere anche una directory.

Non creare nuovi mostri Markdown.

Questa chat è già prova del problema: contenuti lunghi vanno modularizzati.

## Stato del bundle 20260505-193057

Analisi sintetica già fatta:

```text
passed: true
recommendation_count: 20
patch_plan_count: 20
deterministic_synthesizer_used: true
provider_execution_performed: true
patch_application_performed: false
source_writes_performed: false
persistent_memory_write_performed: false
manual_review_required: true
```

Broker bootstrap:

```text
tool_call_entry_count: 3
executed_count: 3
failed_count: 0
blocked_count: 0
```

Provider/tool gap:

```text
runtime_tool_request_count: 220
runtime_tool_execution_count: 0
provider tool requests not executed/reinjected yet
```

Repository consistency:

```text
finding_count: 9615
high: 2457
medium: 7115
low: 43
```

NPU:

```text
npu_audit_count: 18
npu_audit_success_count: 18
npu_to_gpu_avg_duration_ratio: about 2.963
```

Main issue from this bundle:

```text
The uploaded ZIP did not include the deterministic chunks directory recursively.
This must be fixed in future bundle completeness logic.
```

## Immediate next patch recommendation

Do not start from dead-code deletion.

Do not promote NPU/GPU0 real coworker execution immediately.

First harden the foundation:

```text
1. bundle completeness builder/checker with recursive evidence directory inclusion
2. SQLite/memory lane Full0To10 visibility and manifest policy
3. hardware capability manifest report-only for CPU/GPU0/NPU
4. NPU tool-proxy and GPU0 worker schema docs
5. broker delegation contract + telemetry counters
6. validators for bundle completeness and hardware/delegation reports
```

## Local cleanup state

User reports local working tree has been cleaned after bundle push.

Before next work, verify:

```powershell
git status --short
git log --oneline -8
```

Expected remote head contains:

```text
4cbfaf5 test(ai): add unused useful tool promotion run evidence
027ffea docs(ai): add global markdown directory split policy
316e088 docs(chatgpt): add recursive md directory policy
```

## Start next chat with this instruction

```text
Read CHATGPT/next-chat-monolithic-full0to10-bundle-sqlite-memory-handoff-2026-05-05.md first.
Continue on branch codex/unified-local-ai-refactor-launcher.
Full0To10 means TUTTO su TUTTO: SQLite/memory lane active, CSV/index/discovery at run start, complete recursive bundle, telemetry/capability/final summary, provider diagnostics, decision loop, recommendations, patch plan and evidence directories included.
Do not create Markdown monsters: split maintained docs over 500 lines into <name>.md/ directories with README.md and numbered child docs.
Next patch should harden bundle completeness + SQLite/memory visibility + hardware capability/delegation contracts, report-only first.
```
