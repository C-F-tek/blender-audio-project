# AI Workload Report Quality Gate

This document defines the report/schema contract for the AI workload report quality gate introduced by `P-AI-WORKLOAD-REPORT-QUALITY-GATE`.

The gate is app-agnostic and report-only. It classifies already-generated workload reports before they are used as advisory context by packet/proposal builders.

## Purpose

The gate prevents corrupted or non-linguistic provider output from influencing repository suggestions.

Typical current behavior:

```text
Ollama/GPU/CUDA workload report -> usable_text -> primary advisory context
OpenVINO/NPU workload report -> unusable_output when numeric/hex-like -> excluded from advisory context
```

NPU remains valid as a probe, decode diagnostic, guardrail and knowledge broker. Passing local NPU resource/probe checks does not promote NPU output to primary advisory context.

## Unified launcher requirement

The canonical local-AI entrypoint is:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

When the unified launcher is run with any of these provider/advisory intents:

```text
-Full0To10
-UsePrimaryAdvisoryProvider
provider mode with primary advisory routing
```

then workload quality routing is required unless explicitly disabled by the operator:

```text
-NoWorkloadQuality
```

Required launcher behavior:

```text
real run: build or read output/validation/ai_workload_report_quality.json before primary advisory context is trusted
real run: fail clearly if primary provider routing is requested and the quality report cannot be produced/read
dry run: mark workload quality generation as planned instead of failing on the missing file
manifest: expose workload_quality_report, workload_quality_routing_ok and quality_gate_passed
```

Silent degradation is not allowed. A run must not say primary provider routing is complete while workload quality routing is absent.

## Producer

```text
Tools/validation/check_ai_workload_report_quality.py
```

Default input reports:

```text
output/ai_packets/npu_real_workload_report.md
output/ai_packets/ollama_gpu_real_workload_report.md
```

Default output:

```text
output/validation/ai_workload_report_quality.json
```

## Required command

```powershell
python .\Tools\validation\check_ai_workload_report_quality.py `
  --repo-root . `
  --output .\output\validation\ai_workload_report_quality.json
```

Optional explicit input reports:

```powershell
python .\Tools\validation\check_ai_workload_report_quality.py `
  --repo-root . `
  --report npu=output/ai_packets/npu_real_workload_report.md `
  --report ollama=output/ai_packets/ollama_gpu_real_workload_report.md `
  --output .\output\validation\ai_workload_report_quality.json
```

## Report contract

Required root fields:

```text
schema_version
kind
repo_root
passed
errors
warnings
provider_execution_performed
source_writes_performed
policy
mode
usable_lanes
unusable_lanes
decision
checks
```

Required kind:

```text
ai_workload_report_quality
```

Required policy:

```text
usable_text_lanes_only_for_advisory_context
```

Required mode:

```text
report_only_workload_quality_gate
```

Provider semantics:

```text
provider_execution_performed=false
source_writes_performed=false
```

The quality gate only reads already-generated report text and writes a validation report. It must not call Ollama, OpenVINO, NPU, GPU, Blender or FFmpeg.

## Per-result contract

Each entry under `checks.results` should expose:

```text
path
lane
provider
compute_lane
exists
usable
classification
advisory_use
provider_execution_performed
errors
warnings
metrics
```

Known lane mapping:

```text
ollama -> provider=ollama, compute_lane=gpu_cuda
npu    -> provider=openvino_npu, compute_lane=npu
```

Classification values currently used:

```text
usable_text
unusable_output
missing
```

## Decision block

The `decision` object exposes an aggregate routing decision:

```text
usable_lanes
unusable_lanes
ollama_gpu_primary_advisory_allowed
npu_report_text_usable
npu_excluded_from_primary_advisory
provider_execution_seen
source_writes_performed
routing_policy
```

Expected policy-preserving state when Ollama is usable and NPU output is corrupted:

```text
usable_lanes = ["ollama"]
unusable_lanes = ["npu"]
ollama_gpu_primary_advisory_allowed = true
npu_report_text_usable = false
npu_excluded_from_primary_advisory = true
provider_execution_seen = false
source_writes_performed = false
```

## Manifest visibility contract

The unified launcher manifest must include:

```text
primary_provider_requested
workload_quality_report
workload_quality_routing_ok
quality_gate_passed
phase_reports.workload_quality when generated
phase_status.workload_quality or equivalent status when selected
```

For `-Full0To10`, missing workload quality is acceptable only when the operator explicitly supplies `-NoWorkloadQuality`. Otherwise it is an execution failure for real runs and a planned step for dry runs.

## Advisory routing consumers

Primary consumers:

```text
Tools/ai/workload_quality.py
Tools/ai/build_workload_quality_lane_routing.py
Tools/ai/suggest_repository_updates.py
Tools/ai/build_repository_change_proposals.py
Tools/ai/build_github_evidence_bundle.py
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Routing contract:

```text
known workload report paths fail closed when the quality report is missing/unreadable
non-workload docs may remain trusted if routing is unavailable
unusable NPU workload reports remain visible in routing metadata but are excluded from advisory context
```

## NPU metadata sidecar

`Tools/npu/run_npu_review.py` can optionally emit:

```text
output/validation/npu_review_metadata.json
```

Command without provider loading:

```powershell
python .\Tools\npu\run_npu_review.py `
  --metadata-only `
  --metadata-out .\output\validation\npu_review_metadata.json
```

Required sidecar fields:

```text
schema_version
kind
repo_root
passed
errors
warnings
engine
provider
device
metadata_only
provider_execution_performed
generated_output_written
source_writes_performed
patch_application_performed
advisory_role
quality_gate_required_before_advisory_use
```

Expected metadata-only state:

```text
kind=npu_review_metadata
metadata_only=true
provider_execution_performed=false
generated_output_written=false
quality_gate_required_before_advisory_use=true
```

## Compatibility alias

Some local reports and drift checks may refer to the promotion gate as:

```text
quality_report_required_before_advisory_use
```

This is equivalent to the sidecar field:

```text
quality_gate_required_before_advisory_use
```

Both names mean that workload report quality must be checked before any generated workload text is trusted as advisory context.

## Guardrails

The quality gate must not:

```text
execute providers implicitly
hide unusable workload output
promote NPU/OpenVINO to primary advisory
introduce OpenVINO GPU as a primary lane
change model configuration, temperature, prompt prose or provider orchestration
apply patches
run Blender
edit full analysis JSON
commit SQLite memory DBs
hand-edit generated indexes
```

## Validation block

```powershell
python .\Tools\validation\check_ai_workload_report_quality.py --repo-root . --output .\output\validation\ai_workload_report_quality.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
git diff --check
```

Unified launcher dry-run check:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -DryRun `
  -SkipGitSync `
  -NoBranch `
  -AllowDirty
```
