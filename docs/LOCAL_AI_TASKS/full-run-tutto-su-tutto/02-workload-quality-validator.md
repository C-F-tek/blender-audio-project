# Workload quality validator

`Tools/validation/check_ai_workload_report_quality.py` valida report workload
testuali.

## Input supportati

- `--report-dir`;
- `--report lane=path`;
- `--include-missing-known-reports`.

## Report noti

- `ollama_gpu_real_workload_report.md`;
- `npu_real_workload_report.md`.

## Policy

Il validator è report-only:

```text
provider_execution_performed=false
patch_application_performed=false
source_writes_performed=false
persistent_memory_write_performed=false
```

Il report NPU può essere utile come evidence, ma non promuove NPU a primary
advisory lane.
