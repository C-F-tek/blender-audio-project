# Local Validation Evidence Bundle

- Generated at: `2026-05-03T16:54:31`
- Kind: `github_validation_evidence_bundle`

## Decision summary
- `ollama_gpu_primary_advisory`: `False`
- `npu_excluded_when_unusable`: `False`
- `provider_execution_seen`: `True`
- `npu_decode_smoke_passed`: `False`
- `selected_chunks_evidence_seen`: `True`
- `selected_chunks_built`: `True`
- `budget_respected`: `True`
- `artifact_manifest_built`: `True`
- `included_artifacts_built`: `True`
- `included_artifact_count`: `25`
- `patch_plan_summary_seen`: `True`

## Reports

### `output/ai_pipeline/md_py_consistency_20260503-163709_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_npu_parallel_orchestrator`
- Passed: `False`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/md_py_consistency_20260503-163709_parallel_gpu.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_gpu_deep_planning_supervised`
- Passed: `False`
- Provider execution performed: `True`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `0`
- Recommended next layer: `build_agent_review_patch_plan.py`
- Errors: `["round 1: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 2: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 3: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 4: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 5: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 6: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 7: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 8: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 9: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 10: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 11: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 12: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 13: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 14: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 15: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 16: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 17: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 18: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 19: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value", "round 20: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value"]`

### `output/analysis/code_interpreter_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `code_interpreter_report`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `146`

### `output/validation/markdown_inventory_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `markdown_inventory`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`

### `output/validation/python_line_count_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_line_count_csv`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/python_syntax_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `python_syntax`
- Passed: `True`

### `output/validation/gpu_planner_json_contract_smoke_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/deterministic_recommendation_synthesizer_smoke_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `1`

### `output/validation/agent_review_decision_loop_smoke_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `1`
- Recommendation count: `1`

### `output/validation/agent_review_patch_bundle_builder_smoke_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_bundle_builder_smoke`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/npu_provider_environment_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `npu_provider_environment`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_json_contract_replay_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_planner_json_contract_replay`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/analysis/gpu_npu_run_sync_md_py_consistency_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `gpu_npu_run_sync_analysis`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_synthesizer`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Recommendation count: `12`

### `output/ai_pipeline/md_py_consistency_20260503-163709_bridge_orchestrator.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/ai_pipeline/md_py_consistency_20260503-163709_agent_review_decision_loop.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_decision_loop`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`
- Recommendation count: `12`

### `output/patch_specs/md_py_consistency_20260503-163709_agent_review_patch_plan.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_plan`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`
- Patch plan count: `12`
- Patch plan summary count: `12`
- Fallback used: `False`
- Manual review required: `True`

### `output/validation/md_py_consistency_patch_bundle_builder_20260503-163709.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `agent_review_patch_bundle_builder`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

### `output/validation/full_memory_tool_regeneration_20260503-163709_workflow.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `full_memory_tool_regeneration_workflow`
- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Patch plan summary

### `output/patch_specs/md_py_consistency_20260503-163709_agent_review_patch_plan.json`

- Patch plan count: `12`
- Fallback used: `False`
- Manual review required: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

#### det_doc_code_001 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/config_model.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

#### det_doc_code_002 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/diagnostics.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

#### det_doc_code_003 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.

#### det_doc_code_004 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_ONBOARDING.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.

#### det_doc_code_005 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_SOURCE_MAP.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.

#### det_doc_code_006 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/AI_REFERENCE_SOURCE_MAP.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.

#### det_doc_code_007 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code-quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

#### det_doc_code_008 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code_quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

#### det_doc_code_009 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/CODE_CONSULTATION_REPORT.md']
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/ci.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

#### det_doc_doc_001 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

#### det_doc_doc_002 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['docs/JSON_SCHEMAS.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

#### det_doc_doc_003 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Status: `ready_for_manual_review`
- Target files: ['Tools/validation/README.md']
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.


## Artifact manifest

- `output/ai_pipeline/md_py_consistency_20260503-163709_orchestrator.json` exists=`True` size=`39238` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/md_py_consistency_20260503-163709_parallel_gpu.json` exists=`True` size=`137790` suffix=`.json` preview_chars=`1500`
- `output/analysis/code_interpreter_md_py_consistency_20260503-163709.json` exists=`True` size=`1375681` suffix=`.json` preview_chars=`1500`
- `output/validation/markdown_inventory_md_py_consistency_20260503-163709.json` exists=`True` size=`348545` suffix=`.json` preview_chars=`1500`
- `output/validation/python_line_count_md_py_consistency_20260503-163709.json` exists=`True` size=`3141` suffix=`.json` preview_chars=`1500`
- `output/validation/python_syntax_md_py_consistency_20260503-163709.json` exists=`True` size=`36667` suffix=`.json` preview_chars=`1500`
- `output/validation/gpu_planner_json_contract_smoke_md_py_consistency_20260503-163709.json` exists=`True` size=`7152` suffix=`.json` preview_chars=`1500`
- `output/validation/deterministic_recommendation_synthesizer_smoke_md_py_consistency_20260503-163709.json` exists=`True` size=`5177` suffix=`.json` preview_chars=`1500`
- `output/validation/agent_review_decision_loop_smoke_md_py_consistency_20260503-163709.json` exists=`True` size=`1447` suffix=`.json` preview_chars=`1420`
- `output/validation/agent_review_patch_bundle_builder_smoke_md_py_consistency_20260503-163709.json` exists=`True` size=`1728` suffix=`.json` preview_chars=`1500`
- `output/validation/npu_provider_environment_md_py_consistency_20260503-163709.json` exists=`True` size=`1745` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_json_contract_replay_md_py_consistency_20260503-163709.json` exists=`True` size=`31251` suffix=`.json` preview_chars=`1500`
- `output/analysis/gpu_npu_run_sync_md_py_consistency_20260503-163709.json` exists=`True` size=`2538` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.json` exists=`True` size=`119254` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/md_py_consistency_20260503-163709_bridge_orchestrator.json` exists=`True` size=`29876` suffix=`.json` preview_chars=`1500`
- `output/ai_pipeline/md_py_consistency_20260503-163709_agent_review_decision_loop.json` exists=`True` size=`2632` suffix=`.json` preview_chars=`1500`
- `output/patch_specs/md_py_consistency_20260503-163709_agent_review_patch_plan.json` exists=`True` size=`194381` suffix=`.json` preview_chars=`1500`
- `output/validation/md_py_consistency_patch_bundle_builder_20260503-163709.json` exists=`True` size=`9019` suffix=`.json` preview_chars=`1500`
- `output/validation/full_memory_tool_regeneration_20260503-163709_workflow.json` exists=`True` size=`4937` suffix=`.json` preview_chars=`1500`

## Included artifact contents

### `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `28880`
- SHA-256: `297a0ceb34ac4116980c3023a6eb7ae5bbafe5b3475bea590cd439c4268b36b0`
- Content included: `True`
- Content truncated: `True`

```text
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
  --min-recommendations 1 `
  --min-patch-plans 1
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
  ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.md"
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
  --artifact ".\docs\LOCAL_AI_TAS
```

### `output/validation/markdown_inventory_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `118901`
- SHA-256: `f032a332195144c7c43735c24b0235c97f97b48602cb3c5450f6fa383ff82bcc`
- Content included: `True`
- Content truncated: `True`

```text
# Full Markdown Inventory

- Stamp: 20260503-163709
- File count: 1228
- Python/tool related count: 1123
- Visibility rule: all counted Markdown files are listed below; do not truncate.

| Lines | Python/tool related | File |
|---:|---|---|
| 7375 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_20260503-151613.md` |
| 7173 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_20260503-160523.md` |
| 4723 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\complex_local_ai_tool_usage_bundle_complex_ai_tool_usage_20260503-092256.md` |
| 4610 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_20260503-151613.md` |
| 4527 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_agent_review_decision_loop_20260503-160523.md` |
| 3783 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_refactor_duplication_audit_bundle_20260503-082504.md` |
| 2579 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\code_refactor_ai_to_ai_bundle_20260502-215518.md` |
| 2446 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\pr109_static_code_plan_bundle_20260502-143630.md` |
| 2339 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_balanced_ai_to_ai_bundle_20260502-210841.md` |
| 2152 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\complex_local_ai_provider_toolbox_bundle_complex_ai_provider_toolbox_20260503-100241.md` |
| 1839 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\complex_local_ai_provider_backed_bundle_complex_ai_provider_backed_20260503-092828.md` |
| 1803 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_20260503-163709.md` |
| 1800 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_20260503-160523.md` |
| 1796 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_20260503-151613.md` |
| 1771 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_20260503-011858.md` |
| 1762 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_20260502-225859.md` |
| 1659 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\pr109_code_interpreter_and_agnostic_bundle_20260502-141921.md` |
| 1620 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\pr109_static_code_plan_bundle_20260502-142630.md` |
| 1399 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_20260503-014138.md` |
| 1380 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\project_complete_ai_to_ai_bundle_20260502-195523.md` |
| 1273 | True | `.\docs\LOCAL_VALIDATION_EVIDENCE\heavy_prototype_review_bundle_20260502-193942.md` |
| 847 | True | `.\indexAI\project_code_index.md` |
| 783 | True | `.aider.chat.history.md` |
| 759 | True | `.\Tools\npu\npu_music_chunks\chunk_001_music_overview.md` |
| 737 | True | `.\docs\LOCAL_AI_TASKS\code-refactor-0-to-10-procedure.md` |
| 705 | True | `.\docs\LOCAL_AI_TASKS\full-toolbox-0-to-10-semi-automatic-procedure.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_223_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_219_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_325_blender_manual_html_grid_dilate_erode.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_227_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_235_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_231_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_321_blender_manual_html_field_to_grid.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_215_blender_manual_html_mesh_to_volume.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_199_blender_manual_html_points_to_volume.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_195_blender_manual_html_distribute_points_in_volume.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_191_blender_manual_html_keying_sets.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_203_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_211_blender_manual_html_material.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_207_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_329_blender_manual_html_grid_mean.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_301_blender_manual_html_sss.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_297_blender_manual_html_specular_bsdf.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_247_blender_manual_html_diffuse.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_309_blender_manual_html_translucent.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_255_blender_manual_html_glass.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_259_blender_manual_html_glossy.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_267_blender_manual_html_hair_principled.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_276_blender_manual_html_metallic.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_289_blender_manual_html_refraction.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_317_blender_manual_html_clip_grid.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_239_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_293_blender_manual_html_sheen.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_313_blender_manual_html_transparent.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_280_blender_manual_html_principled.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_285_blender_manual_html_ray_portal.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_082_blender_manual_html_force_field.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_086_blender_manual_html_volume_displace.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_077_blender_manual_html_workflow_examples.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_065_blender_manual_html_introduction.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_069_blender_manual_html_troubleshooting.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_090_blender_manual_html_mesh_to_volume.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_106_blender_manual_html_maintain_volume.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_110_blender_manual_html_modifiers.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_102_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_094_blender_manual_html_volume_to_mesh.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_098_blender_manual_html_editing.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_049_blender_manual_html_geometry_nodes.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_015_blender_manual_html_volume_scatter.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_019_blender_manual_html_particle_info.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_011_blender_manual_html_volume_principled.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_003_blender_manual_html_volume_absorption.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_007_blender_manual_html_volume_coefficients.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_023_blender_manual_html_volume_info.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_041_blender_manual_html_particle_system.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_045_blender_manual_html_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_036_blender_manual_html_particle_instance.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_027_blender_manual_html_material.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_031_blender_manual_html_drivers_panel.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_115_blender_manual_html_material_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_139_blender_manual_html_volume_cube.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_174_blender_manual_html_add.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_135_blender_manual_html_volume_to_mesh.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_156_blender_manual_html_volume.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_170_blender_manual_html_shader_to_rgb.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_143_blender_manual_html_material_settings.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_131_blender_manual_html_set_material_index.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_182_blender_manual_html_mix.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_119_blender_manual_html_material_selection.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_186_blender_manual_html_introduction.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_127_blender_manual_html_set_material.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_123_blender_manual_html_replace_material.md` |
| 696 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_178_blender_manual_html_index.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_053_blender_manual_html_material.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_272_blender_manual_html_holdout.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_057_blender_manual_html_material.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_165_blender_manual_html_volume.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_161_blender_manual_html_volumes.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_152_blender_manual_html_volumes.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_061_blender_manual_html_material.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_073_blender_manual_html_usage.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_251_blender_manual_html_emission.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_305_blender_manual_html_toon.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_263_blender_manual_html_hair.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_243_blender_manual_html_background.md` |
| 695 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_147_blender_manual_html_material_settings.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_163_blender_manual_html_volume.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_270_blender_manual_html_holdout.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_241_blender_manual_html_background.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_249_blender_manual_html_emission.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_071_blender_manual_html_usage.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_145_blender_manual_html_material_settings.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_055_blender_manual_html_material.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_059_blender_manual_html_material.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_051_blender_manual_html_material.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_159_blender_manual_html_volumes.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_261_blender_manual_html_hair.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_150_blender_manual_html_volumes.md` |
| 685 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_303_blender_manual_html_toon.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_029_blender_manual_html_drivers_panel.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_168_blender_manual_html_shader_to_rgb.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_245_blender_manual_html_diffuse.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_034_blender_manual_html_particle_instance.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_315_blender_manual_html_clip_grid.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_176_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_025_blender_manual_html_material.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_237_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_172_blender_manual_html_add.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_319_blender_manual_html_field_to_grid.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_141_blender_manual_html_material_settings.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_047_blender_manual_html_geometry_nodes.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_307_blender_manual_html_translucent.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_257_blender_manual_html_glossy.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_137_blender_manual_html_volume_cube.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_311_blender_manual_html_transparent.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_039_blender_manual_html_particle_system.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_154_blender_manual_html_volume.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_043_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_253_blender_manual_html_glass.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_217_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_013_blender_manual_html_volume_scatter.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_197_blender_manual_html_points_to_volume.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_323_blender_manual_html_grid_dilate_erode.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_221_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_327_blender_manual_html_grid_mean.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_209_blender_manual_html_material.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_205_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_009_blender_manual_html_volume_principled.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_213_blender_manual_html_mesh_to_volume.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_193_blender_manual_html_distribute_points_in_volume.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_184_blender_manual_html_introduction.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_021_blender_manual_html_volume_info.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_001_blender_manual_html_volume_absorption.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_180_blender_manual_html_mix.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_233_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_017_blender_manual_html_particle_info.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_225_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_189_blender_manual_html_keying_sets.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_229_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_005_blender_manual_html_volume_coefficients.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_133_blender_manual_html_volume_to_mesh.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_108_blender_manual_html_modifiers.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_201_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_080_blender_manual_html_force_field.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_295_blender_manual_html_specular_bsdf.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_075_blender_manual_html_workflow_examples.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_274_blender_manual_html_metallic.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_121_blender_manual_html_replace_material.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_299_blender_manual_html_sss.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_117_blender_manual_html_material_selection.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_278_blender_manual_html_principled.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_088_blender_manual_html_mesh_to_volume.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_291_blender_manual_html_sheen.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_092_blender_manual_html_volume_to_mesh.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_287_blender_manual_html_refraction.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_084_blender_manual_html_volume_displace.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_283_blender_manual_html_ray_portal.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_104_blender_manual_html_maintain_volume.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_096_blender_manual_html_editing.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_100_blender_manual_html_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_125_blender_manual_html_set_material.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_063_blender_manual_html_introduction.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_113_blender_manual_html_material_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_265_blender_manual_html_hair_principled.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_129_blender_manual_html_set_material_index.md` |
| 684 | True | `.\Tools\npu\npu_blender_manual_chunks\chunk_067_blender_manual_html_troubleshooting.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_130_blender_manual_html_set_material_index.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_052_blender_manual_html_material.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_194_blender_manual_html_distribute_points_in_volume.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_056_blender_manual_html_material.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_097_blender_manual_html_editing.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_081_blender_manual_html_force_field.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_134_blender_manual_html_volume_to_mesh.md` |
| 605 | False | `.\Tools\npu\npu_blender_manual_chunks\chunk_101_blender_manual_html_index.md` |
| 605 | 
```

### `output/validation/python_line_count_all_python_files_20260503-163709.md`

- Role: `explicit_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `17860`
- SHA-256: `0eb9db41967f1a995f0afc726b62efd8042c7c277648821cf7dc8dfce7a3613b`
- Content included: `True`
- Content truncated: `False`

