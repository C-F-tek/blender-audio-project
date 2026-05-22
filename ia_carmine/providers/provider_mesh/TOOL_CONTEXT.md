# ia_carmine/providers/provider_mesh context

## Role

`ia_carmine/providers/provider_mesh` contains provider-lane tools and diagnostics for local/remote AI execution, GPU/NPU coordination, Ollama/OpenVINO integration and provider evidence reports.

This area is evidence-producing and advisory unless a downstream matrix/code-product stage turns output into validated diff/code.

It concretizes the provider part of:

```text
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Provider lanes

```text
Ollama / GPU1 -> primary planning, proposal and synthesis lane
GPU0 / Ollama Vulkan -> coworker/reviewer or companion workload lane
NPU / OpenVINO -> microtask auditor and diagnostic guardrail lane
CPU/helper -> broker, scanning, validation and composition support
```

CPU/helper is not a provider lane. Complete run-unica evidence accepts only
GPU1/Ollama with `ollama ps` accelerator residency proof, GPU0/Ollama Vulkan
with verified peer workload, and NPU/OpenVINO on `NPU`. OpenVINO `CPU`,
OpenVINO GPU0 fallback, heuristic fallback and CPU-only/unproven Ollama
residency are diagnostic-only and must classify the run as blocked/unviable
when complete provider evidence is required.

Canonical run-unica requests GPU1 full model-layer offload with
`--ollama-gpu-layers all`. This is not a GPU-card count; it maps to
`options.num_gpu=-1` only at the Ollama API edge. A mixed `ollama ps` line such
as `36%/64% CPU/GPU` means part of the model is resident in system memory. In a
complete run-unica provider profile this blocks GPU1 unless non-strict auto
selection repairs the lane with a smaller installed model that proves
`100% GPU`.

## Main responsibilities

- Probe local provider availability and hardware lanes.
- Build provider analysis input bundles.
- Build peer exchange packets.
- Build GPU0 Ollama/Vulkan companion task and peer workload reports.
- Build NPU microtask companion/audit reports.
- Build GPU/NPU sync and workload reports.
- Run supervised GPU planning and GPU/NPU orchestration.
- Run NPU review/audit helpers.
- Provide Ollama gateway integration.
- Produce provider evidence with explicit guardrails.
- Report runtime hardware capability and degraded/unavailable states.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m ia_carmine.cli run_local_provider_probe ...
python -m ia_carmine.cli check_local_resource_lanes ...
python -m ia_carmine.cli runtime_hardware_capability ...
python -m ia_carmine.cli build_analysis_input_bundle ...
python -m ia_carmine.cli peer_exchange_packet ...
python -m ia_carmine.cli gpu_deep_planning_supervised ...
python -m ia_carmine.cli gpu_deep_planning_review ...
python -m ia_carmine.cli replay_gpu_planner_json_contract ...
python -m ia_carmine.cli gpu_npu_parallel_orchestrator ...
python -m ia_carmine.cli npu_gpu_deep_review_auditor ...
python -m ia_carmine.cli ollama_tool_gateway ...
python -m ia_carmine.cli build_ollama_gpu0_peer_report ...
python -m ia_carmine.cli ensure_ollama_role_models ...
python -m ia_carmine.cli ensure_openvino_npu_model ...
python -m ia_carmine.cli ensure_provider_role_coexistence ...
python -m ia_carmine.cli build_gpu0_companion_task_lane ...
python -m ia_carmine.cli run_gpu0_peer_companion_worker ...
python -m ia_carmine.cli build_npu_micro_task_companion_report ...
python -m ia_carmine.cli check_npu_provider_environment ...
python -m ia_carmine.cli build_openvino_hardware_governance_report ...
python -m ia_carmine.cli provider_mesh_runtime ...
python -m ia_carmine.cli build_gpu_repair_failure_recommendation ...
```

## Guardrails

- Provider output is not a code product by itself.
- Provider availability is not proof of proposal quality.
- `provider_execution_performed` must be backed by explicit workload or provider report evidence.
- Provider reports must expose `provider_backend`, `provider_compute_device`,
  `provider_device_verified` and `cpu_provider_fallback_performed`.
- Provider-capable Python is a repository contract, not a generic example:
  `$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path`,
  `$env:IA_CARMINE_PYTHON = $RepoPy`, `$env:PYTHONPATH = (Resolve-Path .).Path`.
  When the active checkout has no `.venv`, verify the machine-specific
  provider Python before writing commands. On the current workstation, the
  available provider-capable Python is
  `C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe`;
  keep `PYTHONPATH` pointed at the checkout being validated.
