# Next Chat Handoff — GPU peer-exchange code continuation — 2026-05-06

## Repository

```text
C-F-tek/blender-audio-project
```

Active branch:

```text
codex/md-bundle-telemetry-refactor
```

## Mode

Resume from the code/integration work that was active before the MD-only coherence pass.

Default mode:

```text
GitHub/API first
local commands only when explicitly requested or for operator validation
no merge to master
no force-push
no history rewrite
no deploy
no secret/permission/billing/visibility changes
no Blender runtime
no FFmpeg runtime
no raw output/** commit
no indexAI/code_chunks/** commit
no *.db / *.sqlite commit
```

When touching code/scripts, always report resulting line count.

## Current doctrine

Local AI lanes are not isolated providers.

Canonical production roles:

```text
GPU1 / Ollama / RTX 5080 = mandatory primary advisory planner
GPU0 / OpenVINO = companion peer worker
NPU = micro-fast task assistant and lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
runtime tool broker = controlled tool execution for GPU1 and GPU0 requests
```

Primary reference:

```text
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
```

## Code state before MD-only pass

The previous code work promoted GPU0 from isolated workload evidence toward a companion lane.

Implemented/validated locally before the MD-only pass:

```text
Tools/ai/build_gpu0_companion_task_lane.py
Tools/validation/check_gpu0_companion_contract.py
Tools/validation/check_full0to10_provider_acceptance.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/ai/build_openvino_gpu0_workload_report.py
Tools/ai/runtime_hardware_capability/workloads.py
Tools/ai/build_agent_review_evidence_sufficiency.py
AGENTS.md
docs/LOCAL_AI_TASKS/full0to10-mini-acceptance-run.md
```

Hotfixes applied locally during that work fixed:

```text
AGENTS.md accidental truncation risk
GPU0 companion contract path resolution
literal backslash-n JSON writer bug
provider gate evidence missing gpu0_companion_lane
late provider gate after final GPU0 workload
GPU0 provider support metadata serialization
```

Important: verify whether this code patch is already committed/pushed locally. A later `git commit` attempt reported `nothing added to commit` except one untracked line-count CSV, which suggests the code patch may already be in HEAD or had been committed earlier. Confirm with marker checks below before reapplying anything.

## Last meaningful acceptance run

Run stamp:

```text
gpu0_companion_full0to10_quick_20260506-191903
```

Observed result:

```text
Full toolbox decision loop: Passed=False
Integrated warning policy: Passed=True
Provider acceptance gate: exit code 2
Final OpenVINO GPU0 workload: passed=True
```

Interpretation:

```text
GPU0 workload works
GPU0 companion/report lane exists
provider gates can see companion evidence
but real AI peer-exchange is still missing
```

Current correct classification:

```text
failed_full0to10_provider_acceptance
gpu0_final_workload_passed
gpu0_companion_static_or_report_only
gpu1_primary_advisory_not_proven
gpu1_gpu0_peer_exchange_missing
gpu0_tool_requests_not_broker_consumed
npu_micro_task_switch_not_integrated
```

Do not keep rerunning the same acceptance as the final proof until peer exchange is implemented.

## Next code target

Implement:

```text
feat(ai): add AI peer-exchange lane
```

Required behavior:

```text
GPU1/Ollama/RTX5080 primary advisory executes for real Full0To10 runs unless explicitly disabled or classified degraded.
GPU1 writes bounded task packets for GPU0.
GPU0 companion worker reads task packets and emits response/evidence packets.
GPU0 may use OpenVINO GenAI on GPU.0 when IA_CARMINE_GPU0_COMPANION_MODEL_DIR is configured.
GPU0 may fallback to numeric/tool/report-only response when no semantic model is configured, but must classify the fallback.
Runtime tool broker may consume tool requests from GPU1 and GPU0.
NPU receives GPU1/GPU0 context only for micro-fast support/checkpoint tasks.
Heavy audit remains deterministic script-owned.
Orchestrator records roundtrip, timings, execution counts, failures, classifications, telemetry and bundle evidence.
```

Expected new or updated artifacts:

```text
Tools/ai/build_ai_peer_exchange_packet.py
Tools/ai/run_gpu0_peer_companion_worker.py
Tools/validation/check_ai_peer_exchange_contract.py
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/validation/check_full0to10_provider_acceptance.py
```

Expected evidence surfaces:

```text
gpu1_primary_advisory_<stamp>.json/md
gpu0_peer_task_packet_<stamp>.json
gpu0_peer_response_<stamp>.json/md
gpu0_tool_requests_<stamp>.json
ai_peer_exchange_<stamp>.json/md
provider acceptance gate with peer-exchange classifications
runtime telemetry and final bundle inclusion
```

## Marker checks before coding

Run locally after syncing:

```powershell
git status --short

git ls-files `
  .\Tools\ai\build_gpu0_companion_task_lane.py `
  .\Tools\validation\check_gpu0_companion_contract.py

Select-String -Path .\AGENTS.md `
  -Pattern "GPU0 companion worker principle|GPU1 / Ollama / RTX 5080|Markdown coherence policy"

Select-String -Path .\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1 `
  -Pattern "GPU0 companion|Gpu0Companion|gpu0_companion"

Select-String -Path .\Tools\validation\check_full0to10_provider_acceptance.py `
  -Pattern "gpu0_companion_lane|companion_evidence_required|schema_version|gpu0_peer"
```

If marker checks pass and status is clean, continue with peer-exchange implementation. If markers are missing, inspect recent commits before reapplying patches.

## Local environment preflight

Provider-capable Python must be visible before GPU0/NPU/Full0To10 validation:

```powershell
$env:IA_CARMINE_PYTHON = "C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe"
$env:PYTHONPATH = "C:\Users\carmi\blender\blender-audio-project"

& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"
```

Expected device list on the IA-Carmine workstation:

```text
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

GPU.1 is RTX 5080/Ollama primary lane. Do not assign OpenVINO workload to GPU.1.

## MD-only pass after code work

After the GPU0 companion work, a GitHub-only MD coherence pass was performed. It added/updated docs and created issue `#195` for future Markdown split/pruning follow-up. It also closed issue `#57` as completed.

## 2026-05-07 PR194 continuation note

The next runtime-heap continuation should treat commit `bcabedf` as the baseline and keep the peer-exchange production chain focused on small parser-safe integrations, not a broad PowerShell-to-Python migration.

Current intended production wiring:

```text
GPU1/Ollama primary advisory
  -> live provider runtime heap init
  -> GPU1->GPU0 live evidence request
  -> GPU0 peer response
  -> GPU0 broker live results
  -> NPU micro support signal
  -> provider runtime heap telemetry
  -> full toolbox telemetry, shared bundle and compact evidence
```

Line-count CSV evidence is part of the compact evidence surface. The workflow should preserve generated `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_*.csv` files when they appear in `evidence_to_commit`, and bundle builders should discover CSV side artifacts declared by JSON reports.

NPU micro support is bounded separately from heavy NPU audit waits. It remains non-blocking and support-only; deterministic scripts remain the heavy audit authority.

New/current docs to preserve:

```text
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
docs/LOCAL_AI_TASKS/md-coherence-only-github-pass-2026-05-06.md
docs/AI_SESSION_NOTES/2026-05-06-gpu1-primary-gpu0-companion-peer-exchange.md
docs/AI_SESSION_NOTES/2026-05-06-md-coherence-github-only-pass.md
CHATGPT/next-chat-handoff-gpu-peer-exchange-code-continuation-2026-05-06.md
```

Markdown policy now:

```text
active maintained .md hard threshold <= 500 lines
preferred active runbook <= 400 lines
maintained code/script file <= 400 lines
```

## Validation after peer-exchange patch

Minimum local validation:

```powershell
$env:IA_CARMINE_PYTHON = "C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe"
$env:PYTHONPATH = "C:\Users\carmi\blender\blender-audio-project"

& $env:IA_CARMINE_PYTHON -m py_compile `
  .\Tools\ai\build_ai_peer_exchange_packet.py `
  .\Tools\ai\run_gpu0_peer_companion_worker.py `
  .\Tools\validation\check_ai_peer_exchange_contract.py `
  .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py

# focused contract smoke once implemented
& $env:IA_CARMINE_PYTHON .\Tools\validation\check_ai_peer_exchange_contract.py --help

git diff --check
```

Then run a small full perimeter acceptance, not a reduced-scope smoke:

```powershell
$Stamp = "gpu_peer_exchange_full0to10_quick_$(Get-Date -Format 'yyyyMMdd-HHmmss')"

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

Acceptance should fail explicitly if primary advisory, peer exchange, broker consumption or companion response is missing. Silent downgrade is not acceptable.
