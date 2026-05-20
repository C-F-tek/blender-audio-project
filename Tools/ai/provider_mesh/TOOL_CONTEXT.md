# Tools/ai/provider_mesh context

## Role

`Tools/ai/provider_mesh` contains provider-lane tools and diagnostics for local/remote AI execution, GPU/NPU coordination, Ollama/OpenVINO integration and provider evidence reports.

This area is evidence-producing and advisory unless a downstream matrix/code-product stage turns output into validated diff/code.

It concretizes the provider part of:

```text
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Provider lanes

```text
Ollama / GPU1 -> primary planning, proposal and synthesis lane
GPU0 / OpenVINO -> coworker/reviewer or companion workload lane
NPU / OpenVINO -> microtask auditor and diagnostic guardrail lane
CPU/helper -> broker, scanning, validation and composition support
```

## Main responsibilities

- Probe local provider availability and hardware lanes.
- Build provider analysis input bundles.
- Build peer exchange packets.
- Build GPU0 companion task and workload reports.
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
python -m Tools.ai run_local_provider_probe ...
python -m Tools.ai check_local_resource_lanes ...
python -m Tools.ai runtime_hardware_capability ...
python -m Tools.ai build_analysis_input_bundle ...
python -m Tools.ai peer_exchange_packet ...
python -m Tools.ai gpu_deep_planning_supervised ...
python -m Tools.ai gpu_deep_planning_review ...
python -m Tools.ai replay_gpu_planner_json_contract ...
python -m Tools.ai gpu_npu_parallel_orchestrator ...
python -m Tools.ai npu_gpu_deep_review_auditor ...
python -m Tools.ai ollama_tool_gateway ...
python -m Tools.ai build_openvino_gpu0_workload_report ...
python -m Tools.ai build_gpu0_companion_task_lane ...
python -m Tools.ai run_gpu0_peer_companion_worker ...
python -m Tools.ai build_npu_micro_task_companion_report ...
python -m Tools.ai run_npu_decode_smoke_diagnostic ...
python -m Tools.ai check_npu_provider_environment ...
python -m Tools.ai build_openvino_hardware_governance_report ...
python -m Tools.ai provider_mesh_runtime ...
python -m Tools.ai build_gpu_repair_failure_recommendation ...
```

## Guardrails

- Provider output is not a code product by itself.
- Provider availability is not proof of proposal quality.
- `provider_execution_performed` must be backed by explicit workload or provider report evidence.
- GPU0 is not complete when it only reports device visibility; it must produce observable workload/peer evidence when selected.
- NPU should remain a sampled microtask/audit lane unless a specific compute-provider contract changes that.
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
OpenVINO device/workload reports
GPU0 companion task lane report
GPU0 peer companion worker report
NPU microtask companion report
NPU diagnostic decode report
Ollama gateway reports
hardware capability reports
provider error diagnostics
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
python -m Tools.ai provider_runtime_blackboard ...
python -m Tools.ai provider_runtime_broker_bridge ...
python -m Tools.ai provider_runtime_live_signals ...
python -m Tools.ai provider_runtime_validation_bridge ...
```

## Validation expectations

Relevant validation areas:

```powershell
python -m Tools.validation run_ollama_tool_gateway_smoke ...
python -m Tools.validation check_runtime_hardware_delegation_contract ...
python -m Tools.validation check_openvino_peer_topology_contract ...
python -m Tools.validation run_openvino_peer_topology_contract_smoke ...
python -m Tools.validation check_gpu0_companion_contract ...
python -m Tools.validation run_npu_micro_task_companion_smoke ...
python -m Tools.validation run_npu_tool_request_contract_smoke ...
python -m Tools.validation run_observable_peer_activity_contract_smoke ...
python -m Tools.validation run_provider_empty_response_diagnostics_smoke ...
```

## Extension notes

Add new provider behavior in report-only or diagnostic form first. Add validation under `Tools/validation/provider_mesh` before treating a provider lane as product-critical.