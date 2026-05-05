<!-- IA-CARMINE-MD-SPLIT: part -->
# full-toolbox-0-to-10-semi-automatic-procedure — parte 003 di 004

Sorgente indice: [`../full-toolbox-0-to-10-semi-automatic-procedure.md`](../full-toolbox-0-to-10-semi-automatic-procedure.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-002.md)
- [Parte successiva](part-004.md)

### 7. CPU/helper: replay GPU contract + GPU/NPU sync analysis

```powershell
python .\Tools\ai\replay_gpu_planner_json_contract.py `
  --repo-root . `
  --gpu-report $GpuOut `
  --output ".\output\analysis\gpu_json_contract_replay_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\analysis\gpu_json_contract_replay_full_toolbox_$Stamp.md"

python .\Tools\ai\analyze_gpu_npu_run_sync.py `
  --repo-root . `
  --orchestrator $OrchOut `
  --output ".\output\analysis\gpu_npu_run_sync_full_toolbox_$Stamp.json" `
  --markdown-output ".\output\analysis\gpu_npu_run_sync_full_toolbox_$Stamp.md"
```

### 8. Decision loop: evidence -> recommendations -> patch plan

```powershell
python .\Tools\ai\run_agent_review_decision_loop.py `
  --repo-root . `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --orchestrator $OrchOut `
  --gpu-report $GpuOut `
  --tool-report ".\output\analysis\code_interpreter_full_toolbox_$Stamp.json" `
  --tool-report ".\output\validation\python_line_count_full_toolbox_$Stamp.json" `
  --tool-report ".\output\validation\python_syntax_full_toolbox_$Stamp.json" `
  --tool-report ".\output\validation\gpu_planner_json_contract_smoke_full_toolbox_$Stamp.json" `
  --tool-report ".\output\validation\deterministic_recommendation_synthesizer_smoke_full_toolbox_$Stamp.json" `
  --tool-report ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.json" `
  --tool-report ".\output\validation\agent_review_patch_bundle_builder_smoke_full_toolbox_$Stamp.json" `
  --tool-report ".\output\validation\npu_provider_environment_full_toolbox_$Stamp.json" `
  --tool-report ".\output\analysis\gpu_json_contract_replay_full_toolbox_$Stamp.json" `
  --tool-report ".\output\analysis\gpu_npu_run_sync_full_toolbox_$Stamp.json" `
  --tool-report $MemoryWorkflow `
  --recommendations-output ".\output\ai_pipeline\full_toolbox_${Stamp}_deterministic_recommendations.json" `
  --recommendations-markdown ".\output\ai_pipeline\full_toolbox_${Stamp}_deterministic_recommendations.md" `
  --bridge-orchestrator-output ".\output\ai_pipeline\full_toolbox_${Stamp}_bridge_orchestrator.json" `
  --patch-plan-output ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.json" `
  --patch-plan-markdown ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.md" `
  --output ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.json" `
  --markdown-output ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.md" `
  --max-recommendations 80 `
  --max-patch-plans 0 `
  --min-recommendations 20 `
  --min-patch-plans 20
```

### 9. Post-validation packet and compact evidence

