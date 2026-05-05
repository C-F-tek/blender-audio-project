<!-- IA-CARMINE-MD-SPLIT: part -->
# full-toolbox-0-to-10-semi-automatic-procedure — parte 001 di 004

Sorgente indice: [`../full-toolbox-0-to-10-semi-automatic-procedure.md`](../full-toolbox-0-to-10-semi-automatic-procedure.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# IA-Carmine Full Toolbox 0 -> 10 Semi-Automatic Procedure

## Purpose
## Root launcher reference

Canonical full-run launcher variable reference:

    FULL_RUN_UNICA_TUTTO_SU_TUTTO.md

This root document contains the complete TUTTO SU TUTTO launcher variable inventory, canonical single-script run command, output-dir naming rule, and current run evidence for provider workload probe / workload-quality routing failures.


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

Current full-run policy: TUTTO SU TUTTO.

In the canonical full run, memory lanes are active when the launcher supports them. This includes input persistence / memory reload / runtime memory evidence lanes unless an explicit `-NoMemoryWrite` maintenance flag is supplied.

Expected current full toolbox reporting:

```text
memory lanes active by default in full real runs
sqlite_write_performed and persistent_memory_write_performed must be reported truthfully
no silent memory write is allowed outside the declared memory lane
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



### Global DataStamp and AI packets contract

Every unified launcher run must resolve one timestamp only. The run stamp is the single global version key for all run-scoped folders introduced by this contract.

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$DataStamp = $Stamp
```

The run-scoped AI packets directory is:

```powershell
$AiPacketsRoot = ".\output\ai_packets"
$AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp
```

Contract:

```text
output/ai_packets/<DataStamp> is the run packet directory.
It is a directory, not a context file.
Never pass output/ai_packets/<DataStamp> as -ExtraContextFile.
Only concrete files inside the directory may be used as context/report inputs.
```

Allowed packet files include:

```text
output/ai_packets/<DataStamp>/npu_real_workload_report.md
output/ai_packets/<DataStamp>/ollama_gpu_real_workload_report.md
```

The workload-quality gate must receive the directory through:

```powershell
--report-dir $AiPacketsDir
```

The official/local advisory context must receive only concrete files. Before passing `-ExtraContextFile`, sanitize context inputs:

```powershell
$ContextFiles = @($ContextFiles | Where-Object {
    $ContextPath = [string]$_
    -not (Test-Path -LiteralPath $ContextPath -PathType Container)
})
```

Git policy remains unchanged:

```text
Do not commit output/**.
Commit only source, docs, tests, and compact evidence explicitly listed by evidence_to_commit.
```
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
