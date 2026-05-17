# External heap real run debug procedure — 2026-05-11

## Scopo

Questo documento registra la procedura corretta, verificata dalla run locale `heap_context_closure_20260511-192953`, per eseguire una run heap completa e poi il post-run package esterno.

Correzione operativa importante: `Tools/ai/build_heap_runtime_launcher_command.py` non lancia la run. E' solo un command builder reviewabile.

La run vera e' `Tools/ai/run_heap_runtime_context_closure.py`.

Il post-run vero e' `Tools/ai/run_external_heap_postrun_package.py`.

## Flusso corretto

```text
1. definire richiesta operativa
2. lanciare direttamente run_heap_runtime_context_closure.py
3. attendere fine run
4. lanciare run_external_heap_postrun_package.py
5. leggere launcher/composer/provider/pointer/revision/long-response
```

## Cosa non usare come esecuzione

Non considerare questo comando una run:

```powershell
& $RepoPy -m Tools.ai build_heap_runtime_launcher_command `
  --repo-root . `
  --profile balanced_external_heap `
  --request $DebugRequest `
  --include-postrun-package-command `
  --output .\output\validation\heap_launcher_command_debug_current_code.json
```

Quel comando genera solo un JSON con campi `command` e `postrun_package_command`.

## Run completa diretta

```powershell
cd C:\Users\carmi\blender\blender-audio-project

$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path

$DebugRequest = @"
Run heap esterno BALANCED per proposte di debug code-driven sul codice attuale.

Obiettivo:
analizza il codice reale del repository, riusa tool/evidence/memoria/context pack gia' disponibili, individua bug concreti, incoerenze di wiring, funzioni non usate ma utili al loop heap, problemi nei profili, nel launcher, nel post-run package, nei pointer e nel revision context.

Regole:
- reuse-first
- code-driven
- non modificare gate
- non modificare tool call interni del gate
- non modificare il formato dell'output finale lungo
- non applicare patch
- non dichiarare file inesistenti
- non generare placeholder/stub
- usa solo path repo reali
- produci proposal chunks concreti con TARGET_FILES, PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, VALIDATION_COMMANDS, RISKS, EXIT_DECISION
- GPU1 puo' muoversi avanti/indietro sui pointer
- GPU0 deve rivalutare blocchi vecchi e proporre refinements
- NPU deve auditare guardrail, placeholder, path inventati e source write non dichiarati
- se il prodotto non e' accettabile, blocca con reason concreta
"@

& $RepoPy -m Tools.ai run_heap_runtime_context_closure `
  --repo-root . `
  --python-exe $RepoPy `
  --request $DebugRequest `
  --budget-minutes 10 `
  --max-iterations 4 `
  --max-provider-revisions 3 `
  --timeout-seconds 1200 `
  --preflight-timeout-seconds 120 `
  --npu-device-workload-seconds 5.0 `
  --npu-device-workload-iterations 5000 `
  --startup-max-memory-chars 64000 `
  --startup-max-context-files 80 `
  --startup-max-chars-per-file 12000 `
  --allow-provider-generation
```

## Post-run package

Eseguire solo dopo la fine della run:

```powershell
& $RepoPy -m Tools.ai run_external_heap_postrun_package `
  --repo-root . `
  --include-rejected-history `
  --include-peer-blocks
```

## Selezione run reale

Per selezionare la run piu' recente usare solo directory complete, cioe' con `heap_runtime_context_closure_launcher.json` o `heap_final_proposal_composer.json`.

```powershell
$RunDir = Get-ChildItem .\output\validation -Directory |
  Where-Object { $_.Name -like "heap_context_closure_*" -and (Test-Path (Join-Path $_.FullName "heap_runtime_context_closure_launcher.json")) } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

$RunDir.FullName
```

## Controlli launcher e composer

