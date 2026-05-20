<!-- IA-CARMINE-MD-SPLIT: part -->
# JSON_SCHEMAS — parte 002 di 002

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## AI workload report quality

```text
File pattern:
output/validation/ai_workload_report_quality.json
Producer:
Tools/validation/ai_workload/report_quality/cli.py
Consumer:
Tools/ai/_shared/workload_quality.py and workload-aware proposal/report builders.
Required fields:
schema_version, kind, repo_root, passed, errors, warnings, provider_execution_performed, source_writes_performed, policy, mode, usable_lanes, unusable_lanes, decision, checks
Required kind:
ai_workload_report_quality
Required policy:
usable_text_lanes_only_for_advisory_context
Provider semantics:
The report validates already-generated workload reports and must keep provider_execution_performed=false.
Notes:
Each checks.results entry may expose path, lane, provider, compute_lane, exists, usable, classification, advisory_use, provider_execution_performed, errors, warnings and metrics.
Ollama/GPU/CUDA reports can enter advisory context only when classified usable_text.
OpenVINO/NPU reports classified unusable_output are excluded from advisory context.
```

## NPU review metadata

```text
File pattern:
output/validation/npu_review_metadata.json
Producer:
python -m Tools.npu run_npu_review --metadata-out
Consumer:
workload-gate reviewers, validation report contract checks and local AI handoffs.
Required fields:
schema_version, kind, repo_root, passed, errors, warnings, engine, provider, device, metadata_only, provider_execution_performed, generated_output_written, source_writes_performed, patch_application_performed, advisory_role, quality_gate_required_before_advisory_use
Required kind:
npu_review_metadata
Provider semantics:
metadata_only=true means no provider was loaded, no generated review text was written and provider_execution_performed=false.
Notes:
A metadata sidecar does not make NPU advisory. It records that quality_gate_required_before_advisory_use is true before advisory_use is allowed.
```

<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END id=det_doc_doc_002:docs-json_schemas.md -->
