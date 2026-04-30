# Runtime-Safe Provider Result Report Adoption

## Status

active

## Priority

P2

## Context

The app-agnostic local AI/NPU core now has green local reports for:

```text
local_ai_resource_lanes
npu_runtime_output_manifest
provider_result_parsing
local_provider_probe
```

The next controlled step is adopting provider result reports in runtime-adjacent tooling without changing legacy provider execution behavior.

## Scope

Allowed:

```text
parse already-produced provider payloads
parse deterministic simulated provider payloads
write provider_result_report JSON under output/validation or an explicit report-only destination
keep provider_execution_performed accurate
add validators and packet/proposal visibility
```

Not allowed:

```text
execute providers from the legacy runtime path
change prompt prose
change model selection
change temperature or provider parameters
change provider orchestration
change Blender runtime
change Ready To Jazz
edit full analysis JSON
hand-edit generated indexes
```

## Target files

```text
Tools/npu/build_provider_result_report.py
Tools/npu/pipeline/providers.py
Tools/npu/pipeline/reports.py
Tools/validation/check_provider_result_parsing.py
Tools/validation/check_npu_pipeline_modules.py
Tools/npu/pipeline/README.md
docs/JSON_SCHEMAS.md
Tools/ai/build_repository_change_proposals.py
Tools/ai/suggest_repository_updates.py
```

## Validation

```powershell
python .\Tools\validation\check_provider_result_parsing.py --repo-root . --output .\output\validation\provider_result_parsing.json
python .\Tools\npu\build_provider_result_report.py --repo-root . --use-samples --output .\output\validation\provider_result_report.json
python .\Tools\ai\run_local_provider_probe.py --repo-root . --run-ollama --run-npu --output .\output\validation\local_provider_probe.json
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output\ai_packets -Basename npu_provider_adoption_after_tests -ProposalBasename npu_provider_adoption_proposals -ReportFile output\validation\provider_result_parsing.json,output\validation\provider_result_report.json,output\validation\local_provider_probe.json,output\validation\npu_runtime_output_manifest.json,output\validation\local_ai_resource_lanes.json
```

## Stop conditions

Stop if any planned change would:

```text
execute providers from legacy runtime
alter provider execution parameters
alter prompt prose
write outside report-only destinations
modify Blender runtime or generated media scripts
```

## Notes

This plan intentionally separates:

```text
runtime-safe report adoption -> provider_execution_performed=false
explicit local provider probe -> provider_execution_performed=true
```