```powershell
$Launcher = Get-Content (Join-Path $RunDir.FullName "heap_runtime_context_closure_launcher.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$Composer = Get-Content (Join-Path $RunDir.FullName "heap_final_proposal_composer.json") -Raw -Encoding UTF8 | ConvertFrom-Json

$Launcher |
  Select-Object `
    launcher_packaging_succeeded,
    launcher_passed,
    preflight_passed,
    startup_reload_passed,
    startup_can_continue,
    heap_passed,
    composer_passed,
    composer_packaging_performed,
    composer_blocking_issue_count,
    heap_returncode,
    composer_returncode,
    final_proposal_txt,
    final_download_manifest_txt |
  Format-List

$Composer |
  Select-Object `
    product_status,
    quality_output_passed,
    proposal_count,
    accepted_proposal_count,
    rejected_proposal_count,
    gpu0_review_count,
    npu_audit_count,
    blocking_issue_count |
  Format-List
```

## Controllo provider

```powershell
$ProviderDir = Join-Path $RunDir.FullName "provider_teamwork"

Get-ChildItem $ProviderDir -File |
  Select-Object Name, Length, LastWriteTime |
  Format-Table -AutoSize
```

Una run completa con provider deve avere, come minimo, file simili a:

```text
gpu0_openvino_peer_workload*.json/md
gpu1_ollama_provider_probe*.json
npu_micro_task_auditor*.json/md
```

## Controlli post-run

```powershell
$Post = Get-Content (Join-Path $RunDir.FullName "external_heap_postrun_package.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$Pointer = Get-Content (Join-Path $RunDir.FullName "external_heap_block_pointer_manifest.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$Revision = Get-Content (Join-Path $RunDir.FullName "external_heap_revision_context.json") -Raw -Encoding UTF8 | ConvertFrom-Json

$Post |
  Select-Object schema_version, passed, run_dir_selection_policy, long_response_markdown, revision_context_json |
  Format-List

$Pointer |
  Select-Object protocol, block_count, edge_count, roles_present, has_forward_pointers, has_backrefinement_pointers, has_resume_pointers, accepted_block_count, rejected_proposal_block_count |
  Format-List

$Revision |
  Select-Object protocol, resume_from_block_id, latest_block_id, parallel_task_count, gpu1_task_count, gpu0_task_count, npu_task_count, documents_copy_performed |
  Format-List
```

## Apertura output lungo

```powershell
notepad (Join-Path $RunDir.FullName "external_heap_primary_long_response.md")
```

## Evidenza run locale 2026-05-11

Run locale osservata:

```text
output/validation/heap_context_closure_20260511-192953
```

Risultati sintetici riportati dall'operatore:

```text
launcher_packaging_succeeded  : True
launcher_passed               : False
preflight_passed              : True
startup_reload_passed         : True
startup_can_continue          : True
heap_passed                   : True
composer_passed               : False
composer_blocking_issue_count : 9
heap_returncode               : 0
composer_returncode           : 2

product_status                : blocked_with_reason
quality_output_passed         : False
proposal_count                : 3
accepted_proposal_count       : 0
rejected_proposal_count       : 3
gpu0_review_count             : 7
npu_audit_count               : 7
blocking_issue_count          : 9

postrun passed                : True
pointer block_count           : 15
pointer edge_count            : 8
accepted_block_count          : 0
rejected_proposal_block_count : 3
revision parallel_task_count  : 11
revision gpu1_task_count      : 5
revision gpu0_task_count      : 3
revision npu_task_count       : 3
```

Interpretazione iniziale:

- la run vera e' partita;
- i provider sono stati eseguiti;
- heap gate passato;
- composer finale ha bloccato correttamente il prodotto;
- post-run package passato;
- pointer/revision context generati;
- nessun blocco proposta accettato;
- il debug successivo deve concentrarsi sul perche' GPU1 continua a produrre proposal rigettate/placeholder o troppo simili.

## Nota sul command builder

`Tools/ai/build_heap_runtime_launcher_command.py` resta utile per produrre una stringa comando reviewabile e per ispezionare profili/revision context, ma non e' il comando da usare come run effettiva.

Per run reali preferire il comando diretto su `run_heap_runtime_context_closure.py` finche' non verra' introdotto un launcher esecutivo separato.
