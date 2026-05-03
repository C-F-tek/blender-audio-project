# IA-Carmine Full Toolbox 0 -> 10 Semi-Automatic Procedure

## Purpose

This is the post-PR171 canonical procedure for the IA-Carmine full toolbox loop.

Use this document when the user asks for:

```text
Tutto su tutto
full toolbox
0-10
cassetta degli attrezzi completa
multi-macro patch
multi-script
multi-fase
semi-automatic process
```

The goal is not only to make an AI read files. The goal is to run a controlled AI operating system for the repository:

```text
tools -> evidence -> recommendation -> decision -> patch plan -> patch bundle -> explicit apply -> validation -> PR
```

## Current baseline

Required merged layers:

```text
PR #169: deterministic recommendation synthesizer
PR #170: agent review decision loop + integrated warning-policy workflow
PR #171: review-safe patch bundle builder + explicit bundle apply path
```

Current master baseline after PR #171:

```text
8e49305 feat(ai): add agent review patch bundle builder
fe6065a feat(ai): add agent review decision loop
2f48534 feat(ai): add deterministic recommendation synthesizer
```

## Toolbox body model

Treat the toolbox as a body. Each organ has a role. Do not mix roles.

```text
Skeleton / contracts:
  schemas, JSON contracts, report fields, validation contract, guardrails

Nervous system / orchestration:
  Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
  Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
  Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1

Brain / decision layer:
  Tools/ai/build_deterministic_recommendations.py
  Tools/ai/run_agent_review_decision_loop.py
  Tools/ai/build_agent_review_patch_plan.py

Eyes / evidence collectors:
  line count inventory
  code interpreter report
  GPU/NPU reports
  replay/sync analysis
  memory/tool inventory
  validation outputs

Immune system / validators:
  Tools/validation/check_python_syntax.py
  Tools/validation/check_validation_report_contract.py
  Tools/validation/check_github_evidence_bundle.py
  smoke tests under Tools/validation

Memory:
  indexAI/agent_memory/agent_memory.sqlite as persistent read-only inventory/status
  output/ai_runtime_memory as future operational-memory lane only if explicitly scoped

Muscles / patch execution lane:
  Tools/ai/build_agent_review_patch_bundle.py
  generated run_patch_bundle.py
  generated validate_after_patch.ps1

Bloodstream / compact evidence:
  docs/LOCAL_VALIDATION_EVIDENCE/*.json
  docs/LOCAL_VALIDATION_EVIDENCE/*.md
  compact, reviewable, Git-trackable evidence only

Hands / GitHub + CLI:
  branch, commit, PR, ready, merge
```

## Role policy

### GPU

Role:

```text
primary advisory/planner lane
large-context recommendation generation
schema/JSON diagnostic producer
```

Allowed only when explicitly requested by provider run:

```text
provider execution
live GPU planner output
full advisory pass
```

Not allowed:

```text
source mutation
SQLite write
Blender runtime
Git operation
merge
```

### NPU

Role:

```text
auditor/probe/checkpoint observer
secondary resource lane
validation/audit support
```

Not allowed:

```text
primary advisory promotion
OpenVINO GPU primary lane
source mutation
patch application
```

### CPU/helper

Role:

```text
deterministic tools
line count
syntax validation
report building
warning policy
bundle building
contract checking
```

### Memory

Current policy:

```text
persistent SQLite may be read in read-only mode
persistent SQLite must not be written unless a dedicated memory PR explicitly authorizes it
operational SQLite/cache is future work and must be separately scoped
```

Expected current full toolbox result:

```text
sqlite_write_performed=false
persistent_memory_write_performed=false
```

### Warning ledger

Warnings are not ignored. They are classified.

```text
input_nonfatal_warnings[]
fatal_report_failures[]
warning_ledger[]
warning_level_counts
warning_classification_counts
```

A `passed=false` diagnostic report can become `input_nonfatal` only if the final authoritative decision layer recovers it into valid recommendations and patch plans while guardrails remain false.

### Procedure maintenance and telemetry policy

Whenever a patch changes workflow behavior, telemetry outputs, provider/advisory semantics, planning caps, bundle contents, guardrails, or full-toolbox evidence shape, update this `0 -> 10` procedure in the same PR.

Current telemetry and cap rules:

