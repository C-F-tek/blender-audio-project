# Evidence Chunk 0004/0028

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-231855.md`
- source_sha256: `67abdf3a424f48df981c09aedf66a8fdd609b54cc1cbb41f7454d4a8b714e3f1`
- line_start: `663`
- line_end: `1013`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0003.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-231855_cloud_semantic_deterministic_chunks/full_toolbox_agent_review_decision_loop_20260503-231855_md_67abdf3a424f_chunk_0005.md`
- summary_source: `deterministic`

## Local chunk summary

Chunk deterministico. Sezioni: 2. Discover existing tools/helpers before proposing refactor; 2.1 Optional memory/tool reload after code or knowledge changes; 3. Build full Python line-count evidence; 4. Static validation and code interpreter report; 5. Contract/tool smoke before provider run. Preview: ## 2. Discover existing tools/helpers before proposing refactor Inspect existing reusable primitives before inventing new modules: ```powershell Get-Content .\Tools\ai\code_patch_plan_common.py -TotalCount 360 Get-Content .\Tools\ai\code_edit_proposal_helpers....

## Context before

Get-Content .\docs\LOCAL_VALIDATION_EVIDENCE\README.md -TotalCount 240
```

Purpose:

```text
avoid reinventing architecture
reuse existing project rules
respect evidence/bundle policy
stay aligned with current post-PR115 diagnostics
```


## Chunk content

````md
## 2. Discover existing tools/helpers before proposing refactor

Inspect existing reusable primitives before inventing new modules:

```powershell
Get-Content .\Tools\ai\code_patch_plan_common.py -TotalCount 360
Get-Content .\Tools\ai\code_edit_proposal_helpers.py -TotalCount 420
Get-Content .\Tools\ai\build_agent_review_code_patch_plan.py -TotalCount 420
Get-Content .\Tools\ai\build_code_edit_proposal_from_plan.py -TotalCount 420
Get-Content .\Tools\ai\build_code_interpreter_report.py -TotalCount 360
Get-Content .\Tools\ai\build_github_evidence_bundle.py -TotalCount 420
Get-Content .\Tools\validation\build_python_line_count_csv.py -TotalCount 320
Get-Content .\Tools\validation\run_agent_review_code_patch_plan_smoke.py -TotalCount 360
Get-Content .\Tools\validation\check_python_syntax.py -TotalCount 260
Get-Content .\Tools\validation\check_validation_report_contract.py -TotalCount 300
```

Search for already-factored utilities:

```powershell
Get-ChildItem .\Tools -Recurse -File -Filter *.py |
  Select-String -Pattern "def repo_rel|def resolve_path|def write_json|def render_markdown|report_only_guardrails|write_json_and_markdown|normalize_repo_path|load_line_counts" |
  Select-Object Path, LineNumber, Line |
  Format-Table -AutoSize
