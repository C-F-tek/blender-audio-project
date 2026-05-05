<!-- IA-CARMINE-MD-SPLIT: part -->
# full-toolbox-0-to-10-semi-automatic-procedure — parte 002 di 004

Sorgente indice: [`../full-toolbox-0-to-10-semi-automatic-procedure.md`](../full-toolbox-0-to-10-semi-automatic-procedure.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)
- [Parte successiva](part-003.md)

### Regenerate repo help, context and evidence after corpus purge

When generated context corpus is deleted or default-excluded, run this phase before any new full-toolbox/provider decision run.

Required order:

```text
1. Delete/purge generated corpus.
2. Rebuild indexAI with Tools/npu/build_project_ai_index.py --force.
3. Remove stale project_awareness snapshots that point to deleted corpus.
4. Rebuild tool inventory and memory inventory.
5. Rebuild repository consistency map and smoke.
6. Run Python syntax validation.
7. Regenerate runtime tool capability manifest.
8. Regenerate semantic cloud handoff chunks.
9. Verify no stale references remain outside generator/policy docs.
```

Do not commit `output/**`. Commit only regenerated source/index files and explicit evidence under `docs/LOCAL_VALIDATION_EVIDENCE`.


### Full run unica - TUTTO SU TUTTO canonical command

The current canonical full run is not the conservative/read-only variant. It is the all-lanes run.

Use the unified launcher, current branch, one global stamp, `-Mode all`, and `-Full0To10`. Do not add `-No*` flags unless performing a deliberate maintenance/debug run.

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode all `
  -Full0To10 `
  -Stamp $Stamp `
  -RunIntensity balanced `
  -BudgetMinutes 30 `
  -MaxRounds 20 `
  -FilesPerRound 8 `
  -MaxContextFiles 220 `
  -MaxCharsPerFile 6000 `
  -MaxNewTokens 3600 `
  -KeepAlive 35m
```

This activates the full runtime body: probes, providers, GPU/NPU advisory/audit, workload quality, evidence, patch specs, telemetry, memory lane, integrated decision loop and validation reports.

The run still remains report/proposal oriented until a separate explicit patch-apply command is issued.

### Strict real-run tool activation

Every real run must activate all declared probes, tools and provider lanes unless an explicit `-No*` flag disables a specific lane.

A real run is any launcher execution that is not `-DryRun` and is not limited to `smoke` or reset planning.

Strict real-run activation enables:

```text
RunOllamaProbe
RunNpuProbe
RunNpuDecodeSmoke
RunMultistepProviderWorkflow
BuildWorkloadQualityReport
BuildEvidence
GeneratePatchSpecs
UseOllamaAdvisory
UsePrimaryAdvisoryProvider
RunLegacyFullToolboxIntegrated
SaveInputsToMemoryDb
```

The policy does not fake successful provider execution. If a required provider lane does not produce its required files, the workflow must create schema-valid failure artifacts so the bundle contains a complete diagnosis instead of a missing-file cascade.

Required provider artifacts include:

```text
output/ai_pipeline/full_toolbox_<Stamp>_orchestrator.json
output/ai_pipeline/full_toolbox_<Stamp>_parallel_gpu.json
output/ai_pipeline/agent_review_evidence_sufficiency.json
```

`-NoStrictRealRunActivation` is reserved for local maintenance/debug runs only.

## Global guardrails

Never do without explicit user command:

```text
delete
force-push
rewrite history
change secrets
change permissions
change billing
change visibility
deploy production
merge to master/protected branch
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
raw checkpoints
large full analysis JSON outside compact evidence policy
```

Default state for canonical full run:

```text
TUTTO SU TUTTO runtime activation
all declared probes/tools/provider/advisory/evidence/patch-spec/memory lanes active
manual-review required for patch application
patch application only through explicit --apply or explicit source-edit instruction
Git destructive actions remain separate explicit commands
```

---

# Procedure variants

## Variant A - Expanded/manual 0 -> 10 full toolbox run

This is the full manual 0 -> 10 flow. It is the expanded version of the procedure Carmine used before the integrated wrapper existed.

Current post-PR171 default branch is `master`. If reproducing the historical PR #170 run, replace `master` with `codex/agent-review-decision-loop`.

Compatibility note:

```text
The historical pasted command used -WriteCompactBundle with run_full_memory_tool_regeneration.ps1.
Current workflow-compatible usage omits that parameter unless the script explicitly exposes it.
```

### 0. Sync repository and setup

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
"STAMP=$Stamp"
```

