# Real product run unica runbook — 2026-05-10

## Stato codice riflesso dal runbook

Questo documento fotografa la struttura reale dopo la chiusura della catena PR #270-#296. La run unica non è più una sequenza manuale guidata fase per fase: l'operatore fornisce una richiesta Markdown, il wrapper esegue preflight obbligatorio, poi delega al launcher unico. Il centro resta dinamico: heap/exchange, GPU1, GPU0, NPU, memoria condivisa, SQLite FTS, broker/tool, adapter ufficiale, provider advisory e patch-spec lane cooperano e producono evidenza.

Entrata e uscita sono invece rigide:

- entrata unica: `Tools/workflow/run_unified_real_product_pr.ps1`;
- centro dinamico: `Tools/workflow/run_unified_local_ai_refactor.ps1`;
- uscita unica: review PR product validato da final product contract.

## Catena reale corrente

Ordine concettuale:

1. task Markdown o `-ProcessGateTask`;
2. RepoPy/PYTHONPATH gate;
3. mandatory real product preflight;
4. launcher unico;
5. inventory, JSON, Markdown, script census, semantic chunks, context pack, agent state;
6. workload quality routing;
7. heap/exchange runtime entry;
8. task ingress contract;
9. heap peer runtime manifest;
10. heap/exchange closure audit;
11. OpenVINO GPU0 observable workload;
12. official local AI adapter;
13. Ollama/GPU1 advisory packet;
14. task Markdown patch suggestion report;
15. generated patch specs for review PR;
16. heap/exchange runtime exit product;
17. final chain contract;
18. runtime evidence correlation;
19. `prepare_review_pr.py`;
20. draft PR finale.

La catena non deve continuare fingendo prodotto quando l'apply report espone `operation_count=0` o solo draft metadata-only. Dopo #295, le generated patch specs metadata-only falliscono in modo esplicito se `--apply` è richiesto. Dopo #296, il proposal builder può leggere evidenza runtime current-stamp e generare `P-RUNTIME-PEER-EVIDENCE-FEED` con operazioni concrete reviewable.

## Preflight obbligatorio

Il wrapper real product esegue sempre `Tools/validation/run_real_product_preflight_gate.py` prima della delega al launcher. Non esiste skip operativo per questa gate.

Il preflight verifica almeno:

- real product profile smoke;
- intrinsic capability contract;
- runtime mesh contract;
- OpenVINO peer topology contract;
- review PR prepare args;
- product readiness;
- full product PR chain smoke;
- runtime evidence correlation;
- launcher wiring della correlation;
- manifest runtime evidence correlation schema;
- review PR final product contract.

Il preflight non esegue provider reali, non applica patch, non lancia Blender/FFmpeg, non crea PR. Serve a impedire falsi positivi prima della parte dinamica.

## GPU1, GPU0, NPU: semantica corrente

GPU1 è la lane advisory/provider principale legata a Ollama/CUDA. Deve ragionare sulle evidenze correnti e non solo su report statici. Dopo #296, `build_repository_change_proposals.py` scopre report current-stamp da output runtime e li usa nella proposal lane.

GPU0 è la lane OpenVINO/tool workload. Dopo l'hardening osservabile, non è sufficiente produrre un JSON minimale: il workload deve essere osservabile, durare abbastanza e dichiarare esito reale nel report `openvino_gpu0_workload_<stamp>.json`.

NPU è peer micro/diagnostic lane, non ancora primary compute lane. Non deve essere spacciata come generazione computazionale se il report dichiara solo diagnostic/report-only. Il suo valore attuale è presenza nel mesh, probing, evidence e contesto condiviso per GPU1/GPU0.

## Generated patch specs e prodotto reale

Regola attuale:

- task Markdown sotto `output/local_ai_task_inputs/` è entry contract, non sorgente obbligatoria di patch;
- se non contiene fence patch-suggestion, può passare come `deferred_to_runtime_product=true`;
- una patch-spec metadata-only non è prodotto reale;
- con `--apply`, `apply_generated_patch_specs_for_review_pr.py` deve fallire se non trova operazioni concrete allowlisted;
- operazioni concrete ammesse: `replace_once`, `append_once`, `insert_after_once`, `insert_before_once`, `write_file`;
- target vietati: `output/**`, `indexAI/**`, `docs/LOCAL_VALIDATION_EVIDENCE/**`, `renders/**`, database/runtime artifact.

## Runtime evidence feed verso proposals

Dopo #296, la proposal lane legge evidenze current-stamp tra cui:

- `output/validation/openvino_gpu0_workload_*.json`;
- `output/validation/npu_micro_peer_*.json`;
- `output/validation/*runtime_evidence_correlation*.json`;
- `output/validation/*patch_suggestion_bundle_apply*.json`;
- `output/local_ai_runs/*/ai_packets/heap_exchange_runtime_entry.json`;
- `output/local_ai_runs/*/ai_packets/heap_peer_runtime_manifest.json`;
- `output/local_ai_runs/*/ai_packets/heap_exchange_closure_audit.json`;
- `output/patch_specs/*_manifest.json`.

Se heap/GPU0/NPU/runtime-correlation sono presenti ma il prodotto generato è metadata-only, la proposta corretta è `P-RUNTIME-PEER-EVIDENCE-FEED`, non il fallback generico `P-NEXT-NPU-OBSERVABILITY`.

