# Heap Exchange Runtime Lifecycle Patch Bundle

## Purpose

Promote heap/exchange from a static validation edge to a runtime lifecycle around the dynamic center of the unified run.

The run remains code-driven and reuse-first:

- reuses `unified_run_observer.ps1` and `ai_public_events.jsonl`;
- reuses generated patch specs and the existing review-PR bridge;
- reuses `check_unified_chain_contract.py` for final product envelope validation;
- adds entry/exit lifecycle artifacts so the heap/exchange layer is present while provider/GPU/NPU/runtime lanes operate.

## Runtime model

```text
controlled entry
  -> heap/exchange runtime session
       center remains dynamic
       GPU0 / GPU1 / NPU / provider / official adapter / context lanes publish evidence
  -> controlled exit
       concrete deterministic product or hard failure
```

The lifecycle does not prescribe internal reasoning or lane order.

## Added tools

```text
Tools/ai/build_heap_exchange_runtime_entry.py
Tools/ai/build_heap_exchange_runtime_exit.py
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/ai/patch_unified_heap_exchange_lifecycle_wiring.py
```

## Local apply procedure

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git switch codex/heap-exchange-runtime-lifecycle
git pull --ff-only origin codex/heap-exchange-runtime-lifecycle

python -m Tools.ai patch_unified_heap_exchange_lifecycle_wiring `
  --repo-root . `
  --dry-run

python -m Tools.ai patch_unified_heap_exchange_lifecycle_wiring `
  --repo-root .
```

## Validation

```powershell
python -m py_compile `
  .\Tools\ai\build_heap_exchange_runtime_entry.py `
  .\Tools\ai\build_heap_exchange_runtime_exit.py `
  .\Tools\ai\patch_unified_heap_exchange_lifecycle_wiring.py `
  .\Tools\validation\check_heap_exchange_runtime_lifecycle.py `
  .\Tools\validation\run_heap_exchange_runtime_lifecycle_smoke.py

python -m Tools.validation run_heap_exchange_runtime_lifecycle_smoke `
  --repo-root .

$PsPath = "Tools/workflow/run_unified_local_ai_refactor.ps1"
$tokens = $null
$parseErrors = $null
$null = [System.Management.Automation.Language.Parser]::ParseFile(
  (Resolve-Path $PsPath).Path,
  [ref]$tokens,
  [ref]$parseErrors
)
if ($parseErrors.Count -gt 0) {
  $parseErrors | ForEach-Object { Write-Error $_.Message }
  throw "PowerShell parser failed"
} else {
  Write-Host "[OK] PowerShell parser passed"
}

Select-String `
  -Path .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Pattern "HEAP-EXCHANGE-RUNTIME|Build heap/exchange runtime entry|Build heap/exchange runtime exit product|Validate heap/exchange runtime lifecycle" `
  -Context 3,8

git diff --check
```

## Expected launcher phase placement

The codemod inserts:

1. `Build heap/exchange runtime entry` after `Build AI workload quality routing report`.
2. `Build heap/exchange runtime exit product` after `Apply generated patch specs for review PR`.
3. `Validate heap/exchange runtime lifecycle` before `Validate unified heap/exchange chain contract`.

## Expected failure class after wiring

If provider/GPU/NPU lanes run but no concrete patch product emerges, the run should fail at heap/exchange exit or lifecycle validation before producing a misleading review PR.

Expected failure example:

```text
heap/exchange exit has no concrete deterministic operation candidate
```

This is correct. It means the dynamic center was entered but did not produce concrete product.

## Commit scope

Do not commit runtime outputs.

Allowed product files for this PR:

```text
Tools/ai/build_heap_exchange_runtime_entry.py
Tools/ai/build_heap_exchange_runtime_exit.py
Tools/ai/patch_unified_heap_exchange_lifecycle_wiring.py
Tools/validation/check_heap_exchange_runtime_lifecycle.py
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/workflow/run_unified_local_ai_refactor.ps1
```

This documentation file may be committed as the patch bundle.
