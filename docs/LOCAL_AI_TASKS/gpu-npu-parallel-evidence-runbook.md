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

## Purpose

Use the local machine as a controlled multi-lane AI system:

```text
CPU orchestration
GPU/Ollama planner
NPU/OpenVINO checkpoint auditor
Git-trackable evidence bundle
master-AI review before any patch
```

The current diagnostic focus is:

```text
GPU/Ollama can complete many planning rounds but produce zero recommendations.
NPU/OpenVINO audits selected checkpoints successfully.
The fallback patch-plan layer can still produce manual-review patch candidates from evidence sufficiency.
```

## Guardrails

```text
Do not apply patches automatically.
Do not commit output/**.
Do not commit SQLite databases.
Do not run Blender.
Do not promote NPU output to primary advisory.
Do not make OpenVINO GPU a primary advisory lane.
Do not change provider/model settings unless explicitly requested.
Do not create or merge a real PR unless explicitly requested by the human/master AI.
```

Provider execution must be explicit. Report-only tools should keep:

```text
patch_application_performed: false
source_writes_performed: false
manual_review_required: true
```

## Required input artifacts

Before running the full GPU/NPU parallel workflow, these local reports should exist:

```text
output/ai_pipeline/agent_review_evidence_sufficiency.json
output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json
output/ai_pipeline/local_ai_core_tool_activation_agent_memory_inventory.json
output/ai_pipeline/local_ai_core_tool_activation_agnostic_tool_inventory.json
output/ai_pipeline/local_ai_core_tool_activation_transient_request_context.json
output/ai_packets/gpu_planner_nonempty_recommendations_advisory_manifest.json
output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json
```

The first two are the core planning inputs:

```text
agent_review_evidence_sufficiency.json
  tells whether there is enough evidence for manual-review patch candidates.

local_ai_core_tool_activation_megalithic_refined_review_v3.json
  contains refined doc/code/doc-doc/code-code findings after noise reduction.
```

The `report-file` inputs enrich the planner context with memory/tool/transient/advisory state.

## Optional NPU provider preflight

Before a live NPU run, check the dedicated NPU Python environment:

```powershell
$NpuPy = "$HOME\blender\venvs\blender-npu-ai\Scripts\python.exe"

& $NpuPy -c "import sys; print(sys.executable); import openvino; print('openvino OK'); import openvino_genai; print('openvino_genai OK')"
& $NpuPy -c "import openvino as ov; print(ov.Core().available_devices)"
```

Expected output pattern:

```text
openvino OK
openvino_genai OK
['CPU', 'GPU.0', 'GPU.1', 'NPU']
```

Naming rule:

```text
Python import module: openvino_genai
PyPI package name: openvino-genai
```

The project-owned preflight is preferred when available:

```powershell
python .\Tools\ai\check_npu_provider_environment.py `
  --repo-root . `
  --output .\output\validation\npu_provider_environment.json `
  --markdown-output .\output\validation\npu_provider_environment.md
```

Expected report fields:

```text
passed: true
checks.openvino_import: true
checks.openvino_genai_import: true
checks.npu_available: true
decision.npu_ready_for_auditor: true
provider_execution_performed: false
patch_application_performed: false
```

## Full GPU/NPU parallel run

Use this command for the diagnostic run used by the current evidence bundle:

```powershell
python .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py `
  --repo-root . `
  --budget-minutes 30 `
  --max-rounds 24 `
  --files-per-round 10 `
  --max-context-files 240 `
  --max-chars-per-file 8000 `
  --max-new-tokens 4800 `
  --keep-alive 35m `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --refined-review .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review_v3.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agent_memory_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agnostic_tool_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_transient_request_context.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --context-root docs `
  --context-root Tools\ai `
  --context-root Tools\validation `
  --context-root Tools\workflow `
  --run-npu-auditor-provider `
  --npu-auditor-every-rounds 4 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 600 `
  --npu-max-context-chars 12000 `
  --npu-max-prompt-chars 1500 `
  --npu-max-new-tokens 512 `
  --npu-final-wait-seconds 120 `
  --checkpoint-dir .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_checkpoints `
  --gpu-output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_parallel_gpu.json `
  --gpu-markdown-output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_parallel_gpu.md `
  --output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --markdown-output .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.md
