# AI Workload Report Quality Gate

## Status

Current contract for deciding whether generated workload reports may be used as
advisory context.

This is not a provider runner. It validates already-generated reports and fails
closed when a tracked workload report is missing, unreadable or not usable.

## Canonical command

Use the dispatcher surface:

```powershell
python -m Tools.validation check_ai_workload_report_quality --repo-root . --output .\output\validation\ai_workload_report_quality.json
```

Source validator name for compatibility and drift checks:

```text
check_ai_workload_report_quality.py
```

## Report contract

Required report kind:

```text
ai_workload_report_quality
```

The report must preserve these guardrails:

```text
provider_execution_performed=false
source_writes_performed=false
patch_application_performed=false
```

Policy:

```text
usable_text_lanes_only_for_advisory_context
quality_report_required_before_advisory_use
quality_gate_required_before_advisory_use
```

Compatibility alias:

```text
quality_report_required_before_advisory_use
```

means the same routing rule as:

```text
quality_gate_required_before_advisory_use
```

## Lane routing

Allowed advisory source:

```text
Ollama/GPU/CUDA usable_text -> advisory context allowed
```

Excluded or diagnostic source:

```text
OpenVINO/NPU unusable_output -> advisory context excluded
metadata-only -> not advisory text
```

NPU metadata can be recorded as:

```text
npu_review_metadata
metadata_only=true
generated_output_written=false
```

The metadata sidecar does not promote NPU to advisory text. It only records
that a quality gate is required before advisory use.

## Failure policy

Tracked workload reports fail closed:

```text
missing report -> fail closed
unreadable report -> fail closed
metadata-only report -> excluded from advisory text
unusable_output -> excluded from advisory text
```

This gate proves only advisory-context quality. It does not prove provider
execution, product readiness, patch applicability or full runtime success.