```text
runtime tool telemetry:
  docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json
  docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.md

run telemetry summary:
  docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json
  docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.md

provider advisory:
  GPU/orchestrator passed=false may be downgraded to warning only when the deterministic decision lane produced enough valid recommendations and patch plans.

patch-plan count semantics:
  patch_plan_count must not be lower than available_patch_plan_count because of an artificial display/config cap.
  patch_plan_count may be lower only when the patch planner itself rejects candidates through target validation, cosmetic suppression, missing evidence, forbidden paths, or guardrail policy.

MaxPatchPlans:
  accepted only for backward compatibility/telemetry.
  must not truncate valid patch plans.
```


### Semantic evidence chunking for cloud handoff

Large evidence files must be split before zip/upload/cloud handoff when they exceed practical cloud-context limits. The local AI path may still generate and validate the full bundle, but the cloud handoff must use a manifest plus ordered chunks.

Current rule:

```text
Ollama local summaries are enabled by default.
Use --no-ollama only when local Ollama must be disabled.
This chunking phase uses direct local Ollama only; no NPU/GPU audit lane is executed.
Chunks must preserve source SHA256, line ranges, previous/next links, and overlap context.
Do not use plain truncation as the primary cloud-handoff strategy.
```

Canonical tool:

```powershell
python .\Tools\ai\build_semantic_evidence_chunks.py `
  --repo-root . `
  --basename full_toolbox_${Stamp}_cloud_semantic `
  --source .\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_${Stamp}.json `
  --source .\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_${Stamp}.md `
  --output-dir .\docs\LOCAL_VALIDATION_EVIDENCE `
  --chunk-output-dir .\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_${Stamp}_cloud_semantic_chunks `
  --chunk-max-chars 12000 `
  --chunk-overlap-lines 12 `
  --zip-output .\output\validation\full_toolbox_${Stamp}_cloud_semantic_chunks.zip
```

To disable Ollama:

```powershell
--no-ollama
```


### Semantic chunk collision guard

When splitting multiple sources that share the same base filename, chunk filenames must include the source suffix and a short source hash.

Required invariant:

```text
chunk_file paths in *_chunk_manifest.json must be globally unique.
.json and .md sources with the same stem must not write to the same *_chunk_0001.md path.
Regenerate the chunk directory from a clean state before cloud handoff.
```

Validation:

```powershell
$M = Get-Content ".\docs\LOCAL_VALIDATION_EVIDENCE\${Base}_chunk_manifest.json" -Raw | ConvertFrom-Json
($M.chunk_files | Group-Object | Where-Object Count -gt 1).Count
```

Expected duplicate count: `0`.


### Runtime tool capability manifest

Every cloud/AI-to-AI handoff must carry the tool body, not only the evidence mind.

Required files:

```text
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.md
```

The capability manifest must describe:

```text
- allowlisted tool names
- allowed args
- guardrails
- safe default mode
- broker source file
- observed usage by tool/caller/phase
- rule: cloud can reason about tools; execution remains local broker-controlled
```

Semantic chunk handoff must include the capability manifest as a source file.


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

Default state:

```text
report-only until explicit apply
manual-review required
provider execution only with explicit provider flag/path
patch application only through explicit --apply or explicit source-edit instruction
```

---

# Procedure variants

## Variant A — Expanded/manual 0 -> 10 full toolbox run

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

## Variant B — Integrated no-provider semi-automatic flow

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

## Variant C — Integrated provider semi-automatic flow

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

## Variant D — Patch bundle builder from a real patch plan

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

## Variant E — Evidence-only commit

After a full toolbox run, commit only compact Git-trackable evidence when useful:

```powershell
git add `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_$Stamp.csv" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.md" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.json" `
  ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.md"

git diff --cached --name-only
```

Must not include:

```text
output/**
*.db
*.sqlite
renders/**
```

## CLI merge commands

Ready PR:

```powershell
gh pr ready <PR_NUMBER> --repo C-F-tek/blender-audio-project
```

Squash merge with head protection:

```powershell
gh pr merge <PR_NUMBER> `
  --repo C-F-tek/blender-audio-project `
  --squash `
  --match-head-commit <HEAD_SHA> `
  --subject "<subject>" `
  --body "<body>"
```

Refresh master after merge:

```powershell
git switch master
git pull --ff-only origin master
git log --oneline -5
git status --short
```

## Final decision rules

Proceed when:

```text
validation reports passed
fatal_report_failure_count=0 when warning policy is used
patch_plan_count >= 1 when implementation is expected
bundle dry-run passed before apply
apply is explicit
post-apply git diff --check passed
status contains only intended source/docs changes
```

Stop when:

```text
syntax validation fails
validation contract fails
bundle builder has operation_count=0 unexpectedly
bundle runner reports errors
SQLite/persistent memory write is true without explicit memory PR
provider execution happened in a no-provider path
output/** appears in staged files
```
