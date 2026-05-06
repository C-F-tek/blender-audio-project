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
```

Git branch/sync behavior must follow the active runbook for the current task. If local branch switching would be unsafe, fix the launcher/task branch configuration before claiming production acceptance.

### Diagnostic run

Use this only while developing or debugging a patch.

Allowed only as non-production evidence:

```text
-AllowDirty
-SkipGitSync
-NoBranch
-Prod
-NoExecutionTail
partial -Mode lists
isolated smoke commands
```

A diagnostic run can explain a failure or validate a narrow fix, but it is not acceptance evidence.

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

## Canonical mini acceptance command

From repository root, after `git status --short` is clean:

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

Do not add `-Mode official,contract,full_validation` for acceptance. That is a partial diagnostic run.

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
```

The manifest must show `full_0_to_10_requested=True`, `run_intensity=quick`, and visible phase/evidence surfaces for the new capability.

## Result classification

Use these labels consistently:

```text
accepted_mini_full0to10
failed_mini_full0to10
blocked_dirty_worktree
blocked_provider_python_environment_missing_dependency
blocked_openvino_device_visibility
blocked_launcher_branch_management
partial_diagnostic_only
```

Only `accepted_mini_full0to10` can be used to claim production integration.