```text
# Full Python Line Count Inventory

- Stamp: 20260503-163709
- CSV: docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-163724.csv
- File count: 312
- Total Python lines: 90309
- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20.

| Lines | File |
|---:|---|
| 2197 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` |
| 1773 | `Tools/npu/run_dual_ai_pipeline.py` |
| 1513 | `old script legacy/spaziotempo_asset_visual_v61.py` |
| 1262 | `Scripting/v61b/scene_tuning_panel.py` |
| 1230 | `Tools/workflow/workflow_state.py` |
| 1179 | `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` |
| 1174 | `old script legacy/spaziotempo_asset_visual_v6.py` |
| 1115 | `Tools/ai/run_agent_gpu_deep_planning_supervised.py` |
| 1097 | `Scripting/v61b_backgood/scene_tuning_panel.py` |
| 1079 | `Scripting/v61b/animation.py` |
| 1019 | `Scripting/v61b_backgood/animation.py` |
| 969 | `old script legacy/spaziotempo_album_visual_v5.py` |
| 902 | `Tools/ai/run_agent_gpu_deep_planning_review.py` |
| 738 | `Tools/workflow/gui/workflow_gui.py` |
| 737 | `Scripting/v61b/physics_setup.py` |
| 725 | `Tools/ai/build_refactor_duplication_audit.py` |
| 725 | `Scripting/v61b_backgood/asset_setup.py` |
| 725 | `Scripting/v61b/asset_setup.py` |
| 720 | `Scripting/v61b_backgood/physics_setup.py` |
| 715 | `Tools/ai/agent_runtime_tool_broker.py` |
| 711 | `Tools/npu/build_music_context.py` |
| 710 | `old script legacy/spaziotempo_album_visual_v3.py` |
| 694 | `Tools/ai/run_npu_gpu_deep_review_auditor.py` |
| 685 | `Tools/ai/build_deterministic_recommendations.py` |
| 657 | `Scripting/v61b/materials.py` |
| 631 | `Tools/npu/run_npu_review.py` |
| 627 | `Tools/validation/check_npu_pipeline_modules.py` |
| 618 | `Tools/ai/build_selective_execution_plan.py` |
| 608 | `Tools/ai/build_agent_review_patch_bundle.py` |
| 607 | `Tools/workflow/workflow_debug.py` |
| 604 | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` |
| 582 | `Tools/ai/build_repository_change_proposals.py` |
| 579 | `Tools/ai/build_ai_context_pack.py` |
| 573 | `Tools/ai/run_pipeline_dry_run_matrix.py` |
| 570 | `Tools/ai/build_agent_review_patch_plan.py` |
| 554 | `Scripting/v61b/atmosphere_setup.py` |
| 551 | `Tools/ai/suggest_repository_updates.py` |
| 544 | `Tools/ai/agent_state.py` |
| 543 | `Scripting/v61b_backgood/atmosphere_setup.py` |
| 527 | `Tools/ai/agent_runtime_sqlite_memory.py` |
| 519 | `Tools/ai/run_megalithic_repo_review.py` |
| 513 | `Scripting/v61b_backgood/materials.py` |
| 499 | `Tools/ai/build_agent_review_code_patch_plan.py` |
| 497 | `Tools/validation/ai_pipeline_report_contracts.py` |
| 490 | `Tools/npu/npu_guardrail_service.py` |
| 489 | `Tools/ai/refine_megalithic_review_signals.py` |
| 487 | `Tools/validation/run_agent_review_patch_plan_full_validation.py` |
| 483 | `Tools/validation/run_agnostic_ai_tools_smoke_matrix.py` |
| 471 | `Tools/ai/agent_memory_routing_policy.py` |
| 469 | `normalize_scene_spec.py` |
| 446 | `Tools/validation/check_reviewed_patch_specs.py` |
| 443 | `Tools/repo_patch_runner/apply_repo_mods.py` |
| 442 | `Tools/ai/promote_patch_spec_draft.py` |
| 439 | `Scripting/v61b/config.py` |
| 438 | `Tools/npu/ollama_runtime.py` |
| 437 | `Tools/ai/build_code_interpreter_report.py` |
| 436 | `Tools/npu/build_project_ai_index.py` |
| 425 | `Tools/validation/check_ai_context_pack_contract.py` |
| 422 | `Tools/workflow/gui/components/storage_dashboard.py` |
| 419 | `Tools/workflow/scene_brief.py` |
| 414 | `Tools/ai/build_patch_specs_from_proposals.py` |
| 411 | `Tools/ai/schema_repair_context.py` |
| 408 | `Tools/ai/build_agent_agnostic_tool_inventory.py` |
| 408 | `Tools/ai/agent_review_warning_policy.py` |
| 407 | `Tools/ai/build_agent_review_evidence_sufficiency.py` |
| 402 | `Tools/npu/build_npu_code_context.py` |
| 401 | `Tools/validation/check_github_evidence_bundle.py` |
| 400 | `Tools/validation/check_patch_spec_drafts.py` |
| 399 | `Scripting/v61b/encode_ffmpeg_v61b.py` |
| 398 | `Tools/ai/build_dry_run_matrix_evidence_bundle.py` |
| 397 | `Tools/ai/build_agent_memory_inventory.py` |
| 395 | `Scripting/v61b_backgood/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/hotpatch/hero_material_patch.py` |
| 395 | `Scripting/v61b/encode_image_sequence_v61b.py` |
| 392 | `Tools/validation/check_code_contract_drift.py` |
| 392 | `Tools/ai/build_full_context_golden_proposals.py` |
| 392 | `Scripting/v61b/fog_dynamics.py` |
| 390 | `Tools/workflow/gui/components/artifact_browser.py` |
| 380 | `Tools/ai/gpu_planner_json_contract.py` |
| 376 | `Scripting/v61b_backgood/encode_image_sequence_v61b.py` |
| 369 | `Tools/npu/generated_blender_script_candidate_FristNear.py` |
| 369 | `Tools/npu/generated_blender_script_candidate.py` |
| 369 | `indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py` |
| 366 | `Tools/validation/check_repository_change_proposals.py` |
| 359 | `Tools/validation/test_npu_pipeline_helpers.py` |
| 358 | `Scripting/v61b_backgood/config.py` |
| 357 | `Tools/ai/build_local_ai_enrichment_plan.py` |
| 355 | `Tools/npu/build_ai_service_packet.py` |
| 353 | `Tools/workflow/project_awareness.py` |
| 341 | `Tools/validation/check_ai_dry_run_matrix_contract.py` |
| 339 | `Tools/validation/check_selected_semantic_chunks.py` |
| 335 | `Tools/ai/check_local_resource_lanes.py` |
| 331 | `Tools/validation/apply_docs_contract_drift_fixes.py` |
| 327 | `Tools/npu/build_npu_knowledge_broker_packet.py` |
| 326 | `Tools/npu/build_blender_manual_context.py` |
| 325 | `Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py` |
| 324 | `Tools/workflow/workflow_shell.py` |
| 321 | `Tools/validation/check_dry_run_matrix_evidence_bundle.py` |
| 319 | `Tools/workflow/gui/workflow_gui_modern.py` |
| 319 | `Tools/ai/build_music_intermediates.py` |
| 317 | `Tools/validation/check_local_ai_adapter_manifest.py` |
| 315 | `Tools/ai/github_evidence_bundle_artifacts.py` |
| 314 | `Tools/ai/run_npu_decode_smoke_diagnostic.py` |
| 307 | `Tools/validation/run_agent_review_decision_loop_smoke.py` |
| 307 | `Tools/validation/check_full_context_golden_proposals.py` |
| 307 | `Tools/ai/agent_memory_policy.py` |
| 305 | `Tools/ai/run_agent_review_decision_loop.py` |
| 304 | `Tools/ai/build_analysis_input_bundle.py` |
| 301 | `Scripting/v61b/hotpatch/accent_patch.py` |
| 297 | `Tools/npu/pipeline/providers.py` |
| 291 | `Tools/ai/select_semantic_code_chunks.py` |
| 291 | `Tools/ai/build_agent_transient_request_context.py` |
| 290 | `Tools/validation/run_gpu_planner_json_contract_smoke.py` |
| 290 | `Tools/validation/check_ai_pipeline_modules.py` |
| 286 | `Tools/ai/build_gpu_repair_failure_recommendation.py` |
| 286 | `Scripting/v61b/hotpatch/diagnostics.py` |
| 284 | `Tools/workflow/startup_check.py` |
| 283 | `Tools/validation/run_agent_review_patch_plan_smoke.py` |
| 278 | `Tools/workflow/gui/components/session_overview.py` |
| 276 | `Tools/ai/analyze_gpu_npu_run_sync.py` |
| 270 | `Tools/validation/check_full_context_golden_docs_contract.py` |
| 270 | `Scripting/v61b/render_setup.py` |
| 267 | `Tools/workflow/ai_runtime_diagnostics.py` |
| 267 | `Scripting/v61b_backgood/render_setup.py` |
| 266 | `Tools/ai/build_code_patch_docs_followup.py` |
| 260 | `Tools/validation/check_ai_workload_report_quality.py` |
| 259 | `Tools/validation/check_docs_contract_drift.py` |
| 259 | `Tools/ai/build_megalithic_review_pr_draft.py` |
| 258 | `Tools/validation/run_refactor_duplication_audit_smoke.py` |
| 258 | `Tools/ai/build_code_patch_artifact_pack.py` |
| 257 | `analyze_wav.py` |
| 256 | `Tools/validation/run_agnostic_context_stack_smoke.py` |
| 250 | `Tools/ai/build_code_edit_proposal_from_plan.py` |
| 247 | `Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py` |
| 244 | `Tools/validation/run_agent_runtime_tool_broker_smoke.py` |
| 244 | `Tools/validation/run_agent_review_patch_bundle_builder_smoke.py` |
| 240 | `Tools/ai/review_wave_entrypoints.py` |
| 240 | `Scripting/v61b_backgood/fog_dynamics.py` |
| 238 | `Tools/validation/check_selective_execution_plan.py` |
| 238 | `Tools/npu/run_ollama_music_agent.py` |
| 237 | `Tools/validation/run_agent_review_warning_policy_smoke.py` |
| 234 | `Tools/validation/run_agent_memory_routing_policy_smoke.py` |
| 232 | `Tools/ai/smart_ai_gatekeeper.py` |
| 232 | `Tools/ai/replay_gpu_planner_json_contract.py` |
| 231 | `Tools/ai/enrich_github_evidence_bundle_code_plan.py` |
| 230 | `Tools/validation/check_ai_dry_run_matrix_outputs.py` |
| 229 | `Tools/validation/check_npu_knowledge_broker_packet.py` |
| 228 | `Tools/ai/build_github_evidence_bundle.py` |
| 222 | `Tools/validation/check_generated_artifact_path_policy.py` |
| 222 | `Tools/ai/workload_quality.py` |
| 221 | `Scripting/v61b/spaziotempo/core/registry.py` |
| 219 | `Tools/workflow/smart_ai_context.py` |
| 217 | `Tools/validation/generated_file_policy.py` |
| 217 | `Tools/ai/artifact_domain_registry.py` |
| 212 | `Tools/validation/build_python_line_count_csv.py` |
| 211 | `Tools/ai/github_evidence_bundle_reports.py` |
| 209 | `Tools/validation/check_local_ai_enrichment_plan.py` |
| 209 | `Tools/ai/github_evidence_bundle_markdown.py` |
| 208 | `Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py` |
| 207 | `Tools/validation/check_core_activation_agnostic_contract.py` |
| 206 | `Scripting/v61b_backgood/hotpatch/render_patch.py` |
| 206 | `Scripting/v61b/hotpatch/render_patch.py` |
| 205 | `Tools/ai/code_patch_plan_common.py` |
| 204 | `Tools/validation/run_agent_review_evidence_sufficiency_smoke.py` |
| 203 | `Tools/validation/run_code_edit_proposal_smoke.py` |
| 203 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py` |
| 201 | `Tools/validation/run_agent_review_code_patch_plan_smoke.py` |
| 201 | `Tools/validation/check_validation_report_contract.py` |
| 201 | `Tools/ai/code_edit_proposal_helpers.py` |
| 200 | `Tools/ai/validate_ai_artifacts.py` |
| 200 | `Scripting/v61b/main_v61b.py` |
| 198 | `Scripting/v61b/world_setup.py` |
| 197 | `Tools/validation/generated_python_policy.py` |
| 197 | `Tools/ai/pipeline/steps.py` |
| 190 | `Tools/validation/run_runtime_tool_guidance_fallback_smoke.py` |
| 190 | `Tools/validation/report_utils.py` |
| 189 | `Tools/ai/check_npu_provider_environment.py` |
| 186 | `Tools/workflow/git_auto_push.py` |
| 186 | `Tools/validation/run_npu_runtime_tool_context_smoke.py` |
| 186 | `Tools/ai/build_workload_quality_lane_routing.py` |
| 185 | `Tools/ai/pipeline/remediation.py` |
| 183 | `Tools/workflow/gui/components/action_panel.py` |
| 183 | `Tools/validation/run_schema_repair_retry_smoke.py` |
| 183 | `Tools/validation/check_ai_dry_run_matrix_cases.py` |
| 182 | `Tools/workflow/gui/components/live_output_panel.py` |
| 182 | `Tools/ai/run_local_provider_probe.py` |
| 181 | `Tools/workflow/gui/workflow_gui_with_push.py` |
| 181 | `Scripting/v61b_backgood/main_v61b.py` |
| 174 | `Scripting/v61b_backgood/world_setup.py` |
| 173 | `Tools/validation/check_generated_blender_script_policy.py` |
| 173 | `Tools/ai/runtime_tool_guidance.py` |
| 172 | `Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py` |
| 168 | `Tools/validation/run_schema_repair_context_smoke.py` |
| 167 | `Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py` |
| 161 | `Tools/validation/run_npu_runtime_tool_execution_smoke.py` |
| 161 | `Scripting/shared/image_sequence.py` |
| 160 | `Tools/npu/npu_runtime.py` |
| 159 | `Tools/validation/check_npu_decode_quality_remediation.py` |
| 159 | `Tools/validation/run_provider_empty_response_diagnostics_smoke.py` |
| 159 | `Scripting/v61b/fog_filaments.py` |
| 159 | `Tools/ai/github_evidence_bundle_io.py` |
| 157 | `Tools/npu/pipeline/__init__.py` |
| 156 | `Tools/validation/run_schema_repair_retry_bootstrap_smoke.py` |
| 154 | `Tools/validation/run_runtime_tool_feedback_loop_smoke.py` |
| 152 | `Tools/ai/pipeline/models.py` |
| 150 | `Scripting/v61b/hotpatch/lighting_patch.py` |
| 149 | `Tools/validation/check_refactor_status_consistency.py` |
| 148 | `Tools/npu/build_runtime_output_manifest.py` |
| 147 | `Tools/validation/check_blender_shared_compat_smoke.py` |
| 147 | `Tools/npu/build_provider_result_report.py` |
| 146 | `Tools/ai/github_evidence_bundle_decisions.py` |
| 144 | `Tools/workflow/artifact_consult.py` |
| 143 | `Tools/validation/run_npu_runtime_tool_fallback_smoke.py` |
| 142 | `Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py` |
| 141 | `Tools/validation/check_docs_links.py` |
| 140 | `Scripting/shared/blender_compat.py` |
| 134 | `Scripting/shared/ffmpeg_encoder.py` |
| 133 | `Scripting/v61b/hotpatch/fog_patch.py` |
| 133 | `Scripting/shared/render_profiles.py` |
| 132 | `Tools/validation/check_json_artifacts.py` |
| 132 | `Scripting/v61b/spaziotempo/core/collections.py` |
| 130 | `Tools/ai/model_json.py` |
| 128 | `Tools/ai/build_agent_state_packet.py` |
| 127 | `Tools/npu/run_npu_artifact_reviewer.py` |
| 127 | `Tools/npu/pipeline/artifact_paths.py` |
| 125 | `Tools/validation/check_agent_memory_policy.py` |
| 125 | `Tools/validation/check_generated_python_policy.py` |
| 125 | `Scripting/v61b_backgood/hotpatch/accent_patch.py` |
| 125 | `Tools/npu/pipeline/reports.py` |
| 124 | `Scripting/v61b_backgood/hotpatch/fog_patch.py` |
| 123 | `Tools/validation/check_execution_plan_status.py` |
| 119 | `Tools/validation/check_package_structure.py` |
| 119 | `Tools/validation/check_ai_model_json.py` |
| 118 | `Tools/ai/pipeline/schema_report.py` |
| 117 | `Tools/workflow/workflow_shell_with_push.py` |
| 116 | `Tools/validation/run_runtime_sqlite_persistent_write_smoke.py` |
| 113 | `build_track_summary.py` |
| 111 | `Tools/npu/ai_memory_context.py` |
| 110 | `Tools/workflow/asset_inventory.py` |
| 107 | `Tools/npu/pipeline/config.py` |
| 107 | `Tools/ai/pipeline/markdown_report.py` |
| 105 | `Tools/validation/check_python_syntax.py` |
| 104 | `Tools/ai/pipeline/preflight.py` |
| 103 | `Scripting/v61b/hotpatch/runner.py` |
| 102 | `Tools/ai/pipeline/runner.py` |
| 102 | `Scripting/shared/path_utils.py` |
| 99 | `Tools/npu/pipeline/prompts.py` |
| 97 | `Tools/ai/pipeline/guardrail_models.py` |
| 97 | `Scripting/v61b_backgood/scene_utils.py` |
| 97 | `Scripting/v61b/scene_utils.py` |
| 96 | `Tools/validation/check_npu_pipeline_docs.py` |
| 92 | `Tools/workflow/gui/components/st_theme.py` |
| 91 | `Tools/npu/build_semantic_code_chunks.py` |
| 91 | `Scripting/v61b_backgood/hotpatch/common.py` |
| 91 | `Scripting/v61b/hotpatch/common.py` |
| 90 | `Tools/validation/run_npu_tool_request_contract_smoke.py` |
| 88 | `Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py` |
| 88 | `Scripting/shared/json_io.py` |
| 86 | `Tools/ai/pipeline/artifact_contracts.py` |
| 85 | `Scripting/v61b_backgood/hotpatch/lighting_patch.py` |
| 84 | `Tools/npu/pipeline/validators.py` |
| 83 | `Tools/validation/check_provider_result_parsing.py` |
| 81 | `Scripting/v61b_backgood/io_utils.py` |
| 81 | `Scripting/v61b/io_utils.py` |
| 80 | `Tools/npu/pipeline/fixtures.py` |
| 79 | `Scripting/_template_audio_reactive_package/main.py` |
| 75 | `Tools/npu/pipeline/context_builder.py` |
| 75 | `Scripting/_template_audio_reactive_package/encode_ffmpeg.py` |
| 74 | `Tools/ai/pipeline/reports.py` |
| 73 | `Tools/ai/pipeline/compat.py` |
| 71 | `Tools/validation/build_full_python_line_count_markdown.py` |
| 70 | `Tools/npu/pipeline/runner.py` |
| 70 | `Tools/ai/pipeline/refactor_status.py` |
| 69 | `Tools/ai/review_agent_memory.py` |
| 68 | `Tools/npu/pipeline/migration_readiness.py` |
| 66 | `Tools/ai/pipeline/scheduler.py` |
| 65 | `Tools/validation/check_ai_pipeline_report_contract.py` |
| 65 | `Tools/ai/run_parallel_artifact_pipeline.py` |
| 64 | `Tools/validation/check_artifact_domain_registry.py` |
| 63 | `Scripting/v61b/hot_update_scene_v61b.py` |
| 61 | `Tools/npu/pipeline/io_utils.py` |
| 61 | `Scripting/v61b_backgood/hot_update_scene_v61b.py` |
| 60 | `Scripting/v61b_backgood/hotpatch/runner.py` |
| 59 | `Tools/validation/check_npu_pipeline_helper_tests.py` |
| 56 | `Tools/npu/pipeline/artifact_writer.py` |
| 53 | `Tools/ai/merge_ai_candidates.py` |
| 52 | `Tools/npu/pipeline/legacy_compat.py` |
| 51 | `Scripting/v61b/reload_utils.py` |
| 51 | `Scripting/_template_audio_reactive_package/audio_mapping.py` |
| 50 | `Tools/ai/pipeline/cli.py` |
| 49 | `Scripting/_template_audio_reactive_package/config.py` |
| 35 | `Scripting/_template_audio_reactive_package/materials.py` |
| 31 | `Tools/ai/pipeline/orchestrator.py` |
| 29 | `Scripting/v61b_backgood/camera_setup.py` |
| 29 | `Scripting/v61b/camera_setup.py` |
| 26 | `Scripting/_template_audio_reactive_package/render_settings.py` |
| 26 | `Scripting/_template_audio_reactive_package/camera.py` |
| 23 | `Tools/ai/pipeline/__init__.py` |
| 23 | `Scripting/_template_audio_reactive_package/lighting.py` |
| 21 | `Scripting/_template_audio_reactive_package/scene_objects.py` |
| 20 | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/render_profiles_reference.py` |
| 19 | `Scripting/v61b/spaziotempo/features/catalog.py` |
| 15 | `Tools/ai/pipeline/defaults.py` |
| 13 | `Scripting/shared/__init__.py` |
| 4 | `Scripting/v61b/spaziotempo/__init__.py` |
| 3 | `Scripting/v61b_backgood/hotpatch/__init__.py` |
| 3 | `Scripting/v61b/hotpatch/__init__.py` |
| 1 | `Scripting/v61b_backgood/__init__.py` |
| 1 | `Tools/workflow/gui/components/__init__.py` |
| 1 | `Scripting/v61b/spaziotempo/features/__init__.py` |
| 1 | `Scripting/v61b/__init__.py` |
| 1 | `Scripting/v61b/spaziotempo/core/__init__.py` |

```

