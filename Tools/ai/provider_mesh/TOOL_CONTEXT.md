# Tools/ai/provider_mesh context

## Role

`Tools/ai/provider_mesh` contains provider-lane tools and diagnostics for local/remote AI execution, GPU/NPU coordination, Ollama/OpenVINO integration and provider evidence reports.

This area is evidence-producing and advisory unless a downstream matrix/code-product stage turns output into validated diff/code.

## Provider lanes

```text
GPU1/Ollama -> primary planning and proposal lane
GPU0/OpenVINO -> reviewer/refiner or companion workload lane
NPU/OpenVINO -> sampled auditor and guardrail lane
CPU/helper -> broker, scanning, validation and composition support
```

## Main responsibilities

- Probe local provider availability and hardware lanes.
- Build GPU/NPU sync and workload reports.
- Run supervised GPU planning and GPU/NPU orchestration.
- Run NPU review/audit helpers.
- Provide Ollama gateway integration.
- Produce provider evidence with explicit guardrails.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m Tools.ai run_local_provider_probe ...
python -m Tools.ai check_local_resource_lanes ...
python -m Tools.ai gpu_deep_planning_supervised ...
python -m Tools.ai gpu_deep_planning_review ...
python -m Tools.ai gpu_npu_parallel_orchestrator ...
python -m Tools.ai npu_gpu_deep_review_auditor ...
python -m Tools.ai ollama_tool_gateway ...
python -m Tools.ai build_openvino_gpu0_workload_report ...
python -m Tools.ai build_openvino_hardware_governance_report ...
python -m Tools.ai provider_mesh_runtime ...
```

## Guardrails

- Provider output is not a code product by itself.
- Provider availability is not proof of proposal quality.
- `provider_execution_performed` must be backed by explicit workload or provider report evidence.
- NPU should remain a sampled audit lane unless a specific contract changes that.
- Provider prompts must use verified context and target allowlists where applicable.
- Path invention and placeholder patches should be blocked downstream.

## Expected artifacts

Typical outputs include:

```text
provider reports
GPU/NPU sync diagnostics
OpenVINO device/workload reports
Ollama gateway reports
peer exchange packets
analysis input bundles
provider error diagnostics
```

## Extension notes

Add new provider behavior in report-only or diagnostic form first. Add validation under `Tools/validation/provider_mesh` before treating a provider lane as product-critical.
