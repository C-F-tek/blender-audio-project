# Local AI Core Tool Activation

## Status

Current compact contract for using AI workload reports inside local core/tool
activation without promoting diagnostic output into advisory truth.

## AI workload report quality gate

The AI workload report quality gate runs after provider or probe reports exist
and before generated workload text influences packets, proposals or repository
suggestions.

Canonical dispatcher command:

```powershell
python -m Tools.validation check_ai_workload_report_quality --repo-root . --output .\output\validation\ai_workload_report_quality.json
```

Source validator name for compatibility and drift checks:

```text
check_ai_workload_report_quality.py
```

Routing semantics:

```text
Ollama/GPU usable_text -> may enter advisory context
NPU unusable_output -> excluded from advisory context
OpenVINO/NPU metadata-only -> diagnostic sidecar only
```

The gate is report-only. It must not execute providers, write source, apply
patches, promote NPU to advisory text, or make OpenVINO GPU the primary
provider lane.

Required guardrails:

```text
provider_execution_performed=false
source_writes_performed=false
patch_application_performed=false
```

## Activation rule

Local AI core/tool activation may consume workload reports only after the
quality report has classified their lane.

```text
usable_text -> advisory context allowed
unusable_output -> diagnostic evidence only
metadata-only -> diagnostic evidence only
missing quality report for tracked workload -> fail closed
```

This document does not replace the provider-lane contracts. For complete or
full profiles, required lane viability is still governed by:

```text
docs/CORE_LANE_COMPLETENESS_CONTRACT.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
```
