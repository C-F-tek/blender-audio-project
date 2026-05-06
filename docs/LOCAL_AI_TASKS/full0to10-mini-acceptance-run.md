# Full0To10 mini acceptance run

## Purpose

This is the canonical small production-style acceptance procedure for a newly integrated local-AI capability.

It must be used when a tool/lane has moved beyond isolated implementation or smoke validation and must prove it is reachable from the active operator workflow.

## Rule

A capability is not production-integrated until it passes a mini complete run through the unified launcher.

Do not classify a capability as complete from only:

```text
module import success
unit-level helper success
isolated smoke command
manual one-off provider command
hidden script output
partial Mode selection
```

The acceptance proof must simulate a small but complete Full0To10 run.

## Required run shape

Use:

```text
-Full0To10
-RunIntensity quick
```

Do not pass a reduced `-Mode` list for production acceptance.

`quick` changes budget and capacity only. It does not reduce the Full0To10 semantic perimeter.

## Clean acceptance versus diagnostic runs

### Acceptance run

Use this when deciding whether a capability is integrated.

Required:

```text
working tree clean
provider-capable .venv preflight green when provider/GPU/NPU lanes matter
no -AllowDirty
no -DryRun
no phase-reducing -Mode list
no -No* disabler for the lane under test
no stale generated evidence in docs/LOCAL_VALIDATION_EVIDENCE from previous failed attempts
no modified generated indexAI/code_chunks files
```

A failed or partial prior run must be parked before rerunning acceptance. Do not let stale evidence make the next acceptance dirty before it starts.

### Branch-safety controls for PR acceptance

When validating a PR-only capability, the mini acceptance run must stay on the PR head or a branch created from the PR head.

These flags are allowed for PR acceptance because they protect the tested code from being replaced by `master`:

```text
-SkipGitSync
-NoBranch
```

They are branch-safety controls, not capability bypasses.

Use them when the default launcher branch workflow would switch away from the current PR branch before executing the new capability.

### Capability bypasses

These are not allowed for production acceptance of the lane under test:

```text
-AllowDirty
-DryRun
partial -Mode lists
-No* flags that disable the lane under test
isolated smoke commands as the only proof
```

They can be useful for diagnosis, but the result must be classified as non-production evidence.

### Diagnostic run

Use this only while developing or debugging a patch.

Allowed only as non-production evidence:

```text
-AllowDirty
-Prod
-NoExecutionTail
partial -Mode lists
isolated smoke commands
```

A diagnostic run can explain a failure or validate a narrow fix, but it is not acceptance evidence.

## Pre-run cleanup for failed prior attempts

If a previous mini acceptance attempt created compact evidence and then failed, park it before the next acceptance run unless you are deliberately committing it as failed evidence.

Use the failed stamp:

```powershell
$FailedStamp = "gpu0_full0to10_quick_YYYYMMDD-HHMMSS"
$Park = ".\output\validation\parked_partial_diagnostic_$FailedStamp"
New-Item -ItemType Directory -Force -Path $Park | Out-Null

Get-ChildItem .\docs\LOCAL_VALIDATION_EVIDENCE -Force |
  Where-Object { $_.Name -match [regex]::Escape($FailedStamp) } |
  ForEach-Object { Move-Item -LiteralPath $_.FullName -Destination $Park -Force }
```

Generated index files must not make the acceptance dirty:

```powershell
git restore .\indexAI\code_chunks\semantic_code_chunks.json
git restore .\indexAI\code_chunks\semantic_code_chunks_manifest.json
```

Then verify:

```powershell
git status --short
```

Acceptance should start from a clean working tree.

## Provider-capable .venv preflight

Before any provider/OpenVINO/GPU0/NPU acceptance run:

```powershell
$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"

& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"
```

Required packages for OpenVINO/GPU0/NPU lanes:

```text
numpy
openvino
openvino-genai
```

Expected IA-Carmine workstation device visibility:

```text
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

Missing packages are `provider_python_environment_missing_dependency`, not GPU0/NPU failure.

If imports pass but `GPU.0` is not visible, classify as OpenVINO device/runtime visibility failure.

`GPU.1` may be visible through OpenVINO but remains reserved for CUDA/Ollama and must not receive OpenVINO workload.

## Canonical mini acceptance commands

### PR-branch acceptance command

Use this when validating code that exists only on the PR branch.

From repository root, after `git status --short` is clean and the current branch is the PR branch:

```powershell
$Stamp = "mini_acceptance_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Stamp $Stamp `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b `
  -OfficialAdapterTimeoutSeconds 1800 `
  -SkipGitSync `
  -NoBranch `
  -Prod
```

Do not add `-Mode official,contract,full_validation` for acceptance. That is a partial diagnostic run.

### Mainline acceptance command

Use this only when the tested capability already exists on the branch the launcher would normally select.

```powershell
$Stamp = "mini_acceptance_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$env:IA_CARMINE_PYTHON = "<repo>\.venv\Scripts\python.exe"
$env:PYTHONPATH = "<repo>"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Stamp $Stamp `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b `
  -OfficialAdapterTimeoutSeconds 1800 `
  -Prod
```

If this switches away from the tested branch and loses the capability under test, the result is `blocked_launcher_branch_management`.

## Required acceptance outputs

The mini acceptance run must produce or explicitly classify these surfaces:

```text
unified_local_ai_refactor_manifest.json
phase_status entries
phase_reports entries
report_files entries
Markdown inventory/report output
JSON/report contract output
Python/script inventory output
semantic chunk manifest or explicit unavailable/degraded classification
context pack output
agent-state or memory handoff output, unless explicitly disabled
provider diagnostics when provider lanes are selected
OpenVINO GPU0 workload JSON/MD when GPU0 lane is selected
workload quality routing output when provider/Full0To10 is selected
patch-spec output when patch specs are selected
compact evidence bundle/summary
runtime tool usage telemetry JSON/MD
runtime tool capability manifest JSON/MD
full toolbox run telemetry summary JSON/MD
shared AI-to-AI bundle JSON/MD
full validation status
shared AI-to-AI bundle summary or explicit unavailable/degraded classification
```

Missing surfaces are acceptable only when one of these is recorded in manifest, phase reports, telemetry or validator output:

```text
explicit -No* disabler
unavailable tool
provider failure
degraded runtime dependency
operator-documented exclusion
```

Provider warnings are not ignorable in Full0To10. They must be visible as warnings, degraded state or failure in manifest/phase reports/telemetry/contract outputs.

Examples that require explicit classification:

```text
Generate provider workload probe inputs failed with exit code 2
Ollama probe did not pass
Primary advisory provider execution requested: False
Ollama advisory execution used: False
GPU0 lane did not run
```

## Bundle and telemetry requirement

The acceptance evidence must preserve all compact telemetry surfaces produced under `docs/LOCAL_VALIDATION_EVIDENCE`.

Include compact JSON/Markdown evidence for:

```text
full_memory_tool_regeneration_bundle
full_toolbox_agent_review_decision_loop
full_toolbox_run_telemetry_summary
runtime_tool_usage_telemetry
runtime_tool_capability_manifest
shared_toolbox_ai_to_ai_bundle
provider/GPU0 evidence when produced
```

Do not commit:

```text
output/**
indexAI/code_chunks/**
*.db
*.sqlite
large deterministic chunk folders with path-length risk
```

If cloud semantic deterministic chunks are generated as a folder, commit only the compact manifest unless the task explicitly approves those chunks and their paths are safe.

## GPU0-specific acceptance checks

When validating OpenVINO GPU0 integration, inspect:

```powershell
Get-ChildItem .\output\validation -Filter "openvino_gpu0_workload_$Stamp.json" -File

Get-Content ".\output\validation\openvino_gpu0_workload_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, provider_execution_performed, openvino_gpu0_visible, openvino_gpu0_workload_performed, openvino_gpu0_workload_passed, openvino_gpu1_reserved_visible, openvino_gpu1_workload_performed, selected_device, errors, warnings
```

Expected GPU0 acceptance state:

```text
passed=True
provider_execution_performed=True
openvino_gpu0_visible=True
openvino_gpu0_workload_performed=True
openvino_gpu0_workload_passed=True
openvino_gpu1_workload_performed=False
selected_device=GPU.0
```

Resource Monitor showing `0%` GPU usage is not enough to prove GPU0 failure for the current micro workload because it may complete between samples.

However, if the production advisory/provider flow never calls GPU0 as a support lane, that must be classified as `gpu0_support_lane_not_integrated`, not accepted as Full0To10 production integration.

A future sustained GPU0 workload may be added to make resource-level monitoring visible, but that is separate from the routing/evidence acceptance check.

## Manifest inspection

Find the manifest for the stamp:

```powershell
$Manifest = Get-ChildItem .\output\local_ai_runs -Recurse -Filter "unified_local_ai_refactor_manifest.json" |
  Where-Object { $_.FullName -match [regex]::Escape($Stamp) } |
  Select-Object -First 1

$M = Get-Content $Manifest.FullName -Raw | ConvertFrom-Json
$M.full_0_to_10_requested
$M.run_intensity
$M.phase_status
$M.phase_reports
$M.report_files
$M.warnings
$M.errors
```

The manifest must show `full_0_to_10_requested=True`, `run_intensity=quick`, and visible phase/evidence surfaces for the new capability.


## Production provider support hardening

For GPU0/provider work, acceptance is not satisfied by a final isolated micro workload alone.

A valid Full0To10 quick acceptance must now include:

```text
OpenVINO GPU0 provider support lane before or inside provider/advisory flow
sustained GPU0 workload evidence with production_support=true
full0to10_provider_acceptance JSON/MD gate
provider warnings promoted to classifications
```

The provider acceptance gate must classify and fail/degrade the run when it sees:

```text
provider_lane_degraded
ollama_probe_failed
primary_advisory_not_executed
blocked_missing_refined_review_input
gpu0_support_lane_not_integrated
gpu0_sustained_workload_not_performed
```

GPU0 Resource Monitor staying at 0% during provider/advisory phases is an operator-visible warning. It is not the sole proof of failure, but it requires checking the provider support lane report and the provider acceptance gate.

Expected new report files:

```text
output/validation/openvino_gpu0_provider_support_<stamp>.json
output/validation/openvino_gpu0_provider_support_<stamp>.md
output/validation/full0to10_provider_acceptance_<stamp>.json
output/validation/full0to10_provider_acceptance_<stamp>.md
```

The final compact bundle must include telemetry surfaces:

```text
runtime_tool_usage_telemetry
runtime_tool_capability_manifest
full_toolbox_run_telemetry_summary
shared_toolbox_ai_to_ai_bundle
full0to10_provider_acceptance
OpenVINO GPU0 provider/final workload evidence
```

## GPU0 companion worker principle

GPU0 is not a passive accelerator, smoke target or final evidence-only lane.

In IA-Carmine production workflows, GPU0 must be treated as a peer/companion worker:

```text
GPU1 / Ollama = primary planner
GPU0 / OpenVINO = companion worker
NPU = auditor / reviewer
runtime tool broker = controlled tool execution layer
```

The GPU0 companion worker can receive bounded task packets, produce compact JSON/Markdown evidence, request tools through the runtime broker contract, and feed its report back into GPU1/Ollama and NPU audit lanes as `--report-file` context.

A capability is not production-integrated when GPU0 only performs preflight, isolated smoke, or final workload evidence. For Full0To10 acceptance, GPU0 companion evidence must be visible through workflow reports, provider gates, runtime telemetry, bundle/handoff surfaces, or an explicit degraded/unavailable classification.

This principle applies to provider, advisory, audit, broker, memory, evidence and patch-plan lanes.\n\n## Result classification

Use these labels consistently:

```text
accepted_mini_full0to10
failed_mini_full0to10
blocked_dirty_worktree
blocked_provider_python_environment_missing_dependency
blocked_openvino_device_visibility
blocked_launcher_branch_management
provider_lane_degraded
primary_advisory_not_executed
ollama_probe_failed
gpu0_not_reached
gpu0_support_lane_not_integrated
partial_diagnostic_only
```

Only `accepted_mini_full0to10` can be used to claim production integration.