### 1. CPU/helper: optional memory/tool reload

```powershell
.\Tools\workflow\run_full_memory_tool_regeneration.ps1 `
  -RepoRoot . `
  -Stamp $Stamp `
  -Profile full_refactor `
  -Objective "Reload IA-Carmine full toolbox context before agent review decision-loop full run."

$MemoryWorkflow = ".\output\validation\full_memory_tool_regeneration_${Stamp}_workflow.json"
$MemoryBundleJson = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_${Stamp}.json"
$MemoryBundleMd = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_${Stamp}.md"
$MemoryLineCountCsv = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_${Stamp}.csv"
```

Inspect memory guardrails:

```powershell
Get-Content $MemoryWorkflow -Raw |
  ConvertFrom-Json |
  Select-Object passed, provider_execution_performed, patch_application_performed, sqlite_write_performed, persistent_memory_write_performed, errors, warnings
```

Expected:

```text
passed=True
provider_execution_performed=False
patch_application_performed=False
sqlite_write_performed=False
persistent_memory_write_performed=False
```

### 2. CPU/helper: full Python inventory

```powershell
python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output ".\output\validation\python_line_count_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\validation\python_line_count_full_toolbox_$Stamp.md"

$LineCountReport = Get-Content ".\output\validation\python_line_count_full_toolbox_$Stamp.json" -Raw | ConvertFrom-Json
$LineCountCsv = $LineCountReport.csv_written
$LineCountAllMd = ".\output\validation\python_line_count_all_python_files_$Stamp.md"

$Rows = Import-Csv $LineCountCsv | Sort-Object {[int]$_.Lines} -Descending
$TotalLines = ($Rows | Measure-Object -Property Lines -Sum).Sum
$FileCount = ($Rows | Measure-Object).Count

$Lines = @()
$Lines += "# Full Python Line Count Inventory"
$Lines += ""
$Lines += "- Stamp: $Stamp"
$Lines += "- CSV: $LineCountCsv"
$Lines += "- File count: $FileCount"
$Lines += "- Total Python lines: $TotalLines"
$Lines += "- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20."
$Lines += ""
$Lines += "| Lines | File |"
$Lines += "|---:|---|"
foreach ($Row in $Rows) {
  $Lines += "| $($Row.Lines) | ``$($Row.File)`` |"
}
$Lines | Set-Content -Path $LineCountAllMd -Encoding UTF8
```

### 3. CPU/helper: static validation and code interpreter report

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_full_toolbox_$Stamp.json"

python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/npu `
  --input Tools/workflow `
  --input Scripting/v61b `
  --input Scripting/shared `
  --output ".\output\analysis\code_interpreter_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\analysis\code_interpreter_full_toolbox_$Stamp.md"
```

### 4. CPU/helper: contract/tool smoke before provider run

```powershell
python -m py_compile `
  .\Tools\ai\gpu_planner_json_contract.py `
  .\Tools\ai\replay_gpu_planner_json_contract.py `
  .\Tools\ai\analyze_gpu_npu_run_sync.py `
  .\Tools\ai\build_deterministic_recommendations.py `
  .\Tools\ai\build_agent_review_patch_plan.py `
  .\Tools\ai\build_full_toolbox_run_telemetry_summary.py `
  .\Tools\ai\build_runtime_tool_usage_telemetry.py `
  .\Tools\ai\run_agent_review_decision_loop.py `
  .\Tools\ai\build_agent_review_patch_bundle.py `
  .\Tools\ai\run_agent_gpu_deep_planning_review.py `
  .\Tools\ai\run_agent_gpu_deep_planning_supervised.py `
  .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  .\Tools\validation\run_deterministic_recommendation_synthesizer_smoke.py `
  .\Tools\validation\run_agent_review_decision_loop_smoke.py `
  .\Tools\validation\run_agent_review_patch_bundle_builder_smoke.py