```powershell
$ContextFiles = @(
  ".\docs\LOCAL_AI_TASKS\code-refactor-0-to-10-procedure.md",
  ".\docs\LOCAL_AI_TASKS\full-toolbox-0-to-10-semi-automatic-procedure.md",
  ".\docs\LOCAL_AI_TASKS\gpu-npu-parallel-evidence-runbook.md",
  ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-procedure.md",
  ".\Tools\ai\run_agent_review_decision_loop.py",
  ".\Tools\ai\build_deterministic_recommendations.py",
  ".\Tools\ai\build_agent_review_patch_plan.py",
  ".\Tools\ai\build_agent_review_patch_bundle.py",
  ".\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py",
  ".\Tools\validation\run_agent_review_decision_loop_smoke.py",
  ".\Tools\validation\run_agent_review_patch_bundle_builder_smoke.py",
  $LineCountAllMd,
  ".\output\analysis\code_interpreter_full_toolbox_$Stamp.md",
  ".\output\analysis\gpu_json_contract_replay_full_toolbox_$Stamp.md",
  ".\output\analysis\gpu_npu_run_sync_full_toolbox_$Stamp.md",
  ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.md",
  ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.md",
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.md",
  ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.md"
)

$ReportFiles = @(
  $OrchOut,
  $GpuOut,
  ".\output\analysis\code_interpreter_full_toolbox_$Stamp.json",
  ".\output\validation\python_line_count_full_toolbox_$Stamp.json",
  ".\output\validation\python_syntax_full_toolbox_$Stamp.json",
  ".\output\validation\gpu_planner_json_contract_smoke_full_toolbox_$Stamp.json",
  ".\output\validation\deterministic_recommendation_synthesizer_smoke_full_toolbox_$Stamp.json",
  ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.json",
  ".\output\validation\agent_review_patch_bundle_builder_smoke_full_toolbox_$Stamp.json",
  ".\output\validation\npu_provider_environment_full_toolbox_$Stamp.json",
  ".\output\analysis\gpu_json_contract_replay_full_toolbox_$Stamp.json",
  ".\output\analysis\gpu_npu_run_sync_full_toolbox_$Stamp.json",
  ".\output\ai_pipeline\full_toolbox_${Stamp}_deterministic_recommendations.json",
  ".\output\ai_pipeline\full_toolbox_${Stamp}_bridge_orchestrator.json",
  ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.json",
  ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.json",
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.json",
  ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.json",
  $MemoryWorkflow
) | Where-Object { Test-Path $_ }

$params = @{
  Profile     = "core"
  ContextFile = $ContextFiles
  ReportFile  = $ReportFiles
}

& .\Tools\workflow\run_post_validation_ai_packet.ps1 @params
```

Build compact evidence:

```powershell
python -m Tools.ai.build_shared_toolbox_ai_to_ai_bundle `
  --repo-root . `
  --stamp $Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --validate-bundle `
  --recursive-max-files 160 `
  --chunk-large-files-lines 200

python -m Tools.ai.build_github_evidence_bundle `
  --repo-root . `
  --basename full_toolbox_agent_review_decision_loop_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($ReportFiles -join ',') `
  --report ".\output\ai_pipeline\repository_change_proposals.json" `
  --report ".\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json" `
  --report ".\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json" `
  --artifact ".\docs\LOCAL_AI_TASKS\code-refactor-0-to-10-procedure.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\full-toolbox-0-to-10-semi-automatic-procedure.md" `
  --artifact ".\docs\LOCAL_AI_TASKS\gpu-npu-parallel-evidence-runbook.md" `
  --artifact ".\Tools\ai\run_agent_review_decision_loop.py" `
  --artifact ".\Tools\ai\build_agent_review_patch_bundle.py" `
  --artifact ".\Tools\validation\run_agent_review_decision_loop_smoke.py" `
  --artifact ".\Tools\validation\run_agent_review_patch_bundle_builder_smoke.py" `
  --artifact $LineCountAllMd `
  --artifact $LineCountCsv `
  --artifact ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.md" `
  --artifact ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.md" `
  --max-included-artifact-chars 16000 `
  --max-included-artifacts 24

python -m Tools.validation.check_github_evidence_bundle `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_$Stamp.json" `
  --output ".\output\validation\full_toolbox_agent_review_decision_loop_${Stamp}_bundle_validation.json"
```

### 10. Final scoped validation and summary inspect

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_full_toolbox_final_$Stamp.json"

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --report-file ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\agent_review_patch_bundle_builder_smoke_full_toolbox_$Stamp.json" `
  --report-file ".\output\validation\python_syntax_full_toolbox_final_$Stamp.json" `
  --report-file ".\output\validation\full_toolbox_agent_review_decision_loop_${Stamp}_bundle_validation.json" `
  --output ".\output\validation\validation_report_contract_full_toolbox_final_$Stamp.json"

git diff --check
git status --short

Get-Content ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, recommendation_count, patch_plan_count, deterministic_synthesizer_used, patch_plan_fallback_used, provider_execution_performed, patch_application_performed, errors, warnings

Get-Content ".\output\validation\full_toolbox_agent_review_decision_loop_${Stamp}_bundle_validation.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```

---

## Variant B - Integrated no-provider semi-automatic flow

Use this when existing orchestrator/GPU artifacts are valid enough and the goal is to test the deterministic decision and patch-plan path quickly.

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch master
git pull --ff-only origin master
git status --short

$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

.\Tools\workflow\run_agent_review_full_toolbox_decision_loop_integrated.ps1 `
  -RepoRoot . `
  -Stamp $Stamp
