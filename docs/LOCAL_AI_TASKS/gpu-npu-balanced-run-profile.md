# GPU/NPU Balanced Run Profile

## Purpose

Balanced profile proposal for complete local AI-to-AI runs when the GPU planner advances much faster than the NPU checkpoint auditor.

The goal is not perfect lockstep. The goal is useful NPU checkpoint coverage without blocking GPU progress or leaving NPU audits too stale.

## Reference run observation

Reference run:

```text
project_complete_20260502-195523
```

Observed behavior:

```text
GPU planner completed 24 rounds
NPU checkpoint auditor completed 5 audits
NPU audits succeeded
GPU output still ended with repair_attempt_failed
```

Interpretation:

```text
NPU is useful as a sampled checkpoint auditor, not as a per-round synchronous reviewer.
```

## Baseline complete-run parameters

Previous project-complete run used:

```text
--budget-minutes 30
--max-rounds 24
--files-per-round 10
--max-context-files 240
--max-chars-per-file 8000
--max-new-tokens 4800
--npu-auditor-every-rounds 4
--max-concurrent-npu-audits 1
--npu-auditor-timeout-seconds 600
--npu-max-context-chars 12000
--npu-max-prompt-chars 1500
--npu-max-new-tokens 512
--npu-final-wait-seconds 120
```

## Balanced profile candidate

Use this profile for the next comparative complete run after JSON-contract integration is available:

```text
--budget-minutes 30
--max-rounds 20
--files-per-round 8
--max-context-files 220
--max-chars-per-file 6000
--max-new-tokens 3600
--npu-auditor-every-rounds 3
--max-concurrent-npu-audits 1
--npu-auditor-timeout-seconds 420
--npu-max-context-chars 8000
--npu-max-prompt-chars 1200
--npu-max-new-tokens 384
--npu-final-wait-seconds 180
```

## Rationale

GPU-side changes:

```text
slightly smaller file batches
slightly smaller per-file context
lower max-new-tokens than 4800
fewer max rounds
```

Expected effect:

```text
less prompt echo pressure
less malformed long JSON
more compact GPU responses
less runaway round count
```

NPU-side changes:

```text
smaller context budget
smaller prompt budget
smaller decode budget
shorter per-audit timeout
longer final wait
```

Expected effect:

```text
faster NPU checkpoint completion
less chance that final NPU audits are still draining after GPU completion
better end-of-run audit inclusion
```

Cadence:

```text
npu-auditor-every-rounds 3
```

Expected effect:

```text
more frequent checkpoint coverage than every 4 rounds, while still avoiding per-round lockstep.
```

## Guardrails

```text
NPU remains non-blocking
NPU remains checkpoint/audit/support lane
NPU is not promoted to primary advisory
OpenVINO GPU is not used as primary lane
no provider/model setting changes first
no patch auto-apply
no source writes through patch runner
no Blender runtime execution
raw output/** remains local only
compact bundle remains required
```

## Required analysis tool

Use:

```powershell
python -m Tools.ai analyze_gpu_npu_run_sync `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_<STAMP>_orchestrator.json" `
  --output ".\output\analysis\gpu_npu_run_sync_<STAMP>.json" `
  --markdown-output ".\output\analysis\gpu_npu_run_sync_<STAMP>.md"
```

The sync analysis report must be included in the evidence bundle for any future complete run that changes GPU/NPU cadence parameters.

## Success criteria

A balanced run is better if:

```text
GPU JSON contract failures decrease
context_echo_detected is separated from raw parse failure
NPU audit success remains true
NPU audit coverage improves or remains useful
final bundle includes NPU audit evidence and sync analysis
fallback patch-plan remains available when GPU recommendations are empty
```
