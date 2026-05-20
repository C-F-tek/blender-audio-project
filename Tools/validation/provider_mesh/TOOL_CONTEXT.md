# Tools/validation/provider_mesh context

## Role

`Tools/validation/provider_mesh` validates provider-lane reports and contracts for GPU, GPU0, NPU, Ollama and OpenVINO-related workflows.

## Responsibilities

- Validate GPU0 companion contracts.
- Validate OpenVINO peer topology reports.
- Validate NPU companion and review reports.
- Validate Ollama gateway reports.
- Validate provider result parsing.
- Validate observable peer activity contracts.

## Representative command surface

Use through the validation dispatcher:

```powershell
python -m Tools.validation check_gpu0_companion_contract ...
python -m Tools.validation check_openvino_peer_topology_contract ...
python -m Tools.validation run_openvino_peer_topology_contract_smoke ...
python -m Tools.validation run_npu_micro_task_companion_smoke ...
python -m Tools.validation run_ollama_tool_gateway_smoke ...
python -m Tools.validation run_gpu_planner_json_contract_smoke ...
python -m Tools.validation check_provider_result_parsing ...
python -m Tools.validation run_observable_peer_activity_contract_smoke ...
```

## Contract model

```text
provider lane report -> parser/contract check -> diagnostic or readiness result
```

## Expected artifacts

```text
GPU0 companion report
OpenVINO topology report
NPU companion report
Ollama gateway report
provider parsing report
observable peer activity report
```

## Boundaries

- Provider availability is not product applicability.
- Provider text remains evidence until checked by product layers.
- Diagnostics should stay explicit when a lane is unavailable or degraded.

## Extension notes

When adding provider report fields, update parser checks and related smoke tests together.