```

Inspect:

```powershell
Get-Content ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_integrated.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, base_workflow_passed, warning_policy_passed, decision_recovered, recommendation_count, patch_plan_count, input_nonfatal_warning_count, fatal_report_failure_count, provider_execution_performed, patch_application_performed, sqlite_write_performed, persistent_memory_write_performed, errors, warnings
```

Expected when diagnostic inputs are recovered:

```text
passed=True
decision_recovered=True
recommendation_count >= 1
patch_plan_count >= 1
fatal_report_failure_count=0
```

## Variant C - Integrated provider semi-automatic flow

Use when a fresh full GPU/NPU run is needed.

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

.\Tools\workflow\run_agent_review_full_toolbox_decision_loop_integrated.ps1 `
  -RepoRoot . `
  -Stamp $Stamp `
  -RunGpuNpuProvider
```

GPU-heavier variant:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

.\Tools\workflow\run_agent_review_full_toolbox_decision_loop_integrated.ps1 `
  -RepoRoot . `
  -Stamp $Stamp `
  -RunGpuNpuProvider `
  -BudgetMinutes 40 `
  -MaxRounds 28 `
  -FilesPerRound 12 `
  -MaxContextFiles 280 `
  -MaxCharsPerFile 9000 `
  -MaxNewTokens 5200 `
  -NpuAuditorEveryRounds 4 `
  -NpuAuditorTimeoutSeconds 360 `
  -NpuMaxContextChars 6000 `
  -NpuMaxPromptChars 900 `
  -NpuMaxNewTokens 256 `
  -NpuFinalWaitSeconds 120
```

## Variant D - Patch bundle builder from a real patch plan

Use after a successful decision loop has produced:

```text
output/patch_specs/full_toolbox_<STAMP>_agent_review_patch_plan.json
```

Find latest patch plans:

```powershell
Get-ChildItem .\output\patch_specs\*agent_review_patch_plan.json |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 FullName, LastWriteTime, Length
```

Set target patch plan:

```powershell
$Stamp = "20260503-160523"
$PatchPlan = ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.json"
Test-Path $PatchPlan
```

Build bundle:

```powershell
python .\Tools\ai\build_agent_review_patch_bundle.py `
  --repo-root . `
  --patch-plan $PatchPlan `
  --output-dir .\output\validation\patch_bundles `
  --basename full_toolbox_agent_review_patch_bundle `
  --stamp $Stamp `
  --output ".\output\validation\agent_review_patch_bundle_builder_${Stamp}.json" `
  --markdown-output ".\output\validation\agent_review_patch_bundle_builder_${Stamp}.md" `
  --write-bundle
```

Expected:

```text
passed=True
operation_count > 0
bundle_zip is not empty
patch_application_performed=False
sqlite_write_performed=False
```

Inspect operations:

```powershell
Get-Content ".\output\validation\patch_bundles\full_toolbox_agent_review_patch_bundle_${Stamp}\patches\manifest.json" -Raw |
  ConvertFrom-Json |
  Select-Object -ExpandProperty operations |
  Select-Object id, plan_id, target, kind, mode
```

Dry-run:

```powershell
python ".\output\validation\patch_bundles\full_toolbox_agent_review_patch_bundle_${Stamp}\run_patch_bundle.py" --repo-root .
```

Apply only after manual review:

```powershell
python ".\output\validation\patch_bundles\full_toolbox_agent_review_patch_bundle_${Stamp}\run_patch_bundle.py" --repo-root . --apply
```

Validate after apply:

```powershell
& ".\output\validation\patch_bundles\full_toolbox_agent_review_patch_bundle_${Stamp}\scripts\validate_after_patch.ps1" -RepoRoot .

git diff --stat
git diff --check
git status --short
```

Stage only modified source/docs files. Never stage `output/**`.

Example from PR #171:

```powershell
git add `
  .\Tools\validation\README.md `
  .\docs\AI_ONBOARDING.md `
  .\docs\AI_REFERENCE_ONBOARDING.md `
  .\docs\AI_REFERENCE_SOURCE_MAP.md `
  .\docs\CODE_CONSULTATION_REPORT.md `
  .\docs\JSON_SCHEMAS.md `
  .\docs\LOCAL_AI_CORE_TOOL_ACTIVATION.md

git commit -m "docs(ai): apply review patch bundle notes"
git push
```