```

### Expected behavior

The orchestrator should behave as follows:

```text
GPU/Ollama process runs continuously and writes round checkpoints.
NPU/OpenVINO audits selected checkpoints in parallel.
GPU review must not be blocked by NPU audit latency.
CPU joins the final report.
```

Healthy output should include:

```text
passed: true
gpu_returncode: 0
gpu_round_count > 0
npu_audit_count >= 1
npu_audit_success_count >= 1
gpu_review_blocked_by_npu: false
patch_application_performed: false
```

For this specific diagnostic family, it is acceptable and expected that the GPU report may still show:

```text
gpu_recommendation_count: 0
```

That is the problem under investigation, not proof that the full run failed.

## Inspect the full run output

After the run, inspect the orchestrator report:

```powershell
$orch = Get-Content .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json -Raw | ConvertFrom-Json

$orch |
  Select-Object kind, passed, provider_execution_performed, patch_application_performed, elapsed_seconds, gpu_returncode, npu_audit_count, npu_audit_success_count

$orch.gpu_summary
$orch.decision

$orch.npu_audits |
  Select-Object round, status, classification, provider_execution_requested, provider_load_attempted, provider_execution_succeeded, provider_execution_performed, dependency_missing, gpu_review_blocked, warnings |
  Format-List
```

Inspect the GPU report selected by the orchestrator:

```powershell
$GpuReport = $orch.gpu_output
$gpu = Get-Content $GpuReport -Raw | ConvertFrom-Json

$gpu |
  Select-Object kind, passed, round_count, recommendation_count

$gpu.decision
$gpu.rounds |
  Select-Object round, status, json_ok, recommendation_count, parse_error, empty_recommendations_reason |
  Format-Table -AutoSize
```

## Post-validation AI packet

Use the project-owned post-validation AI packet, not a manual ZIP, to produce advisory/proposal files from selected context and report files.

First resolve the GPU report path:

```powershell
$par = Get-Content .\output\ai_pipeline\agent_gpu_npu_parallel_orchestrator_live.json -Raw | ConvertFrom-Json
$GpuReport = $par.gpu_output
$GpuReport
```

If using the diagnostic orchestrator output from this runbook, use:

```powershell
$par = Get-Content .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json -Raw | ConvertFrom-Json
$GpuReport = $par.gpu_output
$GpuReport
```

Then pass arrays, not repeated PowerShell parameters:

```powershell
$ContextFiles = @(
  ".\docs\LOCAL_AI_TASKS\improve-gpu-planner-nonempty-recommendations.md",
  ".\Tools\ai\run_agent_gpu_deep_planning_review.py",
  ".\Tools\ai\run_agent_gpu_deep_planning_supervised.py",
  ".\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py",
  ".\Tools\ai\build_agent_review_patch_plan.py"
)

$ReportFiles = @(
  ".\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json",
  $GpuReport
)

$params = @{
  Profile     = "core"
  ContextFile = $ContextFiles
  ReportFile  = $ReportFiles
}

& .\Tools\workflow\run_post_validation_ai_packet.ps1 @params
```

Expected output files include:

```text
output/ai_packets/gpu_planner_nonempty_recommendations_advisory.json
output/ai_packets/gpu_planner_nonempty_recommendations_advisory.md
output/ai_packets/gpu_planner_nonempty_recommendations_advisory_manifest.json
output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json
output/ai_packets/gpu_planner_nonempty_recommendations_proposals.md
output/ai_pipeline/repository_change_proposals.json
output/ai_pipeline/repository_change_proposals.md
```

## Patch-plan fallback layer

When the GPU planner returns zero recommendations but evidence sufficiency says candidates are ready, use the patch-plan builder as the deterministic/manual-review fallback layer.

Typical command:

```powershell
python .\Tools\ai\build_agent_review_patch_plan.py `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output .\output\patch_specs\agent_review_patch_plan.json `
  --markdown-output .\output\patch_specs\agent_review_patch_plan.md
