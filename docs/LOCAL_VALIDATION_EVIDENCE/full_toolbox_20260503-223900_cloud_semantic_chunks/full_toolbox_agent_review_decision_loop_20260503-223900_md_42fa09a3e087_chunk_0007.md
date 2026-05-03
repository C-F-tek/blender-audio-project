# Evidence Chunk 0007/0031

- source: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_20260503-223900.md`
- source_sha256: `42fa09a3e087ebc6b51a8d9d2d501922dd8ed8c400791441877ab803557340fa`
- line_start: `1102`
- line_end: `1448`
- section_kinds: `['markdown_heading_section']`
- previous_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0006.md`
- next_chunk_file: `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_20260503-223900_cloud_semantic_chunks/full_toolbox_agent_review_decision_loop_20260503-223900_md_42fa09a3e087_chunk_0008.md`
- summary_source: `ollama`

## Local chunk summary

**Scopo**: Eseguire il workflow completo di diagnostica GPU/NPU in modalità parallela, raccogliendo prove Git‑trackable e interpretando il problema “gpu_recommendation_count == 0”.  
**Segnali principali**: GPU/Ollama completa molte round di pianificazione ma restituisce zero raccomandazioni; NPU/OpenVINO verifica con successo i checkpoint selezionati; il layer fallback può generare candidati di patch manuali.  
**Guardrail**: Nessuna patch automatica, nessun commit in output/**, nessuna modifica di provider/model senza richiesta, nessuna promozione di output NPU a lane primaria, nessuna

## Context before

  --output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" `
  --markdown-output ".\output\validation\npu_provider_environment_code_refactor_$Stamp.md"
```

Inspect:

```powershell
Get-Content ".\output\validation\npu_provider_environment_code_refactor_$Stamp.json" -Raw |
  ConvertFrom-Json |
  Select-Object passed, provider_execution_performed, patch_application_performed, errors, warnings
```


## Chunk content

````md
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

````

## Context after

## Patch-plan fallback layer

When the GPU planner returns zero recommendations but evidence sufficiency says candidates are ready, use the patch-plan builder as the deterministic/manual-review fallback layer.

Typical command:

```powershell
python .\Tools\ai\build_agent_review_patch_plan.py `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\gpu_planner_nonempty_diagnostics_orchestrator.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --output .\output\patch_specs\agent_review_patch_plan.json `