python .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  --repo-root . `
  --output ".\output\validation\gpu_planner_json_contract_smoke_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\validation\gpu_planner_json_contract_smoke_full_toolbox_$Stamp.md"

python .\Tools\validation\run_deterministic_recommendation_synthesizer_smoke.py `
  --repo-root . `
  --output ".\output\validation\deterministic_recommendation_synthesizer_smoke_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\validation\deterministic_recommendation_synthesizer_smoke_full_toolbox_$Stamp.md"

python .\Tools\validation\run_agent_review_decision_loop_smoke.py `
  --repo-root . `
  --output ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.md"

python .\Tools\validation\run_agent_review_patch_bundle_builder_smoke.py `
  --repo-root . `
  --output ".\output\validation\agent_review_patch_bundle_builder_smoke_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\validation\agent_review_patch_bundle_builder_smoke_full_toolbox_$Stamp.md"
```

### 5. NPU role: preflight/probe readiness

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output ".\output\validation\npu_provider_environment_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_full_toolbox_$Stamp.md"
```

### 6. GPU primary advisory + NPU auditor: balanced provider run

```powershell
python .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py `
  --repo-root . `
  --budget-minutes 30 `
  --max-rounds 20 `
  --files-per-round 8 `
  --max-context-files 220 `
  --max-chars-per-file 6000 `
  --max-new-tokens 3600 `
  --keep-alive 35m `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --refined-review .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review_v3.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agent_memory_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agnostic_tool_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_transient_request_context.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --report-file ".\output\analysis\code_interpreter_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\python_line_count_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\python_syntax_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\gpu_planner_json_contract_smoke_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\deterministic_recommendation_synthesizer_smoke_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\agent_review_patch_bundle_builder_smoke_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\npu_provider_environment_full_toolbox_$Stamp.json" `
  --report-file $MemoryWorkflow `
  --context-root docs `
  --context-root Tools\ai `
  --context-root Tools\validation `
  --context-root Tools\workflow `
  --context-root Tools\npu `
  --context-root Scripting\v61b `
  --context-root Scripting\shared `
  --context-root $LineCountAllMd `
  --run-npu-auditor-provider `
  --npu-auditor-every-rounds 3 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 420 `
  --npu-max-context-chars 8000 `
  --npu-max-prompt-chars 1200 `
  --npu-max-new-tokens 384 `
  --npu-final-wait-seconds 180 `
  --checkpoint-dir ".\output\ai_pipeline\full_toolbox_${Stamp}_checkpoints" `
  --gpu-output ".\output\ai_pipeline\full_toolbox_${Stamp}_parallel_gpu.json" `
  --gpu-markdown-output ".\output\ai_pipeline\full_toolbox_${Stamp}_parallel_gpu.md" `
  --output ".\output\ai_pipeline\full_toolbox_${Stamp}_orchestrator.json" `
  --markdown-output ".\output\ai_pipeline\full_toolbox_${Stamp}_orchestrator.md"

$OrchOut = ".\output\ai_pipeline\full_toolbox_${Stamp}_orchestrator.json"
$GpuOut = ".\output\ai_pipeline\full_toolbox_${Stamp}_parallel_gpu.json"
```

GPU-heavier variant if explicitly needed:

```powershell
# Replace the provider-run knobs above with:
--budget-minutes 40 `
--max-rounds 28 `
--files-per-round 12 `
--max-context-files 280 `
--max-chars-per-file 9000 `
--max-new-tokens 5200 `
--npu-auditor-every-rounds 4 `
--npu-auditor-timeout-seconds 360 `
--npu-max-context-chars 6000 `
--npu-max-prompt-chars 900 `
--npu-max-new-tokens 256 `
--npu-final-wait-seconds 120
```