### `output/ai_pipeline/md_py_consistency_20260503-163709_agent_review_decision_loop.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1085`
- SHA-256: `f442f30101c4ebbb89f558e2eca9bd36546f2690ca8ac70a0e37823f581ceb98`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Decision Loop

- Passed: `True`
- Recommendation count: `12`
- Patch plan count: `12`
- Deterministic synthesizer used: `True`
- Patch plan fallback used: `False`
- Provider execution performed: `False`
- Patch application performed: `False`

## Outputs

- `recommendations`: `output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.json` exists=`True` size=`119254`
- `recommendations_markdown`: `output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.md` exists=`True` size=`6900`
- `bridge_orchestrator`: `output/ai_pipeline/md_py_consistency_20260503-163709_bridge_orchestrator.json` exists=`True` size=`29876`
- `patch_plan`: `output/patch_specs/md_py_consistency_20260503-163709_agent_review_patch_plan.json` exists=`True` size=`194381`
- `patch_plan_markdown`: `output/patch_specs/md_py_consistency_20260503-163709_agent_review_patch_plan.md` exists=`True` size=`6752`

## Guardrails

Report-only decision loop. No provider execution, patch application, SQLite write or Blender runtime.

```

### `output/patch_specs/md_py_consistency_20260503-163709_agent_review_patch_plan.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6752`
- SHA-256: `7737734f60807def1d3dc0019098a27019f914a03f0b8f9442b7eca1253effd8`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Patch Plan

- Passed: `True`
- Apply mode: `report_only_manual_review_patch_plan`
- Provider execution performed: `False`
- Patch application performed: `False`
- Patch plan count: `12`
- Fallback used: `False`
- Manual review required: `True`

## Inputs

- `orchestrator`: `output/ai_pipeline/md_py_consistency_20260503-163709_bridge_orchestrator.json`
- `evidence`: `output/ai_pipeline/agent_review_evidence_sufficiency.json`
- `gpu_report`: `output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.json`
- `orchestrator_kind`: `deterministic_recommendation_patch_plan_bridge_orchestrator`
- `evidence_kind`: `agent_review_evidence_sufficiency`
- `gpu_kind`: `deterministic_recommendation_synthesizer`

## Patch plans

### det_doc_code_001 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/config_model.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

### det_doc_code_002 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/diagnostics.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

### det_doc_code_003 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.

### det_doc_code_004 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.

### det_doc_code_005 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.

### det_doc_code_006 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.

### det_doc_code_007 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code-quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

### det_doc_code_008 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code_quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

### det_doc_code_009 — doc_code
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/ci.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

### det_doc_doc_001 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

### det_doc_doc_002 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['docs/JSON_SCHEMAS.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

### det_doc_doc_003 — doc_doc
- Source: `gpu_recommendation`
- Risk: `low`
- Target files: `['Tools/validation/README.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

## Guardrail

This artifact is a plan only. It contains no replacements and must not be treated as an apply queue.

```

### `output/validation/md_py_consistency_patch_bundle_builder_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1396`
- SHA-256: `f0dd8e6b89d227497a4a3f81081ca0434afb4a47fe2ce2e9c62a3fd57826e173`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Patch Bundle Builder

- Passed: `True`
- Bundle: `md_py_consistency_patch_bundle_20260503-163709`
- Bundle ZIP: `output/validation/patch_bundles/md_py_consistency_patch_bundle_20260503-163709.zip`
- Operation count: `12`
- Skipped candidates: `0`
- Patch application performed: `False`
- SQLite write performed: `False`

## Operations
- `det_doc_code_001-docs-ai_onboarding.md` -> `docs/AI_ONBOARDING.md`
- `det_doc_code_002-docs-ai_onboarding.md` -> `docs/AI_ONBOARDING.md`
- `det_doc_code_003-docs-ai_reference_onboarding.md` -> `docs/AI_REFERENCE_ONBOARDING.md`
- `det_doc_code_004-docs-ai_reference_onboarding.md` -> `docs/AI_REFERENCE_ONBOARDING.md`
- `det_doc_code_005-docs-ai_reference_source_map.md` -> `docs/AI_REFERENCE_SOURCE_MAP.md`
- `det_doc_code_006-docs-ai_reference_source_map.md` -> `docs/AI_REFERENCE_SOURCE_MAP.md`
- `det_doc_code_007-docs-code_consultation_report.md` -> `docs/CODE_CONSULTATION_REPORT.md`
- `det_doc_code_008-docs-code_consultation_report.md` -> `docs/CODE_CONSULTATION_REPORT.md`
- `det_doc_code_009-docs-code_consultation_report.md` -> `docs/CODE_CONSULTATION_REPORT.md`
- `det_doc_doc_001-docs-local_ai_core_tool_activation.md` -> `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md`
- `det_doc_doc_002-docs-json_schemas.md` -> `docs/JSON_SCHEMAS.md`
- `det_doc_doc_003-tools-validation-readme.md` -> `Tools/validation/README.md`

```

### `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-163724.csv`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.csv`
- Size bytes: `15055`
- SHA-256: `52fd72f5f65b8d70263898135b906f8979aee5d0c13f3c1bcd4a205b4c5fbb00`
- Content included: `True`
- Content truncated: `False`

```text
File,Lines
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py,2197
Tools/npu/run_dual_ai_pipeline.py,1773
old script legacy/spaziotempo_asset_visual_v61.py,1513
Scripting/v61b/scene_tuning_panel.py,1262
Tools/workflow/workflow_state.py,1230
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py,1179
old script legacy/spaziotempo_asset_visual_v6.py,1174
Tools/ai/run_agent_gpu_deep_planning_supervised.py,1115
Scripting/v61b_backgood/scene_tuning_panel.py,1097
Scripting/v61b/animation.py,1079
Scripting/v61b_backgood/animation.py,1019
old script legacy/spaziotempo_album_visual_v5.py,969
Tools/ai/run_agent_gpu_deep_planning_review.py,902
Tools/workflow/gui/workflow_gui.py,738
Scripting/v61b/physics_setup.py,737
Scripting/v61b/asset_setup.py,725
Scripting/v61b_backgood/asset_setup.py,725
Tools/ai/build_refactor_duplication_audit.py,725
Scripting/v61b_backgood/physics_setup.py,720
Tools/ai/agent_runtime_tool_broker.py,715
Tools/npu/build_music_context.py,711
old script legacy/spaziotempo_album_visual_v3.py,710
Tools/ai/run_npu_gpu_deep_review_auditor.py,694
Tools/ai/build_deterministic_recommendations.py,685
Scripting/v61b/materials.py,657
Tools/npu/run_npu_review.py,631
Tools/validation/check_npu_pipeline_modules.py,627
Tools/ai/build_selective_execution_plan.py,618
Tools/ai/build_agent_review_patch_bundle.py,608
Tools/workflow/workflow_debug.py,607
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py,604
Tools/ai/build_repository_change_proposals.py,582
Tools/ai/build_ai_context_pack.py,579
Tools/ai/run_pipeline_dry_run_matrix.py,573
Tools/ai/build_agent_review_patch_plan.py,570
Scripting/v61b/atmosphere_setup.py,554
Tools/ai/suggest_repository_updates.py,551
Tools/ai/agent_state.py,544
Scripting/v61b_backgood/atmosphere_setup.py,543
Tools/ai/agent_runtime_sqlite_memory.py,527
Tools/ai/run_megalithic_repo_review.py,519
Scripting/v61b_backgood/materials.py,513
Tools/ai/build_agent_review_code_patch_plan.py,499
Tools/validation/ai_pipeline_report_contracts.py,497
Tools/npu/npu_guardrail_service.py,490
Tools/ai/refine_megalithic_review_signals.py,489
Tools/validation/run_agent_review_patch_plan_full_validation.py,487
Tools/validation/run_agnostic_ai_tools_smoke_matrix.py,483
Tools/ai/agent_memory_routing_policy.py,471
normalize_scene_spec.py,469
Tools/validation/check_reviewed_patch_specs.py,446
Tools/repo_patch_runner/apply_repo_mods.py,443
Tools/ai/promote_patch_spec_draft.py,442
Scripting/v61b/config.py,439
Tools/npu/ollama_runtime.py,438
Tools/ai/build_code_interpreter_report.py,437
Tools/npu/build_project_ai_index.py,436
Tools/validation/check_ai_context_pack_contract.py,425
Tools/workflow/gui/components/storage_dashboard.py,422
Tools/workflow/scene_brief.py,419
Tools/ai/build_patch_specs_from_proposals.py,414
Tools/ai/schema_repair_context.py,411
Tools/ai/agent_review_warning_policy.py,408
Tools/ai/build_agent_agnostic_tool_inventory.py,408
Tools/ai/build_agent_review_evidence_sufficiency.py,407
Tools/npu/build_npu_code_context.py,402
Tools/validation/check_github_evidence_bundle.py,401
Tools/validation/check_patch_spec_drafts.py,400
Scripting/v61b/encode_ffmpeg_v61b.py,399
Tools/ai/build_dry_run_matrix_evidence_bundle.py,398
Tools/ai/build_agent_memory_inventory.py,397
Scripting/v61b/encode_image_sequence_v61b.py,395
Scripting/v61b/hotpatch/hero_material_patch.py,395
Scripting/v61b_backgood/hotpatch/hero_material_patch.py,395
Scripting/v61b/fog_dynamics.py,392
Tools/ai/build_full_context_golden_proposals.py,392
Tools/validation/check_code_contract_drift.py,392
Tools/workflow/gui/components/artifact_browser.py,390
Tools/ai/gpu_planner_json_contract.py,380
Scripting/v61b_backgood/encode_image_sequence_v61b.py,376
indexAI/scene_scripts/lll_luca_vera_master_scene_builder_candidate.py,369
Tools/npu/generated_blender_script_candidate.py,369
Tools/npu/generated_blender_script_candidate_FristNear.py,369
Tools/validation/check_repository_change_proposals.py,366
Tools/validation/test_npu_pipeline_helpers.py,359
Scripting/v61b_backgood/config.py,358
Tools/ai/build_local_ai_enrichment_plan.py,357
Tools/npu/build_ai_service_packet.py,355
Tools/workflow/project_awareness.py,353
Tools/validation/check_ai_dry_run_matrix_contract.py,341
Tools/validation/check_selected_semantic_chunks.py,339
Tools/ai/check_local_resource_lanes.py,335
Tools/validation/apply_docs_contract_drift_fixes.py,331
Tools/npu/build_npu_knowledge_broker_packet.py,327
Tools/npu/build_blender_manual_context.py,326
Tools/validation/run_shared_toolbox_ai_to_ai_bundle_smoke.py,325
Tools/workflow/workflow_shell.py,324
Tools/validation/check_dry_run_matrix_evidence_bundle.py,321
Tools/ai/build_music_intermediates.py,319
Tools/workflow/gui/workflow_gui_modern.py,319
Tools/validation/check_local_ai_adapter_manifest.py,317
Tools/ai/github_evidence_bundle_artifacts.py,315
Tools/ai/run_npu_decode_smoke_diagnostic.py,314
Tools/ai/agent_memory_policy.py,307
Tools/validation/check_full_context_golden_proposals.py,307
Tools/validation/run_agent_review_decision_loop_smoke.py,307
Tools/ai/run_agent_review_decision_loop.py,305
Tools/ai/build_analysis_input_bundle.py,304
Scripting/v61b/hotpatch/accent_patch.py,301
Tools/npu/pipeline/providers.py,297
Tools/ai/build_agent_transient_request_context.py,291
Tools/ai/select_semantic_code_chunks.py,291
Tools/validation/check_ai_pipeline_modules.py,290
Tools/validation/run_gpu_planner_json_contract_smoke.py,290
Scripting/v61b/hotpatch/diagnostics.py,286
Tools/ai/build_gpu_repair_failure_recommendation.py,286
Tools/workflow/startup_check.py,284
Tools/validation/run_agent_review_patch_plan_smoke.py,283
Tools/workflow/gui/components/session_overview.py,278
Tools/ai/analyze_gpu_npu_run_sync.py,276
Scripting/v61b/render_setup.py,270
Tools/validation/check_full_context_golden_docs_contract.py,270
Scripting/v61b_backgood/render_setup.py,267
Tools/workflow/ai_runtime_diagnostics.py,267
Tools/ai/build_code_patch_docs_followup.py,266
Tools/validation/check_ai_workload_report_quality.py,260
Tools/ai/build_megalithic_review_pr_draft.py,259
Tools/validation/check_docs_contract_drift.py,259
Tools/ai/build_code_patch_artifact_pack.py,258
Tools/validation/run_refactor_duplication_audit_smoke.py,258
analyze_wav.py,257
Tools/validation/run_agnostic_context_stack_smoke.py,256
Tools/ai/build_code_edit_proposal_from_plan.py,250
Tools/validation/run_gpu_runtime_tool_bootstrap_smoke.py,247
Tools/validation/run_agent_review_patch_bundle_builder_smoke.py,244
Tools/validation/run_agent_runtime_tool_broker_smoke.py,244
Scripting/v61b_backgood/fog_dynamics.py,240
Tools/ai/review_wave_entrypoints.py,240
Tools/npu/run_ollama_music_agent.py,238
Tools/validation/check_selective_execution_plan.py,238
Tools/validation/run_agent_review_warning_policy_smoke.py,237
Tools/validation/run_agent_memory_routing_policy_smoke.py,234
Tools/ai/replay_gpu_planner_json_contract.py,232
Tools/ai/smart_ai_gatekeeper.py,232
Tools/ai/enrich_github_evidence_bundle_code_plan.py,231
Tools/validation/check_ai_dry_run_matrix_outputs.py,230
Tools/validation/check_npu_knowledge_broker_packet.py,229
Tools/ai/build_github_evidence_bundle.py,228
Tools/ai/workload_quality.py,222
Tools/validation/check_generated_artifact_path_policy.py,222
Scripting/v61b/spaziotempo/core/registry.py,221
Tools/workflow/smart_ai_context.py,219
Tools/ai/artifact_domain_registry.py,217
Tools/validation/generated_file_policy.py,217
Tools/validation/build_python_line_count_csv.py,212
Tools/ai/github_evidence_bundle_reports.py,211
Tools/ai/github_evidence_bundle_markdown.py,209
Tools/validation/check_local_ai_enrichment_plan.py,209
Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py,208
Tools/validation/check_core_activation_agnostic_contract.py,207
Scripting/v61b/hotpatch/render_patch.py,206
Scripting/v61b_backgood/hotpatch/render_patch.py,206
Tools/ai/code_patch_plan_common.py,205
Tools/validation/run_agent_review_evidence_sufficiency_smoke.py,204
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/encode_final_youtube.py,203
Tools/validation/run_code_edit_proposal_smoke.py,203
Tools/ai/code_edit_proposal_helpers.py,201
Tools/validation/check_validation_report_contract.py,201
Tools/validation/run_agent_review_code_patch_plan_smoke.py,201
Scripting/v61b/main_v61b.py,200
Tools/ai/validate_ai_artifacts.py,200
Scripting/v61b/world_setup.py,198
Tools/ai/pipeline/steps.py,197
Tools/validation/generated_python_policy.py,197
Tools/validation/report_utils.py,190
Tools/validation/run_runtime_tool_guidance_fallback_smoke.py,190
Tools/ai/check_npu_provider_environment.py,189
Tools/ai/build_workload_quality_lane_routing.py,186
Tools/validation/run_npu_runtime_tool_context_smoke.py,186
Tools/workflow/git_auto_push.py,186
Tools/ai/pipeline/remediation.py,185
Tools/validation/check_ai_dry_run_matrix_cases.py,183
Tools/validation/run_schema_repair_retry_smoke.py,183
Tools/workflow/gui/components/action_panel.py,183
Tools/ai/run_local_provider_probe.py,182
Tools/workflow/gui/components/live_output_panel.py,182
Scripting/v61b_backgood/main_v61b.py,181
Tools/workflow/gui/workflow_gui_with_push.py,181
Scripting/v61b_backgood/world_setup.py,174
Tools/ai/runtime_tool_guidance.py,173
Tools/validation/check_generated_blender_script_policy.py,173
Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py,172
Tools/validation/run_schema_repair_context_smoke.py,168
Tools/validation/run_agent_review_full_toolbox_workflow_static_smoke.py,167
Scripting/shared/image_sequence.py,161
Tools/validation/run_npu_runtime_tool_execution_smoke.py,161
Tools/npu/npu_runtime.py,160
Scripting/v61b/fog_filaments.py,159
Tools/ai/github_evidence_bundle_io.py,159
Tools/validation/check_npu_decode_quality_remediation.py,159
Tools/validation/run_provider_empty_response_diagnostics_smoke.py,159
Tools/npu/pipeline/__init__.py,157
Tools/validation/run_schema_repair_retry_bootstrap_smoke.py,156
Tools/validation/run_runtime_tool_feedback_loop_smoke.py,154
Tools/ai/pipeline/models.py,152
Scripting/v61b/hotpatch/lighting_patch.py,150
Tools/validation/check_refactor_status_consistency.py,149
Tools/npu/build_runtime_output_manifest.py,148
Tools/npu/build_provider_result_report.py,147
Tools/validation/check_blender_shared_compat_smoke.py,147
Tools/ai/github_evidence_bundle_decisions.py,146
Tools/workflow/artifact_consult.py,144
Tools/validation/run_npu_runtime_tool_fallback_smoke.py,143
Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py,142
Tools/validation/check_docs_links.py,141
Scripting/shared/blender_compat.py,140
Scripting/shared/ffmpeg_encoder.py,134
Scripting/shared/render_profiles.py,133
Scripting/v61b/hotpatch/fog_patch.py,133
Scripting/v61b/spaziotempo/core/collections.py,132
Tools/validation/check_json_artifacts.py,132
Tools/ai/model_json.py,130
Tools/ai/build_agent_state_packet.py,128
Tools/npu/pipeline/artifact_paths.py,127
Tools/npu/run_npu_artifact_reviewer.py,127
Scripting/v61b_backgood/hotpatch/accent_patch.py,125
Tools/npu/pipeline/reports.py,125
Tools/validation/check_agent_memory_policy.py,125
Tools/validation/check_generated_python_policy.py,125
Scripting/v61b_backgood/hotpatch/fog_patch.py,124
Tools/validation/check_execution_plan_status.py,123
Tools/validation/check_ai_model_json.py,119
Tools/validation/check_package_structure.py,119
Tools/ai/pipeline/schema_report.py,118
Tools/workflow/workflow_shell_with_push.py,117
Tools/validation/run_runtime_sqlite_persistent_write_smoke.py,116
build_track_summary.py,113
Tools/npu/ai_memory_context.py,111
Tools/workflow/asset_inventory.py,110
Tools/ai/pipeline/markdown_report.py,107
Tools/npu/pipeline/config.py,107
Tools/validation/check_python_syntax.py,105
Tools/ai/pipeline/preflight.py,104
Scripting/v61b/hotpatch/runner.py,103
Scripting/shared/path_utils.py,102
Tools/ai/pipeline/runner.py,102
Tools/npu/pipeline/prompts.py,99
Scripting/v61b/scene_utils.py,97
Scripting/v61b_backgood/scene_utils.py,97
Tools/ai/pipeline/guardrail_models.py,97
Tools/validation/check_npu_pipeline_docs.py,96
Tools/workflow/gui/components/st_theme.py,92
Scripting/v61b/hotpatch/common.py,91
Scripting/v61b_backgood/hotpatch/common.py,91
Tools/npu/build_semantic_code_chunks.py,91
Tools/validation/run_npu_tool_request_contract_smoke.py,90
Scripting/shared/json_io.py,88
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py,88
Tools/ai/pipeline/artifact_contracts.py,86
Scripting/v61b_backgood/hotpatch/lighting_patch.py,85
Tools/npu/pipeline/validators.py,84
Tools/validation/check_provider_result_parsing.py,83
Scripting/v61b/io_utils.py,81
Scripting/v61b_backgood/io_utils.py,81
Tools/npu/pipeline/fixtures.py,80
Scripting/_template_audio_reactive_package/main.py,79
Scripting/_template_audio_reactive_package/encode_ffmpeg.py,75
Tools/npu/pipeline/context_builder.py,75
Tools/ai/pipeline/reports.py,74
Tools/ai/pipeline/compat.py,73
Tools/validation/build_full_python_line_count_markdown.py,71
Tools/ai/pipeline/refactor_status.py,70
Tools/npu/pipeline/runner.py,70
Tools/ai/review_agent_memory.py,69
Tools/npu/pipeline/migration_readiness.py,68
Tools/ai/pipeline/scheduler.py,66
Tools/ai/run_parallel_artifact_pipeline.py,65
Tools/validation/check_ai_pipeline_report_contract.py,65
Tools/validation/check_artifact_domain_registry.py,64
Scripting/v61b/hot_update_scene_v61b.py,63
Scripting/v61b_backgood/hot_update_scene_v61b.py,61
Tools/npu/pipeline/io_utils.py,61
Scripting/v61b_backgood/hotpatch/runner.py,60
Tools/validation/check_npu_pipeline_helper_tests.py,59
Tools/npu/pipeline/artifact_writer.py,56
Tools/ai/merge_ai_candidates.py,53
Tools/npu/pipeline/legacy_compat.py,52
Scripting/_template_audio_reactive_package/audio_mapping.py,51
Scripting/v61b/reload_utils.py,51
Tools/ai/pipeline/cli.py,50
Scripting/_template_audio_reactive_package/config.py,49
Scripting/_template_audio_reactive_package/materials.py,35
Tools/ai/pipeline/orchestrator.py,31
Scripting/v61b/camera_setup.py,29
Scripting/v61b_backgood/camera_setup.py,29
Scripting/_template_audio_reactive_package/camera.py,26
Scripting/_template_audio_reactive_package/render_settings.py,26
Scripting/_template_audio_reactive_package/lighting.py,23
Tools/ai/pipeline/__init__.py,23
Scripting/_template_audio_reactive_package/scene_objects.py,21
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/render_profiles_reference.py,20
Scripting/v61b/spaziotempo/features/catalog.py,19
Tools/ai/pipeline/defaults.py,15
Scripting/shared/__init__.py,13
Scripting/v61b/spaziotempo/__init__.py,4
Scripting/v61b/hotpatch/__init__.py,3
Scripting/v61b_backgood/hotpatch/__init__.py,3
Scripting/v61b/__init__.py,1
Scripting/v61b/spaziotempo/core/__init__.py,1
Scripting/v61b/spaziotempo/features/__init__.py,1
Scripting/v61b_backgood/__init__.py,1
Tools/workflow/gui/components/__init__.py,1

```

### `output/ai_pipeline/agent_review_evidence_sufficiency.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `35905`
- SHA-256: `a2216b89a69fc267b8015cfcbf775591b4c8b05abd127aef322936947f80683c`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_review_evidence_sufficiency",
  "generated_at": "2026-05-01T17:46:48",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_evidence_sufficiency",
  "inputs": {
    "refined_review": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json",
    "refined_proposals": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_proposals_v3.json",
    "refined_proposal_count": 2,
    "context_reports": [
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agent_memory_inventory.json",
        "exists": true,
        "kind": "agent_memory_inventory",
        "passed": true,
        "error": "",
        "summary": {}
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_agnostic_tool_inventory.json",
        "exists": true,
        "kind": "agent_agnostic_tool_inventory",
        "passed": true,
        "error": "",
        "summary": {
          "tool_count": 166,
          "category_counts": {
            "validator": 50,
            "provider_probe_or_adapter": 41,
            "orchestrator_pipeline": 30,
            "support_tool": 28,
            "agent_context_builder": 6,
            "proposal_or_review_builder": 5,
            "git_helper": 3,
            "review_helper": 3
          },
          "owner_lane_counts": {
            "npu_explicit_provider_tool": 65,
            "cpu_validation": 29,
            "gpu_cuda_explicit_provider_tool": 27,
            "cpu_support": 22,
            "cpu_orchestration": 18,
            "cpu_context_builder": 3,
            "cpu_proposal_builder": 2
          },
          "consumed_lane_counts": {
            "cpu": 166,
            "npu": 123,
            "gpu_cuda": 89
          },
          "apply_mode_counts": {
            "not_declared": 121,
            "manual_review_only": 20,
            "report_only": 16,
            "explicit_git_operation": 9
          },
          "provider_execution_default_counts": {
            "none_or_reported": 151,
            "explicit_only": 15
          }
        }
      },
      {
        "path": "output/ai_pipeline/local_ai_core_tool_activation_transient_request_context.json",
        "exists": true,
        "kind": "agent_transient_request_context",
        "passed": true,
        "error": "",
        "summary": {}
      }
    ]
  },
  "areas": {
    "doc_code": {
      "area": "doc_code",
      "item_count": 9,
      "ready_for_manual_patch_count": 9,
      "needs_more_context_count": 0,
      "items": [
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/config_model.py",
          "candidate_references": [
            "Scripting/shared/config_model.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/config_model.py",
                "Scripting/shared/config_model.py"
              ],
              "snippet": " still needing staged decomposition. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do"
            },
            {
              "path": "Scripting/shared/config_model.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_ONBOARDING.md",
          "reference": "Scripting/shared/diagnostics.py",
          "candidate_references": [
            "Scripting/shared/diagnostics.py"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 5329,
              "lines": 115,
              "matched_terms": [
                "Scripting/shared/diagnostics.py",
                "Scripting/shared/diagnostics.py"
              ],
              "snippet": "on. |\n| `Tools/npu/pipeline/` | Additive app-agnostic helper package exists on the NPU decomposition branch; it is not wired into the runtime orchestrator until local validation and index regeneration pass. |\n| `indexAI/` | Generated AI context. Regenerate after structural or documentation changes; do not hand-refactor as source. |\n| JSON schemas | Documented as partial. Preserve unknown fields and avoid destructive normalization. |\n\nNot yet complete:\n\n```text\nScripting/shared/blender_compat.py\nScripting/shared/config_model.py\nScripting/shared/diagnostics.py\nruntime adoption of Tools/npu/pipeline/ helpers inside Tools/npu/run_dual_ai_pipeline.py\nfull production JSON schemas\nautomated Blender runtime validation\n```\n\n## First-session checklist\n\nRun only lightweight inspection first:\n\n```powershell\ngit status --short\ngit remote -v\nGet-ChildItem -File .\\docs\nGet-ChildItem -Directory .\\Scripting\nGet-ChildItem -File .\\Scripting\\shared\n```\n\nBefore code changes, run the smallest relevant validation:\n\n```powershell\npython .\\Tools\\validation\\check_python_syntax.py --repo-root .\npython .\\Tools\\validation\\check_package_structure.py --repo-root .\npython .\\Tools\\validation\\check_json_artifacts.py --repo-root .\n```\n\nFor NPU helper work, run the focused helper validation before the full runner:\n\n```powershell\npowershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1\n```\n\nFor documentation-only changes, a path/link review and `git diff` may be enough unless generated indexes must be refreshed.\n\n## Common traps\n\n- Do not assume every status document"
            },
            {
              "path": "Scripting/shared/diagnostics.py",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/external_references",
          "candidate_references": [
            "docs/external_references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/external_references",
                "docs/external_references"
              ],
              "snippet": "rnal repositories.\n\n## What this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;\n- a replacement for local validation;\n- a runtime dependency;\n- a permission to perform destructive changes;\n- a reason to bypass `AGENTS.md`, execution plans or validators.\n\n## Repository policy\n\nFull external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nThe committed repository should contain only:\n\n```text\ndocs/AI_REFERENCE_ONBOARDING.md\ndocs/AI_REFERENCE_SOURCE_MAP.md\ndocs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\ndocs/AI_GUARDRAILS_VALIDATION_GUIDE.md\ndocs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md\n```\n\nThis keeps remote AI agents effective without bloating the repository.\n\n## Recommended agent behavior\n\nWhen an AI agent uses this reference layer, it should:\n\n1. identify the target work area;\n2. read the related guide;\n3. map external concepts to existing project files;\n4. avoid introducing new dependencies unless explicitly approved;\n5. prefer additive documentation, validators and helper modules;\n6. preserve current Blender package behavior;\n7. keep NPU helper work provider-free unless a validated phase says otherwise;\n8. update `docs/README.md` when adding stable documentation;\n9. report uncertainty rather than inventing unsupported repository state.\n\n## Task routing\n\n| Task | Read first |\n|---|---|\n| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_"
            },
            {
              "path": "docs/external_references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_ONBOARDING.md",
          "reference": "docs/references",
          "candidate_references": [
            "docs/references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_ONBOARDING.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3909,
              "lines": 106,
              "matched_terms": [
                "docs/references",
                "docs/references"
              ],
              "snippet": "t this layer is not\n\nThis layer is not:\n\n- a complete mirror of OpenVINO, ONNX Runtime, Guardrails, Promptfoo, DeepEval, OpenAI Evals, AGENTS.md or MCP documentation;\n- a replacement for local validation;\n- a runtime dependency;\n- a permission to perform destructive changes;\n- a reason to bypass `AGENTS.md`, execution plans or validators.\n\n## Repository policy\n\nFull external repositories, if downloaded locally for study, should remain outside committed source or under ignored folders such as:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nThe committed repository should contain only:\n\n```text\ndocs/AI_REFERENCE_ONBOARDING.md\ndocs/AI_REFERENCE_SOURCE_MAP.md\ndocs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md\ndocs/AI_GUARDRAILS_VALIDATION_GUIDE.md\ndocs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md\n```\n\nThis keeps remote AI agents effective without bloating the repository.\n\n## Recommended agent behavior\n\nWhen an AI agent uses this reference layer, it should:\n\n1. identify the target work area;\n2. read the related guide;\n3. map external concepts to existing project files;\n4. avoid introducing new dependencies unless explicitly approved;\n5. prefer additive documentation, validators and helper modules;\n6. preserve current Blender package behavior;\n7. keep NPU helper work provider-free unless a validated phase says otherwise;\n8. update `docs/README.md` when adding stable documentation;\n9. report uncertainty rather than inventing unsupported repository state.\n\n## Task routing\n\n| Task | Read first |\n|---|---|\n| AI artifact pipeline changes | `docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md` |\n| NPU"
            },
            {
              "path": "docs/references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_SOURCE_MAP.md",
          "reference": "docs/external_references",
          "candidate_references": [
            "docs/external_references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_SOURCE_MAP.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3956,
              "lines": 94,
              "matched_terms": [
                "docs/external_references",
                "docs/external_references"
              ],
              "snippet": "command;\n- a package README update;\n- a documented execution plan.\n\n### 4. Keep AI instructions compact\n\nLarge instructions degrade agent reliability. Long background belongs in `docs/`; immediate rules belong in `AGENTS.md` and package-level README files.\n\n### 5. Prefer provider-agnostic architecture\n\nThe project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.\n\n## Local reference folders\n\nOptional local-only folders:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nSuggested `.gitignore` entries if those folders are used:\n\n```gitignore\ndocs/external_references/\ndocs/references/\n```\n\n## Maintenance rules\n\nWhen adding a new reference:\n\n1. add it to this source map;\n2. explain why it matters to this repository;\n3. map it to concrete local files;\n4. avoid copying large upstream content;\n5. add or update a validator when the rule is enforceable;\n6. update `docs/README.md` if the new document is stable.\n"
            },
            {
              "path": "docs/external_references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/AI_REFERENCE_SOURCE_MAP.md",
          "reference": "docs/references",
          "candidate_references": [
            "docs/references"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/AI_REFERENCE_SOURCE_MAP.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 3956,
              "lines": 94,
              "matched_terms": [
                "docs/references",
                "docs/references"
              ],
              "snippet": "E update;\n- a documented execution plan.\n\n### 4. Keep AI instructions compact\n\nLarge instructions degrade agent reliability. Long background belongs in `docs/`; immediate rules belong in `AGENTS.md` and package-level README files.\n\n### 5. Prefer provider-agnostic architecture\n\nThe project may use OpenVINO, Ollama, OpenAI-compatible endpoints or local Python tools, but orchestration should avoid hard-coding one provider into core logic.\n\n## Local reference folders\n\nOptional local-only folders:\n\n```text\ndocs/external_references/\ndocs/references/\n```\n\nSuggested `.gitignore` entries if those folders are used:\n\n```gitignore\ndocs/external_references/\ndocs/references/\n```\n\n## Maintenance rules\n\nWhen adding a new reference:\n\n1. add it to this source map;\n2. explain why it matters to this repository;\n3. map it to concrete local files;\n4. avoid copying large upstream content;\n5. add or update a validator when the rule is enforceable;\n6. update `docs/README.md` if the new document is stable.\n"
            },
            {
              "path": "docs/references",
              "exists": false,
              "kind": "target_path",
              "chars": 0,
              "lines": 0,
              "matched_terms": [],
              "snippet": ""
            }
          ]
        },
        {
          "doc": "docs/CODE_CONSULTATION_REPORT.md",
          "reference": "github/workflows/code-quality.yml",
          "candidate_references": [
            "github/workflows/code-quality.yml",
            "github/workflows/code-quality.yml"
          ],
          "existing_candidate": null,
          "evidence_sufficient": true,
          "recommendation": "manual_doc_reference_patch_candidate",
          "confidence": "medium",
          "reason": "source doc exists and target path remains missing",
          "evidence_files": [
            {
              "path": "docs/CODE_CONSULTATION_REPORT.md",
              "exists": true,
              "kind": "source_markdown",
              "chars": 8873,
              "lines": 267,
              "matched_terms": [
                "github/workflows/code-quality.yml",
                "github/workflows/code-quality.yml",
                "github/workflows/code-quality.yml"
              ],
              "snippet": "ty check was launched.\n\nThe review is non-destructive. No working Blender script was refactored or modified.\n\n## Repository status\n\n- Repository: `C-F-tek/blender-audio-project`\n- Default branch: `master`\n- Visibility: private\n- GitHub App permissions observed: admin, maintain, pull, push, triage\n- Repository size observed: about 2564 KB\n\n## Code quality workflow visibility\n\nNo workflow run was visible through the available GitHub connector for the checked commits.\n\nThe following common workflow paths were not found:\n\n```text\n.github/workflows/code-quality.yml\n.github/workflows/code_quality.yml\n.github/workflows/ci.yml\n```\n\nThis means that the code-quality action may be 
```

### `output/ai_pipeline/md_py_consistency_20260503-163709_bridge_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `29876`
- SHA-256: `a74b2701b908693dfc8c149f7ecc15469df9cf490bc2cd0900a2d50e9173d49e`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
  "generated_at": "2026-05-03T16:54:29",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "gpu_output": "output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.json",
  "gpu_recommendation_count": 12,
  "gpu_empty_recommendations_reason": "",
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-03T16:37:42",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "skipped",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:39:00",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 4,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_004.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_004_npu_async_audit.json",
      "started_at": "2026-05-03T16:39:24",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:40:42",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_004_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_004_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 8,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_008.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_008_npu_async_audit.json",
      "started_at": "2026-05-03T16:40:44",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:42:02",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_008_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_008_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 12,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_012.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_012_npu_async_audit.json",
      "started_at": "2026-05-03T16:43:34",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:44:52",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_012_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_012_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 16,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_016.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_016_npu_async_audit.json",
      "started_at": "2026-05-03T16:47:52",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_016.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_016_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_016_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_016_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_016_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_016_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_016_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:49:10",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_016_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_016_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"np
```

### `output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `119254`
- SHA-256: `0466179b2103121bddcae2a45b566cbde0c09f802da00ca3b31b33e822da7bd4`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "deterministic_recommendation_synthesizer",
  "generated_at": "2026-05-03T16:54:29",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": true,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "manual_review_required": true,
  "recommendation_count": 12,
  "recommendations": [
    {
      "id": "det_doc_code_001",
      "area": "doc_code",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/AI_ONBOARDING.md"
      ],
      "rationale": "source doc exists and target path remains missing",
      "proposed_strategy": "Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/config_model.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.",
      "risk": "low",
      "validation_commands": [
        "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
        "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
        "git diff --check",
        "git status --short"
      ],
      "stop_conditions": [
        "Stop if the referenced file exists after refreshing master.",
        "Stop if the fix requires creating runtime code instead of correcting documentation or references.",
        "Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime."
      ],
      "source": "deterministic_evidence_synthesizer",
      "evidence": [
        "docs/AI_ONBOARDING.md",
        "Scripting/shared/config_model.py"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/code_interpreter_md_py_consistency_20260503-163709.json",
          "kind": "code_interpreter_report",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/markdown_inventory_md_py_consistency_20260503-163709.json",
          "kind": "markdown_inventory",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/python_line_count_md_py_consistency_20260503-163709.json",
          "kind": "python_line_count_csv",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/python_syntax_md_py_consistency_20260503-163709.json",
          "kind": "python_syntax",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu_planner_json_contract_smoke_md_py_consistency_20260503-163709.json",
          "kind": "gpu_planner_json_contract_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_md_py_consistency_20260503-163709.json",
          "kind": "deterministic_recommendation_synthesizer_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/agent_review_decision_loop_smoke_md_py_consistency_20260503-163709.json",
          "kind": "agent_review_decision_loop_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/agent_review_patch_bundle_builder_smoke_md_py_consistency_20260503-163709.json",
          "kind": "agent_review_patch_bundle_builder_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/npu_provider_environment_md_py_consistency_20260503-163709.json",
          "kind": "npu_provider_environment",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_json_contract_replay_md_py_consistency_20260503-163709.json",
          "kind": "gpu_planner_json_contract_replay",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_npu_run_sync_md_py_consistency_20260503-163709.json",
          "kind": "gpu_npu_run_sync_analysis",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/full_memory_tool_regeneration_20260503-163709_workflow.json",
          "kind": "full_memory_tool_regeneration_workflow",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        }
      ],
      "npu_audit_refs": [
        {
          "round": 1,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 4,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 8,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 12,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 16,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 20,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 24,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        }
      ],
      "guardrails": {
        "patch_application_performed": false,
        "manual_review_required": true
      }
    },
    {
      "id": "det_doc_code_002",
      "area": "doc_code",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/AI_ONBOARDING.md"
      ],
      "rationale": "source doc exists and target path remains missing",
      "proposed_strategy": "Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/diagnostics.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.",
      "risk": "low",
      "validation_commands": [
        "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
        "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
        "git diff --check",
        "git status --short"
      ],
      "stop_conditions": [
        "Stop if the referenced file exists after refreshing master.",
        "Stop if the fix requires creating runtime code instead of correcting documentation or references.",
        "Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime."
      ],
      "source": "deterministic_evidence_synthesizer",
      "evidence": [
        "docs/AI_ONBOARDING.md",
        "Scripting/shared/diagnostics.py"
      ],
      "tool_evidence": [
        {
          "path": "output/analysis/code_interpreter_md_py_consistency_20260503-163709.json",
          "kind": "code_interpreter_report",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/markdown_inventory_md_py_consistency_20260503-163709.json",
          "kind": "markdown_inventory",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/python_line_count_md_py_consistency_20260503-163709.json",
          "kind": "python_line_count_csv",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/python_syntax_md_py_consistency_20260503-163709.json",
          "kind": "python_syntax",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": null,
          "patch_application_performed": null
        },
        {
          "path": "output/validation/gpu_planner_json_contract_smoke_md_py_consistency_20260503-163709.json",
          "kind": "gpu_planner_json_contract_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/deterministic_recommendation_synthesizer_smoke_md_py_consistency_20260503-163709.json",
          "kind": "deterministic_recommendation_synthesizer_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/agent_review_decision_loop_smoke_md_py_consistency_20260503-163709.json",
          "kind": "agent_review_decision_loop_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/agent_review_patch_bundle_builder_smoke_md_py_consistency_20260503-163709.json",
          "kind": "agent_review_patch_bundle_builder_smoke",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/npu_provider_environment_md_py_consistency_20260503-163709.json",
          "kind": "npu_provider_environment",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_json_contract_replay_md_py_consistency_20260503-163709.json",
          "kind": "gpu_planner_json_contract_replay",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/analysis/gpu_npu_run_sync_md_py_consistency_20260503-163709.json",
          "kind": "gpu_npu_run_sync_analysis",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        },
        {
          "path": "output/validation/full_memory_tool_regeneration_20260503-163709_workflow.json",
          "kind": "full_memory_tool_regeneration_workflow",
          "passed": true,
          "tool_request_count": null,
          "tool_execution_count": null,
          "failed_tool_count": null,
          "blocked_tool_count": null,
          "provider_execution_performed": false,
          "patch_application_performed": false
        }
      ],
      "npu_audit_refs": [
        {
          "round": 1,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 4,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 8,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 12,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 16,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 20,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        },
        {
          "round": 24,
          "status": "finished",
          "classification": "usable_audit_text",
          "runtime_tool_context_seen": false,
          "npu_tool_request_count": 0,
          "npu_runtime_tool_execution_count": null,
          "npu_runtime_tool_failed_count": null,
          "npu_runtime_tool_blocked_count": null
        }
      ],
      "guardrails": {
        "patch_application_performed": false,
        "manual_review_required": true
      }
    },
    {
      "id": "det_doc_code_003",
      "area": "doc_code",
      "status": "ready_for_patch_plan",
      "target_files": [
        "docs/AI_REFERENCE_ONBOARDING.md"
      ],
      "rationale": "source doc exists and target path remains missing",
      "proposed_strategy": "Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFE
```

### `output/ai_pipeline/md_py_consistency_20260503-163709_deterministic_recommendations.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `6900`
- SHA-256: `be8fadd2022338579f3f5174ac5f31cbe86bc0eeb55ee8dea5b63a2714bd69f4`
- Content included: `True`
- Content truncated: `False`

```text
# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `12`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `json_parse_failure`
- Evidence ready for manual patch count: `12`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### det_doc_code_001 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/config_model.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/config_model.py`.

### det_doc_code_002 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/AI_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Scripting/shared/diagnostics.py` and update `docs/AI_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `Scripting/shared/diagnostics.py`.

### det_doc_code_003 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.

### det_doc_code_004 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_ONBOARDING.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_ONBOARDING.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.

### det_doc_code_005 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/external_references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/external_references`.

### det_doc_code_006 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/AI_REFERENCE_SOURCE_MAP.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `docs/references` and update `docs/AI_REFERENCE_SOURCE_MAP.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `docs/references`.

### det_doc_code_007 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code-quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code-quality.yml`.

### det_doc_code_008 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/code_quality.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/code_quality.yml`.

### det_doc_code_009 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/CODE_CONSULTATION_REPORT.md']`
- Rationale: source doc exists and target path remains missing
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `github/workflows/ci.yml` and update `docs/CODE_CONSULTATION_REPORT.md` only if the reference is stale or should point at an existing artifact. Candidate references observed: `github/workflows/ci.yml`.

### det_doc_doc_001 — doc_doc
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `provider_execution_performed`, `patch_application_performed`, `manual_review_only`, `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

### det_doc_doc_002 — doc_doc
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['docs/JSON_SCHEMAS.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

### det_doc_doc_003 — doc_doc
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['Tools/validation/README.md']`
- Rationale: contract doc exists and missing terms are explicit
- Strategy: Add a compact cross-reference for `code_contract_drift`, `docs_contract_drift`. Link or summarize the canonical source instead of duplicating large contract sections.

## Guardrails

This report is deterministic and report-only. It is not a patch queue.

```

### `output/ai_pipeline/md_py_consistency_20260503-163709_orchestrator.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `39238`
- SHA-256: `19523b688b929627560a2909645ef53131ac2c364e224c2d00da8a43a4ed295a`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_npu_parallel_orchestrator",
  "generated_at": "2026-05-03T16:54:28",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": false,
  "errors": [],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_parallel_gpu_planner_npu_auditor",
  "elapsed_seconds": 1014.356,
  "gpu_returncode": 2,
  "gpu_stdout_tail": "{\n  \"passed\": false,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_parallel_gpu.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_parallel_gpu.md\",\n  \"provider_execution_performed\": true,\n  \"patch_application_performed\": false,\n  \"elapsed_seconds\": 1006.107,\n  \"round_count\": 28,\n  \"npu_audit_count\": 0,\n  \"npu_audit_success_count\": 0,\n  \"npu_auditor_disabled_reason\": \"\",\n  \"recommendation_count\": 0,\n  \"raw_recommendation_candidate_count\": 0,\n  \"filtered_recommendation_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"empty_recommendations_reason\": \"json_parse_failure\",\n  \"runtime_tool_broker_enabled\": false,\n  \"runtime_tool_bootstrap_executed\": false,\n  \"runtime_tool_bootstrap_passed\": null,\n  \"runtime_tool_bootstrap_request_count\": 0,\n  \"runtime_tool_bootstrap_execution_count\": 0,\n  \"runtime_tool_bootstrap_failed_count\": 0,\n  \"runtime_tool_bootstrap_blocked_count\": 0,\n  \"runtime_tool_request_count\": 112,\n  \"runtime_tool_execution_count\": 0,\n  \"runtime_tool_failed_count\": 0,\n  \"runtime_tool_blocked_count\": 0,\n  \"runtime_tool_result_count\": 0,\n  \"provider_empty_response_count\": 0,\n  \"evidence_ready_for_manual_patch_count\": 12,\n  \"ready_for_patch_plan\": false,\n  \"recommended_next_layer\": \"build_agent_review_patch_plan.py\"\n}\n",
  "gpu_stderr_tail": "",
  "gpu_output": "output/ai_pipeline/md_py_consistency_20260503-163709_parallel_gpu.json",
  "gpu_markdown": "output/ai_pipeline/md_py_consistency_20260503-163709_parallel_gpu.md",
  "gpu_recommendation_count": 0,
  "gpu_empty_recommendations_reason": "json_parse_failure",
  "gpu_evidence_ready_for_manual_patch_count": 12,
  "gpu_recommended_next_layer": "build_agent_review_patch_plan.py",
  "runtime_tool_broker_enabled": false,
  "runtime_tool_bootstrap_executed": false,
  "runtime_tool_bootstrap_passed": null,
  "runtime_tool_bootstrap_request_count": 0,
  "runtime_tool_bootstrap_execution_count": 0,
  "runtime_tool_bootstrap_failed_count": 0,
  "runtime_tool_bootstrap_blocked_count": 0,
  "runtime_tool_request_count": 112,
  "runtime_tool_execution_count": 0,
  "runtime_tool_failed_count": 0,
  "runtime_tool_blocked_count": 0,
  "runtime_tool_result_count": 0,
  "gpu_runtime_tool_broker_enabled": false,
  "gpu_runtime_tool_request_count": 112,
  "gpu_runtime_tool_execution_count": 0,
  "gpu_runtime_tool_failed_count": 0,
  "gpu_runtime_tool_blocked_count": 0,
  "gpu_runtime_tool_result_count": 0,
  "runtime_tool_provider_request_count": 112,
  "runtime_tool_provider_request_execution_count": 0,
  "runtime_tool_provider_request_failed_count": 0,
  "runtime_tool_provider_request_blocked_count": 0,
  "runtime_tool_provider_request_result_count": 0,
  "deterministic_runtime_tool_fallback_request_count": 0,
  "deterministic_runtime_tool_fallback_execution_count": 0,
  "deterministic_runtime_tool_fallback_failed_count": 0,
  "deterministic_runtime_tool_fallback_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap": {
    "enabled": false,
    "executed": false,
    "bootstrap": true,
    "requested_tool_count": 0,
    "tool_results": []
  },
  "orchestrator_runtime_tool_bootstrap_executed": false,
  "orchestrator_runtime_tool_bootstrap_passed": null,
  "orchestrator_runtime_tool_bootstrap_request_count": 0,
  "orchestrator_runtime_tool_bootstrap_execution_count": 0,
  "orchestrator_runtime_tool_bootstrap_failed_count": 0,
  "orchestrator_runtime_tool_bootstrap_blocked_count": 0,
  "orchestrator_runtime_tool_bootstrap_result_count": 0,
  "gpu_orchestrated_runtime_tool_brokers": [],
  "gpu_orchestrated_runtime_tool_request_count": 0,
  "gpu_orchestrated_runtime_tool_execution_count": 0,
  "gpu_orchestrated_runtime_tool_failed_count": 0,
  "gpu_orchestrated_runtime_tool_blocked_count": 0,
  "gpu_orchestrated_runtime_tool_result_count": 0,
  "gpu_runner_direct_runtime_tool_broker": false,
  "gpu_summary": {
    "passed": false,
    "round_count": 28,
    "recommendation_count": 0,
    "raw_recommendation_candidate_count": 0,
    "filtered_recommendation_count": 0,
    "json_parse_error_count": 28,
    "repair_attempt_count": 0,
    "empty_recommendations_reason": "json_parse_failure",
    "evidence_ready_for_manual_patch_count": 12,
    "recommended_next_layer": "build_agent_review_patch_plan.py",
    "runtime_tool_broker_enabled": false,
    "runtime_tool_request_count": 112,
    "runtime_tool_execution_count": 0,
    "runtime_tool_failed_count": 0,
    "runtime_tool_blocked_count": 0,
    "runtime_tool_result_count": 0,
    "decision": {
      "ready_for_patch_plan": false,
      "ready_count": 0,
      "needs_more_context_count": 0,
      "fallback_patch_plan_recommended": true,
      "npu_auditor_non_blocking": true,
      "npu_unusable_or_failed_count": 0,
      "npu_audit_success_count": 0,
      "npu_auditor_disabled_reason": "",
      "recommended_next_layer": "build_agent_review_patch_plan.py",
      "manual_review_required": true
    },
    "gpu_direct_runtime_tool_request_count": 112,
    "gpu_direct_runtime_tool_execution_count": 0,
    "gpu_direct_runtime_tool_failed_count": 0,
    "gpu_direct_runtime_tool_blocked_count": 0,
    "gpu_direct_runtime_tool_provider_request_count": 112,
    "gpu_direct_runtime_tool_provider_request_execution_count": 0,
    "gpu_direct_runtime_tool_feedback_context_report_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_request_count": 0,
    "gpu_direct_deterministic_runtime_tool_fallback_execution_count": 0,
    "gpu_lane": {
      "mode": "primary_fast_loop",
      "provider_execution_performed": true,
      "round_count": 28,
      "recommendation_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "direct_runtime_tool_execution_count": 0,
      "direct_provider_request_execution_count": 0,
      "feedback_context_report_count": 0
    },
    "runtime_tool_feedback_context_report_count": 0
  },
  "checkpoint_dir": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints",
  "npu_audit_count": 7,
  "npu_audit_success_count": 7,
  "npu_tool_context_seen_count": 0,
  "npu_tool_request_count": 0,
  "npu_deterministic_tool_fallback_count": 0,
  "npu_runtime_tool_request_count": 0,
  "npu_runtime_tool_execution_count": 0,
  "npu_runtime_tool_failed_count": 0,
  "npu_runtime_tool_blocked_count": 0,
  "npu_runtime_tool_result_count": 0,
  "npu_audits": [
    {
      "round": 1,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_001.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_001_npu_async_audit.json",
      "started_at": "2026-05-03T16:37:42",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_001_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "skipped",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:39:00",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_001_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_001_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 4,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_004.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_004_npu_async_audit.json",
      "started_at": "2026-05-03T16:39:24",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_004_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:40:42",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_004_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_004_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 8,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_008.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_008_npu_async_audit.json",
      "started_at": "2026-05-03T16:40:44",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit.json",
        "--markdown-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit.md",
        "--context-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_context.md",
        "--npu-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_npu.md",
        "--npu-notes-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_npu_notes.md",
        "--npu-metadata-output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_008_npu_async_audit_metadata.json",
        "--timeout-seconds",
        "360",
        "--max-context-chars",
        "6000",
        "--max-prompt-chars",
        "900",
        "--max-new-tokens",
        "256",
        "--run-npu"
      ],
      "npu_lane_mode_at_launch": "slow",
      "npu_effective_auditor_every_rounds_at_launch": 4,
      "finished_at": "2026-05-03T16:42:02",
      "returncode": 0,
      "stdout_tail": "{\n  \"passed\": true,\n  \"output\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_008_npu_async_audit.json\",\n  \"markdown\": \"C:\\\\Users\\\\carmi\\\\blender\\\\blender-audio-project\\\\output\\\\ai_pipeline\\\\md_py_consistency_20260503-163709_checkpoints\\\\round_008_npu_async_audit.md\",\n  \"npu_python\": \"C:\\\\Users\\\\carmi\\\\blender\\\\venvs\\\\blender-npu-ai\\\\Scripts\\\\python.exe\",\n  \"npu_python_exists\": true,\n  \"provider_execution_requested\": true,\n  \"provider_load_attempted\": true,\n  \"provider_execution_succeeded\": true,\n  \"provider_empty_response\": false,\n  \"dependency_missing\": false,\n  \"patch_application_performed\": false,\n  \"non_blocking\": true,\n  \"classification\": \"usable_audit_text\",\n  \"runtime_tool_context_seen\": false,\n  \"runtime_tool_context_report_count\": 0,\n  \"tool_request_count\": 0,\n  \"valid_tool_request_count\": 0,\n  \"invalid_tool_request_count\": 0,\n  \"npu_deterministic_tool_fallback_used\": false,\n  \"npu_deterministic_tool_fallback_count\": 0,\n  \"gpu_review_blocked\": false\n}\n",
      "stderr_tail": "",
      "classification": "usable_audit_text",
      "provider_execution_requested": true,
      "provider_load_attempted": true,
      "provider_execution_succeeded": true,
      "provider_execution_performed": true,
      "dependency_missing": false,
      "warnings": [],
      "runtime_tool_context_seen": false,
      "runtime_tool_context_report_count": 0,
      "npu_tool_request_count": 0,
      "npu_valid_tool_request_count": 0,
      "npu_invalid_tool_request_count": 0,
      "npu_deterministic_tool_fallback_used": false,
      "npu_deterministic_tool_fallback_count": 0,
      "npu_tool_requests": [],
      "gpu_review_blocked": false
    },
    {
      "round": 12,
      "checkpoint": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_012.json",
      "audit_output": "output/ai_pipeline/md_py_consistency_20260503-163709_checkpoints/round_012_npu_async_audit.json",
      "started_at": "2026-05-03T16:43:34",
      "status": "finished",
      "command": [
        "C:\\Python314\\python.exe",
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-163709_checkpoints\\round_012.json",
        "--output",
        "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\ai_pipeline\\md_py_consistency_20260503-
```

### `output/ai_pipeline/md_py_consistency_20260503-163709_orchestrator.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2749`
- SHA-256: `2f27e5be96ee87cc74998b6b59215e8fcc8e1c2c0e808a367157be75ddb50a4f`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU/NPU Parallel Orchestrator

- `passed`: `False`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `gpu_returncode`: `2`
- `elapsed_seconds`: `1014.356`
- `npu_audit_count`: `7`
- `npu_audit_success_count`: `7`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `gpu_recommendation_count`: `0`
- `gpu_empty_recommendations_reason`: `json_parse_failure`
- `gpu_evidence_ready_for_manual_patch_count`: `12`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_request_count`: `112`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_failed_count`: `0`
- `runtime_tool_blocked_count`: `0`
- `runtime_tool_result_count`: `0`

## Decision
- `gpu_review_blocked_by_npu`: `False`
- `npu_auditor_mode`: `parallel_best_effort`
- `npu_audit_success_count`: `7`
- `npu_tool_context_seen_count`: `0`
- `npu_tool_request_count`: `0`
- `npu_deterministic_tool_fallback_count`: `0`
- `npu_runtime_tool_request_count`: `0`
- `npu_runtime_tool_execution_count`: `0`
- `npu_runtime_tool_failed_count`: `0`
- `npu_runtime_tool_blocked_count`: `0`
- `npu_runtime_tool_result_count`: `0`
- `ready_for_patch_plan`: `False`
- `fallback_patch_plan_recommended`: `True`
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `gpu_empty_recommendations_reason`: `json_parse_failure`
- `runtime_tool_broker_enabled`: `False`
- `runtime_tool_bootstrap_executed`: `False`
- `runtime_tool_bootstrap_execution_count`: `0`
- `runtime_tool_provider_request_count`: `0`
- `runtime_tool_provider_request_execution_count`: `0`
- `deterministic_runtime_tool_fallback_execution_count`: `0`
- `runtime_tool_execution_count`: `0`
- `runtime_tool_result_count`: `0`
- `manual_review_required`: `True`
- `gpu_lane_mode`: `primary_fast_loop`
- `npu_lane_mode`: `slow`
- `gpu_direct_runtime_tool_provider_request_execution_count`: `0`
- `runtime_tool_feedback_context_report_count`: `0`
- `npu_effective_auditor_every_rounds`: `4`

## NPU Audits
- round `1` status=`finished` class=`usable_audit_text` success=`True`
- round `4` status=`finished` class=`usable_audit_text` success=`True`
- round `8` status=`finished` class=`usable_audit_text` success=`True`
- round `12` status=`finished` class=`usable_audit_text` success=`True`
- round `16` status=`finished` class=`usable_audit_text` success=`True`
- round `20` status=`finished` class=`usable_audit_text` success=`True`
- round `24` status=`finished` class=`usable_audit_text` success=`True`

```

### `output/ai_pipeline/md_py_consistency_20260503-163709_parallel_gpu.json`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.json`
- Size bytes: `137790`
- SHA-256: `e3ff9a381d6b71ac0d30d20f4788414c08f087c10a793c5e84b7bb181c806674`
- Content included: `True`
- Content truncated: `True`

```text
{
  "schema_version": 1,
  "kind": "agent_gpu_deep_planning_supervised",
  "generated_at": "2026-05-03T16:54:20",
  "repo_root": "C:\\Users\\carmi\\blender\\blender-audio-project",
  "passed": false,
  "errors": [
    "round 1: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 2: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 3: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 4: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 5: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 6: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 7: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 8: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 9: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 10: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 11: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 12: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 13: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 14: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 15: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 16: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 17: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 18: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 19: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 20: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 21: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 22: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 23: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 24: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 25: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 26: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 27: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
    "round 28: UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value"
  ],
  "warnings": [],
  "provider_execution_performed": true,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
  "model_used": "qwen2.5-coder:14b",
  "ollama_base_url": "http://127.0.0.1:11434",
  "budget_minutes": 40,
  "elapsed_seconds": 1006.107,
  "context_file_count": 900,
  "round_count": 28,
  "rounds": [
    {
      "round": 1,
      "elapsed_seconds": 5.589,
      "file_count": 12,
      "files": [
        "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "docs/AI_CHUNKING_STRATEGY.md",
        "docs/AI_CONTEXT_PACKS.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/AI_EXTERNAL_KNOWLEDGE.md",
        "docs/AI_GENERATED_PACKAGE_STANDARD.md",
        "docs/AI_GUARDRAILS_VALIDATION_GUIDE.md",
        "docs/AI_MEMORY_POLICY.md",
        "docs/AI_NPU_RUNTIME_REFERENCE_GUIDE.md",
        "docs/AI_ONBOARDING.md",
        "docs/AI_PIPELINE_ARCHITECTURE.md"
      ],
      "response_chars": 0,
      "raw_response_preview": "",
      "parsed_response": {
        "summary": "provider error",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "cannot access local variable 'raw_response' where it is not associated with a value"
        ],
        "next_best_action": "inspect provider error"
      },
      "schema_repair_retry": {
        "attempted": false,
        "accepted": false,
        "reason": "not_attempted",
        "json_ok": null,
        "schema_ok": null,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,
        "empty_recommendations_reason": ""
      },
      "provider_empty_response": false,
      "tool_requests": [
        {
          "id": "fallback_python_syntax",
          "tool": "check_python_syntax",
          "reason": "Deterministic fallback after provider emitted no valid tool_requests: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_transient_context",
          "tool": "build_agent_transient_request_context",
          "reason": "Deterministic fallback to refresh transient request context: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_gpu_contract_smoke",
          "tool": "run_gpu_planner_json_contract_smoke",
          "reason": "Deterministic fallback to verify planner JSON/tool-request contract: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        }
      ],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 4,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        },
        "source": "provider_tool_requests",
        "provider_generated_tool_requests": true
      },
      "provider_tool_request_count": 4,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": false,
      "parse_error": "UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "",
      "contract": {},
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
      "round": 2,
      "elapsed_seconds": 69.697,
      "file_count": 12,
      "files": [
        "docs/AI_PIPELINE_OPTIMIZATION.md",
        "docs/AI_PIPELINE_REFACTOR_STATUS.md",
        "docs/AI_PROVIDER_AGNOSTIC_PIPELINE_GUIDE.md",
        "docs/AI_REFERENCE_ONBOARDING.md",
        "docs/AI_REFERENCE_SOURCE_MAP.md",
        "docs/AI_SELECTIVE_PLANNER.md",
        "docs/AI_SMART_POLICY.md",
        "docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md",
        "docs/AUDIO_ANALYSIS_PIPELINE.md",
        "docs/AUTO_PUSH_GENERATED_ARTIFACTS.md",
        "docs/BLENDER_SCRIPT_ENTRYPOINTS.md",
        "docs/CODE_CONSULTATION_REPORT.md"
      ],
      "response_chars": 0,
      "raw_response_preview": "",
      "parsed_response": {
        "summary": "provider error",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "cannot access local variable 'raw_response' where it is not associated with a value"
        ],
        "next_best_action": "inspect provider error"
      },
      "schema_repair_retry": {
        "attempted": false,
        "accepted": false,
        "reason": "not_attempted",
        "json_ok": null,
        "schema_ok": null,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,
        "empty_recommendations_reason": ""
      },
      "provider_empty_response": false,
      "tool_requests": [
        {
          "id": "fallback_python_syntax",
          "tool": "check_python_syntax",
          "reason": "Deterministic fallback after provider emitted no valid tool_requests: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_transient_context",
          "tool": "build_agent_transient_request_context",
          "reason": "Deterministic fallback to refresh transient request context: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_gpu_contract_smoke",
          "tool": "run_gpu_planner_json_contract_smoke",
          "reason": "Deterministic fallback to verify planner JSON/tool-request contract: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        }
      ],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 4,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        },
        "source": "provider_tool_requests",
        "provider_generated_tool_requests": true
      },
      "provider_tool_request_count": 4,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": false,
      "parse_error": "UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "",
      "contract": {},
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
      "round": 3,
      "elapsed_seconds": 7.707,
      "file_count": 12,
      "files": [
        "docs/CODEX_APP_HANDOFF_NEXT_STEPS.md",
        "docs/codex_project_status_handoff.md",
        "docs/COMPATIBILITY.md",
        "docs/DATA_FLOW.md",
        "docs/DEVELOPER_GUIDE.md",
        "docs/EXECUTION_PLANS/abandoned/README.md",
        "docs/EXECUTION_PLANS/active/2026-04-29_agent_state_memory_integration.md",
        "docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md",
        "docs/EXECUTION_PLANS/active/2026-04-29_formal_json_schema_validation.md",
        "docs/EXECUTION_PLANS/active/2026-04-29_superseded_pr_followups.md",
        "docs/EXECUTION_PLANS/active/2026-04-30_ai_pipeline_report_contracts.md",
        "docs/EXECUTION_PLANS/active/2026-04-30_dry_run_matrix_contract_followups.md"
      ],
      "response_chars": 0,
      "raw_response_preview": "",
      "parsed_response": {
        "summary": "provider error",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "cannot access local variable 'raw_response' where it is not associated with a value"
        ],
        "next_best_action": "inspect provider error"
      },
      "schema_repair_retry": {
        "attempted": false,
        "accepted": false,
        "reason": "not_attempted",
        "json_ok": null,
        "schema_ok": null,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,
        "empty_recommendations_reason": ""
      },
      "provider_empty_response": false,
      "tool_requests": [
        {
          "id": "fallback_python_syntax",
          "tool": "check_python_syntax",
          "reason": "Deterministic fallback after provider emitted no valid tool_requests: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_transient_context",
          "tool": "build_agent_transient_request_context",
          "reason": "Deterministic fallback to refresh transient request context: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_gpu_contract_smoke",
          "tool": "run_gpu_planner_json_contract_smoke",
          "reason": "Deterministic fallback to verify planner JSON/tool-request contract: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        }
      ],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 4,
        "executed": false,
        "tool_results": [],
        "guardrails": {
          "broker_execution_requires_enable_runtime_tool_broker": true,
          "patch_application_performed": false,
          "persistent_memory_write_performed": false
        },
        "source": "provider_tool_requests",
        "provider_generated_tool_requests": true
      },
      "provider_tool_request_count": 4,
      "deterministic_runtime_tool_fallback_used": false,
      "deterministic_runtime_tool_fallback_reason": "",
      "deterministic_runtime_tool_fallback_request_count": 0,
      "json_ok": false,
      "parse_error": "UnboundLocalError: cannot access local variable 'raw_response' where it is not associated with a value",
      "schema_ok": false,
      "schema_errors": [],
      "context_echo_detected": false,
      "model_output_schema_mismatch": false,
      "contract_empty_recommendations_reason": "",
      "contract": {},
      "repair_attempt_count": 0,
      "raw_recommendation_candidate_count": 0,
      "filtered_recommendation_count": 0,
      "recommendation_count": 0,
      "tool_request_count": 0,
      "valid_tool_request_count": 0,
      "invalid_tool_request_count": 0,
      "empty_recommendations_reason": "json_parse_failure",
      "evidence_ready_for_manual_patch_count": 12,
      "provider_tool_request_absence_reason": "",
      "recommended_next_layer": ""
    },
    {
      "round": 4,
      "elapsed_seconds": 25.838,
      "file_count": 12,
      "files": [
        "docs/EXECUTION_PLANS/active/2026-04-30_npu_output_policy_provider_preflight.md",
        "docs/EXECUTION_PLANS/active/2026-04-30_npu_pipeline_decomposition_plan.md",
        "docs/EXECUTION_PLANS/active/2026-04-30_runtime_safe_provider_report_adoption.md",
        "docs/EXECUTION_PLANS/active/2026-04-30_validator_report_consistency_review.md",
        "docs/EXECUTION_PLANS/active/2026-05-01_evidence_schema_contracts.md",
        "docs/EXECUTION_PLANS/active/2026-05-01_proposal_patch_spec_writer.md",
        "docs/EXECUTION_PLANS/active/2026-05-01_suggestion_artifact_contracts.md",
        "docs/EXECUTION_PLANS/active/README.md",
        "docs/EXECUTION_PLANS/completed/2026-04-29_generated_file_policy_blender_first.md",
        "docs/EXECUTION_PLANS/completed/2026-04-29_json_parser_utility_review.md",
        "docs/EXECUTION_PLANS/completed/2026-04-30_generated_python_policy.md",
        "docs/EXECUTION_PLANS/completed/2026-04-30_generic_artifact_path_policy.md"
      ],
      "response_chars": 0,
      "raw_response_preview": "",
      "parsed_response": {
        "summary": "provider error",
        "confidence": "low",
        "recommendations": [],
        "missing_evidence": [
          "cannot access local variable 'raw_response' where it is not associated with a value"
        ],
        "next_best_action": "inspect provider error"
      },
      "schema_repair_retry": {
        "attempted": false,
        "accepted": false,
        "reason": "not_attempted",
        "json_ok": null,
        "schema_ok": null,
        "recommendation_count": 0,
        "valid_tool_request_count": 0,
        "empty_recommendations_reason": ""
      },
      "provider_empty_response": false,
      "tool_requests": [
        {
          "id": "fallback_python_syntax",
          "tool": "check_python_syntax",
          "reason": "Deterministic fallback after provider emitted no valid tool_requests: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_validation_contract",
          "tool": "check_validation_report_contract",
          "reason": "Deterministic fallback to refresh validation contract evidence: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_transient_context",
          "tool": "build_agent_transient_request_context",
          "reason": "Deterministic fallback to refresh transient request context: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        },
        {
          "id": "fallback_gpu_contract_smoke",
          "tool": "run_gpu_planner_json_contract_smoke",
          "reason": "Deterministic fallback to verify planner JSON/tool-request contract: evidence_ready_but_no_tool_requests.",
          "args": {},
          "source": "deterministic_fallback"
        }
      ],
      "invalid_tool_request_errors": [],
      "runtime_tool_broker": {
        "enabled": false,
        "requested_tool_count": 4,
        "executed": false,
        "tool_results"
```

### `output/ai_pipeline/md_py_consistency_20260503-163709_parallel_gpu.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1055`
- SHA-256: `ba5c7afb283e8e46659f86d02192f70ef920bb956527572c3581772efaf8220d`
- Content included: `True`
- Content truncated: `False`

```text
# Agent GPU Deep Planning Review

- Passed: `False`
- Provider execution performed: `True`
- Patch application performed: `False`
- Model: `qwen2.5-coder:14b`
- Elapsed seconds: `1006.107`
- Round count: `28`
- Recommendation count: `0`
- Raw recommendation candidates: `0`
- Filtered recommendation count: `0`
- Tool request count: `0`
- Valid tool request count: `0`
- Invalid tool request count: `0`
- JSON parse error count: `28`
- Context echo detected count: `0`
- Model output schema mismatch count: `0`
- Empty recommendations reason: `json_parse_failure`
- Evidence ready for manual patch count: `12`

## Decision

- `ready_for_patch_plan`: `False`
- `ready_count`: `0`
- `needs_more_context_count`: `0`
- `fallback_patch_plan_recommended`: `True`
- `npu_auditor_non_blocking`: `True`
- `npu_unusable_or_failed_count`: `0`
- `npu_audit_success_count`: `0`
- `npu_auditor_disabled_reason`: ``
- `recommended_next_layer`: `build_agent_review_patch_plan.py`
- `manual_review_required`: `True`

## Recommendations


```

### `output/analysis/code_interpreter_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `7084`
- SHA-256: `0c39096bdb7da7852700407ae77ab38e78c67d10e4f948eddad4e3615692bcc5`
- Content included: `True`
- Content truncated: `False`

```text
# Static Code Interpreter Report

- Passed: `True`
- File count: `266`
- Parsed files: `266`
- Total lines: `73916`
- Total functions: `2595`
- Total classes: `92`
- Risk signals: `55`
- TODO/FIXME markers: `21`
- Recommendation count: `146`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest files

- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines, risk `high`
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines, risk `high`
- `Tools/workflow/workflow_state.py` — `1230` lines, risk `high`
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1115` lines, risk `high`
- `Scripting/v61b/animation.py` — `1079` lines, risk `high`
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines, risk `high`
- `Tools/workflow/gui/workflow_gui.py` — `738` lines, risk `medium`
- `Scripting/v61b/physics_setup.py` — `737` lines, risk `medium`
- `Scripting/v61b/asset_setup.py` — `725` lines, risk `medium`
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines, risk `medium`
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines, risk `medium`
- `Tools/npu/build_music_context.py` — `711` lines, risk `medium`
- `Tools/ai/run_npu_gpu_deep_review_auditor.py` — `694` lines, risk `medium`
- `Tools/ai/build_deterministic_recommendations.py` — `685` lines, risk `medium`
- `Scripting/v61b/materials.py` — `657` lines, risk `medium`
- `Tools/npu/run_npu_review.py` — `631` lines, risk `medium`
- `Tools/validation/check_npu_pipeline_modules.py` — `627` lines, risk `medium`
- `Tools/ai/build_selective_execution_plan.py` — `618` lines, risk `medium`
- `Tools/ai/build_agent_review_patch_bundle.py` — `608` lines, risk `medium`

## Recommendations

- `code_static_001` `Scripting/shared/image_sequence.py` risk `medium`: complex functions detected
- `code_static_002` `Scripting/v61b/animation.py` risk `high`: large Python module, large functions detected, complex functions detected
- `code_static_003` `Scripting/v61b/asset_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_004` `Scripting/v61b/atmosphere_setup.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_005` `Scripting/v61b/config.py` risk `medium`: medium-size Python module
- `code_static_006` `Scripting/v61b/encode_ffmpeg_v61b.py` risk `medium`: large functions detected, static risk calls detected
- `code_static_007` `Scripting/v61b/encode_image_sequence_v61b.py` risk `medium`: complex functions detected
- `code_static_008` `Scripting/v61b/fog_dynamics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_009` `Scripting/v61b/hotpatch/accent_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_010` `Scripting/v61b/hotpatch/diagnostics.py` risk `medium`: large functions detected, complex functions detected
- `code_static_011` `Scripting/v61b/hotpatch/fog_patch.py` risk `medium`: large functions detected
- `code_static_012` `Scripting/v61b/hotpatch/hero_material_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_013` `Scripting/v61b/hotpatch/render_patch.py` risk `medium`: large functions detected, complex functions detected
- `code_static_014` `Scripting/v61b/main_v61b.py` risk `medium`: large functions detected
- `code_static_015` `Scripting/v61b/materials.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_016` `Scripting/v61b/physics_setup.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_017` `Scripting/v61b/render_setup.py` risk `medium`: large functions detected, complex functions detected
- `code_static_018` `Scripting/v61b/scene_tuning_panel.py` risk `high`: large Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_019` `Scripting/v61b/scene_utils.py` risk `medium`: complex functions detected
- `code_static_020` `Tools/ai/agent_memory_policy.py` risk `medium`: complex functions detected
- `code_static_021` `Tools/ai/agent_memory_routing_policy.py` risk `medium`: medium-size Python module, large functions detected
- `code_static_022` `Tools/ai/agent_review_warning_policy.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_023` `Tools/ai/agent_runtime_sqlite_memory.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_024` `Tools/ai/agent_runtime_tool_broker.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected, static risk calls detected
- `code_static_025` `Tools/ai/agent_state.py` risk `medium`: medium-size Python module
- `code_static_026` `Tools/ai/analyze_gpu_npu_run_sync.py` risk `medium`: complex functions detected
- `code_static_027` `Tools/ai/build_agent_agnostic_tool_inventory.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_028` `Tools/ai/build_agent_memory_inventory.py` risk `medium`: large functions detected
- `code_static_029` `Tools/ai/build_agent_review_code_patch_plan.py` risk `medium`: medium-size Python module
- `code_static_030` `Tools/ai/build_agent_review_evidence_sufficiency.py` risk `medium`: medium-size Python module
- `code_static_031` `Tools/ai/build_agent_review_patch_bundle.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_032` `Tools/ai/build_agent_review_patch_plan.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_033` `Tools/ai/build_ai_context_pack.py` risk `medium`: medium-size Python module, complex functions detected
- `code_static_034` `Tools/ai/build_code_interpreter_report.py` risk `medium`: medium-size Python module, TODO/FIXME markers detected
- `code_static_035` `Tools/ai/build_deterministic_recommendations.py` risk `medium`: medium-size Python module, large functions detected, complex functions detected
- `code_static_036` `Tools/ai/build_dry_run_matrix_evidence_bundle.py` risk `medium`: complex functions detected
- `code_static_037` `Tools/ai/build_full_context_golden_proposals.py` risk `medium`: large functions detected
- `code_static_038` `Tools/ai/build_github_evidence_bundle.py` risk `medium`: large functions detected
- `code_static_039` `Tools/ai/build_local_ai_enrichment_plan.py` risk `medium`: large functions detected
- `code_static_040` `Tools/ai/build_music_intermediates.py` risk `medium`: large functions detected, complex functions detected

## Guardrail

This is static interpretation only. It does not execute repository code or apply changes.

```

### `output/analysis/gpu_json_contract_replay_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `599`
- SHA-256: `c625ce0532fa2219b6aa5dc888aaa9ab06f9b205811d6a744bc92f84d3f0d06a`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Replay

- Passed: `True`
- Replayed rounds: `28`
- Context echo detected: `0`
- JSON parse failures: `28`
- Schema mismatches: `0`
- Valid recommendation outputs: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## Contract reason counts

- `json_parse_failure`: `28`

## Decision

- `contract_helper_replay_available`: `True`
- `safe_to_wire_runner_after_replay`: `True`
- `recommended_next_layer`: `wire validate_model_response_contract into run_agent_gpu_deep_planning_review.py`
- `manual_review_required`: `True`


```

### `output/analysis/gpu_npu_run_sync_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1496`
- SHA-256: `0bab88804adc7d4d71efc246f34d80104bd48d66df97e576f9abccc8f04f75fe`
- Content included: `True`
- Content truncated: `False`

```text
# GPU/NPU Run Sync Analysis

- Passed: `True`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Metrics

- `gpu_round_count`: `28`
- `npu_audit_count`: `7`
- `npu_audit_success_count`: `7`
- `npu_audit_round_coverage`: `0.25`
- `avg_gpu_round_seconds`: `36.227`
- `p50_gpu_round_seconds`: `36.227`
- `p90_gpu_round_seconds`: `36.227`
- `avg_npu_audit_seconds`: `78.286`
- `p50_npu_audit_seconds`: `78.0`
- `p90_npu_audit_seconds`: `78.0`
- `npu_to_gpu_avg_duration_ratio`: `2.161`
- `gpu_elapsed_seconds`: `1014.356`
- `provider_execution_performed`: `True`
- `patch_application_performed`: `False`
- `source_writes_performed`: `False`
- `gpu_metrics_source`: `gpu_summary_or_elapsed_estimate`

## Suggested balanced profile

- `npu_auditor_every_rounds`: `2`
- `max_concurrent_npu_audits`: `1`
- `npu_auditor_timeout_seconds`: `420`
- `npu_max_context_chars`: `8000`
- `npu_max_prompt_chars`: `1200`
- `npu_max_new_tokens`: `384`
- `npu_final_wait_seconds`: `180`
- `gpu_max_new_tokens`: `3600`
- `gpu_files_per_round`: `8`
- `gpu_max_chars_per_file`: `6000`

## Reasoning

- NPU audit coverage is low compared with GPU round count; keep checkpoint auditing sampled, not per-round.
- Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.
- NPU audits are usable; tune cadence rather than disabling the lane.


```

### `output/validation/agent_review_decision_loop_smoke_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `212`
- SHA-256: `ab8c829b5f099b245a1f6048441784a3a280a173d7787782e1288efabc3bec5e`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Decision Loop Smoke

- Passed: `True`
- Return code: `0`
- Recommendation count: `1`
- Patch plan count: `1`
- Deterministic synthesizer used: `True`
- Patch application performed: `False`

```

### `output/validation/agent_review_patch_bundle_builder_smoke_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `208`
- SHA-256: `724e7a84b082a9e09ec3f7653b799bdacec2033b904c581c98f701599fff7802`
- Content included: `True`
- Content truncated: `False`

```text
# Agent Review Patch Bundle Builder Smoke

- Passed: `True`
- Return code: `0`
- Operation count: `1`
- Skipped candidate count: `1`
- Bundle ZIP exists: `True`
- Patch application performed: `False`

```

### `output/validation/deterministic_recommendation_synthesizer_smoke_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1487`
- SHA-256: `d0f044b80c6e1d6797bf9c34875a8ef1b4045cc6392587ff084a34a99d942566`
- Content included: `True`
- Content truncated: `False`

```text
# Deterministic Recommendation Synthesizer Smoke

- Passed: `True`
- Recommendation count: `1`
- Deterministic synthesizer used: `True`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Synthesized report preview

# Deterministic Recommendation Synthesizer

- Passed: `True`
- Recommendation count: `1`
- Deterministic synthesizer used: `True`
- GPU empty recommendations reason: `json_parse_failure`
- Evidence ready for manual patch count: `1`
- Next best action: `build_agent_review_patch_plan.py`
- Patch application performed: `False`

## Recommendations

### det_doc_code_001 — doc_code
- Source: `deterministic_evidence_synthesizer`
- Status: `ready_for_patch_plan`
- Risk: `low`
- Target files: `['AGENTS.md']`
- Rationale: The documentation points at a recommendation lane that must be normalized before patch-plan construction.
- Strategy: Create a narrow manual-review patch plan for the documentation/code reference mismatch. Inspect `Tools/ai/build_deterministic_recommendations.py` and update `AGENTS.md` only if the reference is stale or should point at an existing artifact. Prefer existing candidate `Tools/ai/build_agent_review_patch_plan.py` over inventing a new runtime artifact. Candidate references observed: `Tools/ai/build_agent_review_patch_plan.py`, `Tools/ai/gpu_planner_json_contract.py`.

## Guardrails

This report is deterministic and report-only. It is not a patch queue.

```

### `output/validation/full_memory_tool_regeneration_20260503-163709_workflow.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `2956`
- SHA-256: `bc31b4e110592e32fa24b0d21dd98bee28025bbb50823b1e0833a37a7d0cbcae`
- Content included: `True`
- Content truncated: `False`

```text
# Full Memory / Tool Regeneration Workflow

- Passed: `True`
- Stamp: `20260503-163709`
- Profile: `full_refactor`
- Report count: `13`
- Artifact count: `14`
- Provider execution performed: `False`
- Patch application performed: `False`
- SQLite write performed: `False`
- Persistent memory write performed: `False`

## Reports

- `.\output\ai_pipeline\full_memory_tool_regeneration_20260503-163709_agent_memory_inventory.json`
- `.\output\ai_pipeline\full_memory_tool_regeneration_20260503-163709_agnostic_tool_inventory.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_persistent_memory_status.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_operational_memory_status.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_memory_routing_policy.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_runtime_tool_broker.json`
- `.\output\ai_pipeline\full_memory_tool_regeneration_20260503-163709_transient_request_context.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_python_line_count.json`
- `.\output\analysis\full_memory_tool_regeneration_20260503-163709_code_interpreter.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_python_syntax.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_validation_report_contract.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_runtime_tool_broker_smoke.json`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_memory_routing_policy_smoke.json`

## Artifacts

- `.\docs\LOCAL_AI_TASKS\full-memory-tool-regeneration-procedure.md`
- `.\Tools\workflow\run_full_memory_tool_regeneration.ps1`
- `.\output\ai_pipeline\full_memory_tool_regeneration_20260503-163709_agent_memory_inventory.md`
- `.\output\ai_pipeline\full_memory_tool_regeneration_20260503-163709_agnostic_tool_inventory.md`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_persistent_memory_status.md`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_operational_memory_status.md`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_memory_routing_policy.md`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_runtime_tool_broker.md`
- `.\output\ai_pipeline\full_memory_tool_regeneration_20260503-163709_transient_request_context.md`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_python_line_count.md`
- `.\docs/LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_20260503-163709.csv`
- `.\output\analysis\full_memory_tool_regeneration_20260503-163709_code_interpreter.md`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_runtime_tool_broker_smoke.md`
- `.\output\validation\full_memory_tool_regeneration_20260503-163709_memory_routing_policy_smoke.md`

```

### `output/validation/gpu_planner_json_contract_smoke_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1585`
- SHA-256: `76dd638fee0692e6dd33f6f1e939f55c30942291b9aabbed865675f425bfc8b1`
- Content included: `True`
- Content truncated: `False`

```text
# GPU Planner JSON Contract Smoke

- Passed: `True`
- Case count: `7`
- Failed case count: `0`
- Patch application performed: `False`
- Source writes performed: `False`

## `valid_recommendation`

- Passed: `True`
- Expected reason: ``
- Reason: ``
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`

## `tool_requests_pending`

- Passed: `True`
- Expected reason: `tool_requests_pending`
- Reason: `tool_requests_pending`
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `invalid_tool_request`

- Passed: `True`
- Expected reason: `model_output_schema_mismatch`
- Reason: `model_output_schema_mismatch`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `False`

## `evidence_ready_no_tool_request`

- Passed: `True`
- Expected reason: `evidence_ready_but_no_tool_requests`
- Reason: `evidence_ready_but_no_tool_requests`
- JSON OK: `True`
- Schema OK: `True`
- Context echo detected: `False`

## `malformed_json`

- Passed: `True`
- Expected reason: `json_parse_failure`
- Reason: `json_parse_failure`
- JSON OK: `False`
- Schema OK: `False`
- Context echo detected: `False`

## `schema_context_echo`

- Passed: `True`
- Expected reason: `context_echo_detected`
- Reason: `context_echo_detected`
- JSON OK: `True`
- Schema OK: `False`
- Context echo detected: `True`


```

### `output/validation/npu_provider_environment_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `304`
- SHA-256: `ebcef793de1795cfc3f55063d9a02cad3467d28b6cee31e068b8067e70e75ded`
- Content included: `True`
- Content truncated: `False`

```text
# NPU Provider Environment

- `passed`: `True`
- `npu_python`: `C:\Users\carmi\blender\venvs\blender-npu-ai\Scripts\python.exe`
- `npu_python_exists`: `True`
- `openvino_import`: `True`
- `openvino_genai_import`: `True`
- `openvino_genai_pip_package`: `openvino-genai`
- `npu_available`: `True`

```

### `output/validation/python_line_count_md_py_consistency_20260503-163709.md`

- Role: `auto_related_artifact`
- Exists: `True`
- Suffix: `.md`
- Size bytes: `1741`
- SHA-256: `9fd4dccb552799ac9f0f33caf8517373c99f94bb3e36aed1fcae033d6e12c2b9`
- Content included: `True`
- Content truncated: `False`

```text
# Python Line Count CSV

- Passed: `True`
- CSV: `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260503-163724.csv`
- File count: `312`
- Total lines: `90309`
- Provider execution performed: `False`
- Patch application performed: `False`
- Source writes performed: `False`

## Largest Python files

- `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py` — `2197` lines
- `Tools/npu/run_dual_ai_pipeline.py` — `1773` lines
- `old script legacy/spaziotempo_asset_visual_v61.py` — `1513` lines
- `Scripting/v61b/scene_tuning_panel.py` — `1262` lines
- `Tools/workflow/workflow_state.py` — `1230` lines
- `Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py` — `1179` lines
- `old script legacy/spaziotempo_asset_visual_v6.py` — `1174` lines
- `Tools/ai/run_agent_gpu_deep_planning_supervised.py` — `1115` lines
- `Scripting/v61b_backgood/scene_tuning_panel.py` — `1097` lines
- `Scripting/v61b/animation.py` — `1079` lines
- `Scripting/v61b_backgood/animation.py` — `1019` lines
- `old script legacy/spaziotempo_album_visual_v5.py` — `969` lines
- `Tools/ai/run_agent_gpu_deep_planning_review.py` — `902` lines
- `Tools/workflow/gui/workflow_gui.py` — `738` lines
- `Scripting/v61b/physics_setup.py` — `737` lines
- `Scripting/v61b/asset_setup.py` — `725` lines
- `Scripting/v61b_backgood/asset_setup.py` — `725` lines
- `Tools/ai/build_refactor_duplication_audit.py` — `725` lines
- `Scripting/v61b_backgood/physics_setup.py` — `720` lines
- `Tools/ai/agent_runtime_tool_broker.py` — `715` lines

## Guardrail

This artifact is line-count evidence only. It is not a patch plan and it must not be committed from `output/**`.

```

## Selected chunks evidence

### `docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json`

- Exists: `True`
- JSON OK: `True`
- Kind: `selected_semantic_chunks_evidence`
- Passed: `True`
- Provider execution performed: `False`
- Source writes performed: `False`
- Selected count: `24`
- Total selected chars: `28649`
- Max total chars: `32000`
- Decision: `{'selected_chunks_built': True, 'budget_respected': True, 'provider_execution_seen': False, 'source_writes_performed': False, 'forbidden_paths_blocked': True}`

## Git push helper

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add local ai workflow evidence bundle"
git push
```