## Comando operativo consigliato

Prerequisiti:

- working tree pulito;
- `indexAI/code_chunks/**` ripristinato se modificato da run precedente;
- `docs/LOCAL_VALIDATION_EVIDENCE/**` non usato come prodotto di commit;
- `.venv` disponibile come RepoPy;
- Ollama model disponibile;
- OpenVINO importa correttamente e vede device attesi.

Forma consigliata:

~~~powershell
cd C:\Users\carmi\blender\blender-audio-project

git switch master
git pull --ff-only origin master

git restore --worktree `
  .\indexAI\code_chunks\semantic_code_chunks.json `
  .\indexAI\code_chunks\semantic_code_chunks_manifest.json

$DirtyBefore = git status --short
if (-not [string]::IsNullOrWhiteSpace($DirtyBefore)) {
  Write-Host "[ERROR] Working tree is not clean before run:" -ForegroundColor Red
  Write-Host $DirtyBefore
  throw "Stop: clean working tree required."
}

$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy -c "import sys; print(sys.executable); import openvino as ov; print(ov.Core().available_devices)"
ollama show qwen2.5-coder:14b | Out-Host

$Stamp = "heap_exchange_process_gate_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$Branch = "CARMINEai/heap-exchange-process-gate-$Stamp"

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File ".\Tools\workflow\run_unified_real_product_pr.ps1" `
  -RepoRoot "." `
  -ProcessGateTask `
  -TaskBranch $Branch `
  -Stamp $Stamp `
  -RunIntensity custom `
  -Model "qwen2.5-coder:14b" `
  -PythonExe $RepoPy `
  -BudgetMinutes 10 `
  -MaxRounds 600 `
  -FilesPerRound 6 `
  -MaxContextFiles 3020 `
  -MaxCharsPerFile 7000 `
  -MaxNewTokens 2200 `
  -KeepAlive 15m `
  -ProviderMaxContextChars 14000 `
  -ContextPackMaxTotalChars 72000 `
  -ContextPackMaxFileChars 5000 `
  -AgentStateMaxMemoryChars 28000 `
  -MaxRecommendations 700 `
  -MaxPatchPlans 700 `
  -OfficialAdapterTimeoutSeconds 600 `
  -PreflightTimeoutSeconds 180 `
  -OpenObserverConsoles `
  -OpenExtendedObserverConsoles `
  -ObserverRefreshSeconds 2 `
  -UseGeneratedPatchSpecs `
  -ReviewPrMaxAppliedPatches 5 `
  -Push `
  -CreatePr `
  -DraftPr
~~~

## Validazioni mirate dopo sync

~~~powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path

& $RepoPy -m py_compile `
  .\Tools\ai\build_repository_change_proposals.py `
  .\Tools\ai\build_patch_specs_from_proposals.py `
  .\Tools\ai\apply_generated_patch_specs_for_review_pr.py `
  .\Tools\validation\run_repository_change_proposals_runtime_evidence_smoke.py `
  .\Tools\validation\run_generated_patch_specs_empty_product_smoke.py

& $RepoPy .\Tools\validation\run_repository_change_proposals_runtime_evidence_smoke.py --repo-root .
& $RepoPy .\Tools\validation\run_generated_patch_specs_empty_product_smoke.py --repo-root .

git diff --check
~~~

## Segnali di successo

- mandatory preflight passa;
- GPU0 produce workload osservabile;
- NPU report dichiara correttamente peer/diagnostic semantics;
- runtime evidence correlation viene emessa dopo final chain contract;
- generated patch specs non restano metadata-only;
- apply report ha `operation_count > 0` e `changed_count > 0`;
- `prepare_review_pr.py` crea commit di prodotto e draft PR;
- il prodotto finale non include `output/**`, `indexAI/code_chunks/**`, database o artifact runtime.

## Segnali di blocco da trattare domani

- `operation_count=0` con generated specs: proposal lane ancora non sta producendo operazioni concrete;
- fallback `P-NEXT-NPU-OBSERVABILITY`: GPU1/Ollama non sta consumando abbastanza evidenza runtime current-stamp;
- `provider_execution_performed=false` in report che dichiarano provider reali: semantica falsa da correggere;
- GPU0 JSON passa ma senza attività visibile: workload osservabile da aumentare;
- NPU dichiarata come compute mentre è diagnostic-only: classificazione da bloccare;
- working tree sporco prima del task: pulire/ripristinare artifact generati prima della run.

## Standalone heap lane before full-run promotion

A new standalone heap universe lane is being incubated outside the full run.

```text
Tools/ai/run_heap_runtime_context_closure.py
```

Purpose:

```text
test the heap universe as a strict IN -> dynamic heap/refinement loop -> composed OUT runtime before wiring it as a mandatory full-run phase
```

This lane must prove:

```text
tool-owned preload
SQLite/operational memory visibility
semantic chunk/context artifact visibility
same-heap GPU1/GPU0/NPU participation
refinement artifacts consumed across revisions
composer as assembler only
final package exported on success and blocked states
```

Until those criteria are stable, the full run remains the product path and the standalone heap lane remains an incubation path. After validation, it should be promoted into the selected run-unica phase set rather than duplicated as another parallel architecture.