```

Helper decision taxonomy for every proposed refactor:

```text
reuse_existing_helper
promote_existing_function
extract_new_shared_helper
keep_local_by_design
```

Promotion candidates:

```text
path normalization
JSON read/write
Markdown report rendering
guardrail blocks
compact value/list helpers
validation command generation
line-count loading/parsing
report-only schema fields
forbidden target checks
```

Preferred promotion targets:

```text
Tools/ai/code_patch_plan_common.py
Tools/validation/report_utils.py
existing local helper modules in Tools/ai or Tools/validation
```

Do not create a new shared helper module if an existing one is a better fit.

## 2.1 Optional memory/tool reload after code or knowledge changes

Use this optional step only when the repository knowledge surface changed materially before a 0 -> 10 run.

Typical triggers:

```text
- new or modified AI tooling under Tools/ai, Tools/validation, Tools/workflow or Tools/npu
- new or modified docs/runbooks under docs/LOCAL_AI_TASKS or docs/LOCAL_VALIDATION_EVIDENCE
- merged PRs that change runtime toolbox, broker, orchestrator, memory routing or provider diagnostics
- stale evidence bundle after code/doc changes
- ChatGPT/local IA handoff says the memory/tool context may be outdated
```

Default behavior:

```text
optional
report-only
no provider execution
no patch application
no Blender runtime
no persistent memory write
no raw output/** commit
```

Recommended safe reload command:

```powershell
$MemoryReloadStamp = Get-Date -Format "yyyyMMdd-HHmmss"

.\Tools\workflow\run_full_memory_tool_regeneration.ps1 `
  -RepoRoot . `
  -Stamp $MemoryReloadStamp `
  -Profile full_refactor `
  -Objective "Reload IA-Carmine memory/tool context after code or knowledge changes before a 0 -> 10 run." `
  -WriteCompactBundle
```

Inspect the workflow report:

```powershell
Get-Content ".\output\validation\full_memory_tool_regeneration_${MemoryReloadStamp}_workflow.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, profile, provider_execution_performed, patch_application_performed, sqlite_write_performed, persistent_memory_write_performed, report_count, artifact_count, errors, bundle_json, bundle_markdown
```

Required guardrail result:

```text
passed=True
provider_execution_performed=False
patch_application_performed=False
sqlite_write_performed=False
persistent_memory_write_performed=False
```

Evidence policy:

```text
Commit compact evidence only if it is needed for the review:
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_python_line_count_<STAMP>.csv
```

Never commit:

```text
output/**
*.db
*.sqlite
renders/**
```

If this optional reload is run, add the generated compact bundle as a `--report-file` or committed evidence reference in the later GPU/NPU/refactor run so the local IA sees the refreshed state.

## 3. Build full Python line-count evidence

Run the deterministic line-count tool:

```powershell
python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --timestamped `
  --report-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
  --markdown-output ".\output\validation\python_line_count_refactor_large_code_$Stamp.md"
```

Inspect report summary:

```powershell
$LineCountReport = Get-Content ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" -Raw | ConvertFrom-Json
$LineCountCsv = $LineCountReport.csv_written

$LineCountReport |
  Select-Object passed, file_count, total_lines, csv_written, errors, warnings

"LINE_COUNT_CSV=$LineCountCsv"
```

Create a full untruncated Markdown inventory from the CSV:

```powershell
$LineCountAllMd = ".\output\validation\python_line_count_all_python_files_$Stamp.md"
$Rows = Import-Csv $LineCountCsv | Sort-Object {[int]$_.Lines} -Descending
$TotalLines = ($Rows | Measure-Object -Property Lines -Sum).Sum
$FileCount = ($Rows | Measure-Object).Count

$Lines = @()
$Lines += "# Full Python Line Count Inventory"
$Lines += ""
$Lines += "- Stamp: `$Stamp`"
$Lines += "- CSV: `$LineCountCsv`"
$Lines += "- File count: `$FileCount`"
$Lines += "- Total Python lines: `$TotalLines`"
$Lines += "- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20."
$Lines += ""
$Lines += "| Lines | File |"
$Lines += "|---:|---|"
foreach ($Row in $Rows) {
  $Lines += "| $($Row.Lines) | `$($Row.File)` |"
}
$Lines | Set-Content -Path $LineCountAllMd -Encoding UTF8

Get-Content $LineCountAllMd -Raw
```

Rule:

```text
The complete inventory is the input. Do not reduce the planner view to only top 10/top 20 files.
```

## 4. Static validation and code interpreter report

Run baseline syntax validation:

```powershell
python -m Tools.validation.check_python_syntax `
  --repo-root . `
  --output ".\output\validation\python_syntax_code_refactor_$Stamp.json"
```

Run static/code interpreter style report with current tool roots and template roots:

```powershell
python -m Tools.ai.build_code_interpreter_report `
  --repo-root . `
  --input Tools/ai `
  --input Tools/validation `
  --input Tools/npu `
  --input Tools/workflow `
  --input Scripting/v61b `
  --input Scripting/shared `
  --output ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" `
  --markdown-output ".\output\analysis\code_interpreter_code_refactor_$Stamp.md"
```

Inspect summary:

```powershell
Get-Content ".\output\validation\python_syntax_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, checked_count, failed_count, errors, warnings

Get-Content ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, errors, warnings
```

Stop if syntax validation fails unexpectedly.

## 5. Contract/tool smoke before provider run

Post-PR115 diagnostics depend on the GPU JSON contract helpers. Validate them before a long run:

```powershell
python -m py_compile `
  .\Tools\ai\gpu_planner_json_contract.py `
  .\Tools\ai\replay_gpu_planner_json_contract.py `
  .\Tools\ai\analyze_gpu_npu_run_sync.py `
  .\Tools\ai\build_gpu_repair_failure_recommendation.py `
  .\Tools\ai\run_agent_gpu_deep_planning_review.py `
  .\Tools\ai\run_agent_gpu_deep_planning_supervised.py `
  .\Tools\validation\run_gpu_planner_json_contract_smoke.py

python .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  --repo-root . `
  --output ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json" `
  --markdown-output ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.md"
```

Inspect:

```powershell
Get-Content ".\output\validation\gpu_planner_json_contract_smoke_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, case_count, failed_case_count, patch_application_performed, source_writes_performed
```

## 6. NPU/provider preflight

Run NPU provider environment check:

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.md"
```

Inspect:

```powershell
Get-Content ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, provider_execution_performed, patch_application_performed, errors, warnings
```

## 7. Run balanced GPU/NPU complete review

Use the balanced profile. Do not increase token budget before evaluating post-PR115 diagnostics.

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
  --report-file ".\output\analysis\code_interpreter_code_refactor_$Stamp.json" `
  --report-file ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
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
  --checkpoint-dir ".\output\ai_pipeline\cod
```

### `docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `15694`
- SHA-256: `084bfbae973243cd05aca6a0e5497d8ddf29e469d6156335f2ffbaca54ae8053`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Parallel Evidence Runbook

This task/runbook explains how a local AI agent should run the full GPU/NPU parallel diagnostic workflow, collect compact Git-trackable evidence, and interpret the initial `gpu_recommendation_count == 0` problem.

It is intended for non-interactive local AI runs and master-AI handoff review.

## Required reading order

A local AI agent must read these files first, before running commands or proposing edits:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md
```

If any instruction in this runbook conflicts with `AGENTS.md`, preserve `AGENTS.md` and stop with a conflict report.

````

## Context after

## Purpose

Use the local machine as a controlled multi-lane AI system:

```text
CPU orchestration
GPU/Ollama planner
NPU/OpenVINO checkpoint auditor
Git-trackable evidence bundle
master-AI review before any patch
```

