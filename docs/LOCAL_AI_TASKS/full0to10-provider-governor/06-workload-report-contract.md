# Workload report contract

Una futura run reale deve produrre report validabili.

## Report richiesti

- `ollama_gpu_real_workload_report.md`;
- `full0to10_provider_runtime_telemetry.json`;
- `full0to10_provider_recommendations.json`.

## Validator

```text
Tools/validation/check_ai_workload_report_quality.py --report-dir
```

## Hard fail

- patch application;
- report mancante;
- telemetry mancante;
- output non testuale;
- GPU.0 takeover.
