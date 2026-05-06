# Full0To10 foundation report-only patch — bundle completeness, memory visibility, hardware contracts

## Status

Patch foundation report-only.

This document is intentionally compact. It does not replace the unified launcher runbook.

## Scope

This patch family adds small modular tools for:

```text
recursive Full0To10 evidence ZIP bundle creation
bundle completeness validation
runtime hardware capability manifest for CPU/GPU0/NPU/NVIDIA
hardware/delegation report-only contract validation
```

## Non-goals

```text
no Blender runtime
no FFmpeg runtime
no provider generation
no patch-spec apply
no source writes outside these tool/doc files
no SQLite DB commit
no output/** commit
no autonomous NPU/GPU0 worker
```

## Commands

Build recursive evidence ZIP for a run stamp:

```powershell
python .\Tools\ai\build_full_run_evidence_bundle_zip.py `
  --repo-root . `
  --stamp 20260505-193057 `
  --basename ia_carmine_full0to10_complete_bundle_20260505-193057
```

Validate the produced ZIP and completeness sidecar:

```powershell
python .\Tools\validation\check_full_run_bundle_completeness.py `
  --repo-root . `
  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\ia_carmine_full0to10_complete_bundle_20260505-193057.zip `
  --completeness-report .\docs\LOCAL_VALIDATION_EVIDENCE\ia_carmine_full0to10_complete_bundle_20260505-193057_bundle_completeness_report.json `
  --output .\output\validation\full0to10_bundle_completeness_validation_20260505-193057.json
```

Build report-only hardware capability manifest:

```powershell
python .\Tools\ai\build_runtime_hardware_capability_manifest.py `
  --repo-root . `
  --output .\output\validation\runtime_hardware_capability_manifest.json `
  --markdown-output .\output\validation\runtime_hardware_capability_manifest.md
```

Validate report-only hardware/delegation contract:

```powershell
python .\Tools\validation\check_runtime_hardware_delegation_contract.py `
  --repo-root . `
  --hardware-manifest .\output\validation\runtime_hardware_capability_manifest.json `
  --output .\output\validation\runtime_hardware_delegation_contract_validation.json
```

## Bundle completeness rule

The builder includes stamped compact evidence files and recursively includes required evidence directories such as:

```text
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunks/
```

If that directory exists and is required for review, it must not be replaced by only a manifest.

## Hardware contract rule

The first hardware manifest is report-only.

It may detect resources, but it must not run generated-provider workloads.

Expected resources in the manifest:

```text
CPU
GPU.0
NPU
NVIDIA_GPU
```

GPU0 and NPU may be unavailable on a specific host, but the resources must be visible as capability entries with explicit status.

## Line-count design

The implementation is intentionally split into small modules:

```text
Tools/ai/full_run_bundle_zip/
Tools/ai/runtime_hardware_capability/
Tools/validation/full_run_bundle_completeness.py
Tools/validation/runtime_hardware_delegation_checks.py
```

Entrypoints are thin wrappers.


## Direct execution contract

The thin entrypoints bootstrap the repository root into `sys.path`.

They can be executed directly from the repository root without pre-setting `PYTHONPATH`:

```powershell
python .\Tools\ai\build_runtime_hardware_capability_manifest.py `
  --repo-root . `
  --output .\output\validation\runtime_hardware_capability_manifest.json `
  --markdown-output .\output\validation\runtime_hardware_capability_manifest.md

python .\Tools\validation\check_runtime_hardware_delegation_contract.py `
  --repo-root . `
  --hardware-manifest .\output\validation\runtime_hardware_capability_manifest.json `
  --output .\output\validation\runtime_hardware_delegation_contract_validation.json
```

This is required because direct script execution puts the script directory on `sys.path`, not the repository root.
