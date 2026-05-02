# GPU Repair Failure Recommendation Layer

## Purpose

Document the report-only diagnostic layer for this observed failure mode:

```text
GPU/Ollama provider execution completed
recommendation_count == 0
empty_recommendations_reason == repair_attempt_failed
evidence_ready_for_manual_patch_count > 0
```

The goal is not to force the GPU planner to invent recommendations. The goal is to make this state explicit, auditable and actionable by emitting one deterministic manual-review recommendation that routes reviewers to the fallback patch-plan layer.

## Tool

```text
Tools/ai/build_gpu_repair_failure_recommendation.py
```

## Inputs

```text
orchestrator report JSON
GPU planner report JSON
```

Typical project-complete run inputs:

```text
output/ai_pipeline/project_complete_<STAMP>_orchestrator.json
output/ai_pipeline/project_complete_<STAMP>_parallel_gpu.json
```

## Command

```powershell
python .\Tools\ai\build_gpu_repair_failure_recommendation.py `
  --repo-root . `
  --orchestrator ".\output\ai_pipeline\project_complete_<STAMP>_orchestrator.json" `
  --gpu-report ".\output\ai_pipeline\project_complete_<STAMP>_parallel_gpu.json" `
  --output ".\output\analysis\gpu_repair_failure_recommendation_<STAMP>.json" `
  --markdown-output ".\output\analysis\gpu_repair_failure_recommendation_<STAMP>.md"
```

## Output behavior

When the repair-failure state is detected, the report emits:

```text
kind: gpu_repair_failure_recommendation
recommendation_count: 1
recommendations[0].id: gpu_repair_failure_001
recommendations[0].status: ready_for_manual_review
recommended_next_layer: build_agent_review_patch_plan.py
```

Guardrails stay report-only:

```text
provider_execution_performed=false
patch_application_performed=false
source_writes_performed=false
blender_runtime_execution_performed=false
sqlite_write_performed=false
manual_review_required=true
```

## Why the JSON broke in the reference run

The reference run showed:

```text
GPU/Ollama provider execution: true
round_count: 24
recommendation_count: 0
raw_recommendation_candidate_count: 0
filtered_recommendation_count: 0
json_parse_error_count: 16
empty_recommendations_reason: repair_attempt_failed
evidence_ready_for_manual_patch_count: 12
```

Operational interpretation:

```text
The local provider ran and returned text, but enough rounds failed the strict JSON contract that the repair layer could not recover valid recommendation objects.
The model did not produce parseable recommendation candidates, even though the deterministic evidence layer had ready manual-review candidates.
The correct next layer is therefore the fallback manual-review patch-plan builder, not a forced or hallucinated GPU recommendation.
```

Likely contributing causes to inspect in future work:

```text
prompt too large or too mixed between instructions, evidence and file previews
model returning prose or partially fenced JSON instead of one strict JSON object
model output truncation or malformed escaping in long recommendation fields
local parser not reusing the shared Tools.ai.model_json helper everywhere
post-validation packet currently reporting Ollama used=false in the included evidence, which may hide provider-path expectations for that stage
```

## Future fix direction

Small safe follow-ups:

```text
reuse Tools.ai.model_json.parse_model_json_object in GPU planner parsing paths
add explicit JSON-only prompt footer with a minimal schema example
record first parse error, repair attempt count and raw response preview hash per failed round
emit gpu_repair_failure_recommendation as an input to the compact evidence bundle
```

Do not change provider/model settings until the diagnostic path is validated.