- `check_local_resource_lanes` is not a static file read. Even when
  `provider_execution_performed=false`, it is a resource/provider preflight
  that may touch Ollama service state or OpenVINO device enumeration. Its
  reports must expose `resource_mechanics_performed=true` and
  `resource_probe_performed=true` when lane checks run.
- GPU0 is not complete when it only reports device visibility; it must produce observable Ollama/Vulkan peer evidence when selected.
- GPU0 native model/tool-loop timeout is provider failure in complete run-unica mode; OpenVINO GPU0/tensor workload alone is diagnostic.
- GPU0 must use Ollama/Vulkan. OpenVINO GPU0 is not a full/complete lane fallback; OpenVINO `GPU.1` is reserved for Ollama/CUDA and must not receive GPU0 workload.
- GPU0/Intel selection must not rely on Windows Task Manager numbering. On the IA-Carmine workstation Windows shows Intel as GPU 0 and NVIDIA as GPU 1, while Vulkan may enumerate NVIDIA as index 0 and Intel as index 1. GPU0/Ollama Vulkan must select the Intel integrated device by Vulkan identity (`vendorID=0x8086`, Intel name/device UUID) and set `GGML_VK_VISIBLE_DEVICES` to that resolved Vulkan index.
- `ensure_ollama_role_models` proves GPU1 and GPU0 are simultaneously alive on their
  separate Ollama servers, then unloads both by default.
- `ensure_openvino_npu_model` proves the NPU micro lane by loading the OpenVINO
  GenAI model on `NPU`, running the compact tool-loop probe, then releasing the
  child process so model memory is not held after the check.
- `ensure_provider_role_coexistence` proves GPU1 Ollama, GPU0 Ollama/Vulkan and
  NPU OpenVINO are alive during the same runtime window before unloading or
  exiting all three provider roles.
- In full provider runtime handoff mode, GPU1 and GPU0 Ollama models stay
  resident through the provider production cycle. A lane subprocess may finish
  and be joined, but model unload and GPU0 `11435` shutdown are final cleanup
  operations so provider lanes can call back into each other across revisions.
- NPU should remain a sampled microtask/audit lane unless a specific compute-provider contract changes that; NPU provider evidence must be OpenVINO `NPU`, not CPU fallback.
- NPU native model/tool-loop timeout is provider failure in complete run-unica mode; device enumeration or micro-preflight alone is diagnostic.
- Provider prompts must use verified context and target allowlists where applicable.
- Path invention and placeholder patches should be blocked downstream.
- Provider agreement does not bypass CPU validators or product boundaries.

## Expected artifacts

Typical outputs include:

```text
provider reports
provider analysis input bundle
peer exchange packet
GPU/NPU sync diagnostics
Ollama/OpenVINO device reports
GPU0 Ollama/Vulkan companion task lane report
GPU0 Ollama/Vulkan peer report
NPU microtask companion report
triple provider role coexistence report
Ollama gateway reports
hardware capability reports
repair recommendation reports
```

## Relationship to runtime blackboard

Provider reports become operationally useful when materialized into blackboard/exchange surfaces:

```text
provider_mesh report
-> provider_runtime_blackboard
-> broker/live/validation bridge reports
-> heap/exchange evidence
-> product or blocked classification
```

Use:

```powershell
python -m ia_carmine.cli provider_runtime_blackboard ...
python -m ia_carmine.cli provider_runtime_broker_bridge ...
python -m ia_carmine.cli provider_runtime_live_signals ...
python -m ia_carmine.cli provider_runtime_validation_bridge ...
```

## Validation expectations

Relevant validation areas:

```powershell
python -m Tools.validation run_ollama_tool_gateway_smoke ...
python -m Tools.validation check_runtime_hardware_delegation_contract ...
python -m Tools.validation run_ollama_sdk_adapter_smoke ...
python -m Tools.validation check_openvino_peer_topology_contract ...
python -m Tools.validation run_openvino_peer_topology_contract_smoke ...
python -m Tools.validation check_gpu0_companion_contract ...
python -m Tools.validation run_npu_micro_task_companion_smoke ...
python -m Tools.validation run_npu_tool_request_contract_smoke ...
python -m Tools.validation run_observable_peer_activity_contract_smoke ...
```

## Extension notes

Add new provider behavior as real provider evidence first. Add validation under `Tools/validation/provider_mesh` before treating a provider lane as product-critical.
