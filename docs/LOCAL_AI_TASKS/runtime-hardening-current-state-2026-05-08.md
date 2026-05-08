# Runtime hardening current state — 2026-05-08

## Stato

Questo documento aggiorna lo stato operativo corrente dopo le fix su Python repo-owned, Markdown split directory-form e run unified launcher.

È intenzionalmente docs-only e non modifica workflow, provider, NPU, patch specs o runtime.

## Documenti superseded / da leggere come storici

I seguenti documenti possono contenere parti storiche non più congrue con lo stato operativo attuale:

```text
docs/LOCAL_AI_TASKS/next-chat-unified-launcher-external-controls.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
docs/LOCAL_AI_TASKS/code-aware-command-contract.md
```

Regola: non usare sezioni che indicano auto-attivazione legacy, NPU legacy auditor o lettura Markdown come solo file semplice senza verificare il codice corrente.

## Stato confermato

### Python workflow policy

Le lane workflow devono usare Python di progetto/repo:

```text
.venv/Scripts/python.exe
venv/Scripts/python.exe
.venv314/Scripts/python.exe
```

Non è più accettabile ricadere su:

```text
python da PATH
WindowsApps Python
Get-Command python
return "python"
```

Il validator di riferimento è:

```powershell
python .\Tools\validation\check_workflow_python_invocation_policy.py `
  --repo-root . `
  --output .\output\validation\workflow_python_invocation_policy.json `
  --markdown-output .\output\validation\workflow_python_invocation_policy.md
```

Expected:

```text
passed: true
violation_count: 0
```

### Markdown split directory-form

Il layout canonico per Markdown lunghi è:

```text
nomefile.md/
  README.md
  part-001.md
  part-002.md
```

Qualunque tool che legge context files Markdown deve fare prima:

```text
if path.is_file(): read_text
elif path.is_dir() and path.name.endswith(".md"): read README.md + part-*.md
else: report read_error
```

Bug già chiuso:

```text
Tools/ai/build_ai_context_pack.py
```

Bug emerso durante run e da chiudere nella PR di hardening locale:

```text
Tools/ai/suggest_repository_updates.py
```

Sintomo:

```text
PermissionError: docs/PROJECT_STATUS_POINT.md
```

Causa: `docs/PROJECT_STATUS_POINT.md` ora può essere directory split Markdown.

### context_pack evidence

La fase `context_pack` deve produrre:

```text
output/ai_context_packs/*.json
output/ai_context_packs/*.md
output/validation/*_evidence.json
output/validation/*_evidence.md
```

Non deve sporcare run ordinarie con nuovi file sotto:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*context_pack*_evidence.*
```

Quella directory è Git-trackable e deve restare riservata a evidence esplicitamente selezionata per commit.

### Legacy full-toolbox lane

La lane legacy full-toolbox integrata non deve partire implicitamente dalla run moderna.

Vietato come comportamento default:

```text
-Full0To10 -> RunLegacyFullToolboxIntegrated automatico
```

Consentito solo come diagnostica esplicita:

```powershell
-RunLegacyFullToolboxIntegrated
```

### NPU

Non reintegrare NPU tramite:

```powershell
-RunLegacyNpuAuditorProvider
```

La direzione corretta è una lane moderna:

```text
npu_micro_task_companion
```

Caratteristiche richieste:

```text
parallel
non-blocking
timeout-bound
report-only
evidence-producing
not primary advisory
no legacy auditor
```

## Run completa consigliata

Per run completa di test non disattivare fasi con `-No*` salvo richiesta esplicita.

Comando base 20 minuti:

```powershell
$Stamp = "agent_runtime_debug_lab_full_20m_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$Task = ".\docs\LOCAL_AI_TASKS\agent-runtime-debug-lab-mvp-2026-05-08.md"
$Branch = "CARMINEai/agent-runtime-debug-lab-mvp-$Stamp"

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File ".\Tools\workflow\run_unified_local_ai_refactor.ps1" `
  -RepoRoot "." `
  -Mode smoke,md,json,python,chunks,context_pack,agent_state,official,provider,patch_specs,evidence,contract,full_validation `
  -TaskFile $Task `
  -Stamp $Stamp `
  -RunIntensity custom `
  -BudgetMinutes 20 `
  -MaxRounds 12 `
  -FilesPerRound 8 `
  -MaxContextFiles 160 `
  -MaxCharsPerFile 6000 `
  -MaxNewTokens 3000 `
  -KeepAlive 25m `
  -ProviderMaxContextChars 18000 `
  -ContextPackMaxTotalChars 96000 `
  -ContextPackMaxFileChars 6000 `
  -AgentStateMaxMemoryChars 36000 `
  -MaxRecommendations 30 `
  -MaxPatchPlans 30 `
  -RepositoryConsistencyMapWorkers 8 `
  -MatrixWorkers 12 `
  -OfficialAdapterTimeoutSeconds 900 `
  -BuildWorkloadQualityReport `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UseOllamaAdvisory `
  -UsePrimaryAdvisoryProvider `
  -RunMultistepProviderWorkflow `
  -BuildEvidence `
  -GeneratePatchSpecs `
  -BuildTaskPatchSuggestionReport `
  -ReviewPrApplyDeterministicSuggestions `
  -PrepareReviewPr `
  -ReviewPrBranch $Branch `
  -ReviewPrBaseBranch "master" `
  -ReviewPrTitle "feat(ai): add agent runtime debug lab MVP" `
  -ReviewPrCommitMessage "feat(ai): add agent runtime debug lab MVP" `
  -ReviewPrPush `
  -ReviewPrCreate
```

## Monitor RAM/processi

Se PowerShell supera 8–10 GB durante una fase report-only/adapter, trattarlo come potenziale loop o child process bloccato.

Diagnostica:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match '^(powershell|pwsh|python|python.exe|ollama|git)\.exe$' } |
  Select-Object `
    @{Name='MB';Expression={[math]::Round($_.WorkingSetSize / 1MB, 1)}},
    ProcessId,
    ParentProcessId,
    Name,
    @{Name='CommandLine';Expression={
      $cmd = $_.CommandLine
      if ($cmd -and $cmd.Length -gt 220) { $cmd.Substring(0,220) + "..." } else { $cmd }
    }} |
  Sort-Object MB -Descending |
  Format-Table -AutoSize -Wrap
```

Stop mirato:

```powershell
taskkill /PID <PID> /T /F
```

Non usare kill globale su tutti i processi Python/PowerShell.

## Validazioni dopo hardening locale

```powershell
python -m py_compile .\Tools\ai\suggest_repository_updates.py
python -m py_compile .\Tools\docs\refactor_markdown_splits.py
python -m py_compile .\Tools\ai\build_ai_context_pack.py

python .\Tools\ai\suggest_repository_updates.py `
  --repo-root . `
  --profile core `
  --basename repository_update_suggestions_split_md_smoke `
  --max-context-chars 2000

git diff --check
git status --short
```

## Prossimo ordine consigliato

1. completare o fermare la run corrente;
2. applicare/validare hardening locale su `suggest_repository_updates.py`;
3. PR hardening: split Markdown + no implicit legacy + evidence output location;
4. solo dopo, PR `agent_runtime_debug_lab` MVP;
5. poi PR NPU micro-task companion lane.
