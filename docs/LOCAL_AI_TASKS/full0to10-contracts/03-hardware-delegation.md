# Hardware delegation

Full0To10 deve dichiarare come vengono delegate le lane hardware.

## CPU

La CPU resta responsabile di:

- discovery iniziale;
- CSV/index;
- validation;
- repository consistency;
- bundle building;
- smoke e contract checks.

## GPU/Ollama

La GPU/Ollama è la primary advisory/planning lane per:

- provider diagnostics;
- deep planner;
- recommendation generation;
- discrepancy analysis.

## NPU/OpenVINO

La NPU resta sampled auditor, non lockstep primary lane:

- audit campionato;
- decode/probe diagnostics;
- guardrail;
- classificazione qualità.

## Contratto di parallelismo

Eseguire in parallelo dove possibile, ma senza perdere contabilità:

```text
phase_status
phase_reports
runtime_tool_usage_telemetry
runtime_tool_capability_manifest
full_toolbox_run_telemetry_summary
```

Ogni fase deve restare distinguibile nel bundle finale.