```

Expected behavior:

```text
manual_review_only
patch_application_performed: false
fallback_used: true when GPU recommendations are empty and evidence candidates exist
```

Validate it:

```powershell
python .\Tools\validation\run_agent_review_patch_plan_smoke.py `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output .\output\validation\agent_review_patch_plan_smoke.json `
  --markdown-output .\output\validation\agent_review_patch_plan_smoke.md
```

## Git-trackable evidence bundle procedure

Do not upload or commit raw `output/**` reports directly.

The project-owned evidence flow is:

```text
build_github_evidence_bundle.py
→ docs/LOCAL_VALIDATION_EVIDENCE/*.json/*.md
→ check_github_evidence_bundle.py
→ git add only compact evidence docs
→ commit/push
```

Build the compact evidence bundle:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename gpu_planner_nonempty_recommendations_evidence `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json `
  --report .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --report .\output\patch_specs\agent_review_patch_plan.json `
  --report .\output\validation\agent_review_patch_plan_full_validation.json `
  --report .\output\validation\agent_review_patch_plan_smoke.json `
  --report .\output\validation\validation_report_contract.json `
  --report .\output\ai_pipeline\repository_change_proposals.json `
  --report .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --report .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_parallel_gpu.json
```

Expected Git-trackable outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Validate the evidence bundle:

```powershell
python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.json `
  --output .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json
```

Inspect validation:

```powershell
Get-Content .\output\validation\gpu_planner_nonempty_recommendations_evidence_validation.json -Raw |
  ConvertFrom-Json |
  Select-Object kind, passed, bundle_count, errors, warnings
```

## Final validation before push

Run standard validation:

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
git status --short
```

Only Git-trackable compact evidence should be staged for an evidence-only update:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Commit and push:

```powershell
git add `
  .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.json `
  .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_nonempty_recommendations_evidence.md

git commit -m "test(ai): add gpu planner nonempty recommendations evidence bundle"

git push -u origin codex/improve-gpu-planner-nonempty-recommendations
```

## Review of the initial problem

The initial problem is not that the GPU/NPU full run fails. The full run can be healthy while still exposing a planning-quality issue.

Observed state:

```text
orchestrator passed
GPU/Ollama completed many rounds
NPU/OpenVINO audits were usable and non-blocking
patch_application_performed was false
GPU recommendation_count was 0
agent_review_evidence_sufficiency had ready manual-review candidates
patch-plan fallback generated candidates
```

Interpretation:

```text
The infrastructure works.
The GPU planner needs better diagnostics and/or stricter output contract enforcement.
The fallback patch-plan layer is currently required to convert evidence sufficiency into actionable manual-review plans.
```

Recommended fix direction:

```text
1. Add explicit diagnostics to GPU planner round reports:
   - json_ok
   - parse_error
   - repair_attempt_count
   - raw_recommendation_candidate_count
   - filtered_recommendation_count
   - recommendation_count
   - empty_recommendations_reason
   - evidence_ready_for_manual_patch_count

2. If evidence_sufficiency.ready_for_manual_patch_count > 0 and GPU recommendations remain empty, report:
   - empty_recommendations_reason: evidence_ready_but_no_gpu_plan
   - recommended_next_layer: build_agent_review_patch_plan.py

3. Keep fallback patch-plan generation deterministic and manual-review-only.

4. Do not force the GPU planner to invent recommendations. Prefer explicit empty-state diagnostics over hallucinated patch plans.
```

Acceptable end state:

```text
GPU recommendations may still be 0.
But the report must explain why and point to the fallback/manual-review patch-plan layer.
```

## What to send to a master AI after push

After pushing the evidence bundle, send either the branch/PR or these two files:

```text
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
```

Do not send raw `output/**` unless explicitly requested for local-only debugging.
